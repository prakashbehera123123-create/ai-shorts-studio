"""Build the motion-engine spec (studio/motion/engine.html) from a schema-v2 storyboard and real word timings,
and run the deterministic frame renderer (scripts/render_motion.cjs)."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .compose_types import SceneTiming
from .errors import MediaToolError
from .tts import WordTime

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RENDERER = PROJECT_ROOT / "scripts" / "render_motion.cjs"
RENDER_TIMEOUT_SECONDS = 1800
from .storyboard import VISUAL_TEMPLATES as TEMPLATES  # single source of truth
FORM_DEFAULT_TEMPLATE = {"kinetic_type": "kinetic", "title_card": "title", "chart": "chart", "split_screen": "split",
                         "ui_mock": "panel", "architecture_flow": "flow", "diagram_2d": "flow", "scene_3d": "scene3d"}
QUESTION_BEATS = frozenset({"context", "tension", "explanation", "example", "reveal"})
WEAK_END = frozenset("a an the to of and or but your you my our in on at for with how so if is are it that this".split())
MAX_CAPTION_WORDS = 4
MAX_CAPTION_CHARS = 24
CAPTION_HOLD = 0.6
MIN_CHUNK_SECONDS = 0.8
MAX_MERGED_WORDS = 5
MAX_MERGED_CHARS = 30


def _norm(w: str) -> str:
    return re.sub(r"[^a-z0-9.]", "", w.lower()).strip(".")


def merge_flashes(chunks: list[list[WordTime]]) -> list[list[WordTime]]:
    """Merge chunks spoken in under MIN_CHUNK_SECONDS into a neighbour (next first, else previous) when the result
    stays <= MAX_MERGED_WORDS words / MAX_MERGED_CHARS chars, so captions do not flash."""
    def dur(c: list[WordTime]) -> float:
        return c[-1].end - c[0].start

    def fits(c: list[WordTime]) -> bool:
        return len(c) <= MAX_MERGED_WORDS and len(" ".join(w.text for w in c)) <= MAX_MERGED_CHARS

    out = [list(c) for c in chunks]
    i = 0
    while i < len(out):
        if dur(out[i]) < MIN_CHUNK_SECONDS and len(out) > 1:
            if i + 1 < len(out) and fits(out[i] + out[i + 1]):
                out[i:i + 2] = [out[i] + out[i + 1]]
                continue
            if i > 0 and fits(out[i - 1] + out[i]):
                out[i - 1:i + 1] = [out[i - 1] + out[i]]
                i -= 1
                continue
        i += 1
    return out


def caption_chunks(scene_words: list[list[WordTime]], scene_ends: list[float]) -> list[dict[str, Any]]:
    """Phrase-aware karaoke chunks: <= 4 words / 24 chars, break after punctuation, never end on a weak word,
    never span a scene boundary. Each chunk stays up until the next starts (max CAPTION_HOLD after its last word)."""
    chunks: list[list[WordTime]] = []
    for words in scene_words:
        scene_chunks: list[list[WordTime]] = []
        cur: list[WordTime] = []
        for w in words:
            if cur and (len(cur) >= MAX_CAPTION_WORDS or len(" ".join(x.text for x in [*cur, w])) > MAX_CAPTION_CHARS):
                carry = []
                while len(cur) > 1 and _norm(cur[-1].text) in WEAK_END and not re.search(r"[.,?!;:]$", cur[-1].text):
                    carry.insert(0, cur.pop())
                scene_chunks.append(cur)
                cur = carry
            cur.append(w)
            if re.search(r"[.,?!;:]$", w.text):
                scene_chunks.append(cur)
                cur = []
        if cur:
            scene_chunks.append(cur)
        chunks.extend(merge_flashes(scene_chunks))
    out = []
    ends_by_word = {id(w): e for words, e in zip(scene_words, scene_ends) for w in words}
    for i, c in enumerate(chunks):
        nxt = chunks[i + 1][0].start if i + 1 < len(chunks) else c[-1].end + CAPTION_HOLD
        end = min(nxt, c[-1].end + CAPTION_HOLD, ends_by_word[id(c[-1])])
        out.append({"start": round(c[0].start, 3), "end": round(max(end, c[-1].end), 3),
                    "words": [{"text": w.text, "start": round(w.start, 3), "end": round(w.end, 3)} for w in c]})
    return out


def resolve_cues(cue_words: list[str], words: list[WordTime], scene_start: float) -> list[float | None]:
    """Each cue word -> seconds from scene start of its first occurrence after the previous cue (None if absent)."""
    out: list[float | None] = []
    pos = 0
    for cue in cue_words:
        target = _norm(cue)
        hit = next((i for i in range(pos, len(words)) if _norm(words[i].text).startswith(target)), None)
        if hit is None:
            out.append(None)
            continue
        out.append(round(max(0.0, words[hit].start - scene_start - 0.05), 3))
        pos = hit + 1
    return out


def step_labels(scenes: list[dict[str, Any]]) -> list[str]:
    nums = [int(m.group(1)) if (m := re.match(r"^\s*(\d)\s*[.:)]", str(s.get("on_screen_text", "")))) else None for s in scenes]
    total = max((n for n in nums if n), default=0)
    return [f"{n}/{total}" if n and total > 1 else "" for n in nums]


def source_chips(sources_md: str) -> dict[str, str]:
    chips = {}
    for line in sources_md.splitlines():
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) >= 5 and re.fullmatch(r"S\d+", cells[0]):
            pub = re.sub(r"\s*\(.*?\)", "", cells[2]).strip()
            date = cells[3] if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[3]) else ""
            chips[cells[0]] = f"Source: {pub}" + (f" · {date}" if date else "")
    return chips


ICON_DIR = Path(__file__).resolve().parents[1] / "vendor" / "node_modules" / "lucide-static" / "icons"


def icon_svg(name: str) -> str:
    """Inline SVG for a Lucide icon (ISC licence, vendor/node_modules/lucide-static)."""
    if not re.fullmatch(r"[a-z0-9-]+", name or ""):
        raise MediaToolError(f"icon name '{name}' must be a Lucide id like 'radio-tower'")
    path = ICON_DIR / f"{name}.svg"
    if not path.is_file():
        raise MediaToolError(f"unknown Lucide icon '{name}' (browse https://lucide.dev/icons; installed in vendor/)")
    svg = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S).strip()
    return re.sub(r'\s(width|height)="24"', "", svg, count=2)


def _resolve_icons(v: dict[str, Any]) -> dict[str, Any]:
    """Replace icon names with inline SVG: v.icon, v.icons[], nodes[].icon, branches[].icon, left/right.icon."""
    if v.get("icon"):
        v["icon_svg"] = icon_svg(v["icon"])
    if v.get("icons"):
        v["icons_svg"] = [icon_svg(n) if n else "" for n in v["icons"]]
    for key in ("nodes", "branches"):
        if isinstance(v.get(key), list):
            v[key] = [dict(n, icon_svg=icon_svg(n["icon"])) if isinstance(n, dict) and n.get("icon") else n for n in v[key]]
    for key in ("left", "right"):
        if isinstance(v.get(key), dict) and v[key].get("icon"):
            v[key] = dict(v[key], icon_svg=icon_svg(v[key]["icon"]))
    return v


def visual_for(scene: dict[str, Any]) -> dict[str, Any]:
    v = dict(scene.get("visual") or {})
    if not v.get("template"):
        v["template"] = FORM_DEFAULT_TEMPLATE.get(scene.get("visual_form", ""), "kinetic")
    if v["template"] == "flow" and not v.get("nodes"):  # no structured content: degrade honestly to kinetic type
        v = {"template": "kinetic", "lines": [scene.get("on_screen_text", "")]}
    if v["template"] not in TEMPLATES:
        raise MediaToolError(f"scene {scene.get('id')}: unknown visual template '{v['template']}'")
    return _resolve_icons(v)


def build_spec(board: dict[str, Any], timings: list[SceneTiming], scene_words: list[list[WordTime]], sources_md: str,
               fps: int, crf: int, preset: str) -> dict[str, Any]:
    scenes = board["scenes"]
    chips = source_chips(sources_md)
    steps = step_labels(scenes)
    question = (board.get("creative") or {}).get("central_question", "")
    out_scenes = []
    for s, tm, words, step in zip(scenes, timings, scene_words, steps):
        v = visual_for(s)
        emphasis = [e for e in (s.get("voice") or {}).get("emphasis", []) if e]
        accent = next((e for e in emphasis if _norm(e) in {_norm(w) for w in str(s["on_screen_text"]).split()}), None)
        out_scenes.append({
            "id": s["id"], "start": tm.start, "end": tm.end, "speech": round(tm.speech, 3),
            "transition_in": s.get("transition_in", "cut"), "beat": s.get("beat", ""),
            "headline": s["on_screen_text"], "accent": accent, "step": step,
            "question": question if s.get("beat") in QUESTION_BEATS else "",
            "source": next((chips[x] for x in s.get("source_ids", []) if x in chips), ""),
            "visual": v, "cues": resolve_cues(v.get("cues", []), words, tm.start),
        })
    return {"fps": fps, "crf": crf, "preset": preset, "duration": timings[-1].end,
            "scenes": out_scenes, "captions": caption_chunks(scene_words, [t.end for t in timings])}


def captions_srt(captions: list[dict[str, Any]]) -> str:
    def ts(x: float) -> str:
        ms = int(round(x * 1000))
        return f"{ms // 3_600_000:02d}:{ms // 60_000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    return "".join(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{' '.join(w['text'] for w in c['words'])}\n\n"
                   for i, c in enumerate(captions, start=1))


def run_renderer(spec_path: Path, out: Path, channel: str, log: Path, extra: list[str] | None = None) -> str:
    node = shutil.which("node")
    if node is None:
        raise MediaToolError("Node.js not found; the motion renderer needs node + the global @playwright/cli install")
    cmd = [node, str(RENDERER), str(spec_path), str(out), "--channel", channel, *(extra or [])]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=RENDER_TIMEOUT_SECONDS, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("motion render timed out") from exc
    with log.open("a", encoding="utf-8") as fh:
        fh.write("$ " + " ".join(cmd) + "\n" + p.stdout[-2000:] + p.stderr[-4000:] + "\n")
    if p.returncode != 0:
        raise MediaToolError(f"motion renderer failed: {p.stderr.strip()[-400:]}")
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
