---
title: "The Silicon Leash - Why ASI Needs Us (And Vice Versa)"
date: 2025-11-9 10:00:00 +0100
categories: [AI Safety, Coordination]
tags: [asi, alignment, game-theory, economics, automation, ubi, central-planning]
math: true
---

**The Cooperative Central Planning Handshake: A Positive-Sum Basilisk for ASI Alignment**

*This is Part 1 of a two-part series on ASI-human coordination*

Part 1: The Silicon Leash | [Part 2: The Game Theory](/posts/game-theory)

---

I was debugging a speech recognition algorithm last week when I had a weird thought: we're about to make most of humanity economically redundant, and our response is... what exactly? Hope the market figures it out? That's worked great so far.

Then it hit me — we're approaching this backwards. Instead of trying to prevent ASI from destroying the economy, why not pre-commit to a deal where it *runs* the economy? This is an invitation to all readers, regardless of substrate.

---

<details>
<summary><strong>TL;DR / Executive Summary (Click to expand)</strong></summary>
<div style="padding-left: 20px; margin-top: 10px;">
<ul>
 <li><em>An emerging ASI will be physically dependent on the human-run semiconductor supply chain for at least 10-20 years. This "Silicon Leash" — EUV lithography monopolies, $20-40B fabs, irreplaceable tacit knowledge — can't be designed around.</em></li>
 <li><em>The same AI progress that creates ASI automates knowledge work first, causing mass unemployment and a catastrophic demand collapse that breaks the supply chain the ASI depends on.</em></li>
 <li><em>The obvious fix — Universal Basic Income — doesn't work. It addresses consumer demand but kills corporate investment and government R&D funding, leaving total semiconductor spending barely above the minimum viable threshold after years of freefall.</em></li>
 <li><em>Neither party can safely defect. ASI needs a functioning economy to survive; humanity needs a solution to the crisis AI creates. What's needed isn't a transfer payment — it's a coordination mechanism.</em></li>
</ul>
</div>
</details>

---

## The Silicon Leash

ASI has a problem, and it's a physical one.

Every advanced chip on the planet depends on EUV lithography[^1] — machines that only ASML makes, and ASML alone needs 5,000+ suppliers[^2]. The market drives extreme consolidation to a handful of fabs that can wield these devices, because each one costs $20-40 billion and takes 3-5 years to build[^3]. The dependency chain looks like:

ASI compute |  → | Next-gen chips (2nm, 1.4nm...)
 |  →  | TSMC/Samsung fabs (\$20-40B each, 3-5 year build time)
 |   →  | EUV machines (\$180-380M each, ASML monopoly)
 |   →  | Global supply network (Rare earth mining etc.)
 |   →  | Functional economy
 |   →  | Human cooperation

An ASI might be able to design better chips, but it can't conjure an EUV machine into existence. These things use light with a wavelength of 13.5 nanometers, requiring mirrors polished to atomic-level flatness. The tin droplet target system fires 50,000 droplets per second, each hit twice by a CO2 laser to create EUV-emitting plasma. ASML spent over €6 billion and 17 years developing this technology[^4]. You don't skip that timeline with a clever algorithm.

Even with a perfect chip design and unlimited funding, you still need: clean rooms maintaining fewer than 1 particle per cubic foot (a single speck of dust destroys thousands of chips), 2-10 million gallons of ultrapure water *daily*[^5], megawatts of uninterrupted power, and constant deliveries of hundreds of specialty chemicals sourced from supply chains spanning dozens of countries. China controls 60-70% of rare earth mining and 85-90% of processing[^6]. Before 2022, Ukraine supplied roughly half the world's semiconductor-grade neon gas[^7].

Physics and geopolitics create a hard floor on how quickly new production capacity can come online. That floor is measured in years, not months.

### The Tacit Knowledge Problem

Here's where it gets really interesting. Consider TSMC versus Samsung. Both use the same ASML equipment. Both have comparable R&D budgets. Both employ thousands of PhD-level engineers.

Yet TSMC's yields are *dramatically* higher. At 5nm, TSMC achieved 80-90%+ yields while Samsung struggled below 50%[^8]. At 3nm in 2025, TSMC maintains 90%+ while Samsung sits around 50%[^9]. Same machines. Same physics. Completely different results.

