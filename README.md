# Evidence-First Medical Writing

**循证医学科研写作**

<img src="assets/logo.png" alt="Evidence-First Medical Writing logo" width="144">

[中文说明](README.zh-CN.md)

A bilingual Codex skill for planning, diagnosing, revising, and checking medical research manuscripts with evidence boundaries and research credibility first.

Published and maintained by **Yi**. Contact: [duyinapoleon@gmail.com](mailto:duyinapoleon@gmail.com).

This project is independent. It is not affiliated with, authorized by, or endorsed by any author, publisher, journal, institution, platform, or other third party.

Method provenance: the workflow distills transferable principles, workflows, and checklists from diverse medical research-writing and editorial practice. Private editorial sources are not identified. Third-party software components are credited under their own licenses.

Repository: <https://github.com/duyi-neurooph/evidence-first-medical-writing>

## What it does

- **Writing examples (1.0.1):** The bundled [example cards](skills/evidence-first-medical-writing/references/writing-example-cards.md) are available offline. When a writing decision calls for an example, the skill consults the relevant card: positive examples show what to keep, and negative examples show what can mislead a reader and how to fix it. All examples are synthetic, not evidence or a source of facts for your manuscript.
- **Title and abstract (1.0.1):** What study would you expect from the title alone? What would the abstract tell you on its own? The skill records those readings separately, then checks both against the actual design and available results. If the wording misleads, it suggests the smallest change that fixes the reader’s inference without changing facts, numbers or conclusions. An accurate title or abstract can stay as written.
- **Participant flow (0.9.1):** Say “Draw a flowchart from my data” and supply your study counts. No journal name is needed. [Patient groups branch downward; only exclusions point right](skills/evidence-first-medical-writing/references/participant-flow.md). Try the [synthetic randomized trial](skills/evidence-first-medical-writing/assets/flow-community-bp.json).
  Observational examples: [cohort selection](skills/evidence-first-medical-writing/assets/flow-observational-cohort.json) and [case-control sampling](skills/evidence-first-medical-writing/assets/flow-case-control.json).

- **New in 0.8.0:** [reference verification](skills/evidence-first-medical-writing/references/reference-verification.md) is included in every presubmission check. Audit all entries, then test priority claims against original sources; do not change the bibliography by default. The standalone skill includes the Python helper and [upstream MIT notice](skills/evidence-first-medical-writing/third-party/aperivue-verify-refs.md).
- Builds a research task card, PICO-T frame, core claim, and IMRaD outline.
- Checks alignment across the question, design, endpoint, analysis, results, and conclusion.
- Flags research-integrity and reporting risks before language polishing.
- Confirms the actual study design with the author before applying a design-specific guideline, resolving decisive missing facts instead of trusting labels.
- Retrieves applicable reporting guidelines through EQUATOR and official sources before substantive drafting or review, then records versions and item-level improvements.
- Uses task-matched JAMA design definitions and NEJM statistical guidance as references, without replacing the actual target journal's rules.
- Provides offline statistical-review profiles and checks for stable skill updates on use, with optional authorized updating of clean standalone installations.
- Briefly reminds authors to disclose AI use under the target journal's current policy and flags a conflict in the requested task, without tracking AI-use history or automatically drafting a disclosure.
- Revises titles, abstracts, sections, tables, figures, cover letters, and reviewer responses.
- Runs independent multi-reviewer simulated peer review with a separate editor, iterative revision, a Decision Ledger, and non-regression checks.
- Reconciles the final submission package across data, references, numbering, participant flow, registration, terminology, statistical summaries, eligibility, contributions, and reviewer responses.
- Offers optional authorized, de-identified data reconciliation and statistical-method checks, with anomaly triage rather than claims of fraud detection.
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

AI-assisted tasks, including reviewer-response drafting, are subject to the actual target journal's current policy. Disclosure does not make a prohibited use permissible.

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

