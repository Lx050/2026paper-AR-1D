# PCA-B0 PDF/VLM 阅读报告

生成日期：2026-05-25  
工作目录：`G:\Lbx\paper\2026_5_25`

## 1. 读取范围与验证

本报告整理当前目录下 6 个 PDF 的阅读结果，包括 5 个 weekly runbook 和 1 个 guiding charter。

| 文件 | 页数 | 角色 |
|---|---:|---|
| `week1_experiment_runbook_v3.pdf` | 9 | 资源清算、环境搭建、PCA-B0 定义 |
| `week2_experiment_runbook_v3.pdf` | 8 | 评分器安装、调用、统一 CSV 输出 |
| `week3_experiment_runbook_v3.pdf` | 8 | 候选生成、门控、排序 pipeline |
| `week4_experiment_runbook_v3.pdf` | 8 | 人类小样本验证、激活词标注 |
| `week5_experiment_runbook_v3.pdf` | 9 | 分析、消融、报告、论文雏形 |
| `PCA_B0_guiding_charter_v1.pdf` | 11 | 指导层 / 宪法层 / 判断层 |

合计：6 个 PDF，53 页。

## 2. 读取方法

- 文本索引：使用 `pypdf` 抽取每页文本，生成页级目录、关键词标记和内容摘要。
- 视觉核对：将 53 页临时渲染为 PNG，并生成 6 张 PDF 总览图；用 VLM 检查标题层级、表格、命令块、页码和中文排版。
- 临时文件：页面图和总览图只用于核对，完成后已删除。
- 结论可靠性：`pypdf` 文本与 VLM 视觉核对一致；没有发现渲染失败、页码错乱或明显文本错位。

## 3. 总纲摘要

`PCA_B0_guiding_charter_v1.pdf` 是整套资料的最高层文档。它定义 PCA-B0 的共同判断顺序：

> 先保住用户最不想失去的核心不变量，再在合格候选中选择最能激活用户感知、记忆、情绪和偏好的输出。

核心公式是：

```text
Good Output = Core Consistency Gate + Perceptual Activation Ranking
```

总纲将实验拆成三层目标：

- 显像层：输出先作为可显示、可感知的信号存在，第一阶段落在图像生成上。
- 一致性层：参考图不是复制模板，而是用户价值锚点；必须保留核心不变量。
- 激活层：通过门控后，才比较偏好、情绪、记忆、文化语境等激活效果。

关键原则包括：一致性是门槛不是终点；偏离不一定是错；指标是证据不是裁判；每个实验必须能失败；数据集服务于定义，不反过来支配定义。

总纲还给出决策规则：

- 偏好分高但主体一致性低：不合格。
- 主体一致性高但用户不喜欢：通过门控但排序失败。
- 自动指标高但用户拒绝：指标失真，加入 evaluator failure set。
- 偏离参考但用户更喜欢：如果核心不变量没有丢，可能是成功。
- 所有候选都不过门控：候选生成能力不足或任务约束过强。
- 人类也无法判断：任务欠定或约束冲突。

失败分型包括任务欠定、不变量错误、表示缺失、耦合缺失、搜索失败、约束冲突、底座能力不足。

## 4. 五周 Runbook 摘要

### Week 1：资源清算、环境搭建与 PCA-B0 定义

目标是先搭骨架，再跑实验。第 1 周禁止训练模型、禁止盲目下载所有大数据、禁止开始写论文结论。

本周产物：

- PCA-B0 项目目录骨架。
- `README_research.md`，写清目标和边界。
- Python/Conda 环境与 smoke test。
- Hugging Face 缓存、登录、权限配置。
- `resource_matrix.csv`，登记资源的 paper/repo/data/weights/license/第一阶段用途。
- `pca_b0_schema.json`，统一 task、candidate、score、human eval 字段。
- 3 条 smoke pilot tasks。
- Week2 scorer 优先级。

Go/No-Go 标准：环境 smoke test、资源矩阵、schema、3 条 smoke tasks、Week2 scorer 优先级都完成后，才进入 Week 2。

### Week 2：评分器安装、调用与统一输出

目标是把候选图变成可比较数据行，而不是产出漂亮图片。每个 scorer 必须支持输入 CSV、输出 CSV、错误不崩溃、可批处理。

评分模块：

- Preference：ImageReward 必跑，HPSv2 或 PickScore 至少跑一个。
- Emotion：EmotionCLIP 优先，不顺则 CLIP zero-shot 情绪词。
- Subject：CLIP/DINO 参考相似度优先。
- Structure：GenEval 优先，不顺则人工 `structure_pass` 模板。
- Text：EasyOCR 或 PaddleOCR，第一版只做 exact/contains。
- Memory：LaMem/MemNet 可能环境较旧，第一版可先记录或用 proxy。