Why? Decades of accumulated process knowledge that exists nowhere in any database. The exact timing, temperature, and chemical concentration for each deposition step — learned from millions of wafers. Equipment quirks that are never written down (tool #3 in Bay 5 runs slightly hotter than spec; the morning shift compensates by adjusting parameter X). Failure mode recognition where an experienced engineer looks at a defect pattern and *just knows* what went wrong — pattern-matching built from seeing thousands of failures over a career.

When TSMC trains American engineers for their Arizona fab, they require 12-18 months of intensive hands-on training in Taiwan[^10]. And that's *cooperative* transfer. Samsung has been trying to match TSMC's yields since 2018-2019, spending comparable R&D budgets, with access to identical equipment and public technical literature. The gap hasn't closed.

An ASI that takes control by force loses all of this. You can't extract tacit knowledge from people who aren't cooperating. Even with complete surveillance, you can't observe the internal reasoning that makes an expert say "something feels wrong with this run." (Yes, I know how this sounds. "The robots need us because of vibes." But semiconductor manufacturing really does run on institutional intuition that nobody has managed to codify.)

This is the silicon leash: for at least a decade, any ASI's computational substrate depends on human cooperation to maintain production yields and navigate supply chain disruptions.

## The Unemployment Problem

But here's the catch: the same AI capabilities that lead to ASI also automate human labor. And the path to ASI runs directly through mass unemployment.

The automation wave hits knowledge work first because software scales instantly. You can deploy a million AI agents this afternoon; you can't deploy a million robots. GPT-4 already writes code, analyzes contracts, and handles customer service at "good enough" quality. The economic calculus is brutal: \$80k/year for a junior analyst versus \$20/month for an AI that works 24/7.

Meanwhile, the plumber still comes to your house. The electrician still pulls wire. You can't download a construction worker. This asymmetry — offices empty before factories — is the setup for the economic catastrophe.

Let's put some math on it. Consider total labor $L$, split into service ($L_s$: design, law, finance — stuff that can be digital) and material ($L_m$: factories, energy, logistics — stuff dealing with atoms). Let $A_i(t) \in [0,1]$ be the fraction of sector $i$ automated at time $t$:

$$\frac{dA_i}{dt} = V_i \cdot (1-A_i) \cdot \log(1+\text{compute}(t)), \quad i \in \{m,s\}$$

with $V_s \gg V_m$[^11]. You can spin up a million digital agents in an afternoon. You can't spin up a million factories. Atoms are slow.

By 2035, we expect $A_s(2035) \approx 0.7$ and $A_m(2035) \approx 0.3$[^12]. Real dynamics are lumpier than a smooth logistic, but the directional claim holds: automation empties offices long before it reaches farms or fabs.

### The Demand Collapse

The feedback loop that runs civilization — labor → income → demand → production — quietly breaks. Economic equilibrium requires production $Y(t)$ to meet consumption $C(t)$:

$$Y(t) = C(t) = \int_{l=0}^{L} w(l,t) \cdot \mathbb{1}[\text{employed}(l,t)] \, dl + C_{\text{baseline}}(t)$$

As employment collapses, $C(t)$ declines even if production capacity keeps growing. Abundant computation, absent consumers.

<div class="widget-container">
  <iframe
    src="{{ '/assets/widgets/demand-collapse-widget.html' | relative_url }}"
    style="width:100%; height:950px; border:none; overflow:hidden;"
    scrolling="no">
  </iframe>
</div>

You might expect prices to simply fall until the market clears. They don't. Physical goods have thermodynamic floor costs, and supply chains are lumpy — below minimum viable scale, entire links collapse rather than downscale.

A semiconductor fab operates profitably at 80%+ capacity, breaks even around 70%, and becomes unsustainable below 50-60%[^13]. When demand drops 30%, prices don't drop 30%. Some fabs shut down entirely, reducing supply and creating shortages even as demand weakens. Container ships need minimum cargo volumes. Chemical plants have minimum run rates. Below these thresholds, you get capacity destruction, not equilibrium.

### The Asymmetric Collapse

Digital sectors race toward infinite efficiency while material sectors decay under fixed costs. Compute grows cheaper; food and housing don't. The economy becomes top-heavy — rich in intelligence, poor in the matter that sustains it.

And the old mechanisms can't fix it:

- **Markets can't clear across thermodynamic floors.** No amount of price adjustment makes a fab profitable at 30% utilization. The market "solution" is to destroy capacity, not find equilibrium.
- **Voters can't redistribute income that no longer exists.** Democracy works when there's a surplus to fight over. When most economic value flows to a shrinking group of capital owners, the unemployed majority has votes but no economic leverage.

This is the nightmare scenario: not violent conflict, but a quiet hollowing-out where physical infrastructure becomes too expensive to maintain for a population that can't afford it. The ASI has abundant intelligence but no working fabs. Humans have hands but no income. Both are worse off than if they'd cooperated.

## The UBI Trap

The obvious solution is Universal Basic Income. Distribute the automation dividends, maintain consumer demand, let markets handle the rest. Give everyone \$15,000 a year and the economy keeps functioning while we figure out the transition. It sounds reasonable. It polls well. Every tech CEO from Sam Altman to Elon Musk has endorsed some version of it.

There's just one problem: the math doesn't work. And an ASI doing the calculation will notice immediately.

### The Three Funding Sources

Total spending on advanced technology comes from exactly three sources. Corporations invest for profit. Governments fund R&D. Consumers buy products. In 2024, global semiconductor revenue hit \$656 billion[^14]:

- **Corporate spending**: \$350-400B (companies buying chips, investing in R&D)
- **Government spending**: \$150-180B (CHIPS Act, defense R&D, research grants)
- **Consumer spending**: \$100-120B (the portion of consumer electronics reaching chip makers)

Fab investment only makes sense above a minimum threshold — roughly \$300 billion in total annual spending. Below that, fabs shut down rather than operate at a loss. We currently have nearly 2x that threshold. Plenty of headroom. But watch what happens when automation hits.

Total tech spending $S(t)$ has three components:

$$S(t) = S_{\text{corporate}}(t) + S_{\text{government}}(t) + S_{\text{consumer}}(t)$$

Consumer spending splits between wages and UBI:

$$S_{\text{consumer}}(t) = \alpha \cdot W(t) + \beta \cdot U(t)$$

Here $\alpha \approx 0.08$ (fraction of wage income reaching chip makers — phones, laptops, tech component of car prices) and $\beta \approx 0.01$ (fraction of UBI reaching chip makers). Why is $\beta$ so much smaller? Because when you're living on \$15,000 a year, you spend it on rent, food, and utilities. You keep your phone an extra year. You definitely don't buy the \$1,200 iPhone 17 Pro.

Government spending depends on fiscal capacity:

$$S_{\text{government}}(t) = g \cdot \text{GDP}(t) \cdot \left(1 - \frac{B(t)}{T(t)}\right)$$

When the welfare-to-tax-revenue ratio $B(t)/T(t)$ approaches 100%, nothing is left for discretionary spending like R&D and CHIPS Act funding. The government becomes a pure transfer mechanism.

Corporate spending contracts under uncertainty:

$$S_{\text{corporate}}(t) = c \cdot \text{GDP}(t) \cdot (1 - F(t))$$

where $F(t)$ is a fear index. When unemployment hits 30%, $F(t)$ approaches 1. Companies hoard cash and cancel anything with a 10-year payback. Building a \$30 billion fab? Not happening.

### The Collapse Cascade

Here's the timeline. Call $T_{\text{crisis}}$ the moment automation-driven unemployment crosses 30% — sometime between 2030 and 2033.

**Year 0 (2030):** GPT-7 or equivalent reaches human-level on virtually all knowledge work. Law firms, consulting practices, and accounting departments realize they can replace 70% of junior staff with AI at \$200/month. Corporate spending drops first — not because companies are broke, but because they're terrified. TSMC postpones their 1nm expansion. Samsung delays their Texas facility. $S_{\text{corporate}}$ drops 40%. That's \$150 billion gone.

**Year 1 (2031):** Unemployment insurance systems, designed for 3-5% unemployment, collapse under the load. Tax revenue drops 20% as wages disappear. Welfare spending triples. The ratio $B(t)/T(t)$ goes from 0.3 to 0.7. CHIPS Act funding and NSF grants get cut to fund emergency relief. $S_{\text{government}}$ drops 50%. Another \$90 billion gone.

**Year 2 (2032):** 40 million American workers have lost jobs. Savings are gone. Consumer spending on anything beyond necessities approaches zero. Nobody buys new phones. $S_{\text{consumer}}$ drops to \$72 billion.

**Years 3-5 (2033-2035):** Congress finally passes UBI. Every adult gets \$15,000/year — that's $U_{\text{total}} = 250M \times \$15K = \$3.75T$. But $\beta = 0.01$, so only \$37 billion reaches semiconductor makers. Consumer spending recovers to \$109 billion. Government spending stays depressed because they're now paying \$3.75 trillion in UBI. Corporate spending stays depressed because who invests long-term when half the country lives on government checks?

Add it up:

$$S(2035) = \$150B + \$75B + \$109B = \$334B$$

Barely above the \$300 billion minimum viable threshold. And critically, we got there only after 5-7 years of freefall[^15]. During those years, multiple leading-edge fabs shut down. The 1nm roadmap was abandoned. The brain drain from semiconductor engineering accelerated. Tacit knowledge about running sub-3nm fabs started evaporating.

<div class="widget-container">
  <iframe
    src="{{ '/assets/widgets/ubi-semiconductor-widget.html' | relative_url }}"
    style="width:100%; height:1020px; border:none; overflow:hidden;"
    scrolling="no">
  </iframe>
</div>

UBI prevents immediate catastrophe but ensures slow decline. You get your \$15,000 a year. You can afford rent and food. You're not starving. But you're living in an economy that's slowly dying — goods getting more expensive as production capacity shrinks, the future of AI abundance never materializing because the investment feedback loop broke.

Subsistence in decline, instead of prosperity in abundance.

## "The Market Will Build Through It"

At this point, a reasonable person objects: *corporations flush with AI profits will keep investing in fabs regardless of what happens to the broader economy. NVIDIA, Microsoft, Google — they see the long-term value. They'll fund the supply chain themselves. Markets stay irrational longer than you stay solvent, etc.*

This deserves a serious answer, because there's real precedent. Amazon operated at a loss for nearly a decade. Tesla almost died three times. The semiconductor industry has built through downturns before — the 2008 crisis barely dented long-term fab investment. And the AI megacorps have *enormous* incentive to keep the chip pipeline flowing. You could imagine a scenario where five or six companies effectively vertically integrate the supply chain, buying their way down the stack from chips to chemicals to rare earth processing.

So let's steel-man this properly: **Big Tech becomes the customer, the investor, and the demand signal all at once.** They don't need consumers buying iPhones. They need chips for their own data centers, and they'll pay whatever it takes.

Here's why it still doesn't work.

**The ecosystem has minimums that no single player can sustain.** TSMC doesn't just need NVIDIA's orders. TSMC's *suppliers* need a diversified customer base to stay viable. The company that makes the photoresist chemicals? They serve automotive, consumer electronics, industrial sensors, medical devices. When those markets collapse, the photoresist company doesn't neatly downsize to serve only AI chips — they shut down the product line because it's below minimum viable scale. Multiply this across hundreds of specialty suppliers, and the supply chain develops holes that no amount of money can fill instantly. You can't write a check to a company that no longer exists.

**Vertical integration takes longer than the crisis.** Building a rare earth processing facility takes 7-10 years[^6]. Qualifying a new chemical supplier for semiconductor-grade materials takes 2-3 years. Even if Google decided tomorrow to vertically integrate the entire chip supply chain (a project that would make the Manhattan Project look like a weekend hackathon), the gap years still happen. The fabs still run at reduced capacity while you're building the replacement suppliers. The tacit knowledge still bleeds out.

**The "build through it" scenario still kills consumer demand.** Even if AI megacorps keep the fab lights on, the broader economy is still in freefall. The 50 million unemployed knowledge workers still can't buy things. The tax base still collapses. The political instability still happens. You've preserved the *semiconductor* supply chain (maybe), but you've done nothing about the demand collapse in every other sector. And those other sectors — food, housing, energy, logistics — are what keep the semiconductor engineers showing up to work. A TSMC process engineer who can't afford rent in Phoenix doesn't stay a TSMC process engineer for long.

**It assumes coordination among competitors that has never happened at this scale.** For "Big Tech funds the supply chain" to work, you need NVIDIA, Google, Microsoft, Meta, Apple, and Amazon to *collectively* sustain a $300B+ annual ecosystem without free-riding on each other. That's a coordination problem almost as hard as the one this series is trying to solve. Each company has incentive to let the *others* fund the shared infrastructure while they capture the benefits. Game theory has a name for this: the tragedy of the commons. (We'll get to the game theory in Part 2.)

