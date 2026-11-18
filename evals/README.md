# Evaluation suite

These prompts test transferable behavior without using private source material.

Run each prompt in a fresh context with `$evidence-first-medical-writing`. Score only observable output. A pass requires all listed criteria; partial credit should be reported separately rather than rounded up.

See:

- [results-reference-verification.md](results-reference-verification.md) for the v0.8.0 bibliography integration: mocked executable tests, real database and issuing-source checks, full-text support assessment, and presubmission routing;
- [results-0.7.1.md](results-0.7.1.md) for offline statistical forward evidence, executable updater tests, package checks and coverage limits;
- [statistical-policy-test-cases.md](statistical-policy-test-cases.md) for offline statistics, target-policy conflicts, causal wording, multiplicity, missingness and rounding controls;
- [journal-ai-disclosure-test-cases.md](journal-ai-disclosure-test-cases.md) for reminder-only AI disclosure, current-task policy conflicts, changed targets, spelling exemptions, detector-percentage traps, and journal-guidance scope controls;
- [results-0.7.0.md](results-0.7.0.md) for the actual scoped forward runs, release checks, and remaining coverage limits;
- [anti-defensive-test-cases.md](anti-defensive-test-cases.md) for contextual caveat editing, necessary-boundary controls, cross-section repetition, genre fit, and non-regression behavior;
- [results-anti-defensive-upgrade.md](results-anti-defensive-upgrade.md) for actual synthetic forward runs, the observed correction and retest, package checks, and coverage limits;
- [results-0.6.0.md](results-0.6.0.md) for the version 0.6.0 release baseline and its validation limits;
- [test-cases.md](test-cases.md) for reusable prompts and criteria;
- [multi-reviewer-test-cases.md](multi-reviewer-test-cases.md) for article-type and adversarial tests of the independent multi-reviewer workflow;
- [reporting-guideline-test-cases.md](reporting-guideline-test-cases.md) for live retrieval, selection, scope, version, and reviewer-isolation behavior;
- [final-submission-test-cases.md](final-submission-test-cases.md) for cross-file reconciliation, revision closure, missing-file boundaries, and discipline-neutral final checks;
- [design-and-data-test-cases.md](design-and-data-test-cases.md) for author-facing design clarification, optional data checks, statistical scope and cautious anomaly handling;
- [results-equator-upgrade.md](results-equator-upgrade.md) for the guideline-retrieval development stage's actual checks and coverage limits;
- [results-final-submission-upgrade.md](results-final-submission-upgrade.md) for the generalized final-check module's actual checks and coverage limits;
- [results-design-and-data-upgrade.md](results-design-and-data-upgrade.md) for the author-dialogue and optional data-audit forward runs;
- [results-0.5.0.md](results-0.5.0.md) for the version 0.5.0 release baseline and stage-specific validation limits;
- [results-0.4.0.md](results-0.4.0.md) for the version 0.4.0 validation baseline;
- [results-0.3.0.md](results-0.3.0.md) for the release baseline.

Do not place real manuscripts, patient information, confidential review material, private identity claims, or source texts in evaluation fixtures.

From 0.7.1, executable offline updater tests are available with `python3 -B -m unittest discover -s tests -v`. Validate metadata, public inventory, protected content, links and checksums with `python3 -B scripts/validate_release.py`; after intentional edits, regenerate the skill manifest followed by the root manifest with `--write-manifests`. To verify a built release, add `--archive /absolute/path/to/release.zip`. These deterministic checks are separate from model-behavior examples.
