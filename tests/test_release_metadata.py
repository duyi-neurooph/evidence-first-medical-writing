"""Offline acceptance cases for local candidates and dated release metadata."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_release import NAME, check_release_metadata


def links(version):
    base = f"https://github.com/duyi-neurooph/{NAME}/releases"
    return (f"[Release]({base}/tag/v{version})\n"
            f"[ZIP]({base}/download/v{version}/{NAME}-{version}-github-global.zip)\n")


def fixture(candidate):
    version, previous, release_date = "3.10.0", "3.9.1", "2024-02-29"
    status = "Unreleased" if candidate else release_date
    changelog = f"## {version} — {status}\n\n## {previous} — 2024-01-15\n"
    citation = f'version: "{version}"\n'
    if candidate:
        body = f"Local candidate: {version}.\n" + links(previous)
    else:
        body = links(version)
        citation += f"date-released: {release_date}\n"
    return dict(version=version, changelog=changelog, citation=citation,
                readmes={"README.md": body, "README.zh-CN.md": body})


class ReleaseMetadataTests(unittest.TestCase):
    def test_candidate_links_to_previous_dated_release(self):
        self.assertEqual(check_release_metadata(**fixture(True)), "unreleased")

    def test_dated_version_passes_release_gate(self):
        self.assertEqual(check_release_metadata(**fixture(False), require_release=True), "dated")

    def test_candidate_cannot_pass_release_gate(self):
        with self.assertRaises(AssertionError):
            check_release_metadata(**fixture(True), require_release=True)

    def test_rejects_stale_citation_version_or_date(self):
        for old, new in (("3.10.0", "3.9.1"), ("2024-02-29", "2024-01-15")):
            with self.subTest(stale=new), self.assertRaises(AssertionError):
                case = fixture(False)
                case["citation"] = case["citation"].replace(old, new)
                check_release_metadata(**case)

    def test_candidate_cannot_claim_a_release_date(self):
        case = fixture(True)
        case["citation"] += "date-released: 2024-02-29\n"
        with self.assertRaises(AssertionError):
            check_release_metadata(**case)

    def test_candidate_cannot_link_to_its_own_tag_or_zip(self):
        for link in links("3.10.0").splitlines():
            with self.subTest(link=link), self.assertRaises(AssertionError):
                case = fixture(True)
                case["readmes"]["README.zh-CN.md"] += link
                check_release_metadata(**case)

    def test_each_readme_needs_tag_and_asset_for_the_linked_version(self):
        for candidate in (True, False):
            case = fixture(candidate)
            lines = case["readmes"]["README.md"].splitlines()
            for missing in (line for line in lines if line.startswith("[")):
                with self.subTest(candidate=candidate, missing=missing), self.assertRaises(AssertionError):
                    case["readmes"]["README.md"] = "\n".join(line for line in lines if line != missing)
                    check_release_metadata(**case)
