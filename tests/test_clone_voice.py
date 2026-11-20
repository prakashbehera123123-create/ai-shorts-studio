import unittest

from studio.clone_voice import estimate_word_times, fit_tempo
from studio.errors import StudioError


class EstimateWordTimesTests(unittest.TestCase):
    def test_trims_lead_and_tail_silence(self) -> None:
        wt = estimate_word_times(["Hello", "world."], [(0.0, 0.4), (2.6, 3.0)], 3.0)
        self.assertAlmostEqual(wt[0].start, 0.4)
        self.assertAlmostEqual(wt[-1].end, 2.6)

    def test_internal_pause_snaps_to_punctuation(self) -> None:
        words = ["One", "good", "answer.", "It", "fails", "later."]
        wt = estimate_word_times(words, [(1.5, 1.9)], 3.4)
        # pause belongs after "answer."; "It" starts when speech resumes
        self.assertAlmostEqual(wt[2].end, 1.5)
        self.assertAlmostEqual(wt[3].start, 1.9)
        self.assertTrue(all(b.start >= a.start for a, b in zip(wt, wt[1:])))
        self.assertAlmostEqual(wt[-1].end, 3.4)

    def test_longer_words_get_more_time(self) -> None:
        wt = estimate_word_times(["a", "extraordinarily"], [], 2.0)
        self.assertGreater(wt[1].end - wt[1].start, wt[0].end - wt[0].start)

    def test_empty(self) -> None:
        self.assertEqual(estimate_word_times([], [], 1.0), [])


class FitTempoTests(unittest.TestCase):
    def test_no_speedup_when_it_fits(self) -> None:
        self.assertEqual(fit_tempo(50.0, 54.0, 1.12), 1.0)

    def test_gentle_speedup(self) -> None:
        f = fit_tempo(58.0, 54.0, 1.12)
        self.assertTrue(1.07 <= f <= 1.08)

    def test_refuses_extreme_speedup(self) -> None:
        with self.assertRaisesRegex(StudioError, "shorten the script"):
            fit_tempo(70.0, 54.0, 1.12)


class TakeSelectionTests(unittest.TestCase):
    def test_cache_key_changes_with_inputs(self) -> None:
        import tempfile
        from pathlib import Path

        from studio.clone_voice import cache_key

        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "ref.wav"
            ref.write_bytes(b"voice")
            s = {"exaggeration": 0.5, "cfg_weight": 0.3}
            k = cache_key("Hello.", ref, s, 1, "en")
            self.assertEqual(k, cache_key("Hello.", ref, s, 1, "en"))
            self.assertNotEqual(k, cache_key("Hello!", ref, s, 1, "en"))
            self.assertNotEqual(k, cache_key("Hello.", ref, {**s, "cfg_weight": 0.5}, 1, "en"))
            self.assertNotEqual(k, cache_key("Hello.", ref, s, 2, "en"))
            ref.write_bytes(b"new voice")
            self.assertNotEqual(k, cache_key("Hello.", ref, s, 1, "en"))

    def test_pick_takes(self) -> None:
        from studio.clone_voice import pick_takes

        best, weak = pick_takes({1: [70.0, 92.0, 88.0], 2: [95.0], 3: [60.0, 80.0]}, 85.0)
        self.assertEqual(best, {1: 1, 2: 0, 3: 1})
        self.assertEqual(weak, [3])


@unittest.skipUnless(__import__("shutil").which("ffmpeg"), "FFmpeg missing")
class DenoiseIntegrationTests(unittest.TestCase):
    def test_denoise_lowers_background_noise(self) -> None:
        import shutil
        import subprocess
        import tempfile
        from pathlib import Path

        from studio.audio_clean import denoise, noise_profile

        with tempfile.TemporaryDirectory() as tmp:
            noisy = Path(tmp) / "noisy.wav"
            # 'speech' bursts (tone on/off every 0.5 s) over constant pink noise
            subprocess.run([shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
                            "-f", "lavfi", "-i", "sine=f=220:d=4,volume=enable='lt(mod(t,1),0.5)':volume=1,volume=enable='gte(mod(t,1),0.5)':volume=0",
                            "-f", "lavfi", "-i", "anoisesrc=d=4:c=pink:a=0.02",
                            "-filter_complex", "[0][1]amix=inputs=2:normalize=0", "-ar", "24000", str(noisy)], check=True, timeout=60)
            clean = Path(tmp) / "clean.wav"
            denoise(noisy, clean)
            before, after = noise_profile(noisy), noise_profile(clean)
            self.assertLess(after["noise_db"], before["noise_db"] - 6)
            self.assertGreater(after["snr_db"], before["snr_db"])


if __name__ == "__main__":
    unittest.main()
