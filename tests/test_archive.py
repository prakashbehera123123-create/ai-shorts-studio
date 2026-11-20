import tempfile
import unittest
from datetime import date
from pathlib import Path

from studio.archive import archive_previous_render, deliver


class ArchiveTests(unittest.TestCase):
    def test_rerender_keeps_old_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp) / "render"
            r.mkdir()
            (r / "draft.mp4").write_bytes(b"v1")
            (r / "captions.srt").write_text("1", encoding="utf-8")
            first = archive_previous_render(r)
            self.assertEqual((first / "draft.mp4").read_bytes(), b"v1")
            self.assertFalse((r / "draft.mp4").exists())
            (r / "draft.mp4").write_bytes(b"v2")
            second = archive_previous_render(r)
            self.assertNotEqual(first, second)  # same-second stamps get a -vN folder, never overwrite
            self.assertEqual((first / "draft.mp4").read_bytes(), b"v1")
            self.assertIsNone(archive_previous_render(r))

    def test_deliver_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "production" / "2026-11-20-x"
            (folder / "render").mkdir(parents=True)
            (folder / "render" / "draft.mp4").write_bytes(b"a")
            (folder / "metadata.md").write_text("m", encoding="utf-8")
            root = Path(tmp) / "final"
            d1 = deliver(folder, root, date(2026, 11, 20))
            d2 = deliver(folder, root, date(2026, 11, 20))
            self.assertEqual(d1, root / "2026-11-20" / "2026-11-20-x")
            self.assertEqual(d2.name, "2026-11-20-x-v2")
            self.assertEqual((d1 / "draft.mp4").read_bytes(), b"a")
            self.assertTrue((d2 / "metadata.md").is_file())


if __name__ == "__main__":
    unittest.main()
