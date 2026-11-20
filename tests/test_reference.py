import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from studio.reference import change_times, frame_differences, shot_stats, slug, speech_stats

SRT = "1\n00:00:00,500 --> 00:00:02,500\nEver wondered how this works?\n\n2\n00:00:02,500 --> 00:00:04,500\nHere is the answer.\n"


class ReferenceParsingTests(unittest.TestCase):
    def test_slug_is_ascii_and_short(self) -> None:
        self.assertEqual(slug("Full Video Neeche Hai 👇 #systemdesign_1080p.mp4"), "full-video-neeche-hai-systemdesign-1080p")

    def test_shot_stats(self) -> None:
        s = shot_stats([2.0, 5.0, 12.0], 20.0)
        self.assertEqual((s["shots"], s["cuts"], s["cuts_first_10s"]), (4, 3, 2))
        self.assertEqual(s["longest_shot_s"], 8.0)

    def test_speech_stats(self) -> None:
        s = speech_stats(SRT)
        self.assertEqual(s["transcript_words"], 9)
        self.assertEqual(s["first_speech_at_s"], 0.5)
        self.assertEqual(s["words_per_minute"], 135)

    def test_change_times_peaks_and_spacing(self) -> None:
        diffs = [0, 30, 0] + [5] * 10 + [40, 45, 5] + [5] * 10 + [20, 5]
        times = change_times(diffs)
        self.assertEqual(len(times), 2)  # start-up spike ignored; adjacent peaks merged
        self.assertAlmostEqual(times[0], (14 - 1) / 4)

    def test_no_changes_in_flat_signal(self) -> None:
        self.assertEqual(change_times([5.0] * 40), [])


@unittest.skipUnless(shutil.which("ffmpeg"), "FFmpeg not installed")
class FrameDifferenceIntegrationTests(unittest.TestCase):
    def test_detects_hard_cut_between_black_and_white(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "cut.mp4"
            subprocess.run([shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
                            "-f", "lavfi", "-i", "color=c=black:s=320x568:d=3:r=30",
                            "-f", "lavfi", "-i", "color=c=white:s=320x568:d=3:r=30",
                            "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", str(out)], check=True, timeout=60)
            times = change_times(frame_differences(out))
            self.assertEqual(len(times), 1)
            self.assertAlmostEqual(times[0], 3.0, delta=0.5)


if __name__ == "__main__":
    unittest.main()
