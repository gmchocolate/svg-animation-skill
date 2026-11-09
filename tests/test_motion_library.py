"""Offline integration tests for the user's private motion reference library."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "svg-animation" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from motion_library import (  # noqa: E402
    InputError, add_reference, feedback, inspect_svg, load_index,
    prepare, remove_reference, select_references,
)

VALID_SVG = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100">
<title>Sample</title><style>@keyframes move {to {opacity: .5}}
@media (prefers-reduced-motion: reduce) { * { animation: none; } }</style>
<path d="M0 0 H100"/></svg>'''


class MotionLibraryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / "private"
        self.source = self.root / "source.svg"
        self.source.write_bytes(VALID_SVG)

    def test_add_select_prepare_and_remove(self):
        saved = add_reference(self.home, self.source, title="Quiet path",
                              use_cases=["hero"], tags=["subtle"],
                              likes=["progressive drawing"], rating=5)
        self.assertTrue(Path(saved["absolute_path"]).is_file())
        self.assertNotEqual(str(self.source), saved["absolute_path"])
        self.assertEqual(saved["media_type"], "svg")
        selected = select_references(self.home, use_case="hero", tags=["subtle"])
        self.assertEqual(selected[0]["id"], saved["id"])
        manifest = prepare(self.home, request="Draw a hero", use_case="hero",
                           tags=["subtle"], top=2)
        self.assertTrue(manifest["must_open_media"])
        self.assertEqual(len(manifest["references"]), 1)
        changed = feedback(self.home, saved["id"], rating=4,
                           likes=["settles into a resting state"],
                           avoids=["copy logo"])
        self.assertIn("copy logo", changed["avoid_copying"])
        removed = remove_reference(self.home, saved["id"])
        self.assertEqual(removed["removed"], saved["id"])
        self.assertFalse(Path(saved["absolute_path"]).exists())
        self.assertEqual(load_index(self.home)["references"], [])

    def test_duplicate_merges_metadata(self):
        first = add_reference(self.home, self.source, tags=["calm"])
        second = add_reference(self.home, self.source, tags=["hero"], rating=5)
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(len(load_index(self.home)["references"]), 1)
        self.assertEqual(second["tags"], ["calm", "hero"])
        self.assertEqual(second["rating"], 5)

    def test_low_rated_references_do_not_auto_select(self):
        add_reference(self.home, self.source, rating=1)
        self.assertEqual(select_references(self.home), [])

    def test_empty_library_does_not_claim_visual_inspection(self):
        result = prepare(self.home, request="anything", use_case="hero", tags=[], top=2)
        self.assertEqual(result["references"], [])
        self.assertTrue(result["warnings"])
        self.assertTrue(result["must_open_media"])

    def test_reject_active_svg(self):
        for payload in [
            b'<svg><script>alert(1)</script></svg>',
            b'<svg onload="alert(1)"/>',
            b'<svg><foreignObject/></svg>',
            b'<svg><image href="https://example.com/a.png"/></svg>',
            b'<!DOCTYPE svg [<!ENTITY x "y">]><svg/>',
            b'<svg><style>@import url(https://example.com/a.css);</style></svg>',
        ]:
            with self.subTest(payload=payload):
                with self.assertRaises(InputError):
                    inspect_svg(payload)

    def test_reject_wrong_media_and_bad_magic(self):
        bogus = self.root / "bad.mp4"
        bogus.write_bytes(b"not a video")
        with self.assertRaises(InputError):
            add_reference(self.home, bogus)
        another = self.root / "bad.exe"
        another.write_bytes(b"any")
        with self.assertRaises(InputError):
            add_reference(self.home, another)

    def test_lottie_json_supported_as_data(self):
        item = self.root / "lottie.json"
        item.write_text(json.dumps({"v": "5.0", "layers": []}))
        saved = add_reference(self.home, item)
        self.assertEqual(saved["media_type"], "lottie-json")
        self.assertTrue(Path(saved["absolute_path"]).is_file())

    def test_safe_media_rejects_path_escape(self):
        saved = add_reference(self.home, self.source)
        index = load_index(self.home)
        index["references"][0]["media_path"] = "../../outside.svg"
        (self.home / "index.json").write_text(json.dumps(index))
        with self.assertRaises(InputError):
            select_references(self.home)

    def test_max_selection_three(self):
        with self.assertRaises(InputError):
            select_references(self.home, top=4)


if __name__ == "__main__":
    unittest.main()
