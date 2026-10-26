# Evidence-First Medical Writing

**循证医学科研写作**

<img src="assets/logo.png" alt="Evidence-First Medical Writing logo" width="144">

[中文说明](README.zh-CN.md)

A bilingual Codex skill for planning, diagnosing, revising, and checking medical research manuscripts with evidence boundaries and research credibility first.

Published and maintained by **Yi**. Contact: [duyinapoleon@gmail.com](mailto:duyinapoleon@gmail.com).

This project is independent. It is not affiliated with, authorized by, or endorsed by any author, publisher, journal, institution, platform, or other third party.

Method provenance: the workflow distills transferable principles, workflows, and checklists from diverse medical research-writing and editorial practice. The public repository identifies no specific third-party source or contributor.

Repository: <https://github.com/duyi-neurooph/evidence-first-medical-writing>

## What it does

- Builds a research task card, PICO-T frame, core claim, and IMRaD outline.
- Checks alignment across the question, design, endpoint, analysis, results, and conclusion.
- Flags research-integrity and reporting risks before language polishing.
- Retrieves applicable reporting guidelines through EQUATOR and official sources before substantive drafting or review, then records versions and item-level improvements.
- Revises titles, abstracts, sections, tables, figures, cover letters, and reviewer responses.
- Runs independent multi-reviewer simulated peer review with a separate editor, iterative revision, a Decision Ledger, and non-regression checks.
- Reconciles the final submission package across data, references, numbering, participant flow, registration, terminology, statistical summaries, eligibility, contributions, and reviewer responses.
- Supports randomized, observational, diagnostic, prediction, systematic review/meta-analysis, case-based, and short-form work.
- Prioritizes findings as `P0 credibility blocker`, `P1 research logic`, `P2 structure and self-evidence`, and `P3 language and format`.

## Safety boundaries

The skill must not:

- invent data, methods, registrations, ethics approvals, citations, or reviewer decisions;
- change endpoints, thresholds, analysis sets, or conclusions to pursue significance;
- turn association into causation or non-significance into equivalence;
- conceal negative primary outcomes, limitations, deviations, errors, or uncertainty;
- impersonate a living person or reproduce a recognizable personal writing style;
- claim authorization, endorsement, affiliation, or official status without verifiable permission;
- expose patient information, confidential manuscripts, private correspondence, or identity mappings.

It assists with writing and research reasoning. It does not replace clinical judgment, statistical sign-off, ethics review, legal advice, or the current instructions of a target journal.

## Use

1. Download the latest release from this repository.
2. Install the skill or skills-only plugin using the workflow supported by your Codex environment.
3. Invoke `$evidence-first-medical-writing` or ask for an evidence-first medical manuscript review.

Repository clone:

```bash
git clone https://github.com/duyi-neurooph/evidence-first-medical-writing.git
```

The runnable entry point is:

```text
skills/evidence-first-medical-writing/SKILL.md
```

Example prompts:

```text
Use $evidence-first-medical-writing to diagnose the three most important
credibility or alignment problems in this manuscript before editing the language.
```

```text
Build a title, structured abstract plan, and IMRaD outline for this observational
study. Do not invent missing results; mark them as author queries.
```

```text
Rewrite this reviewer response while separating our position, action taken,
result, impact on the conclusion, and manuscript location.
```

### Current reporting guidelines at task time

