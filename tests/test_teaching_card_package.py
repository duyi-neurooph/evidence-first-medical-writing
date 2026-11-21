"""Distribution invariants; scientific decisions are tested with held-out prompts."""
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


SKILL = Path(__file__).resolve().parents[1] / "skills" / "evidence-first-medical-writing"
CARDS = SKILL / "references" / "writing-example-cards.md"


class TeachingCardPackage(unittest.TestCase):
    def test_runtime_entry_links_to_self_contained_cards(self):
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(CARDS.relative_to(SKILL).as_posix(), re.findall(r"\]\(([^)]+)\)", entry))
        body = CARDS.read_text(encoding="utf-8")
        self.assertNotRegex(body, r"(?i)https?://")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            url = urlsplit(target)
            self.assertFalse(url.scheme or url.netloc)
            dest = (CARDS.parent / url.path).resolve()
            self.assertTrue(SKILL in dest.parents and dest.exists(), target)

    def test_no_public_account_article_hosts_in_runtime_docs(self):
        for path in SKILL.rglob("*.md"):
            with self.subTest(path=path.relative_to(SKILL)):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r"(?i)\bmp\.weixin\.qq\.com\b")
