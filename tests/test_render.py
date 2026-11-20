import json
import shutil
import subprocess
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from PIL import Image

from studio.compose import build_cues, plan_timings, render_production, scaled_timings, source_lines
from studio.config import load_config
from studio.errors import ConfigError, StudioError
from studio.production import create_production, set_status
from studio.render_config import DEFAULT_RENDER_CONFIG, load_render_config
from studio.tts import apply_pronunciations
from studio.visuals import CardRenderer, chunk_caption, readability_problems, time_cues, to_srt
from tests.script_fixtures import SOURCES, write_valid

CFG = load_config()
RCFG = load_render_config()
NOW = datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)


class CaptionTests(unittest.TestCase):
    def test_chunks_respect_limits_and_keep_all_words(self) -> None:
        text = "Here is a simple habit that fixes this problem for most teams, and it is cheap."
        chunks = chunk_caption(text, 6, 30)
        self.assertEqual(" ".join(chunks).split(), text.split())
        for c in chunks:
            self.assertLessEqual(len(c.split()), 7)

    def test_breaks_after_punctuation(self) -> None:
        self.assertEqual(chunk_caption("Hello there, tool calling needs it.", 6, 30), ["Hello there,", "tool calling needs it."])
        # never a one-word caption: a lone "First," stays with the following words
        self.assertEqual(chunk_caption("First, tool calling needs it.", 6, 30), ["First, tool calling needs it."])

    def test_cue_timing_is_contiguous_and_proportional(self) -> None:
        cues = time_cues(1, 2.0, 3.0, ["aaaa", "aaaaaaaa"])
        self.assertAlmostEqual(cues[0].start, 2.0)
        self.assertAlmostEqual(cues[0].end, 3.0)
        self.assertAlmostEqual(cues[1].end, 5.0)

    def test_srt_format(self) -> None:
        srt = to_srt(time_cues(1, 61.5, 1.0, ["Hello there"]))
        self.assertIn("00:01:01,500 --> 00:01:02,500\nHello there", srt)


class TimingTests(unittest.TestCase):
    def test_plan_timings_snap_to_frames(self) -> None:
        t = plan_timings([2.01, 3.333], 0.35, 30)
        self.assertEqual(t[0].start, 0.0)
        self.assertEqual(t[1].start, t[0].end)
        for tm in t:
            self.assertAlmostEqual(tm.end * 30, round(tm.end * 30), places=3)

    def test_parse_loudnorm_json(self) -> None:
        from studio.compose import parse_loudnorm_json
        from studio.errors import MediaToolError

        stderr = 'noise\n[Parsed_loudnorm_0 @ 0x1]\n{\n "input_i" : "-21.3", "input_tp" : "-6.0", "input_lra" : "3.1",\n' \
                 ' "input_thresh" : "-31.5", "target_offset" : "0.2"\n}\n'
        self.assertEqual(parse_loudnorm_json(stderr)["input_i"], "-21.3")
        with self.assertRaises(MediaToolError):
            parse_loudnorm_json("no json here")

    def test_directed_pauses_extend_scenes(self) -> None:
        from studio.compose import scene_pauses

        scenes = [{"id": 1, "voice": {"pause_after_ms": 300}}, {"id": 2}]
        pauses = scene_pauses(scenes)
        self.assertEqual(pauses, [0.3, 0.0])
        with_pause = plan_timings([2.0, 2.0], 0.0, 30, pauses)
        self.assertAlmostEqual(with_pause[0].end, 2.3, places=3)
        self.assertAlmostEqual(with_pause[1].end, 4.3, places=3)

    def test_scaled_timings_end_at_audio_length(self) -> None:
        scenes = [{"id": 1, "start_seconds": 0, "end_seconds": 20}, {"id": 2, "start_seconds": 20, "end_seconds": 40}]
        t = scaled_timings(scenes, 44.0, 30)
        self.assertAlmostEqual(t[0].end, 22.0)
        self.assertAlmostEqual(t[-1].end, 44.0)

    def test_cues_are_gapless_and_cover_timeline(self) -> None:
        scenes = [{"id": 1, "narration": "One two three four five six seven eight."},
                  {"id": 2, "narration": "Nine ten eleven."}]
        timings = plan_timings([2.0, 1.5], 0.35, 30)
        cues = build_cues(scenes, timings, RCFG.style, 30)
        self.assertEqual(cues[0].start, 0.0)
        self.assertEqual(cues[-1].end, timings[-1].end)
        for a, b in zip(cues, cues[1:]):
            self.assertEqual(a.end, b.start)