重要原则：偏好分数不是个人记忆激活，也不应该单独决定最终输出；结构和 OCR 的复杂依赖不要卡住第一版 pipeline。

### Week 3：候选生成、门控与排序 Pipeline

目标是从评分器变成完整实验。流程为：

```text
任务表 -> 候选生成 -> 多评分 -> 一致性门控 -> 感知激活排序 -> baseline 对比
```

任务设计：

- 建 50 条任务，不要更多。
- 每条任务必须写出不变量、允许变化、禁止丢失。
- 类型覆盖 subject、spatial、count/color、text、culture/emotion。
- 每条任务生成 4 个 seeds，避免把搜索失败误判成结构失败。

对比方法：

| 方法 | 选图规则 | 暴露的问题 |
|---|---|---|
| Raw | 每个 task 取第一个 seed | 最低基线 |
| Preference-only | 取 ImageReward/HPS 最高 | 好看但可能丢主体/结构 |
| Consistency-only | 取 subject/structure 最高 | 像但可能无激活感 |
| PCA-B0 | 先 gate，再 rank | 核心不丢，同时优化激活 |

验收要求：`reports/week3_pipeline_report.md` 至少放 5 个案例，解释某张图为什么被 gate 拒绝、某张图为什么被 rank 选中。

### Week 4：人类小样本验证与激活词标注

目标是用人类判断校验 baseline。自动指标只是代理，最终要回答 PCA-B0 是否比 preference-only 和 consistency-only 更接近用户判断。

标注设计：

- 从 Week3 选 20-30 个任务。
- 每个任务准备 4 张图：Raw、Preference-only、Consistency-only、PCA-B0。
- 四张图随机打乱顺序，做成 2x2 contact sheet。
- 标注者只看 A/B/C/D，不需要知道方法来源。

建议规模：

| 规模 | 要求 |
|---|---|
| 最低 | 5 人 × 20 题 = 100 条选择 |
| 较稳 | 10 人 × 30 题 = 300 条选择 |
| 单人时长 | 不超过 20 分钟 |
| 记录 | 匿名 user_id、annotation_item_id、选择、理由、激活词 |

Week4 报告必须回答：

- PCA-B0 是否更常被选。
- preference-only 是否丢核心。
- consistency-only 是否无激活。
- 用户激活词是否支持理论。
- 哪些任务失败，并按 subject/spatial/text/culture 分类。

### Week 5：分析、消融、报告与论文雏形

目标是把 pilot 变成可交付科研材料。第 5 周不是继续跑更多图，而是清算脚本可复现性、结果可信度、pilot 边界和下一阶段扩展。

核心产物：

- 汇总 Week1-4 报告和核心 CSV。
- 生成三张核心表：Resources、Methods、Human Metrics。
- 使用描述统计和 bootstrap CI，不写夸张显著性结论。
- 建失败案例库。
- 写下一轮消融设计。
- 写论文 0 框架。
- 完成复现与开源前检查。

失败案例库至少收集：

| 失败类型 | 至少收集 |
|---|---|
| Preference-only failure | 3 个：好看但丢主体/结构/文字 |
| Consistency-only failure | 3 个：一致但用户不喜欢/无激活 |
| Emotion-overfit | 3 个：情绪强但任务错 |
| Culture mismatch | 3 个：视觉合理但地域语境错 |
| Evaluator failure | 3 个：自动分高但用户反对 |

下一 10 周路线：

- Week 6-7：扩展到 200-500 tasks，稳定 scorer 缓存。
- Week 8-9：用 pairwise 数据学习 rank 权重。
- Week 10-11：加入 IP-Adapter/PhotoMaker 作为 reference-guided generation baseline。
- Week 12-13：做文化/地域 subset 和个体偏好 subset。
- Week 14-15：论文 0 完整初稿和仓库整理。

## 5. 页级目录

### `week1_experiment_runbook_v3.pdf`

| 页 | 内容 |
|---:|---|
| 1 | 第 1 周总览：资源清算、环境搭建、PCA-B0 定义；列出目录骨架、smoke test、资源矩阵、schema、Week2 就绪。 |
| 2 | Day 1：项目目录和 README。 |
| 3 | Day 2：Python/Conda 环境。 |
| 4 | Day 3：Hugging Face 登录、缓存和权限。 |
| 5 | Day 4：资源矩阵逐项清算，上半部分资源。 |
| 6 | 资源矩阵逐项清算，下半部分资源和 CSV 模板。 |
| 7 | Day 5：Smoke tests，不生成图，只验证库能用。 |
| 8 | Day 6：Schema 和 Pilot Task 模板。 |
| 9 | Day 7：周报告和进入 Week2 的 Go/No-Go。 |