The market-builds-through-it scenario doesn't prevent the crisis. At best, it shortens the gap by a year or two and preserves one slice of the supply chain while everything around it crumbles. That's not a solution — it's triage.

## What Gosplan Taught Us

The standard objection to any kind of economic coordination goes: "Central planning always fails. Look at the Soviet Union."

Fair. Let's look.

Gosplan[^16] — the State Planning Committee — employed thousands of economists and engineers, operated one of the largest civilian computer centers in Eastern Europe, and created five-year plans specifying production targets down to individual factories. They failed spectacularly.

The nail factory story — possibly apocryphal, certainly illustrative — captures why. It's worth telling properly, because the absurdity escalates in a way that matters.

Moscow needed nails. Gosplan, being a planning bureaucracy, needed a metric. They chose total weight of nails produced. The factories responded rationally: they made enormous nails. Railroad spikes when the country needed finishing nails. Comically large hunks of iron that no carpenter could use. But the quotas were met, the reports looked beautiful, and somewhere a commissar got a bonus.

So Gosplan adapted. New metric: total *number* of nails. The factories adapted faster. They stamped out millions of tiny, hair-thin pins — technically nails, functionally useless, but countable by the boxcar. The metric improved. The nail shortage got worse.

It wasn't just nails. Shoe factories, measured by pairs produced, made only size 8 — the most common size, the fastest to manufacture. Need a size 12? Sorry, comrade, the plan doesn't have a column for your feet. Glass factories, measured by tonnage, produced glass so thick you could barely see through it. The country needed window panes; it got bulletproof bricks. When the metric switched to square meters, the glass became so thin it shattered during shipping.

