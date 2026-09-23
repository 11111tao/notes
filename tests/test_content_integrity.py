import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXPECTED_PAGES = {
    "AI/Frameworks/cnn.md",
    "AI/Harness/how-agents-work.md",
    "AI/RSI/recursive-self-improvement.md",
    "Bai Lab/meeting-0920.md",
    "Bai Lab/mission-001-read-articles.md",
    "Crypto/diary-001.md",
    "Physical Intelligence/pi0.md",
    "TDP Dataset/0902-report-preparation.md",
}


def public_markdown_files():
    return [
        path
        for path in DOCS.rglob("*.md")
        if "superpowers" not in path.relative_to(DOCS).parts
    ]


class ContentIntegrityTests(unittest.TestCase):
    def test_expected_notes_were_migrated(self):
        actual = {str(path.relative_to(DOCS)) for path in public_markdown_files()}
        self.assertTrue(EXPECTED_PAGES <= actual)

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


if __name__ == "__main__":
    unittest.main()
