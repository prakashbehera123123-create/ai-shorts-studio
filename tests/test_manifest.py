import tempfile
import unittest
from pathlib import Path

from studio.errors import ContractError
from studio.manifest import COLUMNS, read_manifest, validate_rows, write_empty_manifest


def row(**overrides: str) -> dict[str, str]:
    base = {c: "" for c in COLUMNS}
    base.update(asset_id="A1", filename="a.png", asset_type="generated_graphic", license="internal-generated", attribution_required="no")
    base.update(overrides)
    return base


class ManifestTests(unittest.TestCase):
    def test_valid_generated_row(self) -> None:
        self.assertEqual(validate_rows([row()]), [])

    def test_licensed_stock_requires_source_and_license_url(self) -> None:
        problems = validate_rows([row(asset_type="licensed_stock")])
        self.assertTrue(any("source_url" in p for p in problems))
        self.assertTrue(any("license_url" in p for p in problems))

    def test_attribution_requires_creator(self) -> None:
        self.assertTrue(any("creator" in p for p in validate_rows([row(attribution_required="yes")])))

    def test_unknown_type_and_duplicate_id(self) -> None:
        problems = validate_rows([row(asset_type="youtube_rip"), row()])
        self.assertTrue(any("asset_type" in p for p in problems))
        self.assertTrue(any("duplicate" in p for p in problems))

    def test_empty_manifest_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assets" / "manifest.csv"
            write_empty_manifest(path)
            self.assertEqual(read_manifest(path), [])
            with self.assertRaisesRegex(ContractError, "no assets"):
                read_manifest(path, require_rows=True)

    def test_bad_header_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.csv"
            path.write_text("id,file\n1,a.png\n", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "header"):
                read_manifest(path)


if __name__ == "__main__":
    unittest.main()
