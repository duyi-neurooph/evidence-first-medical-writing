# Release checks and optional updates

## On-use behavior

Read the loaded version locally for each new task. If allowed, the next eligible task checks online at most once per installation per rolling seven days, including failed attempts. Do not run a background service, install a scheduled task, retry a failed check repeatedly, or check separately in each reviewer subagent. A user request for offline work or no update checks overrides this default. A failed/unavailable check must not block manuscript work or be described as "up to date."

For a local installation with Python 3, run the bundled `scripts/update_skill.py` using the actual loaded skill folder. The default does not change the installation. It records the attempt locally before requesting release metadata; it does not download a ZIP or transmit manuscript text, raw data, prompts, or AI-use history. Update preferences contain only the installation path, mode, pinned version, update consent and backup-retention choice. Ordinary network requests still disclose normal connection metadata to GitHub. The helper uses the Python standard library only.

The JSON describes the installation on disk (`installed_version`) and, if checked, the official stable release (`latest_version`). Neither field establishes which instructions are loaded in this chat. For the task notice, compare the version captured when this skill was loaded with the verified stable release. If the loaded version is newer than the official stable release, say so; do not call it the latest official release. A pin limits installation, not the availability of a newer release. If the check was skipped or could not be verified, say so in the user's language. On `weekly_check_skipped`, do not go online. If useful, date `last_checked_version` using `last_attempt_utc_epoch` (UTC); a null version means no verified result. Never treat the cache as a fresh check or use it to install. If the receipt cannot be persisted, skip automatic lookup.

```text
python3 -B /absolute/path/to/evidence-first-medical-writing/scripts/update_skill.py
```

Do not infer permission to install updates from permission to review a manuscript. On the first available update, briefly offer automatic installation or the official release link. Only after the user explicitly chooses automatic updates, and the host permits local writes, configure the exact standalone installation once:

```text
python3 -B /absolute/path/to/evidence-first-medical-writing/scripts/update_skill.py --configure auto --consent
```

The same ordinary on-use invocation then attempts an update only when all safety checks pass. The helper cannot grant filesystem/network permission or change the host's approval rules. A user who requests a one-time update may use `--apply --consent`; that does not opt into future automatic updates. The `--consent` option represents a real user choice, not a flag the assistant may add merely to bypass the default.

By default each update keeps a verified old-version ZIP. Only if the user explicitly requests no retained backups for a particular installation, configure its retention preference. Example for an already authorized auto-updating standalone install (use the actual absolute paths):

```text
python3 -B /path/to/v1.0.5-or-newer/scripts/update_skill.py --root /path/to/installed/evidence-first-medical-writing --configure auto --consent --no-backup
python3 -B /path/to/v1.0.5-or-newer/scripts/update_skill.py --root /path/to/installed/evidence-first-medical-writing
```

Use the newer helper for **both** commands on the first upgrade from an older installation; older helpers do not honor the new preference. Keep the existing mode and repeat any existing `--pin` unless the user wants to change them. For check-only mode configure `--configure check --no-backup`; a one-time authorized `--apply --consent` then respects that preference. To resume archiving, use `--keep-backup` when configuring. Omitting either flag leaves retention unchanged; installations with no setting keep backups. An explicit opt-out affects future updates to that installation only; it never deletes existing archives.

To check without installing even when automatic mode is enabled, add `--check`. To disable checking, use `--configure off`. To return to check-only mode, use `--configure check`. To keep a fixed version, use `--configure check --pin 0.7.1` (replace the version as requested); configuring again without `--pin` clears the pin. Preferences are stored beside, not inside, the skill folder so release replacement cannot reset them.

## Safe installation boundary

Automatic installation supports only a writable, unmodified **standalone skill folder** with `version.json` and `SKILL-MANIFEST.sha256`. It refuses source checkouts, packaged plugins, system/managed cache paths, symlinks, unsupported schemas, local edits, additional files/directories, and missing manifests. Use the package manager or host's update mechanism for managed installations; do not copy over its cache. Do not delete custom files to force an update through. A standalone copy inside a source checkout also requires manual handling.

