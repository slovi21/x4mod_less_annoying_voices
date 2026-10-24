"""Tests for tools/classify_extension.py.

Run: python -I -m unittest discover -s tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import classify_extension as ce  # noqa: E402


def make_ext(root, files):
    """Creates an extension folder with content.xml plus the given {relative path: bytes} files."""
    ext = Path(root) / "ext"
    for rel, data in {"content.xml": b"<content/>", **files}.items():
        p = ext / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    return ext


def cat_line(path, size):
    return f"{path} {size} 1729500000 {'0' * 32}\n"


class ClassifyPath(unittest.TestCase):
    def cls(self, rel):
        return ce.classify(ce.normalize(rel))

    def test_audio(self):
        self.assertEqual(self.cls("libraries/sound_library.xml"), "audio")
        self.assertEqual(self.cls("Libraries\\Sound_Library.XML"), "audio")
        self.assertEqual(self.cls("voice/10201/normal/10201001.ogg"), "audio")

    def test_gameplay_and_unknown(self):
        for rel in ("md/x.xml", "aiscripts/x.xml", "libraries/wares.xml", "index/macros.xml",
                    "assets/units/size_s/macros/ship_macro.xml", "assets/x.xmf", "textures/x.gz", "readme"):
            self.assertEqual(self.cls(rel), "other", rel)

    def test_windows_trailing_dots_and_spaces_are_stripped(self):
        self.assertEqual(self.cls("md/x.xml."), "other")
        self.assertEqual(self.cls("md/x.xml . "), "other")
        self.assertEqual(self.cls("voice/a.ogg."), "audio")

    def test_code(self):
        self.assertEqual(self.cls("ui/addons/x.xml"), "ui_code")
        self.assertEqual(self.cls("ui/icons/x.dds"), "ui_code")
        self.assertEqual(self.cls("anything/x.lua"), "ui_code")

    def test_candidates(self):
        self.assertEqual(self.cls("t/0001-l044.xml"), "candidate_text")
        self.assertEqual(self.cls("t/sub/0001-l044.xml"), "other")
        self.assertEqual(self.cls("assets/textures/hull.dds"), "candidate_texture")
        self.assertEqual(self.cls("assets/fx/dust.dds"), "other")

    def test_documentation_only_at_root(self):
        self.assertEqual(self.cls("readme.txt"), "documentation")
        self.assertEqual(self.cls("md/readme.txt"), "other")

    def test_unsafe_paths_are_invalid(self):
        for rel in ("../md/x.xml", "voice/../md/x.ogg", "/abs/x.ogg", "C:/x.ogg", "voice/a.ogg:stream", "voice/.../a.ogg"):
            self.assertEqual(self.cls(rel), "invalid", rel)


class ScanExtension(unittest.TestCase):
    def verdict(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            items = ce.scan_extension(make_ext(tmp, files))
            return ce.verdict(items)[0], items

    def test_this_mod_layout_qualifies(self):
        v, _ = self.verdict({"libraries/sound_library.xml": b"<diff/>", "voice/10201/normal/10201001.ogg": b"x"})
        self.assertEqual(v, "qualifies")

    def test_one_gameplay_file_fails(self):
        v, _ = self.verdict({"libraries/sound_library.xml": b"<diff/>", "md/x.xml": b"<mdscript/>"})
        self.assertEqual(v, "fails")

    def test_candidates_are_reported_separately(self):
        v, _ = self.verdict({"t/0001-l044.xml": b"<language/>"})
        self.assertEqual(v, "candidates")

    def test_only_metadata_fails(self):
        v, _ = self.verdict({"readme.txt": b"hi"})
        self.assertEqual(v, "fails")

    def test_catalog_entries_are_classified(self):
        cat = cat_line("libraries/sound_library.xml", 3) + cat_line("md/some file.xml", 2)
        v, items = self.verdict({"ext_01.cat": cat.encode(), "ext_01.dat": b"abcde"})
        self.assertEqual(v, "fails")
        self.assertIn("other", [c for _, c in items])

    def test_catalog_audio_only_qualifies(self):
        cat = cat_line("libraries/sound_library.xml", 3) + cat_line("voice/10201/normal/1.ogg", 2)
        v, _ = self.verdict({"ext_01.cat": cat.encode(), "ext_01.dat": b"abcde"})
        self.assertEqual(v, "qualifies")

    def test_malformed_catalog_line_fails_closed(self):
        cat = cat_line("voice/1.ogg", 2) + "garbage line\n"
        v, _ = self.verdict({"ext_01.cat": cat.encode(), "ext_01.dat": b"ab"})
        self.assertEqual(v, "fails")

    def test_dat_size_mismatch_fails_closed(self):
        v, _ = self.verdict({"ext_01.cat": cat_line("voice/1.ogg", 2).encode(), "ext_01.dat": b"abc"})
        self.assertEqual(v, "fails")

    def test_orphan_dat_fails_closed(self):
        v, _ = self.verdict({"voice/1.ogg": b"x", "ext_02.dat": b"abc"})
        self.assertEqual(v, "fails")

    def test_missing_content_xml_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(ce.main([tmp]), 2)
            self.assertEqual(ce.main([str(Path(tmp) / "missing")]), 2)


if __name__ == "__main__":
    unittest.main()
