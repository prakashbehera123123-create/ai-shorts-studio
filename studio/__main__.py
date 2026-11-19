"""Command line: python -m studio {new,validate,status} ...

There is intentionally no publish/upload command.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .config import load_config
from .errors import ContractError, StudioError
from .production import create_production, parse_day, set_status, validate_production


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m studio", description="AI Shorts Studio production contracts")
    sub = p.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="scaffold production/YYYY-MM-DD-slug")
    new.add_argument("slug")
    new.add_argument("--title", default="")
    new.add_argument("--language", required=True, help="English or Hinglish")
    new.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")

    val = sub.add_parser("validate", help="validate one or more production folders")
    val.add_argument("folders", nargs="+", type=Path)

    st = sub.add_parser("status", help="show or change a production's status")
    st.add_argument("folder", type=Path)
    st.add_argument("--set", dest="target", default=None)
    st.add_argument("--note", default="")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cfg = load_config()
        if args.command == "new":
            day = parse_day(args.date) if args.date else date.today()
            folder = create_production(cfg, day, args.slug, args.title, args.language)
            print(f"Created {folder}")
            return 0
        if args.command == "validate":
            failed = False
            for folder in args.folders:
                problems = validate_production(folder, cfg)
                print(json.dumps({"folder": str(folder), "valid": not problems, "problems": problems}, indent=2))
                failed = failed or bool(problems)
            return 1 if failed else 0
        if args.command == "status":
            if args.target is None:
                print((args.folder / "status.json").read_text(encoding="utf-8"))
            else:
                data = set_status(args.folder, cfg, args.target, args.note)
                print(f"{data['video_id']}: {data['status']}")
            return 0
    except ContractError as exc:
        for problem in exc.problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    except (StudioError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
