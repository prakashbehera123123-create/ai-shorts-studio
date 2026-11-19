"""Command line: python -m studio {new,validate,status} ...

There is intentionally no publish/upload command.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .config import ProductionConfig, load_config
from .errors import ContractError, StudioError
from .production import create_production, parse_day, set_status, validate_production
from .script import check_fact_check, check_script
from .research import load_research_config, load_research_file, select_topics, validate_research
from .shortlist import DEFAULT_BACKLOG, DEFAULT_RESEARCH_ROOT, apply_selection, prior_titles


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

    sc = sub.add_parser("script", help="check script.md, storyboard.json and fact_check.md")
    sc.add_argument("folders", nargs="+", type=Path)

    rs = sub.add_parser("research", help="validate, score and select researched topics")
    rsub = rs.add_subparsers(dest="research_command", required=True)
    init = rsub.add_parser("init", help="create research/YYYY-MM-DD/candidates.json skeleton")
    init.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    for name, help_text in (("check", "validate and dry-run selection (writes nothing)"),
                            ("apply", "create briefs/sources for selected topics and update backlog")):
        sp = rsub.add_parser(name, help=help_text)
        sp.add_argument("file", type=Path)
    return p


def _research(args: argparse.Namespace, cfg: ProductionConfig) -> int:
    rcfg = load_research_config()
    if args.research_command == "init":
        day = parse_day(args.date) if args.date else date.today()
        path = DEFAULT_RESEARCH_ROOT / day.isoformat() / "candidates.json"
        if path.exists():
            raise StudioError(f"Already exists: {path}")
        path.parent.mkdir(parents=True)
        skeleton = {"research_date": day.isoformat(), "window_days": rcfg.window_days, "candidates": []}
        path.write_text(json.dumps(skeleton, indent=2) + "\n", encoding="utf-8")
        print(f"Created {path}")
        return 0

    data = load_research_file(args.file)
    day = parse_day(str(data.get("research_date", "")))
    if day > date.today():
        raise StudioError(f"research_date {day} is in the future")
    errors, warnings = validate_research(data, rcfg, cfg.languages, day)
    if errors:
        raise ContractError(errors)
    decisions = select_topics(data, rcfg, day, prior_titles(DEFAULT_BACKLOG, cfg.production_root))
    if args.research_command == "check":
        print(json.dumps({
            "warnings": warnings,
            "ranking": [{"id": d.id, "score": d.score, "selected": d.selected, "reasons": d.reasons}
                        for d in sorted(decisions, key=lambda x: (-x.score, x.id))],
        }, indent=2))
        return 0
    summary = apply_selection(decisions, warnings, day, cfg, rcfg, args.file)
    print(json.dumps(summary, indent=2))
    return 0


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
        if args.command == "research":
            return _research(args, cfg)
        if args.command == "script":
            failed = False
            for folder in args.folders:
                rep = check_script(folder, cfg)
                fact = check_fact_check(folder, rep.claims) if rep.claims else []
                out = rep.as_dict() | {"folder": folder.name, "fact_check_problems": fact}
                out["ok"] = not rep.errors and not fact
                print(json.dumps(out, indent=2))
                failed = failed or not out["ok"]
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
