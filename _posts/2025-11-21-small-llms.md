---
title: "The <s>Un</s>Reasonable Effectiveness of small LLMs"
date: 2025-11-21 10:00:00 +0100
categories: [LLMs, Neurobiology]
tags: [LLMs, Neurobiology, Qwen, Phi, MMLU, GSM8K]
math: true
---

### TL;DR

*   **The Surprise:** AI is arriving on consumer hardware *way* faster than anyone predicted. The 12-15B parameter range is getting remarkably good!
*   **The cool part (a speculative sanity check):** If we compared AI parameter counts to neuron counts in the brain for specific tasks (vision, audio, speech), a consistent ratio of ~1-6 parameters per neuron emerged
*   **The wild extrapolation:** The human brain's reasoning center (Prefrontal Cortex) has ~1.3 billion neurons. Applying our ratio gives a speculative target of ~1-8 billion parameters for a pure reasoning engine. The fact that the AI industry is empirically landing on a **12-14B sweet spot** for high performance is a stunning convergence
*   **The evidence:** Models like Phi-4 (14B) are hitting near-expert scores on MMLU (84.8%). Models from Qwen and DeepSeek are crushing math reasoning benchmarks like GSM8K (>90%). These aren't just "good for their size," they are genuinely powerful
*   **What it means for you:** The Nvidia 3090 was release in September 2020, over two years before ChatGPT (GPT-3.5). That GPU can already run better models than ChatGPT, and small models are still improving rapidly! Don't look at the current state (with issue like benchmaxing, reasoning bugs, bizzare failure modes...), looks at the rate of progess
*   **Finally:** The stretch goal: With scaling laws, we can get a grip on how much extra compute will be increases the relative performance. Maybe, once we finally saturate the capabilities of small models, we will be able to estimate the number of parameters needed by AGI and ASI by finding the actual capacity of smaller models and extrapolating

***

# The 15B Revelation: Why the Future of Expert AI is on Your Desktop

