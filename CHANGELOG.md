# Changelog

## 1.0.5 — 2026-11-22

### English

- **Statistical reporting:** Check the software and key package versions used for the reported analysis against the original analyst's records, including work done by an independent statistician or with a graphical tool. Flag unknowns; do not substitute local versions or infer AI assistance. No statistical analysis engine was added.
- **References:** Use the target journal's article-title style consistently; default to sentence case for English journal-article titles when no style is specified. Preserve proper names and scientific notation. Ordinary case differences are formatting issues, not evidence of a wrong citation.
- **Cover letters:** Follow the journal's instructions. Otherwise address the assigned editor or, if none is assigned, the verified editor-in-chief or all joint editors-in-chief. Use a neutral greeting when names cannot be verified.
- **Local updates:** An installation can opt out of retaining an old-version ZIP. Package verification and rollback during installation still apply. The default for other installations is unchanged.

### 中文

- **统计报告**：核对原分析者实际使用的软件及关键包版本，包括统计师代做和图形界面软件。缺失就标为待确认，不用本机版本代填，不推断使用过 AI；没有新增统计分析功能。
- **参考文献**：按目标期刊统一英文期刊论文题名大小写；未指定时采用句首大写，保留专名和科学符号。仅普通大小写不同属于格式问题，不算错引。
- **投稿信**：期刊有指定则遵从；否则优先称呼负责该稿的编辑。未指定时，称呼经核实的主编或全部共同主编；无法核实姓名时使用中性称呼。
- **本机更新**：可为单个安装选择不保留旧版 ZIP，仍校验新版并保留安装过程中失败回滚的能力；其他安装的默认设置不变。

## 1.0.4 — 2026-11-22

### English

- Participant flow: decide who remains in each denominator before drawing. Retained groups branch downward; only actual removals from that stage point right. Missing local records need not mean exclusion, loss to follow-up, or absence of care.
- Editable SVGs use consistent column widths, equal heights for single-line boxes, centered labels and balanced forks. Show counts first; indent exclusion reasons without shrinking their type. Use a short figure title and add a note only when necessary for interpretation.
- Keep source locators and internal review notes in the local audit, outside the figure. Examples and regression tests use fictional aggregate data.
- On hosts that did not show the installation message, the first writing task can show the localized wish in chat. It is never part of the manuscript.

### 中文

- 患者流程图先核对各阶段的分母，再决定箭头方向。仍计入分析的分组向下，只有在该阶段真正排除才向右；本机构无记录不等于排除、失访或未接受诊疗。
- 可编辑 SVG 的同列框等宽、单行框等高，文字居中，分叉对称。人数在前；排除原因用缩进区分，不缩小字号。图题尽量简短，只有影响解读时才补注。
- 来源定位和内部核对备注保留在本地审核记录里，不写入图中。示例和测试只用虚构的汇总数据。
- 平台未显示安装寄语时，首次实际写作可在对话中补发，不写入稿件。

## 1.0.3 — 2026-11-21

### English

- Default to plain submission headings, retaining informative table rules, legends and author footnotes. In statistical tables, link each reported P value to its confirmed test; place an omnibus result on the variable row. A journal’s own template or reporting rules take precedence.
- Choose P-value notation before rounding: `P < 0.001` below 0.001, three decimals from 0.001 through 0.999, and `P > 0.999` above that range but below 1. Reserve `P = 1.000` for a confirmed exact 1; ask for adequate precision rather than guessing from a threshold or rounded output.
- Report the loaded version, verified update status (or inability to check), and a brief author-responsibility reminder once per new writing task in chat. Reserve a separate localized greeting for a verified first installation or actual upgrade. Neither message goes into submission materials.
- Identify Professor Yi Du as the personal maintainer in the distributed skill. The listed affiliation does not imply institutional publication, authorization, or endorsement.

### 中文

- 投稿标题默认朴素排版，保留有信息作用的表线、图例和作者脚注。统计表中每个报告的 P 值均可对应到已确认的检验；多分类变量的总体检验标在变量行。目标期刊的模板和报告要求优先。
- 先按未舍入的 P 值选择写法：小于 0.001 写 `P < 0.001`，0.001 至 0.999（含两端）统一保留三位小数，大于 0.999 但小于 1 写 `P > 0.999`。仅在确认精确等于 1 时写 `P = 1.000`；不从阈值或软件舍入结果推测精确值。
- 每个写作新任务只在对话中提示一次实际加载版本、已核实的更新状态（或说明未能核实）及简短的作者责任提醒。确认首次安装或实际更新成功时，才另给用户惯用语言的寄语；两者都不写入投稿文件。
- 随包主说明注明 Yi Du 教授为个人维护者；机构与团队仅用于说明个人所属，不代表机构发布、授权或背书。

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
