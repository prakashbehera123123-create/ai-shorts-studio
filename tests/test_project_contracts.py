import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    assert match, f"{path} has no frontmatter"
    pairs = (line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
    return {k.strip(): v.strip() for k, v in pairs}


class ProjectContractTests(unittest.TestCase):
    def test_required_project_files_exist(self) -> None:
        required = [
            "CLAUDE.md",
            "config/channel-brand.md",
            "config/content-strategy.md",
            "config/production.json",
            ".claude/skills/produce-daily-shorts/SKILL.md",
            ".claude/agents/research-analyst.md",
            "scripts/validate_video.py",
            "templates/status.example.json",
            "templates/storyboard.example.json",
            "templates/assets-manifest.example.csv",
        ]
        for item in required:
            self.assertTrue((ROOT / item).is_file(), item)

    def test_no_publish_automation_command_exists(self) -> None:
        # Publishing is intentionally manual.
        skills = list((ROOT / ".claude" / "skills").glob("**/SKILL.md"))
        text = "\n".join(p.read_text(encoding="utf-8") for p in skills).lower()
        self.assertTrue("never publish" in text or "never upload" in text)

    def test_cli_has_no_publish_or_upload_command(self) -> None:
        from studio.__main__ import build_parser

        sub = next(a for a in build_parser()._actions if a.dest == "command")
        for name in sub.choices:  # type: ignore[union-attr]
            self.assertNotRegex(name, r"publish|upload|schedule")

    def test_main_session_and_agents_never_default_to_opus(self) -> None:
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(settings.get("model"), "sonnet")
        for agent in (ROOT / ".claude" / "agents").glob("*.md"):
            model = frontmatter(agent).get("model", "")
            self.assertIn(model, {"haiku", "sonnet"}, f"{agent.name} uses '{model}'")

    def test_example_templates_are_valid(self) -> None:
        from studio.config import load_config
        from studio.manifest import read_manifest
        from studio.status import validate_status_data
        from studio.storyboard import validate_storyboard_data

        cfg = load_config()
        status = json.loads((ROOT / "templates/status.example.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_status_data(status), [])
        storyboard = json.loads((ROOT / "templates/storyboard.example.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_storyboard_data(storyboard, cfg), [])
        self.assertEqual(len(read_manifest(ROOT / "templates/assets-manifest.example.csv")), 1)


if __name__ == "__main__":
    unittest.main()
