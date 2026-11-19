import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from studio.config import load_config
from studio.errors import StudioError
from studio.production import create_production, validate_production
from studio.research import load_research_config, select_topics
from studio.shortlist import BACKLOG_HEADER, apply_selection, prior_titles
from tests.research_fixtures import TODAY, candidate, research

CFG = load_config()
RCFG = load_research_config()
NOW = datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)


class ApplySelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.prod = base / "production"
        self.prod.mkdir()
        self.backlog = base / "topic-backlog.md"
        self.backlog.write_text(f"# Topic backlog\n\n{BACKLOG_HEADER}\n|---|---|---|---|---:|---|---|\n", encoding="utf-8")
        self.rfile = base / "research" / "2026-11-20" / "candidates.json"
        self.rfile.parent.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def apply(self, data=None):  # type: ignore[no-untyped-def]
        data = data or research()
        self.rfile.write_text(json.dumps(data), encoding="utf-8")
        decisions = select_topics(data, RCFG, TODAY, prior_titles(self.backlog, self.prod))
        return apply_selection(decisions, [], TODAY, CFG, RCFG, self.rfile, self.backlog, self.prod, NOW)

    def test_creates_valid_folders_with_brief_and_sources(self) -> None:
        summary = self.apply()
        self.assertEqual([s["id"] for s in summary["selected"]], ["C01", "C02"])
        for s in summary["selected"]:
            folder = self.prod / Path(s["folder"]).name
            self.assertEqual(validate_production(folder, CFG), [])
            sources = (folder / "sources.md").read_text(encoding="utf-8")
            self.assertIn("https://example.com/notes", sources)
            self.assertIn("2026-11-18", sources)  # published
            self.assertIn("2026-11-20", sources)  # accessed
            self.assertIn("Weighted score", (folder / "brief.md").read_text(encoding="utf-8"))
            self.assertEqual(json.loads((folder / "status.json").read_text())["status"], "RESEARCHED")

    def test_backlog_records_every_candidate(self) -> None:
        self.apply()
        rows = [ln for ln in self.backlog.read_text(encoding="utf-8").splitlines() if ln.startswith("| 2026-11-20")]
        self.assertEqual(len(rows), 8)
        self.assertEqual(sum("| selected |" in r for r in rows), 2)
        self.assertEqual(sum("| deferred: daily limit |" in r for r in rows), 6)
        # only produced topics block future runs: 2 selected backlog rows + 2 folder slugs
        self.assertEqual(len(prior_titles(self.backlog, self.prod)), 2 + 2)

    def test_report_and_selection_written(self) -> None:
        self.apply()
        report = (self.rfile.parent / "shortlist.md").read_text(encoding="utf-8")
        self.assertIn("SELECTED", report)
        self.assertIn("accessed 2026-11-20", report)
        self.assertTrue((self.rfile.parent / "selection.json").is_file())

    def test_cannot_apply_twice(self) -> None:
        self.apply()
        with self.assertRaisesRegex(StudioError, "already applied"):
            self.apply()

    def test_weak_run_flags_action_needed(self) -> None:
        summary = self.apply(research([candidate(1, score=4), candidate(2, score=1)]))
        self.assertEqual(len(summary["selected"]), 1)
        self.assertIn("Action needed", (self.rfile.parent / "shortlist.md").read_text(encoding="utf-8"))

    def test_daily_limit_checked_before_writing(self) -> None:
        create_production(CFG, TODAY, "existing-one", "x", "English", root=self.prod, now=NOW)
        before = self.backlog.read_text(encoding="utf-8")
        with self.assertRaisesRegex(StudioError, "exceed"):
            self.apply()
        self.assertEqual(self.backlog.read_text(encoding="utf-8"), before)
        self.assertEqual(len(list(self.prod.iterdir())), 1)

    def test_pipe_in_title_does_not_break_table(self) -> None:
        self.apply(research([candidate(1, title="RAG | evals in practice")]))
        row = next(ln for ln in self.backlog.read_text(encoding="utf-8").splitlines() if "RAG" in ln)
        self.assertIn("RAG \\| evals", row)
        self.assertIn("RAG | evals in practice", prior_titles(self.backlog, self.prod))


if __name__ == "__main__":
    unittest.main()
