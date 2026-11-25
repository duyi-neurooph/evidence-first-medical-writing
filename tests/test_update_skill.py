"""Offline behavioral/security tests; never contact GitHub or change an install."""

import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest import mock
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / "skills/evidence-first-medical-writing/scripts/update_skill.py"
SPEC = importlib.util.spec_from_file_location("update_skill", SCRIPT)
up = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(up)


def manifest(files):
    return "".join(up.digest(data) + "  ./" + name + "\n" for name, data in sorted(files.items())).encode()


def skill_files(number="0.7.1"):
    files = {
        "SKILL.md": b"---\nname: evidence-first-medical-writing\ndescription: Test\n---\n",
        "version.json": json.dumps({"schema": 1, "name": up.NAME, "repository": up.REPO, "version": number}).encode(),
        "references/example.md": b"Protected example.\n",
        "scripts/future.py": b"raise AssertionError('Downloaded code must not be executed')\n",
    }
    files[up.MANIFEST] = manifest(files)
    return files


def package(files, extra=None):
    items = {"skills/" + up.NAME + "/" + name: data for name, data in files.items()}
    items["README.md"] = b"Release package\n"
    items["FILE-MANIFEST.sha256"] = manifest(items)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in items.items():
            archive.writestr(up.NAME + "/" + name, data)
        if extra:
            archive.writestr(*extra)
    return stream.getvalue()


