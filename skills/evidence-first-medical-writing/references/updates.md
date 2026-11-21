# Release checks and optional updates

## On-use behavior

Once at the start of a new writing/review task, before freezing the manuscript and reviewer package, check the official repository's latest stable release if network access and the host's tools permit. Do not run a background service, install a scheduled task, retry a failed check repeatedly, or check separately in each reviewer subagent. A user request for offline work or no update checks overrides this default. A failed/unavailable check must not block manuscript work or be described as "up to date."

For a local installation with Python 3, run the bundled `scripts/update_skill.py` using the actual loaded skill folder. The default is a read-only release-metadata check; it does not download a ZIP or transmit manuscript text, raw data, prompts, or AI-use history. Update preferences contain only the installation path, mode, pinned version and update consent. Ordinary network requests still disclose normal connection metadata to GitHub. The helper uses the Python standard library only.

The JSON describes the installation on disk (`installed_version`) and, if checked, the official stable release (`latest_version`). Neither field establishes which instructions are loaded in this chat. For the task notice, compare the version captured when this skill was loaded with the verified stable release. If the loaded version is newer than the official stable release, say so; do not call it the latest official release. A pin limits installation, not the availability of a newer release. If the check was skipped or could not be verified, say so in the user's language.

```text
python3 -B /absolute/path/to/evidence-first-medical-writing/scripts/update_skill.py
```

Do not infer permission to install updates from permission to review a manuscript. On the first available update, briefly offer automatic installation or the official release link. Only after the user explicitly chooses automatic updates, and the host permits local writes, configure the exact standalone installation once:

```text
python3 -B /absolute/path/to/evidence-first-medical-writing/scripts/update_skill.py --configure auto --consent
```

The same ordinary on-use invocation then attempts an update only when all safety checks pass. The helper cannot grant filesystem/network permission or change the host's approval rules. A user who requests a one-time update may use `--apply --consent`; that does not opt into future automatic updates. The `--consent` option represents a real user choice, not a flag the assistant may add merely to bypass the default.

To check without installing even when automatic mode is enabled, add `--check`. To disable checking, use `--configure off`. To return to check-only mode, use `--configure check`. To keep a fixed version, use `--configure check --pin 0.7.1` (replace the version as requested); configuring again without `--pin` clears the pin. Preferences are stored beside, not inside, the skill folder so release replacement cannot reset them.

## Safe installation boundary

Automatic installation supports only a writable, unmodified **standalone skill folder** with `version.json` and `SKILL-MANIFEST.sha256`. It refuses source checkouts, packaged plugins, system/managed cache paths, symlinks, unsupported schemas, local edits, additional files/directories, and missing manifests. Use the package manager or host's update mechanism for managed installations; do not copy over its cache. Do not delete custom files to force an update through. A standalone copy inside a source checkout also requires manual handling.

Do not edit the skill files concurrently with installation. The update lock excludes other copies of this updater, not arbitrary editors or other programs. A customized standalone copy can still switch to `--configure off` or `--configure check`; pristine-file checks apply to installation and enabling automatic updates, not to opting out.

The helper checks the pinned official repository, stable version order, exact release asset identity, GitHub's asset SHA-256, package and skill manifests, archive paths/file types and conservative size limits. It stages the new skill without running downloaded code, verifies a recoverable ZIP backup, checks the original again, uses a per-installation update lock, replaces the folder, and validates the result. A failed replacement rolls back when possible; if rollback itself fails, the original staging path and backup are reported and retained for manual recovery. It never downgrades. Checksums detect mismatch/corruption; they are not an independent signature or a guarantee that a future publisher release is safe.

Backups are kept in the sibling hidden directory `.evidence-first-medical-writing-backups/`; each ZIP contains the exact prior skill files. Do not automatically prune them. Restore only with the user's permission, into a separate folder first, and preserve any current customizations. A stale `.evidence-first-medical-writing.update-lock` requires checking that no update is running before removing it; do not silently defeat the lock.

If an update succeeds, report the old/new versions and backup location. The current assistant context may still contain old instructions: reload/reinvoke the skill in a fresh task (restart the host if required) before claiming to use the new version. Do not switch instructions midway through a frozen manuscript review or between independent reviewers. If an ongoing task has already begun, defer installation until it ends.

## Installation completion message

In the chat or installer that completes a **verified first installation or actual version upgrade**, give one short wish in the user's language, once for that operation. The bundled updater's success event is `updated_reload_required`, including when an older copy of the updater performed the upgrade. For a manual or host-managed installation, rely on the installer confirming a new install/upgrade, or verify that the intended target went from absent to installed or from an older to a newer version. A download, a directory that happens to exist, a first conversation, a reinstall of the same version, a release check (including “current” or “update available”), configuring preferences, a failure or a rollback is not such an event.

Use the following wording or its natural equivalent in the user's language:

- 中文：愿你始终对未知好奇，也珍惜那些出乎意料的答案——今天如实写下的发现，也许能让明天的病人少走一段弯路。这个工具帮你把研究写得清楚、规范；写下什么，怎样解释，仍由你把关。
- English: May you stay curious, especially when a result surprises you—what you report honestly today may help a patient tomorrow. This tool helps you write clearly; what you report and how you interpret it remain your decisions.

This is a completion message, not a first-use banner. Show it in one place only; do not repeat it on reload, during ordinary writing, or in a submission artifact. If an installation completes in the same chat as a writing task, use just the first sentence of the wish alongside the task's separate responsibility reminder. Hosts with no observable installation event or completion UI cannot guarantee this message; do not guess or set up background tracking.

## Capability fallbacks

- Without Python or writable local files, a browser/connector may read the [latest official release](https://github.com/duyi-neurooph/evidence-first-medical-writing/releases/latest) and compare it with `version.json`. Offer the release link; do not pretend installation occurred.
- Without browsing/network permission, state "update check unavailable" when relevant and continue with the installed version. Never upload manuscript materials to perform an update check.
- Skill instructions are not an always-running updater. Host invocation, available tools, user consent, and permissions determine whether checks/updates actually run. No universal automatic-update guarantee is made for Codex, ChatGPT, WorkBuddy, or other hosts.
- Versions earlier than 0.7.1 do not contain this mechanism. Users must install 0.7.1 or later once before on-use checks are available; existing 0.7.0 copies do not update themselves retroactively.

For maintainers: generate `SKILL-MANIFEST.sha256` from all distributable skill files except that manifest itself, then regenerate the repository-level `FILE-MANIFEST.sha256`, then build the release ZIP. Never include installed preferences, backups, locks, manuscript files or generated Python caches. Run the offline updater tests before publication. A release lacking GitHub's asset digest remains checkable but cannot be automatically installed.
