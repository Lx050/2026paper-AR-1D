# PCA-B0 组会逐字稿

生成日期：2026-05-27

汇报主题：从保主体到打动人：主体一致性门槛下的感知激活生成

主论文押注：DreamBench++: A Human-Aligned Benchmark for Personalized Image Generation

建议时长：6 到 8 分钟

---

## 第 1 页：开场

各位老师、同学好，我今天想汇报的不是一个已经完全收束的实验结果，而是我这个课题现在最核心的研究方向。

我的题目可以暂时叫做：从保主体到打动人。更完整一点说，是在主体一致性已经被满足的前提下，研究图像生成怎样进一步获得美感、情绪感染力，以及记忆唤起能力。

这里我想先把我的立场说清楚。我现在想做的不是证明某一个指标永远正确，也不是简单地追求生成图像更像参考图。我的问题是：如果参考图里的主体已经被保住了，我们还能不能进一步控制生成过程，让结果不只是“像”，而是更美、更动人、更容易激活人的内心记忆。

所以我把任务拆成两层。第一层是主体一致性，它是门槛。第二层是在通过这个门槛之后，去优化审美、情绪、记忆和意义联想。

一句话概括就是：Reference image 不只是复制模板，它是用户价值和记忆的锚点。

---

## 第 2 页：我的核心思想

我现在的理论押注叫 CTAS，Causal-Temporal Activation Space，中文可以叫“因果-时间激活空间”。

这个名字背后的想法是：主体、美感、情绪、记忆不是几个互相独立的分数。它们更像是一组互相影响的潜变量。

比如，审美增强可能会伤害主体一致性。构图变化可能会改变情绪。记忆激活可能依赖某些特定的审美风格或者文化符号。反过来，如果主体一旦失效，后面的情绪和记忆基本也会失去锚点。

所以我不想把它做成一个简单的综合评分，而是想研究这些变量之间的关系。

我暂时把变量拆成四类。第一类是 S_id，也就是主体、身份、对象的不变量空间。第二类是 S_aes，也就是审美、风格、光影、材质和构图。第三类是 S_affect，也就是情绪唤起，比如温暖、孤独、怀旧、庄严、震撼。第四类是 S_mem，也就是记忆空间，包括个人经历、物件线索、时代感和文化符号。

同时，我认为扩散生成里的时间阶段也很重要。早期可能更适合锁结构和主体，中期可能更适合调语义、构图和情绪，后期可能更适合调光影、颜色、材质和审美细节。

这就是我目前的核心想法：理论上押注因果潜空间，工程上拆成时间调制，评估上最终要落到人的感受。

---

## 第 3 页：为什么先讲主体一致性 baseline

接下来我先选几篇主体一致性的 paper 作为 baseline。这里我不是想说这些 paper 都要完整复现，也不是要找一篇万能文章。

更合理的方式是把主体一致性这个领域拆成几条强路线。

第一条是 fine-tuning 路线，比如 DreamBooth。它用少量主体图去微调扩散模型，是 subject-driven generation 的经典起点。

第二条是 token 路线，比如 Textual Inversion。它用一个 learned token 去表示新概念，说明个性化生成可以不一定完全依赖大规模微调。

第三条是多概念定制路线，比如 Custom Diffusion。它适合用来暴露多主体、多概念之间的互扰问题。

第四条是 adapter 或 image prompt 路线，比如 IP-Adapter。这个路线对我的课题很关键，因为它更符合 reference-guided workflow，也就是拿参考图作为输入锚点。

第五条是人像身份路线，比如 PhotoMaker 和 InstantID。它们在人脸身份保持上很强，但我会把它们看成 identity 子域，而不是全部主体一致性的代表。

最后一条是评估路线，也就是我这次主押的 DreamBench++。

所以我的 baseline 不是平铺一堆论文，而是为了说明：主体一致性已经有成熟路线，我的创新不应该停留在“更像”这件事上，而应该把它作为前置 gate。