def release(blob, number="0.7.2"):
    base = "https://github.com/" + up.REPO + "/releases/"
    name = up.NAME + "-" + number + "-github-global.zip"
    return {"tag_name": "v" + number, "draft": False, "prerelease": False,
            "html_url": base + "tag/v" + number,
            "assets": [{"name": name, "state": "uploaded", "size": len(blob),
                        "digest": "sha256:" + up.digest(blob),
                        "browser_download_url": base + "download/v" + number + "/" + name}]}


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="efmw-updater-tests-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.enter_receipt_patch = mock.patch.object(up, "receipt_dir", return_value=self.base / "local-state")
        self.enter_receipt_patch.start()
        self.addCleanup(self.enter_receipt_patch.stop)
        self.root = self.base / up.NAME
        self.root.mkdir()
        self.original = skill_files()
        up.write_tree(self.root, self.original)
        self.new = skill_files("0.7.2")
        self.blob = package(self.new)
        self.info = release(self.blob)
        self.calls = []

    def fetch(self, url, limit, asset=False):
        self.calls.append((url, asset))
        return self.blob if asset else json.dumps(self.info).encode()

    def run_update(self, **kwargs):
        return up.run(self.root, fetcher=self.fetch, **kwargs)

    def assert_original(self):
        self.assertEqual(up.read_installation(self.root), self.original)

    def test_default_is_check_only_and_never_downloads_zip(self):
        self.assertEqual(self.run_update()["status"], "update_available")
        self.assertEqual(self.calls, [(up.API, False)])
        self.assert_original()
        self.assertFalse(up.config_path(self.root).exists())

    def test_cooldown_starts_at_attempt_and_expires_at_seven_days(self):
        start = 1700000000
        with mock.patch.object(up.time, "time", return_value=start) as clock:
            self.assertEqual(self.run_update()["status"], "update_available")
            clock.return_value = start + up.WEEK - 1
            cached = self.run_update(force_check=True)
            self.assertEqual(cached["status"], "weekly_check_skipped")
            self.assertEqual(cached["last_attempt_utc_epoch"], start)
            self.assertEqual(cached["last_checked_version"], "0.7.2")
            self.assertEqual(self.calls, [(up.API, False)])
            clock.return_value += 1
            self.assertEqual(self.run_update()["status"], "update_available")
            self.assertEqual(self.calls, [(up.API, False)] * 2)

    def test_failed_attempt_is_not_retried_in_the_same_window(self):
        with self.assertRaises(OSError):
            up.run(self.root, fetcher=mock.Mock(side_effect=OSError("offline")))
        result = self.run_update()
        self.assertEqual(result["status"], "weekly_check_skipped")
        self.assertIsNone(result["last_checked_version"])
        self.assertFalse(self.calls)

    def test_overlapping_tasks_cannot_start_two_checks(self):
        def during_fetch(*args):
            self.assertEqual(self.run_update()["status"], "weekly_check_skipped")
            return self.fetch(*args)
        self.assertEqual(up.run(self.root, fetcher=during_fetch)["status"], "update_available")
        self.assertEqual(self.calls, [(up.API, False)])

    def test_unavailable_receipt_never_falls_back_to_network(self):
        up.receipt_dir().write_text("not a directory")
        with self.assertRaises(OSError):
            self.run_update()
        self.assertFalse(self.calls)

    def test_explicit_apply_installs_and_preserves_verified_backup(self):
        result = self.run_update(apply=True, consent=True)
        self.assertEqual(result["status"], "updated_reload_required")
        self.assertEqual((result["previous_version"], result["installed_version"]), ("0.7.1", "0.7.2"))
        self.assertEqual(up.read_installation(self.root), self.new)
        with zipfile.ZipFile(result["backup"]) as backup:
            self.assertEqual({name: backup.read(name) for name in backup.namelist()}, self.original)
        self.assertEqual(len(self.calls), 2)
        self.assertFalse(list(self.base.glob(".efmw-update-*")))

    def test_retry_after_success_does_not_signal_another_upgrade(self):
        self.assertEqual(self.run_update(apply=True, consent=True)["status"], "updated_reload_required")
        self.calls.clear()
        repeated = self.run_update(apply=True, consent=True)
        self.assertEqual(repeated["status"], "current")
        self.assertNotIn("previous_version", repeated)
        self.assertNotIn("backup", repeated)
        self.assertEqual(self.calls, [(up.API, False)])

    def test_another_install_during_metadata_check_is_not_our_upgrade(self):
        def fetch_after_external_update(url, limit, asset=False):
            if not asset:
                for name, data in self.new.items():
                    (self.root / name).write_bytes(data)
            return self.fetch(url, limit, asset)

        with self.assertRaisesRegex(up.UpdateError, "version changed"):
            up.run(self.root, apply=True, consent=True, fetcher=fetch_after_external_update)
        self.assertEqual(self.calls, [(up.API, False)])
        self.assertEqual(up.read_installation(self.root), self.new)

    def test_apply_without_consent_does_not_access_network(self):
        with self.assertRaisesRegex(up.UpdateError, "consent"):
            self.run_update(apply=True)
        self.assertFalse(self.calls)
        self.assert_original()

    def test_auto_configuration_requires_consent(self):
        with self.assertRaisesRegex(up.UpdateError, "consent"):
            up.configure(self.root, "auto", None, False)
        self.assertFalse(up.config_path(self.root).exists())

    def test_authorized_auto_mode_installs(self):
        up.configure(self.root, "auto", None, True)
        self.assertEqual(self.run_update()["status"], "updated_reload_required")
        self.assertEqual(up.read_installation(self.root), self.new)

    def test_legacy_auto_preferences_keep_verified_backup(self):
        legacy = {"schema": 1, "installation": str(self.root), "mode": "auto",
                  "automatic_updates_authorized": True, "pinned_version": None}
        up.config_path(self.root).write_text(json.dumps(legacy), encoding="utf-8")
        with zipfile.ZipFile(self.run_update()["backup"]) as archive:
            self.assertEqual({p: archive.read(p) for p in archive.namelist()}, self.original)

    def test_cli_opt_out_auto_and_leave_old_archives_untouched(self):
        backup_dir = self.base / ("." + up.NAME + "-backups")
        backup_dir.mkdir()
        previous = backup_dir / "historical.zip"
        previous.write_bytes(b"Existing archive")
        with mock.patch("sys.stdout", new_callable=io.StringIO):
            up.main(["--root", str(self.root), "--configure", "auto", "--consent", "--no-backup"])
        up.configure(self.root, "check", None, False)
        self.assertIs(up.read_config(self.root)["keep_backup"], False)
        up.configure(self.root, "auto", None, True)
        result = self.run_update()
        self.assertEqual(result["status"], "updated_reload_required")
        self.assertIsNone(result["backup"])
        self.assertEqual(up.read_installation(self.root), self.new)
        self.assertEqual(list(backup_dir.iterdir()), [previous])
        self.assertEqual(previous.read_bytes(), b"Existing archive")
        self.assertFalse(list(self.base.glob(".efmw-update-*")))
        with mock.patch("sys.stdout", new_callable=io.StringIO):
            up.main(["--root", str(self.root), "--configure", "check", "--keep-backup"])
        self.assertIs(up.read_config(self.root)["keep_backup"], True)

    def test_no_backup_still_rolls_back_failed_swap(self):
        up.configure(self.root, "check", None, False, keep_backup=False)
        replace = os.replace
        def failing_replace(source, target):
            if Path(source).name == "next":
                raise PermissionError("simulated failure after moving original")
            return replace(source, target)
        with mock.patch.object(up.os, "replace", side_effect=failing_replace):
            with self.assertRaisesRegex(PermissionError, "simulated failure"):
                self.run_update(apply=True, consent=True)
        self.assert_original()
        self.assertFalse((self.base / ("." + up.NAME + "-backups")).exists())
        self.assertFalse(list(self.base.glob(".efmw-update-*")))

    def test_no_backup_reports_and_keeps_original_on_failed_rollback(self):
        replace = os.replace
        def failing_replace(source, target):
            if Path(source).name in ("next", "previous"):
                raise PermissionError("simulated failure")
            return replace(source, target)
        with mock.patch.object(up.os, "replace", side_effect=failing_replace):
            with self.assertRaisesRegex(up.UpdateError, "no persistent backup") as caught:
                up.install(self.root, self.original, self.new, keep_backup=False)
        previous, = self.base.glob(".efmw-update-*/previous")
        self.assertIn(str(previous), str(caught.exception))
        self.assertEqual(up.read_installation(previous), self.original)
        self.assertFalse((self.base / ("." + up.NAME + "-backups")).exists())

    def test_force_check_overrides_auto(self):
        up.configure(self.root, "auto", None, True)
        self.assertEqual(self.run_update(force_check=True)["status"], "update_available")
        self.assert_original()

    def test_off_mode_makes_no_network_request(self):
        up.configure(self.root, "off", None, False)
        self.assertEqual(self.run_update()["status"], "disabled")
        self.assertFalse(self.calls)

    def test_customized_installation_can_disable_updates(self):
        up.configure(self.root, "auto", None, True)
        (self.root / "references/example.md").write_text("My customization", encoding="utf-8")
        up.configure(self.root, "off", None, False)
        self.assertEqual(self.run_update()["status"], "disabled")
        self.assertFalse(self.calls)
        self.assertEqual((self.root / "references/example.md").read_text(), "My customization")

    def test_pin_prevents_upgrade(self):
        up.configure(self.root, "auto", "0.7.1", True)
        self.assertEqual(self.run_update()["status"], "update_available_pinned")
        self.assertEqual(len(self.calls), 1)
        self.assert_original()

    def test_current_release_and_downgrade_are_not_installed(self):
        for number, status in (("0.7.1", "current"), ("0.7.0", "newer_local_version_preserved")):
            with self.subTest(number=number):
                self.info = release(package(skill_files(number)), number)
                self.assertEqual(self.run_update(apply=True, consent=True)["status"], status)
                self.assert_original()

    def test_version_comparison_is_numeric(self):
        self.assertGreater(up.version("0.10.0"), up.version("0.9.9"))
        for value in ("v0.7.2", "0.7.2-beta", "0.07.2", "../0.7.2", None):
            with self.subTest(value=value), self.assertRaises(up.UpdateError):
                up.version(value)

    def test_dirty_file_is_not_overwritten(self):
        (self.root / "references/example.md").write_text("Author customization", encoding="utf-8")
        with self.assertRaisesRegex(up.UpdateError, "Checksum mismatch"):
            self.run_update(apply=True, consent=True)
        self.assertEqual((self.root / "references/example.md").read_text(), "Author customization")
        self.assertEqual(len(self.calls), 1)

    def test_extra_file_or_empty_directory_is_protected(self):
        extra = self.root / "my-notes.md"
        extra.write_text("Keep", encoding="utf-8")
        with self.assertRaises(up.UpdateError):
            self.run_update(apply=True, consent=True)
        extra.unlink()
        (self.root / "my-folder").mkdir()
        with self.assertRaisesRegex(up.UpdateError, "directories"):
            self.run_update(apply=True, consent=True)
        self.assertTrue((self.root / "my-folder").is_dir())

    def test_local_symlink_and_symlinked_root_are_rejected(self):
        (self.root / "link.md").symlink_to(self.root / "SKILL.md")
        with self.assertRaisesRegex(up.UpdateError, "symlink"):
            self.run_update(apply=True, consent=True)
        (self.root / "link.md").unlink()
        target = self.base / "linked"
        target.mkdir()
        (target / up.NAME).symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(up.UpdateError, "Symlink"):
            up.run(target / up.NAME, fetcher=self.fetch)

    def test_source_checkout_is_read_only(self):
        (self.base / ".git").mkdir()
        self.assertEqual(self.run_update()["status"], "update_available")
        with self.assertRaisesRegex(up.UpdateError, "check-only"):
            self.run_update(apply=True, consent=True)
        self.assert_original()

    def test_managed_cache_requires_host_update(self):
        destination = self.base / "plugins" / up.NAME
        destination.parent.mkdir()
        self.root.rename(destination)
        with self.assertRaisesRegex(up.UpdateError, "host"):
            up.run(destination, apply=True, consent=True, fetcher=self.fetch)

    def test_stable_release_identity_and_digest_are_required(self):
        for key, value in (("draft", True), ("prerelease", True), ("html_url", "https://example.com")):
            with self.subTest(key=key):
                bad = dict(self.info, **{key: value})
                with self.assertRaises(up.UpdateError):
                    up.release_info(bad)
        for key, value in (("browser_download_url", "https://example.com/a.zip"), ("state", "new")):
            with self.subTest(key=key):
                bad = dict(self.info, assets=[dict(self.info["assets"][0], **{key: value})])
                with self.assertRaises(up.UpdateError):
                    up.release_info(bad)

    def test_missing_digest_is_checkable_but_never_auto_installed(self):
        self.info["assets"][0]["digest"] = None
        up.configure(self.root, "auto", None, True)
        result = self.run_update()
        self.assertEqual(result["status"], "update_available_manual")
        self.assertEqual(result["latest_version"], "0.7.2")
        self.assertEqual(self.calls, [(up.API, False)])
        self.assert_original()

    def test_zip_checksum_mismatch_preserves_original(self):
        self.info["assets"][0]["digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(up.UpdateError, "checksum"):
            self.run_update(apply=True, consent=True)
        self.assert_original()

    def test_archive_traversal_is_rejected_before_extraction(self):
        for path in ("../outside", up.NAME + "/../outside", "/absolute", up.NAME + "/a\\b"):
            with self.subTest(path=path):
                blob = package(self.new, (path, b"bad"))
                with self.assertRaises(up.UpdateError):
                    up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")
        self.assertFalse((self.base / "outside").exists())

    def test_windows_drive_reserved_and_alias_paths_are_rejected(self):
        for path in ("D:/outside.txt", "references/D:/outside.txt", "references/x:stream", "CON.txt", "references/NUL", "references/file.", "references/file "):
            with self.subTest(path=path), self.assertRaises(up.UpdateError):
                up.relative_path(path)

    def test_archive_root_cannot_be_a_file(self):
        blob = package(self.new, (up.NAME, b"not a directory"))
        with self.assertRaisesRegex(up.UpdateError, "root"):
            up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")

    def test_archive_symlink_is_rejected(self):
        item = zipfile.ZipInfo(up.NAME + "/evil-link")
        item.create_system = 3
        item.external_attr = (stat.S_IFLNK | 0o777) << 16
        blob = package(self.new, (item, b"../../outside"))
        with self.assertRaisesRegex(up.UpdateError, "symlink"):
            up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")

    def test_extra_unmanifested_package_file_is_rejected(self):
        blob = package(self.new, (up.NAME + "/unexpected.txt", b"extra"))
        with self.assertRaisesRegex(up.UpdateError, "inventory"):
            up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")

    def test_internal_manifest_or_version_mismatch_is_rejected(self):
        changed = dict(self.new, **{"references/example.md": b"Tampered"})
        blob = package(changed)
        with self.assertRaisesRegex(up.UpdateError, "Checksum"):
            up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")
        blob = package(skill_files("0.7.3"))
        with self.assertRaisesRegex(up.UpdateError, "metadata"):
            up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")

    def test_zip_expansion_limit(self):
        blob = package(self.new, (up.NAME + "/large.txt", b"0" * (up.MAX_FILE + 1)))
        with self.assertRaisesRegex(up.UpdateError, "expansion"):
            up.unpack_archive(blob, release(blob)["assets"][0], "0.7.2")

    def test_no_network_failures_change_installation(self):
        def offline(*args, **kwargs):
            raise OSError("offline")
        with self.assertRaises(OSError):
            up.run(self.root, apply=True, consent=True, fetcher=offline)
        self.assert_original()

    def test_untrusted_redirect_is_rejected(self):
        for url in ("http://github.com/a", "https://example.com/a", "https://github.com:443@evil.test/a", "file:///tmp/a"):
            with self.subTest(url=url), self.assertRaises(up.UpdateError):
                up.allowed_url(url, True)
        up.allowed_url("https://release-assets.githubusercontent.com/a", True)

    def test_fetch_checks_deadline_between_single_reads(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = up.API
        response.headers = {}
        response.read1.return_value = b"partial"
        opener = mock.Mock()
        opener.open.return_value = response
        with mock.patch.object(up.urllib.request, "build_opener", return_value=opener), mock.patch.object(up.time, "monotonic", side_effect=[0, 0, up.DEADLINE + 1]):
            with self.assertRaisesRegex(up.UpdateError, "timed out"):
                up.fetch(up.API, 1024)
        response.read1.assert_called_once()
        response.read.assert_not_called()

    def test_lock_prevents_concurrent_update(self):
        (self.base / ("." + up.NAME + ".update-lock")).mkdir()
        with self.assertRaisesRegex(up.UpdateError, "lock"):
            up.install(self.root, self.original, self.new)
        self.assert_original()

    def test_second_rename_failure_rolls_back_original(self):
        replace = os.replace
        def failing_replace(source, target):
            if Path(source).name == "next":
                raise PermissionError("simulated install failure")
            return replace(source, target)
        with mock.patch.object(up.os, "replace", side_effect=failing_replace):
            with self.assertRaises(PermissionError):
                up.install(self.root, self.original, self.new)
        self.assert_original()
        self.assertFalse(list(self.base.glob(".efmw-update-*")))

    def test_failed_rollback_preserves_original_staging_and_backup(self):
        replace = os.replace
        def failing_replace(source, target):
            if Path(source).name in ("next", "previous"):
                raise PermissionError("simulated filesystem failure")
            return replace(source, target)
        with mock.patch.object(up.os, "replace", side_effect=failing_replace):
            with self.assertRaisesRegex(up.UpdateError, "manual recovery"):
                up.install(self.root, self.original, self.new)
        preserved = list(self.base.glob(".efmw-update-*/previous"))
        self.assertEqual(len(preserved), 1)
        self.assertEqual(up.read_installation(preserved[0]), self.original)
        self.assertEqual(len(list(self.base.glob("." + up.NAME + "-backups/*.zip"))), 1)

    def test_changed_installation_before_swap_is_not_overwritten(self):
        stale = dict(self.original)
        stale["SKILL.md"] = b"Old snapshot"
        with self.assertRaisesRegex(up.UpdateError, "changed"):
            up.install(self.root, stale, self.new)
        self.assert_original()

    def test_cli_offline_error_is_nonblocking_json(self):
        output = io.StringIO()
        with mock.patch.object(up, "run", side_effect=OSError("offline")), mock.patch("sys.stdout", output):
            up.main(["--root", str(self.root)])
        result = json.loads(output.getvalue())
        self.assertEqual(result["status"], "not_updated")
        self.assertIn("Continue", result["action"])
        self.assert_original()


if __name__ == "__main__":
    unittest.main()
