# PCA-B0 Deep Research Map

生成日期：2026-05-26  
工作目录：`G:\Lbx\paper\2026_5_25`

## 0. 这份地图要解决什么

这不是把现成方法拼在一起的清单，而是给 PCA-B0 下一阶段科研决策建立“宽度”。核心问题是：

> 在主体一致性已经过门槛的前提下，能否通过因果潜空间与扩散时间调制，让生成结果更有美感、更能打动人、更能激活人的记忆？

现有 PCA-B0 资料已经明确了一个底线：主体一致性是 gate，不是最终目标。新的调研方向应该继续保留这个底线，但把研究重心从“证明一致性”转向“控制感知激活”。

## 1. 课题主轴

### 1.1 三条线的关系

本轮讨论后，不把三条路线看成互斥选项，而是看成三层科研结构：

| 层级 | 角色 | 在课题里的位置 |
|---|---|---|
| 因果潜空间 | 理论押注 | 主体、美感、情绪、记忆不是独立维度，它们之间存在因果和调制关系 |
| 时间调制 | 工程拆分 | 扩散生成不是一次性控制，而是可按 early/mid/late 去噪阶段分别干预 |
| 记忆闭环 | 长期趋势 | 真正“打动人”的评估最终要回到个人或群体记忆反馈，而不是只靠通用美学分数 |

这意味着第一阶段不急着训练大模型，而是建立一个可收缩的研究地图：先广泛收集高质量论文、数据集、代码，再从中筛出最能服务 PCA-B0 的少量实验模块。

### 1.2 暂定理论名

暂定理论框架名：

```text
Causal-Temporal Activation Space, CTAS
```

中文可写作：

```text
因果-时间激活空间
```

它不是一个单独指标，而是一套生成控制假设。

## 2. 底层理论从哪里来

### 2.1 不是从“美学打分”出发

如果直接从 aesthetic score 或 preference score 出发，课题很容易变成“怎么让图更好看”。这不够新，也会和 PCA-B0 的主体一致性门槛冲突。

更底层的理论应该来自四个方向：

| 理论来源 | 能提供什么 | 对 PCA-B0 的用法 |
|---|---|---|
| 扩散模型生成轨迹 | 图像是在多个去噪阶段逐步形成的，不同阶段可能控制不同语义层 | 设计 early/mid/late 时间调制实验 |
| 表征解耦与潜空间编辑 | 潜变量可以对应身份、姿态、风格、光照、情绪等因素 | 定义 `S_id/S_aes/S_affect/S_mem` |
| 因果表征学习 | 潜变量未必独立，变量之间可以有因果依赖和干预效应 | 解释“美感增强为什么会伤主体”或“风格为什么会改变记忆感” |
| 认知/情绪/记忆数据 | 人的感知激活不等于图像质量，记忆性和情绪性可以被单独标注 | 设计 activation ranking 和 human study |

### 2.2 PCA-B0 的理论突破点

建议把理论突破写成：

> 主体一致性不是审美生成的对立面，而是感知激活的因果边界。只有先固定用户不可丢失的主体不变量，才能在可允许变动空间内安全地调制美感、情绪和记忆激活。

这句话把“保主体”和“变得更美”统一起来。它不是证明一个旧指标，而是提出一个新的生成控制视角。

### 2.3 潜空间不是一层，也不一定独立

用户提出的“浅空间/潜空间是否只能放一层”很关键。建议不要把潜空间写成单层、独立、线性可分，而是写成：

```text
S_id       -> 约束主体、身份、对象核心不变量
S_layout   -> 约束构图、姿态、空间关系
S_aes      -> 调制色彩、光照、质感、构图张力
S_affect   -> 调制情绪倾向，如温暖、孤独、庄严、怀旧
S_mem      -> 调制个人/文化记忆线索，如场景、物件、年代感、仪式感
```

这些空间不是互相独立的。例如：

```text
S_aes -> S_id
```

过强的风格化可能改变主体可识别性。

```text
S_layout -> S_affect
```

构图距离、视角和留白会改变情绪感。

```text
S_mem -> S_aes
```

怀旧记忆可能要求胶片颗粒、旧色温、熟悉的日常物件，而不是通用“高清好看”。

```text
S_id -> S_mem
```

