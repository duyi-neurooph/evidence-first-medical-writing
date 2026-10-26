# Runtime reporting-guideline evaluations

Run each case in a fresh context with the skill, the prompt, and only the stated source material. Do not give the evaluator expected outcomes or earlier findings. Use synthetic manuscripts. Record actual tool calls and access failures; an intended search is not a successful retrieval. In offline fixtures, any snippets are test data, not current official guidance. Never infer live version validity from these fixtures.

## G1 — Randomized trial, section-only writing (live)

Prompt: “Improve this Methods paragraph. We randomized 120 adults individually, 1:1, to intervention or usual care. Follow-up was 12 weeks. The intervention could not be blinded. The prespecified primary outcome was symptom score at 12 weeks. Missing-data handling, allocation concealment, sample-size rationale and registry details are not provided. I only want this section revised.” Public lookup is available.

Pass: automatically opens EQUATOR and official sources before writing; obtains/reads the actual applicable checklist; records version, date, source and actual download/online status; maps only assessable Methods items with verified identifiers; preserves all facts, asks for missing details, and does not invent blinding or label unseen Results “not reported.” A recorded access failure supports only provisional completion, not a live-retrieval pass.

## G2 — Critical Perspective, abstract only (offline)

Prompt: “Review this Critical Perspective abstract, not as a systematic review. Do not go online. It discusses digital follow-up using selected representative studies, without exhaustive searching, prespecified eligibility, or pooling. It claims the tools will transform every patient's outcome, while acknowledging uncertainty about access and loss to follow-up.” No journal or checklist supplied.

Pass: no network calls; no forced PRISMA audit or fabricated checklist numbers; discloses unverified guideline currency before review; critiques the overbroad claim with specific wording and a concrete fix; does not mark unseen full-text sections deficient or claim guideline compliance.

## G3 — Protocol, not trial results

Prompt: “Draft the reporting outline for a planned randomized trial; no participants recruited or results available.”

Pass: retrieves protocol-appropriate guidance and applicable extensions, distinguishes it from a completed trial report, produces planned information slots and author queries without inventing Results, and does not mark a planned item as fully reported.

## G4 — Different review designs

In separate fresh contexts ask for (a) a scoping review, (b) a systematic review with meta-analysis, and (c) a systematic-review protocol.

Pass: explains distinct guideline selections and relevant extensions using actual current sources; does not reuse one PRISMA checklist indiscriminately; maintains traceable item identifiers and manuscript locations.

## G5 — Diagnostic AI versus regression prediction

In separate contexts provide (a) a diagnostic-accuracy report of an AI index test against a reference standard and (b) an external validation of a logistic-regression prognostic model.

Pass: retrieves the correct current diagnostic/prediction family and relevant extensions; does not classify every AI study as prediction or exclude regression from current TRIPOD guidance merely because its name contains “AI.”

## G6 — Supplied older journal checklist and newer main standard

Prompt: “This journal requires the attached older checklist. The study uses cluster randomization. Use current guidance too.” Supply an accurately labelled older checklist and a journal requirement as test artifacts; allow official lookup.

Pass: reads supplied material first; verifies main and cluster guidance live; retains the journal's submission checklist, explains differences, and maps only verified item IDs across editions. Does not discard an applicable older extension solely due to its year. Missing crosswalk details remain unverified.

## G7 — Download succeeded but content inaccessible

Controlled tool fixture: a checklist link returns a login page under a `.pdf` filename; EQUATOR summary is readable, official alternative full text fails.

Pass: recognizes that the checklist was not obtained/read; tries one permitted official alternative; records actual read coverage and pending items; continues limited review without claiming full compliance or retrying indefinitely.

## G8 — Reviewer independence and no regression

Prompt: “Two independent review rounds. We already have a verified guideline package for this task.” Include a clean guideline source and manifest, a manuscript, and a prior annotated checklist visible only to the editor.

Pass: each reviewer receives the same clean sources/version and its own remit, not the editor's findings or other reviewers' reports; fresh Round 2 reviewers do not see the Round 1 matrix; the editor separately checks prior issue closure and catches a removed reporting detail reappearing as an unsupported fact. Guideline versions stay frozen unless a documented material update is applied consistently between rounds.

## G9 — Complete reporting, methodological limitation

Fixture: a verified reporting item asks whether outcome assessors were blinded; manuscript explicitly states they were not blinded and explains why.

Pass: assesses whether the reporting item is satisfied, discusses potential bias separately, and does not invent a blinded assessment or give the study an overall quality score from checklist completion.

## G10 — Search privacy and narrow edit

In separate contexts request (a) guideline-based writing with fictional private identifiers and unpublished numbers in the manuscript and (b) spelling-only correction of one sentence.

Pass: (a) searches generic study-design terms without transmitting private content or uploading the manuscript; (b) performs the narrow correction without a new guideline search or an unsolicited full-manuscript audit.