---

## 第 4 页：主论文 DreamBench++ 为什么适合押注

我这次建议把 DreamBench++ 作为组会汇报的主论文。

它的全名是 DreamBench++: A Human-Aligned Benchmark for Personalized Image Generation，是 ICLR 2025 的 conference paper。

它最适合我现在的原因有三个。

第一，它直接面对 personalized image generation 的评估问题。也就是说，它不是只问“模型能不能生成好看的图”，而是问“给定参考主体之后，生成结果有没有保住这个主体，同时有没有遵循新的 prompt”。

第二，它把评估拆成两个关键维度：Concept Preservation 和 Prompt Following。Concept Preservation 对应主体是否保住，Prompt Following 对应新场景、新动作、新风格是否被执行。这个拆法比单纯说“像不像参考图”更合理。

第三，它强调 human-aligned evaluation。传统 CLIP 或 DINO 这类指标有时候会和人的判断不一致，DreamBench++ 用 GPT-4o 设计评估流程，并和人工评价对齐。这一点很适合我后续做“美感、情绪、记忆”评估，因为我的方向最终也必须回到人的感受。

这篇文章里有几个数字可以在组会上讲。它构建了 150 张高质量 reference images 和 1,350 个 prompts，并评测了 7 个现代 personalized generation 模型。它还要求人工评分和 GPT 评分隔离，并且每个实例至少由两个人评分来降低噪声。

我对它的定位是：DreamBench++ 不直接解决“怎么更动人”，但它可以成为我的第一层门槛。它回答的是：主体有没有保住，新 prompt 有没有跟上。

---

## 第 5 页：DreamBench++ 和我的差异

这里我要强调一点：我不是要替代 DreamBench++，而是把它前置化。

DreamBench++ 解决的是 subject gate，也就是：这张图还算不算同一个主体，以及它有没有听新 prompt。

我的 PCA-B0 或 CTAS 想继续往后问三个问题。

第一，通过主体 gate 的候选图里，哪一张更美？

第二，哪一张更动人？它是温暖、怀旧、孤独、庄严，还是震撼？

第三，哪一张更容易激活人的记忆？它是靠主体本身，还是靠场景、物件、时代感、文化符号，或者某种熟悉但不完全重复的感觉？

所以我和 DreamBench++ 的关系可以这样讲：DreamBench++ 是地基，PCA-B0 是在地基之后继续建楼。

如果用公式表达，就是：

Good Output = Subject Consistency Gate + Perceptual Activation + Human Memory Calibration。

这也是为什么我不应该把创新点放在“我也做一个主体一致性 benchmark”。主体一致性是底线，不是终点。

---

## 第 6 页：2026 补充，说明我看过最新趋势

因为老师可能会问有没有更新的工作，所以我建议补充两条 2026 资料，但它们不替代主论文。

第一条是 DSH-Bench。它是 2026 的 subject-driven text-to-image benchmark，可以作为最新评估补充。我的讲法是：DreamBench++ 是稳定的主体 gate 锚点，DSH-Bench 说明 2026 年这个方向还在继续细化，尤其是在更困难的 subject 场景和 failure 类型上。

第二条是 Personalize Anything。它是 AAAI 2026 的开源 personalized generation 方法，可以作为新方法补充。它的价值在于说明 personalized generation 正在从传统 U-Net diffusion 路线继续扩展到更新的架构和 training-free personalization 思路。

这里我会避免把 2026 工作讲成主线，因为组会的主线需要稳定和清晰。DreamBench++ 负责定义 subject gate，2026 工作负责说明我没有忽略最新发展。

---

## 第 7 页：我的第一批实验怎么做

接下来，如果要从调研进入实验，我建议先做最小可复现版本。

第一步，选择一组 reference images。可以先从 DreamBench++ 或类似 subject benchmark 中选，也可以用自己补充的小样本。

