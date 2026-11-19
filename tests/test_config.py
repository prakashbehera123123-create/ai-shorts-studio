import json
import tempfile
import unittest
from pathlib import Path

from studio.config import DEFAULT_CONFIG_PATH, load_config
from studio.errors import ConfigError


class ConfigTests(unittest.TestCase):
    def test_project_config_matches_production_target(self) -> None:
        cfg = load_config()
        self.assertEqual((cfg.width, cfg.height), (1080, 1920))
        self.assertEqual((cfg.video_codec, cfg.audio_codec), ("h264", "aac"))
        self.assertEqual((cfg.min_duration, cfg.max_duration), (25, 55))
        self.assertEqual(cfg.languages, ("English", "Hinglish"))
        self.assertEqual(cfg.max_videos_per_day, 2)

    def _write(self, data: object) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, tmp)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink)
        return Path(tmp.name)

    def test_missing_file_raises(self) -> None:
        with self.assertRaises(ConfigError):
            load_config(Path("does-not-exist.json"))

    def test_missing_key_raises(self) -> None:
        with self.assertRaisesRegex(ConfigError, "video.width"):
            load_config(self._write({"video": {}}))

    def test_horizontal_video_rejected(self) -> None:
        base = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
        base["video"]["width"], base["video"]["height"] = 1920, 1080
        with self.assertRaisesRegex(ConfigError, "vertical"):
            load_config(self._write(base))


if __name__ == "__main__":
    unittest.main()