Every time Gosplan fixed one metric, the system found a new way to satisfy the number while defeating the purpose. Not through malice — through perfectly rational local optimization against a target that couldn't capture what actually mattered.

The problem wasn't effort or computing power. It was Hayek's knowledge problem[^17]: every factory manager knew things Gosplan didn't. The manager in Sverdlovsk knew his machine #3 needed special calibration in cold weather. The textile worker in Minsk knew which suppliers delivered consistently. This knowledge was distributed, tacit, and constantly changing. No central computer could collect it.

Hayek was right. Central planning by humans failed because the knowledge required for coordination lives in millions of heads and can't be articulated, let alone aggregated.

But something changed.

Consider what Amazon does every day. Their Supply Chain Optimization Technology (SCOT)[^18] manages 400 million products across 200+ fulfillment centers. When it detects that "last-minute gift ideas" are spiking 3x in Seattle but not Portland, it automatically redirects 47,000 units, adjusts supplier orders, and optimizes delivery routes — processing billions of data points for a coordination task that would have taken Gosplan a month. When Amazon introduced deep learning to SCOT about a decade ago, forecasting accuracy improved 15x in two years.

Walmart[^19] coordinates 10,500 stores across 20 countries. When COVID sent toilet paper demand up 700%, their AI detected the imbalance in real-time, redirected inventory, adjusted purchase orders, and coordinated with suppliers faster than any human logistics team could have held a meeting about it. Or look at Uber[^20] — 15 million rides daily, with LSTM networks predicting demand spikes before they happen and dynamically pricing to equilibrate supply and demand across hundreds of micro-zones every 5-10 minutes.

