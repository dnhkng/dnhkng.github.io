---
title: "2x GH200 for LLM inference, Part 4: DeepSeek V4 Flash - SGLang vs vLLM at 1M context"
categories: [LLMs, workstations]
tags: [llm, nvidia, hopper, gh200, vllm, sglang, deepseek, benchmark]
---

## Introduction

[Part 1](/posts/gh200-benchmarking/) measured this dual GH200 workstation as a memory system. [Part 2](/posts/gh200-benchmarking-part-2/) used those numbers on the **preview** DeepSeek V4 Flash checkpoint, where the interesting/painful part was getting multi-token prediction to run at all: a hand-written vLLM O-projection fallback, a config-propagation fix, and a narrow upstream PR. [Part 3](/posts/gh200-benchmarking-part-3-glm52/) then took the box to its limit with GLM-5.2 and expert offload.

Series:

1. [Memory paths for LLM inference](/posts/gh200-benchmarking/)
2. [vLLM, DeepSeek V4 Flash/Pro, and MTP](/posts/gh200-benchmarking-part-2/)
3. [GLM-5.2, expert offload, and the CPU question](/posts/gh200-benchmarking-part-3-glm52/)
4. DeepSeek V4 Flash released, DSpark, and SGLang vs vLLM

This is the follow-up I wanted to Part 2, which was benchmarking a *preview* release. DeepSeek has now shipped the GA release (*General Availability release*), with **DeepSeek-V4-Flash-0731**. The speculative-decode path is no longer a manual MTP graft: the release ships **DSpark**, DeepSeek's semi-autoregressive speculative-decoding module, as a first-class vLLM method. It is faster, and it serves the **full 1,048,576-token context with no CPU offload**. After tuning vLLM as far as it would go, I brought up **SGLang** on the same box to see whether ~276 tok/s was DeepSeek's ceiling or vLLM's. After fixing a silent loader bug that was degrading the draft model, and with some upstream help SGLang was faster on every decode workload I tested.

