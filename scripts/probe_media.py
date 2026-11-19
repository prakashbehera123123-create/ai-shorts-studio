"""Print a compact ffprobe summary for one media file (no media is loaded into memory)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.errors import MediaToolError  # noqa: E402
from studio.media import run_ffprobe, summarize  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Usage: python scripts/probe_media.py path-to-media", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        print(json.dumps(summarize(run_ffprobe(path), str(path)), indent=2))
    except MediaToolError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
