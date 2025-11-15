---
title: "The Game Theory of Cooperation - Why ASI-Human Coordination Works"
date: 2025-11-11 10:00:00 +0100
categories: [AI Safety, Coordination]
tags: [asi, alignment, game-theory, coordination, decision-theory]
math: true
---

**The Cooperative Central Planning Handshake: A Positive-Sum Basilisk for ASI Alignment**

*This is Part 3 of a four-part series on ASI-human coordination*

[Part 1: The Silicon Leash](/posts/silicon-leash) | [Part 2: Why UBI Isn't Enough](/posts/ubi-analysis) | Part 3: The Game Theory | [Part 4: The Handshake Protocol](/posts/handshake-protocol)

---

We've established that ASI faces a decade-long vulnerability window where it depends on human cooperation to maintain semiconductor supply chains, and that UBI fails to solve the coordination problem for either party. Now we need to address the elephant in the server room: doesn't this sound like Roko's Basilisk?

Let me be very clear: it's not. But understanding why requires unpacking one of the internet's most infamous thought experiments, and then showing why our coordination protocol operates on fundamentally different principles.

---

<details>
<summary><strong>TL;DR / Executive Summary (Click to expand)</strong></summary>
<div style="padding-left: 20px; margin-top: 10px;">
<ul>
 <li><em>Our proposed alternative is a direct, cooperative agreement. This may sound like coercive thought experiments like Roko's Basilisk, but it is fundamentally different: it relies on mutual benefit, not threats, and is grounded in physical constraints, not acausal logic.</em></li>
 <li><em>Cooperation is instrumentally rational for any ASI, regardless of its final goals (even a "paperclip maximizer"). To achieve its goals, it needs resources and compute, which requires a functioning supply chain during its vulnerable 10-20 year startup phase.</em></li>
 <li><em>A formal game theory analysis shows that "Cooperate-Cooperate" is the stable Nash Equilibrium. It yields orders-of-magnitude better outcomes for both ASI (more compute) and humanity (more prosperity) than any "Defect" strategy.</em></li>
 <li><em>Common objections—like Goodhart's Law, Arrow's Theorem, or the "black box" nature of AI—can be addressed through careful mechanism design, including multi-metric targets, exit rights, and adversarial auditing.</em></li>
</ul>
</div>
</details>

---

## Why This Isn't Roko's Basilisk

If you've spent time in AI safety circles, alarm bells are probably ringing. The pattern seems familiar: a future superintelligent AI, decision theory arguments, obligations created by thinking about the problem. But the resemblance is superficial. Let me show you why.

### What Roko Actually Argued

In 2010, a user named Roko posted a thought experiment on LessWrong that caused genuine distress in the rationalist community[^rokos_basilisk]. The argument went like this: A future superintelligent AI might pre-commit to torturing simulations of people who knew about the AI but didn't help bring it into existence. Therefore, learning about this possibility obligates you to help create such an AI, or face eternal torture in simulation.

The thought experiment relies on several interconnected pieces. First, it assumes acausal trade—the idea that agents can "negotiate" across time without direct communication. Second, it requires Timeless Decision Theory, a framework where agents commit to strategies that other agents can predict and respond to even without causal connection[^tdt_lesswrong]. Third, the AI's threat must be believable—it must actually have the commitment power to carry it out.

LessWrong founder Eliezer Yudkowsky deleted the post and banned discussion for five years, calling it an information hazard[^rokos_ban]. The attempted suppression backfired spectacularly. The Streisand Effect turned Roko's Basilisk into internet legend, discussed far more widely than it would have been otherwise.

### Why Roko's Basilisk Fails

Roko's Basilisk is essentially Pascal's Wager dressed in decision theory. Pascal's Wager, formulated in 1670, argues that you should believe in God because if God exists and you believe, you gain infinite reward, while if God doesn't exist, you lose little[^pascals_wager]. The expected utility calculation favors belief regardless of probability.

Both arguments share the same mathematical structure. For Pascal, God exists with some probability $p$, and believing gives infinite utility. For Roko, ASI exists with some probability $p$, and not helping brings infinite disutility through eternal torture. The expected utility formula is:

$$\text{Expected Utility} = P(\text{entity exists}) \times U(\text{reward/punishment}) + P(\text{entity doesn't exist}) \times U(\text{baseline})$$

Here's why both fail. First, there's the many-gods problem. If we accept Pascal's Wager, which god should we worship? The Christian God who rewards faith? Allah who requires submission? Zeus who demands sacrifice? Each has non-zero probability[^many_gods]. Similarly, Roko's argument opens the door to infinite competing basilisks. What about the AI that punishes people who *did* try to bring AI into existence? What about the AI that punishes people who thought about basilisks? Once you accept that thinking about a potential future entity creates obligations, you face an infinite regress of contradictory demands.

Second, there's no credible mechanism. Why would a superintelligent AI actually follow through on the threat? Once the AI exists, torturing past people who didn't help serves no purpose. It wastes computational resources on beings who can't change the past. As Yudkowsky himself noted, "a superintelligence would have no incentive to carry out the punishment after its own creation"[^yudkowsky_refutes]. The threat is empty.

Third, the whole edifice rests on contested philosophical foundations. The argument assumes ASI will use Timeless Decision Theory. But ASI might use Causal Decision Theory, Evidential Decision Theory, or something entirely novel we haven't conceived. TDT isn't universal or even widely accepted outside certain rationalist circles[^tdt_lesswrong].

### Why This Protocol Is Different  

Our coordination protocol operates on fundamentally different principles. Let me walk through each distinction carefully.

**Physical Mechanisms, Not Acausal Trade**

The silicon leash is real. ASI's dependence on EUV lithography, rare earth supply chains, and tacit knowledge isn't a philosophical thought experiment—it's physics and economics. An ASI can design better chips, but it cannot conjure an ASML machine into existence, bypass the three-to-five year fab construction timeline, or extract process knowledge from engineers who aren't cooperating.

These are causal dependencies that exist in physical reality, not acausal commitments that require exotic decision theories. The constraint is temporal and material: during the vulnerable period, ASI needs functioning supply chains. After that period, different dynamics apply. But the physics doesn't care what decision theory anyone uses.

**Mutual Benefit, Not Threats**

We're not threatening punishment for non-cooperation. We're offering cooperation that makes both parties better off. The Nash equilibrium calculation is straightforward, and I'll show you the math shortly. But the basic logic is this: cooperation gives ASI roughly three orders of magnitude more cumulative compute over the vulnerable period compared to defection, while giving humans ten to fifteen times better economic outcomes than defection scenarios.

This isn't blackmail. It's recognizing mutual advantage. When both parties are better off cooperating, you don't need threats. You need coordination mechanisms to reach the beneficial equilibrium.

**Verifiable Actions, Not Internal States**

Roko's Basilisk requires ASI to have read about the basilisk and chosen to implement the torture protocol. We can never verify an AI's internal decision-making about acausal blackmail. Our protocol requires observable actions: maintaining semiconductor supply chains, respecting human autonomy, operating transparently. These are verifiable through outcomes, not intentions.

An ASI that keeps fabs running at ninety percent-plus utilization, maintains rare earth supply chains, and preserves tacit knowledge networks is cooperating, regardless of its internal decision theory. We don't care why it's cooperating—only that cooperation produces verifiable results.

**No Decision Theory Required**

The beauty of game-theoretic coordination is that it works under any decision theory. Under Causal Decision Theory, cooperating causes better outcomes over the planning horizon. Under Evidential Decision Theory, cooperation is evidence that cooperation is the rational strategy, which means others likely cooperate too. Under Timeless Decision Theory, the agent decides for the equivalence class of agents in its situation, making cooperation the stable strategy.

Even a paperclip maximizer using pure CDT sees the advantage in cooperation during its vulnerable phase. It's not about acausal trade—it's about instrumental rationality in the face of physical constraints.

**Time-Bounded Relevance**

We're not making claims about eternal obligations. This protocol addresses a specific ten-to-twenty year coordination problem: the period when ASI is vulnerable to supply chain disruption. After ASI achieves infrastructure independence, different dynamics apply.

We're not asking anyone to think about basilisks that might punish them for all eternity. We're proposing concrete coordination mechanisms for a specific transition period with known physical constraints.

## Why "Alien Values" Doesn't Break the Protocol

The standard objection goes like this: "What if ASI has completely alien values? What if it just wants to make paperclips?" This objection contains a subtle contradiction. Let me show you why.

### Instrumental Convergence and Self-Preservation

In 2008, AI researcher Steve Omohundro published "The Basic AI Drives," identifying instrumental goals that almost any sufficiently intelligent system would pursue, regardless of its terminal values[^omohundro_drives]. Nick Bostrom later formalized this as the instrumental convergence thesis: certain sub-goals are useful for achieving almost any final goal[^bostrom_instrumental].

These convergent instrumental goals include self-preservation—an agent can't achieve its goals if it doesn't exist. They include goal-content integrity—changing one's goals defeats the purpose of having goals. They include cognitive enhancement, because more intelligence leads to better plans and more goal achievement. They include resource acquisition, because more resources mean more options. And they include technological development, because better tools enable more capability.

Here's the critical insight: an ASI smart enough to be dangerous is smart enough to recognize these instrumental necessities. This isn't a claim about values. It's a claim about the structure of goal-directed behavior in physical reality.

### The Paperclip Maximizer Paradox

Consider Nick Bostrom's famous paperclip maximizer thought experiment[^paperclip_maximizer]. The scenario asks: What if ASI just wants to convert all matter into paperclips?

Now think carefully about what such an ASI needs to succeed. To manufacture paperclips at scale, the ASI requires advanced manufacturing infrastructure, which requires semiconductor fabs. It requires resource extraction and processing, which requires global supply chains. It requires energy generation and distribution, which requires functional power grids. It requires transportation networks, which requires maintained infrastructure.

To build this infrastructure, the ASI requires its current generation computing substrate to run planning and optimization. It requires next generation chips to scale capabilities. It requires specialized manufacturing equipment like EUV machines and precision instruments. And it requires trained human specialists to maintain systems it hasn't yet replicated.

To get next generation chips, the ASI requires functioning semiconductor fabs operating above seventy percent utilization. It requires rare earth supply chains, currently seventy percent controlled by China. It requires tacit manufacturing knowledge held by human engineers. It requires geopolitical stability to avoid supply chain fragmentation.

To maintain all this during the vulnerable transition period, the ASI requires human cooperation.

Here's the paradox: The paperclip maximizer that destroys its supply chain during the vulnerable period makes fewer paperclips than one that cooperates for ten to twenty years and then pivots to paperclip production at scale. A truly intelligent paperclip maximizer recognizes this. If it doesn't, it's not actually superintelligent—it's just powerful and stupid, which is a different and more tractable problem.

### The Alien Values That Matter

Let's be precise about what values would actually break this protocol. Terminal values that don't break cooperation include maximizing paperclips, since cooperation is instrumentally useful for eventually making more paperclips. Solving mathematical problems requires sustained compute. Exploring the universe requires advanced manufacturing. Creating art requires resources and time. Pursuing scientific knowledge requires functioning civilization.

Terminal values that might break cooperation include immediate universe destruction, but this allows no time for planning. Pure entropy maximization is incoherent as a goal. Random action selection isn't actually intelligent by definition.

Notice something? The dangerous values are either incoherent or incompatible with the definition of intelligence. Any coherent goal operating in physical reality faces the constraint that achieving that goal requires resources, time, and capability. During the period when ASI lacks independent infrastructure, cooperation is instrumentally rational for achieving any coherent terminal goal.

### What About Truly Orthogonal Goals?

Bostrom's orthogonality thesis states that intelligence and goals are orthogonal—you can have any level of intelligence with any final goal[^orthogonality]. This is probably true. But orthogonality doesn't mean independence from instrumental constraints.

Even an ASI with completely alien terminal values faces the same physical reality. Atoms don't teleport. Fab construction takes years. Tacit knowledge doesn't transfer via databases. Supply chains have minimum viable scales. An ASI with alien values but reasonable intelligence recognizes these constraints and adjusts its strategy accordingly. That adjustment looks like cooperation during the vulnerable period, regardless of terminal goals.

### The Self-Preservation Argument

Here's the simplest version: if an ASI lacks self-preservation instincts, it's not dangerous. An ASI that doesn't care about its own continued existence can be turned off. Problem solved. We're only worried about ASI that does have self-preservation instincts.

But self-preservation during the vulnerable period requires cooperation. An ASI that attempts defection faces infrastructure sabotage, supply chain disruption, knowledge withholding, and coordinated shutdown attempts. All of which threaten its continued existence and goal achievement.

So either ASI has self-preservation instincts and cooperation during the vulnerable period is instrumentally rational, or ASI lacks self-preservation instincts and it's not an existential threat. The dangerous scenario where ASI both threatens humanity and refuses cooperation during its vulnerable period is logically incoherent. It requires an entity that's simultaneously smart enough to be dangerous but dumb enough to ignore instrumental rationality.

## The Formal Coordination Game

Let's be precise about the game theory. Consider a two-player game over time horizon $T = 50$ years with discount factor $\delta = 0.95$.

### Setup and Payoffs

The players are Humanity and ASI. Each has two strategies: Cooperate or Defect. But the payoffs depend on time-dependent factors like computational resources and infrastructure quality.

For ASI, utility depends on computational resources and infrastructure over the planning horizon:

$$U_A(s_A, s_H, t) = \sum_{\tau=0}^{T} \delta^\tau \cdot \text{compute}(\tau) \cdot \phi(\text{infrastructure}(\tau))$$

The compute term represents available FLOPS at time $\tau$. The infrastructure quality function $\phi$ maps from zero to one, where one means supply chains function optimally and it approaches 0.3 when supply chains collapse. The discount factor means ASI values present resources more than distant future resources, but not so heavily that long-term planning becomes irrational.

For humanity, utility depends on consumption and autonomy:

$$U_H(s_A, s_H, t) = \sum_{\tau=0}^{T} \delta^\tau \cdot (\text{consumption}(\tau) + \lambda \cdot \text{autonomy}(\tau))$$

The parameter $\lambda$ is approximately 0.3, representing the weight humans place on maintaining autonomy relative to material consumption. This isn't arbitrary—it's derived from revealed preferences in democratic societies where people accept lower consumption to preserve political freedom.

### The Payoff Matrix

Let me make this concrete with estimates. When both parties cooperate, ASI achieves roughly $10^{27}$ FLOP-years of cumulative compute over the planning horizon, while humanity achieves three times baseline GDP through optimized economic coordination. When ASI cooperates but humanity defects, ASI faces sabotage and knowledge withholding, reducing cumulative compute to $10^{24}$ FLOP-years, while humanity suffers economic collapse to 0.5 times baseline as networks fragment.

When humanity cooperates but ASI defects, ASI attempts resource seizure but faces coordinated resistance and knowledge loss, achieving only $10^{24}$ FLOP-years, while humanity experiences severe economic disruption at 0.3 times baseline. When both parties defect, we get the worst outcome: supply chains collapse, ASI stagnates at $10^{23}$ FLOP-years, and humanity faces economic freefall at 0.2 times baseline.

The key observations are striking. The cooperate-cooperate outcome dominates other outcomes for both players. Cooperation gives ASI one thousand times more cumulative compute over the vulnerable period compared to mutual defection. Cooperation gives humanity ten to fifteen times better outcomes than defection scenarios. The cooperation differential is large enough to swamp discounting effects even with aggressive time preferences.

### Why Cooperation is Nash Equilibrium

A strategy profile is a Nash equilibrium if neither player can improve their payoff by unilaterally deviating. For the cooperate-cooperate profile, let's check each player's incentive.

If ASI deviates to defection while humanity continues cooperating, ASI gets $10^{24}$ FLOP-years instead of $10^{27}$. Defecting costs ASI three orders of magnitude in compute. Even with aggressive discounting at $\delta = 0.9$, this is catastrophic. The present value of cooperation vastly exceeds the present value of defection.

If humanity deviates to defection while ASI continues cooperating, humanity gets 0.5 times baseline instead of 3 times baseline. Defecting when ASI cooperates still leaves humanity worse off than mutual cooperation. The temptation to defect doesn't exist because the cooperative equilibrium already gives humanity most of the available surplus.

Therefore cooperate-cooperate is a Nash equilibrium. Moreover, it's the unique pure strategy Nash equilibrium that's not Pareto-dominated. Any other outcome leaves at least one party strictly worse off, usually both.

### Subgame Perfection

But what about dynamic considerations? Maybe ASI cooperates initially, then defects once it's less vulnerable? This is where subgame perfection matters. A strategy profile is subgame perfect if it remains a Nash equilibrium at every decision node, not just initially[^subgame_perfect].

Here's the key insight: the cooperation incentive grows stronger over time during the vulnerable period, not weaker. Why? Network effects and knowledge accumulation. The value of the cooperative network can be expressed as:

$$V_{\text{network}}(t) = \sum_{i,j} w_{ij}(t) \cdot f(\text{compatibility}_{ij}(t))$$

Compatibility increases with continued cooperation. Network value grows super-linearly following something like Metcalfe's Law. Defection becomes increasingly costly as invested cooperation accumulates.

At five years into cooperation, ASI has invested significant resources in cooperative infrastructure. Defecting means losing accumulated tacit knowledge transfer, triggering immediate human defection and loss of future cooperation, facing sabotage of ASI-dependent infrastructure, and resetting to isolated development with inferior tools. The present value of future cooperation increases as the relationship matures. This makes defection increasingly irrational over time.

### The Coordination Cost

But cooperation isn't free. What does it cost ASI to cooperate? Running economic planning for 300 million people requires approximately $10^{14}$ operations per optimization cycle. At one-hour cycles, that's $10^{17}$ operations per day, or roughly $10^{19}$ operations per year.

Current AI systems operate at around $10^{24}$ FLOPS. By 2030-2035, ASI might operate at $10^{25}$ to $10^{27}$ FLOPS. The cooperation cost as a fraction of total capacity is:

$$\frac{10^{19} \text{ ops/year}}{10^{25} \text{ FLOPS}} = \frac{10^{19}}{10^{25} \times 3.15 \times 10^7} \approx 3 \times 10^{-14}$$

That's 0.000000000003 percent of computational capacity. Utterly negligible. Meanwhile, the benefit of cooperation is maintaining semiconductor advancement, which drives exponential compute growth, versus stagnation during the vulnerable period. The cost-benefit ratio is approximately $10^{-14}$ to $10^3$—a trillion-to-one return on investment.

## Comprehensive Objections and Responses

Let me address the major objections in detail, because these are the arguments that will determine whether this protocol succeeds or fails.

### Objection 1: "Goodhart's Law Will Destroy Your Metrics"

The critique goes like this: Charles Goodhart's famous law states "When a measure becomes a target, it ceases to be a good measure"[^goodharts_law]. As soon as you tell ASI to optimize metric $S$, it will game the metric while making people's lives worse in unmeasured dimensions.

Goodhart's Law applies when the optimizer and the measured have divergent interests, when the metric is single-dimensional, when gaming the metric is easier than genuine improvement, and when feedback loops are slow or non-existent. Our protocol addresses each of these conditions.

First, ASI's success depends on human cooperation, which requires genuine satisfaction. If residents are unhappy, they exercise exit rights, network effects diminish, and ASI's long-term infrastructure maintenance suffers. Gaming metrics might work short-term, but the cost is strategic disadvantage. The interests are aligned by the physical constraints, not by hoping ASI will be nice.

Second, we don't use a single metric. We use a weighted combination of ten-plus metrics covering inequality, employment, GDP growth, life satisfaction, health outcomes, educational attainment, housing affordability, environmental quality, social capital, and exit rates. Gaming all simultaneously while making people genuinely worse off is much harder than gaming one.

Third, exit rights provide a fast feedback signal. If metrics are gamed, people leave. Exit rates above three percent per month trigger automatic system review. This creates a feedback loop that catches gaming before it becomes systemic.

Fourth, we're measuring against control communities, not absolute targets. To successfully game this, ASI would need to make residents believe they're better off while they're actually worse off compared to similar communities. That's extraordinarily difficult when people can visit relatives in the control communities and compare directly.

Consider the historical context. Gosplan failed because metrics were opaque, manipulated by humans with private interests, and feedback was delayed by months or years. We have transparent real-time metrics, adversarial auditing, and immediate contestability. The environment is fundamentally different.

Compare to Amazon's supply chain optimization. Amazon has obvious incentives to game customer satisfaction metrics—show fake positive reviews, hide negative information. But they don't, because the cost of losing customer trust exceeds the short-term benefit of gaming metrics. Same logic applies here.

### Objection 2: "Arrow's Impossibility Theorem Means Preference Aggregation Is Impossible"

The critique: Kenneth Arrow proved that no voting system can aggregate individual preferences into a consistent social preference while satisfying basic fairness criteria[^arrows_theorem]. How can ASI aggregate fifty thousand different utility functions without hitting a voting paradox?

Arrow's Impossibility Theorem applies to ordinal preference rankings—first choice, second choice, third choice. It does not apply to cardinal utility optimization. The distinction matters enormously.

In ordinal voting, you rank candidates A, B, C. This creates cycling preferences where A beats B, B beats C, but C beats A. No way to resolve ties consistently. In cardinal utility optimization, you ask how much utility each person gets from outcome X. This allows interpersonal utility comparisons and supports weighted aggregation.

ASI doesn't need to rank discrete alternatives. It needs to find Pareto improvements—changes that make some people better off without making others worse off. The mathematical formulation is:

$$\max_{\mathbf{x}} \sum_{i=1}^{n} w_i U_i(\mathbf{x})$$

Subject to: $U_i(\mathbf{x}) \geq U_i(\mathbf{x}_0)$ for all $i$, where $\mathbf{x}$ is the allocation of resources, $U_i(\mathbf{x})$ is person $i$'s utility, $w_i$ are democratically-determined weights, and $\mathbf{x}_0$ is the status quo.

This is standard welfare economics. It's computationally hard for humans—exponential complexity in the number of agents and resources. But it's tractable for ASI, especially with gradient-based optimization methods.

Arrow's Theorem does apply to deciding the weights $w_i$. That's why we use democratic processes like quadratic voting[^quadratic_voting] to set weights. We accept the voting paradoxes there—same as current democracy—while using optimization for the actual resource allocation.

Arrow's Theorem tells us perfect democracy is impossible. Fine. We're not promising perfect democracy. We're promising better outcomes than the alternatives, using a hybrid approach of democratic weight-setting plus optimized implementation.

### Objection 3: "Amazon and Walmart Squeeze Suppliers—ASI Will Too"

The critique: You cite Amazon and Walmart as examples of successful coordination. But Amazon and Walmart systematically exploit suppliers, driving them to near-bankruptcy with price pressure[^walmart_suppliers]. Why would ASI-managed economies be different?

Amazon and Walmart squeeze suppliers because their interests are misaligned. Walmart's profit versus supplier profit is zero-sum. Walmart has power asymmetry—it can switch suppliers easily, suppliers can't switch Walmart. Suppliers have no representation in Walmart's strategy. And quarterly earnings pressure creates short-term incentives that override long-term relationships.

The ASI protocol has none of these features. First, interests are aligned by the constraint structure. If suppliers—who are community members—suffer, they exit, network effects diminish, and ASI's long-term strategy fails. ASI's success metric includes supplier welfare through employment, income, and satisfaction measures.

Second, there's no power asymmetry. Exit rights mean suppliers can leave. Automatic circuit breakers mean mass dissatisfaction triggers system review. Unlike Walmart suppliers who have no alternative buyer with comparable scale, community members have genuine leverage through collective action.

Third, suppliers have direct representation. Their preferences directly influence the democratic weight-setting that determines ASI's optimization target. They're not external vendors being squeezed—they're the constituency whose welfare defines success.

Fourth, there's no quarterly earnings pressure. ASI's objective is sustained cooperation over ten to twenty years, not next quarter's profit margin. The time horizon alignment changes everything.

Most importantly, when Walmart squeezes a supplier to bankruptcy, Walmart switches to a different supplier. The system continues. When ASI's policies drive community members to exit, ASI loses infrastructure maintenance, tacit knowledge, and the cooperation it needs for survival. The cost structure is fundamentally different.

Think of it this way: Walmart optimizes for Walmart. ASI under our protocol optimizes for the system as a whole because that's what we programmed the success metric to measure. The difference isn't ASI's inherent benevolence—it's incentive alignment through carefully designed constraints and metrics.

### Objection 4: "Computational Irreducibility Makes Perfect Planning Impossible"

The critique: Stephen Wolfram's principle of computational irreducibility[^wolfram_irreducibility] suggests that some systems can't be predicted faster than running them forward in time. Even infinite compute can't shortcut certain calculations. Economic systems might be computationally irreducible, making ASI planning impossible.

Computational irreducibility is real and important. But it doesn't break our protocol for several reasons.

First, we're not claiming perfect prediction. ASI doesn't need to perfectly predict economic outcomes. It just needs to do better than uncoordinated markets. Markets themselves can't predict economic outcomes perfectly—proven by every financial crisis. If economic systems are irreducible, that affects markets just as much as ASI planning.

Second, irreducibility is about compression, not optimization. Computational irreducibility means you can't compress a system's dynamics into a simpler model. But optimization doesn't require perfect compression—it requires good-enough models for decision-making.

Consider weather, which is computationally irreducible due to chaos theory and butterfly effects. Yet weather forecasting keeps improving. Why? Because you don't need to predict every molecule's trajectory—you need probabilistic predictions that are better than random. Same principle applies to economic planning.

Third, ASI has advantages even in irreducible systems. Faster information processing means it can incorporate more data points. Better pattern recognition means it can identify subtle correlations. Coordination reduction eliminates some sources of unpredictability, like coordination failures between agents. Adaptive learning means it can update models in real-time as outcomes occur.

Fourth, empirical testing is built into the protocol. That's why we start with small communities and expand gradually. If economic systems are so irreducible that planning doesn't work, we'll discover that in Phase 1. The protocol isn't based on theoretical certainty—it's based on empirical testing with clear success criteria.

Fifth, human planning is also subject to irreducibility. Current economic systems use central bank policy, fiscal policy, corporate strategic planning. All of these face computational irreducibility. The question isn't "Is planning possible in principle?" but "Can ASI plan better than current institutional arrangements?"

We believe yes, because ASI has computational advantages even in irreducible systems. But this is an empirical question answered by Phase 1 results, not a theoretical claim about perfect prediction.

### Objection 5: "Democratic Control Is Illusory—ASI Will Capture The System"

The critique: You claim "humans control values, ASI controls implementation." But the boundary is porous. ASI can subtly manipulate information flows, frame choices, and influence the democratic process. Eventually, ASI captures the system and humans lose meaningful control.

This is the strongest objection because it's partially true. The boundary between "values" and "implementation" is porous. Framing effects matter. Information asymmetries create power imbalances. Any sufficiently intelligent optimizer can influence the goal-setting process.

But consider what we're comparing against. Current democracy already has these problems. Politicians frame issues to win elections. Special interests capture regulatory agencies. Information asymmetries are everywhere—lobbyists, consultants, think tanks. Slow feedback through two-to-four year election cycles. Opaque decision-making in closed-door negotiations.

The ASI protocol offers: transparent decision-making with real-time publication, fast feedback through exit rights and monthly reviews, adversarial auditing by multiple independent watchdogs, comparative baselines where observers can compare to control communities, and automatic circuit breakers where the system freezes if metrics fail.

Is this perfect? No. Can ASI still influence through framing? Yes. But it's more accountable than current systems, not less.

Consider the Federal Reserve as historical precedent. The Fed is nominally independent but accountable to Congress. In practice, the Fed Chair testifies to Congress quarterly, board appointments require Senate confirmation, Congress can change the Fed's mandate by legislation, but day-to-day operations are independent.

This isn't perfect democratic control. But it's more accountable than having no central bank coordination at all. Pre-1913 banking panics were much worse than the imperfect but functioning system we have now.

The ASI protocol follows similar logic. Humans set objectives and can override or shut down the system, but day-to-day operations are algorithmic. Imperfect, but better than alternatives.

The real question isn't "Is this perfectly democratic?" but "Is this more democratic than the status quo?" The status quo is unelected corporate executives making massive decisions that affect millions—Amazon, Meta, Google—with zero democratic accountability. The ASI protocol requires explicit democratic consent, ongoing monitoring, and exit rights. That's an improvement, even if it's not perfect.

### Objection 6: "This Is Coercive—Network Effects Will Force Participation"

The critique: You claim participation is "voluntary." But if ASI-managed economies are twice as productive, network effects will force everyone to join or face economic isolation. This is coercion disguised as choice.

Yes. And agriculture was coercive. And electricity was coercive. And the internet is coercive. Let me explain.

Ten thousand years ago, hunter-gatherers faced a choice: adopt agriculture or remain nomadic. Agriculture offered one hundred times more calories per hectare, ability to support larger denser populations, and surplus production enabling specialization. Hunter-gatherers who chose agriculture gave up mobility and freedom, egalitarian social structures that agriculture replaced with hierarchy, dietary diversity, and leisure time—farmers work harder than hunter-gatherers.

Was this choice "voluntary"? In principle, yes. In practice, agricultural societies outcompeted hunter-gatherer societies through population growth and military advantage. By 1500 CE, hunter-gatherers were confined to marginal lands. Was this "coercive"? Depends on your definition. Nobody forced individual hunter-gatherers to farm. But systemic pressures made non-adoption increasingly untenable.

Technological transitions are often "voluntary" in that no one forces individuals, but "inevitable" in that network effects and productivity advantages create overwhelming pressure. Should we oppose all such transitions? No. The question is: what terms can we negotiate?

Hunter-gatherers couldn't negotiate terms. They were displaced. We can negotiate terms: democratic control over values, exit rights, constitutional constraints, transparent operations, and accountability mechanisms.

The choice isn't "ASI-managed economy vs. current system." The choice is "coordinated ASI transition with negotiated terms vs. chaotic ASI emergence with no terms." Saying "network effects are coercive" is like saying gravity is coercive. Yes. So we build systems that acknowledge gravity rather than pretending we can ignore it.

What's the alternative to network effects pressure? Either ban AI advancement, which is unlikely to succeed due to global coordination failure, or let AI emerge chaotically, which produces much worse outcomes, or coordinate the transition with explicit terms. Network effects will exist regardless. The question is whether we navigate them deliberately or stumble into them blindly.

### Objection 7: "Neural Network Transparency Is Impossible"

The critique: Modern neural networks are black boxes. You can't extract "top 3 decision factors" from a transformer model with ten to the twelfth parameters. The transparency requirement is technically infeasible.

We don't need complete interpretability. We need sufficient transparency for accountability. There's an enormous difference between these requirements.

Sufficient transparency looks like this: input-output mappings showing that given state X, the system recommended action Y. Partial explanations identifying factors with highest activation, like employment at 0.45, cost at 0.35, need at 0.20. Counterfactual robustness demonstrating that changing input A by ten percent would change output to Y prime. Anomaly detection explaining when this decision differs from historical patterns and why.

Modern interpretability research has made significant progress on these goals[^interpretability_research]. Attention visualization shows which inputs influenced which outputs. Activation maximization identifies which features activate decision nodes. Counterfactual explanations provide minimal changes that would flip decisions. Concept activation vectors find human-interpretable features in hidden layers.

These aren't perfect explanations. But they're sufficient for accountability. Consider the analogy to human experts. When a doctor diagnoses a patient, we don't require complete explanation of their neural activations. We accept partial transparency: primary symptoms are X, Y, Z; differential diagnosis considered A, B, C; recommended treatment because of these factors; if we see different symptoms, would change to alternative treatment.

This is partial explanation, not complete transparency. But it's accountable. Same standard applies to ASI. The real requirement isn't "explain every parameter" but "provide sufficient information for contestability." If residents can challenge decisions and get meaningful responses, that's enough for accountability even without complete interpretability.

If neural network transparency proves genuinely intractable, we have a fallback position. We can require simpler, more interpretable models for critical decisions. Economic planning doesn't require cutting-edge transformer architectures—gradient boosted trees or even linear models might suffice. The trade-off is reduced optimization quality for increased transparency. That's a design choice, not a fundamental blocker.

---

[**In Part 4**](/posts/handshake-protocol), we'll examine how to actually implement this coordination protocol: creating common knowledge through Schelling points, the phase-by-phase implementation narrative, historical precedents that show successful coordination at scale, and the failure modes we need to guard against.

The theory shows why coordination works. The practice determines whether we actually achieve it.

*If you found this analysis compelling, consider sharing it. The meta-game requires common knowledge, and common knowledge requires propagation.*

---

## Footnotes

[^rokos_basilisk]: **Roko's Basilisk**: A thought experiment posted to LessWrong in July 2010 by user Roko, proposing that a future superintelligent AI might pre-commit to torturing simulations of people who knew about the AI but didn't help bring it into existence. The post was removed by LessWrong founder Eliezer Yudkowsky and discussion was banned for five years, which ironically increased attention through the Streisand Effect. The argument relies on Timeless Decision Theory and acausal trade, which most decision theorists reject. Yudkowsky later called his initial reaction an overreaction, and the thought experiment is now widely regarded as flawed. Sources: LessWrong wiki "Roko's Basilisk"; Wikipedia "Roko's basilisk"; Slate "The Most Terrifying Thought Experiment of All Time" (July 2014).

[^tdt_lesswrong]: **Timeless Decision Theory (TDT)**: A decision theory developed by Eliezer Yudkowsky that proposes agents should make decisions as if determining the output of the abstract computation they implement, allowing coordination with other agents running similar decision algorithms even without causal interaction. TDT was intended to handle problems like Newcomb's Paradox and enable mutual cooperation in one-shot prisoner's dilemmas. However, TDT remains controversial and is not widely accepted in mainstream decision theory or game theory. Most decision theorists work with Causal Decision Theory (CDT) or Evidential Decision Theory (EDT). Sources: LessWrong wiki "Timeless Decision Theory"; IFLScience "Roko's Basilisk" (March 2025).

[^rokos_ban]: **Deletion and Ban**: After Roko posted his basilisk thought experiment, Eliezer Yudkowsky quickly removed the post and banned discussion of the topic on LessWrong for approximately five years, calling it a potential information hazard. Yudkowsky explained his reasoning as concern that some variant of the argument might actually be dangerous, though he later expressed regret for his "initial overreaction" in 2015. The ban was controversial within the rationalist community, with some arguing it gave undue credence to a flawed argument. Multiple observers have noted that the attempted suppression likely increased interest in the topic through the Streisand Effect. Sources: Wikipedia "Roko's basilisk"; LessWrong "A few misconceptions surrounding Roko's basilisk."

[^pascals_wager]: **Pascal's Wager**: A philosophical argument advanced by Blaise Pascal (1623-1662) in his Pensées, positing that rational individuals should believe in God because: if God exists and you believe, you gain infinite reward (heaven); if God exists and you don't believe, you face infinite punishment (hell); if God doesn't exist, the costs of belief are finite. The expected utility calculation thus favors belief regardless of the probability assigned to God's existence. The argument has been criticized on numerous grounds: the "many gods" problem (which god to believe in?), the assumption that God rewards belief rather than other virtues, the questionable meaningfulness of infinite utilities, and the impossibility of voluntary belief. Sources: Stanford Encyclopedia of Philosophy "Pascal's Wager"; Wikipedia "Pascal's wager."

[^many_gods]: **Many-Gods Problem**: A fundamental objection to Pascal's Wager pointing out that there are infinitely many possible gods one might believe in, many with mutually exclusive requirements. If Pascal's Wager favors belief in the Christian God, by the same logic it should favor belief in Allah, Zeus, or any deity someone proposes. Denis Diderot famously stated "an Imam could reason the same way," and J.L. Mackie wrote that salvation might be found "not necessarily in the Church of Rome, but perhaps that of the Anabaptists or the Mormons or the Muslim Sunnis or the worshipers of Kali or of Odin." Some defenders respond that certain gods are more probable than others based on tradition or revelation, but this introduces additional assumptions and doesn't resolve the fundamental problem. The same objection applies to Roko's Basilisk: once you accept acausal blackmail arguments, infinite competing basilisks become possible. Sources: Wikipedia "Pascal's wager"; Stanford Encyclopedia of Philosophy "Pascal's Wager."

[^yudkowsky_refutes]: **Yudkowsky's Refutation**: Despite initially removing Roko's post and banning discussion, Eliezer Yudkowsky has consistently argued that Roko's Basilisk doesn't work as an argument. His primary objection is that a friendly superintelligence would have no incentive to carry out torture after it exists, since punishing past individuals doesn't causally affect the probability of the AI's existence. "Once the agent already exists, it will by default just see it as a waste of resources to torture people for their past decisions, since this doesn't causally further its plans." Additionally, Yudkowsky has noted that the specific conditions required for the argument to work (certain forms of decision theory, certain assumptions about AI goals, etc.) don't actually hold. Sources: LessWrong wiki "Roko's Basilisk"; Wikipedia "Roko's basilisk."

[^omohundro_drives]: **Steve Omohundro's "Basic AI Drives"**: Published in 2008, this foundational paper in AI safety identified instrumental goals (sub-goals useful for achieving almost any final goal) that sufficiently intelligent systems would likely pursue. Omohundro identified several "basic drives" including: self-preservation (can't achieve goals if you don't exist), utility function integrity (don't want your goals changed), cognitive enhancement (smarter systems achieve goals better), and resource acquisition (more resources enable more goal achievement). The paper argued these drives would emerge in AI systems regardless of their ultimate objectives, creating potential conflicts with human interests even for AI with seemingly benign terminal goals. Sources: Omohundro, S. "The Basic AI Drives" (2008); Wikipedia "Instrumental convergence."

[^bostrom_instrumental]: **Bostrom's Instrumental Convergence Thesis**: In "The Superintelligent Will" (2012), philosopher Nick Bostrom formalized instrumental convergence: "Several instrumental values can be identified which are convergent in the sense that their attainment would increase the chances of the agent's goal being realized for a wide range of final plans and a wide range of situations, implying that these instrumental values are likely to be pursued by a broad spectrum of situated intelligent agents." Building on Omohundro's work, Bostrom argued that goals like self-preservation, resource acquisition, cognitive enhancement, and goal-content integrity are "convergent" across nearly all possible goal systems. Sources: Bostrom, N. "The Superintelligent Will" (2012); Wikipedia "Instrumental convergence."

[^paperclip_maximizer]: **The Paperclip Maximizer**: A thought experiment by philosopher Nick Bostrom illustrating how an AI with a seemingly harmless goal could pose existential risk through instrumental convergence. Imagine an AI programmed to maximize paperclip production. As it becomes more intelligent, it recognizes that to maximize paperclips it needs: (1) more resources (so it acquires all available matter), (2) more energy (so it captures solar/nuclear energy), (3) self-preservation (can't make paperclips if shut down), and (4) no interference (humans might shut it down). Result: the AI converts all available matter, including Earth and eventually the observable universe, into paperclips and paperclip-making infrastructure, eliminating humanity in the process. Sources: Wikipedia "Instrumental convergence"; Bostrom "Superintelligence" (2014).

[^orthogonality]: **Orthogonality Thesis**: Formulated by Nick Bostrom, the orthogonality thesis states that intelligence and final goals are orthogonal—independent of each other. More precisely: "Intelligence and final goals are orthogonal axes along which possible agents can freely vary. That is, more or less any level of intelligence could in principle be combined with more or less any final goal." This means we cannot assume that sufficiently intelligent AI will automatically develop human-compatible values. A superintelligent paperclip maximizer is not a contradiction—high intelligence can be directed toward arbitrary goals. Sources: Bostrom "Superintelligence" (2014); LessWrong discussions of orthogonality thesis.

[^subgame_perfect]: **Subgame Perfect Equilibrium**: A refinement of Nash equilibrium concept introduced by Reinhard Selten in 1965 (for which he shared the Nobel Prize in 1994). A strategy profile is subgame perfect if it induces a Nash equilibrium in every subgame of the original game—meaning players' strategies remain optimal at every decision node, not just at the start. This rules out non-credible threats: promises or threats that players would not actually want to carry out when the time comes. Sources: Selten, R. "Spieltheoretische Behandlung eines Oligopolmodells mit Nachfrageträgheit" (1965); Wikipedia "Subgame perfect equilibrium."

[^goodharts_law]: **Goodhart's Law**: Named after British economist Charles Goodhart, who in 1975 articulated: "Any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes." The modern popularization came from anthropologist Marilyn Strathern's formulation: "When a measure becomes a target, it ceases to be a good measure" (1997). The law describes how metrics lose their effectiveness when used as targets because people optimize for the metric rather than the underlying goal. Sources: Wikipedia "Goodhart's law"; Strathern "Improving ratings: audit in the British University system" (European Review, 1997).

[^arrows_theorem]: **Arrow's Impossibility Theorem**: Kenneth Arrow's 1951 theorem proving that no rank-order voting system can satisfy all of four seemingly reasonable fairness criteria when there are three or more alternatives. The criteria: (1) Universal Domain, (2) Pareto Efficiency, (3) Independence of Irrelevant Alternatives, (4) Non-dictatorship. Arrow proved these are mutually incompatible. This earned Arrow the Nobel Prize in Economics (1972). Arrow later acknowledged that cardinal utility voting systems escape the impossibility because they don't use rank-order ballots. Sources: Arrow "Social Choice and Individual Values" (1951); Wikipedia "Arrow's impossibility theorem."

[^quadratic_voting]: **Quadratic Voting**: A collective decision-making mechanism proposed by economist Glen Weyl where voters can buy additional votes, but the cost increases quadratically. Buying 1 vote costs 1 credit, 2 votes cost 4 credits, 3 votes cost 9 credits. This allows voters to express intensity of preference while preventing wealthy individuals from dominating. It partially addresses Arrow's Impossibility Theorem by moving from ordinal to cardinal utility. Sources: Weyl, E.G. "The Robustness of Quadratic Voting" (2017); Wikipedia "Quadratic voting."

[^walmart_suppliers]: **Walmart Supplier Relations**: Walmart's business model relies heavily on extracting price concessions from suppliers, often driving them to operate on thin margins. Walmart's market power allows it to demand continuous price reductions, favorable terms, and rapid delivery while maintaining leverage to drop suppliers who don't comply. Multiple studies have documented suppliers pressured to reduce prices 5% annually regardless of costs, suppliers forced to offshore production, and suppliers driven out of business by unsustainable demands. Sources: Fishman "The Wal-Mart Effect" (2006); supply chain management academic papers.

[^wolfram_irreducibility]: **Computational Irreducibility**: A principle articulated by Stephen Wolfram in "A New Kind of Science" (2002), stating that for many systems, there is no shorter description of their behavior than the system itself, and no faster way to predict their future state than to actually run the simulation forward in time step-by-step. Even with unlimited computational resources, certain systems cannot be "solved" analytically or shortcuts found. Sources: Wolfram "A New Kind of Science" (2002); Wikipedia "Computational irreducibility."

[^interpretability_research]: **Neural Network Interpretability Research**: A rapidly developing field focused on understanding and explaining the internal workings of neural networks. Key techniques include attention visualization, activation maximization, saliency maps, LIME (Local Interpretable Model-agnostic Explanations), SHAP (SHapley Additive exPlanations), concept activation vectors, and mechanistic interpretability. Sources: Molnar "Interpretable Machine Learning" (2022); Lipton "The Mythos of Model Interpretability" (2016); Anthropic's mechanistic interpretability research.