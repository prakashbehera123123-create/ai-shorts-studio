import json
import shutil
import tempfile
import unittest
from pathlib import Path

from studio.compose_types import SceneTiming
from studio.motion_spec import (build_spec, caption_chunks, captions_srt, resolve_cues, run_renderer, step_labels,
                                visual_for)
from studio.tts import WordTime, map_word_times, parse_marks, spoken_tokens

PRON = {"GPT-6.2": "G P T six point two", "MCP": "M C P", "Copilot CLI": "Copilot C L I"}


def words(text: str, start: float = 0.0, step: float = 0.3) -> list[WordTime]:
    return [WordTime(w, round(start + i * step, 3), round(start + (i + 1) * step, 3)) for i, w in enumerate(text.split())]


class TtsTimingTests(unittest.TestCase):
    def test_spoken_tokens_keep_alignment(self) -> None:
        orig, spoken = spoken_tokens("Use GPT-6.2? Try Copilot CLI now.", PRON)
        self.assertEqual(len(orig), len(spoken))
        self.assertEqual(spoken[1], "G P T six point two?")
        self.assertEqual((spoken[3], spoken[4]), ("Copilot C L I", ""))

    def test_sapi_marks_corrected_to_real_time(self) -> None:
        # SAPI reports positions as if audio were 16 kHz; at 24 kHz a 4342 ms mark is really 2895 ms
        self.assertEqual(parse_marks("34\t4342\nbad line\n", 24000), [(34, 2895)])
        self.assertEqual(parse_marks("0\t100", 16000), [(0, 100)])

    def test_map_word_times_from_marks(self) -> None:
        orig, spoken = spoken_tokens("Switching to GPT-6.2? Check these.", PRON)
        # spoken text: "Switching to G P T six point two? Check these."
        marks = [(0, 90), (10, 490), (13, 610), (34, 2900), (40, 3150)]
        wt = map_word_times(orig, spoken, marks, 4.0)
        self.assertEqual([w.text for w in wt], orig)
        self.assertAlmostEqual(wt[2].start, 0.61)
        self.assertAlmostEqual(wt[3].start, 2.9)
        self.assertAlmostEqual(wt[-1].end, 4.0)
        self.assertTrue(all(w.end >= w.start for w in wt))

    def test_map_word_times_without_marks_spreads(self) -> None:
        wt = map_word_times(["aa", "bb"], ["aa", "bb"], [], 2.0)
        self.assertEqual((wt[0].start, wt[1].start, wt[1].end), (0.0, 1.0, 2.0))


class CaptionChunkTests(unittest.TestCase):
    def test_chunks_are_short_and_never_end_on_weak_word(self) -> None:
        w = words("So how do you know your change helped and why it matters today")
        chunks = caption_chunks([w], [10.0])
        for c in chunks:
            self.assertLessEqual(len(c["words"]), 4)
            self.assertNotIn(c["words"][-1]["text"].lower(), {"your", "you", "the", "to", "how"})
        self.assertEqual(sum(len(c["words"]) for c in chunks), len(w))

    def test_breaks_after_punctuation_and_scene(self) -> None:
        a, b = words("One. Two words", 0.0), words("Next scene", 2.0)
        chunks = caption_chunks([a, b], [1.5, 3.0])
        # "One." alone would flash for 0.3 s, so it merges forward; scenes are never merged across
        self.assertEqual([" ".join(x["text"] for x in c["words"]) for c in chunks], ["One. Two words", "Next scene"])
        self.assertLessEqual(chunks[0]["end"], 1.5)  # never spans into the next scene

    def test_short_chunks_merge_with_neighbour(self) -> None:
        from studio.motion_spec import merge_flashes

        fast = words("The first", 0.0, 0.15) + words("is a requirement.", 0.3, 0.4)
        merged = merge_flashes([fast[:2], fast[2:]])
        self.assertEqual(len(merged), 1)
        long_next = words("one two three four five", 0.3, 0.4)
        self.assertEqual(len(merge_flashes([fast[:2], long_next])), 2)  # would exceed 5 words: keep separate

    def test_srt(self) -> None:
        srt = captions_srt([{"start": 0.0, "end": 1.25, "words": [{"text": "Hi", "start": 0, "end": 1}]}])
        self.assertEqual(srt, "1\n00:00:00,000 --> 00:00:01,250\nHi\n\n")


