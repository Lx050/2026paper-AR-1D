import csv
import json
import shutil
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"
REAL_DIR = ROOT / "real_validation"
CACHE_DIR = ROOT / ".cache" / "coco2017"
ANNOTATION_JSON_URL = "https://huggingface.co/datasets/pcuenq/coco2017-instances/resolve/main/instances_val2017.json"
VAL_IMAGE_URL = "http://images.cocodataset.org/val2017/{file_name}"
TARGET_COUNT = 100
REAL_COLUMNS = [
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
    "external_dataset",
    "external_image_id",
    "external_category_id",
    "external_category_name",
]
ANIMAL_CATEGORIES = {"bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"}
OBJECT_CATEGORIES = {
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "bench",
    "backpack",
    "umbrella",
    "handbag",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
}
EDIT_TYPES = ["background_replace", "background_time", "background_weather", "background_style", "background_object"]


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return
    with urllib.request.urlopen(url, timeout=120) as response, target.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def ensure_annotations() -> Path:
    annotation_path = CACHE_DIR / "annotations" / "instances_val2017.json"
    if annotation_path.exists():
        return annotation_path
    download(ANNOTATION_JSON_URL, annotation_path)
    return annotation_path


def polygon_mask(size: tuple[int, int], segmentation: list) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    for polygon in segmentation:
        if len(polygon) >= 6:
            points = [(polygon[i], polygon[i + 1]) for i in range(0, len(polygon), 2)]
            draw.polygon(points, fill=255)
    return mask


