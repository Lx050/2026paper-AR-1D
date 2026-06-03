import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


BYTES_PER_MB = 1024 * 1024
DATA_URL_PATTERN = re.compile(r"data:image/([a-zA-Z0-9.+-]+);base64,([A-Za-z0-9+/=]+)")
BASE64_PATTERN = re.compile(r"^[A-Za-z0-9+/=]+$")
IMAGE_BASE64_PREFIXES = {
    "iVBORw0KGgo": "png",
    "/9j/": "jpeg",
    "UklGR": "webp",
}
DEFAULT_MAX_MB = 50.0


def require_codex_session_path(path: Path) -> None:
    """Limit writes to Codex session JSONL files; this avoids accidental project-file rewrites."""
    resolved = path.expanduser().resolve()
    sessions_root = (Path.home() / ".codex" / "sessions").resolve()
    if sessions_root not in resolved.parents:
        raise SystemExit(f"Refusing to clean outside Codex sessions: {resolved}")
    if resolved.suffix != ".jsonl":
        raise SystemExit(f"Refusing to clean non-jsonl file: {resolved}")
    if not resolved.exists() or not resolved.is_file():
        raise SystemExit(f"Session JSONL does not exist: {resolved}")


def replacement_for(match: re.Match[str]) -> str:
    image_format = match.group(1)
    payload = match.group(2)
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()[:16]
    return f"codex-cleaned-image://{image_format}/{digest}?base64_chars={len(payload)}"


def scrub_string(value: str) -> tuple[str, int]:
    replacements = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal replacements
        replacements += 1
        return replacement_for(match)

    cleaned = DATA_URL_PATTERN.sub(replace, value)
    if replacements:
        return cleaned, replacements

    # Image generation events store a second copy as a bare base64 PNG/JPEG/WebP
    # string. The saved_path field and copied dataset images are the source of
    # truth, so this bulky inline result can be replaced safely.
    if len(value) > 100_000 and BASE64_PATTERN.fullmatch(value):
        for prefix, image_format in IMAGE_BASE64_PREFIXES.items():
            if value.startswith(prefix):
                digest = hashlib.sha256(value.encode("ascii")).hexdigest()[:16]
                return f"codex-cleaned-image://{image_format}/{digest}?base64_chars={len(value)}", 1

    return cleaned, 0


def scrub_value(value: Any) -> tuple[Any, int]:
    """Recursively preserve JSON structure while removing heavyweight image data URLs."""
    if isinstance(value, str):
        return scrub_string(value)
    if isinstance(value, list):
        total = 0
        cleaned_items = []
        for item in value:
            cleaned_item, count = scrub_value(item)
            cleaned_items.append(cleaned_item)
            total += count
        return cleaned_items, total
    if isinstance(value, dict):
        total = 0
        cleaned_obj = {}
        for key, item in value.items():
            cleaned_item, count = scrub_value(item)
            cleaned_obj[key] = cleaned_item
            total += count
        return cleaned_obj, total
    return value, 0


def clean_lines(path: Path) -> tuple[list[str], int, int]:
    cleaned_lines: list[str] = []
    replacements = 0
    invalid_lines = 0

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                cleaned_lines.append(line)
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                # Keep invalid lines byte-for-byte so the cleaner never hides corruption.
                invalid_lines += 1
                cleaned_lines.append(line)
                continue
            cleaned_obj, count = scrub_value(obj)
            replacements += count
            cleaned_lines.append(json.dumps(cleaned_obj, ensure_ascii=False, separators=(",", ":")) + "\n")

    return cleaned_lines, replacements, invalid_lines


def write_cleaned_file(path: Path, cleaned_lines: list[str]) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak-{timestamp}")
    temp_path = path.with_name(f"{path.name}.tmp-{timestamp}")

    shutil.copy2(path, backup_path)
    with temp_path.open("w", encoding="utf-8", newline="") as handle:
        handle.writelines(cleaned_lines)
    try:
        os.replace(temp_path, path)
    except PermissionError:
        # Codex keeps the active session file open on Windows. In that case the
        # atomic replace can be denied even though direct writing is allowed.
        # The backup above is already complete, so direct rewrite is the safest
        # practical fallback for the active thread JSONL.
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.writelines(cleaned_lines)
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
    return backup_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove embedded image base64 payloads from a Codex session JSONL.")
    parser.add_argument("session_jsonl")
    parser.add_argument("--max-mb", type=float, default=DEFAULT_MAX_MB)
    parser.add_argument("--apply", action="store_true", help="Rewrite the JSONL. Without this flag, only dry-run.")
    args = parser.parse_args()

    path = Path(args.session_jsonl).expanduser().resolve()
    require_codex_session_path(path)
    if args.max_mb <= 0:
        raise SystemExit("--max-mb must be > 0")

    before_bytes = path.stat().st_size
    cleaned_lines, replacements, invalid_lines = clean_lines(path)
    after_bytes = sum(len(line.encode("utf-8")) for line in cleaned_lines)
    max_bytes = int(args.max_mb * BYTES_PER_MB)

    print(f"Mode: {'APPLY' if args.apply else 'DRY_RUN'}")
    print(f"Session JSONL: {path}")
    print(f"Before MB: {before_bytes / BYTES_PER_MB:.2f}")
    print(f"Estimated after MB: {after_bytes / BYTES_PER_MB:.2f}")
    print(f"Max MB: {args.max_mb:.2f}")
    print(f"Embedded image payloads replaced: {replacements}")
    print(f"Invalid JSONL lines preserved: {invalid_lines}")
    print(f"Estimated under max: {'yes' if after_bytes <= max_bytes else 'no'}")

    if args.apply:
        backup_path = write_cleaned_file(path, cleaned_lines)
        final_bytes = path.stat().st_size
        print(f"Backup: {backup_path}")
        print(f"Final MB: {final_bytes / BYTES_PER_MB:.2f}")
        print(f"Final under max: {'yes' if final_bytes <= max_bytes else 'no'}")
        return 0 if final_bytes <= max_bytes else 2

    return 0 if after_bytes <= max_bytes else 2


if __name__ == "__main__":
    raise SystemExit(main())