class TtsAndConfigTests(unittest.TestCase):
    def test_pronunciations_only_whole_terms(self) -> None:
        p = {"GPT-6.2": "G P T six point two", "MCP": "M C P", "/eval": "slash eval"}
        self.assertEqual(apply_pronunciations("Moving to GPT-6.2? Use MCP and /eval.", p),
                         "Moving to G P T six point two? Use M C P and slash eval.")
        self.assertEqual(apply_pronunciations("MCPS stays", p), "MCPS stays")

    def test_caption_size_floor_enforced(self) -> None:
        d = json.loads(DEFAULT_RENDER_CONFIG.read_text(encoding="utf-8"))
        d["style"]["caption_size"] = 30
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "r.json"
            p.write_text(json.dumps(d), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "unreadable"):
                load_render_config(p)

    def test_source_lines(self) -> None:
        self.assertEqual(source_lines(SOURCES)["S1"], "Source: Example · 2026-11-17")


@unittest.skipUnless(Path(RCFG.style["font_bold"]).is_file(), "system font missing")
class CardTests(unittest.TestCase):
    def test_card_is_vertical_and_readable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "f.png"
            metrics = CardRenderer(RCFG.style).render("Test before and after", "Rerun the same eval", "Source: GitHub · 2026-11-17", 0.5, out)
            with Image.open(out) as img:
                self.assertEqual(img.size, (1080, 1920))
            self.assertEqual(readability_problems(metrics, RCFG.style), [])

    def test_balanced_wrap_avoids_orphan_word(self) -> None:
        from PIL import ImageDraw

        from studio.visuals import _font, balanced_wrap

        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        font = _font(RCFG.style["font_bold"], RCFG.style["caption_size"])
        lines = balanced_wrap(d, "GitHub just added a way to", font, 800)
        self.assertEqual(len(lines), 2)
        self.assertGreater(len(lines[1].split()), 1)

    def test_readability_flags_bad_layout(self) -> None:
        bad = {"caption_size": 40, "caption_left": 10, "caption_right": 1075, "caption_bottom": 1700,
               "headline_lines": 6, "caption_lines": 3}
        self.assertEqual(len(readability_problems(bad, RCFG.style)), 5)


@unittest.skipUnless(shutil.which("ffmpeg") and Path(RCFG.style["font_bold"]).is_file(), "FFmpeg or font missing")
class RenderIntegrationTests(unittest.TestCase):
    def test_manual_voiceover_render_meets_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = create_production(CFG, date(2026, 11, 20), "demo", "Demo", "English", root=root, now=NOW)
            write_valid(folder)
            set_status(folder, CFG, "APPROVED_TOPIC", now=NOW)
            with self.assertRaisesRegex(StudioError, "SCRIPT_READY"):
                render_production(folder, CFG, RCFG, "manual")
            set_status(folder, CFG, "SCRIPT_READY", now=NOW)
            with self.assertRaisesRegex(StudioError, "does not exist"):
                render_production(folder, CFG, RCFG, "manual")
            vo = folder / "voiceover" / "voiceover.wav"
            vo.parent.mkdir()
            subprocess.run([shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                            "-i", "sine=frequency=220:duration=40", "-ar", "48000", str(vo)], check=True, timeout=60)

            rep = render_production(folder, CFG, RCFG, "auto")
            self.assertEqual(rep.voice_source, "manual")
            self.assertEqual(rep.errors, [])
            self.assertEqual((rep.probe["width"], rep.probe["height"]), (1080, 1920))
            self.assertEqual((rep.probe["video_codec"], rep.probe["audio_codec"]), ("h264", "aac"))
            self.assertAlmostEqual(rep.duration_seconds, 40.0, delta=0.25)
            self.assertTrue((folder / "render" / "captions.srt").read_text(encoding="utf-8").startswith("1\n00:00:00,000"))

            set_status(folder, CFG, "ASSETS_READY", now=NOW)
            final = set_status(folder, CFG, "RENDERED", now=NOW)
            self.assertEqual(final["status"], "RENDERED")


if __name__ == "__main__":
    unittest.main()
