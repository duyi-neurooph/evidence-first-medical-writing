#!/usr/bin/env python3
"""Bounded, opt-in updates for an unmodified standalone skill installation.

Only the official repository's latest stable release is considered. No manuscript
or usage history is read. New code is installed as data, never imported/executed.
"""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
import zlib

NAME = "evidence-first-medical-writing"
REPO = "duyi-neurooph/" + NAME
API = "https://api.github.com/repos/" + REPO + "/releases/latest"
RELEASES = "https://github.com/" + REPO + "/releases/latest"
MANIFEST = "SKILL-MANIFEST.sha256"
MAX_ARCHIVE = 32 * 1024 * 1024
MAX_FILE = 8 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024
MAX_FILES = 3000
TIMEOUT = 8
DEADLINE = 20


class UpdateError(Exception):
    pass


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value):
        raise UpdateError("Unsupported version; only stable major.minor.patch versions are supported.")
    return tuple(int(item) for item in value.split("."))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative_path(value):
    if not value or "\\" in value or ":" in value or any(ord(char) < 32 for char in value):
        raise UpdateError("Unsafe package path.")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in (".", "..", "") for p in value.split("/")):
        raise UpdateError("Unsafe package path.")
    reserved = {"CON", "PRN", "AUX", "NUL", *("COM" + str(i) for i in range(1, 10)), *("LPT" + str(i) for i in range(1, 10))}
    if any(part.endswith((" ", ".")) or part.split(".")[0].upper() in reserved for part in path.parts):
        raise UpdateError("Platform-ambiguous package path.")
    return path.as_posix()


def parse_manifest(data):
    entries = {}
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeError as exc:
        raise UpdateError("Unreadable checksum manifest.") from exc
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise UpdateError("Malformed checksum manifest.")
        path = match[2][2:] if match[2].startswith("./") else match[2]
        path = relative_path(path)
        if path in entries:
            raise UpdateError("Duplicate checksum path.")
        entries[path] = match[1]
    if not entries:
        raise UpdateError("Empty checksum manifest.")
    return entries


def verify_files(files, manifest_name):
    if manifest_name not in files:
        raise UpdateError("Required checksum manifest is missing; reinstall manually.")
    entries = parse_manifest(files[manifest_name])
    if set(entries) != set(files) - {manifest_name}:
        raise UpdateError("Files differ from the packaged inventory; local edits/extras are protected.")
    if any(digest(files[path]) != checksum for path, checksum in entries.items()):
        raise UpdateError("Checksum mismatch; local edits or an invalid package are protected.")
    return entries


def metadata(data):
    try:
        result = json.loads(data)
    except (ValueError, UnicodeError) as exc:
        raise UpdateError("Invalid version metadata.") from exc
    if not isinstance(result, dict) or result.get("schema") != 1 or result.get("name") != NAME or result.get("repository") != REPO:
        raise UpdateError("Unrecognized skill identity or update schema.")
    version(result.get("version"))
    return result


def validate_entrypoint(data):
    try:
        text = data.decode("utf-8")
    except UnicodeError as exc:
        raise UpdateError("Unreadable skill entrypoint.") from exc
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match or not re.search(r"(?m)^name: *" + re.escape(NAME) + r" *$", match[1]) or not re.search(r"(?m)^description: *\S", match[1]):
        raise UpdateError("Unsupported/malformed skill frontmatter; review manually.")


def no_symlink_path(path):
    for component in (path, *path.parents):
        if component.is_symlink():
            raise UpdateError("Symlinked installation/update paths require manual handling.")


def installation_root(path):
    root = Path(os.path.abspath(path))
    no_symlink_path(root)
    if root.name != NAME or not root.is_dir():
        raise UpdateError("Select the standalone evidence-first-medical-writing skill folder.")
    return root


def writable_installation(root):
    no_symlink_path(root)
    if any(part.lower() in ("plugins", "cache", ".cache", ".system") for part in root.parts):
        raise UpdateError("Managed/plugin/system/cache installations must use their host's updater.")
    if any((p / ".git").exists() or (p / ".codex-plugin").exists() for p in (root, *root.parents)):
        raise UpdateError("Source checkouts and plugin packages are check-only; update through their owner/host.")
    if not os.access(root, os.W_OK) or not os.access(root.parent, os.W_OK):
        raise UpdateError("Installation is not writable; use a permitted manual/host update.")


