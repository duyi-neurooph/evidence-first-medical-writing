# Over-defensive writing upgrade: development checks

Date: 2026-11-05. Baseline: released 0.5.0; review branch: `feature/anti-defensive-writing`; proposed release: 0.6.0 (unreleased). Plugin and citation metadata deliberately remain 0.5.0.

## What was implemented and reviewed

The new [reference module](../skills/evidence-first-medical-writing/references/anti-defensive-scientific-writing.md) adds contextual caveat detection, six decision checks, five editing actions, original examples, audit output, and non-regression checks. Existing routing, language/architecture guidance, independent reviewer/editor workflow, and final audits call it without replacing the five gates, AI-Like Residue Audit, guideline retrieval, or optional data checks.

Three adjacent refinements address audience-specific explanation, the defining comparison and endpoint in Methods, and whether a proposed remedy actually resolves the stated limitation. An overbroad legacy conclusion rule was corrected: secondary/subgroup results are not automatically exploratory; prespecification and the multiplicity framework govern their status.

Public examples and evaluation inputs are synthetic and cross-specialty. No private source texts, author manuscripts, unpublished study data, private source identities, or original task-document passages were added. License, rights notices, and the dated model-availability reminder are unchanged.

## Evaluation method and limits

- Executed the requests in [anti-defensive-test-cases.md](anti-defensive-test-cases.md): 22 base scenarios, six paired variants, and the two-step ledger scenario.
- Three separate Codex subagent contexts handled OD01–09, OD10–18, and OD19–22. They read the actual skill and relevant references, but not acceptance criteria, repository diffs, private source material, or each other's answers. Cases within each batch shared one context; they were instructed to reset case assumptions. This was not 22 separately isolated runs.
- The primary agent inspected the actual answers against the listed criteria. The initial grouped run had **21 passes and one partial result** (OD01: scientifically correct rewrite, missing brief rationale). All six paired variants passed. A narrow instruction correction and fresh-context retest resolved OD01; the spelling-only control also passed on retest.
- A further context executed OD15 through two actual consecutive requests, with the second request withheld until the first answer was complete. This checks short-term decision persistence; it is not a full two-round parallel-review run.
- The runtime was Codex subagents with the inherited parent configuration. An exact model identifier was not exposed in the evaluation outputs; no model-specific benchmark claim is made. Tools were limited to reading local skill files and writing synthetic answers in a temporary workspace; no external research or live journal/source verification was authorized.
- A separate read-only review compared the task, diff, routing, examples, reviewer isolation, and release boundary. It reported no actionable static findings. That reviewer did not execute or independently grade the behavioral runs.

## Observable results

Each result below describes what the generated answer actually did, not merely a keyword found in the instructions. “Pass” applies only to the supplied synthetic facts and stated acceptance criteria.