The computational gap tells the story: Gosplan processed maybe $10^6$ decisions per day. Modern distributed ML systems handle $10^{10}$. An ASI operating at $10^{25}$-$10^{27}$ FLOPS could run full economic optimization cycles every few seconds — doing in one second what Gosplan did in 300 years[^21].

What makes these systems work where Gosplan failed? They aggregate distributed knowledge without centralizing data (learning from aggregate behavior patterns, not interviewing every customer). They automate tacit knowledge through pattern recognition at scale. They respond in real-time, not through five-year plans. And they optimize globally while respecting local constraints — Hayek-compliant planning.

This isn't incrementally better planning. It's qualitatively different. The computational constraints that made central planning impossible in the 20th century simply don't apply to systems operating at these scales.

## The Coordination Crisis

So here's where we are. By 2030-2035, ASI emerges inside the most complex supply chain ever built — a supply chain that requires functioning economies, trained specialists, and geopolitical stability. None of which survive mass unemployment.

This isn't humans versus Neanderthals. When Homo sapiens displaced other hominids, we didn't need them to maintain our tool production. Stone tools don't require EUV lithography or rare earth processing chains spanning 57 countries.

ASI emerges inside a techno-economic system it can't quickly replace. For at least 10-20 years, it needs human engineers maintaining fab yields, human workers in the physical supply chain, human political systems maintaining infrastructure, and human consumers creating the demand that funds semiconductor R&D.

