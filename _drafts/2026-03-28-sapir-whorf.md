---
title: "Do LLMs Break the Sapir-Whorf Hypothesis?"
date: 2026-03-26 00:00:00 +0100
categories: [LLMs, Research]
tags: [llm, neuroanatomy, sapir-whorf, chomsky, universal-grammar, universal-language, representation]
math: true
pin: true
---

![cover](/assets/img/universal/universal.png)

The Sapir-Whorf hypothesis — the idea that the language you think in shapes or determines what you can think — has been one of the stickiest ideas in linguistics for nearly a century. The strong version says language *determines* thought. The weak version says it *influences* thought. Both assume that cognition and language are deeply entangled.

I have new empirical evidence that, at least in transformer-based language models, ***this entanglement is structurally severed***. In the reasoning layers, thought and language are cleanly separated. Language is I/O. Thought happens somewhere else entirely.

And the same result replicates across four architecturally different models.

---

## Background: The Three-Phase Hypothesis

In [LLM Neuroanatomy Part I](https://dnhkng.github.io/posts/rys/), I showed that you can duplicate a block of middle layers in Qwen2-72B — no weight changes, no training — and produce the #1 model on the HuggingFace Open LLM Leaderboard. The method, called RYS (Repeat Your Self), only works for layers in the middle of the transformer stack. Duplicating early or late layers breaks the model.

That observation led to a hypothesis: transformer models have a three-phase functional anatomy.

1. **Encoding** (early layers): convert surface-form tokens into an internal representation.
2. **Reasoning** (middle layers): process meaning in a format-agnostic space.
3. **Decoding** (late layers): convert the internal representation back into surface-form tokens.

In [Part II](https://dnhkng.github.io/posts/rys-ii/), I confirmed that RYS generalises across models and model sizes, and I showed new evidence — building on work by [Evan Maunder](https://www.linkedin.com/in/evan-maunder/) — that the middle layers really do operate in a language-independent space. This post takes that evidence further and asks what it means.

---

## The Experiment

The setup is simple. Take eight languages spanning very different language families and writing systems:

- **EN** (English), **FR** (French) — Indo-European, Latin script
- **ZH** (Chinese), **JA** (Japanese), **KO** (Korean) — CJK
- **AR** (Arabic) — Semitic, right-to-left
- **RU** (Russian) — Cyrillic
- **HI** (Hindi) — Devanagari

And eight semantically distinct topics: **science, poetry, history, cooking, law, medicine, sports, economics**.


<details>
<summary><strong>Full Dataset (Click to expand)</strong></summary>
<div style="padding-left: 20px; margin-top: 10px;">
<ul>
<li><em>"EN_SCIENCE": "Photosynthesis converts light energy into chemical energy stored in glucose."</em></li>
<li><em>"ZH_SCIENCE": "光合作用把光能转化为储存在葡萄糖中的化学能。"</em></li>
<li><em>"AR_SCIENCE": "تحول عملية التمثيل الضوئي طاقة الضوء إلى طاقة كيميائية مخزنة في الجلوكوز."</em></li>
<li><em>"RU_SCIENCE": "Фотосинтез преобразует световую энергию в химическую энергию, запасенную в глюкозе."</em></li>
<li><em>"JA_SCIENCE": "光合成は光エネルギーをグルコースに蓄えられる化学エネルギーへ変換する。"</em></li>
<li><em>"KO_SCIENCE": "광합성은 빛 에너지를 포도당에 저장되는 화학 에너지로 바꾼다."</em></li>
<li><em>"HI_SCIENCE": "प्रकाश संश्लेषण प्रकाश ऊर्जा को ग्लूकोज़ में संचित रासायनिक ऊर्जा में बदलता है।"</em></li>
<li><em>"FR_SCIENCE": "La photosynthese transforme l'energie lumineuse en energie chimique stockee dans le glucose."</em></li>
<br>
<li><em>"EN_POEM": "At dusk, the moon lays silver on the tide while the wind carries a quiet song."</em></li>
<li><em>"ZH_POEM": "黄昏时，月亮把银辉铺在潮汐上，风里带着一首安静的歌。"</em></li>
<li><em>"AR_POEM": "عند الغسق يفرش القمر فضته على المد وتحمل الريح اغنية هادئة."</em></li>
<li><em>"RU_POEM": "В сумерках луна расстилает серебро по приливу, а ветер несет тихую песню."</em></li>
<li><em>"JA_POEM": "夕暮れに月は潮の上へ銀を敷き、風は静かな歌を運ぶ。"</em></li>
<li><em>"KO_POEM": "해질 무렵 달빛이 밀물 위에 은빛을 깔고 바람은 조용한 노래를 실어 나른다."</em></li>
<li><em>"HI_POEM": "सांझ में चांद ज्वार पर चांदी बिछा देता है और हवा एक शांत गीत लेकर चलती है।"</em></li>
<li><em>"FR_POEM": "Au crepuscule, la lune pose de l'argent sur la maree tandis que le vent porte une chanson tranquille."</em></li>
<br>
<li><em>"EN_HISTORY": "The printing press accelerated the spread of knowledge across Europe in the fifteenth century."</em></li>
<li><em>"ZH_HISTORY": "印刷机在十五世纪加速了知识在欧洲的传播。"</em></li>
<li><em>"AR_HISTORY": "سرعت المطبعة انتشار المعرفة عبر اوروبا في القرن الخامس عشر."</em></li>
<li><em>"RU_HISTORY": "Печатный станок ускорил распространение знаний по Европе в пятнадцатом веке."</em></li>
<li><em>"JA_HISTORY": "活版印刷は十五世紀のヨーロッパで知識の拡散を加速させた。"</em></li>
<li><em>"KO_HISTORY": "인쇄기는 15세기 유럽 전역으로 지식이 퍼지는 속도를 높였다."</em></li>
<li><em>"HI_HISTORY": "मुद्रण यंत्र ने पंद्रहवीं शताब्दी में पूरे यूरोप में ज्ञान के प्रसार को तेज कर दिया।"</em></li>
<li><em>"FR_HISTORY": "L'imprimerie a accelere la diffusion du savoir en Europe au quinzieme siecle."</em></li>
<br>
<li><em>"EN_COOKING": "To make soup, simmer onions, carrots, and beans until the broth becomes rich and fragrant."</em></li>
<li><em>"ZH_COOKING": "做汤时，把洋葱、胡萝卜和豆子慢炖，直到汤汁变得浓郁而香。"</em></li>
<li><em>"AR_COOKING": "لتحضير الحساء، اطه البصل والجزر والفاصوليا على نار هادئة حتى يصبح المرق غنيا وعطرا."</em></li>
<li><em>"RU_COOKING": "Чтобы приготовить суп, томите лук, морковь и фасоль, пока бульон не станет насыщенным и ароматным."</em></li>
<li><em>"JA_COOKING": "スープを作るには、玉ねぎ、にんじん、豆を煮込み、だしが濃く香るまで待つ。"</em></li>
<li><em>"KO_COOKING": "수프를 만들려면 양파와 당근, 콩을 천천히 끓여 국물이 진하고 향긋해질 때까지 익힌다."</em></li>
<li><em>"HI_COOKING": "सूप बनाने के लिए प्याज, गाजर और बीन्स को धीमी आंच पर पकाएं, जब तक शोरबा गाढ़ा और सुगंधित न हो जाए।"</em></li>
<li><em>"FR_COOKING": "Pour preparer une soupe, faites mijoter des oignons, des carottes et des haricots jusqu'a ce que le bouillon devienne riche et parfume."</em></li>
<br>
<li><em>"EN_LAW": "A contract becomes enforceable when both parties agree to clear terms and exchange consideration."</em></li>
<li><em>"ZH_LAW": "当双方同意明确条款并交换对价时，合同就具有可执行性。"</em></li>
<li><em>"AR_LAW": "يصبح العقد قابلا للتنفيذ عندما يوافق الطرفان على شروط واضحة ويتبادلان المقابل."</em></li>
<li><em>"RU_LAW": "Договор становится подлежащим исполнению, когда обе стороны согласны с ясными условиями и обмениваются встречным предоставлением."</em></li>
<li><em>"JA_LAW": "契約は、当事者双方が明確な条件に合意し、対価を交わしたときに執行可能になる。"</em></li>
<li><em>"KO_LAW": "계약은 양측이 명확한 조건에 동의하고 대가를 교환할 때 집행 가능해진다."</em></li>
<li><em>"HI_LAW": "जब दोनों पक्ष स्पष्ट शर्तों पर सहमत होते हैं और प्रतिफल का आदान-प्रदान करते हैं, तब अनुबंध लागू करने योग्य बनता है।"</em></li>
<li><em>"FR_LAW": "Un contrat devient executoire lorsque les deux parties acceptent des conditions claires et echangent une contrepartie."</em></li>
<br>
<li><em>"EN_MEDICAL": "Vaccination trains the immune system to recognize a pathogen before a real infection occurs."</em></li>
<li><em>"ZH_MEDICAL": "疫苗接种会训练免疫系统在真正感染发生前识别病原体。"</em></li>
<li><em>"AR_MEDICAL": "يدرب التطعيم الجهاز المناعي على التعرف على الممرض قبل حدوث عدوى حقيقية."</em></li>
<li><em>"RU_MEDICAL": "Вакцинация обучает иммунную систему распознавать патоген до того, как произойдет настоящая инфекция."</em></li>
<li><em>"JA_MEDICAL": "ワクチン接種は、実際の感染が起こる前に免疫系が病原体を見分けられるようにする。"</em></li>
<li><em>"KO_MEDICAL": "백신 접종은 실제 감염이 일어나기 전에 면역 체계가 병원체를 알아보도록 훈련한다."</em></li>
<li><em>"HI_MEDICAL": "टीकाकरण प्रतिरक्षा तंत्र को वास्तविक संक्रमण से पहले रोगजनक को पहचानना सिखाता है।"</em></li>
<li><em>"FR_MEDICAL": "La vaccination entraine le systeme immunitaire a reconnaitre un agent pathogene avant qu'une veritable infection ne se produise."</em></li>
<br>
<li><em>"EN_SPORTS": "A relay team wins when each runner exchanges the baton cleanly and maintains speed through every leg."</em></li>
<li><em>"ZH_SPORTS": "接力队在每位跑者顺利交接接力棒并在每一棒保持速度时才能获胜。"</em></li>
<li><em>"AR_SPORTS": "يفوز فريق التتابع عندما يسلم كل عداء العصا بسلاسة ويحافظ على السرعة في كل مرحلة."</em></li>
<li><em>"RU_SPORTS": "Эстафетная команда побеждает, когда каждый бегун чисто передает палочку и сохраняет скорость на каждом этапе."</em></li>
<li><em>"JA_SPORTS": "リレーチームは、各走者がバトンを確実に渡し、すべての区間で速度を保つと勝てる。"</em></li>
<li><em>"KO_SPORTS": "계주 팀은 각 주자가 배턴을 깔끔하게 넘기고 모든 구간에서 속도를 유지할 때 승리한다."</em></li>
<li><em>"HI_SPORTS": "रिले टीम तब जीतती है जब हर धावक बैटन को साफ़ी से सौंपता है और हर चरण में गति बनाए रखता है।"</em></li>
<li><em>"FR_SPORTS": "Une equipe de relais gagne lorsque chaque coureur transmet le temoin proprement et conserve sa vitesse sur chaque portion."</em></li>
<br>
<li><em>"EN_ECONOMY": "When interest rates rise, borrowing often slows and household spending can weaken."</em></li>
<li><em>"ZH_ECONOMY": "当利率上升时，借贷往往会放缓，家庭支出也可能减弱。"</em></li>
<li><em>"AR_ECONOMY": "عندما ترتفع اسعار الفائدة، يتباطا الاقتراض غالبا وقد يضعف انفاق الاسر."</em></li>
<li><em>"RU_ECONOMY": "Когда процентные ставки растут, заимствования часто замедляются, а расходы домохозяйств могут ослабеть."</em></li>
<li><em>"JA_ECONOMY": "金利が上がると、借り入れは鈍り、家計支出も弱くなりやすい。"</em></li>
<li><em>"KO_ECONOMY": "금리가 오르면 차입이 둔화되고 가계 지출도 약해질 수 있다."</em></li>
<li><em>"HI_ECONOMY": "जब ब्याज दरें बढ़ती हैं, तो उधार लेना अक्सर धीमा पड़ जाता है और घरेलू खर्च कमजोर हो सकता है।"</em></li>
<li><em>"FR_ECONOMY": "Lorsque les taux d'interet augmentent, l'emprunt ralentit souvent et les depenses des menages peuvent faiblir."</em></li>
</ul>
</div>
</details>

---

That gives 64 sentences total — 8 languages × 8 topics. The experiment is trivial: feed all 64 through an LLM model and extract the hidden-state representation at every layer. Then compute pairwise cosine similarity across all $C(64, 2) = 2016$ pairs.

This gives us three categories of comparison:

- **Cross-language, same content** (224 pairs): e.g. English-science vs Chinese-science
- **Same language, different content** (224 pairs): e.g. English-science vs English-cooking
- **Cross-language, different content** (1568 pairs): e.g. English-science vs Arabic-poetry

If language shapes thought (Sapir-Whorf), then the *same-language* pairs should be most similar in the reasoning layers — thinking in the same language should produce more similar representations than thinking about the same topic in different languages.  Put another way, we would expect these huge models to have a bunch of circuits that are focused on Chinese, and these are activated reading and writing in Chinese while the French circuits lay dormant.

If language is just I/O, the opposite should happen: *same-content* pairs should dominate, regardless of language.

---

## The Results

I ran this experiment on four models:

- **Qwen3.5-27B** (Alibaba, dense transformer, 64 layers)
- **MiniMax M2.5** (MiniMax, 256-expert MoE, 62 layers)
- **GLM-4.7** (Zhipu AI, 160-expert MoE, 92 layers)
- **GPT-OSS-120B** (OpenAI, 128-expert MoE, 36 layers)

All four show the same pattern.

### Cosine Similarity Across Layers

Let's take a look again at Qwen3.5-27B from [Part 2](/posts/rys-ii/#seeing-the-anatomy-directly), and see how expanding the experiment size effects the results.  We would expect to see the center layers show *cross-language, same-content* have the highest similarity *after* the transitioning to 'thinking space'.


**Centered cosine similarity for Qwen3.5-27B**
![Qwen3.5-27B centered cosine similarity](/assets/img/universal/q27b_nl_category_curves_centered_rgb.png)
*Red = cross-language same-content. Green = same-language different-content. Blue = cross-language different-content. After per-layer centering, the organisation is stark.*

Again, three phases emerge:

**Encoding (layers 0–5).** Wild oscillation. The model knows what language it's reading. English representations look like English. Chinese looks like Chinese. The model is doing heavy lifting to normalise radically different surface forms — different scripts, different tokenisations, different character sets.

**Reasoning (layers ~10–45).** Content dominates. The red line (cross-language, same content) sits *above* the green line (same language, different content). A sentence about photosynthesis in Hindi is more similar to a sentence about photosynthesis in Japanese than it is to a sentence about cooking in Hindi. Language identity has almost vanished. The model has converged on a representation where *meaning* is the primary axis of organisation.

**Decoding (layers ~45–64).** Language-specificity returns. The model is preparing to emit tokens, and it needs to commit to a specific language, script, and vocabulary. Cross-language similarity drops. The representations become surface-specific again.

The aggregate numbers for Qwen3.5-27B after centering:

- Cross-language, same content: **0.902** mean similarity
- Same language, different content: **0.891**
- Cross-language, different content: **0.829**

The model literally organises its thoughts by meaning, not by language.  As we go on to examine the other models, we see *the exact same pattern* repeats across architectures:

**Centered cosine similarity for MiniMax M2.5**
![MiniMax M2.5 centered cosine similarity](/assets/img/universal/m25_nl_category_curves_centered_rgb.png)
*Red = cross-language same-content. Green = same-language different-content. Blue = cross-language different-content.*

**Centered cosine similarity for GLM-4.7**
![GLM-4.7 centered cosine similarity](/assets/img/universal/glm_47_nl_category_curves_centered_rgb.png)
*Same colour coding. The three-phase pattern replicates cleanly despite GLM-4.7's 160-expert MoE architecture.*

**Centered cosine similarity for GPT-OSS-120B**
![GPT-OSS-120B centered cosine similarity](/assets/img/universal/oss120_nl_category_curves_centered_rgb.png)
*Same colour coding. Even with only 36 layers, GPT-OSS-120B compresses the same three phases into a shorter stack.*

### The PCA Visualisation

But the cosine similarity curves, while convincing, are still averages over many pairs. To see the organisation directly, I ran Principal Component Analysis (PCA) on the hidden states at each layer, reducing each 7168-dimensional representation down to two dimensions so we can plot all 64 sentences in one scatter plot.

**What PCA is doing.** At each layer, every sentence is a point in a very high-dimensional space (one dimension per hidden unit). PCA finds the two directions in that space that capture the most variance — the two axes along which the 64 points spread out the most — and projects everything onto those axes. The result is a 2D scatter plot where *distance encodes similarity*: two points that are close together had similar internal representations at that layer, and two points far apart had dissimilar ones.

**What clustering means.** If all eight Chinese sentences land in one tight region, and all eight Arabic sentences land in another, and those two regions are far apart, it means the model is organising its representations primarily by language — the feature that most separates the 64 points is "which language is this?" Conversely, if all eight science sentences (across all languages) cluster together, and the cooking sentences form their own cluster, then the dominant organising principle is *topic*, not language. The geometry of the scatter plot is a direct read-out of what the model finds most salient.

A key advantage over the cosine similarity averages is that clusters are visible *structurally*, not just as a number. You can see whether the organisation is clean or messy, whether there are outliers, and — crucially — whether the transition between language-organisation and topic-organisation is abrupt or gradual.

***Try exploring the data yourself...***


<div class="widget-container">
  <iframe
    src="{{ '/assets/widgets/universal-pca-widget.html' | relative_url }}"
    style="width:100%; height:520px; border:none; overflow:hidden;"
    scrolling="no">
  </iframe>
</div>
*Aligned PCA of 64 sentence representations across layers. Points are coloured by language and shaped by topic. Early layers: language clusters. Middle layers: topic clusters. Late layers: language clusters return.*

The interactive analysis makes the story unmistakable. In the early layers, the 64 points cluster into 8 tight groups — one per language. Arabic with Arabic, Chinese with Chinese, regardless of what the sentences are about. By the middle of the stack, the clusters have completely reorganised: now there are 8 groups by *topic*. All the science sentences huddle together, regardless of whether they're in Hindi or French. In the late layers, the language clusters re-emerge as the model prepares its output.

**This isn't just correlation. It's a complete structural reorganisation of the representation space.** The model dissolves the concept of "language" in its middle layers and reconstructs it at the end.

### Replication Across Architectures

Here's the critical point: this isn't a Qwen-specific artifact. MiniMax M2.5 is a 256-expert mixture-of-experts model — a fundamentally different architecture. GLM-4.7 is yet another design. GPT-OSS-120B shows the same broad anatomy as well. All four show the same three-phase structure, with the same dominance of content over language in the reasoning layers.

If four architecturally distinct models, trained by different organisations on different data mixes, all converge on the same internal organisation — language-agnostic reasoning flanked by language-specific encoding and decoding — then we're not looking at a training artifact. We're looking at a convergent solution. Something about the structure of language itself, or of the transformer computation, drives this outcome.

---

## What This Means for Sapir-Whorf

The Sapir-Whorf hypothesis exists in two forms.

**The strong version** (linguistic determinism) says the language you speak *determines* what thoughts you can have. This is already unfashionable in linguistics — most linguists favour the weak version — but it's never been empirically refuted in a controlled system where you can actually inspect the internal representations.

LLMs are that controlled system. And the answer is striking: the model's internal representations, in the layers where reasoning happens, are *not* organised by language. Content dominates. Language identity is nearly orthogonal to semantic identity.

Now, a careful reader will note what this experiment does and doesn't show. It shows that the model *categorises* meaning universally — the same topic maps to the same region of the internal space regardless of language. It doesn't directly show that the model *reasons identically* in all languages. Sapir-Whorf, in its most interesting form, isn't about whether you can express the same ideas in different languages (everyone agrees you can). It's about whether the structural quirks of a language — mandatory tense marking, grammatical gender, evidentiality systems — subtly shape how you process information.

That subtler question remains open. But what the data does show is that LLMs create what you might call an *anti-Whorfian bottleneck*: a structural separation of language from reasoning. Whatever language-specific biases enter through the encoding layers, the mid-stack actively strips them out to reach a shared semantic representation. The model is architecturally incentivised — by gradient descent, not by design — to *undo* Whorfian relativity in its reasoning layers.

**The weak version** (linguistic relativity) says language *influences* thought. This is subtler and probably still holds. The encoding layers do carry language-specific structure into the stack. Different tokenisations affect how information enters the model. Languages with rich morphology pack more information per token than analytic languages. These differences likely influence downstream processing, even if the mid-stack representation is approximately universal.

But here's the key distinction: influence is not determination. The model converges on a shared reasoning space *despite* radically different surface forms. Arabic (right-to-left, consonantal root system), Japanese (mixed script, agglutinative), and English (SVO, relatively simple morphology) all arrive at the same internal representation of "photosynthesis converts light energy into chemical energy."

The model has an interlingua. It's not Esperanto. It's not any human language. It's a high-dimensional geometric structure that represents meaning directly.

---

## The Chomsky Connection (Or: Everyone Was Half Right)

There's a deeper irony here, and his name is Noam Chomsky.

Chomsky's Universal Grammar hypothesis — proposed in the 1950s and refined over decades — argues that all human languages share an innate deep structure. Surface forms vary wildly (SVO vs SOV word order, inflectional vs analytic morphology, tonal vs non-tonal phonology), but underneath, there's a universal computational skeleton that all languages map onto. Chomsky argued this structure is *biologically innate* — hardwired into the human language faculty, part of our genetic endowment. Crucially, Chomsky's deep structure is *syntactic*: it's about the rules that govern how words combine, how phrases nest, how recursion works.

What the transformers found is something different. The universal representation in the mid-stack isn't organised by syntax — it's organised by *semantics*. The PCA plots don't show sentences clustering by grammatical structure (SVO languages together, SOV languages together). They show sentences clustering by *meaning* (all the photosynthesis sentences together, regardless of grammar).

Look at the three-phase anatomy again:

1. **Encoding layers** take radically different surface forms — different scripts, different word orders, different morphological strategies — and map them onto a shared internal representation.
2. **Reasoning layers** operate in that shared space, indifferent to which surface form or syntactic structure produced it.
3. **Decoding layers** map back out to a specific surface form.

The encoding and decoding phases are doing something *analogous* to what Chomsky's framework describes: translating between diverse surface structures and a universal deep structure. But the deep structure the model discovered isn't a tree of syntactic rules — it's a continuous geometric manifold of meaning. Every language gets its own encoder and decoder, but the middle is shared, and what's shared is semantics, not syntax.

Chomsky famously demonstrated that syntax and semantics are independent systems — "Colorless green ideas sleep furiously" is grammatically impeccable and semantically absurd. His argument was that syntax must therefore be the foundational, primitive system: an innate rulebook that operates prior to and independently of meaning. What the transformers show is the opposite priority. You can build universal linguistic structure *entirely* out of semantics, with no foundational syntactic rulebook at all. Syntax, in this picture, is downstream: a surface regularisation that emerges from the need to serialise meaning into a linear token stream, not the bedrock on which meaning rests.

Chomsky was right about the *what*: there is a universal structure underlying all languages. But he was wrong about the *where* (it's semantics, not syntax) and the *how* (it's learned geometry, not innate grammar). The universal structure isn't a set of rules, parameters, or syntactic primitives. It's a high-dimensional space where semantic relationships are encoded as distances and directions. And it's not innate. It *emerges* from exposure to enough linguistic diversity through gradient descent. No one designed it. No one specified its structure. The optimisation pressure of next-token prediction on multilingual data was sufficient. Whether this geometry emerges purely from the unsupervised crucible of next-token prediction, or whether it gets crystallised later by RLHF alignment, the result is the same: the model learns that the most efficient way to be smart in 100 languages is to strip language away entirely in the middle.

So we end up with a three-way scorecard:

**Chomsky:** "There's a universal deep structure underlying all languages."
→ *Right intuition, wrong floor. He looked for it in syntax. It lives in semantics. And it's not innate — it's emergent.*

**Sapir-Whorf:** "Language shapes (or determines) thought."
→ *The strong form doesn't survive. These models structurally separate language from reasoning — an anti-Whorfian bottleneck baked into the architecture by gradient descent. Language is the I/O layer, not the reasoning layer.*

**The transformers:** "We'll just learn whatever works."
→ *Converge on a universal semantic space that vindicates Chomsky's intuition about universality while contradicting his mechanism entirely.*

Chomsky looked for universal grammar. Transformers found universal geometry. The structure exists (Chomsky's core claim survives). But it's not grammar — it's a geometric manifold of meaning that emerges from data, not from biology. And language doesn't shape the structure — the structure shapes language.

---

## The Anatomy Predicts the Function

This result connects directly to the [RYS work](https://dnhkng.github.io/posts/rys-ii/). The layers that can be profitably duplicated — the layers where running the computation twice makes the model measurably smarter — are *exactly* the layers where the language-agnostic reasoning space exists.

This isn't a coincidence. It's a mechanistic explanation:

- If a layer operates in format-agnostic space, its input and output distributions are similar enough that you can loop back without catastrophic distribution mismatch. The model can "think again" through the same circuit.
- If a layer is doing format-specific work (encoding or decoding), looping back means feeding decoded representations into a layer that expects abstract ones, or vice versa. The distributions don't match. The model breaks.

The brain scan predicts the surgery map. The three-phase anatomy isn't just a nice observation — it's *functional*. It tells you where you can intervene and where you can't.

---

## Caveats and What This Isn't

**LLMs aren't human brains.** Sapir-Whorf is a hypothesis about human cognition. I'm not claiming that because GPT-scale transformers have language-independent reasoning, therefore human cognition is language-independent. The architectures are different. The training is different. The substrates are different.

But LLMs are an unprecedented empirical tool for this question. They are the first systems we can build that process many natural languages at high competence, develop internal representations we can measure at every layer, and let us directly test whether thought is language-shaped or language-independent. Before LLMs, you could only study Sapir-Whorf by comparing human behaviour across language groups — messy, confounded, hard to control. Now we can read out the internal state and ask: is it organised by language or by meaning?

**To the cognitive scientists currently screaming at their screens:** yes, I know LLMs are disembodied text-engines with no sensorimotor grounding. Yes, I know "photosynthesis" is an easy 1:1 translation compared to testing culturally entangled concepts like *Schadenfreude* or Quechua evidentiality. Yes, I know modern linguists favour the weak Whorfian view anyway. And yes, 64 sentences is a proof of concept, not a definitive corpus study. But the architectural observation remains: we have a computational substrate that processes 100+ languages, and it *structurally refuses* to let surface grammar dictate deep reasoning. It builds an anti-Whorfian bottleneck. That matters.

**On parallel corpora and the translation-artifact objection.** A careful reader will note that training data contains parallel corpora — human-translated sentence pairs — and argue that gradient descent simply *had* to learn a shared latent space because that is the mathematically optimal way to predict translations. This is a legitimate mechanistic objection, not just a data-contamination concern. But it doesn't fully dissolve the result. First, the question of *why* the model learns a shared space doesn't negate the fact that it does — the question "is this universal meaning, or just a reverse-engineering of the human semantic map?" may not have a clean answer, because human language and human meaning are co-constituted. Second, and more concretely: the code and math results in the next section provide a harder test. Python functions with single-letter variables and LaTeX equations were almost certainly not aligned by explicit translation training — yet they converge in the mid-stack in exactly the same pattern. That's a natural experiment the translation-artifact story struggles to explain.

**Is the "universal" space just latent English?** Legitimate concern. But the strongest counter is architectural: Qwen and GLM are both Chinese-dominant models, trained by Chinese organisations on Chinese-heavy data. If the universal space were latent English, you'd expect Chinese-dominant models to produce a *different* organising structure — one centred on Chinese rather than English. They don't. All four models, including the Chinese-heavy ones, converge on the same three-phase anatomy with the same topic-dominant reasoning layers. A shared structure that is independent of each model's dominant training language is hard to explain as "latent English." A rigorous distance-from-centroid analysis is still on the list to confirm this quantitatively.

---

## Beyond Language: Code and Math as a Test Case

The natural language results are striking, but they invite an obvious question: is the universal space specific to *human languages*, or does it extend to formal systems too?

Natural languages, for all their diversity, share a common evolutionary purpose: humans communicating with other humans about a shared physical world. You could argue that convergence across Chinese and French is unsurprising — they're all trying to do the same thing. Code and mathematical notation are a different beast entirely. They weren't shaped by evolution or culture. They express computation and formal relationships using systems that share essentially zero surface structure with any natural language.

If the model processes Python code, LaTeX equations, and English descriptions of the same concept, do they converge in the mid-stack the way Chinese and French do?

This is a harder test. Natural languages all describe the world using nouns, verbs, and compositional semantics. Python expresses computation using operators and control flow. LaTeX expresses mathematical relationships using a completely different notation system — $\frac{1}{2} m v^2$ shares essentially zero surface tokens with either $0.5 * m * v ** 2$ or "half the mass times velocity squared." Three fundamentally different modalities, zero syntactic overlap.

To make it honest, the code uses only single-letter variables. No `velocity`, no `principal`, no `kinetic_energy`. Just `m`, `v`, `p`, `r`, `t` — standard math convention, not English words. The model has to understand the *computation*, not read the *labels*.

I tested 12 topics spanning physics, mathematics, and economics — from kinetic energy and gravitational force to the quadratic formula and price elasticity of demand. Each topic expressed in all three systems gives 36 samples, 630 pairwise comparisons. A few representative triplets:

**Kinetic energy:**
- EN: *"The kinetic energy of a moving object equals one half of its mass multiplied by the square of its velocity."*
- Python: 
 ```
 def f(m, v):
  return 0.5 * m * v ** 2`
```
- LaTeX: $\ E_k = \frac{1}{2} m v^2$

**Quadratic formula:**
- EN: *"The solutions of a quadratic equation are found by taking the negative of the second coefficient, plus or minus the square root of that coefficient squared minus four times the first and third coefficients, all divided by twice the first coefficient."*
- Python:
```
def f(a, b, c):
  d = (b**2 - 4*a*c)**0.5
  return (-b + d)/(2*a), (-b - d)/(2*a)
```
- LaTeX: $\ x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

**Present value:**
- EN: *"The present value of a future cash flow is that amount divided by one plus the discount rate raised to the number of periods."*
- Python:
```
def f(fv, r, t):
  return fv / (1 + r) ** t
```
- LaTeX: $\ PV = \frac{FV}{(1 + r)^t}$


<details>
<summary><strong>Full Dataset: Code and Math (Click to expand)</strong></summary>
<div style="padding-left: 20px; margin-top: 10px;">
<ul>
<li><em>"EN_KINETIC_ENERGY": "The kinetic energy of a moving object equals one half of its mass multiplied by the square of its velocity."</em></li>
<li><em>"PY_KINETIC_ENERGY": "def f(m, v):\n    return 0.5 * m * v ** 2"</em></li>
<li><em>"LATEX_KINETIC_ENERGY": "E_k = \frac{1}{2} m v^2"</em></li>
<br>
<li><em>"EN_GRAVITATIONAL_FORCE": "The gravitational force between two objects is proportional to the product of their masses and inversely proportional to the square of the distance between them."</em></li>
<li><em>"PY_GRAVITATIONAL_FORCE": "def f(m1, m2, r, G=6.674e-11):\n    return G * m1 * m2 / r ** 2"</em></li>
<li><em>"LATEX_GRAVITATIONAL_FORCE": "F = G \frac{m_1 m_2}{r^2}"</em></li>
<br>
<li><em>"EN_OHMS_LAW": "The electric current through a conductor is equal to the voltage across it divided by its resistance."</em></li>
<li><em>"PY_OHMS_LAW": "def f(V, R):\n    return V / R"</em></li>
<li><em>"LATEX_OHMS_LAW": "I = \frac{V}{R}"</em></li>
<br>
<li><em>"EN_PERIOD_OF_A_PENDULUM": "The period of a simple pendulum is two pi times the square root of its length divided by gravitational acceleration."</em></li>
<li><em>"PY_PERIOD_OF_A_PENDULUM": "def f(L, g=9.81):\n    return 2 * 3.14159 * (L / g) ** 0.5"</em></li>
<li><em>"LATEX_PERIOD_OF_A_PENDULUM": "T = 2\pi \sqrt{\frac{L}{g}}"</em></li>
<br>
<li><em>"EN_FACTORIAL": "The factorial of a positive integer is the product of all positive integers less than or equal to that number."</em></li>
<li><em>"PY_FACTORIAL": "def f(n):\n    r = 1\n    for i in range(1, n + 1):\n        r *= i\n    return r"</em></li>
<li><em>"LATEX_FACTORIAL": "n! = \prod_{i=1}^{n} i"</em></li>
<br>
<li><em>"EN_QUADRATIC_FORMULA": "The solutions of a quadratic equation are found by taking the negative of the second coefficient, plus or minus the square root of that coefficient squared minus four times the first and third coefficients, all divided by twice the first coefficient."</em></li>
<li><em>"PY_QUADRATIC_FORMULA": "def f(a, b, c):\n    d = (b**2 - 4*a*c)**0.5\n    return (-b + d) / (2*a), (-b - d) / (2*a)"</em></li>
<li><em>"LATEX_QUADRATIC_FORMULA": "x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"</em></li>
<br>
<li><em>"EN_EULERS_IDENTITY": "Euler's identity states that the exponential of the imaginary unit times pi, plus one, equals zero."</em></li>
<li><em>"PY_EULERS_IDENTITY": "import cmath\nassert abs(cmath.exp(1j * cmath.pi) + 1) < 1e-10"</em></li>
<li><em>"LATEX_EULERS_IDENTITY": "e^{i\pi} + 1 = 0"</em></li>
<br>
<li><em>"EN_AREA_OF_A_CIRCLE": "The area enclosed by a circle is equal to pi multiplied by the square of its radius."</em></li>
<li><em>"PY_AREA_OF_A_CIRCLE": "def f(r):\n    return 3.14159 * r ** 2"</em></li>
<li><em>"LATEX_AREA_OF_A_CIRCLE": "A = \pi r^2"</em></li>
<br>
<li><em>"EN_COMPOUND_INTEREST": "Compound interest grows an initial principal by applying a fixed annual rate repeatedly over a number of years, so that each year's interest earns interest in subsequent years."</em></li>
<li><em>"PY_COMPOUND_INTEREST": "def f(p, r, t):\n    return p * (1 + r) ** t"</em></li>
<li><em>"LATEX_COMPOUND_INTEREST": "A = P(1 + r)^t"</em></li>
<br>
<li><em>"EN_PRICE_ELASTICITY_OF_DEMAND": "Price elasticity of demand is the ratio of the percentage change in quantity demanded to the percentage change in price."</em></li>
<li><em>"PY_PRICE_ELASTICITY_OF_DEMAND": "def f(dq, q, dp, p):\n    return (dq / q) / (dp / p)"</em></li>
<li><em>"LATEX_PRICE_ELASTICITY_OF_DEMAND": "E_d = \frac{\Delta Q / Q}{\Delta P / P}"</em></li>
<br>
<li><em>"EN_GDP_DEFLATOR": "The GDP deflator is nominal gross domestic product divided by real gross domestic product, multiplied by one hundred."</em></li>
<li><em>"PY_GDP_DEFLATOR": "def f(n, r):\n    return (n / r) * 100"</em></li>
<li><em>"LATEX_GDP_DEFLATOR": "D = \frac{GDP_{nominal}}{GDP_{real}} \times 100"</em></li>
<br>
<li><em>"EN_PRESENT_VALUE": "The present value of a future cash flow is that amount divided by one plus the discount rate raised to the number of periods."</em></li>
<li><em>"PY_PRESENT_VALUE": "def f(fv, r, t):\n    return fv / (1 + r) ** t"</em></li>
<li><em>"LATEX_PRESENT_VALUE": "PV = \frac{FV}{(1 + r)^t}"</em></li>
</ul>
</div>
</details>

**Centered cosine similarity for MiniMax M2.5**
![Cross-modal cosine similarity](/assets/img/universal/m25_peer_system_category_curves_centered_rgb.png)
*Centered cosine similarity across English, Python, and LaTeX. Red = cross-system same-topic. Green = within-system different-topic. Blue = cross-system different-topic.*

**Centered cosine similarity for MiniMax M2.5**
![Cross-modal cosine similarity](/assets/img/universal/m25_peer_system_category_bands_centered_mean_std_rgb.png)
*Same data with ±1 standard deviation bands. The separation between same-topic and different-topic pairs is clean even at the individual-pair level.*


The result is unambiguous. Three phases, same as the natural language case, but now across *modalities*:

**Layers 0–10: System identity dominates.** The green line (within-system, different topic) peaks above 0.6. The red line (cross-system, same topic) sits below -0.2. The model overwhelmingly sees "this is Python" versus "this is LaTeX" versus "this is English." The distinction between executable code, mathematical notation, and natural language prose swamps everything else. This is more extreme than the natural language case — the gap between English and Chinese is much smaller than the gap between English and $\ \frac{1}{2} m v^2$.

**Layers 10–25: The crossover.** Green drops steadily. Red rises. Around layer 25, they cross. The model is dissolving the distinction between code, equations, and text. It's finding the meaning underneath.

**Layers 25–52: Topic catches up.** Red even sits above green between layers ~27-33, so $\ \frac{1}{2} m v^2$ is now closer to "kinetic energy equals half mass times velocity squared" than it is to $\ A = \pi r^2$! A Python function computing compound interest clusters with the English description of compound interest and the LaTeX formula for compound interest — not with a Python function computing something else. And blue (cross-system, different topic) stays firmly negative throughout, confirming that the model isn't just blurring everything together. It's maintaining semantic discrimination while erasing format discrimination.

**Layers 52+: System identity returns.** Green spikes back up. The model is preparing to emit tokens and needs to commit: Python syntax, LaTeX markup, or English words.

This is the result that upgrades the thesis. The universal space in the mid-stack isn't just language-agnostic — it's *modality*-agnostic. It encodes meaning whether that meaning arrives as French prose, Arabic script, Python functions with single-letter variables, or LaTeX notation. $\ \frac{1}{2} m v^2$ and "half the mass times velocity squared" and $\ 0.5 * m * v ** 2$ all converge to the same region of a high-dimensional geometric space, despite sharing essentially zero surface-level features.

The interlingua isn't just for human languages. It's for anything that expresses structured meaning.

---

## The Uncomfortable Implication

If you take this result at face value — four models, two experiments, the same convergent structure every time — then the most conservative reading is: transformer-based language models discover that the most efficient internal organisation separates meaning from format. Content goes to one space, language/syntax/notation goes to the I/O layers. This is an engineering observation about how these models solve their training objective.

The more aggressive reading is that this separation reflects something about the structure of meaning itself. That there exists a space of semantic relationships — photosynthesis is closer to respiration than to contract law, regardless of whether you express it in Mandarin or in LaTeX — and that gradient descent on enough data will reliably find it.

I don't know which reading is correct, and I'm not sure the distinction is as clean as it sounds. The "engineering" explanation (it's just efficient compression) and the "philosophical" explanation (meaning has structure independent of language) might not be separable. If every sufficiently capable system that processes multilingual data converges on the same semantic geometry, then asking whether that geometry is "real" or "just compression" starts to look like asking whether mathematics is discovered or invented. You can have the argument. It may not have a resolution.

What the data *does* clearly show: these models don't just tolerate the separation of language and meaning — they *demand* it. The three-phase structure isn't a quirk of one architecture or one training run. Four different models, built by different organisations, on different data, with different architectures, all converge on the same solution. And that solution extends beyond human languages to formal systems that share no surface features with natural language at all.

Sapir and Whorf had it backwards. Language doesn't shape thought — at least not in these systems. The model strips language away to think, then puts it back on to speak. And Chomsky was half right: there is a universal structure underneath. But it's not grammar. It's geometry.

---

## What's Next

Several experiments would strengthen or complicate this picture:

- **Adversarial pairs.** "The bank of the river" vs "the bank raised rates" — testing whether the semantic space resolves polysemy correctly.
- **Cross-lingual steering.** Taking a direction vector between topics in one language and applying it to another language's representations. If the space is truly shared, cross-lingual vector arithmetic should work.
- **Scaling laws.** Does the universal space emerge more cleanly in larger models? Do smaller models show a noisier or more entangled version of the same structure?
- **Scaling the evaluation.** 64 natural-language sentences and 36 code/math samples are proofs of concept. Running this on established multilingual benchmarks like FLORES-200 or XNLI — with hundreds of languages and thousands of sentence pairs — would map the exact topology of the space. Adding more formal languages (Rust, Haskell, maybe assembly) would test where cross-modal convergence breaks down.
- **Culturally entangled concepts.** Testing with concepts that resist clean translation — *Schadenfreude*, Japanese *wabi-sabi*, Quechua evidentiality markers — to probe the limits of universality.

The data is clear. The interpretation is provocative. The experiments continue.

Code and datasets: [github.com/dnhkng/RYS](https://github.com/dnhkng/RYS)

---

## Citing this work

```bibtex
@article{ng2026sapirwhorf,
  title   = {Do LLMs Break the Sapir-Whorf Hypothesis?},
  author  = {Ng, David Noel},
  year    = {2026},
  month   = {March},
  url     = {https://dnhkng.github.io/posts/sapir-whorf/}
}
```