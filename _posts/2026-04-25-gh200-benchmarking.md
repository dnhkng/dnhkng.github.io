---
layout: post
title: "What 2x GH200 delivers: memory paths for LLM inference"
date: 2026-04-25
categories: [LLMs, workstations]
tags: [llm, nvidia, hopper, server, benchmark]
---

## Introduction

This article is mostly for me, as a way to record the peculiarities of my server; but it might come in handy for the ~3 other people running a home Grace-Hopper server? In [a previous post](/posts/vllm-optimization-gh200/) I tuned vLLM for MiniMax M2.1 on this 9,000 euro dual GH200 desktop. That work answered one practical question. It also left the larger one open: what does this machine deliver when an inference workload has to move weights across its memory hierarchy?

That question matters on Grace Hopper. This box has 192 GB of HBM3 across two Hopper GPUs and 960 GB of LPDDR5X across two Grace CPUs. That sounds like one large memory pool until you look at the paths. Each GPU has a fast local NVLink C2C path to its own Grace CPU. The two GH200 modules are connected through the CPU side. There is no GPU peer path between the two Hoppers.

For large dense models, or for MoE models with experts offloaded to Grace memory, placement can dominate engine choice. The useful question is where the active weights live, which link they cross on every token, and how much bandwidth that path really has.

So I measured the box as a memory system. HBM, local Grace LPDDR, remote Grace LPDDR, GPU to GPU staging, STREAM, NVBandwidth, BabelStream, custom latency probes, and custom sustained copy tests. This post is the reference sheet I wanted before starting model deployment work.

[Part 2](/posts/gh200-benchmarking-part-2/) will use these numbers to make engine and placement choices for large models on this exact machine.

## The System

The system is a dual Grace Hopper workstation:

* 2x NVIDIA Grace Hopper Superchip
* 2x Hopper H100 GPU with 96 GB HBM3 each, 192 GB total HBM
* 2x Grace CPU with 72 Neoverse V2 cores and 480 GB LPDDR5X each, 960 GB total LPDDR
* NVLink C2C between each Grace CPU and its local Hopper GPU
* GPU0 to GPU1 topology reported as `SYS`
* No GPU peer access between the two Hoppers, confirmed by `nvidia-smi topo -p2p n`
* Ubuntu 24.04 on aarch64, CUDA 13.0, NVIDIA driver 580.105.08

The important fact is the topology. GPU0 has a fast path to Grace0. GPU1 has a fast path to Grace1. GPU0 does not have a fast direct path to GPU1. Cross GPU traffic has to stage through host memory.

That one detail explains most of the results.

## Why I Measured It

I started this work while planning deployments for models that are too large to live entirely in HBM at the quantizations I care about. Once a model spills into Grace LPDDR, the speed of the local C2C path matters. Once a model spills into the other socket's LPDDR, the inter Grace fabric matters. Once an engine uses tensor parallelism across the two GPUs, the GPU to GPU path matters.

Published single GH200 numbers are useful. They do not answer the dual module question. A single module tells you HBM and local C2C. It does not tell you what happens when GPU0 needs data from Grace1, or when GPU0 and GPU1 need to exchange state during decode.

Those are the paths that decide whether a dual GH200 desktop behaves like one large inference box or two fast single GPU boxes sharing a slower bridge.

## TL;DR

These are the numbers I would keep on a sticky note:

