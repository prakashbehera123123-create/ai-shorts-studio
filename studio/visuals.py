"""Caption chunking/timing, SRT output and Pillow scene cards (1080x1920)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .errors import StudioError

Font = ImageFont.FreeTypeFont


@dataclass(frozen=True)
class Cue:
    scene_id: int
    start: float
    end: float
    text: str


def chunk_caption(text: str, max_words: int, max_chars: int) -> list[str]:
    """Split narration into short caption lines; prefer breaking after punctuation."""
    tokens = text.split()
    chunks: list[str] = []
    cur: list[str] = []
    for tok in tokens:
        candidate = " ".join([*cur, tok])
        if cur and (len(cur) >= max_words or len(candidate) > max_chars):
            chunks.append(" ".join(cur))
            cur = []
        cur.append(tok)
        if re.search(r"[.?!,;:]$", tok) and len(cur) >= 2:
            chunks.append(" ".join(cur))
            cur = []
    if cur:
        if chunks and len(cur) == 1 and len(chunks[-1]) + 1 + len(cur[0]) <= max_chars + 6:
            chunks[-1] = f"{chunks[-1]} {cur[0]}"
        else:
            chunks.append(" ".join(cur))
    return chunks


def time_cues(scene_id: int, start: float, speech_seconds: float, chunks: list[str]) -> list[Cue]:
    """Spread chunks across the spoken part of a scene in proportion to their length."""
    weights = [max(len(c), 1) for c in chunks]
    total = sum(weights)
    cues, t = [], start
    for chunk, w in zip(chunks, weights):
        dur = speech_seconds * w / total
        cues.append(Cue(scene_id, round(t, 3), round(t + dur, 3), chunk))
        t += dur
    return cues


def _srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_srt(cues: list[Cue]) -> str:
    return "".join(f"{i}\n{_srt_time(c.start)} --> {_srt_time(c.end)}\n{c.text}\n\n" for i, c in enumerate(cues, start=1))


def _hex(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def _font(path: str, size: int) -> Font:
    try:
        return ImageFont.truetype(path, size)
    except OSError as exc:
        raise StudioError(f"Font not found or unreadable: {path}") from exc


def wrap(draw: ImageDraw.ImageDraw, text: str, font: Font, max_width: int) -> list[str]:
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for line in lines:
        if draw.textlength(line, font=font) > max_width:
            raise StudioError(f"Word too wide for safe area: '{line}'")
    return lines


def balanced_wrap(draw: ImageDraw.ImageDraw, text: str, font: Font, max_width: int) -> list[str]:
    """Like wrap(), but when two lines are needed choose the split that makes them most even (no orphan words)."""
    lines = wrap(draw, text, font, max_width)
    if len(lines) != 2:
        return lines
    words_ = text.split()
    best: tuple[float, list[str]] | None = None
    for i in range(1, len(words_)):
        a, b = " ".join(words_[:i]), " ".join(words_[i:])
        wa, wb = draw.textlength(a, font=font), draw.textlength(b, font=font)
        if max(wa, wb) <= max_width and (best is None or max(wa, wb) < best[0]):
            best = (max(wa, wb), [a, b])
    return best[1] if best else lines


class CardRenderer:
    W, H = 1080, 1920

    def __init__(self, style: dict[str, Any]) -> None:
        self.s = style
        self.bold = {k: _font(style["font_bold"], style[k]) for k in ("headline_size", "caption_size")}
        self.small = _font(style["font_regular"], style["source_size"])
        self.max_w = self.W - 2 * int(style["side_margin"])
        self._bg = self._background()

    def _background(self) -> Image.Image:
        top, bottom = _hex(self.s["background_top"]), _hex(self.s["background_bottom"])
        img = Image.new("RGB", (self.W, self.H))
        px = ImageDraw.Draw(img)
        for y in range(self.H):
            t = y / (self.H - 1)
            px.line([(0, y), (self.W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
        return img

    def render(self, headline: str, caption: str, source_line: str, progress: float, out: Path) -> dict[str, int]:
        """Draw one frame; returns layout metrics used by the readability check."""
        img = self._bg.copy()
        d = ImageDraw.Draw(img, "RGBA")
        accent, text, muted = _hex(self.s["accent"]), _hex(self.s["text"]), _hex(self.s["muted"])
        margin = int(self.s["side_margin"])

        d.rounded_rectangle([margin, 150, self.W - margin, 162], radius=6, fill=(*muted, 70))
        d.rounded_rectangle([margin, 150, margin + max(12, int(self.max_w * progress)), 162], radius=6, fill=accent)

        hfont = self.bold["headline_size"]
        hlines = wrap(d, headline, hfont, self.max_w)
        line_h = int(hfont.size * 1.18)
        y = 560 - (len(hlines) * line_h) // 2
        d.rectangle([margin, y - 40, margin + 120, y - 30], fill=accent)
        for line in hlines:
            d.text((margin, y), line, font=hfont, fill=text)
            y += line_h
        headline_bottom = y

        if source_line:
            d.text((margin, headline_bottom + 40), source_line, font=self.small, fill=muted)

        cfont = self.bold["caption_size"]
        clines = balanced_wrap(d, caption, cfont, self.max_w - 60)
        c_line_h = int(cfont.size * 1.2)
        box_top = int(self.s["caption_top"])
        box_bottom = box_top + 40 + c_line_h * len(clines)
        widest = max(int(d.textlength(c, font=cfont)) for c in clines)
        left = (self.W - widest) // 2 - 30
        d.rounded_rectangle([left, box_top, self.W - left, box_bottom], radius=28, fill=(0, 0, 0, 175))
        cy = box_top + 20
        for line in clines:
            w = d.textlength(line, font=cfont)
            d.text(((self.W - w) / 2, cy), line, font=cfont, fill=text)
            cy += c_line_h

        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, optimize=False)
        return {"caption_size": cfont.size, "caption_left": left, "caption_right": self.W - left,
                "caption_bottom": box_bottom, "headline_lines": len(hlines), "caption_lines": len(clines)}


def readability_problems(metrics: dict[str, int], style: dict[str, Any], height: int = 1920) -> list[str]:
    """Mobile readability: caption size, side margins, and staying above the Shorts UI zone (bottom 18%)."""
    problems = []
    if metrics["caption_size"] < style["min_caption_size"]:
        problems.append(f"caption font {metrics['caption_size']}px below {style['min_caption_size']}px")
    if metrics["caption_left"] < 60 or metrics["caption_right"] > 1080 - 60:
        problems.append("caption box breaks the 60px side safe margin")
    if metrics["caption_bottom"] > int(height * 0.82):
        problems.append("caption box enters the bottom 18% covered by Shorts UI")
    if metrics["caption_lines"] > 2:
        problems.append(f"caption uses {metrics['caption_lines']} lines; max 2")
    if metrics["headline_lines"] > 4:
        problems.append(f"headline uses {metrics['headline_lines']} lines; max 4")
    return problems
