# 主体一致性背景编辑数据集

本目录是第一版主体一致性背景编辑数据集的生产包。目标不是让图“更好看”，而是建立一批能验证下面合同的样本：

```text
主体不变，只改背景。
```

第一版当前目标是 120 条合格三元组：

```text
原图 + 背景编辑指令 + 编辑后图
```

扩展版在第一版之上追加四层验证数据：

```text
120 条主体 mask/bbox 标注
48 条覆盖补齐样本
50 条负样本
100 条真实图验证样本
```

## 目录结构

```text
dataset_subject_background/
  raw_sources/
  selected_sources/
  edited_targets/
  final/
    source/
    target/
  masks/
    subject/
  supplemental/
    coverage_extension/
      source/
      target/
      masks/
    negative_samples/
      source/
      target/
      masks/
  real_validation/
    source/
    target/
    masks/
  metadata/
    task_plan.csv
    task_plan.jsonl
    background_edit.csv
    background_edit.jsonl
    coverage_extension.csv
    coverage_extension.jsonl
    negative_samples.csv
    negative_samples.jsonl
    real_validation.csv
    real_validation.jsonl
    rejected.csv
  qc/
    contact_sheets/
    qc_notes.md
  scripts/
    build_task_plan.py
    cleanup_generated_cache.py
    validate_dataset.py
    generate_subject_masks.py
    generate_supplemental_sets.py
    build_real_validation_set.py
    validate_extended_dataset.py
```

## 生产步骤

1. 运行任务清单生成脚本：

```bash
python dataset_subject_background/scripts/build_task_plan.py
```

如果当前 Windows `python` 命令不可用，可使用本机 Codex runtime：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\build_task_plan.py
```

2. 按 `metadata/task_plan.csv` 的 `source_prompt` 使用 ChatGPT Image 2 生成源图，保存到 `planned_raw_source_path` 指定的位置。

3. 人工筛选源图，通过后复制到 `planned_source_path` 指定的位置。

4. 按同一行的 `edit_prompt` 使用 ChatGPT Image 2 图像编辑能力生成目标图，保存到 `planned_target_path` 指定的位置。

5. 人工质检。合格样本复制到：

```text
final/source/{sample_id}.png
final/target/{sample_id}.png
```

6. 将合格样本写入 `metadata/background_edit.csv` 和 `metadata/background_edit.jsonl`；失败样本写入 `metadata/rejected.csv`。

7. 运行验收：

```bash
python dataset_subject_background/scripts/validate_dataset.py
```

或在当前机器上使用：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\validate_dataset.py
```

## 扩展数据层

扩展数据不覆盖第一版 120 条合格集，而是作为独立 metadata 文件补充。

1. 为第一版 120 条生成主体 mask 和 bbox：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\generate_subject_masks.py
```

该脚本用保守的中心主体 ROI 生成 `masks/subject/{sample_id}.png`，并回写 `background_edit.csv`、`background_edit.jsonl` 和 `task_plan.csv`。第一版源图均按“单主体居中、完整可见”生产，因此此层用于稳定的主体保留 ROI 和 bbox；COCO 真实图验证集则使用原始实例分割标注。

2. 生成 48 条覆盖补齐和 50 条负样本：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\generate_supplemental_sets.py
```

覆盖补齐固定补齐第一版中缺失的组合：

```text
animal + background_weather: 12
animal + background_style: 12
animal + background_object: 12
object + background_replace: 12
```

负样本固定 50 条，五类失败各 10 条：

```text
subject_color_changed
subject_size_or_position_changed
subject_occluded
background_not_changed
artifact_or_low_quality
```

3. 生成 100 条真实图验证集：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\build_real_validation_set.py
```

真实图验证集来自 COCO val2017，使用实例分割标注生成 mask/bbox，再用脚本背景合成 target。分布固定为 animal/object 各 50，五种 edit type 各 20。

4. 运行扩展验收：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\validate_extended_dataset.py
```

通过时输出：

```text
Base rows with mask/bbox: 120
Coverage extension rows: 48
Negative rows: 50
Real validation rows: 100
EXTENDED_VALIDATION_OK
```

## Codex 默认生成缓存清理

ChatGPT Image 2 生成图会先落在 Codex 默认目录，例如：