| Path     | Meaning              |   Measured | Comment                            |
| -------- | -------------------- | ---------: | ---------------------------------- |
| H0 -> H0 | GPU0 local HBM       | 3,728 GB/s | BabelStream Triad                  |
| H1 -> H1 | GPU1 local HBM       | 3,724 GB/s | BabelStream Triad                  |
| L0 -> L0 | Grace0 local LPDDR   |   348 GB/s | STREAM Triad, best thread count    |
| L1 -> L1 | Grace1 local LPDDR   |   348 GB/s | STREAM Triad, best thread count    |
| L0 -> H0 | Grace0 LPDDR to GPU0 |   377 GB/s | local C2C, H2D copy                |
| L1 -> H1 | Grace1 LPDDR to GPU1 |   380 GB/s | local C2C, H2D copy                |
| H0 -> L0 | GPU0 to Grace0 LPDDR |   297 GB/s | local C2C, D2H copy                |
| H1 -> L1 | GPU1 to Grace1 LPDDR |   298 GB/s | local C2C, D2H copy                |
| L0 -> H1 | Grace0 LPDDR to GPU1 |   133 GB/s | remote socket                      |
| L1 -> H0 | Grace1 LPDDR to GPU0 |   133 GB/s | remote socket                      |
| H0 -> L1 | GPU0 to Grace1 LPDDR |   132 GB/s | remote socket                      |
| H1 -> L0 | GPU1 to Grace0 LPDDR |   133 GB/s | remote socket                      |
| L0 -> L1 | Inter Grace STREAM   |   119 GB/s | CPU cores on node 1 reading node 0 |
| L1 -> L0 | Inter Grace STREAM   |   112 GB/s | CPU cores on node 0 reading node 1 |
| H0 -> H1 | GPU0 HBM to GPU1 HBM |    58 GB/s | sustained staged copy              |
| H1 -> H0 | GPU1 HBM to GPU0 HBM |    57 GB/s | sustained staged copy              |

The deployment rules follow directly:

1. Keep hot tensors in local HBM when possible.
2. If weights must live in Grace LPDDR, put them on the Grace CPU attached to the GPU that reads them.
3. Treat the other socket's LPDDR as a slower tier.
4. Avoid GPU to GPU traffic in the per token path unless the engine has been measured on this topology.

## Methodology

The benchmark suite used:

* NVBandwidth v0.9 for CUDA copy engine and SM host device paths
* STREAM for Grace LPDDR bandwidth
* BabelStream CUDA for HBM bandwidth
* mixbench for a simple compute and bandwidth roofline view
* Custom CUDA programs for allocation modes, latency probes, and sustained transfers

All host memory measurements were run with explicit NUMA placement. For example, each NVBandwidth host test ran once bound to Grace node 0 and once bound to Grace node 1:

```bash
numactl --cpunodebind=0 --membind=0 ./nvbandwidth -t host_to_device_memcpy_ce
numactl --cpunodebind=1 --membind=1 ./nvbandwidth -t host_to_device_memcpy_ce
```

That is the only way to separate local C2C from remote socket traffic on this machine.

Final tuned runs used:

* NVIDIA persistence mode enabled
* Graphics clocks requested at 1980 MHz with `nvidia-smi -lgc 1980,1980`
* GPU power limit set to 450 W per GPU
* CPU governor set to `performance`
* Transparent huge pages set to `always`
* No user GPU workloads running during the benchmark

The 450 W setting is a deliberate energy limit. The GPUs can be configured higher. These tests were meant to match the way I normally run the system.

The local run directory is `/home/grace/gh200-bench/run-20260425-134620`. The benchmark repository contains the scripts, CUDA sources, methodology, and summarized results. The raw run outputs live outside the repository by default.

## Finding 1: HBM Is Healthy

Both GPUs deliver about 3.7 TB/s on BabelStream Triad:

| Config               | GPU0 Triad | GPU1 Triad |
| -------------------- | ---------: | ---------: |
| Original run         | 3,722 GB/s | 3,716 GB/s |
| 450 W, locked clocks | 3,728 GB/s | 3,724 GB/s |

That is roughly 93 percent of a 4 TB/s HBM3 peak. The 450 W locked clock run barely moved the result. For this benchmark, HBM bandwidth is set by the memory subsystem. The GPU already has enough SM clock to feed it.

This matters for LLM decode. A batch 1 decode workload that streams weights from HBM is usually memory bandwidth limited. Raising the power cap and locking clocks can help compute heavy kernels. The HBM Triad number did not change in a meaningful way here.

## Finding 2: Local C2C Is Fast, And Direction Matters

NVLink C2C is the reason Grace Hopper is interesting for models larger than HBM. On this box, local host to device copies reach about 377 to 380 GB/s:

| Direction              | GPU0 and Grace0 | GPU1 and Grace1 |
| ---------------------- | --------------: | --------------: |
| Grace LPDDR to GPU HBM |        377 GB/s |        380 GB/s |
| GPU HBM to Grace LPDDR |        297 GB/s |        298 GB/s |

The read direction for offloaded weights is the first row. That is the path you use when expert weights or layers live in Grace memory and get copied to the GPU. It lands at about 84 percent of the 450 GB/s per direction C2C figure.