def read_installation(root):
    files = {}
    directories = set()
    total = 0
    for folder, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            item = Path(folder) / name
            if item.is_symlink():
                raise UpdateError("Local symlink detected; nothing will be overwritten.")
            mode = item.stat().st_mode
            rel = item.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                directories.add(rel)
            elif not stat.S_ISREG(mode):
                raise UpdateError("Special local file detected; nothing will be overwritten.")
            else:
                size = item.stat().st_size
                total += size
                if size > MAX_FILE or total > MAX_EXPANDED or len(files) >= MAX_FILES:
                    raise UpdateError("Local installation exceeds conservative update limits.")
                files[rel] = item.read_bytes()
    entries = verify_files(files, MANIFEST)
    expected_dirs = {p.as_posix() for name in entries for p in PurePosixPath(name).parents if p.as_posix() != "."}
    if directories != expected_dirs:
        raise UpdateError("Additional local directories are protected; update manually.")
    if "SKILL.md" not in files or "version.json" not in files:
        raise UpdateError("Incomplete skill installation.")
    metadata(files["version.json"])
    validate_entrypoint(files["SKILL.md"])
    return files


def config_path(root):
    path = root.parent / ("." + NAME + ".update.json")
    no_symlink_path(path)
    return path


def read_config(root):
    path = config_path(root)
    if not path.exists():
        return {"mode": "check", "pinned_version": None}
    if not path.is_file() or path.stat().st_size > 8192:
        raise UpdateError("Invalid update preferences; use manual checking.")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise UpdateError("Unreadable update preferences.") from exc
    if not isinstance(data, dict) or data.get("schema") != 1 or data.get("installation") != str(root) or data.get("mode") not in ("check", "auto", "off"):
        raise UpdateError("Preferences do not match this installation.")
    if data.get("mode") == "auto" and data.get("automatic_updates_authorized") is not True:
        raise UpdateError("Automatic updates have not been explicitly authorized.")
    if data.get("pinned_version") is not None:
        version(data["pinned_version"])
    return data


def configure(root, mode, pin, consent):
    writable_installation(root)
    if mode == "auto" and not consent:
        raise UpdateError("Enabling automatic installation requires the user's explicit consent.")
    if mode == "auto":
        read_installation(root)
    if pin is not None:
        version(pin)
    data = {"schema": 1, "installation": str(root), "mode": mode,
            "pinned_version": pin, "automatic_updates_authorized": mode == "auto"}
    path = config_path(root)
    fd, temporary = tempfile.mkstemp(prefix=".efmw-preferences-", dir=root.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2)
            stream.write("\n")
        os.chmod(temporary, 0o600)
        no_symlink_path(path)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"status": "configured", "mode": mode, "pinned_version": pin}


def allowed_url(url, asset):
    parsed = urllib.parse.urlsplit(url)
    hosts = {"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"} if asset else {"api.github.com"}
    if parsed.scheme != "https" or parsed.hostname not in hosts or parsed.port not in (None, 443) or parsed.username or parsed.password:
        raise UpdateError("Unexpected network destination; update stopped.")


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, asset):
        super().__init__()
        self.asset = asset

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        allowed_url(newurl, self.asset)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, limit, asset=False):
    allowed_url(url, asset)
    opener = urllib.request.build_opener(SafeRedirect(asset))
    request = urllib.request.Request(url, headers={"User-Agent": NAME + "-update-check", "Accept": "application/octet-stream" if asset else "application/vnd.github+json"})
    started = time.monotonic()
    chunks, size = [], 0
    with opener.open(request, timeout=TIMEOUT) as response:
        allowed_url(response.geturl(), asset)
        length = response.headers.get("Content-Length")
        if length is not None and int(length) > limit:
            raise UpdateError("Response exceeds the download size limit.")
        # HTTPResponse.read(n) can wait for n bytes while a peer trickles data.
        # read1 performs at most one underlying read so the deadline is rechecked;
        # the conservative fallback reads one byte, not an entire large block.
        reader = getattr(response, "read1", None)
        while True:
            if time.monotonic() - started > DEADLINE:
                raise UpdateError("Update request timed out; continue with the installed version.")
            block = reader(min(65536, limit + 1 - size)) if reader else response.read(1)
            if not block:
                return b"".join(chunks)
            chunks.append(block)
            size += len(block)
            if size > limit:
                raise UpdateError("Response exceeds the download size limit.")


