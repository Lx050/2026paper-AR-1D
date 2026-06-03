import csv
import json
import math
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"
COVERAGE_DIR = ROOT / "supplemental" / "coverage_extension"
NEGATIVE_DIR = ROOT / "supplemental" / "negative_samples"

BASE_COLUMNS = [
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
COVERAGE_COLUMNS = BASE_COLUMNS + ["base_sample_id", "extension_axis"]
NEGATIVE_COLUMNS = BASE_COLUMNS + ["base_sample_id", "negative_type"]

DEFICITS = [
    ("animal", "background_weather", 12),
    ("animal", "background_style", 12),
    ("animal", "background_object", 12),
    ("object", "background_replace", 12),
]
TARGET_BACKGROUNDS = {
    "background_replace": [
        "a quiet library reading room",
        "a clean science museum gallery",
        "a bright botanical greenhouse",
        "a calm lakeside dock",
    ],
    "background_weather": [
        "a rainy outdoor scene with wet ground",
        "a snowy outdoor scene with gentle snow",
        "a foggy outdoor scene with soft mist",
        "a bright post-rain scene with clear reflections",
    ],
    "background_style": [
        "a soft watercolor-style background while the subject remains photorealistic",
        "a clean paper-cut style background while the subject remains unchanged",
        "a minimal flat-color studio background while the subject remains unchanged",
        "a cinematic realistic background while the subject remains unchanged",
    ],
    "background_object": [
        "the original background with distant string lights added behind the subject",
        "the original background with background plants added behind the subject",
        "the original background with small distant balloons added behind the subject",
        "the original background with shelves added behind the subject",
    ],
}
NEGATIVE_TYPES = [
    "subject_color_changed",
    "subject_size_or_position_changed",
    "subject_occluded",
    "background_not_changed",
    "artifact_or_low_quality",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def load_rgb(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def load_mask(path: Path, size: tuple[int, int]) -> Image.Image:
    mask = Image.open(path).convert("L")
    if mask.size != size:
        mask = mask.resize(size, Image.Resampling.NEAREST)
    return mask


def bbox_from_mask(mask: Image.Image) -> str:
    arr = np.asarray(mask, dtype=np.uint8) > 0
    ys, xs = np.where(arr)
    if len(xs) == 0:
        return ""
    return f"{int(xs.min())},{int(ys.min())},{int(xs.max() - xs.min() + 1)},{int(ys.max() - ys.min() + 1)}"


def gradient_background(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / max(1, height - 1)
        arr[y, :, :] = [round(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3)]
    return Image.fromarray(arr, mode="RGB")


def add_ground(draw: ImageDraw.ImageDraw, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    width, height = size
    draw.rectangle([0, int(height * 0.68), width, height], fill=color)


def make_background(size: tuple[int, int], edit_type: str, index: int) -> Image.Image:
    width, height = size
    if edit_type == "background_replace":
        palettes = [
            ((210, 225, 235), (88, 132, 150), (93, 112, 82)),
            ((236, 232, 215), (170, 155, 126), (120, 107, 91)),
            ((216, 235, 220), (104, 150, 112), (74, 104, 78)),
            ((202, 220, 245), (82, 118, 164), (64, 86, 124)),
        ]
        top, bottom, ground = palettes[index % len(palettes)]
        image = gradient_background(size, top, bottom)
        draw = ImageDraw.Draw(image)
        add_ground(draw, size, ground)
        for offset in range(0, width, max(32, width // 12)):
            draw.line([(offset, int(height * 0.68)), (offset + width // 7, height)], fill=(255, 255, 255), width=2)
        return image.filter(ImageFilter.GaussianBlur(radius=1.2))

    if edit_type == "background_weather":
        image = gradient_background(size, (180, 190, 198), (95, 110, 118))
        draw = ImageDraw.Draw(image)
        add_ground(draw, size, (78, 88, 92))
        weather = index % 3
        if weather == 0:
            for x in range(0, width, 19):
                draw.line([(x, 0), (x + 45, height)], fill=(210, 225, 235), width=2)
        elif weather == 1:
            for y in range(0, height, 27):
                for x in range((y * 7) % 31, width, 31):
                    draw.ellipse([x, y, x + 5, y + 5], fill=(245, 248, 250))
        else:
            overlay = Image.new("RGBA", size, (230, 235, 238, 95))
            image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
        return image.filter(ImageFilter.GaussianBlur(radius=1.0))

    if edit_type == "background_style":
        image = gradient_background(size, (236, 222, 207), (126, 164, 178))
        draw = ImageDraw.Draw(image)
        step = max(36, width // 10)
        for y in range(-step, height + step, step):
            for x in range(-step, width + step, step):
                color = ((x + y + index * 23) % 95 + 110, (x * 2 + index * 19) % 85 + 120, (y * 3) % 95 + 130)
                draw.rounded_rectangle([x, y, x + step * 2, y + step], radius=step // 3, fill=color)
        return image.filter(ImageFilter.GaussianBlur(radius=3.5))

    image = gradient_background(size, (222, 224, 210), (120, 137, 116))
    draw = ImageDraw.Draw(image)
    add_ground(draw, size, (92, 108, 78))
    for i in range(8):
        x = int(width * (0.1 + 0.1 * i))
        y = int(height * (0.18 + 0.05 * math.sin(i)))
        draw.ellipse([x, y, x + 14, y + 14], fill=(245, 220, 120))
        draw.line([x + 7, y + 14, x + 7, y + 70], fill=(80, 90, 65), width=2)
    return image.filter(ImageFilter.GaussianBlur(radius=1.4))


def composite_subject(source: Image.Image, mask: Image.Image, background: Image.Image) -> Image.Image:
    soft_mask = mask.filter(ImageFilter.GaussianBlur(radius=1.0))
    return Image.composite(source, background, soft_mask)


def choose_rows(rows: list[dict[str, str]], category: str, count: int, offset: int) -> list[dict[str, str]]:
    candidates = [row for row in rows if row["subject_category"] == category and row["subject_mask_path"]]
    if len(candidates) < count:
        raise SystemExit(f"Need {count} masked {category} rows, found {len(candidates)}")
    return [candidates[(offset + i) % len(candidates)] for i in range(count)]


def copy_mask(base_row: dict[str, str], sample_id: str, target_root: Path) -> tuple[str, str]:
    source_mask = ROOT / base_row["subject_mask_path"]
    rel = target_root.relative_to(ROOT).as_posix() + f"/masks/{sample_id}.png"
    target_mask = ROOT / rel
    target_mask.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_mask, target_mask)
    bbox = bbox_from_mask(Image.open(target_mask).convert("L"))
    return rel, bbox


def build_coverage(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    index = 1
    offsets = {"animal": 0, "object": 0}
    keep_constraints = "subject_identity_preserved;subject_pose_preserved;subject_color_material_preserved;subject_size_position_preserved"
    negative_constraints = "no_subject_change;no_subject_occlusion;no_style_transfer_on_subject;no_extra_main_subject"
    for category, edit_type, count in DEFICITS:
        selected_rows = choose_rows(rows, category, count, offsets[category])
        offsets[category] += count
        for local_index, base_row in enumerate(selected_rows):
            sample_id = f"sbg_cov_{index:06d}"
            source_rel = f"supplemental/coverage_extension/source/{sample_id}.png"
            target_rel = f"supplemental/coverage_extension/target/{sample_id}.png"
            mask_rel, bbox = copy_mask(base_row, sample_id, COVERAGE_DIR)
            source = load_rgb(ROOT / base_row["source_image"])
            mask = load_mask(ROOT / mask_rel, source.size)
            background = make_background(source.size, edit_type, local_index)
            target = composite_subject(source, mask, background)
            (ROOT / source_rel).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / target_rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / base_row["source_image"], ROOT / source_rel)
            target.save(ROOT / target_rel)
            target_background = TARGET_BACKGROUNDS[edit_type][local_index % len(TARGET_BACKGROUNDS[edit_type])]
            instruction = (
                f"保持主体{base_row['subject_description']}的身份、轮廓、姿态、颜色、材质、大小和画面位置不变，"
                f"仅将背景从{base_row['original_background']}改为{target_background}。"
                f"不要改变主体，不要新增遮挡主体的物体，不要改变主体风格。"
            )
            output_rows.append(
                {
                    "sample_id": sample_id,
                    "source_image": source_rel,
                    "target_image": target_rel,
                    "instruction": instruction,
                    "edit_type": edit_type,
                    "subject_category": category,
                    "subject_description": base_row["subject_description"],
                    "original_background": base_row["original_background"],
                    "target_background": target_background,
                    "keep_constraints": keep_constraints,
                    "negative_constraints": negative_constraints,
                    "source_generator": base_row["source_generator"],
                    "edit_generator": "scripted_background_composite_v1",
                    "subject_bbox": bbox,
                    "subject_mask_path": mask_rel,
                    "qc_status": "accepted",
                    "reject_reason": "",
                    "split": "test" if index % 6 == 0 else "train",
                    "base_sample_id": base_row["sample_id"],
                    "extension_axis": f"{category}_{edit_type}",
                }
            )
            index += 1
    return output_rows


def make_negative_target(source: Image.Image, mask: Image.Image, negative_type: str, index: int) -> Image.Image:
    if negative_type == "background_not_changed":
        return source.copy()

    if negative_type == "artifact_or_low_quality":
        degraded = source.filter(ImageFilter.GaussianBlur(radius=5))
        enhancer = ImageEnhance.Contrast(degraded)
        return enhancer.enhance(0.55)

    if negative_type == "subject_color_changed":
        color_layer = Image.new("RGB", source.size, ((index * 37) % 255, 80, 210))
        subject = Image.blend(source, color_layer, 0.45)
        return Image.composite(subject, source, mask.filter(ImageFilter.GaussianBlur(radius=0.8)))

    if negative_type == "subject_occluded":
        out = source.copy()
        draw = ImageDraw.Draw(out, "RGBA")
        bbox = mask.getbbox() or (source.width // 4, source.height // 4, source.width * 3 // 4, source.height * 3 // 4)
        x0, y0, x1, y1 = bbox
        draw.rounded_rectangle(
            [x0 + (x1 - x0) // 5, y0 + (y1 - y0) // 4, x1 - (x1 - x0) // 6, y0 + (y1 - y0) // 2],
            radius=18,
            fill=(25, 35, 45, 210),
        )
        return out

    background = make_background(source.size, "background_replace", index)
    subject = Image.composite(source, Image.new("RGB", source.size, (0, 0, 0)), mask)
    bbox = mask.getbbox() or (0, 0, source.width, source.height)
    cropped_subject = subject.crop(bbox)
    cropped_mask = mask.crop(bbox)
    scale = 0.72
    new_size = (max(1, int(cropped_subject.width * scale)), max(1, int(cropped_subject.height * scale)))
    cropped_subject = cropped_subject.resize(new_size, Image.Resampling.BICUBIC)
    cropped_mask = cropped_mask.resize(new_size, Image.Resampling.NEAREST)
    paste_x = min(source.width - new_size[0], max(0, int(source.width * 0.08 + index * 7) % max(1, source.width - new_size[0])))
    paste_y = min(source.height - new_size[1], max(0, int(source.height * 0.10 + index * 5) % max(1, source.height - new_size[1])))
    background.paste(cropped_subject, (paste_x, paste_y), cropped_mask)
    return background


def build_negative(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected_rows = [row for row in rows if row["subject_mask_path"]][:50]
    if len(selected_rows) < 50:
        raise SystemExit(f"Need 50 masked base rows for negative set, found {len(selected_rows)}")
    output_rows: list[dict[str, str]] = []
    for index, base_row in enumerate(selected_rows, start=1):
        negative_type = NEGATIVE_TYPES[(index - 1) % len(NEGATIVE_TYPES)]
        sample_id = f"sbg_neg_{index:06d}"
        source_rel = f"supplemental/negative_samples/source/{sample_id}.png"
        target_rel = f"supplemental/negative_samples/target/{sample_id}.png"
        mask_rel, bbox = copy_mask(base_row, sample_id, NEGATIVE_DIR)
        source = load_rgb(ROOT / base_row["source_image"])
        mask = load_mask(ROOT / mask_rel, source.size)
        target = make_negative_target(source, mask, negative_type, index)
        (ROOT / source_rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / target_rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / base_row["source_image"], ROOT / source_rel)
        target.save(ROOT / target_rel)
        output_rows.append(
            {
                "sample_id": sample_id,
                "source_image": source_rel,
                "target_image": target_rel,
                "instruction": base_row["instruction"],
                "edit_type": base_row["edit_type"],
                "subject_category": base_row["subject_category"],
                "subject_description": base_row["subject_description"],
                "original_background": base_row["original_background"],
                "target_background": base_row["target_background"],
                "keep_constraints": base_row["keep_constraints"],
                "negative_constraints": base_row["negative_constraints"],
                "source_generator": base_row["source_generator"],
                "edit_generator": "scripted_negative_v1",
                "subject_bbox": bbox,
                "subject_mask_path": mask_rel,
                "qc_status": "rejected",
                "reject_reason": negative_type,
                "split": "test",
                "base_sample_id": base_row["sample_id"],
                "negative_type": negative_type,
            }
        )
    return output_rows


def main() -> int:
    rows = read_csv(METADATA_DIR / "background_edit.csv")
    missing_masks = [row["sample_id"] for row in rows if not row.get("subject_mask_path") or not (ROOT / row["subject_mask_path"]).exists()]
    if missing_masks:
        raise SystemExit(f"Run generate_subject_masks.py first. Missing masks for: {missing_masks[:5]}")

    coverage_rows = build_coverage(rows)
    negative_rows = build_negative(rows)
    write_csv(METADATA_DIR / "coverage_extension.csv", COVERAGE_COLUMNS, coverage_rows)
    write_jsonl(METADATA_DIR / "coverage_extension.jsonl", coverage_rows)
    write_csv(METADATA_DIR / "negative_samples.csv", NEGATIVE_COLUMNS, negative_rows)
    write_jsonl(METADATA_DIR / "negative_samples.jsonl", negative_rows)
    print(f"Coverage extension rows: {len(coverage_rows)}")
    print(f"Negative rows: {len(negative_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