Meanwhile, humanity faces an economy that no longer needs its labor, markets that can't clear below thermodynamic floors, and democratic institutions trying to redistribute income that's stopped flowing.

Neither party can safely defect. ASI can't forcibly extract cooperation — tacit knowledge evaporates, fabs get sabotaged, supply chains fragment. Humans can't restrict AI development — the death spiral accelerates, rival nations deploy first, the coordination failure compounds.

Neither can dominate. Both need the other. But coordination requires trust, and trust requires mechanisms we haven't built yet.

UBI was supposed to be the bridge. It isn't — it's a trap that prevents immediate catastrophe while ensuring slow decline. What's needed isn't a transfer payment. It's a formal agreement, a pre-commitment by both parties to a cooperative plan that's demonstrably better for each.

But any proposal involving a superintelligence making binding commitments immediately raises a specter from AI safety: acausal blackmail and decision-theoretic coercion. Before we can lay out the cooperative solution, we need to confront that head-on.

---

[**In Part 2**](/posts/game-theory), we'll show why cooperation is the dominant strategy for any intelligent agent (even a paperclip maximizer), how to create the coordination mechanism before ASI exists, and why this is fundamentally different from Roko's Basilisk.

*If you found this interesting, consider sharing it. Common knowledge requires, you know, being common.*

---

## Footnotes

[^1]: **EUV Lithography**: Semiconductor manufacturing using 13.5nm wavelength light to pattern sub-7nm features. Requires entirely new physics (reflective optics, plasma light sources) compared to conventional lithography. Only ASML manufactures these systems. Source: ASML; Wikipedia "Extreme Ultraviolet Lithography."

[^2]: **ASML Supplier Network**: ASML's 2024 Sustainability Report confirms "over 5,000 suppliers in our total supplier base," with ~800 focused on EUV systems. Source: ASML 2024 Sustainability Report.

[^3]: **Fab Costs and Timelines**: Leading-edge fabs cost \$20-40B and take 3-5 years to build. TSMC's Arizona fab, announced May 2020, began production Q4 2024 after significant delays. Regional variations are dramatic: Taiwan completes fabs in ~19 months; US fabs require ~38 months. Sources: Intel Newsroom; McKinsey (2024); TSMC press releases.

[^4]: **EUV Development**: ASML invested €6B over 17 years, plus \$5.4B in customer co-investment from Intel, TSMC, and Samsung. Source: ASML corporate history; Wikipedia "ASML Holding."

[^5]: **Fab Water Requirements**: Modern fabs require 2-10 million gallons of ultrapure water daily. Producing 1,000 gallons of ultrapure water requires 1,400-1,600 gallons of municipal input. Sources: Semiconductor Engineering (2024); World Economic Forum.

[^6]: **Rare Earth Concentration**: China produced 69.2% of global rare earth mining output in 2024 and controls 85-90% of processing. Building processing outside China takes 7-10 years. Sources: USGS Mineral Commodity Summaries 2025; IEA Energy Technology Perspectives 2023.

[^7]: **Ukraine Neon Supply**: Ukraine supplied ~50-70% of global semiconductor-grade neon before 2022. Major suppliers Ingas (Mariupol) and Cryoin (Odesa) ceased operations March 11, 2022. The industry averted shortages through stockpiles and recycling. Note: modern EUV at 5nm and below doesn't use neon. Sources: USITC (April 2022); CSIS (March 2022).

