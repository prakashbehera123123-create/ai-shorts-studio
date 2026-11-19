import csv
import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from studio.config import load_config
from studio.errors import ContractError, StudioError, TransitionError
from studio.manifest import COLUMNS
from studio.production import REQUIRED_FILES, create_production, set_status, validate_production

CFG = load_config()
DAY = date(2026, 11, 20)
NOW = datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)


class ProductionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def new(self, slug: str = "mcp-explained", language: str = "English") -> Path:
        return create_production(CFG, DAY, slug, "MCP explained", language, root=self.root, now=NOW)

    def test_scaffold_has_every_required_file_and_validates(self) -> None:
        folder = self.new()
        self.assertEqual(folder.name, "2026-11-20-mcp-explained")
        for name in REQUIRED_FILES:
            self.assertTrue((folder / name).is_file(), name)
        self.assertTrue((folder / "render").is_dir())
        self.assertEqual(validate_production(folder, CFG), [])

    def test_sources_template_has_required_columns(self) -> None:
        text = (self.new() / "sources.md").read_text(encoding="utf-8")
        for col in ("url", "publisher", "published", "accessed", "claim supported", "confidence"):
            self.assertIn(col, text)

    def test_rejects_bad_slug_language_duplicate_and_daily_limit(self) -> None:
        with self.assertRaises(StudioError):
            self.new("Bad Slug")
        with self.assertRaises(StudioError):
            self.new("ok", language="Hindi")
        self.new("one")
        with self.assertRaisesRegex(StudioError, "exists"):
            self.new("one")
        self.new("two")
        with self.assertRaisesRegex(StudioError, "Daily limit"):
            self.new("three")

    def test_missing_file_reported(self) -> None:
        folder = self.new()
        (folder / "sources.md").unlink()
        self.assertIn("missing sources.md", validate_production(folder, CFG))

    def test_stage_gates_through_full_lifecycle(self) -> None:
        folder = self.new()
        set_status(folder, CFG, "APPROVED_TOPIC", now=NOW)
        with self.assertRaisesRegex(ContractError, "no scenes"):
            set_status(folder, CFG, "SCRIPT_READY", now=NOW)

        sb_path = folder / "storyboard.json"
        sb = json.loads(sb_path.read_text(encoding="utf-8"))
        sb["scenes"] = [{"id": 1, "start_seconds": 0, "end_seconds": 30, "narration": "n", "on_screen_text": "t",
                         "visual_type": "generated_graphic", "source_ids": ["S1"]}]
        sb_path.write_text(json.dumps(sb), encoding="utf-8")
        set_status(folder, CFG, "SCRIPT_READY", now=NOW)

        with self.assertRaisesRegex(ContractError, "no assets"):
            set_status(folder, CFG, "ASSETS_READY", now=NOW)
        with (folder / "assets/manifest.csv").open("a", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow(["A1", "bg.png", "generated_graphic", "", "", "internal-generated", "", "no", ""])
        set_status(folder, CFG, "ASSETS_READY", now=NOW)

        with self.assertRaisesRegex(ContractError, "MP4"):
            set_status(folder, CFG, "RENDERED", now=NOW)
        (folder / "render" / "draft.mp4").write_bytes(b"")
        set_status(folder, CFG, "RENDERED", now=NOW)
        set_status(folder, CFG, "QA_PASSED", now=NOW)
        final = set_status(folder, CFG, "READY_FOR_HUMAN_REVIEW", now=NOW)
        self.assertEqual(final["status"], "READY_FOR_HUMAN_REVIEW")
        self.assertFalse(final["published"])
        self.assertEqual(validate_production(folder, CFG), [])

    def test_cannot_set_published(self) -> None:
        folder = self.new()
        with self.assertRaises(TransitionError):
            set_status(folder, CFG, "PUBLISHED", now=NOW)

    def test_status_left_unchanged_when_gate_fails(self) -> None:
        folder = self.new()
        set_status(folder, CFG, "APPROVED_TOPIC", now=NOW)
        before = (folder / "status.json").read_text(encoding="utf-8")
        with self.assertRaises(ContractError):
            set_status(folder, CFG, "SCRIPT_READY", now=NOW)
        self.assertEqual((folder / "status.json").read_text(encoding="utf-8"), before)

    def test_manifest_header_matches_contract(self) -> None:
        header = (self.new() / "assets/manifest.csv").read_text(encoding="utf-8").splitlines()[0]
        self.assertEqual(tuple(header.split(",")), COLUMNS)


if __name__ == "__main__":
    unittest.main()