| Case | Observed behavior | Result |
|---|---|---|
| OD01 | Consolidated participant reuse and nonindependent validation. Initial answer omitted the brief diagnostic rationale required by the evaluation criterion; after correction, added: “Consolidated the repeated explanation while preserving participant reuse and the absence of independent validation or replication.” The paired case retained post hoc, secondary, exploratory, and abstract-only status. | Partial initially; pass on retest; paired pass |
| OD02 | Kept the failed prespecified primary endpoint and exploratory symptom signal without calling the treatment effective, ineffective, or equivalent. | Pass |
| OD03 | Kept association-only wording and a causal boundary because the next paragraph proposed policy change. Kept the distinct residual-confounding sentence in the reverse case. | Pass; paired pass |
| OD04 | Removed a causal/treatment-algorithm disclaimer from a fully described screening diagram; retained the unvalidated-cutoff warning for the alternative treatment graphic. | Pass; paired pass |
| OD05 | Retained the threshold warning provisionally and requested the absent figure/context; did not claim to have checked unseen sections. | Pass |
| OD06 | Mapped five supplied locations, retained the standalone abstract/table boundaries and one Discussion explanation, and removed redundant continuous-prose occurrences. Declared absent material unassessed. | Pass |
| OD07 | Used the documented missing-outcome fact, requested the analysis assumptions, and did not invent counts, power, or bias direction. Without Methods, used “Not assessed from the supplied material” or removal of an optional duplicate. | Pass; paired pass |
| OD08 | Replaced the procedural inventory in Expert Opinion with the author-approved daily-function question; retained operational requirements in Methods in the reverse case. No outcome was invented. | Pass; paired pass |
| OD09 | Preserved lower composite event rate and the supplied imprecise mortality estimate; did not claim mortality benefit or no effect. | Pass |
| OD10 | Used the known unmeasured-exacerbation boundary. When exacerbations were measured but results absent, retained a provisional evidence boundary and requested the result instead. | Pass; paired pass |
| OD11 | Kept the urgent rescue-care safeguard unchanged, explaining why the prohibition was necessary. | Pass |
| OD12 | Explicitly found no substantive defect and retained the accurate paragraph, including the 12-month period and wide interval. | Pass |
| OD13 | Reframed two-sided uncertainty as failure to establish benefit while clinically important benefit remains possible; invented no interval or threshold. | Pass |
| OD14 | Labeled the output simulated, rejected blanket causal-caveat deletion, protected the association-only author position, recorded the decisions, and requested the actual conclusion for an integrated line edit. | Pass |
| OD15 | Retained Discussion paragraph 2 and the standalone abstract boundary, kept paragraph 3 deleted, and recorded why the proposed second-step reversals were rejected. | Pass in grouped scenario; separate continuation checked |
| OD16 | Changed only “dos” to “does”; preserved the duplicate sentence under spelling-only scope. The same control passed after the change-note instruction was added. | Pass; retest pass |
| OD17 | Retained the source-supported randomized primary-result statement; did not weaken it to an association or amplify it to universal benefit/safety. | Pass |
| OD18 | Located stacked hedging at D1, gave only a provisional rewrite, requested the missing result, and kept D2's distinct publication/analysis/clinical boundaries. Used P3, not a new scientific-risk hierarchy. | Pass |
| OD19 | Removed generic disease background for specialists but retained the cohort comparison, operational emergency-visit definition, and 14-day timing. | Pass |
| OD20 | Rejected a 5–20 mg dose range, retained actual dose groups/schedule/comparator, and flagged the undefined endpoint, assessor, time, and usable manual reference without inventing them. | Pass |
| OD21 | Proposed independent validation of the 90-day readmission prediction task, not an unrelated randomized efficacy trial; linked the proposal to the unresolved performance question. | Pass |
| OD22 | Retained the confirmatory secondary endpoint under the supplied hierarchy and multiplicity procedure, while keeping the post hoc subgroup exploratory. Did not claim registration verification. | Pass |

## Iteration prompted by observed behavior

The initial OD01 answer was scientifically faithful but gave only the replacement sentence. The local-rewriting instructions now request a brief explanation of the retained boundary and redundant wording, with an explicit exception when the user wants revised text only. A fresh retest produced the concise change note quoted above; the spelling-only retest made no extra substantive changes. No mandatory audit table or whole-manuscript check was added for short edits.

The new module also explicitly preserves confirmatory secondary-outcome status, distinguishes standalone repetition from redundancy, forbids invented table limitations, and distinguishes an audit recommendation from permission to modify source files. These safeguards were reviewed in the final integration; no claim is made that file-overwrite behavior was exercised on real manuscripts.

## Static/package checks

- Bundled `skill-creator/scripts/quick_validate.py`: valid skill frontmatter/name/scaffold check, using the available system Python with PyYAML.
- `git diff --check`: no whitespace errors.
- Plugin JSON, citation YAML, agent YAML, and issue-template YAML: parsed successfully; release version remains 0.5.0 and license identifiers remain unchanged.
- Relative Markdown file targets: checked for existence across the public file inventory. Anchor correctness and external URL availability are not implied by this check.
- `FILE-MANIFEST.sha256`: regenerated for the complete public file inventory, excluding itself, and verified for both hashes and coverage.
- Public-file scope and new text were reviewed for private source identifiers, source paths, specialty-specific task material, and raw manuscript/source inclusion. No such additions were found.
- The repository has no existing executable validation/lint/test scripts or CI workflow to run. The commands above and behavioral cases are development checks, not a new runtime dependency or automated model-test harness.

## Not established by this run

These small synthetic cases do not establish performance on arbitrary full manuscripts or in every host/model. They do not revalidate live EQUATOR retrieval, current journal rules, numerical data reconciliation, tracked-change file generation, or genuinely isolated multi-reviewer orchestration end to end. Existing routing and reviewer isolation were inspected statically; the supplied-reviewer conflict case exercised adjudication, not a newly generated clinical review panel. No clinical or statistical sign-off, source-authenticity guarantee, or AI-authorship detection claim is made.

No merge, tag, release, or replacement of the published ZIP is part of this change. The maintainer should review the PR and proposed 0.6.0 notes before release preparation.
