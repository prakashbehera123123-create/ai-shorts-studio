import tempfile
import unittest
from pathlib import Path
from unittest import mock

from studio import sound
from studio.compose_types import SceneTiming
from studio.errors import MediaToolError
from studio.motion_spec import icon_svg, visual_for


def _gen() -> dict[str, Path]:
    return {n: Path(f"{n}.wav") for n in sound.GENERATORS}


class SoundPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timings = [SceneTiming(i, i * 4.0, 3.5, i * 4.0 + 4.0) for i in range(1, 7)]

    def _board(self, transitions, sfx=None, beats=None):
        return {"scenes": [{"id": i + 1, "transition_in": t, "beat": (beats or ["x"] * 6)[i], "sfx": (sfx or {}).get(i + 1, [])}
                           for i, t in enumerate(transitions)]}

    def test_explicit_cue_and_transition_defaults(self) -> None:
        with mock.patch.object(sound, "licensed_files", return_value=[]):
            cues = sound.plan_sfx(self._board(["cut", "push", "cut", "match_cut", "cut", "crossfade"], {1: ["knock"]}),
                                  self.timings, _gen(), auto=True)
        names = [(c.name, c.time) for c in cues]
        self.assertEqual(names[0], ("knock", 4.0))                 # storyboard cue at scene start
        self.assertIn(("whoosh", 7.65), names)                     # whoosh leads into the push cut (pause 7.5-8.0)
        self.assertIn(("rise", 15.65), names)
        self.assertNotIn(12.0, [t for _, t in names])             # plain cut, same beat: silence

    def test_whoosh_never_overlaps_previous_speech(self) -> None:
        timings = [SceneTiming(1, 0.0, 3.9, 4.0), SceneTiming(2, 4.0, 3.0, 8.0)]  # only 0.1 s pause before scene 2
        board = {"scenes": [{"id": 1, "transition_in": "cut", "beat": "a"}, {"id": 2, "transition_in": "push", "beat": "a"}]}
        with mock.patch.object(sound, "licensed_files", return_value=[]):
            cue = sound.plan_sfx(board, timings, _gen(), auto=True)[0]
        self.assertEqual(cue.name, "whoosh")
        self.assertGreaterEqual(cue.time, 3.9)

    def test_auto_off_keeps_only_explicit(self) -> None:
        with mock.patch.object(sound, "licensed_files", return_value=[]):
            cues = sound.plan_sfx(self._board(["cut", "push", "push", "push", "push", "push"]), self.timings, _gen(), auto=False)
        self.assertEqual(cues, [])

    def test_density_cap(self) -> None:
        cues = [sound.SfxCue(float(t), "pop", Path("pop.wav")) for t in range(0, 30, 3)]
        self.assertEqual(len(sound._thin(cues)), sound.MAX_SFX_PER_30S)

    def test_mix_filter_ducks_bed_and_delays_sfx(self) -> None:
        g = sound.mix_filter(1, 40.0, -4, -10, [sound.SfxCue(2.45, "whoosh", Path("w.wav"))])
        self.assertIn("sidechaincompress", g)
        self.assertIn("adelay=2450|2450", g)
        self.assertIn("amix=inputs=3", g)

    def test_downloaded_audio_needs_licence_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lib = Path(tmp)
            (lib / "music").mkdir()
            (lib / "music" / "a.mp3").write_bytes(b"x")
            (lib / "music" / "b.mp3").write_bytes(b"x")
            (lib / "LICENSES.csv").write_text("file,source_url,creator,license\nmusic/a.mp3,https://x,me,Pixabay Content License\n",
                                              encoding="utf-8")
            with mock.patch.object(sound, "LIBRARY", lib):
                self.assertEqual([p.name for p in sound.licensed_files("music")], ["a.mp3"])


class IconTests(unittest.TestCase):
    def test_icon_resolves_and_rejects_unknown(self) -> None:
        self.assertIn("<svg", icon_svg("bell-ring"))
        with self.assertRaises(MediaToolError):
            icon_svg("not-a-real-icon-name")
        with self.assertRaises(MediaToolError):
            icon_svg("../etc")

    def test_nested_icons_resolved(self) -> None:
        v = visual_for({"id": 1, "visual": {"template": "split", "left": {"title": "A", "icon": "repeat"},
                                              "right": {"title": "B"}}})
        self.assertIn("icon_svg", v["left"])
        self.assertNotIn("icon_svg", v["right"])


if __name__ == "__main__":
    unittest.main()
