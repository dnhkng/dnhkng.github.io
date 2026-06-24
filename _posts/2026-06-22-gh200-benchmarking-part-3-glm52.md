---
title: "2x GH200 for LLM inference, Part 3: GLM-5.2, expert offload, and the CPU question"
categories: [LLMs, workstations]
tags: [llm, nvidia, hopper, gh200, vllm, glm, benchmark]
---

## Introduction

[Part 1](/posts/gh200-benchmarking/) measured the dual GH200 workstation as a memory system. [Part 2](/posts/gh200-benchmarking-part-2/) used those measurements to explain why DeepSeek V4 Flash can be fast in vLLM when the model layout fits the hardware: keep hot weights in HBM, avoid unnecessary Hopper-to-Hopper traffic, and use MTP only where the acceptance rate pays for the draft work.

GLM-5.2 starts at **2.39 output tok/s** on this machine and after a lot of grinding finishes near **50 output tok/s**. That is the whole post in one line. Two moves close the gap: stop the model crossing between the two GH200 modules, then graft an FP8 MTP head onto the INT4 base. Together they take a model that *doesn't fit in VRAM* and serve it at a usable interactive speed.

That gap exists because GLM-5.2 is ***too damn big***. It doesn't fit in HBM, so the Grace memory (*luckily, I have 960 GB LPDDR5X*) has to become part of the serving system. The question jumps in difficulty from *how do I split the model over two Hoppers across a slow interconnect* and becomes to the harder: *how do I split it over two Grace-Hopper modules and juggle the transfer of weights into two separate sets of VRAM?*

The short version from my current measurements is below. **TG** means token generation/decode throughput. **PP** means prompt processing/prefill throughput.

| Model artifact            | Engine                        |                                   Headline batch-1 TG |                         Stable batch-4 TG |             Best PP-heavy result |
| ------------------------- | ----------------------------- | ----------------------------------------------------: | ----------------------------------------: | -------------------------------: |
| GLM-5.2-FP8               | vLLM, TP2, expert UVA offload |                             25.66 output tok/s (best) |              23.63 aggregate output tok/s |               543.66 total tok/s |
| GLM-5.2-AWQ-INT4          | vLLM, TP2, expert UVA offload | 43.39 output tok/s median at `2048->512`, MTP-3 graft | 54.92 aggregate output tok/s, MTP-3 graft |               781.00 total tok/s |
| GLM-5.2 GGUF `UD-IQ2_XXS` | llama.cpp / ik_llama.cpp CPU  |          3.13-3.65 output tok/s short, 1.72-3.62 long |                                not tested | 62.88 pp tok/s with ik_llama.cpp |

The FP8 and AWQ batch-1 MTP headline numbers are from `2048->512` runs. The FP8 MTP-3 point had a 25.64 output tok/s warm mean and 25.66 best sample. The AWQ batch-1 number is now the median of a longer cold-plus-10-warm repeat run, not the best single warm sample. The AWQ batch-4 number is the controlled MTP-3 concurrency result; MTP-4 reached a higher median, but was not repeatable enough to make the headline.

Wait, ***why did I test a slow-ass CPU version too?***  A plausible local-agent architecture is GLM-5.2 on CPU for slower planning, review, or difficult decisions, paired with a much faster DeepSeek V4 Flash instance on GPU for the high-volume path. In commercial-model terms, that is the local version of an Opus/Sonnet style split: *a slower stronger model for the hard calls, and a fast model for the bulk of the work*.  Unfortunately, although it works in practice, it's too damn slow.

## The System Reminder

The machine is still the same dual Grace Hopper workstation:

| Component        |                                   Spec |
| ---------------- | -------------------------------------: |
| GPUs             |        2x Hopper H100, 96 GB HBM3 each |
| CPUs             |                2x Grace, 72 cores each |
| Host memory      | 480 GB LPDDR5X per Grace, 960 GB total |
| GPU local memory |                       192 GB total HBM |
| CUDA             |                                   13.0 |
| Driver           |                             580.105.08 |
| OS               |                  Ubuntu 24.04, aarch64 |

The [topology numbers from Part 1](/posts/gh200-benchmarking/) remain the useful mental model:

