"""Validate a rendered Short against config/production.json. Exit 1 on any error."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.config import load_config  # noqa: E402
from studio.errors import StudioError  # noqa: E402
from studio.media import check_summary, run_ffprobe, summarize  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Usage: python scripts/validate_video.py path-to-video.mp4", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        cfg = load_config()
        report = summarize(run_ffprobe(path), str(path))
    except StudioError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_summary(report, cfg)
    print(json.dumps({"report": report, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
