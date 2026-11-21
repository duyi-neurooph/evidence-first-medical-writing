# Changelog

## 1.0.2 — 2026-11-21

- Abstract drafting, simulated peer review and final submission checks now match actual baseline age and recorded sex/gender to the participant count in human quantitative studies. The check respects the target journal, unavailable data and justified omissions.
- Distinguish eligibility from observed age, enrollment from analysis, and a nested count from a full-cohort percentage. Request the matching aggregate data instead of inferring missing values or group membership.

## 1.0.1 — 2026-11-21

- Added bundled [writing example cards](skills/evidence-first-medical-writing/references/writing-example-cards.md) for use on demand, including offline. Positive and negative examples show when to keep sound wording and how to correct wording that misleads. All examples are synthetic; they do not supply evidence or facts for a manuscript.
- Added a title-only reader check: record what the title alone leads a reader to expect, then read the abstract on its own. Compare both readings with the actual study design and available results. Suggest the smallest correction only where the wording misleads; preserve supported facts, numbers, uncertainty and conclusions.
- Report the version of the skill actually loaded once per task in chat, separately from any update notice. Keep the version out of manuscripts and submission files.

## 0.9.1 — 2026-11-19

- Patient groups and other retained stages now receive downward arrows; only exclusions receive rightward arrows. The same rule applies when redrawing an editable figure. A shorter follow-up period is not itself an exclusion.
- Plain requests such as “按我给你的数据画 flowchart” now route to the participant-flow module without a journal name. Literature selection and nonclinical process diagrams remain separate.

## 0.9.0 — 2026-11-19

- Revised the default participant-flow drawing: solid connectors, straight side exclusions where space permits, unfilled boxes and bold leading counts. Added an English synthetic randomized trial with distinct treatment-receipt, observed-outcome and primary-analysis counts.
- Fit and center short standalone stages while keeping breakdowns aligned. Added English synthetic cohort and case-control diagrams with separate rules for follow-up completeness and control sampling.

- Added a design-aware participant-flow module for original research: create editable diagrams from sourced aggregate counts, audit denominators and exclusions, and distinguish uncertain drafts from reconciled figures. Published examples inform reporting choices; the package includes only independently designed synthetic examples.

## 0.8.0 — 2026-11-18

- Integrated standalone, read-only bibliographic verification into the existing claim-to-citation and F2 submission/resubmission checks. Separates publication identity from original-source claim support; preserves source-specific routes, incomplete-access limits and the upstream MIT notice.
- Title searches yield candidates, not proof. Compare formal records, identifiers and available metadata; report ambiguous matches, duplicate identifiers and inaccessible sources for author review. Ordinary translation and language polishing do not trigger a full audit.
- The standalone skill includes the verification helper and upstream attribution. See [acceptance results](evals/results-reference-verification.md) for offline regression tests and separate live-source checks.

## 0.7.1 — 2026-11-16

- Added offline-first statistical routing with compact JAMA and NEJM profiles. Source scope, check dates and the undated NEJM copy's currency limit are explicit; current target-policy claims still require verification, and runtime EQUATOR selection remains in place.
- Separated methodological concerns, target-journal requirements and optional benchmarks. Refined causal-language, baseline-comparison, multiplicity, missing-data, SAP chronology and precision checks without automatically changing analyses or data.
- Added an on-use stable-release check and optional, explicitly authorized updater for clean standalone skill installations, using only Python's standard library. Local customizations, managed/plugin caches and source checkouts are protected; verification, backup and rollback precede installation. Offline/check-only/disabled/pinned choices remain available.
- Added an installed-version marker, nested checksum inventory, standalone license notice, executable offline update tests, statistical evaluation cases and reproducible package validation. No background updater, manuscript telemetry, AI-use log or automatic disclosure drafting was added.
- Older installations must install 0.7.1 once to gain update checking; unsupported hosts receive a manual update link. Existing review and scientific-integrity workflows and the dated capability reminder are retained.

## 0.7.0 — 2026-11-14

