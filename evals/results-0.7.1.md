# Version 0.7.1 validation report

Prepared for publication: 2026-11-16 (Asia/Singapore). Development started 2026-11-15 from release 0.7.0, commit `601612e`. This patch adds offline statistical routing/profiles and an optional safe update helper; it does not replace the existing manuscript workflow.

## Source and behavior checks

- Current JAMA statistical sections and the linked 2003 editorial were read on 2026-11-15. Their roles are distinct: current target instructions versus historical methodological commentary.
- NEJM official access returned HTTP 403. The complete supplied undated statistical copy, sections A–C, was read and checked independently. Its publication date and live correspondence remain unverified. The original copy and private path are not distributed.
- [SP01–SP09](statistical-policy-test-cases.md) were exercised in [one offline batched forward run](statistical-policy-forward-0.7.1.md): 9/9 self-scored passes with actual response text. The evaluator was separate from the editing agent but saw expectations. This was not nine isolated host sessions, a blinded benchmark, clinical validation, or live policy verification.
- The run covered inaccessible-source fallback, baseline-table scope, causal-policy differences, hierarchical/exploratory/safety multiplicity, another target's policy, retrospective SAP honesty, P-value rounding, absent model details and narrow spelling-only scope.

## Executable checks

Commands, run from the repository root:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_release.py --write-manifests
python3 -B scripts/validate_release.py
git diff --check
```

- **34/34 offline updater tests passed**, independently rerun after review fixes. Coverage includes consent defaults, check-only/disabled/pinned modes, local edits/extras, source and managed installations, version order, malformed release identity, missing digest/manual fallback, archive integrity, symlinks/traversal/Windows paths, bounded reads, backup, lock, changed-tree checks and rollback failures.
- Independent code review found a Windows drive-qualified path vulnerability and two fallback/configuration defects. They were fixed and regression-tested before publication. The final reviewed implementation had no remaining blocking findings.
- The skill-authoring validator accepted the entrypoint/frontmatter. The public-package validator checks JSON, matching versions, relative Markdown links, nested inventories, forbidden private/generated formats, the five gates, F1–F10, and unchanged license/required notice/terms/discovery metadata/AI-disclosure reference and dated capability reminder against 0.7.0.
- A local candidate release ZIP was validated byte-for-byte against the public worktree and accepted by the updater's actual digest, archive and nested-manifest parser. No downloaded code was executed. The final archive is checked again after the release commit using `--archive`.
- A live **metadata-only** check correctly saw published 0.7.0 while the local marker was 0.7.1 and returned `newer_local_version_preserved`; it did not downgrade or download the release attachment. Release verification uses GitHub asset metadata/digest, not a verification download.

## Limits

Native Windows execution, a future real-version automatic installation, every host's invocation behavior, a background update service, and a new end-to-end clinical review panel were not tested or claimed. Windows path guards were exercised on the development host. Python and network/write capabilities are optional host facilities, not guarantees supplied by Markdown instructions.

Update consent/configuration is installation metadata, not AI-use tracking. Unsupported or customized installations remain protected and use manual/host updates. A publisher account compromise is not defeated by checksums from that same publisher. Older versions need a one-time installation of 0.7.1 before on-use checking exists.
