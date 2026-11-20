import ast
import tempfile
import unittest
from pathlib import Path

from studio.metadata import DISCLOSURE_VOICE, build_metadata, metadata_problems
from studio.qa import caption_problems, editorial_problems, parse_editorial, parse_loudness, parse_silences, parse_srt
from tests.script_fixtures import write_valid

ROOT = Path(__file__).resolve().parents[1]

EBUR = """[Parsed_ebur128_0 @ 0x1] Summary:

  Integrated loudness:
    I:         -16.4 LUFS
    Threshold: -26.6 LUFS

  True peak:
    Peak:       -4.4 dBFS
"""


class ParserTests(unittest.TestCase):
    def test_loudness(self) -> None:
        self.assertEqual(parse_loudness(EBUR), (-16.4, -4.4))

    def test_silences(self) -> None:
        self.assertEqual(parse_silences("silence_end: 12.1 | silence_duration: 1.9\n"), [1.9])

    def test_srt_and_caption_coverage(self) -> None:
        srt = "1\n00:00:00,000 --> 00:00:01,000\nHello there\n\n2\n00:00:01,000 --> 00:00:02,000\nGeneral\n"
        cues = parse_srt(srt)
        self.assertEqual(cues[1], (1.0, 2.0, "General"))
        self.assertEqual(caption_problems(cues, 2.0), ([], []))
        errs, _ = caption_problems(cues, 5.0)
        self.assertTrue(any("video is 5.0s" in e for e in errs))
        # short pauses between word-timed cues are fine; long holes and late starts are not
        self.assertEqual(caption_problems([(0.08, 1.0, "a b"), (1.3, 2.0, "c d")], 2.0)[0], [])
        errs, _ = caption_problems([(0.5, 1.0, "a b"), (2.5, 3.0, "c d")], 3.0)
        self.assertTrue(any("start" in e for e in errs) and any("gap" in e for e in errs))
        _, warns = caption_problems([(0.0, 0.3, "x"), (0.3, 1.0, "a" * 40)], 1.0)
        self.assertEqual(len(warns), 2)

    def test_editorial_parsing(self) -> None:
        text = "Decision: FAIL\n\n## Blockers\n- caption typo in scene 3\n\n## Warnings\n- none\n"
        self.assertEqual(parse_editorial(text), ("FAIL", ["caption typo in scene 3"], []))
        self.assertEqual(parse_editorial("Decision: PASS\n## Blockers\n- none\n")[:2], ("PASS", []))
        explained = "Decision: FAIL\n## Blockers\n- None. Checked: factual overstatement (none), captions ok.\n"
        self.assertEqual(parse_editorial(explained)[:2], ("FAIL", []))
        self.assertEqual(parse_editorial("Decision: FAIL\n## Blockers\n- nonexistent source cited\n")[1], ["nonexistent source cited"])


class MetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name) / "2026-11-20-demo"
        (self.folder / "assets").mkdir(parents=True)
        write_valid(self.folder)
        (self.folder / "brief.md").write_text("# Brief\n- Bucket: developer-workflows\n", encoding="utf-8")
        (self.folder / "assets" / "manifest.csv").write_text(
            "asset_id,filename,asset_type,source_url,creator,license,license_url,attribution_required,notes\n"
            "V001,voiceover/narration.wav,generated_audio,,Windows SAPI,local TTS,,no,placeholder\n", encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_generated_metadata_passes_and_discloses_voice(self) -> None:
        (self.folder / "metadata.md").write_text(build_metadata(self.folder), encoding="utf-8")
        self.assertEqual(metadata_problems(self.folder), [])
        self.assertIn(DISCLOSURE_VOICE, (self.folder / "metadata.md").read_text(encoding="utf-8"))
        self.assertIn("https://example.com/a", (self.folder / "metadata.md").read_text(encoding="utf-8"))

    def test_cloned_voice_gets_specific_disclosure(self) -> None:
        from studio.metadata import DISCLOSURE_CLONE

        (self.folder / "assets" / "manifest.csv").write_text(
            "asset_id,filename,asset_type,source_url,creator,license,license_url,attribution_required,notes\n"
            "V001,voiceover/narration.wav,generated_audio,,Chatterbox,MIT,,no,AI-cloned narration of the owner's voice\n", encoding="utf-8")
        (self.folder / "metadata.md").write_text(build_metadata(self.folder), encoding="utf-8")
        self.assertIn(DISCLOSURE_CLONE, (self.folder / "metadata.md").read_text(encoding="utf-8"))
        self.assertEqual(metadata_problems(self.folder), [])

    def test_missing_source_and_hype_detected(self) -> None:
        text = build_metadata(self.folder).replace("https://example.com/a", "")
        text = text.replace("## Title\n", "## Title\nThis INSANE trick ")
        (self.folder / "metadata.md").write_text(text, encoding="utf-8")
        joined = " ".join(metadata_problems(self.folder))
        self.assertIn("missing source URL", joined)
        self.assertIn("hype", joined)

    def test_folder_slug_title_rejected(self) -> None:
        import re

        text = build_metadata(self.folder)
        text = re.sub(r"## Title\n[^\n]*", "## Title\n2026-11-20-some-topic-slug", text, count=1)
        (self.folder / "metadata.md").write_text(text, encoding="utf-8")
        self.assertIn("folder slug", " ".join(metadata_problems(self.folder)))

    def test_editorial_required(self) -> None:
        self.assertIn("missing qa/editorial.md", editorial_problems(self.folder)[0])


class NoPublishGuardTests(unittest.TestCase):
    """The pipeline must have no path to upload or publish anything."""

    FORBIDDEN_IMPORTS = {"requests", "httpx", "urllib.request", "http.client", "googleapiclient", "google_auth_oauthlib", "aiohttp"}

    def test_no_network_or_youtube_client_imports(self) -> None:
        for py in (ROOT / "studio").glob("*.py"):
            tree = ast.parse(py.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for n in names:
                    self.assertNotIn(n, self.FORBIDDEN_IMPORTS, f"{py.name} imports {n}")

    def test_no_upload_endpoints_in_code(self) -> None:
        for py in [*(ROOT / "studio").glob("*.py"), *(ROOT / "scripts").glob("*.py")]:
            text = py.read_text(encoding="utf-8").lower()
            for needle in ("youtube/v3", "upload.youtube", "videos.insert", "youtube.googleapis"):
                self.assertNotIn(needle, text, f"{py.name} contains {needle}")


if __name__ == "__main__":
    unittest.main()
