import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
REQUIRED_COLUMNS = [
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
REQUIRED_INSTRUCTION_FRAGMENTS = ["保持主体", "仅将背景"]
VALID_REJECT_REASONS = {
    "subject_identity_changed",
    "subject_pose_changed",
    "subject_color_changed",
    "subject_material_changed",
    "subject_size_or_position_changed",
    "subject_occluded",
    "background_not_changed",
    "instruction_not_followed",
    "artifact_or_low_quality",
    "duplicate_or_near_duplicate",
    "unsafe_or_sensitive",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path} missing required columns: {', '.join(missing)}")
        return list(reader)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def image_files(path: Path) -> list[Path]:
    return sorted(file for file in path.iterdir() if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS)


def validate_final_rows(dataset_root: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    sample_ids = [row["sample_id"] for row in rows]
    duplicates = [sample_id for sample_id, count in Counter(sample_ids).items() if count > 1]
    require(not duplicates, f"Duplicate sample_id values: {duplicates}", errors)

    final_sources = image_files(dataset_root / "final" / "source")
    final_targets = image_files(dataset_root / "final" / "target")
    require(len(final_sources) == len(rows), "final/source image count must equal background_edit.csv rows", errors)
    require(len(final_targets) == len(rows), "final/target image count must equal background_edit.csv rows", errors)

    source_hashes: dict[str, str] = {}
    target_hashes: dict[str, str] = {}
    for row in rows:
        sample_id = row["sample_id"]
        source_path = dataset_root / row["source_image"]
        target_path = dataset_root / row["target_image"]
        require(source_path.exists(), f"{sample_id} missing source image: {row['source_image']}", errors)
        require(target_path.exists(), f"{sample_id} missing target image: {row['target_image']}", errors)
        for fragment in REQUIRED_INSTRUCTION_FRAGMENTS:
            require(fragment in row["instruction"], f"{sample_id} instruction missing fragment: {fragment}", errors)
        require(row["qc_status"] == "accepted", f"{sample_id} final row qc_status must be accepted", errors)
        require(row["split"] in {"train", "val", "test"}, f"{sample_id} invalid split: {row['split']}", errors)

        if source_path.exists():
            source_hash = sha256(source_path)
            if source_hash in source_hashes:
                errors.append(f"{sample_id} duplicates source image with {source_hashes[source_hash]}")
            source_hashes[source_hash] = sample_id
        if target_path.exists():
            target_hash = sha256(target_path)
            if target_hash in target_hashes:
                errors.append(f"{sample_id} duplicates target image with {target_hashes[target_hash]}")
            target_hashes[target_hash] = sample_id


def validate_rejected_rows(rows: list[dict[str, str]], errors: list[str]) -> None:
    for row in rows:
        sample_id = row["sample_id"] or "<missing sample_id>"
        reasons = [reason for reason in row["reject_reason"].split(";") if reason]
        require(bool(reasons), f"{sample_id} rejected row must include reject_reason", errors)
        invalid = [reason for reason in reasons if reason not in VALID_REJECT_REASONS]
        require(not invalid, f"{sample_id} invalid reject_reason values: {invalid}", errors)


def validate_jsonl(csv_rows: list[dict[str, str]], jsonl_path: Path, errors: list[str]) -> None:
    if not jsonl_path.exists():
        errors.append(f"Missing file: {jsonl_path}")
        return
    lines = [line for line in jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(lines) == len(csv_rows), "background_edit.jsonl row count must equal background_edit.csv", errors)
    for index, line in enumerate(lines, start=1):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSONL line {index}: {exc}")
            continue
        for column in REQUIRED_COLUMNS:
            require(column in obj, f"JSONL line {index} missing field: {column}", errors)


def validate_task_plan(metadata_dir: Path, errors: list[str]) -> None:
    task_plan = metadata_dir / "task_plan.csv"
    if not task_plan.exists():
        errors.append(f"Missing file: {task_plan}")
        return
    with task_plan.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 120, "task_plan.csv must contain 120 planned source/edit tasks", errors)

    subject_counts = Counter(row["subject_category"] for row in rows)
    require(dict(subject_counts) == {"animal": 60, "object": 60}, f"Unexpected subject distribution: {dict(subject_counts)}", errors)

    edit_counts = Counter(row["edit_type"] for row in rows)
    expected_edit_counts = {
        "background_replace": 48,
        "background_time": 24,
        "background_weather": 24,
        "background_style": 12,
        "background_object": 12,
    }
    require(dict(edit_counts) == expected_edit_counts, f"Unexpected edit distribution: {dict(edit_counts)}", errors)

    split_counts = Counter(row["split"] for row in rows)
    require(dict(split_counts) == {"train": 84, "val": 18, "test": 18}, f"Unexpected split distribution: {dict(split_counts)}", errors)

    for row in rows:
        for fragment in REQUIRED_INSTRUCTION_FRAGMENTS:
            require(fragment in row["instruction"], f"{row['sample_id']} task instruction missing fragment: {fragment}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_root", default=str(ROOT))
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root).resolve()
    metadata_dir = dataset_root / "metadata"
    errors: list[str] = []

    final_rows = read_csv(metadata_dir / "background_edit.csv")
    rejected_rows = read_csv(metadata_dir / "rejected.csv")
    validate_task_plan(metadata_dir, errors)
    validate_final_rows(dataset_root, final_rows, errors)
    validate_rejected_rows(rejected_rows, errors)
    validate_jsonl(final_rows, metadata_dir / "background_edit.jsonl", errors)

    print(f"Final accepted rows: {len(final_rows)}")
    print(f"Rejected rows: {len(rejected_rows)}")
    if errors:
        print("VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