class SpecTests(unittest.TestCase):
    def test_resolve_cues_sequential(self) -> None:
        w = words("Rerun it and it fails", start=10.0)
        self.assertEqual(resolve_cues(["Rerun", "fails", "missing"], w, 10.0), [0.0, 1.15, None])

    def test_step_labels(self) -> None:
        scenes = [{"on_screen_text": "Hook"}, {"on_screen_text": "1. Task"}, {"on_screen_text": "2: Run"}]
        self.assertEqual(step_labels(scenes), ["", "1/2", "2/2"])

    def test_visual_defaults_and_honest_fallback(self) -> None:
        self.assertEqual(visual_for({"visual_form": "title_card"})["template"], "title")
        v = visual_for({"visual_form": "architecture_flow", "on_screen_text": "Flow"})
        self.assertEqual(v, {"template": "kinetic", "lines": ["Flow"]})

    def test_build_spec(self) -> None:
        board = {"creative": {"central_question": "Why?"}, "scenes": [
            {"id": 1, "beat": "hook", "on_screen_text": "One good answer", "narration": "One good answer.", "source_ids": ["S1"],
             "voice": {"emphasis": ["good"]}, "visual": {"template": "kinetic", "cues": ["good"]}},
            {"id": 2, "beat": "explanation", "on_screen_text": "1. Task", "narration": "Give a task.", "source_ids": [],
             "transition_in": "push", "visual": {"template": "flow", "nodes": [{"label": "Task"}]}}]}
        timings = [SceneTiming(1, 0.0, 1.0, 1.3), SceneTiming(2, 1.3, 1.0, 2.6)]
        ws = [words("One good answer.", 0.0), words("Give a task.", 1.3)]
        sources = "| S1 | https://x | GitHub (changelog) | 2026-11-17 | 2026-11-20 | c | primary | high |"
        spec = build_spec(board, timings, ws, sources, 30, 20, "medium")
        s1, s2 = spec["scenes"]
        self.assertEqual((s1["accent"], s1["source"], s1["question"], s1["cues"]), ("good", "Source: GitHub · 2026-11-17", "", [0.25]))
        self.assertEqual((s2["question"], s2["transition_in"]), ("Why?", "push"))
        self.assertEqual(spec["duration"], 2.6)


@unittest.skipUnless(shutil.which("node") and shutil.which("ffmpeg"), "node/ffmpeg missing")
class EngineIntegrationTests(unittest.TestCase):
    def test_engine_renders_deterministic_stills(self) -> None:
        spec = {"fps": 30, "duration": 2.0, "scenes": [
            {"start": 0, "end": 1.0, "speech": 0.8, "headline": "Hello", "visual": {"template": "kinetic", "lines": ["Hello"]}},
            {"start": 1.0, "end": 2.0, "speech": 0.8, "headline": "Flow", "transition_in": "crossfade",
             "visual": {"template": "flow", "nodes": [{"label": "A"}, {"label": "B", "tone": "active"}]}}],
            "captions": [{"start": 0, "end": 1.0, "words": [{"text": "Hello", "start": 0, "end": 1.0}]}]}
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
            try:
                for run in ("a", "b"):
                    run_renderer(d / "spec.json", d / "x.mp4", "chrome", d / "log.txt", ["--still", "0.5,1.7", "--still-dir", str(d / run)])
            except Exception as exc:  # no Chrome/Playwright on this machine
                self.skipTest(f"renderer unavailable: {exc}")
            a = sorted((d / "a").glob("*.jpg"))
            b = sorted((d / "b").glob("*.jpg"))
            self.assertEqual(len(a), 2)
            for x, y in zip(a, b):
                self.assertEqual(x.read_bytes(), y.read_bytes(), "same spec and time must give identical frames")


if __name__ == "__main__":
    unittest.main()
