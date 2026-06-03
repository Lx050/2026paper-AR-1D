import argparse
from pathlib import Path


BYTES_PER_MB = 1024 * 1024
DEFAULT_KEEP_LATEST = 4
DEFAULT_TARGET_MB = 10.0
DEFAULT_MAX_MB = 30.0
DEFAULT_SESSION_MAX_MB = 50.0


def default_generated_root() -> Path:
    return Path.home() / ".codex" / "generated_images"


def resolve_thread_dir(generated_root: Path, thread_dir: str | None) -> Path:
    if thread_dir:
        return Path(thread_dir).expanduser().resolve()

    candidates = [path for path in generated_root.iterdir() if path.is_dir()]
    if not candidates:
        raise SystemExit(f"No generated image thread directories found in {generated_root}")
    return max(candidates, key=lambda path: path.stat().st_mtime).resolve()


def require_safe_target(generated_root: Path, thread_dir: Path) -> None:
    generated_root = generated_root.resolve()
    thread_dir = thread_dir.resolve()
    if generated_root not in thread_dir.parents:
        raise SystemExit(f"Refusing to clean outside Codex generated_images: {thread_dir}")
    if not thread_dir.exists() or not thread_dir.is_dir():
        raise SystemExit(f"Generated image thread directory does not exist: {thread_dir}")


def session_jsonl_status(session_jsonl: Path, session_max_mb: float, required_headroom_mb: float) -> bool:
    if not session_jsonl.exists() or not session_jsonl.is_file():
        raise SystemExit(f"Session JSONL does not exist: {session_jsonl}")
    if session_max_mb <= 0:
        raise SystemExit("--session-max-mb must be > 0")
    if required_headroom_mb < 0:
        raise SystemExit("--require-session-headroom-mb must be >= 0")

    session_bytes = session_jsonl.stat().st_size
    session_max_bytes = int(session_max_mb * BYTES_PER_MB)
    required_headroom_bytes = int(required_headroom_mb * BYTES_PER_MB)
    remaining_bytes = session_max_bytes - session_bytes
    has_required_headroom = remaining_bytes >= required_headroom_bytes

    print(f"Session JSONL: {session_jsonl}")
    print(f"Session JSONL MB: {session_bytes / BYTES_PER_MB:.2f}")
    print(f"Session JSONL max MB: {session_max_mb:.2f}")
    print(f"Session JSONL remaining MB: {remaining_bytes / BYTES_PER_MB:.2f}")
    print(f"Required session headroom MB: {required_headroom_mb:.2f}")
    print(f"Session JSONL under max: {'yes' if session_bytes <= session_max_bytes else 'no'}")
    print(f"Session JSONL has required headroom: {'yes' if has_required_headroom else 'no'}")
    return session_bytes <= session_max_bytes and has_required_headroom


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean Codex default generated image cache after dataset images are copied into the repo."
    )
    parser.add_argument("--generated-root", default=str(default_generated_root()))
    parser.add_argument("--thread-dir", default=None)
    parser.add_argument("--keep-latest", type=int, default=DEFAULT_KEEP_LATEST)
    parser.add_argument("--target-mb", type=float, default=DEFAULT_TARGET_MB)
    parser.add_argument("--max-mb", type=float, default=DEFAULT_MAX_MB)
    parser.add_argument("--session-jsonl", default=None, help="Optional Codex session JSONL to guard at 50MB.")
    parser.add_argument("--session-max-mb", type=float, default=DEFAULT_SESSION_MAX_MB)
    parser.add_argument(
        "--require-session-headroom-mb",
        type=float,
        default=0.0,
        help="Fail if the session JSONL has less than this much remaining space.",
    )
    parser.add_argument("--apply", action="store_true", help="Delete files. Without this flag, only print a dry run.")
    args = parser.parse_args()

    generated_root = Path(args.generated_root).expanduser().resolve()
    thread_dir = resolve_thread_dir(generated_root, args.thread_dir)
    require_safe_target(generated_root, thread_dir)
    if args.keep_latest < 0:
        raise SystemExit("--keep-latest must be >= 0")
    if args.target_mb < 0:
        raise SystemExit("--target-mb must be >= 0")
    if args.max_mb < args.target_mb:
        raise SystemExit("--max-mb must be >= --target-mb")

    files = sorted((path for path in thread_dir.iterdir() if path.is_file()), key=lambda path: path.stat().st_mtime)
    total_bytes = sum(path.stat().st_size for path in files)
    target_bytes = int(args.target_mb * BYTES_PER_MB)
    max_bytes = int(args.max_mb * BYTES_PER_MB)

    delete_candidates = files[: max(0, len(files) - args.keep_latest)]
    delete_set = set(delete_candidates)
    remaining_bytes = total_bytes - sum(path.stat().st_size for path in delete_candidates)
    for path in files:
        if remaining_bytes <= target_bytes:
            break
        if path in delete_set:
            continue
        delete_candidates.append(path)
        delete_set.add(path)
        remaining_bytes -= path.stat().st_size

    delete_bytes = sum(path.stat().st_size for path in delete_candidates)
    final_bytes = total_bytes - delete_bytes

    mode = "APPLY" if args.apply else "DRY_RUN"
    print(f"Mode: {mode}")
    print(f"Thread dir: {thread_dir}")
    print(f"Total files: {len(files)}")
    print(f"Total MB: {total_bytes / BYTES_PER_MB:.2f}")
    print(f"Keep latest: {args.keep_latest}")
    print(f"Target MB after cleanup: {args.target_mb:.2f}")
    print(f"Max allowed MB before cleanup: {args.max_mb:.2f}")
    print(f"Over max before cleanup: {'yes' if total_bytes > max_bytes else 'no'}")
    print(f"Delete candidates: {len(delete_candidates)}")
    print(f"Reclaim MB: {delete_bytes / BYTES_PER_MB:.2f}")
    print(f"Final MB after cleanup: {final_bytes / BYTES_PER_MB:.2f}")

    session_ok = True
    if args.session_jsonl:
        session_ok = session_jsonl_status(
            Path(args.session_jsonl).expanduser().resolve(),
            args.session_max_mb,
            args.require_session_headroom_mb,
        )

    if args.apply:
        for path in delete_candidates:
            path.unlink()
        print("Cleanup complete")
    else:
        for path in delete_candidates[:20]:
            print(f"Would delete: {path.name}")
        if len(delete_candidates) > 20:
            print(f"... and {len(delete_candidates) - 20} more")
    return 0 if session_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