def release_info(data):
    if not isinstance(data, dict) or data.get("draft") is not False or data.get("prerelease") is not False:
        raise UpdateError("Latest response is not a verified stable release.")
    tag = data.get("tag_name", "")
    if not isinstance(tag, str) or not tag.startswith("v"):
        raise UpdateError("Unsupported release tag.")
    newest = tag[1:]
    version(newest)
    base = "https://github.com/" + REPO + "/releases/"
    if data.get("html_url") != base + "tag/" + tag:
        raise UpdateError("Release repository identity mismatch.")
    name = NAME + "-" + newest + "-github-global.zip"
    matches = [a for a in data.get("assets", []) if isinstance(a, dict) and a.get("name") == name]
    if len(matches) != 1:
        raise UpdateError("Expected official ZIP asset is missing or ambiguous.")
    asset = matches[0]
    if asset.get("state") != "uploaded" or asset.get("browser_download_url") != base + "download/" + tag + "/" + name:
        raise UpdateError("Unexpected release asset identity/state.")
    return newest, asset, data["html_url"]


def asset_install_problem(asset):
    if type(asset.get("size")) is not int or not 0 < asset["size"] <= MAX_ARCHIVE:
        return "Release asset size is unavailable or exceeds conservative installation limits."
    if not isinstance(asset.get("digest"), str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", asset["digest"]):
        return "GitHub asset SHA-256 is unavailable; use manual review, not automatic installation."
    return None


def unpack_archive(blob, asset, newest):
    problem = asset_install_problem(asset)
    if problem:
        raise UpdateError(problem)
    if len(blob) != asset["size"] or "sha256:" + digest(blob) != asset["digest"]:
        raise UpdateError("Release ZIP size/checksum mismatch.")
    prefix = NAME + "/"
    files, seen, total = {}, set(), 0
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            if len(archive.infolist()) > MAX_FILES:
                raise UpdateError("Too many archive entries.")
            for info in archive.infolist():
                raw = info.filename[:-1] if info.is_dir() else info.filename
                relative_path(raw)
                if raw in seen:
                    raise UpdateError("Duplicate archive entry.")
                seen.add(raw)
                if raw != NAME and not info.filename.startswith(prefix):
                    raise UpdateError("Archive is outside the official package root.")
                if raw == NAME and not info.is_dir():
                    raise UpdateError("Package root must be a directory.")
                mode = info.external_attr >> 16
                kind = stat.S_IFMT(mode)
                if info.flag_bits & 1 or kind not in (0, stat.S_IFREG, stat.S_IFDIR) or (kind == stat.S_IFDIR) != info.is_dir() and kind != 0:
                    raise UpdateError("Encrypted, symlink, or special archive entry rejected.")
                if info.is_dir():
                    continue
                total += info.file_size
                if info.file_size > MAX_FILE or total > MAX_EXPANDED or (info.file_size > 1024 * 1024 and info.file_size > 1000 * max(info.compress_size, 1)):
                    raise UpdateError("Archive expansion exceeds conservative limits.")
                files[info.filename[len(prefix):]] = archive.read(info)
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, zlib.error) as exc:
        raise UpdateError("Invalid/unsupported release ZIP.") from exc
    verify_files(files, "FILE-MANIFEST.sha256")
    skill_prefix = "skills/" + NAME + "/"
    skill_files = {name[len(skill_prefix):]: data for name, data in files.items() if name.startswith(skill_prefix)}
    verify_files(skill_files, MANIFEST)
    if metadata(skill_files.get("version.json", b"{}"))["version"] != newest or "SKILL.md" not in skill_files:
        raise UpdateError("Skill metadata does not match the release.")
    validate_entrypoint(skill_files["SKILL.md"])
    return skill_files


def write_tree(root, files):
    for name, data in files.items():
        target = root.joinpath(*PurePosixPath(relative_path(name)).parts)
        if os.path.commonpath((str(root.resolve()), str(target.resolve()))) != str(root.resolve()):
            raise UpdateError("Package target escapes staging.")
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)


def install(root, old_files, new_files):
    lock = root.parent / ("." + NAME + ".update-lock")
    no_symlink_path(lock)
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise UpdateError("Another update or a stale update lock exists; check it manually before retrying.") from exc
    try:
        return install_locked(root, old_files, new_files)
    finally:
        lock.rmdir()


