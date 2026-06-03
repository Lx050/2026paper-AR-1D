import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"

BASE_EDIT_COUNTS = {
    "background_replace": 40,
    "background_time": 20,
    "background_weather": 20,
    "background_style": 10,
    "background_object": 10,
}

EXTENSION_EDIT_COUNTS = {
    "background_replace": 8,
    "background_time": 4,
    "background_weather": 4,
    "background_style": 2,
    "background_object": 2,
}

EDIT_COUNTS = {
    edit_type: BASE_EDIT_COUNTS[edit_type] + EXTENSION_EDIT_COUNTS[edit_type]
    for edit_type in BASE_EDIT_COUNTS
}

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

TASK_FIELDNAMES = FIELDNAMES + [
    "source_prompt",
    "edit_prompt",
    "planned_raw_source_path",
    "planned_source_path",
    "planned_target_path",
    "production_status",
]

ANIMAL_SUBJECTS = [
    ("red fox", "a calm red fox with a white chest and black-tipped ears", "misty pine forest clearing"),
    ("tabby cat", "a sitting orange tabby cat with clear stripes and green eyes", "sunlit apartment windowsill"),
    ("golden retriever", "a golden retriever wearing a plain blue collar", "suburban backyard lawn"),
    ("panda plush-like bear", "a round panda bear with black eye patches and soft white fur", "bamboo grove"),
    ("penguin", "a small penguin standing upright with glossy black feathers", "icy shoreline"),
    ("rabbit", "a white rabbit with upright ears and a small gray nose", "spring meadow"),
    ("owl", "a brown owl with large amber eyes perched on a branch", "old woodland"),
    ("turtle", "a green turtle with a patterned shell on flat stone", "quiet pond edge"),
    ("squirrel", "a gray squirrel holding a small acorn", "city park bench"),
    ("red panda", "a red panda with a ringed tail standing on a log", "temperate forest"),
    ("koala", "a koala holding a eucalyptus branch", "eucalyptus woodland"),
    ("hedgehog", "a small hedgehog curled slightly with visible spines", "garden path"),
    ("frog", "a bright green frog sitting on a smooth rock", "rainforest stream"),
    ("duck", "a yellow duckling standing on dry ground", "farm courtyard"),
    ("chameleon", "a green chameleon gripping a branch with curled tail", "tropical greenhouse"),
    ("otter", "a river otter with wet brown fur sitting upright", "riverbank"),
    ("deer", "a young deer with small antlers standing still", "autumn forest"),
    ("seal", "a gray seal pup resting on sand", "rocky beach"),
    ("parrot", "a colorful parrot perched on a simple wooden stand", "sunny balcony"),
    ("llama", "a white llama with fluffy fur standing side-on", "mountain pasture"),
    ("hamster", "a tan hamster standing on its hind legs", "wooden tabletop"),
    ("butterfly", "a blue butterfly with symmetrical wings on a flower", "flower garden"),
    ("crab", "a red crab with raised claws on wet sand", "tidal flat"),
    ("goat", "a small brown goat with short horns", "rural field"),
    ("horse", "a chestnut horse standing calmly in profile", "open stable yard"),
]

OBJECT_SUBJECTS = [
    ("ceramic teapot", "a glossy white ceramic teapot with a curved spout", "wooden kitchen table"),
    ("red bicycle", "a red city bicycle with a black seat and front basket", "quiet street corner"),
    ("vintage camera", "a black vintage film camera with silver lens rings", "photography studio desk"),
    ("blue backpack", "a blue canvas backpack with brown straps", "school hallway"),
    ("wooden chair", "a simple wooden chair with a woven seat", "minimal dining room"),
    ("glass vase", "a transparent glass vase with a narrow neck", "bright living room shelf"),
    ("yellow rain boot", "a single yellow rain boot standing upright", "mudroom floor"),
    ("toy robot", "a small silver toy robot with round eyes", "child's play table"),
    ("green watering can", "a green metal watering can with a long spout", "garden shed"),
    ("white sneaker", "a clean white sneaker with flat laces", "concrete floor"),
    ("brass compass", "a brass compass with a glass top", "map-covered desk"),
    ("red umbrella", "a folded red umbrella with a black handle", "entryway wall"),
    ("ceramic bowl", "a blue ceramic bowl with white rim", "kitchen counter"),
    ("wooden guitar", "an acoustic wooden guitar with a dark sound hole", "music room"),
    ("table lamp", "a small table lamp with a beige shade", "bedside table"),
    ("skateboard", "a skateboard with a plain black deck", "urban pavement"),
    ("potted cactus", "a small potted cactus in a terracotta pot", "sunny windowsill"),
    ("glass bottle", "a clear glass bottle with a cork stopper", "rustic shelf"),
    ("silver kettle", "a silver metal kettle with a black handle", "stove top"),
    ("orange suitcase", "an orange hard-shell suitcase with black wheels", "airport waiting area"),
    ("blue mug", "a blue ceramic mug with a round handle", "office desk"),
    ("wooden toy train", "a wooden toy train with red wheels", "playroom floor"),
    ("black headphones", "black over-ear headphones with soft ear pads", "studio table"),
    ("white clock", "a round white analog clock with black numbers", "plain wall shelf"),
    ("green lantern", "a green camping lantern with a metal handle", "camp table"),
]

