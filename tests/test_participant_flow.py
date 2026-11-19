"""Offline CLI acceptance: follow real participant-flow decisions using invented counts."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET


SKILL = Path(__file__).resolve().parents[1] / "skills" / "evidence-first-medical-writing"
SCRIPT = SKILL / "scripts" / "participant_flow.py"
SVG = "{http://www.w3.org/2000/svg}"


def node(key, label, n, row, col, kind="main", **kwargs):
    return dict(id=key, label=label, n=n, row=row, col=col, kind=kind,
                confirmed=True, source="Synthetic log, row " + key, **kwargs)


def group(parent, *children, relation="partition", rationale=None):
    result = dict(parent=parent, children=list(children), relation=relation)
    if rationale is not None:
        result["rationale"] = rationale
    return result


def cohort():
    return dict(title="Eligibility and analysis", design="cohort", synthetic=True, unit="patients",
                nodes=[node("assessed", "Screened", 120, 0, 0),
                       node("excluded", "Age criterion not met", 20, 1, 1, "exclusion"),
                       node("included", "Eligible", 100, 2, 0),
                       node("primary", "Primary analysis", 100, 3, 0, "analysis")],
                groups=[group("assessed", "included", "excluded"),
                        group("included", "primary")])


def visible_text(svg):
    doc = ET.parse(svg).getroot()
    assert doc.tag == SVG + "svg"
    return " ".join("".join(el.itertext()) for el in doc.iter(SVG + "text"))


class ParticipantFlowCLI(unittest.TestCase):
    def setUp(self):
        data = tempfile.TemporaryDirectory(prefix="efmw-flow-acceptance-")
        self.addCleanup(data.cleanup)
        self.folder = Path(data.name)
        self.iteration = 0

    def invoke(self, spec, draft=False):
        self.iteration += 1
        base = self.folder / str(self.iteration)
        base.mkdir()
        src, svg, audit = (base / name for name in ("input.json", "figure.svg", "audit.json"))
        original = json.dumps(spec, ensure_ascii=False).encode("utf-8")
        src.write_bytes(original)
        args = [sys.executable, "-I", "-B", str(SCRIPT), str(src),
                "--svg", str(svg), "--audit", str(audit)]
        if draft:
            args.append("--draft")
        proc = subprocess.run(args, capture_output=True, text=True, timeout=15)
        self.assertEqual(src.read_bytes(), original, "Renderer modified the author's input")
        self.assertNotIn("Traceback", proc.stderr, proc.stderr)
        self.assertTrue(audit.exists(), (proc.returncode, proc.stdout, proc.stderr))
        report = json.loads(audit.read_text(encoding="utf-8"))
        return proc, report, svg

    def blocked(self, spec):
        proc, report, svg = self.invoke(spec)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn(report["status"], {"needs_confirmation", "invalid"})
        self.assertTrue(report["issues"], report)
        self.assertFalse(svg.exists(), "An unresolved ledger produced a submission figure")
        return report

    def ready(self, spec):
        proc, report, svg = self.invoke(spec)
        self.assertEqual(proc.returncode, 0, (report, proc.stderr))
        self.assertEqual(report["status"], "ready", report)
        return visible_text(svg), report, svg

    def test_both_shipped_examples_render_in_isolation(self):
        for name in ("flow-rct.json", "flow-cohort.json"):
            with self.subTest(name=name):
                spec = json.loads((SKILL / "assets" / name).read_text(encoding="utf-8"))
                content, _, _ = self.ready(spec)
                for end in (v for v in spec["nodes"] if v["kind"] == "analysis"):
                    self.assertIn(str(end["n"]), content.replace(",", ""))

    def test_declared_complete_partition_requires_count_conservation(self):
        spec = cohort()
        spec["nodes"][1]["n"] = 21
        self.blocked(spec)

    def test_chinese_paired_diagnostic_draft_keeps_the_unverified_denominator(self):
        spec = dict(title="配对诊断研究", design="前瞻性配对比较", unit="人", language="zh", synthetic=True,
                    nodes=[node("tested","两种检查均完成",90,0,0),
                           node("read_a","读法甲",90,1,0,"analysis"),
                           node("read_b","读法乙",90,1,1,"analysis"),
                           node("primary","主要分析集",None,2,0,"analysis")],
                    groups=[group("tested","read_a","read_b","primary",relation="subsets")])
        self.blocked(spec)
        proc, report, path = self.invoke(spec, draft=True)
        self.assertEqual((proc.returncode, report["figure"]), (2, "draft"))
        shown = visible_text(path)
        self.assertIn("草稿", shown)
        self.assertIn("不可投稿", shown)
        self.assertIn("?", shown)
        self.assertNotIn("180", shown)
        self.assertNotIn("DRAFT", shown)

    def test_randomized_arms_keep_observed_outcomes_separate_from_itt(self):
        spec = dict(
            title="Allocation and analysis", design="RCT", synthetic=True, unit="participants",
            nodes=[node("randomized", "Randomized", 100, 0, 1),
                   node("arm_a", "Allocated to A", 72, 1, 0),
                   node("arm_b", "Allocated to B", 28, 1, 2),
                   node("observed", "A: outcome observed", 66, 2, 0, "analysis"),
                   node("itt_a", "A: imputed ITT", 72, 2, 1, "analysis"),
                   node("itt_b", "B: ITT", 28, 2, 2, "analysis")],
            groups=[group("randomized", "arm_a", "arm_b"),
                    group("arm_a", "observed", "itt_a", relation="subsets",
                          rationale="Six missing outcomes were imputed in the documented ITT analysis."),
                    group("arm_b", "itt_b")])
        text, _, _ = self.ready(spec)
        self.assertIn("66", text)
        self.assertIn("72", text)
        spec["nodes"][2]["n"] = 29  # A 72/29 split cannot represent 100 randomized.
        self.blocked(spec)

    def test_unknown_is_neither_zero_nor_sibling_by_subtraction(self):
        spec = cohort()
        spec["nodes"][1].update(n=None, confirmed=False)
        self.blocked(spec)
        proc, rep, svg = self.invoke(spec, draft=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotEqual(rep["status"], "ready")
        visible = visible_text(svg).lower()
        self.assertRegex(visible, r"draft|草稿")
        self.assertNotRegex(visible, r"(?<!\d)20(?!\d)", "Missing count was inferred")

    def test_source_confirmation_and_discrete_counts_are_required(self):
        for field, bad in (("source", ""), ("confirmed", False), ("n", -1),
                           ("n", 20.5), ("n", True)):
            with self.subTest(field=field, bad=bad):
                spec = cohort()
                spec["nodes"][1][field] = bad
                self.blocked(spec)

    def test_zero_is_a_valid_confirmed_count(self):
        spec = cohort()
        spec["nodes"][0]["n"] = 100
        spec["nodes"][1]["n"] = 0
        self.ready(spec)

    def test_exclusion_reason_counts_have_separate_sources_and_relationship(self):
        spec = cohort()
        removed = spec["nodes"][1]
        removed.update(label="Excluded at screening", reason_relation="partition", reasons=[
            dict(label="Age outside range", n=12, source="Synthetic screen log A", confirmed=True),
            dict(label="Declined invitation", n=8, source="Synthetic screen log B", confirmed=True)])
        visible, report, _ = self.ready(spec)
        self.assertIn("12", visible)
        self.assertIn("Declined", visible)
        self.assertIn("Synthetic screen log B", json.dumps(report))
        removed["reasons"][1]["n"] = 9  # Reasons declared disjoint cannot sum to 21 of 20.
        self.blocked(spec)
        removed["reason_relation"] = "subsets"  # Same patient may meet both reasons.
        self.ready(spec)
        removed["reasons"][1]["source"] = ""
        self.blocked(spec)
        removed["reasons"][1].update(source="Unresolved log", n=None, confirmed=False)
        self.blocked(spec)

    def test_overlapping_analyses_do_not_replace_the_parent_or_get_summed(self):
        spec = cohort()
        spec["nodes"].append(node("safety", "Safety analysis", 98, 3, 1, "analysis"))
        spec["groups"][1] = group("included", "primary", "safety", relation="subsets",
                                  rationale="Safety population overlaps the primary population.")
        visible, _, _ = self.ready(spec)
        self.assertIn("98", visible)
        spec["nodes"][-1]["n"] = 101  # Each subset is bounded individually.
        self.blocked(spec)

    def test_mixed_units_do_not_make_a_valid_count_identity(self):
        spec = cohort()
        spec["nodes"][0]["unit"] = "encounters"
        self.blocked(spec)

    def test_sourced_unit_conversion_without_equality_between_counts(self):
        spec = cohort()
        spec["nodes"].insert(0, node("encounters", "Source encounters", 370, 0, 0,
                                     unit="encounters"))
        for n in spec["nodes"][1:]:
            n["row"] += 1
        spec["groups"].insert(0, group("encounters", "assessed", relation="unit_change",
                                       rationale="Unique patient key; one person per key."))
        visible, _, _ = self.ready(spec)
        self.assertIn("370", visible)
        self.assertIn("120", visible)
        spec["groups"][0]["rationale"] = 4
        proc, report, _ = self.invoke(spec, draft=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotEqual(report["status"], "ready")

    def test_unconnected_analysis_and_cycle_do_not_produce_final_figures(self):
        original = cohort()
        for fault in ("disconnected", "cycle", "duplicate_child", "missing_target"):
            with self.subTest(fault=fault):
                spec = copy.deepcopy(original)
                if fault == "disconnected":
                    spec["groups"].pop()
                elif fault == "cycle":
                    spec["groups"].append(group("primary", "assessed"))
                elif fault == "duplicate_child":
                    spec["groups"][0]["children"].append("excluded")
                else:
                    spec["groups"][0]["children"].append("absent")
                self.blocked(spec)

    def test_disjoint_arms_cannot_be_pooled_into_a_single_arm_denominator(self):
        spec = dict(title="Illustrative allocation", design="trial", unit="people",
                    nodes=[node("all", "Randomized", 100, 0, 1),
                           node("a", "A assigned", 50, 1, 0),
                           node("b", "B assigned", 50, 1, 2),
                           node("both", "Both arms, all participants analyzed", 50, 2, 1, "analysis")],
                    groups=[group("all", "a", "b"), group("a", "both"), group("b", "both")])
        self.blocked(spec)

    def test_two_languages_and_xml_signs_are_text_not_markup(self):
        spec = cohort()
        spec["nodes"][1]["label"] = "年龄 <18 & not eligible"
        _, _, svg = self.ready(spec)
        visible = visible_text(svg)
        self.assertIn("<18", visible)
        self.assertIn("年龄", visible)
        self.assertIn("&", visible)

    def test_existing_artifacts_never_overwritten(self):
        _, _, svg = self.ready(cohort())
        files = [svg, svg.with_name("input.json"), svg.with_name("audit.json")]
        before = [p.read_bytes() for p in files]
        for output in (svg, files[1], files[2]):
            with self.subTest(output=output.name):
                cmd = [sys.executable, "-I", "-B", str(SCRIPT), str(files[1]),
                       "--svg", str(output), "--audit", str(files[2])]
                result = subprocess.run(cmd, capture_output=True, timeout=15)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual([p.read_bytes() for p in files], before)

    def test_never_use_same_new_file_for_figure_and_audit(self):
        src = self.folder / "author-data.json"
        unchanged = json.dumps(cohort(), ensure_ascii=False).encode("utf-8")
        src.write_bytes(unchanged)
        target = self.folder / "new-output"
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(src),
                                 "--svg", str(target), "--audit", str(target)],
                                capture_output=True, timeout=15)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(target.exists())
        self.assertEqual(src.read_bytes(), unchanged)


if __name__ == "__main__":
    unittest.main()
