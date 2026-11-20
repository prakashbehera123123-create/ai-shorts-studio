"""File contracts for project skills, agents and the creative storyboard schema."""
import json
import re
import unittest
from pathlib import Path

from studio.config import load_config
from studio.storyboard import validate_storyboard_data

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"
THIRD_PARTY_SKILLS = {"playwright-cli"}
REQUIRED_SECTIONS = ("Purpose", "Inputs", "Workflow", "Tools", "Decision rules", "Outputs", "Quality checklist", "Failure handling")


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    assert m, "missing frontmatter"
    return {k.strip(): v.strip() for k, v in (ln.split(":", 1) for ln in m.group(1).splitlines() if ":" in ln)}


def project_skills() -> list[Path]:
    return sorted(p for p in SKILLS.glob("*/SKILL.md") if p.parent.name not in THIRD_PARTY_SKILLS)


class SkillContractTests(unittest.TestCase):
    def test_every_project_skill_has_the_eight_sections(self) -> None:
        self.assertGreaterEqual(len(project_skills()), 8)
        for path in project_skills():
            text = path.read_text(encoding="utf-8")
            fm = frontmatter(text)
            self.assertEqual(fm.get("name"), path.parent.name, path)
            self.assertGreater(len(fm.get("description", "")), 30, path)
            headings = re.findall(r"^##\s+(.+?)\s*$", text, re.M)
            for section in REQUIRED_SECTIONS:
                self.assertTrue(any(h.startswith(section) for h in headings), f"{path.parent.name}: missing '## {section}'")

    def test_skill_file_references_exist(self) -> None:
        for path in project_skills():
            for ref in re.findall(r"`((?:docs|config|templates|studio|scripts)/[\w./-]+\.\w+)`", path.read_text(encoding="utf-8")):
                self.assertTrue((ROOT / ref).is_file(), f"{path.parent.name} references missing {ref}")

    def test_skills_never_publish(self) -> None:
        for path in project_skills():
            text = path.read_text(encoding="utf-8").lower()
            self.assertNotRegex(text, r"\b(publish|upload) (it|the video|to youtube) (now|automatically)\b", path)

    def test_creative_docs_exist(self) -> None:
        for doc in ("docs/REFERENCE_VIDEO_ANALYSIS.md", "docs/CREATIVE_PRODUCTION_STANDARD.md",
                    "templates/production-readiness-checklist.md", "templates/storyboard.example.json"):
            self.assertTrue((ROOT / doc).is_file(), doc)


class CreativeStoryboardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_config()
        self.board = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))

    def test_template_is_valid_v2(self) -> None:
        self.assertEqual(self.board.get("schema_version"), 2)
        self.assertEqual(validate_storyboard_data(self.board, self.cfg, require_scenes=True), [])

    def test_v2_requires_creative_keys_and_structure(self) -> None:
        scene = self.board["scenes"][0]
        del scene["beat"]
        joined = " ".join(validate_storyboard_data(self.board, self.cfg))
        self.assertIn("missing creative keys", joined)

    def test_v2_rejects_bad_enums_and_unjustified_3d(self) -> None:
        s = self.board["scenes"][1]
        s["visual_form"], s["transition_in"] = "scene_3d", "star_wipe"
        s.pop("visual_justification", None)
        joined = " ".join(validate_storyboard_data(self.board, self.cfg))
        self.assertIn("transition_in", joined)
        self.assertIn("visual_justification", joined)

    def test_v2_hook_must_be_short(self) -> None:
        self.board["scenes"][0]["end_seconds"] = 4.0
        self.board["scenes"][1]["start_seconds"] = 4.0
        self.assertIn("hook scene is longer", " ".join(validate_storyboard_data(self.board, self.cfg)))

    def test_v2_central_question_fits_overlay(self) -> None:
        self.board.setdefault("creative", {})["central_question"] = "How? " * 20
        self.assertIn("central_question", " ".join(validate_storyboard_data(self.board, self.cfg)))
        self.board["creative"]["central_question"] = "How should an agent wait for feedback without polling?"
        self.assertNotIn("central_question", " ".join(validate_storyboard_data(self.board, self.cfg)))

    def test_v1_storyboards_still_valid(self) -> None:
        v1 = {"video_id": "x", "language": "English", "target_duration_seconds": 40, "format": "9:16", "scenes": []}
        self.assertEqual(validate_storyboard_data(v1, self.cfg), [])


if __name__ == "__main__":
    unittest.main()
