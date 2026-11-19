import unittest
from typing import Any

from studio.config import load_config
from studio.storyboard import validate_storyboard_data

CFG = load_config()


def scene(i: int, start: float, end: float, **kw: Any) -> dict[str, Any]:
    s = {"id": i, "start_seconds": start, "end_seconds": end, "narration": "n", "on_screen_text": "t",
         "visual_type": "generated_graphic", "source_ids": []}
    s.update(kw)
    return s


def board(scenes: list[dict[str, Any]], **kw: Any) -> dict[str, Any]:
    b = {"video_id": "2026-11-20-demo", "language": "English", "target_duration_seconds": 40, "format": "9:16", "scenes": scenes}
    b.update(kw)
    return b


class StoryboardTests(unittest.TestCase):
    def test_contiguous_scenes_valid(self) -> None:
        self.assertEqual(validate_storyboard_data(board([scene(1, 0, 3), scene(2, 3, 8.5)]), CFG), [])

    def test_language_must_be_single_configured(self) -> None:
        for lang in ("Hindi", "English+Hinglish", None):
            self.assertTrue(validate_storyboard_data(board([], language=lang), CFG))

    def test_gap_and_overlap_detected(self) -> None:
        gap = validate_storyboard_data(board([scene(1, 0, 3), scene(2, 4, 6)]), CFG)
        overlap = validate_storyboard_data(board([scene(1, 0, 3), scene(2, 2, 6)]), CFG)
        self.assertTrue(any("gap" in p for p in gap))
        self.assertTrue(any("overlaps" in p for p in overlap))

    def test_too_long_and_bad_visual_type(self) -> None:
        problems = validate_storyboard_data(board([scene(1, 0, 70, visual_type="random_footage")]), CFG)
        self.assertTrue(any("above max" in p for p in problems))
        self.assertTrue(any("visual_type" in p for p in problems))

    def test_target_duration_out_of_range(self) -> None:
        self.assertTrue(validate_storyboard_data(board([], target_duration_seconds=90), CFG))

    def test_require_scenes(self) -> None:
        self.assertTrue(validate_storyboard_data(board([]), CFG, require_scenes=True))


if __name__ == "__main__":
    unittest.main()
