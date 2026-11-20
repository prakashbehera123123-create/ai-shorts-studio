"""Voice clean-up: denoise filter chain and a measurable noise metric.

Metric: split mono 16 kHz audio into 50 ms windows; noise = 10th-percentile window RMS (the quiet gaps between words),
speech = median window RMS; SNR = speech - noise in dB. Used to verify the denoise actually helps.
"""
from __future__ import annotations

import math
import statistics
import struct
import subprocess
from pathlib import Path

from .errors import MediaToolError
from .media import require_tool

# Spectral denoise (adaptive noise tracking) twice, gentle high-pass for rumble, then a soft gate so pauses are clean.
DENOISE_CHAIN = ("highpass=f=80,afftdn=nr=20:nf=-40:tn=1,afftdn=nr=10:nf=-45:tn=1,"
                 "agate=threshold=0.01:ratio=3:attack=5:release=120:range=0.1")
WINDOW_S = 0.05


def window_rms_db(path: Path) -> list[float]:
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(path),
           "-ac", "1", "-ar", "16000", "-f", "s16le", "-"]
    p = subprocess.run(cmd, capture_output=True, timeout=120, shell=False)
    if p.returncode != 0:
        raise MediaToolError(f"could not decode {path}")
    n = int(16000 * WINDOW_S)
    samples = struct.unpack(f"<{len(p.stdout) // 2}h", p.stdout[: len(p.stdout) // 2 * 2])
    out = []
    for i in range(0, len(samples) - n + 1, n):
        w = samples[i:i + n]
        rms = math.sqrt(sum(x * x for x in w) / n) / 32768
        out.append(20 * math.log10(max(rms, 1e-7)))
    return out


def noise_profile(path: Path) -> dict[str, float]:
    levels = sorted(window_rms_db(path))
    if not levels:
        return {"noise_db": 0.0, "speech_db": 0.0, "snr_db": 0.0}
    noise = levels[int(len(levels) * 0.10)]
    speech = statistics.median(levels)
    return {"noise_db": round(noise, 1), "speech_db": round(speech, 1), "snr_db": round(speech - noise, 1)}


def denoise(src: Path, dst: Path, extra_filters: str = "") -> None:
    chain = DENOISE_CHAIN + (f",{extra_filters}" if extra_filters else "")
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-loglevel", "error", "-y", "-i", str(src), "-af", chain, str(dst)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, shell=False)
    if p.returncode != 0:
        raise MediaToolError(f"denoise failed for {src.name}: {p.stderr[-300:]}")
