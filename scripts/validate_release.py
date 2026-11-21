#!/usr/bin/env python3
"""Validate public package metadata, links, invariants and nested inventories.

Run from any directory. --write-manifests regenerates checksums after intentional
edits. --archive verifies a built ZIP against this exact public worktree.
--require-release rejects local candidates even when their metadata is valid.
Uses only Python's standard library; it does not access the network.
"""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
NAME = "evidence-first-medical-writing"
SKILL = ROOT / "skills" / NAME
ROOT_MANIFEST = ROOT / "FILE-MANIFEST.sha256"
SKILL_MANIFEST = SKILL / "SKILL-MANIFEST.sha256"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def inventory():
    names = git("ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")
    paths = {ROOT / name for name in names if name}
    paths.update((ROOT_MANIFEST, SKILL_MANIFEST))
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        assert not path.is_symlink(), f"Symlink in package: {rel}"
        assert path.suffix.lower() not in {".docx", ".pdf", ".html", ".zip", ".eml", ".pyc"}, f"Private/generated format: {rel}"
        assert not re.search(r"(^|/)(private-source-audit|raw-sources|release-kit|source-corpus|source-inventory|guidelines|guideline-audits|__pycache__)(/|$)", rel), f"Private/generated directory: {rel}"
        assert not any(part.startswith((".efmw-", ".evidence-first-medical-writing")) for part in path.relative_to(ROOT).parts), f"Installed update state: {rel}"
    return sorted(paths)


def manifest(base, paths, own):
    return "".join(hashlib.sha256(path.read_bytes()).hexdigest() + "  ./" + path.relative_to(base).as_posix() + "\n"
                   for path in sorted(paths) if path != own)


def check_release_metadata(version, changelog, citation, readmes, require_release=False):
    headings = re.findall(r"^## (.+)$", changelog, re.M)
    version_pattern = r"\d+\.\d+\.\d+"
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    assert re.fullmatch(version_pattern, version), "Version format"
    assert re.findall(r'^version: "([^"]+)"$', citation, re.M) == [version], "Citation version mismatch"
    entry = re.fullmatch(rf"{re.escape(version)} — (Unreleased|{date_pattern})", headings[0]) if headings else None
    assert entry, "Missing or invalid current changelog entry"
    candidate = entry[1] == "Unreleased"
    assert not (candidate and require_release), "Unreleased candidate cannot pass --require-release"
    citation_dates = re.findall(r"^date-released: *(.*)$", citation, re.M)
    if candidate:
        assert not citation_dates, "Unreleased candidate has a citation release date"
        previous = re.fullmatch(rf"({version_pattern}) — ({date_pattern})", headings[1]) if len(headings) > 1 else None
        assert previous, "Missing last dated release after candidate entry"
        date.fromisoformat(previous[2])
        linked_version = previous[1]
        assert tuple(map(int, linked_version.split('.'))) < tuple(map(int, version.split('.'))), "Candidate is not newer than previous release"
    else:
        date.fromisoformat(entry[1])
        assert citation_dates == [entry[1]], "Citation and changelog release dates differ"
        linked_version = version

    base = f"https://github.com/duyi-neurooph/{NAME}/releases"
    for doc, body in readmes.items():
        targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", body)
        tag = f"{base}/tag/v{linked_version}"
        asset = f"{base}/download/v{linked_version}/{NAME}-{linked_version}-github-global.zip"
        assert tag in targets and asset in targets, f"Release links: {doc}"
        if candidate:
            assert version in body, f"Local candidate version not named: {doc}"
            assert not re.search(rf"/releases/(?:tag|download)/v{re.escape(version)}(?=[^\w.-]|$)", body), f"Unreleased candidate linked as a release: {doc}"
    return "unreleased" if candidate else "dated"


def validate(write=False, archive=None, require_release=False):
    paths = inventory()
    skill_paths = [p for p in paths if SKILL in p.parents]
    skill_text = manifest(SKILL, skill_paths, SKILL_MANIFEST)
    if write:
        SKILL_MANIFEST.write_text(skill_text, encoding="utf-8")
    assert SKILL_MANIFEST.read_text(encoding="utf-8") == skill_text, "Stale skill manifest"
    root_text = manifest(ROOT, paths, ROOT_MANIFEST)
    if write:
        ROOT_MANIFEST.write_text(root_text, encoding="utf-8")
    assert ROOT_MANIFEST.read_text(encoding="utf-8") == root_text, "Stale root manifest"

    plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    marker = json.loads((SKILL / "version.json").read_text())
    version = plugin["version"]
    assert marker == {"schema": 1, "name": NAME, "version": version, "repository": "duyi-neurooph/" + NAME}, "Version marker mismatch"
    release_state = check_release_metadata(version, (ROOT / "CHANGELOG.md").read_text(), (ROOT / "CITATION.cff").read_text(),
                                           {doc: (ROOT / doc).read_text() for doc in ("README.md", "README.zh-CN.md")}, require_release)

    text = (SKILL / "SKILL.md").read_text()
    front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert front and f"name: {NAME}\n" in front[1], "Skill identity/frontmatter"
    assert "description: " in front[1], "Missing skill description"
    assert all(gate in text for gate in ("**Credibility:**", "**Alignment:**", "**Self-evidence:**", "**Hierarchy:**", "**Expression:**")), "Missing quality gate"
    final = (SKILL / "references/final-submission-audit.md").read_text()
    assert re.findall(r"^### (F\d+) —", final, re.M) == [f"F{i}" for i in range(1, 11)], "F1-F10 changed"

    for rel in ("LICENSE.md", "NOTICE.md", "TERMS.md", "skills/" + NAME + "/agents/openai.yaml", "skills/" + NAME + "/references/ai-use-and-disclosure.md"):
        assert (ROOT / rel).read_bytes() == git("show", "v0.7.0:" + rel), f"Protected 0.7.0 file changed: {rel}"
    reviewer_path = "skills/" + NAME + "/references/independent-multi-reviewer-workflow.md"
    quote = r"^> For genuinely independent parallel reviewer assessments,.*$"
    old_quote = re.findall(quote, git("show", "v0.7.0:" + reviewer_path).decode(), re.M)
    assert old_quote and re.findall(quote, (ROOT / reviewer_path).read_text(), re.M) == old_quote, "Dated capability reminder changed"

    links = 0
    for path in paths:
        if path.suffix == ".json":
            json.loads(path.read_text())
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            assert dest == ROOT or ROOT in dest.parents, f"Outside-package link in {path.name}: {target}"
            assert dest.exists(), f"Broken relative link in {path.name}: {target}"
            links += 1
    if archive:
        with zipfile.ZipFile(archive) as zf:
            members = {n for n in zf.namelist() if not n.endswith("/")}
            expected = {NAME + "/" + p.relative_to(ROOT).as_posix() for p in paths}
            assert members == expected, "ZIP inventory differs from public worktree"
            assert len(members) == len([n for n in zf.namelist() if not n.endswith("/")]), "Duplicate ZIP members"
            for path in paths:
                assert zf.read(NAME + "/" + path.relative_to(ROOT).as_posix()) == path.read_bytes(), f"ZIP mismatch: {path.name}"
    return {"version": version, "release_state": release_state, "public_files": len(paths), "skill_files": len(skill_paths), "relative_links": links, "archive_verified": bool(archive), "status": "passed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifests", action="store_true")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--require-release", action="store_true", help="reject an unreleased local candidate")
    args = parser.parse_args()
    print(json.dumps(validate(args.write_manifests, args.archive, args.require_release), indent=2))
