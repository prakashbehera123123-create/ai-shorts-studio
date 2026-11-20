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
from .status import load_status
from .production import create_production, parse_day, set_status, validate_production
from .compose import render_production
from .render_config import load_render_config
from .metadata import build_metadata, metadata_problems
from .qa import editorial_problems, run_technical_qa, write_qa_report
from .script import check_fact_check, check_script, parse_sections
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

    dl = sub.add_parser("deliver", help="copy a READY_FOR_HUMAN_REVIEW package to final/YYYY-MM-DD/<id>/ (never overwrites)")
    dl.add_argument("folders", nargs="+", type=Path)

    rn = sub.add_parser("render", help="render a draft MP4 locally (voiceover, captions, frames, FFmpeg)")
    rn.add_argument("folders", nargs="+", type=Path)
    rn.add_argument("--voice", choices=("auto", "sapi", "manual"), default="auto",
                    help="auto = voiceover/voiceover.wav if present, else the local SAPI placeholder")

    vc = sub.add_parser("voice", help="voice-clone utilities")
    vsub = vc.add_subparsers(dest="voice_command", required=True)
    prep = vsub.add_parser("prepare", help="clean a recording of the owner's own voice into the clone reference")
    prep.add_argument("source", type=Path, help="recording of the channel owner's own voice")
    prep.add_argument("--start", type=float, default=0.0)
    prep.add_argument("--seconds", type=float, default=13.8)
    prep.add_argument("--out", type=Path, default=Path("voice/reference_clean.wav"))

    ref = sub.add_parser("reference", help="analyse reference videos into compact evidence (git-ignored output)")
    ref.add_argument("videos", nargs="+", type=Path)
    ref.add_argument("--out", type=Path, default=Path("reference/_analysis"))
    ref.add_argument("--model", type=Path, default=Path("models/ggml-base.bin"), help="whisper.cpp model; skipped if missing")

    qa = sub.add_parser("qa", help="technical QA + assemble qa_report.md (reads qa/editorial.md if present)")
    qa.add_argument("folders", nargs="+", type=Path)

    md = sub.add_parser("metadata", help="write a draft metadata.md (title, description with sources, tags, disclosures)")
    md.add_argument("folders", nargs="+", type=Path)
    md.add_argument("--force", action="store_true", help="overwrite a metadata.md that already has a title")

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
        if args.command == "render":
            rcfg = load_render_config()
            failed = False
            for folder in args.folders:
                print(f"Rendering {folder.name} ...", flush=True)
                rep = render_production(folder, cfg, rcfg, args.voice)
                print(json.dumps({"folder": folder.name, "voice": rep.voice_source, "tts_rate": rep.tts_rate, "output": rep.output,
                                  "duration_seconds": rep.duration_seconds, "scenes": len(rep.scenes), "caption_cues": rep.cues,
                                  "probe": {k: rep.probe.get(k) for k in ("width", "height", "video_codec", "audio_codec")},
                                  "errors": rep.errors, "warnings": rep.warnings}, indent=2))
                failed = failed or bool(rep.errors)
            return 1 if failed else 0
        if args.command == "deliver":
            from .archive import deliver

            for folder in args.folders:
                if load_status(folder / "status.json")["status"] != "READY_FOR_HUMAN_REVIEW":
                    raise StudioError(f"{folder.name} is not READY_FOR_HUMAN_REVIEW")
                print(f"{folder.name} -> {deliver(folder, folder.resolve().parent.parent / 'final').as_posix()}")
            return 0
        if args.command == "voice":
            from .clone_voice import prepare_reference

            args.out.parent.mkdir(parents=True, exist_ok=True)
            result = prepare_reference(args.source, args.out, args.start, args.seconds, load_render_config())
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "reference":
            from .config import PROJECT_ROOT
            from .reference import analyze_video

            for video in args.videos:
                print(f"Analysing {video.name} ...", flush=True)
                s = analyze_video(video, args.out, PROJECT_ROOT, args.model if args.model.is_file() else None)
                print(f"  {s['duration_s']}s {s['width']}x{s['height']} · shots {s['shots']['shots']} "
                      f"(mean {s['shots']['mean_shot_s']}s, {s['shots']['cuts_first_10s']} cuts in first 10s) · "
                      f"{s['loudness_lufs']} LUFS · wpm {s.get('words_per_minute')} · first speech {s.get('first_speech_at_s')}s")
            return 0
        if args.command == "qa":
            failed = False
            for folder in args.folders:
                tech = run_technical_qa(folder, cfg)
                overall = write_qa_report(folder)
                print(f"\n{folder.name}: technical {'PASS' if tech.passed else 'FAIL'} · overall {overall}")
                for c in tech.checks:
                    mark = "ok  " if c.passed else ("WARN" if c.severity == "warning" else "FAIL")
                    print(f"  [{mark}] {c.name}: {c.detail}")
                for p in editorial_problems(folder):
                    print(f"  [TODO] {p}")
                failed = failed or overall != "PASS"
            return 1 if failed else 0
        if args.command == "metadata":
            for folder in args.folders:
                path = folder / "metadata.md"
                if path.is_file() and parse_sections(path.read_text(encoding="utf-8")).get("title") and not args.force:
                    raise StudioError(f"{path} already has a title; use --force to overwrite")
                path.write_text(build_metadata(folder), encoding="utf-8")
                problems = metadata_problems(folder)
                print(json.dumps({"folder": folder.name, "metadata": "metadata.md", "problems": problems}, indent=2))
            return 0
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
                print(f"{data['video_id']}: {data['status']}" + (f" (review package: {data['delivery']})" if data.get("delivery") else ""))
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