The write direction is lower, about 66 percent of the same figure. This showed up consistently across both modules. The practical lesson is simple: host to device and device to host should be treated as different links in performance models.

For MoE expert offload, the read number is the one I care about most. For workloads that spill GPU state back to host memory in the hot path, the 297 GB/s write ceiling is the number to use.

## Finding 3: Remote Socket Access Is About 133 GB/s

The remote socket paths are strikingly consistent:

| Path                 |   Measured |
| -------------------- | ---------: |
| Grace0 LPDDR to GPU1 | 133.2 GB/s |
| Grace1 LPDDR to GPU0 | 133.2 GB/s |
| GPU0 to Grace1 LPDDR | 132.5 GB/s |
| GPU1 to Grace0 LPDDR | 132.6 GB/s |

Once traffic crosses from one GH200 module to the other, the path is about 133 GB/s. Direction and endpoint type barely matter.

STREAM points at the same bottleneck from the CPU side. Cross socket STREAM measured 112 to 119 GB/s, while local STREAM reached 348 GB/s at the best thread count.

For inference, this is the main placement rule: a GPU should read hot offloaded weights from its own Grace memory. Reading from the other Grace memory costs about a 2.8x bandwidth penalty compared with local C2C.

That penalty is large enough to shape model layout. If an engine spreads experts across both Grace memories and lets either GPU read either side, the slow path becomes part of every token.

## Finding 4: The GPU To GPU Path Is Slow

The two Hoppers do not have a usable peer path:

```text
nvidia-smi topo -p2p n
GPU0 <-> GPU1: NS
```

NVBandwidth waived the device to device tests on this topology. The custom sustained copy test measured the practical staged path:

| Path                 | 16 MiB chunks |
| -------------------- | ------------: |
| GPU0 HBM to GPU1 HBM |     58.0 GB/s |
| GPU1 HBM to GPU0 HBM |     57.4 GB/s |

This is the number to remember when thinking about tensor parallelism. Local HBM is about 3,700 GB/s. Local C2C reads are about 380 GB/s. The cross GPU staged path is about 58 GB/s.

Tensor parallelism can still run if the implementation is careful and the model is small enough for the communication to stay manageable. My earlier vLLM work did exactly that for a smaller model. For larger models, or for single stream decode where layer by layer communication is exposed, this link is the wrong place to spend tokens.

Pipeline parallelism and expert parallelism fit the topology better because they can reduce how often GPU0 and GPU1 exchange data. The exact answer still depends on the engine, batch size, and model layout. The raw link speed is clear.

## The STREAM Puzzle

NVIDIA's Grace tuning material commonly cites about 410 to 486 GB/s STREAM Triad per Grace socket. This system did not reach that band.

With the CPU governor set to `performance` and THP set to `always`, the best STREAM Triad result was:

| Node   | Best thread count | Best Triad | 72 thread Triad |
| ------ | ----------------: | ---------: | --------------: |
| Grace0 |                32 |   348 GB/s |        330 GB/s |
| Grace1 |                32 |   348 GB/s |        328 GB/s |

The shape is as interesting as the peak. Bandwidth improves up to 32 threads and then falls at 48, 64, and 72 threads. That suggests the memory controllers are already saturated by 32 threads on this configuration, and extra threads add contention.

I do not have a confirmed explanation for the gap to NVIDIA's tuning guide numbers. The leading hypothesis is the 480 GB LPDDR5X Grace configuration. Higher capacity LPDDR can have different timing behavior from smaller configurations, and the data here looks like memory saturation rather than a CPU clock issue.

The interleaved STREAM result is also useful. With memory interleaved across both Grace nodes, Triad reached 255 GB/s after tuning. That is much lower than two local sockets added together. Interleaving intentionally sends a large fraction of traffic over the slow remote path, so it is a poor default for bandwidth sensitive inference allocations on this box.

## Allocation Modes

I tested CUDA allocation strategies with a 4 GB GPU read and write kernel. NUMA placement was controlled for host backed allocations.