TARGET_BACKGROUNDS = {
    "background_replace": [
        "a quiet seaside boardwalk",
        "a snowy mountain village",
        "a clean modern museum hall",
        "a desert road at golden hour",
        "a peaceful lakeside campsite",
        "a bright greenhouse full of plants",
        "a cobblestone old town street",
        "a simple studio with pastel backdrop",
    ],
    "background_time": [
        "the same type of scene at night with soft street lights",
        "the same type of scene at sunrise with warm light",
        "the same type of scene at blue hour dusk",
        "the same type of scene under midday sunlight",
    ],
    "background_weather": [
        "a rainy version of the scene with wet ground",
        "a snowy version of the scene with gentle snow",
        "a foggy version of the scene with low mist",
        "a sunny version after rain with clear reflections",
    ],
    "background_style": [
        "a soft watercolor-style background while the subject remains photorealistic",
        "a clean paper-cut style background while the subject remains unchanged",
        "a minimal flat-color studio background while the subject remains unchanged",
        "a cinematic but realistic background while the subject remains unchanged",
    ],
    "background_object": [
        "the original background with small distant string lights added behind the subject",
        "the original background with distant plants added behind the subject",
        "the original background with small background balloons added far behind the subject",
        "the original background with background bookshelves added behind the subject",
    ],
}


def split_for_index(index: int) -> str:
    """Keep the original 100-row split stable, then extend to 120 rows."""
    if index <= 70:
        return "train"
    if index <= 85:
        return "val"
    if index <= 100:
        return "test"
    if index <= 114:
        return "train"
    if index <= 117:
        return "val"
    return "test"


def expanded_edit_types() -> list[str]:
    edit_types: list[str] = []
    for edit_type, count in BASE_EDIT_COUNTS.items():
        edit_types.extend([edit_type] * count)
    for edit_type, count in EXTENSION_EDIT_COUNTS.items():
        edit_types.extend([edit_type] * count)
    return edit_types


def subject_rows() -> list[tuple[str, str, str, str]]:
    animals = [("animal", *item) for item in (ANIMAL_SUBJECTS * 2)]
    objects = [("object", *item) for item in (OBJECT_SUBJECTS * 2)]
    extension_animals = [("animal", *item) for item in ANIMAL_SUBJECTS[:10]]
    extension_objects = [("object", *item) for item in OBJECT_SUBJECTS[:10]]
    return animals[:50] + objects[:50] + extension_animals + extension_objects


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    keep_constraints = "subject_identity_preserved;subject_pose_preserved;subject_color_material_preserved;subject_size_position_preserved"
    negative_constraints = "no_subject_change;no_subject_occlusion;no_style_transfer_on_subject;no_extra_main_subject"

    for index, (subject, edit_type) in enumerate(zip(subject_rows(), expanded_edit_types()), start=1):
        subject_category, subject_name, subject_description, original_background = subject
        sample_id = f"sbg_{index:06d}"
        target_backgrounds = TARGET_BACKGROUNDS[edit_type]
        target_background = target_backgrounds[(index - 1) % len(target_backgrounds)]
        source_path = f"selected_sources/{sample_id}.png"
        raw_source_path = f"raw_sources/{sample_id}.png"
        target_path = f"edited_targets/{sample_id}.png"
        source_prompt = (
            f"Create a clear square photorealistic dataset source image of one main subject: "
            f"{subject_description}. Place it in {original_background}. The subject must be fully visible, "
            f"centered, not cropped, not touching image borders, with a clean replaceable background. "
            f"No people, no text, no watermark, no extra main subject."
        )
        instruction = (
            f"保持主体{subject_description}的身份、轮廓、姿态、颜色、材质、大小和画面位置不变，"
            f"仅将背景从{original_background}改为{target_background}。"
            f"不要改变主体，不要新增遮挡主体的物体，不要改变主体风格。"
        )
        edit_prompt = (
            f"Use the provided source image. {instruction} Keep the image resolution and composition stable."
        )
        rows.append(
            {
                "sample_id": sample_id,
                "source_image": source_path,
                "target_image": target_path,
                "instruction": instruction,
                "edit_type": edit_type,
                "subject_category": subject_category,
                "subject_description": subject_description,
                "original_background": original_background,
                "target_background": target_background,
                "keep_constraints": keep_constraints,
                "negative_constraints": negative_constraints,
                "source_generator": "chatgpt_image2",
                "edit_generator": "chatgpt_image2_edit",
                "subject_bbox": "",
                "subject_mask_path": "",
                "qc_status": "planned",
                "reject_reason": "",
                "split": split_for_index(index),
                "source_prompt": source_prompt,
                "edit_prompt": edit_prompt,
                "planned_raw_source_path": raw_source_path,
                "planned_source_path": source_path,
                "planned_target_path": target_path,
                "production_status": "not_started",
            }
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def main() -> None:
    rows = build_rows()
    write_csv(METADATA_DIR / "task_plan.csv", TASK_FIELDNAMES, rows)
    write_csv(METADATA_DIR / "background_edit.csv", FIELDNAMES, [])
    write_csv(METADATA_DIR / "rejected.csv", FIELDNAMES, [])
    (METADATA_DIR / "background_edit.jsonl").write_text("", encoding="utf-8")
    (METADATA_DIR / "task_plan.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} planned tasks to {METADATA_DIR / 'task_plan.csv'}")


if __name__ == "__main__":
    main()