- Added task-matched JAMA study-design definitions and NEJM statistical-reporting guidance, with explicit source roles in the existing Guideline Manifest. Actual study facts and the target journal's requirements remain authoritative; no third-party source originals are bundled.
- Added lightweight submission/resubmission reminders to disclose AI use under the actual target journal's current policy; no AI-use log, history questionnaire, or automatic disclosure draft.
- Added warnings for verified policy conflicts in the requested activity and bounded handling of inaccessible policies. Changed article types, targets, or requested activities trigger policy rechecking rather than historical-use tracking.
- Distinguished basic spelling/grammar exemptions from substantive assistance, author-side simulated review from commissioned confidential review, and disclosure from permission. Detector scores and watermarks do not establish an AI-use percentage or policy compliance.
- Integrated the reminder with submission and final delivery while preserving F1–F10, the five quality gates, and the existing editorial Decision Ledger.
- Added bilingual instructions and synthetic evaluation cases. Preserved the existing license, dated capability reminder, independent-review isolation, and prior features; no new runtime dependency.

## 0.6.0 — 2026-11-05

- Refined audience-calibrated explanation, critical-methods completeness, and limitation–remedy fit within the existing architecture and section playbooks. Preserved mandatory reporting information and study-specific details; corrected an overbroad rule that treated every secondary or subgroup finding as exploratory.
- Added an over-defensive scientific-writing module with eight contextual detection patterns, six decision checks, and Keep / Consolidate / Reframe / Delete / Author decision outcomes.
- Integrated prevention during drafting, minimum-change excerpt revision, semantic cross-section/table/legend audits, independent reviewer remits, editor adjudication, and persistent caveat decisions.
- Preserved scientific strength, safety/ethics disclosures, standalone reading-unit qualifications, reporting requirements, source fidelity, and the existing AI-Like Residue Audit.
- Added original general-medical paired evaluation cases, including no-edit controls and safeguards against invented limitations and regression across rounds.
- Released as a backward-compatible update; the five quality gates, independent reviewer isolation, guideline retrieval, optional data audit, license, and required notices remain in place.

## 0.5.0 — 2026-10-26

- Added an author-facing study-design confirmation gate before final guideline selection, including focused questions on allocation, selection and chronology and protection against unsupported design labels.
- Added an optional authorized, de-identified data/figure/table reconciliation and statistical-method audit, with reproducible findings, cautious anomaly triage and scoped specialist/skill escalation; data sharing is not a prerequisite and anomalies are not findings of misconduct.
- Separated source-data agreement from within-manuscript logical consistency: even reproduced values require independent cross-text/table/figure checks of populations, denominators, timing, units, directions and interpretation; the internal layer also runs without raw data.
- Added runtime EQUATOR discovery and official guideline/checklist retrieval before substantive manuscript writing, revision, and single- or multi-reviewer assessment.
- Added study-type and extension selection, live version verification, journal-edition reconciliation, readable-download checks, and bounded offline/access-failure handling.
- Added a Guideline Manifest and item-level Reporting Guideline Matrix with manuscript locations, specific improvements, author queries, and explicit assessment scope.
- Integrated the clean guideline package with reviewer isolation, frozen versions, editor adjudication, and non-regression checks; separated reporting completeness from study validity and risk of bias.
- Added a discipline-neutral final submission/resubmission audit: cross-file fact and citation reconciliation, first-mention numbering, flow counts, registry history, terminology, statistical summaries, eligibility, factual contributions, and reviewer-response closure.
- Added explicit coverage statuses and safeguards against false passes for missing files, silent data reconciliation, range-to-IQR relabelling, authorship assumptions from author order, and unverified claims of completed revisions.
- Added bilingual usage guidance and evaluation cases without bundling third-party guidelines or adding runtime dependencies.

## 0.4.0 — 2026-08-17

- Added an article-type-aware independent multi-reviewer simulated peer-review workflow with a separate editor and a sequential fallback when isolated subagents are unavailable.
- Added a Manuscript Contract, Decision Ledger, Non-Regression Checklist, Issue Matrix, response matrix, frozen-version rules, two-round defaults, and explicit stopping criteria.
- Added dedicated statistical, claim-to-citation, self-contained-writing, table, journal-compliance, and AI-like-residue audit requirements.
- Added bilingual activation guidance, a copyable end-user template, and adversarial evaluation cases for randomized, diagnostic, critical-review, and systematic-review/meta-analysis manuscripts.

## 0.3.0 — 2026-07-29

- Published and maintained under the name Yi.
- Added English-first repository documentation and a Chinese README.
- Adopted PolyForm Noncommercial License 1.0.0.
- Added a neutral public provenance and rights boundary based on diverse medical research-writing and editorial practice.
- Added privacy, terms, support, security, contribution, and rights-concern channels.
- Added English discovery metadata and English starter prompts.
- Preserved the evidence-first workflow and research-integrity guardrails from the prior internal build.
