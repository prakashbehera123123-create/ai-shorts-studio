from __future__ import annotations


class StudioError(Exception):
    """Base class for all project errors."""


class ConfigError(StudioError):
    """Configuration file is missing or invalid."""


class ContractError(StudioError):
    """A production file violates its contract. Carries every problem found."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("; ".join(self.problems) or "contract violation")


class TransitionError(StudioError):
    """A status change is not allowed by the lifecycle."""


class MediaToolError(StudioError):
    """FFmpeg/FFprobe is missing or failed."""
