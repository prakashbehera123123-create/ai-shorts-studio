from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT
from .errors import ConfigError

DEFAULT_RENDER_CONFIG = PROJECT_ROOT / "config" / "render.json"


@dataclass(frozen=True)
class RenderConfig:
    fps: int
    scene_padding: float
    tts_engine: str
    tts_voice: str
    tts_rate: int
    tts_sample_rate: int
    pronunciations: dict[str, str]
    loudness_lufs: float
    true_peak_db: float
    audio_bitrate: str
    audio_sample_rate: int
    crf: int
    preset: str
    style: dict[str, Any]
    renderer: str = "cards"          # "motion" = studio/motion/engine.html via scripts/render_motion.cjs
    browser_channel: str = "chrome"  # system browser Playwright drives (chrome | msedge)
    clone: dict[str, Any] = field(default_factory=dict)  # voice-clone engine settings (tts.engine == "clone")
    hyperframes: dict[str, Any] = field(default_factory=dict)  # 3D scenes: {"launcher": ".../plugin-cli.mjs"}
    sound: dict[str, Any] = field(default_factory=dict)  # music bed + SFX (studio/sound.py); {} or enabled=false = voice only


def load_render_config(path: Path | None = None) -> RenderConfig:
    path = path or DEFAULT_RENDER_CONFIG
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        cfg = RenderConfig(
            fps=int(d["fps"]),
            scene_padding=float(d["scene_padding_seconds"]),
            tts_engine=str(d["tts"]["engine"]),
            tts_voice=str(d["tts"]["voice"]),
            tts_rate=int(d["tts"]["rate"]),
            tts_sample_rate=int(d["tts"]["sample_rate"]),
            pronunciations={str(k): str(v) for k, v in d["tts"]["pronunciations"].items()},
            loudness_lufs=float(d["audio"]["loudness_lufs"]),
            true_peak_db=float(d["audio"]["true_peak_db"]),
            audio_bitrate=str(d["audio"]["bitrate"]),
            audio_sample_rate=int(d["audio"]["sample_rate"]),
            crf=int(d["video"]["crf"]),
            preset=str(d["video"]["preset"]),
            style=dict(d["style"]),
            renderer=str(d.get("renderer", "cards")),
            browser_channel=str(d.get("browser_channel", "chrome")),
            clone=dict(d["tts"].get("clone", {})),
            hyperframes=dict(d.get("hyperframes", {})),
            sound=dict(d.get("sound", {})),
        )
    except FileNotFoundError as exc:
        raise ConfigError(f"Render config not found: {path}") from exc
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ConfigError(f"Invalid render config {path}: {exc}") from exc
    if not -10 <= cfg.tts_rate <= 10:
        raise ConfigError("tts.rate must be between -10 and 10 (SAPI range)")
    if cfg.style["caption_size"] < cfg.style["min_caption_size"]:
        raise ConfigError("caption_size is below min_caption_size; captions would be unreadable on mobile")
    if not 0 <= cfg.scene_padding <= 1.5:
        raise ConfigError("scene_padding_seconds must be 0-1.5")
    return cfg
