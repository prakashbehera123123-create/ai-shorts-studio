"""Local voiceover: user-recorded file first, Windows SAPI placeholder second. No network, no paid APIs.

SAPI also reports word boundaries (SpeakProgress), which give real word timings for karaoke captions and for
syncing visual builds to the words they illustrate.
"""
from __future__ import annotations

import bisect
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .errors import MediaToolError
from .render_config import RenderConfig

# Fixed script; all inputs arrive via environment variables, so narration text is never interpolated into code.
# Word boundary events are written as "charPos<TAB>audioMs" lines.
SAPI_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$script:marks = New-Object System.Collections.Generic.List[string]
try {
  $s.SelectVoice($env:STUDIO_TTS_VOICE)
  $s.Rate = [int]$env:STUDIO_TTS_RATE
  $fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo([int]$env:STUDIO_TTS_SR, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
  $s.SetOutputToWaveFile($env:STUDIO_TTS_OUT, $fmt)
  $s.add_SpeakProgress({ param($sender, $e) $script:marks.Add("$($e.CharacterPosition)`t$([int]$e.AudioPosition.TotalMilliseconds)") })
  $s.Speak([System.IO.File]::ReadAllText($env:STUDIO_TTS_TEXT, [System.Text.Encoding]::UTF8))
} finally { $s.Dispose() }
[System.IO.File]::WriteAllLines($env:STUDIO_TTS_MARKS, $script:marks)
"""
TTS_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class WordTime:
    text: str      # original caption word (with punctuation)
    start: float   # seconds from the start of this clip
    end: float


def _norm(tok: str) -> str:
    return re.sub(r"^[^\w/]+|[^\w]+$", "", tok)


def spoken_tokens(text: str, pronunciations: dict[str, str]) -> tuple[list[str], list[str]]:
    """Split narration into original tokens and their spoken forms (pronunciation applied per token/phrase).

    Multi-word keys (e.g. "Copilot CLI") replace the first token's spoken form and blank the rest, so token
    indexes stay aligned with the original words.
    """
    orig = text.split()
    spoken = list(orig)
    keys = sorted(pronunciations, key=lambda k: len(k.split()), reverse=True)
    i = 0
    while i < len(orig):
        for key in keys:
            parts = key.split()
            window = [_norm(t) for t in orig[i:i + len(parts)]]
            if window == parts or (len(parts) == 1 and _norm(orig[i]) == key):
                tail = re.sub(r"^.*?([^\w]*)$", r"\1", orig[i + len(parts) - 1])  # keep trailing punctuation
                spoken[i] = pronunciations[key] + tail
                for j in range(i + 1, i + len(parts)):
                    spoken[j] = ""
                i += len(parts) - 1
                break
        i += 1
    return orig, spoken


def apply_pronunciations(text: str, pronunciations: dict[str, str]) -> str:
    """Rewrite terms for the speech engine only (captions keep the original text)."""
    _, spoken = spoken_tokens(text, pronunciations)
    return " ".join(s for s in spoken if s)


def map_word_times(orig: list[str], spoken: list[str], marks: list[tuple[int, int]], duration: float) -> list[WordTime]:
    """Map SAPI (charPos, ms) boundary events on the spoken text back to original words.

    Each original word starts at the first event inside its spoken span; words without an event are interpolated;
    each word ends where the next begins (last word ends at `duration`).
    """
    offsets, pos = [], 0
    for s in spoken:
        offsets.append(pos)
        if s:
            pos += len(s) + 1
    starts: list[float | None] = [None] * len(orig)
    for char_pos, ms in sorted(marks, key=lambda m: m[1]):
        idx = bisect.bisect_right(offsets, char_pos) - 1
        while idx > 0 and not spoken[idx]:
            idx -= 1
        if 0 <= idx < len(orig) and starts[idx] is None:
            starts[idx] = ms / 1000
    known = [(i, t) for i, t in enumerate(starts) if t is not None]
    if not known:  # no events: spread by characters
        total = sum(len(w) for w in orig) or 1
        acc, filled = 0.0, []
        for w in orig:
            filled.append(duration * acc / total)
            acc += len(w)
    else:
        filled = []
        for i in range(len(orig)):
            if starts[i] is not None:
                filled.append(starts[i])
                continue
            prev = max(((j, t) for j, t in known if j < i), default=(-1, 0.0))
            nxt = min(((j, t) for j, t in known if j > i), default=(len(orig), duration))
            frac = (i - prev[0]) / (nxt[0] - prev[0])
            filled.append(prev[1] + (nxt[1] - prev[1]) * frac)
    for i in range(1, len(filled)):  # monotonic
        filled[i] = max(filled[i], filled[i - 1])
    filled = [min(t, duration) for t in filled]
    return [WordTime(w, round(filled[i], 3), round(max(filled[i], filled[i + 1] if i + 1 < len(filled) else duration), 3))
            for i, w in enumerate(orig)]


def synthesize_sapi(text: str, out_wav: Path, rcfg: RenderConfig) -> list[tuple[int, int]]:
    """Speak `text` to `out_wav`; returns SAPI word-boundary marks (charPos in spoken text, audio ms)."""
    exe = shutil.which("powershell") or shutil.which("powershell.exe")
    if exe is None:
        raise MediaToolError("Windows PowerShell not found; SAPI TTS is unavailable. Record voiceover/voiceover.wav instead.")
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    text_file = out_wav.with_suffix(".txt")
    marks_file = out_wav.with_suffix(".marks.txt")
    text_file.write_text(apply_pronunciations(text, rcfg.pronunciations), encoding="utf-8")
    env = os.environ | {
        "STUDIO_TTS_VOICE": rcfg.tts_voice,
        "STUDIO_TTS_RATE": str(rcfg.tts_rate),
        "STUDIO_TTS_SR": str(rcfg.tts_sample_rate),
        "STUDIO_TTS_OUT": str(out_wav.resolve()),
        "STUDIO_TTS_TEXT": str(text_file.resolve()),
        "STUDIO_TTS_MARKS": str(marks_file.resolve()),
    }
    try:
        subprocess.run([exe, "-NoProfile", "-NonInteractive", "-Command", SAPI_SCRIPT], env=env,
                       capture_output=True, text=True, check=True, timeout=TTS_TIMEOUT_SECONDS, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError(f"SAPI TTS timed out for {out_wav.name}") from exc
    except subprocess.CalledProcessError as exc:
        raise MediaToolError(f"SAPI TTS failed for {out_wav.name}: {(exc.stderr or '').strip()[:300]}") from exc
    if not out_wav.is_file() or out_wav.stat().st_size < 1000:
        raise MediaToolError(f"SAPI TTS produced no audio for {out_wav.name}")
    return parse_marks(marks_file.read_text(encoding="utf-8-sig") if marks_file.is_file() else "", rcfg.tts_sample_rate)


SAPI_POSITION_RATE = 16000  # SAPI reports AudioPosition as if output were 16 kHz (measured at 16k/22.05k/24k/48k)


def parse_marks(text: str, sample_rate: int) -> list[tuple[int, int]]:
    """'charPos<TAB>ms' lines -> [(charPos, true_ms)], correcting SAPI's 16 kHz position time base."""
    scale = SAPI_POSITION_RATE / sample_rate
    marks: list[tuple[int, int]] = []
    for line in text.splitlines():
        parts = line.strip().split("\t")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].lstrip("-").isdigit():
            marks.append((int(parts[0]), round(int(parts[1]) * scale)))
    return marks
