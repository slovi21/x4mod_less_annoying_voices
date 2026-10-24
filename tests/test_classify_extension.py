"""Tests for tools/classify_extension.py.

Run: python -I -m unittest discover -s tests
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def test_non_utf8_catalog_fails_closed(self):
        v, _ = self.verdict({"ext_01.cat": b"voice/\xff.ogg 2 1729500000 " + b"0" * 32 + b"\n", "ext_01.dat": b"ab"})
        self.assertEqual(v, "fails")

    def test_catalog_pair_matches_case_insensitively(self):
        v, _ = self.verdict({"EXT_01.CAT": cat_line("voice/1.ogg", 2).encode(), "ext_01.dat": b"ab"})
        self.assertEqual(v, "qualifies")

    def test_lua_inside_catalog_fails(self):
        cat = cat_line("voice/1.ogg", 2) + cat_line("ui/addons/x/menu.lua", 1)
        v, _ = self.verdict({"ext_01.cat": cat.encode(), "ext_01.dat": b"abc"})
        self.assertEqual(v, "fails")

    def test_linked_folder_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            ext = make_ext(tmp, {"voice/1.ogg": b"x"})
            (Path(tmp) / "elsewhere" / "md").mkdir(parents=True)
            try:
                os.symlink(Path(tmp) / "elsewhere", ext / "linked", target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks not available")
            self.assertEqual(ce.verdict(ce.scan_extension(ext))[0], "fails")

    def test_unreadable_folder_fails_closed(self):
        real_scandir = os.scandir

        def scandir(path="."):
            if Path(path).name == "md":
                raise PermissionError(13, "Access is denied", str(path))
            return real_scandir(path)

        with tempfile.TemporaryDirectory() as tmp:
            ext = make_ext(tmp, {"voice/1.ogg": b"x", "md/evil.xml": b"<mdscript/>"})
            with mock.patch("os.scandir", scandir):
                items = ce.scan_extension(ext)
            self.assertEqual(ce.verdict(items)[0], "fails")


class Main(unittest.TestCase):
    def run_main(self, argv):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return ce.main(argv)

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_main([str(make_ext(Path(tmp) / "a", {"voice/1.ogg": b"x"}))]), 0)
            self.assertEqual(self.run_main([str(make_ext(Path(tmp) / "b", {"t/0001-l044.xml": b"<x/>"}))]), 1)
            self.assertEqual(self.run_main([str(make_ext(Path(tmp) / "c", {"md/x.xml": b"<x/>"}))]), 1)
            self.assertEqual(self.run_main([tmp]), 2)
            self.assertEqual(self.run_main([str(Path(tmp) / "missing")]), 2)


if __name__ == "__main__":
    unittest.main()
