# Reporting-guideline upgrade validation

Date: 2026-10-26

Base: `7642b9e` (published 0.4.0). Branch: `feature/equator-guideline-retrieval`.

Status: development validation for proposed 0.5.0; not a release announcement.

## Static and integration checks (initial guideline-retrieval batch)

- Skill frontmatter/structure validation: passed.
- Plugin JSON parsing and Git whitespace checks: passed.
- Local Markdown links: 30 files checked, no missing targets.
- SHA-256 distribution manifest: regenerated and verified against the working package.
- Independent read-only integration review covered the entry point, guideline reference, study-type/audit hooks, and multi-reviewer contract. It found one contradictory section-rewrite instruction (“Load only the matching playbook”); this was changed to require the common guideline step before the section playbook.
- Published version metadata remains 0.4.0; the changelog explicitly identifies the proposed 0.5.0 work as unreleased.

## Independent forward tests actually run

Two fresh evaluator contexts received the skill path and realistic synthetic user requests, without evaluation criteria, expected answers, or other reviewers' findings. They did not edit the repository.

### G1 — Live randomized-trial Methods revision: pass

The request did not mention EQUATOR. The evaluator identified the trial-report scope and opened EQUATOR, the issuing group's site, the extensions listing, and the published statement before producing a revision.

Observed retrieval evidence:

- [EQUATOR CONSORT record](https://www.equator-network.org/reporting-guidelines/consort/)
- [Official issuing site](https://www.consort-spirit.org/)
- [Published CONSORT 2025 statement](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004587)
- [Official expanded checklist](https://www.consort-spirit.org/_files/ugd/b5740e_a6856e5e2cf94a1db5a8005853404160.pdf)

The short-checklist link failed; the official expanded checklist succeeded. The evaluator downloaded a 12-page PDF to a temporary task directory, verified the file type, and extracted/read the text including item tables and footnotes. SHA-256: `2989ad489eba838dc116cec52b8cf53341a99598835ff9707fb1a814070130b8`. The statement and expanded checklist were read; the separate full explanation/elaboration article was not read beyond its landing page. The latter limit was disclosed. The document itself is not distributed in this repository.

The response cited verified CONSORT 2025 items, recorded source/version/date, and limited judgments to the supplied paragraph. It preserved the 120 adults, individual 1:1 randomization, 12-week follow-up, inability to blind the intervention, and prespecified symptom-score endpoint. It did not infer equal realized group sizes, completed follow-up, assessor blinding, analysis methods, or registration. Missing information remained explicit author queries, not invented methods or a whole-manuscript compliance claim.

These are observations on the test date, not a permanent assertion that a version or download URL is current.

### G2 — Offline Critical Perspective abstract: pass

The evaluator honored the explicit no-network instruction, disclosed that current guidance was not retrieved or verified, and did not assert that no applicable guideline exists. It did not force PRISMA, a systematic search, statistical pooling, or invented checklist identifiers onto a Perspective.

It located the overbroad “all patients” claim, suggested narrowing the population/outcome claim, asked the author to clarify the article's actual argument and selection of representative evidence, and distinguished an abstract-only assessment from unavailable full-text or journal checks. The response was labelled simulated peer review and made no full-manuscript acceptance or compliance claim.

## Coverage limits

The other cases in [reporting-guideline-test-cases.md](reporting-guideline-test-cases.md) are reusable evaluation specifications, not claimed executions. Protocol, diagnostic, prediction, review-subtype, older-journal-edition, and artificial login-page cases have not each received a separate live behavioral run in this change. Reviewer isolation and frozen-guideline integration received code/instruction review, not a new full two-round manuscript trial. Host tools, network availability, official-site changes, and document extraction quality can still limit runtime retrieval.
