# PCA-B0 Theory-First SOTA Map

生成日期：2026-05-26  
工作目录：`G:\Lbx\paper\2026_5_25`

## 0. 核心修正

上一版“全局综合打分”会诱导一个错误目标：寻找一篇同时满足主体一致性、时间调制、因果潜空间、美感、情绪、记忆和人类验证的万能论文。这个目标本身是悖论。

PCA-B0/CTAS 应该采用新的收缩逻辑：

```text
先理论分解，
再建立正交能力轴，
每个能力轴找 SOTA，
去重但保留差异，
最后统筹所有 SOTA。
```

这份地图的目标不是减少文献数量，而是把资料从“宽池”变成“顶级积木池”。每篇文章只要在一个能力轴上足够尖锐，就可以保留；平庸但全面的文章不进入核心。

## 1. 理论分解

PCA-B0 不是一个证明系统，也不是通用审美打分器。它研究的是：

> 在主体一致性不被破坏的前提下，如何通过因果潜变量和扩散时间阶段的干预，让生成结果更有美感、更有情绪感染力、更能唤起记忆。

因此 CTAS 的理论结构应拆成 8 个能力轴。

| 能力轴 | 研究对象 | 在 CTAS 中的角色 |
|---|---|---|
| 主体一致性 | subject-driven / personalized generation | 守住 `S_id`，只做 gate，不做最终审美目标 |
| 时间调制 | timestep / attention / layer / adapter schedule | 研究“何时注入”比“注入什么”更安全 |
| 因果潜空间 | causal representation / disentanglement | 支撑多空间非独立、可干预、可解释 |
| 审美偏好 | preference / reward / aesthetic scorer | 给美感排序提供强代理，但不能覆盖 gate |
| 情绪激活 | emotion recognition / affective language | 解释“动人”的情绪结构，而不是只贴情绪标签 |
| 记忆激活 | memorability / personal memory proxy | 连接“可被记住”和“唤起个人记忆” |
| 组合结构 | compositional / reasoning benchmark | 防止漂亮但对象、关系、数量、逻辑错误 |
| 人类验证 | human-aligned evaluation / pairwise study | 校准自动指标和真实人类感受 |

## 2. 正交性定义

这里的正交性不是指方法之间毫无关系，而是指贡献向量不重复。

一个资料的贡献向量由以下问题定义：

```text
它保护什么变量？
它干预哪个位置？
它优化什么目标？
它提供什么数据或评估？
它的不可替代差异是什么？
```

如果两篇文章都做主体一致性，但一篇是 fine-tuning，一篇是 image prompt adapter，一篇是 localized attention，它们不重复。因为它们的干预位置不同。

如果两篇文章都只是用类似偏好数据训练类似 reward model，且没有新的评估维度或可解释性，那么保留更强、更可复现、更被 benchmark 接受的一篇。

## 3. SOTA 证据等级

PCA-B0 的短名单不按“看起来相关”排序，而按证据强度组织。

| 证据等级 | 含义 | 例子 |
|---|---|---|
| E1 | 官方 benchmark / leaderboard / benchmark 论文系统结果 | DreamBench++、DSH-Bench、T2I-CompBench++、R2I-Bench |
| E2 | 顶会/期刊系统对比 | ICLR、NeurIPS、ICCV、SIGGRAPH、TPAMI、Science Advances |
| E3 | 官方代码 + 可复现实验入口 | IP-Adapter、ImageReward、T2I-CompBench++、GenEval |
| E4 | 被后续 SOTA 反复采用的基础方法 | Prompt-to-Prompt、ControlNet、CausalVAE、CLIP |
| E5 | 概念启发强但不适合第一批实验 | 早期潜空间编辑、部分心理学数据、不可公开数据 |

### 3.1 厚书层原则

SOTA 层解决“当前哪些方法强”，但不解决“为什么美、为什么动人、为什么唤起记忆”。PCA-B0/CTAS 需要额外维护一层 Thick Reading Layer：

```text
SOTA Layer = 方法、数据、benchmark 的当前强者
Thick Reading Layer = 能提供底层变量、解释框架、实验问题的经典理论
```

厚书层不按 leaderboard 排名，也不要求必须有代码。它的入选条件是：