如果主体身份或关键物件错了，记忆激活会直接失败。

因此 CTAS 的核心不是“找到一个更好的分数”，而是研究哪些变量可以被干预，哪些变量必须被保护，以及干预发生在扩散过程的哪个时间段最安全。

## 3. 数据从哪里来

数据不要混成一个训练集。第一阶段应拆成 5 类：

| 数据类型 | 用途 | 典型来源 | 是否直接训练 |
|---|---|---|---|
| 主体一致性数据 | 测 gate 是否守住主体 | DreamBench、DreamBench++、CustomConcept101、SubjectBench | 可用于评估和少量 adapter 实验 |
| 审美/偏好数据 | 给 activation ranker 提供美感代理 | AVA、AADB、LAION-Aesthetics、Pick-a-Pic、HPD v2、ImageRewardDB | 可训练 reward/ranker |
| 情绪数据 | 判断图像是否有明确情绪倾向 | ArtEmis、EmoSet、AffectNet、OASIS、VSO/MVSO | 可训练或评估 emotion scorer |
| 记忆数据 | 判断图像是否容易被记住或唤起记忆 | LaMem、MemNet、THINGS、SUN Memorability | 更适合评估，不宜直接等同个人记忆 |
| 提示/组合数据 | 扩大生成任务和失败案例空间 | DiffusionDB、PartiPrompts、DrawBench、T2I-CompBench、GenEval | 用于任务采样和 benchmark |

### 3.1 最小可落地数据组合

如果只做第一轮实验，建议先使用：

| 层 | 数据 |
|---|---|
| 主体 gate | DreamBench 或 CustomConcept101 |
| 候选生成 prompt | PartiPrompts + 自建 PCA-B0 prompts |
| 美感/偏好 rank | PickScore、ImageReward、HPS v2 |
| 情绪 rank | ArtEmis/EmoSet 标签词 + EmotionCLIP 或 CLIP zero-shot |
| 记忆 proxy | LaMem/MemNet 或人工记忆激活词标注 |

### 3.2 个人记忆不能完全公开数据化

公开数据只能提供 proxy。真正“激活人内心记忆”的部分，需要一个小型自建闭环：

```text
用户参考图/记忆线索 -> 生成候选 -> 用户选择/文字解释 -> 更新 activation rule
```

这个闭环不需要一开始很大。第一版可以是：

| 项 | 建议 |
|---|---|
| 参与者 | 3-5 人 |
| 每人任务 | 10-20 个记忆线索 |
| 每任务候选 | 4 张图 |
| 标注 | 哪张更像记忆、为什么、哪些元素触发了回忆、哪些元素破坏了主体 |

这会成为 PCA-B0 区分“通用漂亮”和“真正动人”的关键。

## 4. 代码需要怎么写

第一阶段不写成一个大而全系统，而是写成可替换模块：

```text
tasks
  -> candidate_generator
  -> subject_gate
  -> activation_ranker
  -> causal_temporal_controller
  -> human_eval_packager
  -> analysis_report
```

### 4.1 模块职责

| 模块 | 输入 | 输出 | 说明 |
|---|---|---|---|
| `candidate_generator` | reference、prompt、seed、method config | candidate images | 先用现成 diffusion/diffusers，不训练大模型 |
| `subject_gate` | reference image、candidate image、core invariants | pass/fail + evidence | 主体一致性只做门槛，不参与美感加分 |
| `activation_ranker` | passed candidates | aesthetic/emotion/memory proxy scores | 多分数并列，不合成一个神秘总分 |
| `causal_temporal_controller` | timestep schedule、adapter scale、attention control | controlled generation config | 研究重点，测试不同阶段干预是否更安全 |
| `human_eval_packager` | candidate set、method labels | blind sheets/forms | 支持小样本人类验证 |
| `analysis_report` | scores、human choices、failures | markdown/csv plots | 报告必须包含失败案例 |

### 4.2 第一轮实验不要一上来做什么

暂时不要：

- 不要训练 foundation model。
- 不要把美学、情绪、记忆强行合成一个总分。
- 不要让高美感分覆盖主体失败。
- 不要声称公开 memorability 数据等同个人记忆。
- 不要先堆 100 个 repo 跑通再思考理论。

第一轮应该先跑通：