| Path                              | Measured bandwidth |
| --------------------------------- | -----------------: |
| Local HBM                         |   about 3,700 GB/s |
| Local Grace LPDDR to local Hopper | about 377-380 GB/s |
| Remote Grace LPDDR to Hopper      |     about 133 GB/s |
| Hopper to Hopper staged copy      |   about 57-58 GB/s |

The model does not fit cleanly in HBM, so decode performance depends on how much expert traffic goes over Grace-to-Hopper C2C, and whether each Hopper is reading from its own local Grace memory rather than the remote module.

## A Bandwidth Guestimate

Before measuring vLLM, I wanted a simple guestimate: if the model is split cleanly across both GH200 modules, and each Hopper streams only the active experts from its own local Grace memory, how fast should decode be without MTP?

From the FP8 checkpoint headers, the routed expert weights are about 684 GiB across 76 MoE layers. GLM-5.2 has 256 routed experts per MoE layer and activates 8 experts per token per MoE layer, so each token touches 8 / 256 = 1 / 32 of the routed expert pool. That makes the active expert stream about 684 GiB / 32 = 21.38 GiB per generated token if those experts are fetched from CPU memory every time. This is only the active expert stream, not the whole checkpoint and not the dense attention path.

The optimistic bandwidth math is:

| Assumption                                          |                           Effective expert stream |                        Bandwidth path | Estimated non-MTP decode |
| --------------------------------------------------- | ------------------------------------------------: | ------------------------------------: | -----------------------: |
| One module effectively serializes the stream        |                                   21.38 GiB/token |    377-380 GB/s local Grace to Hopper |              15-18 tok/s |
| Two modules split the layers, no pipeline overlap   | 10.69 GiB/token per module, two sequential stages |    377-380 GB/s local Grace to Hopper |              15-18 tok/s |
| Two modules split the layers, ideal steady pipeline |                        10.69 GiB/token per module |    377-380 GB/s local Grace to Hopper |    30-36 tok/s aggregate |
| Offloaded experts are interleaved or remote         |                        21.38 GiB/token equivalent | about 133 GB/s remote Grace to Hopper |            about 6 tok/s |
| Traffic falls onto the staged Hopper-to-Hopper path |                        21.38 GiB/token equivalent |                      about 57-58 GB/s |          about 2-3 tok/s |

The expert sizes are in GiB while the measured bandwidths are in decimal GB/s. Converting GiB to GB adds a factor of about 1.074 to the byte stream, so this mismatch makes the table slightly conservative. The ranges are wide enough that it does not change the conclusion.

This is deliberately a bandwidth ceiling, ignoring routing overhead, attention, dense layers, synchronization, kernel efficiency, page placement mistakes, and the fact that a single request does not automatically fill a two-stage pipeline. If a strict local-NUMA run lands near 15-18 tok/s batch-1, the system is behaving like the active experts are being streamed over C2C. If it lands near 2-6 tok/s, the layout is probably paying remote-memory or cross-module traffic, and we have messed up our settings.

## What I Tested

I tested three local vLLM artifacts, two from HuggingFace, and one Frankenstein I built during this project:

| Model                         | Location                                                                      | Notes                                                                                                 |
| ----------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **zai-org/GLM-5.2-FP8**       | [GLM-5.2-FP8](https://huggingface.co/zai-org/GLM-5.2-FP8)                     | Official FP8-style artifact, 754B-class MoE, MTP tensors present                                      |
| **cyankiwi/GLM-5.2-AWQ-INT4** | [cyankiwi/GLM-5.2-AWQ-INT4](https://huggingface.co/cyankiwi/GLM-5.2-AWQ-INT4) | AWQ INT4 artifact, loads through compressed-tensors / Marlin WNA16                                    |
| AWQ + FP8 MTP graft           | cyankiwi/GLM-5.2-AWQ-INT4-MTP-FP8                                             | Local experimental graft: AWQ base model plus FP8 layer-78 MTP tensors from the official FP8 artifact |

The INT4 checkpoint changes the byte count a lot, but probably not the token generation speed quite so much. A crude half-byte-per-weight expert-stream estimate would put the same ideal local-memory ceiling roughly around twice the FP8 ceiling. In practice, INT4 is not just a smaller byte stream: Marlin/AWQ kernel costs, dequantization, graph capture, and vLLM placement all add up.

*The first FP8 baseline was awful*: **2.39 output tok/s**. It was mostly a placement problem, with transfers of weights crossing between GH200 modules.

After switching to strict local NUMA placement and reducing the amount of expert offload until the HBM/KV tradeoff stopped improving, the practical non-MTP batch-1 result was:

| Config                                          | Shape        |             Result |
| ----------------------------------------------- | ------------ | -----------------: |
| TP2, offload 270 GiB/rank, non-MTP              | 1 x 256->512 | 20.31 output tok/s |
| TP2, offload 260 GiB/rank, non-MTP, maxlen 3072 | 1 x 256->512 | 20.53 output tok/s |

The `260 GiB` point is technically fastest, but it only works by reducing max context to 3,072. For a general launcher, I would not use it. The safer FP8 non-MTP point is `270 GiB` expert offload with a 4,096-token max context.

That 20 tok/s result is tip: it is above the simple serialized 15-18 tok/s estimate. The likely interpretation is we are getting partial overlap across the two GH200 modules: not the ideal 30-36 tok/s steady pipeline, but clearly better than a fully serialized expert stream.

For short prompts, MTP was much less exciting than it was for DeepSeek V4 Flash, where we saw big bumps in performance.:

| Config                                      | Shape        |             Result |
| ------------------------------------------- | ------------ | -----------------: |
| non-MTP, offload 300 GiB/rank, batched 2048 | 1 x 256->512 | 19.33 output tok/s |
| MTP-1, offload 300 GiB/rank, batched 1024   | 1 x 256->512 | 18.43 output tok/s |
| MTP-1, offload 300 GiB/rank, batched 2048   | 1 x 256->512 | 21.22 output tok/s |
| MTP-1, offload 300 GiB/rank, batched 4096   | 1 x 256->512 | 19.09 output tok/s |
| MTP-2, offload 300 GiB/rank, batched 2048   | 1 x 256->512 |  8.87 output tok/s |

Even MTP-1 is only a small win. It reached 21.22 output tok/s, which is 9.8 percent faster than the matched 300 GiB non-MTP placement, but only 4.5 percent faster than the best practical 270 GiB non-MTP placement. The draft layer is not free, and enabling it forces a different HBM/offload tradeoff.

However, that short-prompt result was not the whole story. With a more realistic `2048->512` batch-1 workload and a 4096 scheduled-token cap, the optimum moved upward:

| Spec tokens | Shape         | Cold output tok/s | Warm output tok/s | Warm acceptance | Decision          |
| ----------: | ------------- | ----------------: | ----------------: | --------------: | ----------------- |
|       MTP-1 | 1 x 2048->512 |             22.60 |      21.94, 22.72 |    86.50-97.30% | Baseline          |
|       MTP-2 | 1 x 2048->512 |             18.68 |      23.78, 23.00 |    82.22-87.17% | Better than MTP-1 |
|       MTP-3 | 1 x 2048->512 |             24.23 |      25.61, 25.66 |          93.58% | Best measured     |
|       MTP-4 | 1 x 2048->512 |             21.62 |      25.48, 16.48 |    47.59-89.06% | Unstable, stop    |

I stopped there rather than running MTP-5. The rule was to walk upward and stop when the curve got worse. MTP-4 produced one good warm run and then collapsed on the second warm run, with acceptance falling to 47.59 percent and output throughput falling to 16.48 tok/s.

For concurrent token generation, MTP is still a disaster in the measured setup:

| Config                        | Shape        |                       Result |
| ----------------------------- | ------------ | ---------------------------: |
| MTP-1, offload 300 GiB/rank   | 4 x 256->512 | 15.15 aggregate output tok/s |
| non-MTP, offload 270 GiB/rank | 4 x 256->512 | 23.63 aggregate output tok/s |

So I would not make MTP the default concurrent-serving profile for FP8. It is a batch-1 latency/throughput knob, and the best speculative depth depends on prompt length and output shape. The FP8 headline PP-heavy result came from a separate non-MTP run:

| Config                                  | Shape        | Output tok/s | Total tok/s | Prompt-processing snapshot |
| --------------------------------------- | ------------ | -----------: | ----------: | -------------------------: |
| non-MTP, offload 270 GiB/rank, PP-heavy | 4 x 2048->64 |        16.47 |      543.66 |         624.5 prompt tok/s |

## INT4: Faster, But With A Different Tradeoff

The AWQ INT4 model was the better vLLM serving target on this machine.

It loads as `compressed-tensors`, and vLLM selected Marlin WNA16 kernels for both linear and MoE paths. In the first serving sweep, the best measured dual-GH200 batch-1 decode was:

| Workload                 | Output tok/s | Total tok/s |     TPOT |
| ------------------------ | -----------: | ----------: | -------: |
| 256->512, concurrency 1  |        24.70 |       37.06 | 37.39 ms |
| 256->1024, concurrency 1 |        26.16 |       32.70 | 37.67 ms |
| 2048->64, concurrency 1  |        17.61 |      581.22 | 37.94 ms |

The best measured throughput profile was:

| Workload     | Output tok/s | Total tok/s | Mean TPOT |
| ------------ | -----------: | ----------: | --------: |
| 4 x 256->512 |        36.98 |       55.47 | 103.79 ms |
| 4 x 2048->64 |        23.67 |      781.00 | 114.32 ms |

That made the INT4 artifact the practical vLLM choice even before MTP. It was faster than FP8 in every measured comparable serving shape.

Originally, the tradeoff was MTP. The INT4 checkpoint itself does not include the MTP layer-78 weights, so MTP startup fails before we get to any acceptance-rate question.

## AWQ + FP8 MTP Graft

To test whether GLM-5.2's MTP head was actually useful, I made a local experimental graft: keep the AWQ INT4 base model, add the FP8 layer-78 MTP tensors from the official FP8 artifact, merge the safetensors index, and patch vLLM so the draft layer can use the FP8 quantization path while the base model stays on AWQ/Marlin. This is not a clean official checkpoint, but it answers the systems question.

To make that reproducible without redistributing a full merged model, I published a small delta repo: [dnhkng/GLM-5.2-AWQ-INT4-FP8-MTP-delta](https://huggingface.co/dnhkng/GLM-5.2-AWQ-INT4-FP8-MTP-delta). It contains only the `model.layers.78.*` MTP tensors extracted from `zai-org/GLM-5.2-FP8`, plus `graft_glm52_awq_mtp.sh`. The delta is 1,569 tensors from the FP8 MTP layer, not a replacement for the AWQ checkpoint. The intended workflow is:

```bash
./graft_glm52_awq_mtp.sh \
  --awq-dir /path/to/GLM-5.2-AWQ-INT4 \
  --mtp-delta-dir /path/to/GLM-5.2-AWQ-INT4-FP8-MTP-delta \
  --out-dir /path/to/GLM-5.2-AWQ-INT4-MTP-FP8
```

The script leaves the AWQ weights unchanged, adds the FP8 MTP layer tensors, updates `model.safetensors.index.json`, and adds `mtp_quantization_config` to `config.json` so vLLM can route the draft layer through the FP8 quantization path while keeping the base model on AWQ/Marlin.

The required vLLM changes were small but specific: allow an MTP-only quantization override in the DeepSeek/GLM decoder layer, read that override from a local `mtp_quantization_config`, and skip missing mixed-quantization parameter names while loading the grafted AWQ/FP8 checkpoint. Without the MTP-only FP8 quantization override, the graft loaded but acceptance was effectively zero.

The answer is: yes, MTP helps the AWQ path a lot when it is wired up correctly. For the short-shape comparison below, I re-ran the non-MTP AWQ baseline in the same benchmark setup as the grafted model, which is why these baseline values are a little higher than the earlier general serving sweep. Use these re-measured non-MTP rows for the MTP improvement percentages; the earlier 24.70 and 26.16 tok/s rows are from the first broader INT4 serving sweep, not the controlled graft comparison.

| Profile     |     Shape | Cold output tok/s |       Warm output tok/s | Warm TPOT | Acceptance |
| ----------- | --------: | ----------------: | ----------------------: | --------: | ---------: |
| AWQ non-MTP |  256->512 |             25.77 | 26.61-26.63, mean 26.62 |  36.51 ms |        n/a |
| AWQ + MTP-1 |  256->512 |             26.96 | 37.29-41.79, mean 38.82 |  24.72 ms |     98.58% |
| AWQ non-MTP | 256->1024 |           not run | 26.94-26.95, mean 26.95 |  36.58 ms |        n/a |
| AWQ + MTP-1 | 256->1024 |           not run | 37.81-38.08, mean 37.95 |  25.81 ms |     98.84% |

The first MTP request still pays first-shape JIT overhead. In the cold 256->512 MTP run, TTFT was 4.17 seconds and the log showed Triton JIT compilation for slot mapping, prefill metadata, EAGLE/MTP input preparation, and rejection sampling kernels. After that, TTFT returned to roughly 0.59 seconds and the steady decode path sat around 38-39 output tok/s.

The very high acceptance rates here are from these synthetic benchmark prompts. Real agent prompts and structured continuations may have lower acceptance, so the short-shape 41-46 percent gain should be treated as a measured benchmark result, not a guaranteed application-level speedup.

I then repeated the speculative-depth sweep with a stricter rule: one cold run plus ten warm runs, no discarded noisy samples, and prompt lengths from `256->512` up to `8192->512`. The server used `MAX_MODEL_LEN=9216`, `MAX_NUM_BATCHED_TOKENS=9216`, `MAX_NUM_SEQS=1`, `TP_SIZE=2`, `CPU_OFFLOAD_GB=170`, expert UVA offload, local NUMA binding, and FP8 MLA KV cache.

The practical comparison is MTP-3 versus MTP-4:

| Profile     |     Shape | Runs | Median output tok/s |   Min |   Max |   P10 |   P90 |    CV | Median TPOT | Median acceptance | Sub-60 acceptance runs |
| ----------- | --------: | ---: | ------------------: | ----: | ----: | ----: | ----: | ----: | ----------: | ----------------: | ---------------------: |
| AWQ non-MTP |  256->512 |   11 |               25.15 | 23.94 | 25.19 | 25.12 | 25.18 | 0.014 |    38.62 ms |               n/a |                      0 |
| AWQ non-MTP | 2048->512 |   11 |               24.03 | 24.01 | 24.05 | 24.02 | 24.05 | 0.001 |    39.31 ms |               n/a |                      0 |
| AWQ non-MTP | 4096->512 |   11 |               23.06 | 23.02 | 23.09 | 23.05 | 23.07 | 0.001 |    39.41 ms |               n/a |                      0 |
| AWQ non-MTP | 8192->512 |   11 |               21.36 | 21.24 | 21.38 | 21.33 | 21.37 | 0.002 |    39.46 ms |               n/a |                      0 |
| AWQ + MTP-3 |  256->512 |   11 |               47.27 | 34.50 | 55.06 | 36.35 | 52.09 | 0.136 |    20.01 ms |            92.16% |                      1 |
| AWQ + MTP-3 | 2048->512 |   11 |               43.39 | 33.32 | 56.72 | 34.43 | 46.13 | 0.147 |    20.66 ms |            91.48% |                      2 |
| AWQ + MTP-3 | 4096->512 |   11 |               42.97 | 40.37 | 48.33 | 40.39 | 46.46 | 0.061 |    19.23 ms |            96.95% |                      0 |
| AWQ + MTP-3 | 8192->512 |   11 |               35.69 | 27.17 | 38.78 | 28.82 | 38.11 | 0.105 |    20.58 ms |            94.03% |                      1 |
| AWQ + MTP-4 |  256->512 |   11 |               45.77 | 36.79 | 70.02 | 38.29 | 61.83 | 0.211 |    20.69 ms |            74.61% |                      2 |
| AWQ + MTP-4 | 2048->512 |   11 |               46.87 | 32.31 | 63.55 | 35.86 | 57.28 | 0.196 |    18.96 ms |            84.83% |                      2 |
| AWQ + MTP-4 | 4096->512 |   11 |               45.97 | 36.47 | 54.68 | 37.29 | 48.72 | 0.108 |    17.71 ms |            92.20% |                      0 |
| AWQ + MTP-4 | 8192->512 |   11 |               29.58 | 22.77 | 43.13 | 27.12 | 42.02 | 0.204 |    26.19 ms |            56.37% |                      6 |

This changes the AWQ story again. MTP-4 is not just "interesting but noisy"; it fails as a default. It has excellent best-case rows, including 70.02 output tok/s on one short synthetic prompt, but under longer prompts the tail is ugly. At `8192->512`, six of eleven MTP-4 runs fell below 60 percent acceptance, and the worst warm run dropped to 22.77 output tok/s, essentially back near non-MTP speed.

MTP-3 is not magic either. It had prompt-sensitive low-acceptance rows, including two sub-60 percent acceptance runs at `2048->512` and one at `8192->512`. But its lower tail is better, its coefficient of variation is lower, and it stays clearly above non-MTP in all tested batch-1 shapes. For real use on this system, the launcher default is now the MTP-3 `stable` profile with `MAX_MODEL_LEN=635904`. The `9216` value in these tests is the benchmark/scheduler token budget used for the `8192->512` sweep, not the production context limit.

I also repeated the `2048->512` test with true concurrency, using `MAX_NUM_SEQS=4`. These are aggregate output throughput numbers:

| Profile     |     Shape | Concurrency | Runs | Median output tok/s |   Min |   Max |   P10 |   P90 |    CV | Median TPOT | Median acceptance |
| ----------- | --------: | ----------: | ---: | ------------------: | ----: | ----: | ----: | ----: | ----: | ----------: | ----------------: |
| AWQ + MTP-3 | 2048->512 |           2 |   11 |               47.92 | 41.87 | 60.64 | 42.39 | 58.85 | 0.129 |    34.65 ms |            80.33% |
| AWQ + MTP-3 | 2048->512 |           4 |   11 |               54.92 | 48.45 | 63.96 | 50.71 | 58.87 | 0.076 |    60.86 ms |            77.42% |
| AWQ + MTP-4 | 2048->512 |           2 |   11 |               50.50 | 35.08 | 67.81 | 41.22 | 63.48 | 0.186 |    32.31 ms |            81.02% |
| AWQ + MTP-4 | 2048->512 |           4 |   11 |               57.17 | 49.54 | 67.83 | 49.70 | 67.01 | 0.111 |    56.51 ms |            72.21% |

The concurrency result is a useful sanity check. MTP-4 still has higher headline medians, but the same tail problem remains. At concurrency 2 it had a warm run with only 46.24 percent acceptance and 35.08 aggregate output tok/s, below the MTP-3 p10. At concurrency 4 it was faster on median, but acceptance was lower and variance was higher. That is not the kind of repeatability I want in a default launcher.

I also ran a small fixed-prompt sanity check with four prompts: coding review, GH200 systems reasoning, blog summarization, and benchmark design. This is not as strong as the full synthetic sweep, because it is only two runs per profile, but it is useful for checking whether synthetic random-token acceptance is too optimistic:

| Profile     | Runs | Median output tok/s |   Min |   Max | Median TPOT | Median acceptance |
| ----------- | ---: | ------------------: | ----: | ----: | ----------: | ----------------: |
| AWQ + MTP-3 |    2 |               35.44 | 34.81 | 36.07 |    25.99 ms |            62.73% |
| AWQ + MTP-4 |    2 |               36.07 | 35.40 | 36.74 |    26.84 ms |            56.55% |

That result makes the caveat concrete. Real prompts drove acceptance much lower than the synthetic runs for both profiles. MTP-4 was only marginally faster on median output throughput and had lower median acceptance, so it still does not justify replacing MTP-3 as the default.

This is very different from the FP8 result. FP8 MTP-1 was only a narrow batch-1 win, and it lost badly for concurrent token generation. The AWQ graft has a much better ratio: the draft layer is cheap enough, and accepted often enough, that MTP-3 roughly halves TPOT versus the non-MTP baseline in the controlled batch-1 tests.

The caveat is important: the base `cyankiwi` AWQ artifact still does not ship usable MTP weights, so everything above depends on a local graft plus local vLLM patches for mixed AWQ/FP8 loading. The delta repo makes the graft reproducible, but this is still a systems experiment, not an official merged model release.

## Context Capacity

With the speed settings locked-down, the last thing was to optimise the context length. I tested the AWQ + FP8 MTP graft as a context-capacity profile with `MAX_NUM_SEQS=2`, `GPU_UTIL=0.90`, `CPU_OFFLOAD_GB=170`, `kv_cache_dtype=fp8_ds_mla`, and CUDA graph memory profiling enabled. By varying the context size, and using the remaining VRAM to triangulate, I was able to quickly optimise the launch flags:

| Setting                                        |         Result |
| ---------------------------------------------- | -------------: |
| MAX_MODEL_LEN                                  | 635,904 tokens |
| MAX_NUM_SEQS                                   |              2 |
| Reported available KV cache memory             |      32.42 GiB |
| Reported GPU KV cache size                     | 635,904 tokens |
| Reported maximum concurrency at 635,904 tokens |          1.00x |

## Single GH200 Did Not Work Yet

I also tried to make the INT4 artifact run through vLLM on one GH200 module.

| Config                                                      | Result                                                                        |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `cpu_offload_gb=330`, `max_model_len=4096`, `gpu_util=0.90` | Model loaded, then KV init failed with `Available KV cache memory: -0.38 GiB` |
| `cpu_offload_gb=350`, `max_model_len=2048`, `gpu_util=0.95` | Worker died during startup before the detailed Python error was captured      |

This vLLM + AWQ artifact path is close enough to the edge that I do not want to describe single-GH200 serving as supported. It may be fixable with a different offload path, a smaller quant, or a vLLM-side startup fix, but I do not have a clean result yet.

## The CPU/GGUF Result

The most hopeful follow-up was CPU serving. I *really* wanted to have GLM5.2 do the slow heavy planning on CPU and have DeepSeek v4 Flash on GPU do the legwork.

Unsloth has a GLM-5.2 GGUF repo with llama.cpp examples and several quantization levels. The public size table lists:

| Quant        | Listed size |
| ------------ | ----------: |
| `UD-IQ2_XXS` |      238 GB |
| `UD-Q3_K_M`  |      343 GB |
| `UD-Q4_K_M`  |      466 GB |
| `UD-Q5_K_M`  |      561 GB |
| `Q8_0`       |      801 GB |
| BF16         |     1.51 TB |

The dual Grace side has 960 GB of LPDDR5X. A 2-bit or 3-bit GGUF should fit entirely in CPU memory, and even Q4_K_M is plausible. If llama.cpp can run GLM-5.2 at a few tokens per second on CPU while leaving both Hoppers free, that unlocks the ultimate fast/slow combo from the intro on a single box:

| Role                  | Model             | Hardware     |
| --------------------- | ----------------- | ------------ |
| Fast worker           | DeepSeek V4 Flash | dual Hoppers |
| Slow planner/reviewer | GLM-5.2 GGUF      | Grace CPUs   |

I started with `UD-IQ2_XXS`, a severely lobotomised model, because the question is *will this work*, not whether it's smart. The result is yes, but only with careful placement:

| Engine               | Quant      | Threads / NUMA                 | Prompt | Output |          PP |         TG |
| -------------------- | ---------- | ------------------------------ | -----: | -----: | ----------: | ---------: |
| llama.cpp 063d9c1    | UD-IQ2_XXS | node1 bind/membind, 72 threads |    256 |    128 |  9.65 tok/s | 3.13 tok/s |
| llama.cpp 063d9c1    | UD-IQ2_XXS | node1 bind/membind, 72 threads |   2048 |    128 |  3.87 tok/s | 3.62 tok/s |
| ik_llama.cpp 6c00e87 | UD-IQ2_XXS | node1 bind/membind, 72 threads |    256 |    128 | 51.54 tok/s | 3.65 tok/s |
| ik_llama.cpp 6c00e87 | UD-IQ2_XXS | node1 bind/membind, 72 threads |   2048 |    128 | 62.88 tok/s | 1.72 tok/s |

The memory footprint was about 234 GiB RSS. Both GPUs remained free.

The `ik_llama.cpp` result is worth separating from the serving conclusion. It is dramatically faster at prompt processing on this GGUF, and for a long-prompt batch it cut wall time from roughly eighteen minutes in my upstream llama.cpp run to under two minutes, but it did not improve the steady token stream. In the 2048-token prompt test, decode fell to 1.72 tok/s (*defo in the **useless** range*).

| Placement          | Threads |   Shape |          PP |         TG |
| ------------------ | ------: | ------: | ----------: | ---------: |
| node0 bind/membind |      72 | 256->32 | 14.95 tok/s | 1.42 tok/s |
| node1 bind/membind |      72 | 256->32 | 13.45 tok/s | 4.30 tok/s |
| interleave 0,1     |     144 | 256->32 | 11.79 tok/s | 0.63 tok/s |
| default            |     144 | 256->32 | 11.11 tok/s | 0.62 tok/s |

*For this GGUF and llama.cpp build, using both Grace CPUs was much worse than binding to node1.*

## Current Takeaways

The bandwidth guestimate turned out to be a useful ruler. The simple FP8 no-MTP ceiling suggested that a well-placed local-memory run should land around 15-18 output tok/s for a serialized batch-1 stream, with an *optimistic* two-module steady pipeline closer to 30-36 tok/s aggregate. The measured FP8 non-MTP result, **about 20 output tok/s**, *is above the serialized estimate*: I speculate the two GH200 modules appear to get some cross-module pipeline overlap, landing between the no-overlap and ideal-overlap rows, or I have messed up the math.

The measured INT4 result is consistent with the same byte-rate story, just messier. Plain AWQ runs in the low-to-mid 20s output tok/s across the controlled `256->512` through `8192->512` sweep — better than FP8 in every comparable shape, but well short of the clean 2x the smaller byte stream might suggest, because AWQ/Marlin execution, dequantization, CUDA graph capture, vLLM scheduling, and MoE routing all eat into the savings. The *real win* comes from the hacky-graft: bolting on MTP-3 lifts the practical batch-1 default into the low 40s (43.39 tok/s median at `2048->512`) and reaches 54.92 aggregate output tok/s at concurrency 4. MTP-4 has faster best-case samples, but the acceptance collapses documented above keep it out of the default.

### Worst to Best
The footprint values are approximate model-weight footprints from the artifacts and checkpoint headers: about 1.51 TB for BF16, about 833 GiB for the FP8 artifact, and about 430 GiB for the AWQ artifact.

| Configuration                                 | Approx footprint |                      Representative result | What changed                                                                          |
| --------------------------------------------- | ---------------: | -----------------------------------------: | ------------------------------------------------------------------------------------- |
| BF16 full weights                             |          1.51 TB |                                    not run | Does not fit in 960 GB Grace memory                                                   |
| FP8, naive placement                          |         ~833 GiB |                          2.39 output tok/s | Cross-module transfers kill the run                                                   |
| FP8, strict local-NUMA offload                |         ~833 GiB |                         20.31 output tok/s | Placement alone gives about an 8.5x speedup                                           |
| FP8 + MTP-3, workload-tuned                   |         ~833 GiB |                         25.66 output tok/s | Speculation helps when the shape is right                                             |
| AWQ INT4, plain                               |         ~430 GiB |   24.03 output tok/s median at `2048->512` | Smaller stream and better base serving target                                         |
| AWQ INT4 + grafted FP8 MTP head, MTP-3 stable |         ~430 GiB | 43.39 tok/s single; 54.92 at concurrency 4 | Same base footprint; the gain comes from the graft, MTP-3, and high enough acceptance |

## Series Takeaway

Across the three posts, the useful deployment map is:

| Goal                      | Best answer from the series                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| Understand the box        | Treat it as two fast GH200 modules joined by a much slower bridge             |
| Fast local serving        | DeepSeek V4 Flash Canada-Quant, MTP benchmarked, stable profile first         |
| Largest vLLM model tested | GLM-5.2 INT4 with strict local-NUMA expert offload and experimental MTP graft |
| CPU-only huge model       | GLM-5.2 IQ2 works, but only at low single-digit decode                        |
| Main hardware rule        | Keep hot traffic local to each GH200 module                                   |