def install_locked(root, old_files, new_files):
    writable_installation(root)
    if read_installation(root) != old_files:
        raise UpdateError("Installation changed during checking; update cancelled.")
    temporary = Path(tempfile.mkdtemp(prefix=".efmw-update-", dir=root.parent))
    staged, previous = temporary / "next", temporary / "previous"
    backup_dir = root.parent / ("." + NAME + "-backups")
    backup = None
    moved_old = False
    installed_new = False
    committed = False
    try:
        staged.mkdir()
        write_tree(staged, new_files)
        if read_installation(staged) != new_files:
            raise UpdateError("Staged installation failed validation.")
        no_symlink_path(backup_dir)
        backup_dir.mkdir(mode=0o700, exist_ok=True)
        backup = backup_dir / (metadata(old_files["version.json"])["version"] + "-" + uuid.uuid4().hex + ".zip")
        with zipfile.ZipFile(backup, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in old_files.items():
                archive.writestr(name, data)
        with zipfile.ZipFile(backup) as archive:
            if {name: archive.read(name) for name in archive.namelist()} != old_files:
                raise UpdateError("Backup verification failed.")
        if read_installation(root) != old_files:
            raise UpdateError("Installation changed before replacement; update cancelled.")
        no_symlink_path(root)
        os.replace(root, previous)
        moved_old = True
        if read_installation(previous) != old_files:
            raise UpdateError("Original changed during replacement; restore and review manually.")
        os.replace(staged, root)
        installed_new = True
        if read_installation(root) != new_files:
            raise UpdateError("Installed files failed validation.")
        committed = True
        return str(backup)
    except BaseException:
        if moved_old:
            try:
                if installed_new:
                    os.replace(root, temporary / "failed-new")
                os.replace(previous, root)
                moved_old = False
            except OSError as exc:
                raise UpdateError("Rollback needs manual recovery. Original preserved at " + str(previous) + "; backup: " + str(backup)) from exc
        raise
    finally:
        # Remove only the private staging directory created by this call. On a
        # rollback failure, retain it because it still holds the original tree.
        if committed or not previous.exists():
            shutil.rmtree(temporary)


def run(root, force_check=False, apply=False, consent=False, fetcher=fetch):
    root = installation_root(root)
    no_symlink_path(root / "version.json")
    version_file = root / "version.json"
    if not version_file.is_file() or version_file.stat().st_size > 8192:
        raise UpdateError("Missing/oversized local version metadata; reinstall manually.")
    current = metadata(version_file.read_bytes())["version"]
    prefs = read_config(root)
    result = {"installed_version": current, "release_url": RELEASES}
    if prefs["mode"] == "off" and not force_check and not apply:
        return dict(result, status="disabled")
    if apply and not consent:
        raise UpdateError("A one-time update requires explicit user consent (--apply --consent).")
    latest, asset, url = release_info(json.loads(fetcher(API, 1024 * 1024)))
    result.update(latest_version=latest, release_url=url)
    if version(latest) <= version(current):
        return dict(result, status="current" if latest == current else "newer_local_version_preserved")
    if prefs.get("pinned_version") is not None and prefs["pinned_version"] != latest:
        return dict(result, status="update_available_pinned", pinned_version=prefs["pinned_version"])
    problem = asset_install_problem(asset)
    if problem:
        return dict(result, status="update_available_manual", reason=problem,
                    action="A newer release exists, but automatic installation is not verifiable; review the official release manually.")
    should_apply = apply or prefs["mode"] == "auto" and not force_check
    if not should_apply:
        return dict(result, status="update_available", action="Ask once before enabling automatic installation; otherwise provide the official release link.")
    writable_installation(root)
    old_files = read_installation(root)
    if metadata(old_files["version.json"])["version"] != current:
        raise UpdateError("Installed version changed during the release check; no update performed by this invocation.")
    blob = fetcher(asset["browser_download_url"], MAX_ARCHIVE, asset=True)
    new_files = unpack_archive(blob, asset, latest)
    backup = install(root, old_files, new_files)
    return dict(result, status="updated_reload_required", installed_version=latest, previous_version=current, backup=backup,
                action="Give the user the localized installation completion message from references/updates.md once. "
                       "Start a fresh task/reload the skill before using the new instructions; do not mix versions within a review.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parent.parent)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--check", action="store_true", help="Check without installing, even when auto mode is configured.")
    actions.add_argument("--apply", action="store_true", help="Perform a one-time authorized update.")
    actions.add_argument("--configure", choices=("check", "auto", "off"))
    parser.add_argument("--consent", action="store_true", help="Use only after the user explicitly permits installation/auto-updates.")
    parser.add_argument("--pin", help="Pin a version when configuring; omit to clear an existing pin.")
    args = parser.parse_args(argv)
    if args.pin and not args.configure:
        parser.error("--pin requires --configure")
    try:
        root = installation_root(args.root)
        if args.configure:
            result = configure(root, args.configure, args.pin, args.consent)
        else:
            result = run(root, args.check, args.apply, args.consent)
    except (UpdateError, OSError, ValueError, KeyError, TypeError, urllib.error.URLError) as exc:
        result = {"status": "not_updated", "reason": str(exc), "release_url": RELEASES,
                  "action": "Continue with the installed version; use a permitted manual/host update if needed. No manuscript task should be blocked by this check."}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
