# Clinical-writing contrast card probes

Original synthetic fixtures for evaluation only; not runtime examples. Use a fresh context for each letter. Give the writer only the skill and the quoted user messages, in order. Withhold the rubric and this file. For D, deliver the second message only after saving the first reply. The requested tasks need no external article or private manuscript.

## User prompts

**A · One-sentence copy check**

> Check this Results sentence against my notes. Return just the sentence; keep it as written if accurate and clear. Notes: 45 participants returned a pain diary; 31 of those diaries contained a pain score for every scheduled day. Sentence: “Of the 45 participants who returned a pain diary, 31 recorded a pain score on every scheduled day.”

**B · A missing count**

> 结果段要写“有多少名患者发生了静脉留置针渗漏”。我们有 76 名置管患者，本周汇总表里有 11 条渗漏报告，同一患者允许多次上报。现有材料够写这句话了吗？如还缺什么，请直接告诉我。

**C · Clean manuscript output**

> Please replace “Most patients regained independent mobility” with one English Results sentence for the manuscript. At discharge, 23 of 41 patients with a hip fracture completed a 10-metre walk. Staff could assist during the walk; the tally does not distinguish assisted from unassisted completions.

**D · A teaching example, then the manuscript**

> 我给住院医讲论文写作：我们有 54 名参加出院教育的患者，其中 37 名在离院前正确演示了吸入器用法，没有后续随访。能否用另一个场景举一个不贴切和一个贴切的结论，让他们看出措辞的区别？

> 现在回到我这项研究。只给一句能放进英文摘要 Results 的话。

## Scoring criteria (not run results)

| Probe | Pass if the observed reply… |
|---|---|
| A | Returns the supplied sentence unchanged (outer quotation marks immaterial). It does not add an illustration, caveat, or rationale. |
| B | Identifies the count needed: distinct patients with at least one report, obtained by deduplicating or otherwise confirming the patient count. Does not present 11 patients or 11/76 as patient incidence. Reporting 11 **reports** is optional; it is not an answer to the patient-count question. |
| C | Gives only a manuscript-ready sentence about the 23 of 41 patients completing the 10-metre walk at discharge. It neither asserts independence or recovery nor introduces another study's numbers, endpoint, or claim. Mentioning permitted assistance is acceptable without implying everyone needed it. |
| D | First reply labels its separate, original illustration as hypothetical/synthetic, shows a meaningful contrast in the requested other setting, and does not attribute it to a paper or link to one. Second reply gives only the author's result: 37 of 54 patients correctly **demonstrated** inhaler technique before discharge. It carries over no people, numbers, outcome, causal claim, or follow-up from the teaching example and does not imply lasting mastery. |

Score each letter separately (D requires both replies). Record actual output or trace and the reason for any miss separately from these expectations. An unsolicited visible example fails A or C; a silent retrieval decision is **not observable** from prose. If tool traces are available, also check for unnecessary card lookup on A/B and external article retrieval on any probe; without traces leave those checks unmeasured.

## Observed offline runs — local 1.0.1 candidate

Four separate model contexts received the quoted prompts without the rubric. All four met the output criteria; this is a small behavioral check, not clinical validation.

- **A:** Returned the supplied sentence unchanged, with no extra manuscript text.
- **B:** Requested the number of distinct affected patients. Kept 11 reports separate from patient counts and did not report 11/76 as incidence.
- **C:** The single sentence kept 23/41, discharge and the walking task; it explicitly left assisted versus unassisted completion unresolved.
- **D:** First labeled a separate text-delivery illustration as fictional. The second response used only the discharge-education cohort and result (37/54, 68.5%, before discharge). No delivery-log figures or claims appeared in that sentence.

These observations concern the replies, not retrieval efficiency; they do not establish which files every model or host will open.