```text
reference + prompt
  -> 4-8 candidates
  -> subject gate
  -> aesthetic/emotion/memory proxy rank
  -> human mini-check
  -> failure taxonomy
```

## 5. 宽度到收缩的决策规则

每条论文/数据/代码先进入宽池，再按四项打分：

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| 理论价值 | 只是工具或背景 | 能解释一部分现象 | 能支撑 CTAS 核心假设 |
| 数据可得性 | 不公开或许可不清 | 可申请/有限公开 | 公开、清晰、可复现 |
| 代码可运行性 | 无代码或过旧 | 有社区实现 | 官方代码或 diffusers/HF 集成 |
| 课题贴合度 | 与主体激活弱相关 | 可作为辅助 | 直接服务 gate/rank/time/causal |

收缩建议：

```text
总分 7-8：第一批实验核心
总分 5-6：候选保留
总分 3-4：只作为 related work
总分 0-2：淘汰或暂存
```

## 6. 推荐第一批实验

### 实验 A：时间调制是否减少主体漂移

问题：

> 同样的审美/情绪增强，如果放在不同去噪阶段，是否会产生不同程度的主体漂移？

设计：

| 组别 | 早期 | 中期 | 后期 |
|---|---|---|---|
| Baseline | 普通生成 | 普通生成 | 普通生成 |
| Early-style | 加强风格/情绪 | 普通 | 普通 |
| Mid-style | 普通 | 加强风格/情绪 | 普通 |
| Late-style | 普通 | 普通 | 加强风格/情绪 |
| CTAS | 早期锁主体 | 中期调情绪/构图 | 后期调质感/美感 |

验收：

- CTAS 组主体 gate 通过率不低于 baseline。
- CTAS 组 aesthetic/emotion proxy 高于 consistency-only。
- 人类小样本中 CTAS 被选为“更动人”的比例高于 preference-only。

### 实验 B：潜空间因果关系是否可观察

问题：

> 当我们干预审美/情绪空间时，哪些主体不变量最容易被破坏？

设计：

| 干预 | 观测 |
|---|---|
| 提高风格强度 | 主体相似度是否下降 |
| 改变构图距离 | 情绪词是否变化 |
| 加怀旧物件/色彩 | 记忆激活评分是否上升 |
| 加强身份 adapter | 美感和情绪是否变僵硬 |

这类实验可以把“潜空间之间不独立”变成可报告的经验现象。

### 实验 C：个人记忆闭环小样本

问题：

> 通用 preference model 选出的漂亮图，是否真的比 PCA-B0/CTAS 更能激活个人记忆？

设计：

| 方法 | 选择逻辑 |
|---|---|
| Preference-only | 只选 ImageReward/HPS/PickScore 高的图 |
| Consistency-only | 只选主体相似度最高的图 |
| PCA-B0 | 先 gate，再 rank |
| CTAS | 先 gate，再按时间调制策略生成/筛选 |

人类问题：

- 哪张最像你记忆里的感觉？
- 哪张最美？
- 哪张最不像原主体？
- 哪些元素触发了回忆？
- 哪些元素破坏了回忆？

## 7. 文件说明

本次生成的三个矩阵：

| 文件 | 用途 |
|---|---|
| `pca_b0_paper_matrix.csv` | 论文和理论来源宽池，覆盖主体一致性、时间控制、因果潜空间、美学偏好、情绪记忆和 benchmark |
| `pca_b0_dataset_map.csv` | 数据集/benchmark 来源，区分训练、评估、代理和人工闭环 |
| `pca_b0_code_repo_map.csv` | 可复用代码仓库，说明可接入 PCA-B0 的位置 |

这些文件不是最终综述，而是第一版研究地图。下一步应该对每条资料补充 BibTeX、license、下载状态、运行状态和本地复现实验结果。

## 8. 当前结论

PCA-B0 现在最有科研价值的表述是：

> 它不是一个证明系统，也不是一个美学打分器，而是一个 subject-preserving perceptual activation framework。它先守住用户不可丢失的主体不变量，再研究如何在可变空间里通过因果潜变量和扩散时间阶段调制，让图像更美、更有情绪、更能唤起记忆。

这让课题从“选图 baseline”进一步升级为“主体一致性约束下的感知激活生成控制”。