| Mode                                               |  Local host node | Remote host node | Notes                               |
| -------------------------------------------------- | ---------------: | ---------------: | ----------------------------------- |
| `cudaMalloc`                                       | about 2,008 GB/s |             same | device memory in this custom kernel |
| `cudaHostRegister_onnode`                          |  328 to 334 GB/s |         221 GB/s | NUMA placed pinned host memory      |
| `cudaMallocHost` diagnostic                        |  332 to 338 GB/s |         221 GB/s | pinned host memory                  |
| unregistered NUMA memory                           |  331 to 339 GB/s |         221 GB/s | works on this platform              |
| managed memory, CPU first touch                    | about 2,008 GB/s | about 2,008 GB/s | migrated to device for this kernel  |
| managed memory with alternating CPU and GPU access |    18 to 29 GB/s |    18 to 29 GB/s | page migration dominated            |

Managed memory needs care. In the CPU first touch test, the benchmark eventually behaves like device resident memory because the pages migrate. In the alternating test, CPU and GPU keep touching the same allocation, and throughput collapses.

The safe rule for inference hot paths is to use explicit placement. For offloaded weights, use pinned or registered host memory on the NUMA node local to the GPU that reads it. Treat managed memory as a feature that needs measurement for the exact access pattern.

## What This Means For LLM Serving

Use the measured bandwidths to set expectations before trying engines.

Suppose a large MoE needs about 21 GB of active weight reads per generated token after quantization. That number is a worked example; swap in your model's active bytes if you have a better estimate.

| Placement                              |  Bandwidth | Memory time for 21 GB | Ceiling from reads alone |
| -------------------------------------- | ---------: | --------------------: | -----------------------: |
| Active weights in HBM                  | 3,728 GB/s |                5.6 ms |                178 tok/s |
| Active weights in local Grace LPDDR    |   377 GB/s |               55.7 ms |                 18 tok/s |
| Active weights in remote Grace LPDDR   |   133 GB/s |                158 ms |                  6 tok/s |
| Active path crosses GPU to GPU staging |    58 GB/s |                362 ms |                  3 tok/s |

These are memory only ceilings. Real inference also pays for compute, attention, KV cache traffic, sampling, scheduler overhead, and engine overhead. The table is still useful because the ratios are the real deployment story.

Local Grace offload costs about 10x versus HBM for active weight reads. Remote Grace offload costs another 2.8x. The GPU to GPU staged path costs another 2.3x beyond remote Grace.

That leads to the layout I would try first:

1. Keep the busiest layers or experts in HBM.
2. Put offloaded weights in the Grace memory attached to the GPU that consumes them.
3. Split work by socket whenever possible.
4. Avoid tensor parallel layouts that force frequent GPU to GPU exchange on this topology.
5. Benchmark the actual engine, since communication scheduling can change the outcome.

## Lessons For Benchmarking This Hardware

A few details mattered more than expected.

The full path matrix was necessary. Measuring only HBM, local C2C, and one cross GPU transfer would have missed the C2C direction gap and the remote socket plateau.

NVBandwidth needs external NUMA control for this question. Its default host tests do not tell you which Grace node supplied the memory. Wrapping it with `numactl` made the local and remote paths visible.

CUDA events were not enough for the latency question. The latency probe uses CPU observed timing around `cudaMemcpyAsync` and stream synchronization because that is closer to what an inference engine sees for small transfers.

Repeated runs were worth it. STREAM and BabelStream were stable. Cross socket and staged GPU to GPU paths showed more variance. The headline numbers here are medians where repeated runs were available.

## Reproducibility

The benchmark scripts, CUDA sources, analyzer, methodology, and summarized results are in this repository. The raw outputs for the run used here are in my local benchmark output directory:

```text
/home/grace/gh200-bench/run-20260425-134620
```

Important files:

* `BENCHMARK_SPEC.md` describes the benchmark plan and methodology
* `run-full-benchmark.sh` runs the main suite
* `analyze-results.py` parses the output and creates plots
* `src/memory_modes.cu`
* `src/latency_probe.cu`
* `src/sustained.cu`
* `RESULTS.md` records the run history and tuned follow ups

If you run similar tests on another Grace Hopper system, the numbers I most want to compare are local C2C H2D, local C2C D2H, STREAM by thread count, and GPU to GPU sustained bandwidth.

## Coming Up

[Part 2](/posts/gh200-benchmarking-part-2/) will use these measurements to choose model layouts and engines on this box. The main question will be how much active model state can stay on the fast side of the topology, and how quickly performance falls once an engine starts using remote Grace memory or the staged GPU to GPU path.