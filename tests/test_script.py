import json
import tempfile
import unittest
from pathlib import Path

from studio.config import load_config
from studio.script import check_fact_check, check_language, check_script, script_gate_problems
from tests.script_fixtures import FACT_CHECK, NARRATION, SPOKEN, storyboard, write_valid, script_md

CFG = load_config()


class ScriptCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name) / "2026-11-20-demo"
        self.folder.mkdir()
        write_valid(self.folder)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def rewrite(self, **kw: str) -> None:
        (self.folder / "script.md").write_text(script_md(**kw), encoding="utf-8")

    def test_valid_fixture_passes(self) -> None:
        rep = check_script(self.folder, CFG)
        self.assertEqual(rep.errors, [])
        self.assertTrue(CFG.min_words <= rep.spoken_words <= CFG.max_words)
        self.assertTrue(CFG.min_duration <= rep.estimated_seconds <= CFG.max_duration)
        self.assertEqual(script_gate_problems(self.folder, CFG), [])

    def test_too_short_script(self) -> None:
        self.rewrite(narration="Too short.")
        joined = " ".join(check_script(self.folder, CFG).errors)
        self.assertIn("spoken words", joined)

    def test_missing_section(self) -> None:
        (self.folder / "script.md").write_text("Language: English\n## Hook\nhi\n", encoding="utf-8")
        self.assertIn("sections missing", check_script(self.folder, CFG).errors[0])

    def test_unmapped_number_rejected(self) -> None:
        self.rewrite(narration=NARRATION + " It cut failures by 73 percent.")
        self.assertTrue(any("'73'" in e for e in check_script(self.folder, CFG).errors))

    def test_mapped_number_allowed(self) -> None:
        narration = NARRATION.replace("small set", "set of 5")
        self.rewrite(narration=narration, claims="| K1 | Use 5 cases | S1 | fact |")
        spoken = SPOKEN.replace("small set", "set of 5")
        (self.folder / "storyboard.json").write_text(json.dumps(storyboard(self.folder.name, spoken)), encoding="utf-8")
        self.assertEqual(check_script(self.folder, CFG).errors, [])

    def test_unknown_source_and_bad_type(self) -> None:
        self.rewrite(claims="| K1 | x | S9 | rumour |")
        joined = " ".join(check_script(self.folder, CFG).errors)
        self.assertIn("S9", joined)
        self.assertIn("type", joined)

    def test_storyboard_must_match_spoken_text(self) -> None:
        board = storyboard(self.folder.name, SPOKEN.replace("habit", "trick"))
        (self.folder / "storyboard.json").write_text(json.dumps(board), encoding="utf-8")
        self.assertTrue(any("differs" in e for e in check_script(self.folder, CFG).errors))

    def test_scene_pace_too_fast(self) -> None:
        board = storyboard(self.folder.name, total=30.0)
        (self.folder / "storyboard.json").write_text(json.dumps(board), encoding="utf-8")
        self.assertTrue(any("wpm" in e for e in check_script(self.folder, CFG).errors))

    def test_language_mismatch_between_files(self) -> None:
        board = storyboard(self.folder.name, language="Hinglish")
        (self.folder / "storyboard.json").write_text(json.dumps(board), encoding="utf-8")
        self.assertTrue(any("language" in e for e in check_script(self.folder, CFG).errors))


class LanguageTests(unittest.TestCase):
    def test_english_with_hinglish_rejected(self) -> None:
        self.assertTrue(check_language("Yeh tool kya hai aur kaise kaam karta hai", "English"))

    def test_clean_english_passes(self) -> None:
        self.assertEqual(check_language("This tool runs evals before and after a change", "English"), [])

    def test_hinglish_must_have_hindi_words(self) -> None:
        self.assertTrue(check_language("This tool runs evals before and after a change", "Hinglish"))
        self.assertEqual(check_language("Yeh tool evals chalata hai, aur change ke baad compare karta hai", "Hinglish"), [])

    def test_devanagari_rejected(self) -> None:
        self.assertTrue(check_language("यह tool", "Hinglish"))


class FactCheckTests(unittest.TestCase):
    def test_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.assertEqual(check_fact_check(folder, ["K1"]), ["missing fact_check.md"])
            (folder / "fact_check.md").write_text(FACT_CHECK, encoding="utf-8")
            self.assertEqual(check_fact_check(folder, ["K1"]), [])
            self.assertIn("no verdict for claim K2", check_fact_check(folder, ["K1", "K2"])[0])
            (folder / "fact_check.md").write_text(FACT_CHECK.replace("supported", "unsupported"), encoding="utf-8")
            self.assertIn("unsupported", check_fact_check(folder, ["K1"])[0])


if __name__ == "__main__":
    unittest.main()