Do not edit the skill files concurrently with installation. The update lock excludes other copies of this updater, not arbitrary editors or other programs. A customized standalone copy can still switch to `--configure off` or `--configure check`; pristine-file checks apply to installation and enabling automatic updates, not to opting out.

The helper checks the pinned official repository, stable version order, exact release asset identity, GitHub's asset SHA-256, package and skill manifests, archive paths/file types and conservative size limits. It stages the new skill without running downloaded code, creates and verifies the ZIP backup unless opted out, checks the original again, uses a per-installation update lock, and keeps the original temporarily until the replacement is validated. A failed replacement rolls back when possible; if rollback itself fails, the original staging path is reported and retained for manual recovery, with the ZIP if enabled. Without a retained ZIP there is **no archived rollback copy after a successful update**. It never downgrades. Checksums detect mismatch/corruption; they are not an independent signature or a guarantee that a future publisher release is safe.

Backups are kept in the sibling hidden directory `.evidence-first-medical-writing-backups/`; each ZIP contains the exact prior skill files. Do not automatically prune them. Restore only with the user's permission, into a separate folder first, and preserve any current customizations. A stale `.evidence-first-medical-writing.update-lock` requires checking that no update is running before removing it; do not silently defeat the lock.

If an update succeeds, report the old/new versions and backup location, or say no old-version ZIP was kept if `backup` is null. The current assistant context may still contain old instructions: reload/reinvoke the skill in a fresh task (restart the host if required) before claiming to use the new version. Do not switch instructions midway through a frozen manuscript review or between independent reviewers. If an ongoing task has already begun, defer installation until it ends.

## Installation completion message

In the chat or installer that completes a **verified first installation or actual version upgrade**, give one short wish in the user's language, once for that operation. The bundled updater's success event is `updated_reload_required`, including when an older copy of the updater performed the upgrade. For a manual or host-managed installation, rely on the installer confirming a new install/upgrade, or verify that the intended target went from absent to installed or from an older to a newer version. A download, a directory that happens to exist, a first conversation, a reinstall of the same version, a release check (including “current” or “update available”), configuring preferences, a failure or a rollback is not such an event.

Label the wish as a message from the creator, in the user's language. In Chinese, use the label “制作者寄语” and address the reader as “您”. Use the following wording or a natural equivalent:

- 中文：制作者寄语：愿您始终对未知好奇，也珍惜那些出乎意料的答案。这个工具帮您把研究写清楚；写下什么、怎样解释，仍由您把关。
- English: A note from the creator: May you stay curious, especially when a result surprises you—what you report honestly today may help a patient tomorrow. This tool helps you write clearly; what you report and how you interpret it remain your decisions.

If the installer was silent or delivery is unknown, show the wish beside the chat-only version receipt on the first substantive writing task with the loaded version; this does not establish that installation just occurred. If reliable host or conversation state says this version's wish was shown, skip it. Without cross-session state, deduplicate at least within the current conversation; do not add telemetry or store manuscript content. Combine overlapping reminders rather than repeating them. No wish for a version-only check, failure or ordinary repeat use. Never include it in copy-ready prose, a figure, comments, cover letter, review report or any other deliverable.

## Capability fallbacks

- Without the helper or reliable persistent state, skip automatic lookup; do not use a browser/connector workaround. You may offer the [official release page](https://github.com/duyi-neurooph/evidence-first-medical-writing/releases/latest).
- Without browsing/network permission, state "update check unavailable" when relevant and continue with the installed version. Never upload manuscript materials to perform an update check.
- Skill instructions are not an always-running updater. Host invocation, available tools, user consent, and permissions determine whether checks/updates actually run. No universal automatic-update guarantee is made for Codex, ChatGPT, WorkBuddy, or other hosts.
- Versions earlier than 0.7.1 do not contain this mechanism. Users must install 0.7.1 or later once before on-use checks are available; existing 0.7.0 copies do not update themselves retroactively.

For maintainers: generate `SKILL-MANIFEST.sha256` from all distributable skill files except that manifest itself, then regenerate the repository-level `FILE-MANIFEST.sha256`, then build the release ZIP. Never include installed preferences, backups, locks, manuscript files or generated Python caches. Run the offline updater tests before publication. A release lacking GitHub's asset digest remains checkable but cannot be automatically installed.