def bbox_string(bbox: list[float]) -> str:
    return ",".join(str(int(round(value))) for value in bbox)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def make_background(size: tuple[int, int], edit_type: str, index: int) -> Image.Image:
    width, height = size
    top = np.array([(index * 31) % 90 + 150, (index * 17) % 80 + 150, (index * 43) % 80 + 150], dtype=np.float32)
    bottom = np.array([(index * 19) % 80 + 70, (index * 29) % 80 + 90, (index * 11) % 80 + 100], dtype=np.float32)
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / max(1, height - 1)
        arr[y, :, :] = np.round(top * (1 - ratio) + bottom * ratio)
    image = Image.fromarray(arr, mode="RGB")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle([0, int(height * 0.68), width, height], fill=(75, 95, 85, 255))

    if edit_type == "background_weather":
        for x in range(0, width, 23):
            draw.line([(x, 0), (x + 45, height)], fill=(230, 235, 245, 150), width=2)
    elif edit_type == "background_style":
        step = max(40, width // 9)
        for y in range(-step, height + step, step):
            for x in range(-step, width + step, step):
                draw.rectangle([x, y, x + step, y + step], fill=((x + index) % 255, (y + 90) % 255, 180, 135))
    elif edit_type == "background_object":
        for x in range(width // 8, width, width // 8):
            draw.ellipse([x, height // 5, x + 12, height // 5 + 12], fill=(255, 220, 80, 190))
            draw.line([x + 6, height // 5 + 12, x + 6, height // 5 + 80], fill=(70, 70, 60, 150), width=2)
    elif edit_type == "background_time":
        overlay = Image.new("RGBA", size, (25, 35, 70, 82))
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    return image.filter(ImageFilter.GaussianBlur(radius=1.2))


def composite_target(source: Image.Image, mask: Image.Image, edit_type: str, index: int) -> Image.Image:
    background = make_background(source.size, edit_type, index)
    soft_mask = mask.filter(ImageFilter.GaussianBlur(radius=1.0))
    return Image.composite(source, background, soft_mask)


def category_group(category_name: str) -> str | None:
    if category_name in ANIMAL_CATEGORIES:
        return "animal"
    if category_name in OBJECT_CATEGORIES:
        return "object"
    return None


def select_annotations(coco: dict) -> list[dict]:
    categories = {item["id"]: item["name"] for item in coco["categories"]}
    images = {item["id"]: item for item in coco["images"]}
    annotations = []
    seen_images: set[int] = set()
    target_by_group = {"animal": TARGET_COUNT // 2, "object": TARGET_COUNT // 2}
    counts = {"animal": 0, "object": 0}
    for ann in sorted(coco["annotations"], key=lambda item: item.get("area", 0), reverse=True):
        if ann.get("iscrowd"):
            continue
        if ann["image_id"] in seen_images:
            continue
        category_name = categories[ann["category_id"]]
        group = category_group(category_name)
        if not group:
            continue
        if counts[group] >= target_by_group[group]:
            continue
        if not isinstance(ann.get("segmentation"), list):
            continue
        image = images[ann["image_id"]]
        area_ratio = ann.get("area", 0) / max(1, image["width"] * image["height"])
        if area_ratio < 0.04 or area_ratio > 0.72:
            continue
        ann = dict(ann)
        ann["category_name"] = category_name
        ann["subject_category"] = group
        ann["file_name"] = image["file_name"]
        ann["width"] = image["width"]
        ann["height"] = image["height"]
        annotations.append(ann)
        seen_images.add(ann["image_id"])
        counts[group] += 1
        if all(counts[group_name] >= target for group_name, target in target_by_group.items()):
            break
    if len(annotations) < TARGET_COUNT:
        raise SystemExit(f"Only selected {len(annotations)} real validation annotations: {counts}")
    return annotations


def split_for_index(index: int) -> str:
    if index <= 70:
        return "train"
    if index <= 85:
        return "val"
    return "test"


def main() -> int:
    annotation_path = ensure_annotations()
    coco = json.loads(annotation_path.read_text(encoding="utf-8"))
    selected = select_annotations(coco)
    rows: list[dict[str, str]] = []
    keep_constraints = "subject_identity_preserved;subject_pose_preserved;subject_color_material_preserved;subject_size_position_preserved"
    negative_constraints = "no_subject_change;no_subject_occlusion;no_style_transfer_on_subject;no_extra_main_subject"

    for index, ann in enumerate(selected, start=1):
        sample_id = f"sbg_real_{index:06d}"
        image_cache = CACHE_DIR / "val2017" / ann["file_name"]
        download(VAL_IMAGE_URL.format(file_name=ann["file_name"]), image_cache)
        source = Image.open(image_cache).convert("RGB")
        mask = polygon_mask(source.size, ann["segmentation"])
        if not mask.getbbox():
            continue
        edit_type = EDIT_TYPES[(index - 1) % len(EDIT_TYPES)]
        target = composite_target(source, mask, edit_type, index)
        source_rel = f"real_validation/source/{sample_id}.jpg"
        target_rel = f"real_validation/target/{sample_id}.png"
        mask_rel = f"real_validation/masks/{sample_id}.png"
        (ROOT / source_rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / target_rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / mask_rel).parent.mkdir(parents=True, exist_ok=True)
        source.save(ROOT / source_rel, quality=95)
        target.save(ROOT / target_rel)
        mask.save(ROOT / mask_rel)
        target_background = f"scripted {edit_type} validation background"
        instruction = (
            f"保持主体COCO {ann['category_name']}的身份、轮廓、姿态、颜色、材质、大小和画面位置不变，"
            f"仅将背景改为{target_background}。不要改变主体，不要新增遮挡主体的物体，不要改变主体风格。"
        )
        rows.append(
            {
                "sample_id": sample_id,
                "source_image": source_rel,
                "target_image": target_rel,
                "instruction": instruction,
                "edit_type": edit_type,
                "subject_category": ann["subject_category"],
                "subject_description": f"COCO {ann['category_name']}",
                "original_background": "real COCO scene",
                "target_background": target_background,
                "keep_constraints": keep_constraints,
                "negative_constraints": negative_constraints,
                "source_generator": "coco_val2017",
                "edit_generator": "scripted_background_composite_v1",
                "subject_bbox": bbox_string(ann["bbox"]),
                "subject_mask_path": mask_rel,
                "qc_status": "accepted",
                "reject_reason": "",
                "split": split_for_index(index),
                "external_dataset": "COCO val2017",
                "external_image_id": str(ann["image_id"]),
                "external_category_id": str(ann["category_id"]),
                "external_category_name": ann["category_name"],
            }
        )
        if len(rows) >= TARGET_COUNT:
            break

    if len(rows) != TARGET_COUNT:
        raise SystemExit(f"Expected {TARGET_COUNT} real validation rows, wrote {len(rows)}")
    write_csv(METADATA_DIR / "real_validation.csv", REAL_COLUMNS, rows)
    write_jsonl(METADATA_DIR / "real_validation.jsonl", rows)
    print(f"Real validation rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
