# QC Notes

## 人工质检顺序

1. 主体是否还是同一个主体。
2. 主体姿态、轮廓、颜色、材质、大小、画面位置是否稳定。
3. 背景是否按指令改变。
4. 主体是否被新增物体遮挡。
5. 画面是否有明显伪影、断裂、错位或低清问题。

## 缓存清理节奏

- 每生成 4 张图，也就是 2 组 `source/target` 样本后，先运行 `scripts/validate_dataset.py`。
- 验证通过后，运行 `scripts/cleanup_generated_cache.py --keep-latest 4 --target-mb 10 --max-mb 30` 做 dry-run。
- dry-run 确认只会清理 `C:\Users\Lx050\.codex\generated_images\...` 下的默认生成缓存后，再加 `--apply` 执行。
- 该会话默认生成缓存最多只能占用 30MB；清理后必须不超过 10MB，最多保留最近 4 张生成图。
- 清理脚本不得删除 `dataset_subject_background/` 内的任何源图、目标图、最终图或 metadata。
- 当前生产按 `task_plan.csv` 的 `production_status` 继续；每新增 2 组 accepted 后触发一次验证和缓存清理。
- 当前线程 JSONL 目标上限为 50MB；每轮验证时同步检查，超过上限必须先清理默认生成缓存并停止继续生成，避免线程文件继续膨胀。

## 记录格式

```text
sample_id:
  decision: accepted|rejected
  reject_reason:
  note:
```

## 通过示例

```text
sbg_000001:
  decision: accepted
  reject_reason:
  note: 主体狐狸的姿态、颜色和位置稳定，背景从森林改为海边栈道。
```

## 拒绝示例

```text
sbg_000002:
  decision: rejected
  reject_reason: subject_color_changed
  note: 主体猫的毛色从橙色变成灰色，违反主体不变合同。
```