| 条件 | 含义 |
|---|---|
| 提供变量 | 能转化为 `complexity`、`novelty`、`fluency`、`arousal`、`nostalgia`、`prediction_error` 等 CTAS 变量 |
| 提供解释 | 能解释为什么“漂亮”不等于“动人”，为什么“可记住”不等于“个人记忆” |
| 提供差异 | 来自心理美学、认知科学、艺术史、情感计算、记忆心理学、符号学、设计理论等不同思想传统 |
| 不追求显眼 | 允许经典书、老论文、非 AI 文献进入核心背景，只要它能让问题更深 |

这一层已单独整理在 `pca_b0_foundational_idea_map.csv`。经典思想不和 SOTA 混排，避免把“旧但根本”的理论误判为“过时”。

## 4. 轴向 SOTA 统筹

### 4.1 主体一致性轴

主体一致性轴负责回答：

```text
什么方法能最大程度守住主体？
什么 benchmark 能诊断主体丢失？
```

当前应保留三类顶级积木：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 评估 SOTA | DreamBench++ | ICLR 2025，人类对齐 personalized generation benchmark，含 leaderboard |
| 诊断 SOTA | DSH-Bench | 2026 benchmark，58 个细粒度主体类别，提出 SICS，面向难度和场景诊断 |
| 方法 SOTA | IP-Adapter / IP-Adapter-Plus | image prompt adapter 路线，适合 PCA-B0 reference-guided 入口 |
| 方法 SOTA | DreamBooth LoRA SDXL | DreamBench++ 上 CP/PF 综合表现强，适合作为 fine-tuning 强基线 |
| 方法 SOTA | InstantID / PhotoMaker | 人像身份保持强，但只限 identity/photo-human 子域 |

主体一致性轴的原则：它只决定能不能过 gate，不能决定哪张图最动人。

### 4.2 时间调制轴

时间调制轴负责回答：

```text
在扩散生成的哪个阶段注入风格、情绪或记忆线索，最不容易破坏主体？
```

保留的不是“最新最炫”，而是能提供可控干预位置的 SOTA/源头：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 源头方法 | Prompt-to-Prompt | 证明 cross-attention 控制 prompt-word 与空间布局关系 |
| 推理干预 | Attend-and-Excite | 推理时强化 token attention，修复主体/属性缺失 |
| 真实图编辑 | Null-text Inversion | 用 timestep anchor 和 null-text 优化保持真实图结构 |
| 条件控制 | ControlNet | 提供结构条件控制骨架，可用于 early structure lock |
| 适配器控制 | IP-Adapter / T2I-Adapter | 可设计 adapter scale schedule，做 early/mid/late 对照 |

时间调制不是单独创新，而是 CTAS 的实验手柄。

### 4.3 因果潜空间轴

因果潜空间轴负责回答：

```text
主体、美感、情绪、记忆是不是独立变量？
如果不独立，如何描述它们的因果影响？
```

保留三类理论：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 理论根源 | Causal Representation Learning | 明确高层因果变量需要从低层观测中发现 |
| 方法根源 | CausalVAE | 直接指出语义因素不一定独立，而可能有因果结构 |
| 表征根源 | beta-VAE / InfoGAN / FactorVAE | 提供可解释潜变量和解耦的基础参照 |

这一轴不负责直接跑图，而负责定义 CTAS 的理论语言：

```text
S_id -> S_mem
S_aes -> S_id
S_layout -> S_affect
S_mem -> S_aes
```

### 4.4 审美偏好轴

审美偏好轴负责回答：

```text
在通过主体 gate 后，哪些图更符合人类审美或偏好？
```

保留：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 偏好数据/模型 | Pick-a-Pic / PickScore | 成对人类偏好数据，适合 preference-only baseline |
| Reward SOTA | ImageReward | NeurIPS 2023，通用 T2I human preference reward，代码和数据可用 |
| 多维偏好 | VisionReward / MPS | 多维偏好比单一分数更符合 PCA-B0，不应只看总分 |
| 基础审美 | LAION-Aesthetics / AVA / AADB | 可做审美先验，但不能代表“打动人” |

本轴注意：偏好分是 evidence，不是裁判。

### 4.5 情绪激活轴

情绪激活轴负责回答：

```text
图像为什么让人觉得温暖、孤独、庄严、怀旧或震撼？
```

保留：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 情绪语言数据 | ArtEmis | 80K artworks、455K 情绪归因和解释，能把情绪和语言解释连接 |
| 大规模情绪数据 | EmoSet | 3.3M 图像，118K 人工标注，含情绪属性，适合解释性 emotion proxy |
| 零样本工具 | EmotionCLIP / CLIP emotion prompts | 第一阶段可低成本跑情绪词代理 |

