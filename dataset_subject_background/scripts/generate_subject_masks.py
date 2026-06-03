import csv
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"
MASK_DIR = ROOT / "masks" / "subject"
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


def image_to_small_array(path: Path, max_side: int = 384) -> tuple[np.ndarray, tuple[int, int]]:
    image = Image.open(path).convert("RGB")
    width, height = image.size
    scale = min(1.0, max_side / max(width, height))
    if scale < 1.0:
        image = image.resize((max(1, round(width * scale)), max(1, round(height * scale))), Image.Resampling.BILINEAR)
    return np.asarray(image, dtype=np.int16), (width, height)


def shifted(mask: np.ndarray, dy: int, dx: int) -> np.ndarray:
    out = np.zeros_like(mask, dtype=bool)
    src_y0 = max(0, -dy)
    src_y1 = mask.shape[0] - max(0, dy)
    src_x0 = max(0, -dx)
    src_x1 = mask.shape[1] - max(0, dx)
    dst_y0 = max(0, dy)
    dst_y1 = mask.shape[0] - max(0, -dy)
    dst_x0 = max(0, dx)
    dst_x1 = mask.shape[1] - max(0, -dx)
    out[dst_y0:dst_y1, dst_x0:dst_x1] = mask[src_y0:src_y1, src_x0:src_x1]
    return out


def dilate(mask: np.ndarray, iterations: int = 1) -> np.ndarray:
    result = mask.astype(bool)
    for _ in range(iterations):
        expanded = np.zeros_like(result, dtype=bool)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                expanded |= shifted(result, dy, dx)
        result = expanded
    return result


def erode(mask: np.ndarray, iterations: int = 1) -> np.ndarray:
    result = mask.astype(bool)
    for _ in range(iterations):
        shrunk = np.ones_like(result, dtype=bool)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                shrunk &= shifted(result, dy, dx)
        result = shrunk
    return result


def close_mask(mask: np.ndarray, iterations: int = 2) -> np.ndarray:
    return erode(dilate(mask, iterations), iterations)


def open_mask(mask: np.ndarray, iterations: int = 1) -> np.ndarray:
    return dilate(erode(mask, iterations), iterations)


def connected_components(mask: np.ndarray) -> list[list[tuple[int, int]]]:
    visited = np.zeros_like(mask, dtype=bool)
    components: list[list[tuple[int, int]]] = []
    height, width = mask.shape
    for start_y in range(height):
        for start_x in range(width):
            if visited[start_y, start_x] or not mask[start_y, start_x]:
                continue
            queue: deque[tuple[int, int]] = deque([(start_y, start_x)])
            visited[start_y, start_x] = True
            component: list[tuple[int, int]] = []
            while queue:
                y, x = queue.popleft()
                component.append((y, x))
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < height and 0 <= nx < width and not visited[ny, nx] and mask[ny, nx]:
                        visited[ny, nx] = True
                        queue.append((ny, nx))
            components.append(component)
    return components


def component_score(component: list[tuple[int, int]], shape: tuple[int, int]) -> float:
    height, width = shape
    coords = np.asarray(component)
    ys = coords[:, 0]
    xs = coords[:, 1]
    center_y = (ys.min() + ys.max()) / 2
    center_x = (xs.min() + xs.max()) / 2
    normalized_distance = abs(center_x - width / 2) / width + abs(center_y - height / 2) / height
    area_ratio = len(component) / (height * width)
    return area_ratio - normalized_distance * 0.08


def central_subject_roi(source_path: Path, subject_category: str) -> tuple[Image.Image, str]:
    image = Image.open(source_path)
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # The generated source images were prompted to keep one full, centered main
    # subject. A conservative ROI is safer than pair-difference segmentation
    # here, because similar source/target backgrounds can be mistakenly selected
    # as the stable component.
    if subject_category == "animal":
        x0, y0, x1, y1 = 0.16, 0.14, 0.88, 0.93
    else:
        x0, y0, x1, y1 = 0.18, 0.16, 0.84, 0.88
    box = [
        int(width * x0),
        int(height * y0),
        int(width * x1),
        int(height * y1),
    ]
    radius = max(16, min(width, height) // 18)
    draw.rounded_rectangle(box, radius=radius, fill=255)
    return mask, f"central_{subject_category}_roi"


def bbox_from_mask(mask: Image.Image) -> str:
    arr = np.asarray(mask, dtype=np.uint8) > 0
    ys, xs = np.where(arr)
    if len(xs) == 0 or len(ys) == 0:
        return ""
    x0 = int(xs.min())
    y0 = int(ys.min())
    x1 = int(xs.max())
    y1 = int(ys.max())
    return f"{x0},{y0},{x1 - x0 + 1},{y1 - y0 + 1}"


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    accepted_path = METADATA_DIR / "background_edit.csv"
    task_plan_path = METADATA_DIR / "task_plan.csv"
    _, accepted_rows = read_csv(accepted_path)
    task_fieldnames, task_rows = read_csv(task_plan_path)
    task_by_id = {row["sample_id"]: row for row in task_rows}

    MASK_DIR.mkdir(parents=True, exist_ok=True)
    method_counts: dict[str, int] = {}
    for row in accepted_rows:
        sample_id = row["sample_id"]
        source_path = ROOT / row["source_image"]
        mask, method = central_subject_roi(source_path, row["subject_category"])
        mask_rel = f"masks/subject/{sample_id}.png"
        mask.save(ROOT / mask_rel)
        bbox = bbox_from_mask(mask)
        row["subject_mask_path"] = mask_rel
        row["subject_bbox"] = bbox
        method_counts[method] = method_counts.get(method, 0) + 1
        if sample_id in task_by_id:
            task_by_id[sample_id]["subject_mask_path"] = mask_rel
            task_by_id[sample_id]["subject_bbox"] = bbox

    write_csv(accepted_path, FIELDNAMES, accepted_rows)
    write_jsonl(METADATA_DIR / "background_edit.jsonl", accepted_rows)
    write_csv(task_plan_path, task_fieldnames, task_rows)
    write_jsonl(METADATA_DIR / "task_plan.jsonl", task_rows)

    print(f"Generated masks: {len(accepted_rows)}")
    print(f"Method counts: {method_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