### Release checks and optional automatic updates

Starting in 1.0.1, a chat notice identifies the skill version actually loaded once per task, independently of the network update check. The notice is not part of the manuscript or any submission file.

From 0.7.1, the skill checks for a newer official stable release once when a new task starts, if its host permits network/tools. It is not a background service. Install 0.7.1 or later once to gain this behavior; older copies cannot update themselves retroactively.

The default is **check and notify**. With your explicit opt-in, the bundled Python 3 standard-library helper can update a clean, writable standalone skill installation. It verifies the official asset identity, SHA-256 and manifests, preserves a backup, and protects local edits. Source checkouts and host-managed plugins/caches require their own update process. Missing tools, denied permissions, pins, offline mode or failed verification lead to a notification/manual link, not forced installation. Reinvoke the skill in a fresh task after an update; a frozen review keeps its original version.

See [update controls and safeguards](skills/evidence-first-medical-writing/references/updates.md) for opt-in, check-only, disable and pin commands. You can simply ask:

```text
Check this skill for updates. If this is a supported clean standalone install,
enable automatic updates for future tasks; preserve backups and never overwrite
my custom edits. Otherwise show me the official update link.
```

Only release metadata and, for authorized installation, the release ZIP are requested from GitHub. Manuscripts, data, prompts and AI-use history are not sent. A real ZIP fetch may increase GitHub's download-request count; metadata-only checks do not fetch the attachment. Python is optional for manuscript work; no third-party Python package is required by the updater. Other hosts may support only checking or manual replacement, not automatic installation.

### Over-defensive scientific writing

Substantive drafting, language rewriting, manuscript revision, whole-manuscript review, simulated peer review, and final audits now distinguish necessary scientific qualifications from repetitive disclaimers. The workflow checks semantic repetition across available sections, tables, supplements, and legends, rather than counting negative words. It complements the existing AI-Like Residue Audit.

Actions are **Keep, Consolidate, Reframe, Delete, or Author decision**. Each finding identifies its location, wording, issue, scientific risk if removed, and proposed revision. Negative primary outcomes, causal limits, analysis hierarchy, safety/ethics disclosures, and qualifications needed by a standalone abstract or table are protected. No defect means no forced rewrite; no missing limitation is invented to fill a table cell. Spelling, formatting, and literal translation do not launch a full-manuscript audit.

```text
Use $evidence-first-medical-writing to revise this manuscript for over-defensive
writing. Identify repetitive caveats across sections and tables. Explain the
scientific risk before deleting any qualification; preserve my conclusions and
necessary evidence boundaries. Record retained and deleted caveats so they do
not regress in later rounds. Do not invent missing facts or limitations.
```

Included from version 0.6.0.

### Current reporting guidelines at task time

For substantive manuscript planning, drafting, rewriting, or review, the skill first discusses the actual study design with you. It explains the evidence for a proposed classification and asks only the decisive missing questions, for example who assigned treatment, how allocation worked, how participants were selected, and when study planning and outcome collection occurred. It does not assume that "random," "prospective," or "retrospective" in a title establishes the design. It reuses facts already confirmed in the task, without repeating the interview.

