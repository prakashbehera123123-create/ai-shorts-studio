from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SceneTiming:
    scene_id: int
    start: float
    speech: float
    end: float