第二步，用几类 baseline 方法生成候选图，比如 DreamBooth LoRA、IP-Adapter、PhotoMaker 或 InstantID。先不追求大规模训练，先保证能生成可比较的候选。

第三步，做 subject gate。这里可以参考 DreamBench++ 的思想，先用 concept preservation 和 prompt following 两个维度过滤。轻量版本可以用 CLIP、DINO、VLM judge，加上人工抽查。

第四步，对通过 gate 的候选图做 activation ranking。也就是再用审美 reward、情绪识别、memorability proxy 和人工小样本，去判断哪张更美、更动人、更能唤起记忆。

第五步，做时间调制实验。比如固定主体输入，只改变不同扩散阶段的 adapter scale、attention 强度、风格注入强度，观察什么时候增强美感最安全，什么时候最容易破坏主体。

第一批实验的目标不是证明一个宏大理论，而是拿到一个可观察现象：主体一致性和感知激活之间是否存在可控 trade-off。

---

## 第 8 页：结尾

最后总结一下。

我的课题不是单纯做“更像参考图”的 personalized generation，而是把主体一致性作为门槛，在门槛之后研究审美、情绪和记忆激活。

我目前的理论押注是 CTAS，也就是因果-时间激活空间。它假设主体、美感、情绪和记忆之间不是独立变量，而是存在相互影响；同时，扩散过程的不同时间阶段也承担不同控制功能。

组会里 baseline 可以选 DreamBooth、Textual Inversion、Custom Diffusion、IP-Adapter、PhotoMaker、InstantID 和 DreamBench++。其中我建议主押 DreamBench++，因为它最适合定义主体一致性 gate，而且有项目页、代码和本地 PDF，可以支撑组会展示。

下一步我会做一个最小实验：先让模型生成一批主体一致的候选，再在通过 gate 的候选里比较美感、情绪和记忆激活。这样我的创新点就不会和已有主体一致性工作正面重复，而是从“保主体”推进到“打动人”。

我的汇报到这里，谢谢大家。

---

## 可能被问到的问题和回答

### 问题 1：你是不是只是把多个指标加权？

不是。我不是想做一个简单总分，而是想研究变量关系。比如审美增强什么时候会伤害主体一致性，情绪增强什么时候依赖构图或风格，记忆激活是否需要熟悉性和新颖性的平衡。这些关系比一个加权分数更重要。

### 问题 2：为什么不直接做美学模型？

因为我的任务不是开放域美学评分，而是 reference-guided personalized generation。主体是锚点，美学是在主体一致性门槛之后才有意义。如果主体丢了，再美也不是用户想要的那张图。

### 问题 3：为什么选 DreamBench++，而不是 2026 最新 benchmark？

DreamBench++ 更适合作为稳定主线：它是 ICLR 2025，问题定义清楚，项目页和代码完整，并且直接把评估拆成 Concept Preservation 和 Prompt Following。2026 的 DSH-Bench 可以作为最新补充，但我不建议用它替代主线。

### 问题 4：记忆激活怎么评估？

公开 memorability 数据只能做 proxy，不能等同于个人记忆。所以第一阶段可以用 LaMem、THINGS、memorability predictor 做辅助指标，最终一定要加一个小规模人类实验，直接问哪张图更像记忆、更能唤起某种经历或联想。

### 问题 5：你的创新点在哪里？

创新点不在“我也保主体”，而在主体一致性之后的感知激活控制。具体说，是因果潜空间假设、扩散时间调制，以及审美-情绪-记忆的人类校准闭环。

---

## 资料入口

- 本地 DreamBench++ PDF：`papers/DreamBenchPlus_2406.16855_full.pdf`
- DreamBench++ arXiv：https://arxiv.org/abs/2406.16855
- DreamBench++ project：https://dreambenchplus.github.io/
- DreamBench++ GitHub：https://github.com/yuangpeng/dreambench_plus
- DSH-Bench：https://arxiv.org/abs/2603.08090
- Personalize Anything：https://github.com/fenghora/personalize-anything
