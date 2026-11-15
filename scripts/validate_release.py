#!/usr/bin/env python3
"""Validate public package metadata, links, invariants and nested inventories.

Run from any directory. --write-manifests regenerates checksums after intentional
edits. --archive verifies a built ZIP against this exact public worktree.
Uses only Python's standard library; it does not access the network.
"""

import argparse
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


def validate(write=False, archive=None):
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
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), "Version format"
    assert marker == {"schema": 1, "name": NAME, "version": version, "repository": "duyi-neurooph/" + NAME}, "Version marker mismatch"
    assert f'version: "{version}"' in (ROOT / "CITATION.cff").read_text(), "Citation version mismatch"
    assert f"## {version} — " in (ROOT / "CHANGELOG.md").read_text(), "Missing changelog entry"
    for doc in ("README.md", "README.zh-CN.md"):
        value = (ROOT / doc).read_text()
        assert f"releases/tag/v{version}" in value and f"{NAME}-{version}-github-global.zip" in value, f"Release links: {doc}"

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
    return {"version": version, "public_files": len(paths), "skill_files": len(skill_paths), "relative_links": links, "archive_verified": bool(archive), "status": "passed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifests", action="store_true")
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.write_manifests, args.archive), indent=2))