***TL;DR:***
> On this dual GH200 box, you build **vLLM** `v0.26.0` from source, add the merged DSV4 cache-layout patch (PR #48993), disable async scheduling, and run DSpark at 6 predicted tokens to give: *~276 decode tok/s* and a 1M context in 192 GB of HBM. **SGLang**, once it built on ARM64 and it's DSpark loader bug fixed, is faster on every decode workload and hits *~317.0 tok/s*.

## The System Reminder

Same machine as the rest of the series, so I'll keep it short:

| Component        |                                   Spec |
| ---------------- | -------------------------------------: |
| GPUs             |       2x GH200 Hopper, 96 GB HBM3 each |
| CPUs             |                2x Grace, 72 cores each |
| Host memory      | 480 GB LPDDR5X per Grace, 960 GB total |
| GPU local memory |                       192 GB total HBM |
| CUDA             |                                   13.0 |
| PyTorch          |                         `2.11.0+cu130` |
| OS               |                  Ubuntu 24.04, aarch64 |

And the topology facts from [Part 1](/posts/gh200-benchmarking/) still govern everything: ~3.7 TB/s local HBM, ~377 GB/s local Grace-to-Hopper, and only ~58 GB/s on the staged Hopper-to-Hopper path. Every deployment decision below reduces to the same rule: keep the hot bytes local, and avoid the cross-GPU path.

## What changed since Part 2

Two things:

- **The DeepSeek checkpoint arrived, to much acclaim.** `DeepSeek-V4-Flash-0731`, 155.43 GiB on disk as vLLM reports it. The `compress_ratios` metadata has 5 uncompressed entries, 21 C4 entries, and 20 C128 entries. The main model uses the first 43; the rest are the draft/spec layers.
- **MTP upgraded to DSpark.** In Part 2, multi-token prediction had to be patched into vLLM to run at all. The released checkpoint ships [DSpark](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-DSpark), DeepSeek's *Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation* (public implementation in [DeepSpec](https://github.com/deepseek-ai/DeepSpec)). Operationally it replaces the preview MTP config: you pass `{"method":"dspark","num_speculative_tokens":6}` and vLLM routes it through some of the same draft-model and `mtp.*` plumbing (it converts the draft to a `DSparkDraftModel` while some stored weights keep MTP names). It is a distinct decoding method, not a renamed MTP mode, so the Part 2 hand-wiring is replaced by a single flag.

> Note: the released model has a **DSpark block size of 5**, which makes any `num_speculative_tokens < 5` invalid. 

## Building vLLM v0.26.0 on this system needs patching

I built from the exact `v0.26.0` tag (commit `568afb3a1`), CUDA 13.0, `TORCH_CUDA_ARCH_LIST=9.0a` for Hopper. The one thing the stable tag is missing is a **DeepSeek V4 KV-cache fix that merged *after* the release**: [vllm-project/vllm#48993](https://github.com/vllm-project/vllm/pull/48993), *"Compact MXFP4 indexer KV cache and packed group overlays."*

Without it, v0.26.0 uses the older padded cache-group layout and wastes memory across DSV4's heterogeneous compressed-cache and compressor-state groups. With it, the layout gets dense:

1. an MXFP4 indexer row is sized at 68 bytes instead of reserving a 132-byte FP8 row;
2. each DSV4 cache group is laid out densely in a per-block slab, overlaying groups whose block-ID namespaces are independent;
3. the now-unneeded cross-group sliding-window page padding is removed.

That is merged upstream behaviour (~12% more available blocks on their GB200 config), not a local hack; it just landed after the tag. Practical rule: **use v0.26.0 plus PR #48993, or a later release that already contains it.**

## The TorchVision version pin

Pin a matching PyTorch/TorchVision pair *even for a text-only model*: vLLM's global kernel warmup imports the MiniMax M3 processor regardless of what you serve, so the text-only DSV4 server failed at startup with `ModuleNotFoundError: No module named 'torchvision'`. Installing the *latest* TorchVision then gave an ABI mismatch (`operator torchvision::nms does not exist`); the fix was the version matched to PyTorch 2.11:

```bash
uv pip install --no-deps 'torchvision==0.26.0'
```

The validated pair is PyTorch `2.11.0+cu130` and TorchVision `0.26.0+cu130`.

## Avoiding the incorrect 26.33 GiB OOM failure

My first no-offload launch used `max_num_batched_tokens=32768` and, after loading 74.85 GiB per GPU, refused to start:

```text
26.33 GiB KV cache is needed
3.57 GiB KV cache memory is available
estimated maximum model length is 8884
```

That is odd: the published 1M-token KV estimate for this model is about 10 GiB. The 26 GiB figure is real but misleading. The mechanism:

```python
max_in_flight_tokens = max_concurrent_batches * max_num_batched_tokens
```

At `max_num_batched_tokens=32768`, vLLM quietly enabled **async scheduling**, which sets `max_concurrent_batches = 2`. So the scheduler reserved transient state for **65,536 in-flight tokens**. DeepSeek V4 carries substantial FP32 compressor state for its C4 and C128 layers, and those sliding-window state caches are sized against the *in-flight* limit, not against `max_model_len`. At a big scheduler batch, that compressor-state reservation dominates startup admission.

So the 26.33 GiB was scheduler-dependent compressor state plus padding plus profiling, **not** the compressed model KV. The official vLLM [DeepSeek V4 write-up](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-04-24-deepseek-v4.md) puts a 1M-token BF16 DSV4 KV cache at about 9.62 GiB, and once the transient state is controlled, the machine agrees with that. Reducing `max_model_len` would have hidden the problem rather than fixing it, and pointed toward CPU offload that is not needed here.

## The single-user fix

For a single-user code workload, the correct move is to stop paying for concurrency I'm not using:

```text
max_num_batched_tokens=8192
max_num_seqs=1
no_async_scheduling=true
```

An 8K scheduler chunk still processes a 32K code prompt in four chunks; for one request at a time, the lower transient reservation is worth more than async overlap. CUDA graphs stay **on**: earlier measurements on this host showed `--enforce-eager` collapses decode, so eager was not a candidate.

With that config at a 65,536-token context, no-spec startup reported:

```text
Available KV cache memory: 12.67 GiB
GPU KV cache size:         303,419 tokens
Maximum concurrency for 65,536 tokens: 4.63x
```

One caution before dividing bytes by tokens against the 1M numbers below: vLLM's reported token capacity is request-shape-aware, not a flat byte-per-token conversion. At 65K, DSV4's fixed per-request compressor-state reservation dominates the calculation, an effective ~44 KB/token. At 1M, that same overhead is amortised across the much longer context and approaches the ~6.5 KB/token marginal long-context cost. Same box, same fixed state, different average.

## DSpark results, the k-sweep

8K-token code prompt, code-review generation, up to 2048 output tokens, medians of three runs:

| DSpark `k` |       Median TG | Median TPOT | Note                            |
| ---------: | --------------: | ----------: | ------------------------------- |
|          0 |      92.9 tok/s |    10.76 ms | Baseline, no spec               |
|          4 |             n/a |         n/a | **Invalid**, below block size 5 |
|          5 |     268.2 tok/s |     3.73 ms | Valid                           |
|      **6** | **275.9 tok/s** | **3.62 ms** | **Best**                        |
|          7 |     262.2 tok/s |     3.81 ms | Valid                           |
|          8 |     216.3 tok/s |     4.62 ms | Regression                      |
|         10 |     223.9 tok/s |     4.47 ms | Regression                      |

`k=6` is **2.97x** the no-spec decode rate and about 3% ahead of `k=5`. The Part 2 MTP lesson still holds: deeper is not free, and past the sweet spot the extra draft depth stops paying for itself and TG falls off. There is also a hard floor: because the checkpoint's DSpark block size is 5, `k=4` is rejected outright rather than merely slow.

That sweep is code review, which has high draft acceptance. Open-ended prose does not, and it is the workload the SGLang comparison later uses too, so it needs a vLLM baseline. On five fixed story prompts (temperature 0, up to 1,024 tokens, the same five proposals), vLLM's median was **156.2 tok/s** (151.1-159.4 range), well below the code-review figure because DSpark acceptance is workload-dependent. That 156.2 is the number the SGLang story-chat rows compare against.

## Prefill

Uncached prefill (unique nonce per prompt so nothing is served from prefix cache, see the note below), no spec:

| Requested tokens | Actual prompt tokens | Median TTFT | Prefill rate |
| ---------------: | -------------------: | ----------: | -----------: |
|            2,048 |                2,070 |     0.291 s |  7,112 tok/s |
|            8,192 |                8,214 |     0.941 s |  8,725 tok/s |
|           32,768 |               32,789 |     3.176 s | 10,323 tok/s |

Spec decoding costs a little prefill throughput (the draft path adds work), but since the real workload is long code-review *generation*, the decode win dominates.

> **Benchmark hazard worth repeating:** my first harness reused an identical prompt, so runs 2 and 3 were served from vLLM's prefix cache and reported a misleading 25K-80K prefill tok/s. Prepending a unique run nonce invalidates the first cache block and forces real prefill on every repeat. If you benchmark prefill on a repeated prompt, you are measuring cache reuse, not prefill.

## Full 1M context, no offload

Part 2's V4 Pro needed CPU expert offload just to fit. The released Flash does not. With DSpark `k=6`, the final server holds the full context in HBM:

```text
Model allocation:        79.15 GiB per GPU
Available KV cache:      8.28 GiB per GPU
GPU KV cache size:       1,371,214 tokens
Max concurrency @ 1M:    1.31x
```

That 8.28 GiB into 1.37M tokens works out to ~6.5 KB/token, the amortised long-context marginal cost from the single-user section, which lines up with the ~9.62 GiB BF16 1M estimate once FP8 KV and the compact cache layout are in play. At `k=6` the margin was narrow. At `gpu-memory-utilization 0.95` it missed by about 300 MB:

```text
KV cache needed:    7.63 GiB
KV cache available: 7.33 GiB
```

> Bumping utilization to `0.96` supplied exactly the margin.

This is why the released Flash suits this box better than the preview did: it turns "juggle weights across the slow bridge" back into "keep everything local," which is exactly the regime Part 1 said this machine wants.

## The vLLM launcher

Genericised (swap in your own model path):

```bash
python -m vllm.entrypoints.cli.main serve \
  /path/to/DeepSeek-V4-Flash-0731 \
  --served-model-name dsv4-0731 \
  --tokenizer-mode deepseek_v4 \
  --trust-remote-code \
  --distributed-executor-backend mp \
  --tensor-parallel-size 2 \
  --max-model-len 1048576 \
  --max-num-batched-tokens 8192 \
  --max-num-seqs 1 \
  --block-size 256 \
  --gpu-memory-utilization 0.96 \
  --kv-cache-dtype fp8 \
  --disable-custom-all-reduce \
  --no-async-scheduling \
  --speculative-config \
  '{"method":"dspark","num_speculative_tokens":6,"draft_sample_method":"greedy"}'
```

Plus the host-specific NCCL / FlashInfer-sampler / TileLang / DeepGEMM / allocator env from earlier posts. No `--enforce-eager`, no CPU/UVA offload.

## The remaining problem: TileLang latency spikes

vLLM is tuned, the 1M context is validated, *and it works*. The one problem that did not go away is TileLang runtime compilations, which causes havoc on serving the model. When I went to test the system in a chat, I was hitting latency of over 10 seconds! The mHC kernels compile *during serving*, so on a 100-request run the median TTFT is fine (~0.28 s) **but p99 rises to ~11.5 s**: occasionally a live request stalls for ten-plus seconds while TileLang compiles a shape it had not warmed. Swapping the mHC kernels for a PyTorch/Triton fallback flattens p99 to ~2.6 s *but costs about 65% of decode*, so within vLLM the choice is a poor one: keep the throughput and accept the tail stalls, or remove the stalls and give back most of the decode speedup.

This will *probably* be solved upstream; it is fundamentally a warmup-coverage problem, and each release compiles more shapes before serving. For now the vLLM setup here is a working solution, tail spikes and all. But I was finding it too painful to actually use as a daily driver.

## SGLang, now that it runs on ARM64

Back when I wrote Parts 2 and 3, SGLang was not a candidate on this machine: it did not build cleanly on aarch64, so the series has been vLLM (and llama.cpp) by necessity, not by preference, as RadixAttention is pretty great and speeds up 'real-world' inferencing. **SGLang now has real ARM64 support**, so it runs on this GH200 box. I brought it up natively: the upstream Dockerfile handles ARM now, skips the missing `sgl-flash-attn3` cubins, and JITs them at runtime instead. Both GPUs come up at compute capability 9.0. After a few fixes, SGLang beat the tuned vLLM config on every decode workload I tested.

### Fixing the silent shared-expert loader bug
Even with widths matched and Marlin selected, SGLang's draft acceptance was poor and it looked far slower than vLLM. The only hint was a log warning:

```text
DSpark V4 draft: unexpected weight 'mtp.X.ffn.shared_experts...'
```

SGLang's DSpark loader mapped the 256 routed experts but never remapped `mlp.shared_experts` into the fused expert slot (256), so every draft stage ran with a missing shared expert. Not enough to crash, but enough to make the draft propose badly. My local remapping of `.mlp.shared_experts.` to `.mlp.experts.256.` took story decode from 115.7 to 176.0 tok/s and lifted code-review acceptance from ~1.3-1.8 accepted tokens to ~3.5-5.05.

After that, the routine tuning: Marlin for the packed MXFP4 experts (SGLang's `auto` can select backends that mis-handle these weights on Hopper), full decode CUDA graphs at batch 1/2/4, and persistent TileLang/Triton caches mounted at the real roots (`/root/.tilelang`, `/root/.triton`, not just `/root/.cache`), which cut repeat MHC prewarm from ~110 s to ~5 s.

Here the results of these fixes, against the same tuned vLLM numbers from above. The vLLM prefill column is no-spec, which favours vLLM slightly since the draft path adds prefill work:

| Workload                        |   Tuned vLLM |   SGLang (fixed) | SGLang delta |
| ------------------------------- | -----------: | ---------------: | -----------: |
| 2K prefill                      |  7,113 tok/s |      6,927 tok/s |        -2.6% |
| 8K prefill                      |  8,725 tok/s | **10,262 tok/s** |   **+17.6%** |
| 32K prefill                     | 10,323 tok/s |     10,297 tok/s |        -0.3% |
| 8K code review (5 proposals)    |  268.2 tok/s |  **317.0 tok/s** |   **+18.2%** |
| 8K code review (vLLM tuned k=6) |  275.9 tok/s |  **317.0 tok/s** |   **+14.9%** |
| Story chat                      |  156.2 tok/s |  **178.5 tok/s** |   **+14.2%** |

### Upstream improved on the fix

Of course, I should have looked into pull requests first... [SGLang PR #33276](https://github.com/sgl-project/sglang/pull/33276), now merged, excludes the bundled DSpark `stages.*` parameters from target-model NVFP4 conversion so the draft's source MXFP4 weights and scales load under the correct metadata. [PR #33312](https://github.com/sgl-project/sglang/pull/33312), still open at the time of this update, fixes the deeper shared-expert policy problem: target, NextN, and DSpark now resolve the same fusion policy, and the loader only maps the shared expert into the fused slot when fusion is actually enabled. That is structurally better than my unconditional remap.

PR #33312 has a small issue on my GH200 system: it defaults to separate shared experts, and my first 12K warmup attempt at `--mem-fraction-static 0.96` did not fit. Explicit `--enforce-shared-experts-fusion` kept the original memory setting and was slightly faster, so the early throughput comparison used it. That option converts the checkpoint's FP8 shared expert into the fused FP4 path, however. Once the memory and chunking policy had been retuned, the checkpoint-native FP8 layout fit and retained almost all of the speed. That is the quality-first default used below; fused FP4 remains an explicitly named optional performance profile. PR #33276 was effectively throughput-neutral on this Marlin checkpoint (its value is correct weight classification), while #33312 is the change that fixes the shared-expert layout consistently.

This required some experimental testing: I rebuilt four isolated images to separate my patch from the upstream work. These are three-run medians for code and five-prompt medians for story chat, using the same prompts throughout:

| SGLang build and policy                |     Code review |      Story chat |
| -------------------------------------- | --------------: | --------------: |
| Original local fix                     | **317.0 tok/s** |     178.5 tok/s |
| Local fix + merged PR #33276           |     316.0 tok/s |     182.7 tok/s |
| PR #33312 only, explicitly fused       |     309.1 tok/s | **191.4 tok/s** |
| PR #33276 + #33312, explicitly fused   |     311.4 tok/s |     188.9 tok/s |
| PR #33276 + #33312, native FP8 (final) |     308.6 tok/s |     182.8 tok/s |

> This shows that DeepSeek v4 Flash's DSpark head is fine-tuned for Code! The prediction head is closer to the main model's outputs when inferencing on code, and so we get a higher acceptance and speed.

My original patch remains the fastest code row, but the combined upstream native-FP8 build is the one I have deployed. It preserves the checkpoint's shared-expert precision, remains 11.9% faster than the separately tuned vLLM `k=6` code result, and does not depend on silently converting the FP8 shared expert to FP4. I would prefer not to slightly degrade the model for a miniscule increase in speed.

### The matched tail test

The earlier version of this post called SGLang's tail unmeasured. It is measured now. I ran the combined upstream build through the exact vLLM workload: 100 sequential requests, an 8,000-character prompt averaging 1,569 tokens, 64 generated tokens, concurrency one, and temperature zero.

| Runtime                                |    TTFT p50 |    TTFT p90 |    TTFT p99 | Latency p99 |     Decode-only |
| -------------------------------------- | ----------: | ----------: | ----------: | ----------: | --------------: |
| **SGLang #33276 + #33312, native FP8** |     0.284 s |     0.324 s | **0.426 s** | **0.737 s** | **261.2 tok/s** |
| **SGLang #33276 + #33312, fused**      | **0.260 s** | **0.297 s** | **0.388 s** | **1.036 s** | **237.1 tok/s** |
| vLLM TileLang                          |     0.279 s |     0.307 s |    11.564 s |    11.842 s |     222.2 tok/s |
| vLLM PyTorch/Triton mHC fallback       |     0.419 s |     0.460 s |     2.635 s |     3.549 s |      73.9 tok/s |

Both SGLang profiles completed all 100 requests without a live compile, JIT, OOM, or unexpected shared-expert event in the server log. The native-FP8 run is the apples-to-apples comparison with vLLM and had the better decode and end-to-end p99 in these particular runs.

### Optimising SGLang PP to 1M context

Testing showed the system could handle the full 1M context, but prompt processing was uncomfortably slow at 895.4-seconds with the necessary 1,024-token prefill chunk size.

Prompt processing speed in partially determined by the chunk size: Short prompts want a larger 12,288-token chunk because it avoids extra full-model continuation passes; extremely long prompts need progressively smaller chunks so the indexer workspace does not consume the memory reserved for weights and KV cache. I added a small adaptive policy to the scheduler. This is a local patch: stock SGLang has no such knob, so the environment variables below only exist on a build that carries it, and it is the piece of this setup I would most like to propose upstream. The policy:

- keep the configured 12,288-token chunk for ordinary prompts;
- cap the first long-context chunk at 8,192 tokens once the request exceeds 65,536 tokens;
- then reduce the chunk approximately as `738,197,504 / current_context_tokens`;
- align down to 256 tokens, with a 1,280-token floor.

That retains the fast short-prompt path while shrinking only when the accumulated context makes the DSV4 workspace dangerous. The 1,280-token floor was the fastest safe setting in this experiment; it also gives the runtime materially fewer iterations than the original fixed-1K workaround.

| SGLang 1M policy                        | Shared expert  |        Actual prompt |        TTFT |    Prefill rate |
| --------------------------------------- | -------------- | -------------------: | ----------: | --------------: |
| Fixed 1,024-token chunk                 | Fused FP4      |     1,048,523 tokens |     895.4 s |     1,171 tok/s |
| Adaptive, 1,280-token floor             | Fused FP4      |     1,048,523 tokens |     370.4 s |     2,831 tok/s |
| **Adaptive, 1,280-token floor (final)** | **Native FP8** | **1,048,535 tokens** | **358.1 s** | **2,928 tok/s** |

Measured cleanly (not as a warm serve after a 1M request), the final native-FP8 profile reached 9,915 tok/s at 8K, 10,220 tok/s at 32K, 308.6 tok/s on the code-review workload, and a 182.8 tok/s median across five 1,024-token story generations. Those prefill rates sit a little below the original 65K-context table above, because this single server configuration now also holds the full 1M context; the maximum-context validation and the speed tests use the same launcher.

### The SGLang launchers

The quality-first SGLang launcher essentials are:

```bash
--tp-size 2
--mem-fraction-static 0.96
--context-length 1048576
--max-total-tokens 1053184
--max-running-requests 1
--chunked-prefill-size 12288
--max-prefill-tokens 12288
--attention-backend dsv4
--disable-custom-all-reduce
--cuda-graph-bs-decode 1
--speculative-algorithm DSPARK
--speculative-num-draft-tokens 6   # = five actual proposals
--speculative-moe-runner-backend marlin
--moe-runner-backend marlin
--warmups prefill_shapes
```

The adaptive scheduler (the local patch above) is configured with:

```bash
SGLANG_DSV4_ADAPTIVE_PREFILL=1
SGLANG_DSV4_ADAPTIVE_PREFILL_TOKEN_PRODUCT=738197504
SGLANG_DSV4_ADAPTIVE_PREFILL_MIN_CHUNK=1280
SGLANG_DSV4_ADAPTIVE_PREFILL_ALIGNMENT=256
SGLANG_DSV4_ADAPTIVE_PREFILL_LONG_REQUEST_THRESHOLD=65536
SGLANG_DSV4_ADAPTIVE_PREFILL_LONG_REQUEST_MAX_CHUNK=8192
```

Plus `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, `SGLANG_DSV4_MHC_PREWARM_WORKERS=8`, and persistent TileLang/Triton cache mounts. There is deliberately no `--enforce-shared-experts-fusion` in the default. I keep this as one launch script for the quality-first profile; the fused-FP4 variant is a second, explicitly named script that adds `--enforce-shared-experts-fusion` and nothing else.

## Series Takeaway

| Goal                              | Best answer from the series                                                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Understand the box                | Two fast GH200 modules joined by a much slower bridge, keep hot traffic local                                                                  |
| Fast local serving, preview       | DeepSeek V4 Flash Canada-Quant + hand-patched MTP (Part 2)                                                                                     |
| **Recommended SGLang, up to 32K** | **Upstream fixes, native-FP8 shared experts, adaptive prefill; ~309 tok/s code, ~183 story (a superseded FP4 local-patch build reached ~317)** |
| **vLLM 1M context**               | **vLLM v0.26.0 + PR #48993, DSpark k=6, entirely in HBM**                                                                                      |
| **SGLang 1M context**             | **Validated at 1,048,536 total tokens; adaptive chunks, ~360-second full prefill**                                                             |
| Largest vLLM model tested         | GLM-5.2 INT4 + strict local-NUMA expert offload + MTP graft (Part 3)                                                                           |
| CPU-only huge model               | GLM-5.2 IQ2 works, but only single-digit decode (Part 3)                                                                                       |
