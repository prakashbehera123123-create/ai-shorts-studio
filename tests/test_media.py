import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from studio.config import load_config
from studio.errors import MediaToolError
from studio.media import check_summary, run_ffprobe, summarize

CFG = load_config()


def probe_json(width: int = 1080, height: int = 1920, vcodec: str = "h264",
               acodec: str | None = "aac", duration: str = "40.0") -> dict:
    streams: list[dict] = [{"codec_type": "video", "codec_name": vcodec, "width": width, "height": height}]
    if acodec:
        streams.append({"codec_type": "audio", "codec_name": acodec})
    return {"streams": streams, "format": {"duration": duration}}


class MediaSummaryTests(unittest.TestCase):
    def test_valid_short_passes(self) -> None:
        self.assertEqual(check_summary(summarize(probe_json()), CFG), [])

    def test_each_violation_reported(self) -> None:
        joined = " ".join(check_summary(summarize(probe_json(1920, 1080, "hevc", None, "70")), CFG))
        for needle in ("1080x1920", "video codec", "No audio", "Duration"):
            self.assertIn(needle, joined)

    def test_bad_duration_field_does_not_crash(self) -> None:
        self.assertEqual(summarize(probe_json(duration="N/A"))["duration_seconds"], 0.0)

    def test_missing_file(self) -> None:
        with self.assertRaises(MediaToolError):
            run_ffprobe(Path("no-such-file.mp4"))


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg not installed")
class MediaIntegrationTests(unittest.TestCase):
    def test_probe_tiny_generated_clip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "t.mp4"
            cmd = [shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
                   "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=1:r=30",
                   "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                   "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(out)]
            subprocess.run(cmd, check=True, timeout=120, capture_output=True)
            summary = summarize(run_ffprobe(out))
            self.assertEqual((summary["width"], summary["height"]), (1080, 1920))
            self.assertEqual((summary["video_codec"], summary["audio_codec"]), ("h264", "aac"))
            errors = check_summary(summary, CFG)
            self.assertEqual(len(errors), 1)
            self.assertIn("Duration", errors[0])


if __name__ == "__main__":
    unittest.main()
