import tempfile
import unittest
from pathlib import Path

from studio.compose_types import SceneTiming
from studio.render_config import load_render_config
from studio.scene3d import Clip3D, check_project, overlay_filter, project_hash, render_3d_clips, scenes_needing_3d
from studio.storyboard import _creative_problems

ROOT = Path(__file__).resolve().parents[1]


class Scene3DTests(unittest.TestCase):
    def test_no_3d_scene_means_no_hyperframes_call(self) -> None:
        board = {"scenes": [{"id": 1, "visual": {"template": "kinetic"}}, {"id": 2, "visual_form": "chart"}]}
        self.assertEqual(scenes_needing_3d(board), [])
        # returns before looking for the HyperFrames CLI at all
        self.assertEqual(render_3d_clips(Path("."), board, [SceneTiming(1, 0, 1, 1)], load_render_config(), Path("x.log")), [])

    def test_scene3d_needs_form_justification_and_project(self) -> None:
        scene = {"id": 3, "visual_form": "flow_diagram", "visual": {"template": "scene3d"}}
        joined = " ".join(_creative_problems(scene, "scene 3", strict=False))
        self.assertIn("needs visual_form 'scene_3d'", joined)
        self.assertIn("visual.project", joined)
        ok = {"id": 3, "visual_form": "scene_3d", "visual_justification": "satellite parts in space",
              "visual": {"template": "scene3d", "project": "assets/3d/scene_03"}}
        self.assertFalse([p for p in _creative_problems(ok, "scene 3", strict=False) if "scene3d" in p or "scene_3d" in p])

    def test_template_matches_visual_zone(self) -> None:
        self.assertEqual(check_project(ROOT / "templates" / "scene3d"), [])
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "index.html").write_text('<div data-width="1080" data-height="1920">Math.random()</div>', encoding="utf-8")
            joined = " ".join(check_project(Path(tmp)))
            self.assertIn("1080", joined)
            self.assertIn("Math.random", joined)

    def test_hash_ignores_render_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "index.html").write_text("a", encoding="utf-8")
            h = project_hash(p)
            (p / "renders").mkdir()
            (p / "renders" / "clip.mov").write_bytes(b"x")
            self.assertEqual(h, project_hash(p))
            (p / "index.html").write_text("b", encoding="utf-8")
            self.assertNotEqual(h, project_hash(p))

    def test_overlay_only_inside_scene_window(self) -> None:
        graph, last = overlay_filter([Clip3D(2, 2.0, 9.5, Path("c.mov"), True)])
        self.assertIn("overlay=0:560", graph)
        self.assertIn("between(t,2.000,9.500)", graph)
        self.assertIn("stop_mode=clone", graph)  # short clip holds its last frame
        self.assertEqual(last, "v1")


if __name__ == "__main__":
    unittest.main()