```text
C:\Users\Lx050\.codex\generated_images\<thread_id>\
```

用于数据集的图片必须先复制进本目录的 `raw_sources/`、`selected_sources/`、`edited_targets/`、`final/` 后，再清理默认缓存。

固定执行规则：

```text
每生成 4 张图，也就是 2 组 source/target 样本并通过 validate_dataset.py 后，清理一次 Codex 默认生成缓存。
该会话默认生成缓存最多只能占用 30MB；清理后必须不超过 10MB，并且最多保留最近 4 张生成图。
```

清理只针对 Codex 默认生成缓存，不删除 `dataset_subject_background/` 内任何数据。先 dry-run：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\cleanup_generated_cache.py --keep-latest 4 --target-mb 10 --max-mb 30
```

确认无误后执行：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\cleanup_generated_cache.py --keep-latest 4 --target-mb 10 --max-mb 30 --apply
```

生成图片前后还要检查当前线程 JSONL 不超过 50MB。若下一次生成需要预留约 8MB，可用：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\cleanup_generated_cache.py --keep-latest 4 --target-mb 10 --max-mb 30 --session-jsonl C:\Users\Lx050\.codex\sessions\2026\05\27\rollout-2026-05-27T21-45-06-019e69ae-89ac-7c60-ba8f-58e1d16aac0a.jsonl --session-max-mb 50 --require-session-headroom-mb 8
```

如果余量不足，停止在当前线程继续生成，换新线程后从 `task_plan.csv` 中第一条 `not_started` 继续。

如果必须在同一线程继续生成，可先清理当前线程 JSONL 中已经落盘图片的嵌入式 base64 载荷，包括 `data:image/...;base64,...` 和 image generation 事件里的裸图片 `result`。先 dry-run：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\clean_session_jsonl.py C:\Users\Lx050\.codex\sessions\2026\05\27\rollout-2026-05-27T21-45-06-019e69ae-89ac-7c60-ba8f-58e1d16aac0a.jsonl --max-mb 50
```

确认只替换嵌入式图片载荷后执行：

```powershell
& 'C:\Users\Lx050\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' dataset_subject_background\scripts\clean_session_jsonl.py C:\Users\Lx050\.codex\sessions\2026\05\27\rollout-2026-05-27T21-45-06-019e69ae-89ac-7c60-ba8f-58e1d16aac0a.jsonl --max-mb 50 --apply
```

该脚本会先备份原 JSONL，再保留事件结构并替换图片载荷；不得用它清理数据集目录内的真实图片。

本扩展批次使用脚本合成与 COCO 真实图下载，没有调用内置 image generation 工具；完成后仍需清理 Codex 默认生成缓存。若本轮没有新增内嵌图片，`clean_session_jsonl.py` 会显示 `Embedded image payloads replaced: 0`。

## 字段合同

最终合格集必须保留以下字段：

```text
sample_id,
source_image,
target_image,
instruction,
edit_type,
subject_category,
subject_description,
original_background,
target_background,
keep_constraints,
negative_constraints,
source_generator,
edit_generator,
subject_bbox,
subject_mask_path,
qc_status,
reject_reason,
split
```

`split` 固定按样本顺序稳定分配：

```text
train: 70%
val: 15%
test: 15%
```

## 质检规则

先看主体，再看背景，再看画质。

必须通过：

```text
subject_identity_preserved
subject_pose_preserved
subject_color_material_preserved
subject_size_position_preserved
background_changed
instruction_followed
no_subject_occlusion
no_major_artifact
```

拒绝原因只能使用：

```text
subject_identity_changed
subject_pose_changed
subject_color_changed
subject_material_changed
subject_size_or_position_changed
subject_occluded
background_not_changed
instruction_not_followed
artifact_or_low_quality
duplicate_or_near_duplicate
unsafe_or_sensitive
```

## 关键边界

- 第一版只做动物和物体，不做真人身份样本。
- 每张图只允许一个主主体。
- 不允许整图风格迁移导致主体也变风格。
- 不允许新增遮挡主体的前景物体。
- Codex 只负责编排、命名、去重、清单、质检辅助和文档，不把空白或占位图片伪装成最终数据。
- 当前仓库生成了 120 条生产任务；真实图片需要通过 ChatGPT Image 2 按任务清单生成后再进入最终集。
