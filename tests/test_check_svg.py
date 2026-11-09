"""Standalone SVG linting smoke tests."""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "svg-animation" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from check_svg import check_file  # noqa: E402


class SVGCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "test.svg"

    def test_sample_passes_strict(self):
        example = Path(__file__).resolve().parents[1] / "skills" / "svg-animation" / "examples" / "line-draw.svg"
        result = check_file(example)
        self.assertTrue(result["ok"])
        self.assertEqual(result["warnings"], [])

    def test_missing_metadata_warns(self):
        self.path.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></svg>')
        result = check_file(self.path)
        self.assertTrue(result["ok"])
        self.assertGreaterEqual(len(result["warnings"]), 2)

    def test_script_is_error(self):
        self.path.write_text("<svg><script>bad()</script></svg>")
        result = check_file(self.path)
        self.assertFalse(result["ok"])
        self.assertTrue(result["errors"])

    def test_duplicate_id_warning(self):
        self.path.write_text('<svg viewBox="0 0 10 10" aria-hidden="true"><circle id="a"/><circle id="a"/></svg>')
        result = check_file(self.path)
        self.assertTrue(result["ok"])
        self.assertIn("Duplicate SVG IDs", result["warnings"][0])


if __name__ == "__main__":
    unittest.main()
