import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
REQUIRED_BASE_COLUMNS = [
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


def read_csv(path: Path, required_columns: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in required_columns if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path} missing columns: {missing}")
        return list(reader)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def image_size(rel_path: str, errors: list[str]) -> tuple[int, int] | None:
    path = ROOT / rel_path
    require(path.exists(), f"Missing file: {rel_path}", errors)
    require(path.suffix.lower() in IMAGE_EXTENSIONS, f"Unexpected image extension: {rel_path}", errors)
    if not path.exists():
        return None
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            return image.size
    except Exception as exc:
        errors.append(f"Unreadable image {rel_path}: {exc}")
        return None


def validate_mask(mask_rel: str, expected_size: tuple[int, int] | None, sample_id: str, name: str, errors: list[str]) -> None:
    path = ROOT / mask_rel
    require(path.exists(), f"Missing file: {mask_rel}", errors)
    if not path.exists():
        return
    try:
        mask = Image.open(path).convert("L")
    except Exception as exc:
        errors.append(f"Unreadable mask {mask_rel}: {exc}")
        return
    if expected_size:
        require(mask.size == expected_size, f"{name} {sample_id} mask size mismatch: {mask.size} != {expected_size}", errors)
    mask_pixels = np.asarray(mask, dtype=np.uint8)
    require(bool(np.any(mask_pixels > 0)), f"{name} {sample_id} mask is empty", errors)


def validate_bbox(bbox: str, image_size_value: tuple[int, int] | None, sample_id: str, name: str, errors: list[str]) -> None:
    parts = bbox.split(",")
    require(len(parts) == 4, f"{name} {sample_id} invalid bbox format: {bbox}", errors)
    if len(parts) != 4:
        return
    try:
        x, y, width, height = [int(round(float(value))) for value in parts]
    except ValueError:
        errors.append(f"{name} {sample_id} non-numeric bbox: {bbox}")
        return
    require(width > 0 and height > 0, f"{name} {sample_id} bbox must be positive: {bbox}", errors)
    if image_size_value:
        image_width, image_height = image_size_value
        require(0 <= x < image_width and 0 <= y < image_height, f"{name} {sample_id} bbox starts outside image: {bbox}", errors)
        require(x + width <= image_width and y + height <= image_height, f"{name} {sample_id} bbox exceeds image: {bbox}", errors)


def validate_rows(
    rows: list[dict[str, str]], expected_count: int, name: str, errors: list[str], require_pair_size_match: bool = True
) -> None:
    require(len(rows) == expected_count, f"{name} must contain {expected_count} rows, found {len(rows)}", errors)
    duplicates = [sample_id for sample_id, count in Counter(row["sample_id"] for row in rows).items() if count > 1]
    require(not duplicates, f"{name} duplicate sample ids: {duplicates}", errors)
    for row in rows:
        sample_id = row["sample_id"]
        source_size = image_size(row["source_image"], errors)
        target_size = image_size(row["target_image"], errors)
        if require_pair_size_match:
            require(
                source_size == target_size,
                f"{name} {sample_id} source/target size mismatch: {source_size} != {target_size}",
                errors,
            )
        validate_mask(row["subject_mask_path"], source_size, sample_id, name, errors)
        require(bool(row["subject_bbox"]), f"{name} {sample_id} missing subject_bbox", errors)
        validate_bbox(row["subject_bbox"], source_size, sample_id, name, errors)
        require("保持主体" in row["instruction"], f"{name} {sample_id} instruction missing 保持主体", errors)


def validate_jsonl(csv_rows: list[dict[str, str]], jsonl_path: Path, errors: list[str]) -> None:
    if not jsonl_path.exists():
        errors.append(f"Missing file: {jsonl_path}")
        return
    lines = [line for line in jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(lines) == len(csv_rows), f"{jsonl_path.name} row count mismatch", errors)
    for index, line in enumerate(lines, start=1):
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{jsonl_path.name} invalid JSON on line {index}: {exc}")


def main() -> int:
    errors: list[str] = []
    base_rows = read_csv(METADATA_DIR / "background_edit.csv", REQUIRED_BASE_COLUMNS)
    coverage_rows = read_csv(METADATA_DIR / "coverage_extension.csv", REQUIRED_BASE_COLUMNS + ["base_sample_id", "extension_axis"])
    negative_rows = read_csv(METADATA_DIR / "negative_samples.csv", REQUIRED_BASE_COLUMNS + ["base_sample_id", "negative_type"])
    real_rows = read_csv(
        METADATA_DIR / "real_validation.csv",
        REQUIRED_BASE_COLUMNS + ["external_dataset", "external_image_id", "external_category_id", "external_category_name"],
    )

    validate_rows(base_rows, 120, "base", errors, require_pair_size_match=False)
    validate_rows(coverage_rows, 48, "coverage_extension", errors)
    validate_rows(negative_rows, 50, "negative_samples", errors)
    validate_rows(real_rows, 100, "real_validation", errors)

    base_missing_masks = [row["sample_id"] for row in base_rows if not row["subject_mask_path"] or not row["subject_bbox"]]
    require(not base_missing_masks, f"Base rows missing mask/bbox: {base_missing_masks[:10]}", errors)

    coverage_counts = Counter((row["subject_category"], row["edit_type"]) for row in coverage_rows)
    expected_coverage = {
        ("animal", "background_weather"): 12,
        ("animal", "background_style"): 12,
        ("animal", "background_object"): 12,
        ("object", "background_replace"): 12,
    }
    require(dict(coverage_counts) == expected_coverage, f"Unexpected coverage extension distribution: {dict(coverage_counts)}", errors)

    negative_counts = Counter(row["reject_reason"] for row in negative_rows)
    require(set(negative_counts).issubset(VALID_REJECT_REASONS), f"Invalid negative reject reasons: {dict(negative_counts)}", errors)
    require(all(row["qc_status"] == "rejected" for row in negative_rows), "All negative rows must be rejected", errors)

    real_source_counts = Counter(row["source_generator"] for row in real_rows)
    require(dict(real_source_counts) == {"coco_val2017": 100}, f"Unexpected real source generators: {dict(real_source_counts)}", errors)

    validate_jsonl(coverage_rows, METADATA_DIR / "coverage_extension.jsonl", errors)
    validate_jsonl(negative_rows, METADATA_DIR / "negative_samples.jsonl", errors)
    validate_jsonl(real_rows, METADATA_DIR / "real_validation.jsonl", errors)

    print(f"Base rows with mask/bbox: {len(base_rows) - len(base_missing_masks)}")
    print(f"Coverage extension rows: {len(coverage_rows)}")
    print(f"Negative rows: {len(negative_rows)}")
    print(f"Real validation rows: {len(real_rows)}")
    if errors:
        print("EXTENDED_VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EXTENDED_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
