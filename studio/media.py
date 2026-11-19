"""Safe FFprobe wrapper and technical checks. Never loads media into memory."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import MediaToolError

PROBE_TIMEOUT_SECONDS = 60


def require_tool(name: str) -> str:
    exe = shutil.which(name)
    if exe is None:
        raise MediaToolError(f"'{name}' not found on PATH. Install FFmpeg and reopen the terminal.")
    return exe


def run_ffprobe(path: Path, timeout: int = PROBE_TIMEOUT_SECONDS) -> dict[str, Any]:
    if not path.is_file():
        raise MediaToolError(f"File not found: {path}")
    cmd = [require_tool("ffprobe"), "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=timeout, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError(f"ffprobe timed out after {timeout}s on {path}") from exc
    except subprocess.CalledProcessError as exc:
        raise MediaToolError(f"ffprobe failed on {path}: {(exc.stderr or '').strip()[:300]}") from exc
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise MediaToolError(f"ffprobe returned invalid JSON for {path}") from exc


def summarize(probe: dict[str, Any], file: str = "") -> dict[str, Any]:
    streams = probe.get("streams", []) or []
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    try:
        duration = float(probe.get("format", {}).get("duration", 0) or 0)
    except (TypeError, ValueError):
        duration = 0.0
    return {
        "file": file,
        "duration_seconds": round(duration, 2),
        "width": video.get("width"),
        "height": video.get("height"),
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name"),
        "has_video": bool(video),
        "has_audio": bool(audio),
    }


def check_summary(summary: dict[str, Any], cfg: ProductionConfig) -> list[str]:
    errors: list[str] = []
    if not summary["has_video"]:
        errors.append("No video stream found")
    else:
        if (summary["width"], summary["height"]) != (cfg.width, cfg.height):
            errors.append(f"Expected {cfg.width}x{cfg.height}, got {summary['width']}x{summary['height']}")
        if summary["video_codec"] != cfg.video_codec:
            errors.append(f"Expected video codec {cfg.video_codec}, got {summary['video_codec']}")
    if not summary["has_audio"]:
        errors.append("No audio stream found")
    elif summary["audio_codec"] != cfg.audio_codec:
        errors.append(f"Expected audio codec {cfg.audio_codec}, got {summary['audio_codec']}")
    d = summary["duration_seconds"]
    if not cfg.min_duration <= d <= cfg.max_duration:
        errors.append(f"Duration {d:.1f}s outside configured {cfg.min_duration:g}-{cfg.max_duration:g}s range")
    return errors