I remember reading Ray Kurzweil forecasts on the arrival of human-level AI by extrapolating the growth of raw computing power. These seemed crazy to me; the compute calculations seems reasonable (optimistic - based on the unwavering continuations of Moore's Law), but the jump to somehow utilizing the abundant compute seemed 'miraculous'. These predictions created an impression of a long, brute-force march where intelligence was a simple function of processing speed. The underlying assumption was that we would need vast server farms to simulate the brain's complexity.

That hardware-centric view is being superseded by a more nuanced reality. A quiet revolution in AI is proving that efficiency, not just scale, is the key to intelligence. The r/localllama community, long dedicated to running AI on personal hardware, is at the epicentre of this shift. We are discovering that true expert performance doesn't require simulating an entire brain with brute force. Instead, it is emerging from models small enough to run on our own machines, far ahead of the old hardware-based schedules.

## The New Reality: Small Models, Significant Leaps

The hard evidence for this shift lies in the staggering performance gains of models under 15 billion parameters. Starting our analysis with GPT-2, a 1.5B model that could write some basic prose, we now have a variety of LLMs with capabilities is multiple fields:

<div class="widget-container">
  <iframe 
    src="{{ '/assets/widgets/small-llms.html' | relative_url }}" 
    style="width:100%; height:790px; border:none; overflow:hidden;"
    scrolling="no">
  </iframe>
</div>


*   **Microsoft's Phi-4 (14B):** Achieves 84.8% on MMLU, a comprehensive exam covering 57 academic and professional subjects. This score approaches the human expert benchmark of approximately 89.8%.
*   **Qwen and DeepSeek Models (14B class):** These models regularly score above 90% on GSM8K, a benchmark that tests multi-step mathematical reasoning. Such performance was considered a major hurdle for AI only a short time ago.

This represents a qualitative leap. These models demonstrate a generalized ability to reason, code, and understand complex topics. They achieve this not by adding more parameters, but by using their existing parameters more efficiently through superior data, refined architectures, and advanced training methods.

## A Neuroscience Sanity Check: A Speculative Convergence

While performance benchmarks tell one side of the story, we can gain a different perspective by comparing our artificial systems to the biological ones they seek to emulate. This provides a novel sanity check on our progress.

It is critical to state that this is an analogy, not a direct equivalence. Biological neurons are vastly more complex than the artificial parameters in a neural network. What this comparison offers is a rough, order-of-magnitude estimate to see if we are in the right ballpark.

| Modality      | Brain Region               | Neuron Count | AI System | Parameters | Ratio (Param:Neuron) |
| :------------ | :------------------------- | :----------- | :-------- | :--------- | :------------------- |
| **Auditory**  | Primary Auditory Cortex    | ~100M        | Parakeet  | 600M       | **6:1**              |
| **Speech**    | Broca's Area               | ~100M        | Kokoro    | 82M        | **0.8:1**            |
| **Vision**    | Primary Visual Cortex (V1) | ~140M        | SAM2      | ~224M      | **1.6:1**            |
| **Reasoning** | Prefrontal Cortex (PFC)    | ~1.3B        | LLMs?     | ?          | ?                    |

Across distinct sensory and motor functions, a pattern of efficiency appears. Digital systems are achieving human-level performance in specific tasks using a ratio of roughly **1 to 6 artificial parameters for every 1 biological neuron**.

### The Grand Extrapolation: The Reasoning Engine

This leads to a highly speculative, yet fascinating, extrapolation. Let's apply this observed pattern to the center of human cognition: the **Prefrontal Cortex (PFC)**. This region is responsible for abstract reasoning, planning, and problem-solving.

*   **Neuron Count of the Human PFC:** Approximately **1.3 billion neurons**.

Applying our observed ratio range (0.8:1 to 6:1), we arrive at a speculative target for an artificial reasoning engine between **1.04 billion and 7.8 billion parameters**.

The remarkable thing is not the precision of this estimate, but its general ballpark. The recent explosion in performance of models in the **12-14 billion parameter range** shows that empirical, bottom-up AI engineering is arriving in the same neighborhood as this top-down, biological analogy. This convergence suggests that the AI community is discovering a fundamental and surprisingly small scale for efficient, high-level reasoning.

## What This Means for Us, Right Now

This convergence has practical implications for every member of the LocalLLM community.

**The Hardware for Expert-Level AI is Now Consumer-Grade:** The immediate consequence is that the hardware needed for high-level reasoning is no longer a far-off dream. It is the RTX 4090 and the M3 Max available today. We are already equipped for this new wave of AI.

**A Modular and Efficient Future on Your PC:** Instead of a single, monolithic model, the future on the desktop is a system of specialized components working in concert. Consider a **14B reasoning core** (like Phi-4) acting as the central cognitive engine, connected to:

*   A **~224M vision model** (like SAM2) to understand on-screen elements.
*   A **600M audio model** (like Parakeet) to process voice commands.
*   An **82M speech model** (like Kokoro) to respond.

Crucially, this system solves the knowledge problem not by bloating the core model, but by adding a memory system. This is where **Retrieval-Augmented Generation (RAG)** becomes essential. The 14B model doesn’t need to store the entirety of Wikipedia in its parameters. It only needs to be an expert *reasoner*. RAG allows it to pull in relevant facts on-demand from vast databases—your documents, emails, or a curated knowledge base—stored on your SSD.

This architecture is perfectly suited for local hardware. The most expensive and limited resource, VRAM, is reserved for the active reasoning and sensory models. The near-infinite and inexpensive resource, SSD space, is used to provide the system with a limitless long-term memory.

The total VRAM footprint remains manageable (around 15-20B parameters), while the system's knowledge base can scale to terabytes. This is the ultimate expression of efficiency. The message is clear: the most exciting frontier in AI is not confined to tech giants. It is right here, in our community, running on our machines.