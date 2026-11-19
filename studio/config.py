from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .errors import ConfigError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "production.json"


@dataclass(frozen=True)
class ProductionConfig:
    width: int
    height: int
    video_codec: str
    audio_codec: str
    min_duration: float
    max_duration: float
    default_target_duration: float
    min_words: int
    max_words: int
    languages: tuple[str, ...]
    max_videos_per_day: int
    production_root: Path


def _require(data: dict, dotted: str) -> object:
    node: object = data
    for key in dotted.split("."):
        if not isinstance(node, dict) or key not in node:
            raise ConfigError(f"Missing config key: {dotted}")
        node = node[key]
    return node


def load_config(path: Path | None = None) -> ProductionConfig:
    path = path or DEFAULT_CONFIG_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"Config root must be an object: {path}")

    try:
        cfg = ProductionConfig(
            width=int(_require(data, "video.width")),
            height=int(_require(data, "video.height")),
            video_codec=str(_require(data, "video.video_codec")),
            audio_codec=str(_require(data, "video.audio_codec")),
            min_duration=float(_require(data, "duration_seconds.min")),
            max_duration=float(_require(data, "duration_seconds.max")),
            default_target_duration=float(_require(data, "duration_seconds.default_target")),
            min_words=int(_require(data, "script_words.min")),
            max_words=int(_require(data, "script_words.max")),
            languages=tuple(str(x) for x in _require(data, "languages")),  # type: ignore[union-attr]
            max_videos_per_day=int(_require(data, "max_videos_per_day")),
            production_root=PROJECT_ROOT / str(_require(data, "production_root")),
        )
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"Invalid value type in {path}: {exc}") from exc

    if cfg.height <= cfg.width:
        raise ConfigError("Video must be vertical (height > width)")
    if not 0 < cfg.min_duration <= cfg.default_target_duration <= cfg.max_duration:
        raise ConfigError("Require 0 < duration min <= default_target <= max")
    if not 0 < cfg.min_words <= cfg.max_words:
        raise ConfigError("Require 0 < script_words.min <= max")
    if not cfg.languages:
        raise ConfigError("At least one language must be configured")
    return cfg
