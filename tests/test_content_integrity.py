import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXPECTED_PAGES = {
    "Concepts/machine-learning/cnn.md",
    "Concepts/agents/how-agents-work.md",
    "Concepts/agents/recursive-self-improvement.md",
    "Papers/machine-learning-driven-impact-resistance.md",
    "Papers/machine-learning-enabled-materials-design.md",
}


def public_markdown_files():
    return [
        path
        for path in DOCS.rglob("*.md")
        if "superpowers" not in path.relative_to(DOCS).parts
    ]


class ContentIntegrityTests(unittest.TestCase):
    def test_topic_indexes_exist(self):
        topic_indexes = [
            "PhD Journey/index.md",
            "Courses/index.md",
            "Courses/chemical-engineering-mathematics/index.md",
            "Papers/index.md",
            "Concepts/index.md",
            "Tools/index.md",
        ]
        for relative_path in topic_indexes:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((DOCS / relative_path).is_file())

    def test_project_docs_are_excluded_from_site(self):
        site = ROOT / "site"
        self.assertTrue(site.is_dir(), "Run mkdocs build --strict before content tests")
        self.assertFalse((site / "superpowers").exists())

    def test_expected_notes_were_migrated(self):
        actual = {path.relative_to(DOCS).as_posix() for path in public_markdown_files()}
        self.assertTrue(EXPECTED_PAGES <= actual)

    def test_retired_public_sections_absent(self):
        for section in ("AI", "Bai Lab", "TDP Dataset", "Physical Intelligence", "Crypto"):
            with self.subTest(section=section):
                self.assertFalse((DOCS / section).exists())
                self.assertFalse((ROOT / "site" / section).exists())

    def test_public_boundary(self):
        for path in public_markdown_files():
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("# Bai Lab Meeting", content)
                self.assertNotIn("Kai Li's focus", content)

    def test_homepage_icons_render_as_svg(self):
        home = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        cards = re.search(r'<div class="grid cards">(.*?)</div>', home, re.DOTALL)
        self.assertIsNotNone(cards)
        self.assertIn('class="twemoji"', cards.group(1))
        self.assertNotRegex(cards.group(1), r":material-[\w-]+:")

    def test_every_public_page_has_h1(self):
        for path in public_markdown_files():
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"(?m)^# .+")

    def test_no_obsidian_embeds_remain(self):
        for path in public_markdown_files():
            with self.subTest(path=path):
                self.assertNotIn("![[", path.read_text(encoding="utf-8"))

    def test_local_images_exist_inside_docs(self):
        pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
        docs_root = DOCS.resolve()
        for path in public_markdown_files():
            text = path.read_text(encoding="utf-8")
            for raw_target in pattern.findall(text):
                target = raw_target.strip().strip("<>").split(" ", 1)[0]
                if target.startswith(("http://", "https://", "data:")):
                    continue
                resolved = (path.parent / target).resolve()
                with self.subTest(path=path, target=target):
                    self.assertTrue(resolved.is_relative_to(docs_root))
                    self.assertTrue(resolved.is_file())

    def test_local_links_resolve_to_source_files(self):
        pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
        for path in public_markdown_files():
            text = path.read_text(encoding="utf-8")
            for raw_target in pattern.findall(text):
                target = raw_target.strip()
                if target.startswith("<") and ">" in target:
                    target = target[1 : target.index(">")]
                else:
                    target = target.split(" ", 1)[0]
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = target.split("#", 1)[0]
                resolved = (path.parent / target).resolve()
                with self.subTest(path=path, target=target):
                    self.assertTrue(resolved.is_file())


if __name__ == "__main__":
    unittest.main()
