---
title: "2x GH200 for LLM inference, Part 2: vLLM, DeepSeek V4 Flash, and MTP"
date: 2026-06-08
categories: [LLMs, workstations]
tags: [llm, nvidia, hopper, gh200, vllm, benchmark]
---

## Introduction

A while back I did some optimisation on my [Hopper system](/posts/vllm-optimization-gh200/) for MiniMax M2.1, and this was followed by some deeper [GH200 benchmarking](/posts/gh200-benchmarking/), where I measured the machine as a memory-shuffling system. The result was a simple topology map: each Hopper has fast local HBM, each Hopper has a fast NVLink C2C path to its own Grace CPU, and the path between the two Hoppers is not a normal GPU peer link. Cross-GPU traffic on this workstation stages through the CPU side and is much slower than local HBM or local C2C.

This is that follow-up (*massively delayed by a much cooler project*). The workload here is ***DeepSeek V4 Flash in vLLM*** on a dual GH200 workstation. The short version is that the hardware behaves exactly like the memory benchmarks predicted. Tensor parallelism can work, but it needs care. The official checkpoint is slower than I expected. A quantized checkpoint from [Canada-Quant](https://huggingface.co/canada-quant/DeepSeek-V4-Flash-W4A16-FP8-MTP) turned out to be much faster. There was some wrangling to get multi-token prediction working, but once the checkpoint and vLLM path were made to agree with each other, I got a very large single-stream speed-up (*for my Chonky local Hermes Agent, bwHaHahahaaa...*).

The best single-request result I measured was about 193 output tokens per second with MTP3 on the Canada-Quant model checkpoint, compared with about 106 tokens per second without MTP. 

***TL;DR: If you want to run DSv4Flash on Hopper, use Canada-Quants and my PR at the end of the blog post.***

## The System Reminder

The machine is a dual Grace Hopper workstation:

| Component        |                                   Spec |
| ---------------- | -------------------------------------: |
| GPUs             |        2x Hopper H100, 96 GB HBM3 each |
| CPUs             |                2x Grace, 72 cores each |
| Host memory      | 480 GB LPDDR5X per Grace, 960 GB total |
| GPU local memory |                       192 GB total HBM |
| CUDA             |                                   13.0 |
| Driver           |                             580.105.08 |
| OS               |                  Ubuntu 24.04, aarch64 |

The important topology facts from Part 1 were:

| Path                              | Measured bandwidth |
| --------------------------------- | -----------------: |
| Local HBM                         |   about 3,700 GB/s |
| Local Grace LPDDR to local Hopper | about 377-380 GB/s |
| Remote Grace LPDDR to Hopper      |     about 133 GB/s |
| Hopper to Hopper staged copy      |   about 57-58 GB/s |

For LLM inference, those numbers give a useful mental model. If the hot decode path streams weights from local HBM, the machine is stupid fast. If it repeatedly crosses the inter-GH200 path, it's more like the cheese-grater onanism; you need to go slow, and most won't have the dedication to last. If an engine creates a lot of GPU-to-GPU traffic at batch 1, the topology will expose it.

## What I Tested

The main target was DeepSeek V4 Flash in vLLM (*yes, I also tested GGUFs with llama.cpp and its fork by [Antirez](https://github.com/antirez/ds4), but it was 5X slower*). I tested two model artifacts:

| Model                                                                                                               | Notes                                                   |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [deepseek-ai/DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)                               | Official checkpoint                                     |
| [canada-quant/DeepSeek-V4-Flash-W4A16-FP8-MTP](https://huggingface.co/canada-quant/DeepSeek-V4-Flash-W4A16-FP8-MTP) | W4A16/FP8 quantized checkpoint with MTP tensors present |

The benchmark shape was deliberately large enough to avoid measuring only startup and scheduler noise:

| Setting                  |         Value |
| ------------------------ | ------------: |
| Prompt length            |   8192 tokens |
| Output length            |   1024 tokens |
| Number of prompts        |             5 |
| Max concurrency          |             1 |
| Tensor parallelism       |             2 |
| `max_model_len`          |         32768 |
| `max_num_batched_tokens` |          8192 |
| `max_num_seqs`           |             1 |
| Sampling                 | temperature 0 |

The main vLLM flags were:

```bash
--distributed-executor-backend mp
--tensor-parallel-size 2
--disable-custom-all-reduce
--block-size 256
--gpu-memory-utilization 0.97
--kv-cache-dtype fp8
--generation-config vllm
```

I also used:

```bash
NCCL_P2P_DISABLE=1
VLLM_USE_FLASHINFER_SAMPLER=0
```

The `NCCL_P2P_DISABLE=1` setting is important on this machine. The two Hoppers do not have a usable direct peer path, so I wanted NCCL to avoid trying to use a topology that does not really exist here.

## First Result: The Canada Quant Is Much Faster

Without MTP, the official checkpoint and the Canada quantized checkpoint did not land in the same performance class.

| Model                       | MTP level | Output throughput |
| --------------------------- | --------: | ----------------: |
| Official DeepSeek V4 Flash  |      MTP0 |        64.9 tok/s |
| Canada W4A16/FP8 checkpoint |      MTP0 |       105.9 tok/s |

That is a large gap, and a WTF I wasn't expecting, as the model size for W4A16/FP8 is 10 GB larger than the original, and all things considered, smaller versions of the same model usually run faster. On this system, the quantized checkpoint is about 63 percent faster for the same single-stream benchmark shape.

This result is not simply a file-size effect. The Canada checkpoint is actually larger on disk than the official checkpoint on my machine: about 159 GB versus about 149 GB. That is partly because it includes MTP tensors and leaves some tensors in BF16 or FP32. So the useful question is not "which directory is smaller?", but "which tensors and kernels are on the hot decode path?"

The Canada artifact uses a different mixed layout: routed expert weights are W4-packed, attention projections are FP8, and some sensitive tensors remain higher precision. For single-stream decode on this topology, that can still reduce the active expert weight traffic and use more favourable vLLM kernel paths, even if the full checkpoint directory is larger. That makes the result consistent with the Part 1 memory measurements, but it is not proof that the speed-up comes only from fewer bytes on disk.

The official model is not "bad". It is just a less forgiving artifact for this exact deployment target. On a dual GH200 workstation with only 96 GB of HBM per GPU and a weak GPU-to-GPU path, the compressed checkpoint is the more natural fit.

There is one caveat: this is a throughput result, not a quality result. I would expect the Canada checkpoint to perform slightly worse than the official checkpoint in some cases, because the routed expert weights are quantized more aggressively. But the checkpoint is not a blunt whole-model 4-bit conversion. Attention projections remain FP8, many sensitive tensors are left BF16 or FP32, and the official baseline is already a compressed FP8 artifact. My expectation is that any quality difference is probably mild, and possibly difficult to detect outside targeted evals. *I have not measured that yet here.*

## MTP was busted

Multi-token prediction should help single-stream generation because it lets the model propose more than one token per target-model step. In practice, I initially hit a checkpoint/software mismatch.

The Canada model is compressed, but the MTP block contains BF16/unquantized tensors such as `mtp.0.*`. vLLM's DeepSeek V4 NVIDIA O-projection path expected FP8 scale metadata on the MTP `wo_a` projection. That is true for a fully FP8 path, but not for this mixed checkpoint.

The failure mode was simple: the main model could load, but MTP startup failed because the draft block did not have the expected FP8 scale tensor.

There are two ways to fix that:

1. Quantize the MTP tensors into the same compressed-tensors format as the rest of the checkpoint.
2. Teach vLLM to run a BF16 fallback for the unquantized MTP O-projection path.

The first option is probably the cleaner model artifact fix. But it requires a real quantization pass over the MTP tensors, and that may require calibration data and more model processing.

The second option is a useful runtime fix. If the MTP block is BF16, run that small draft path as BF16 instead of requiring FP8 metadata. That is what I tested.

There is one extra wrinkle: after sharing these results, the Canada-Quant maintainers pointed out that there are actually three adjacent fixes needed for completely stock end-to-end MTP on this artifact.

1. The artifact metadata needs to match vLLM's runtime module names, not only the on-disk safetensors names. The MTP repo now has a metadata-only fix for this using regex-based ignore patterns.
2. vLLM needs to propagate `prefix=` when constructing the DeepSeek V4 MTP `e_proj` and `h_proj` modules. Without that, compressed-tensors sees an empty layer name and cannot match the module.
3. Once loading and construction succeed, the NVIDIA O-projection execution path needs the BF16 fallback described below for unquantized MTP `wo_a`.

Those are three separate failure points. Missing any one of them breaks the run at a different stage: main-model load, MTP draft construction, or MTP draft execution.

## The vLLM Runtime Fix (yay!)

The patch shape is narrow. In `vllm/models/deepseek_v4/nvidia/ops/o_proj.py`, vLLM can check whether `wo_a` has FP8 scale metadata:

```python
def get_fp8_weight_scale(layer):
    if hasattr(layer, "weight_scale_inv"):
        return layer.weight_scale_inv
    if hasattr(layer, "weight_scale"):
        return layer.weight_scale
    return None
```

If the scale exists, use the normal FP8 path.

If it does not exist, apply inverse RoPE in BF16, reshape the flat grouped `wo_a.weight`, run the grouped matmul, and then continue through `wo_b`:

```python
weight_scale = get_fp8_weight_scale(wo_a)

if weight_scale is None:
    # BF16/unquantized MTP fallback:
    # 1. reshape o to grouped heads
    # 2. apply inverse RoPE to the rope slice
    # 3. reshape to grouped wo_a input
    # 4. reshape flat wo_a.weight to [groups, o_lora_rank, input_size]
    # 5. z = einsum("bgi,gri->bgr", wo_a_input, grouped_weight)
    # 6. return wo_b(z.flatten(1))
    return wo_b(z.flatten(1))

# Existing FP8 path.
```

I also needed to propagate `hf_config_path` into the speculative draft model config. Without that, the target could use the sanitized/local config but the draft path could fall back to a different config source. This is separate from the `prefix=` construction fix above, but it belongs to the same class of issue: the draft path must inherit the same model/config context as the target path.

I added focused tests for the config propagation and the O-projection fallback. For the upstream O-projection PR, I kept the scope narrower: only the NVIDIA O-projection fallback and its unit tests. That PR test file covers scale detection, BF16 inverse RoPE, the grouped `wo_a.weight` reshape, and the production `deep_gemm_fp8_o_proj` fallback branch.

This is not a performance optimization, it's a compatibility fix that unlocks the MTP weights already present in the Canada checkpoint.

## MTP Results - it makes inference faster 🤯

Once that path worked, the Canada checkpoint scaled well with MTP:

| Model            | MTP level | Output throughput | Mean TPOT | Acceptance |
| ---------------- | --------: | ----------------: | --------: | ---------: |
| Canada W4A16/FP8 |      MTP0 |       105.9 tok/s |   9.11 ms |        n/a |
| Canada W4A16/FP8 |      MTP1 |       152.7 tok/s |   6.20 ms |      90.8% |
| Canada W4A16/FP8 |      MTP2 |       179.9 tok/s |   5.18 ms |      81.9% |
| Canada W4A16/FP8 |      MTP3 |       193.0 tok/s |   4.82 ms |      71.1% |
| Canada W4A16/FP8 |      MTP4 |       162.1 tok/s |   5.81 ms |      47.9% |

MTP3 was the best point in this run. MTP4 was worse because the extra draft depth did not pay for itself. Acceptance dropped to about 48 percent, and the additional draft work outweighed the benefit, like eating those last fries when you are already full.

This is the practical lesson: MTP level is a tuning parameter, not a monotonic speed knob. More draft tokens != Faster.

After I posted these numbers, [yangsiqt2](https://huggingface.co/canada-quant/DeepSeek-V4-Flash-W4A16-FP8/discussions/8#6a266e2e43643d62dc5c270e) pointed out another important caveat: MTP acceptance is workload sensitive. Their end-to-end vLLM benchmark used short mixed technical/code/reasoning prompts, 64 sequential requests, and 256 generated tokens. In that setup they saw lower acceptance than this long-prompt, long-output benchmark: about 81 percent for MTP1 and 63 percent for MTP2. That still produced a large speed-up, but not the same acceptance profile. Do your own profiling!


## Official Checkpoint Comparison

The official checkpoint also benefits from MTP, but the baseline is much lower.

| Model                      | MTP level | Output throughput |
| -------------------------- | --------: | ----------------: |
| Official DeepSeek V4 Flash |      MTP0 |        64.9 tok/s |
| Official DeepSeek V4 Flash |      MTP1 |       108.3 tok/s |
| Official DeepSeek V4 Flash |      MTP2 |       138.8 tok/s |
| Official DeepSeek V4 Flash |      MTP3 |       149.5 tok/s |
| Official DeepSeek V4 Flash |      MTP4 |       134.9 tok/s |

The shape is similar: MTP helps, then too much MTP starts to hurt. But the Canada quantized checkpoint remains faster at every comparable point I tested.

> The best official result here was about 149.5 tok/s. The best Canada result was about 193.0 tok/s.

## GH200 Memory Measurements Revisited

Part 1 measured local HBM at about 3.7 TB/s and the staged GPU-to-GPU path at only about 58 GB/s. That huge ratio is what we are trying to tune the inference system to avoid.

A two-GPU tensor-parallel decode workload is only attractive if the engine keeps communication small relative to useful local work. Every unnecessary exchange between the Hoppers is crossing the weakest path in the system. Every reduction in streamed weight bytes helps because the machine is still mostly fighting memory movement during single-stream decode.

The Canada quantized checkpoint helps by reducing the bytes moved through the model path. MTP helps by amortizing target-model steps across multiple accepted tokens. Together, they make the workload a better match for this topology. I can't just go treating my "2x GH200" as a single large GPU. It is two very capable GPU+CPU modules with a much weaker path between them. *Really makes me wish I could jerry-rig an proper NVLink though*, as then I could.  But that bit of hardware would cost 5-figures, even if it wasn't Unobtanium.

## Obvious Takeaways

I hope you didn't read this whole blog article, it's really boring. You could have skipped to here, to read that on this dual GH200 system, the deployment rules are:

1. Keep active decode work in HBM as much as possible.
2. Avoid unnecessary GPU-to-GPU traffic.
3. Use quantized checkpoints when they reduce active weight traffic without breaking kernels.
4. Treat MTP level as a benchmarked parameter.
5. Do not assume the deepest MTP setting is best.

Look, all this is pretty obvious, right? The interesting bit was the journey, and having me waste about 2 days so you can find out that you get great perf from the Canada W4A16/FP8 checkpoint with MTP3 of DeepSeek V4 Flash in vLLM. The best tested configuration was :

```text
105.9 tok/s  without MTP
193.0 tok/s  with MTP3
```

Getting MTP working gave me an 82 percent improvement for the single-stream benchmark, and I opened this as a narrow upstream vLLM PR: [vllm-project/vllm#44847](https://github.com/vllm-project/vllm/pull/44847).