### `week2_experiment_runbook_v3.pdf`

| 页 | 内容 |
|---:|---|
| 1 | 第 2 周总览：评分器安装、调用与统一输出。 |
| 2 | Step 1：统一输入 CSV。 |
| 3 | Step 2：ImageReward 偏好评分器。 |
| 4 | Step 3：HPSv2 或 PickScore 二级偏好评分器。 |
| 5 | Step 4：EmotionCLIP / CLIP zero-shot 情绪评分。 |
| 6 | Step 5：Subject consistency 初版。 |
| 7 | Step 6：Structure / OCR / Relation。 |
| 8 | Step 7：合并分数并做质量检查。 |

### `week3_experiment_runbook_v3.pdf`

| 页 | 内容 |
|---:|---|
| 1 | 第 3 周总览：候选生成、门控与排序 pipeline。 |
| 2 | Step 1：建 50 条任务，不要更多。 |
| 3 | Step 2：生成 Raw candidates。 |
| 4 | Step 3：创建 rewrite baseline。 |
| 5 | Step 4：Matched / Mismatched augmentation。 |
| 6 | Step 5：合并 Week2 scorers 跑全候选。 |
| 7 | Step 6：Gate + Rank。 |
| 8 | Step 7：对比四个 baseline。 |

### `week4_experiment_runbook_v3.pdf`

| 页 | 内容 |
|---:|---|
| 1 | 第 4 周总览：人类小样本验证与激活词标注。 |
| 2 | Step 1：选择任务和候选图。 |
| 3 | Step 2：标注说明，给用户看的原文。 |
| 4 | Step 3：制作 contact sheets。 |
| 5 | Step 4：收集标注。 |
| 6 | Step 5：计算人类指标。 |
| 7 | Step 6：激活词分析。 |
| 8 | Step 7：Week4 报告必须回答的问题。 |

### `week5_experiment_runbook_v3.pdf`

| 页 | 内容 |
|---:|---|
| 1 | 第 5 周总览：分析、消融、报告与论文雏形。 |
| 2 | Step 1：汇总所有文件。 |
| 3 | Step 2：画三张核心表。 |
| 4 | Step 3：统计不要过度。 |
| 5 | Step 4：失败案例库。 |
| 6 | Step 5：消融实验设计。 |
| 7 | Step 6：论文 0 框架。 |
| 8 | Step 7：复现与开源前检查。 |
| 9 | Step 8：下一 10 周路线。 |

### `PCA_B0_guiding_charter_v1.pdf`

| 页 | 内容 |
|---:|---|
| 1 | 封面：PCA-B0 总纲，感知激活-一致性基线的指导层。 |
| 2 | 为什么需要总纲、总命题。 |
| 3 | 三层目标：显像层、一致性层、激活层。 |
| 4 | 核心公式：输入、一致性门控、感知激活排序、最终输出。 |
| 5 | 十二条指导原则，上半部分。 |
| 6 | 十二条指导原则，下半部分；核心概念字典；Week1 统领逻辑。 |
| 7 | Week2-Week5 如何受指导层统领。 |
| 8 | 决策规则；失败分型 F1-F4。 |
| 9 | 失败分型 F5-F7；实验验收标准。 |
| 10 | 数据表总规范；风险边界和不做的事。 |
| 11 | 必须谨慎表达的事；总纲在项目中的位置；挂在墙上的一句话。 |

## 6. 相比初次查看的新增/纠正

- 初次直接读取部分 PDF 时出现编码噪声；使用内置 `pypdf` 后，中文文本可以干净抽取。
- VLM 视觉核对确认 PDF 页面本身排版清晰，没有发现表格、代码块、页码错乱。
- 原始分辨率抽查覆盖了每个 PDF 的首页、末页、命令页、表格页和风险页。
- 当前资料包没有真正的 VLM 实验模块；这里的 VLM 仅用于阅读和核对 PDF 内容，不代表已把 VLM 接入 PCA-B0 pipeline。

## 7. 后续建议

如果要继续把这套资料推进成可执行项目，建议下一步先做 Week1 产物：

1. 建 PCA-B0 项目骨架。
2. 整理 `resource_matrix.csv`。
3. 固化 `pca_b0_schema.json`。
4. 跑环境 smoke test。
5. 写 3 条 smoke pilot tasks。

如果要把 VLM 纳入实验流程，建议作为 Week2/Week3 的新增 scorer，不直接替代人类评估。较稳的放法是：VLM 辅助判定 structure、OCR、forbidden loss 和解释性 reject reason；最终仍由 Week4 人类小样本验证。
