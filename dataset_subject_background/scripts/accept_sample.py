import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELDNAMES = [
    "sample_id",
    "source_image",
    "target_image",
    "instruction",
    "edit_type",
    "subject_category",
    "subject_description",
    "original_background",
    "target_background",
    "keep_constraints",
    "negative_constraints",
    "source_generator",
    "edit_generator",
    "subject_bbox",
    "subject_mask_path",
    "qc_status",
    "reject_reason",
    "split",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def ensure_writable(path: Path) -> None:
    try:
        with path.open("r+", encoding="utf-8"):
            pass
    except PermissionError as exc:
        raise SystemExit(
            f"Metadata file is locked or not writable: {path}. Close it in spreadsheet editors and retry."
        ) from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sample_id")
    args = parser.parse_args()

    sample_id = args.sample_id
    metadata_dir = ROOT / "metadata"
    task_plan_path = metadata_dir / "task_plan.csv"
    accepted_path = metadata_dir / "background_edit.csv"
    jsonl_path = metadata_dir / "background_edit.jsonl"

    task_fieldnames, tasks = read_csv(task_plan_path)
    matches = [row for row in tasks if row["sample_id"] == sample_id]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one task row for {sample_id}, found {len(matches)}")
    task = matches[0]

    selected_source = ROOT / task["planned_source_path"]
    edited_target = ROOT / task["planned_target_path"]
    if not selected_source.exists():
        raise SystemExit(f"Missing selected source: {selected_source}")
    if not edited_target.exists():
        raise SystemExit(f"Missing edited target: {edited_target}")
    for metadata_path in (task_plan_path, accepted_path, jsonl_path):
        ensure_writable(metadata_path)

    final_source_rel = f"final/source/{sample_id}.png"
    final_target_rel = f"final/target/{sample_id}.png"
    final_source = ROOT / final_source_rel
    final_target = ROOT / final_target_rel
    final_source.parent.mkdir(parents=True, exist_ok=True)
    final_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(selected_source, final_source)
    shutil.copy2(edited_target, final_target)

    _, accepted_rows = read_csv(accepted_path)
    accepted_rows = [row for row in accepted_rows if row["sample_id"] != sample_id]
    accepted_rows.append(
        {
            "sample_id": sample_id,
            "source_image": final_source_rel,
            "target_image": final_target_rel,
            "instruction": task["instruction"],
            "edit_type": task["edit_type"],
            "subject_category": task["subject_category"],
            "subject_description": task["subject_description"],
            "original_background": task["original_background"],
            "target_background": task["target_background"],
            "keep_constraints": task["keep_constraints"],
            "negative_constraints": task["negative_constraints"],
            "source_generator": task["source_generator"],
            "edit_generator": task["edit_generator"],
            "subject_bbox": task["subject_bbox"],
            "subject_mask_path": task["subject_mask_path"],
            "qc_status": "accepted",
            "reject_reason": "",
            "split": task["split"],
        }
    )
    accepted_rows.sort(key=lambda row: row["sample_id"])
    write_csv(accepted_path, FIELDNAMES, accepted_rows)
    jsonl_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in accepted_rows),
        encoding="utf-8",
    )

    task["qc_status"] = "accepted"
    task["production_status"] = "accepted"
    write_csv(task_plan_path, task_fieldnames, tasks)
    print(f"Accepted {sample_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