Once the design is confirmed, it searches the [EQUATOR library](https://www.equator-network.org/reporting-guidelines/) and follows the record to current official checklists and applicable extensions. While a design remains unresolved, only design-neutral work or provisional exploration proceeds. You do not need to request EQUATOR separately. It downloads and reads official files when supported, or reads the full official document online and states that no local file was saved.

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

### Journal guidance and AI-use disclosure

From 0.7.1, [offline statistical routing](skills/evidence-first-medical-writing/references/statistical-policy-router.md) and concise JAMA/NEJM profiles let methodological review continue when a journal site is inaccessible. They distinguish methodological concerns from target-specific compliance, including differences in causal wording, multiplicity and statistical display. Profiles have explicit source coverage/currency limits; a dated local summary is not proof of the latest policy. Current target requirements and applicable EQUATOR guidance are still verified when needed. Original guideline documents are not bundled.

From 0.7.0, the existing Guideline Manifest separates design definitions, reporting standards, target-journal requirements, optional methodological benchmarks, and AI-use policies. JAMA definitions can clarify uncertain study terminology; relevant NEJM statistical-reporting sections support clinical original-research writing/review. Neither overrides study facts, author design confirmation, or another journal's format. Supplied or inaccessible guidelines remain explicitly currency-unverified; third-party originals are not distributed in the skill.

At submission or resubmission, the skill gives a brief reminder to disclose AI use truthfully under the actual target journal's current policy. It does not maintain an AI-use log, collect a history questionnaire, or automatically prepare a disclosure draft. The author remains responsible for the disclosure. A change of target journal, article type, or requested activity triggers a check of the affected policy, not historical-use tracking.

If the requested activity conflicts with a verified policy, it warns the author and pauses that activity; disclosure is not a workaround. Unknown policies remain unverified. A basic-spelling exemption does not automatically cover substantive rewriting. No detector score or watermark result establishes an AI-use percentage, policy compliance, or exemption from truthful disclosure.

```text
Before submission, briefly remind me to disclose AI use under the target
journal's current policy. Flag a restriction that conflicts with this request,
and recheck the policy if the target or task changes. Do not track my AI-use
history, give me a history questionnaire, or automatically draft a disclosure.
```

### Optional data and statistical checks

You may provide an authorized, de-identified source/analysis dataset, data dictionary and relevant analysis outputs or code for a bounded read-only check against tables and figures. This is optional: declining or being unable to share data does not prevent writing or review. Do not upload identifying records or data you are not permitted to share; de-identification alone does not establish permission to use a hosted service.

The skill records what was actually calculated, where discrepancies occur, the analysis population and rounding rules, and what remains unverified. It can flag repeated value patterns or records across groups for source verification, but identical numbers can have legitimate explanations and are not proof of fabrication. Statistical comments distinguish wording fixes from changes requiring author approval or specialist reanalysis. Originals are preserved; no automatic exclusions, new significance-seeking analyses, external uploads or authenticity certificates are produced.

Source-data agreement and within-manuscript logic are separate results. Even when values reproduce correctly, the skill checks whether text, tables and figures use compatible populations, denominators, time points, units, directions and conclusions. The internal check still runs when raw data are unavailable.

If deeper statistical reproduction or image/data forensics is needed, it describes the required capability and suggests a human specialist or a suitable skill only after checking what is actually available. It does not install software or transfer data without permission.

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
Confirmed study design and supporting facts (if known):
Optional de-identified data check: yes / no / not available
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
│   ├── scripts/update_skill.py
│   ├── version.json
│   ├── SKILL-MANIFEST.sha256
│   ├── NOTICE.md
│   └── references/
├── scripts/validate_release.py
├── tests/
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

Evidence-First Medical Writing 1.0.1 includes seven original, offline teaching cards and separate title and abstract reader checks.

Published release: [1.0.1](https://github.com/duyi-neurooph/evidence-first-medical-writing/releases/tag/v1.0.1).

The participant-flow module draws and audits editable SVG diagrams from aggregate counts. View the English synthetic examples: [randomized trial](assets/participant-flow/randomized-trial.svg), [cohort](assets/participant-flow/cohort.svg), and [case-control](assets/participant-flow/case-control.svg). Missing or conflicting counts are flagged, not invented. See [CHANGELOG.md](CHANGELOG.md).

Download the [complete 1.0.1 ZIP](https://github.com/duyi-neurooph/evidence-first-medical-writing/releases/download/v1.0.1/evidence-first-medical-writing-1.0.1-github-global.zip). The archive includes the skill, supporting references, documentation, license and required notices.

Copyright © 2026 Yi. See [NOTICE.md](NOTICE.md).