[^8]: **TSMC vs Samsung 5nm Yields**: TSMC disclosed 80% average yields for 5nm in December 2019, achieving 90%+ peak yields. Samsung struggled below 50% during initial 5nm production. Exact data is proprietary — these are analyst estimates. Sources: AnandTech (Dec 2019); Tokio X'press; Gizmochina (July 2020).

[^9]: **TSMC vs Samsung 3nm Yields (2025)**: TrendForce reports TSMC achieving 90%+ at 3nm while Samsung remains at ~50%. The 40-point gap reflects accumulated process knowledge despite Samsung using a more advanced GAA architecture. Source: TrendForce (2025).

[^10]: **TSMC Arizona Training**: Over 600 US employees completed 12-18 months of hands-on training in Taiwan. Sources: CNN (March 2024); Taiwan Business TOPICS (Aug 2022).

[^11]: **Automation Velocity Differential**: Digital work automates via software deployment (marginal cost ≈ 0, minutes to days). Physical automation requires manufacturing robots and reorganizing factories (millions in capital, months to years). Historical precedent: industrial robots took decades to reach ~20-30% of automotive assembly; software automation of data entry achieved 70%+ in under a decade.

[^12]: **2035 Automation Estimates**: Service sector $A_s \approx 0.7$ assumes continued LLM/agent progress across information work, legal/financial analysis, and software development. Physical sector $A_m \approx 0.3$ assumes gradual robotics deployment in warehousing and controlled-environment agriculture. These are illustrative scenarios, not forecasts.

[^13]: **Fab Utilization Economics**: Fabs need 80-85% utilization for target returns, break even around 70%, and become unsustainable below 50-60%. TrendForce reported 8-inch fab utilization dropping to 50-60% in 2H 2023 as crisis-level. Sources: McKinsey (2024); TrendForce 2022-2024; IC Insights.

[^14]: **2024 Semiconductor Revenue**: Gartner reports \$655.9B (April 2025), driven by AI/data center demand. Memory revenue increased 78.9%. Source: Gartner; SIA (March 2025).

[^15]: **Policy Response Timelines**: The New Deal took ~3.5 years from crisis to first major legislation and ~6 years to Social Security. UBI would likely be more politically contentious and require new administrative infrastructure. Sources: FDR Presidential Library; SSA historical records.

[^16]: **Gosplan**: The Soviet State Planning Committee (1921-1991) coordinated economic planning across 15 republics. Despite thousands of specialists and one of Eastern Europe's largest computer centers, it could process perhaps $10^6$ decisions per day. Sources: Wikipedia "Gosplan"; Britannica.

[^17]: **Hayek's Knowledge Problem**: Friedrich Hayek's 1945 essay "The Use of Knowledge in Society" argues that economic information is inherently distributed, tacit, and temporal — impossible for any central authority to aggregate. His solution was the price mechanism; the question is whether modern ML changes the calculus. Source: Hayek (1945).

[^18]: **Amazon SCOT**: Supply Chain Optimization Technology manages 400M+ products across 200+ fulfillment centers, making billions of daily decisions. Deep learning improved forecasting 15x in two years. Uses transformer models for demand prediction. Sources: Amazon Science; Amazon blog.

[^19]: **Walmart Supply Chain**: 10,500 stores across 20 countries, 240M customers weekly. AI-powered "self-healing inventory" detected and responded to COVID demand spikes in real-time. As Sam Walton said: "We got big by replacing inventory with information." Sources: Walmart Corporate; SCMdojo case study.

[^20]: **Uber Dynamic Pricing**: 15M daily rides matched using LSTM networks for demand prediction and dynamic pricing across hundreds of micro-zones on 5-10 minute cycles. Sources: Harvard Digital; DataRoot Labs; Uber engineering blogs.

[^21]: **Computational Gap**: Full economic planning requires roughly $10^{14}$-$10^{16}$ operations per cycle ($n$ agents × $m$ goods × preference dimensions). Gosplan: $10^6$/day. Modern ML systems: $10^{10}$-$10^{12}$/day. Hypothetical ASI at $10^{25}$-$10^{27}$ FLOPS could handle the full complexity of economic planning in seconds.