For substantive manuscript planning, drafting, rewriting, or review, the skill first identifies the actual study type, searches the [EQUATOR library](https://www.equator-network.org/reporting-guidelines/), and follows the record to current official checklists and applicable extensions. You do not need to request EQUATOR separately. It downloads and reads official files when supported, or reads the full official document online and states that no local file was saved.

The output includes a **Guideline Manifest** (selection, version, source links, retrieval date, read coverage, and limitations) and a **Reporting Guideline Matrix** (item, manuscript location, reporting status, concrete improvement, and author query). Journal-required older checklists are reconciled with current guidance; narrative reviews are not automatically assessed as systematic reviews. A completed checklist does not establish study validity or low risk of bias.

This needs browsing/file capabilities in the host assistant. The skill does not bundle guidelines or add a downloader dependency. If external access is prohibited or unavailable, it uses supplied material provisionally and cannot certify the latest version. Pure copyediting does not trigger a fresh retrieval. Within the same review task, reviewers share one frozen, unannotated guideline package; prior findings stay with the editor.

```text
Help me write or review this manuscript. Identify the study type, retrieve the
current applicable reporting guideline and extensions through EQUATOR, state the
version and source links, and give item-by-item improvements. Preserve my facts;
mark missing information for author confirmation.
```

### Final submission or resubmission check

Ask for a "final check before submission" to run ten cross-file checks with exact locations, proposed fixes, and a coverage matrix. Supply the current manuscript and available tables, figures, supplements, references, journal instructions, and revision correspondence. The same checks run at the end of a full-manuscript revision or multi-reviewer workflow.

The audit is discipline-neutral. Missing materials remain **Cannot verify**, not passed. It does not silently reconcile conflicting data, relabel a range as IQR, assume authorship from author order, or rewrite the whole manuscript. Journal-specific reference systems and task-specific terminology take priority over generic formatting preferences.

```text
Please run the final submission check on this version and the attached files.
Reconcile repeated numbers, citations, labels and flow counts; check registration,
abbreviations, statistical summaries, eligibility and factual contributions.
For a resubmission, verify every reviewer-comment subpart against the response and
actual revision. Give locations, smallest fixes, author confirmations and a
coverage matrix. Preserve original files and do not change data on my behalf.
```

### Independent multi-reviewer workflow

Use this workflow when you want isolated clinical, methodological, statistical, evidence, or editorial assessments followed by editor adjudication and revision. The defaults are two rounds, three to four reviewers selected for the article type, one separate editor, journal-compliance review, a Citation Audit, and a clean revision plus Issue Matrix. All reports are explicitly labeled as simulated peer review.

For genuinely independent parallel assessments, use a multi-agent or Ultra-capable mode when available. If it is unavailable, the skill continues with isolated sequential passes and discloses that reviewer independence is approximate.

Copyable request template:

```text
Please perform an independent multi-reviewer peer review and iterative revision
of the attached clinical manuscript. Treat every report and decision as simulated
peer review.

Target journal:
Article type:
Manuscript version:
Journal guidelines:
Public reporting-guideline lookup allowed: yes
Reviewer roles:
Number of review rounds: 2
Broader literature search allowed:
Protected author decisions or unpublished data:
Required outputs:

Each reviewer must assess the same frozen manuscript independently and must not
see the other reviewers' comments. A separate editor should reconcile the reports,
reject weak or conflicting suggestions where appropriate, supervise revision, and
initiate a fresh second-round review. Preserve a Decision Ledger so corrected
problems are not reintroduced. Audit claim-citation fit, citation placement,
self-contained wording, statistical interpretation, tables, figures, journal
compliance, and AI-like or slogan-based prose. Do not alter data or scientific
meaning without explicit author approval.
```

Do not paste confidential manuscripts, identifiable health information, unpublished data, or private reviewer correspondence into public GitHub issues.

## Repository layout

```text
.
├── .codex-plugin/plugin.json
├── .github/
├── assets/
├── skills/evidence-first-medical-writing/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── LICENSE.md
├── NOTICE.md
├── PRIVACY.md
├── SUPPORT.md
└── TERMS.md
```

## License

This repository is **source-available under the [PolyForm Noncommercial License 1.0.0](LICENSE.md)**. Use, modification, and redistribution are permitted only for purposes the license defines as permitted.

It is free to obtain, but it is not presented as open-source software or free software. Review the license before using, modifying, or redistributing the project. Commercial use requires a separate written license from Yi.

Anyone redistributing all or part of the project must include the license terms or their official URL and preserve every `Required Notice:` line supplied with the project.

## Contributing and support

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. For usage and safe reporting channels, see [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), and [TERMS.md](TERMS.md).

If you believe repository content affects rights you hold, use the **Rights concern** issue template or email [duyinapoleon@gmail.com](mailto:duyinapoleon@gmail.com) with the subject `Rights Concern`. Do not post confidential evidence in a public issue.

## Release

Current release: `0.4.0`.

Development changes: runtime reporting-guideline retrieval and a ten-part final submission audit, proposed for `0.5.0` (not yet released). See [CHANGELOG.md](CHANGELOG.md).

Copyright © 2026 Yi. See [NOTICE.md](NOTICE.md).