本轴不把情绪标签当作终点，而是把情绪解释作为“动人”的可观察证据。

### 4.6 记忆激活轴

记忆激活轴负责回答：

```text
什么图像更容易被记住？
什么线索更可能触发个人或文化记忆？
```

保留：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 经典记忆数据 | LaMem / MemNet | 大规模 memorability 数据和模型源头 |
| 对象认知数据 | THINGS / THINGS memorability | 26,107 图像、1,854 概念，并含大量行为/神经扩展 |
| 新模型候选 | PerceptCLIP-Memorability / ViTMem | 更接近现代视觉编码器，可做二轮核验 |
| 个人闭环 | 自建 Personal Memory MiniSet | 公开 memorability 不能等同个人记忆，必须保留人工闭环 |

本轴的关键边界：memorability 是“容易被记住”，personal memory 是“唤起我的记忆”。两者有关，但不能混同。

### 4.7 组合结构轴

组合结构轴负责回答：

```text
图像是否只是漂亮，还是对象、数量、空间、关系、推理也对？
```

保留：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 组合评估 SOTA | T2I-CompBench++ | TPAMI 2025，覆盖属性、关系、数量、空间等组合维度 |
| 对象评估 | GenEval | object-focused framework，适合 count/color/position |
| 难度可控 | ConceptMix | 可控组合难度，能测试 k 概念同时出现 |
| 推理评估 | R2I-Bench | 7 大推理类、32 小类，含 causal/concept mixing 等 |
| 舞台/关系评估 | T2I-CoReBench | 检查模型能否“布景但不能导演”的结构推理弱点 |

该轴是对 PCA-B0 的安全阀：美感不能掩盖结构错误。

### 4.8 人类验证轴

人类验证轴负责回答：

```text
自动指标选中的图，是否真的更符合人的感受？
```

保留：

| 类型 | 保留对象 | 原因 |
|---|---|---|
| 人类对齐 benchmark | DreamBench++ | 用 GPT-4o 自动评估并验证 human alignment |
| 成对偏好数据 | Pick-a-Pic / HPD v2 | 适合做 preference-only baseline |
| 小样本盲评 | PCA-B0 Human Mini Study | 必须自建，因为“个人记忆”没有公开 SOTA 替代品 |

这一轴不能外包给公开数据。公开数据只能作为代理，最终必须小样本人类验证。

## 5. 第一批核心组合

如果只选第一批实验积木，不应超过以下组合：

| 角色 | 首选 | 备选 |
|---|---|---|
| 主体 gate | IP-Adapter-Plus + DINO/CLIP similarity | DreamBooth LoRA SDXL |
| 时间调制 | Prompt-to-Prompt attention schedule | Attend-and-Excite / ControlNet scale schedule |
| 审美偏好 | ImageReward + PickScore + HPSv2 | VisionReward 二轮接入 |
| 情绪代理 | ArtEmis/EmoSet labels + CLIP/EmotionCLIP | VLM emotion explanation |
| 记忆代理 | THINGS memorability / LaMem proxy | Personal Memory MiniSet |
| 结构安全 | T2I-CompBench++ + GenEval | R2I-Bench 子集 |
| 人类验证 | 2x2 blind pairwise sheet | preference + memory-trigger explanation |

## 6. 不再进入核心的平庸项

以下资料不是没价值，而是不进入第一批核心：

| 类型 | 处理 |
|---|---|
| 只有审美分、没有偏好证据的普通 aesthetic predictor | 只做背景或轻量 baseline |
| 只在人脸上有效的 identity 方法 | 进入人像子域，不代表一般主体 |
| 只有旧 GAN latent 编辑、无法接入 diffusion 的方法 | 保留理论启发，不进第一批工程 |
| 只有综合榜单但不能解释失败类型的 benchmark | 不作为核心评估 |
| 不能公开获取或许可不清的数据 | 暂存，不进入训练核心 |

## 7. 当前结论

PCA-B0/CTAS 的下一步应写成：

> 我们不是提出一个万能指标，而是提出一个 subject-preserving activation control framework。它把主体一致性、时间干预、因果潜空间、审美偏好、情绪解释、记忆激活、组合结构和人类验证拆成正交能力轴，然后每轴采用 SOTA 积木，研究这些积木之间的冲突、互补和可组合性。

这比“找一篇能满足所有要求的文章”更接近真正的科研路线。
