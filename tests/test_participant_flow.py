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


def dental_cohort():
    """Load the public fictional ledger afresh so tests cannot share mutations."""
    return json.loads((SKILL / "assets/flow-dental-records.json").read_text(encoding="utf-8"))


def panels_by_id(root):
    return {g.get("data-node"): g for g in root.iter(SVG + "g") if g.get("data-node")}


def panel_rect(panel):
    return tuple(float(panel.find(SVG + "rect").get(a)) for a in ("x", "y", "width", "height"))


def visible_text(svg):
    doc = ET.parse(svg).getroot()
    assert doc.tag == SVG + "svg"
    return " ".join("".join(el.itertext()) for el in doc.iter(SVG + "text"))


def solid_unfilled(root, expected_nodes):
    boxes = [el for el in root.iter(SVG + "rect") if el.get("stroke") not in (None, "none")]
    if len(boxes) != expected_nodes:
        raise AssertionError(f"Expected {expected_nodes} node frames, got {len(boxes)}")
    if any(box.get("fill") != "none" for box in boxes):
        raise AssertionError("Each node frame should be transparent")
    if any(el.get("stroke-dasharray") not in (None, "none") for el in root.iter()):
        raise AssertionError("A relationship still relies on a dashed or dotted line")
    return boxes


def styled_chunks(element, inherited=None):
    """Text/tails retain their own element's type weight in an editable SVG."""
    weight = element.get("font-weight", inherited)
    if element.text:
        yield element.text, weight
    for child in element:
        yield from styled_chunks(child, weight)
        if child.tail:
            yield child.tail, weight


def connector_points(element):
    if element.tag == SVG + "line":
        return [(float(element.get("x1")), float(element.get("y1"))),
                (float(element.get("x2")), float(element.get("y2")))]
    return [tuple(float(v) for v in pair.split(",")) for pair in element.get("points").split()]


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

    def assert_arrow_semantics(self, spec, path):
        """Measure the rendered arrowhead's approach, not a label or routing flag."""
        root = ET.parse(path).getroot()
        boxes = {k: panel_rect(g) for k, g in panels_by_id(root).items()}
        kinds = {n["id"]: n["kind"] for n in spec["nodes"]}
        expected = [(g["parent"], k) for g in spec["groups"] for k in g["children"]]
        arrows = [(e.get("data-from"), e.get("data-to"), connector_points(e))
                  for e in root.iter() if e.get("marker-end")]
        self.assertCountEqual([(p, k) for p, k, _ in arrows], expected)
        for p, k, points in arrows:
            with self.subTest(edge=(p, k)):
                x, y, w, h = boxes[k]
                tip = points[-1]
                previous = next(pt for pt in reversed(points[:-1]) if pt != tip)
                if kinds[k] == "exclusion":
                    self.assertGreater(x, boxes[p][0] + boxes[p][2] / 2)
                    self.assertAlmostEqual(tip[0], x, delta=.05)  # left edge
                    self.assertTrue(y < tip[1] < y + h)
                    self.assertAlmostEqual(previous[1], tip[1], delta=.05)
                    self.assertLess(previous[0], tip[0])
                else:
                    self.assertGreater(y, boxes[p][1] + boxes[p][3])
                    self.assertAlmostEqual(tip[1], y, delta=.05)  # top edge
                    self.assertAlmostEqual(tip[0], x + w / 2, delta=.05)
                    self.assertAlmostEqual(previous[0], tip[0], delta=.05)
                    self.assertLess(previous[1], tip[1])
        return boxes

    def test_shipped_examples_render_in_isolation(self):
        for name in ("flow-rct.json", "flow-cohort.json", "flow-community-bp.json",
                     "flow-observational-cohort.json", "flow-case-control.json"):
            with self.subTest(name=name):
                spec = json.loads((SKILL / "assets" / name).read_text(encoding="utf-8"))
                content, _, file = self.ready(spec)
                root = ET.parse(file).getroot()
                solid_unfilled(root, len(spec["nodes"]))
                self.assert_arrow_semantics(spec, file)
                self.assertNotRegex(content.lower(), r"\bn\s*=|dashed|dotted")
                for end in (v for v in spec["nodes"] if v["kind"] == "analysis"):
                    self.assertIn(str(end["n"]), content.replace(",", ""))

    def test_public_gallery_is_reproducible_from_shipped_fictional_ledgers(self):
        for stem, gallery in (("community-bp", "randomized-trial"), ("observational-cohort", "cohort"),
                              ("case-control", "case-control"), ("dental-records", "dental-records")):
            with self.subTest(stem=stem):
                spec = json.loads((SKILL / "assets" / f"flow-{stem}.json").read_text(encoding="utf-8"))
                self.assertIs(spec["synthetic"], True)
                _, _, svg = self.ready(spec)
                self.assertEqual(svg.read_bytes(), (SKILL.parents[1] / "assets" / "participant-flow"
                                                    / (gallery + ".svg")).read_bytes())

    def test_public_header_does_not_reprint_private_design_or_an_explicit_unit(self):
        spec = dental_cohort()
        spec["title"] = "Screening and analysis of children"
        spec["design"] = "SYNTH_INTERNAL_DESIGN_LOCATOR"
        _, report, path = self.ready(spec)
        public_svg = path.read_text(encoding="utf-8")
        self.assertNotIn(spec["design"], public_svg)
        self.assertNotIn("Counts: children", public_svg)
        self.assertIn("SYNTHETIC EXAMPLE", public_svg)
        self.assertIn(spec["design"], json.dumps(report))

    def test_trial_spine_boxes_fit_and_center_the_count_and_label_together(self):
        spec = json.loads((SKILL / "assets/flow-community-bp.json").read_text(encoding="utf-8"))
        _, _, path = self.ready(spec)
        root = ET.parse(path).getroot()
        panels = panels_by_id(root)
        rects = {k: panel_rect(g) for k, g in panels.items()}
        for key, count, label in (("screen","248","Assessed for eligibility"),
                                  ("randomized","200","Randomized")):
            with self.subTest(key=key):
                x, y, w, h = rects[key]
                lines = panels[key].findall(SVG + "text")
                self.assertEqual(len(lines), 1)
                line = lines[0]
                self.assertEqual(line.get("text-anchor"), "middle")
                self.assertIn(line.get("dominant-baseline"), ("central", "middle"))
                self.assertAlmostEqual(float(line.get("x")), x + w / 2, delta=.05)
                self.assertAlmostEqual(float(line.get("y")), y + h / 2, delta=.05)
                chunks = [(s.strip(), weight) for s, weight in styled_chunks(line) if s.strip()]
                self.assertEqual([s for s, _ in chunks], [count, label])
                self.assertIn(chunks[0][1], ("bold", "700"))
                self.assertNotIn(chunks[1][1], ("bold", "700"))
                self.assertTrue(all(s.get("x") is None for s in line.iter(SVG + "tspan")),
                                "Independent span anchors would center the words and number separately")
        sx, sy, sw, sh = rects["screen"]
        rx, ry, rw, rh = rects["randomized"]
        self.assertAlmostEqual(rw, sw, delta=.05, msg="One lane should not resize each short label independently")
        self.assertAlmostEqual(rh, sh, delta=.05)
        stem = sx + sw / 2
        self.assertAlmostEqual(stem, rx + rw / 2, delta=.05)
        wires = {(e.get("data-from"),e.get("data-to")): connector_points(e)
                 for e in root.iter() if e.get("marker-end")}
        trunk = wires["screen","randomized"]
        self.assertAlmostEqual(trunk[0][1], sy+sh, delta=.05)
        self.assertAlmostEqual(trunk[-1][1], ry, delta=.05)
        self.assertTrue(all(abs(px-stem) < .05 for px, _ in trunk))
        # A single stem/bus may supply both terminal arrows; inspect the
        # actual union of segments below, not duplicate paths at the parent.
        self.assert_centered_fork(root, "randomized", "home", "clinic")
        exclusion_rows = panels["excluded"].findall(SVG + "text")
        self.assertGreater(len(exclusion_rows), 1)
        self.assertTrue(all(row.get("text-anchor", "start") == "start" for row in exclusion_rows))

    def assert_centered_fork(self, root, parent, first, second):
        rects = {k: panel_rect(g) for k, g in panels_by_id(root).items()}
        px, py, pw, ph = rects[parent]
        cx, bottom = px + pw / 2, py + ph
        a, b = sorted((rects[first], rects[second]))
        left, right = a[0] + a[2] / 2, b[0] + b[2] / 2
        self.assertLess(a[0] + a[2], b[0])
        self.assertAlmostEqual(a[1], b[1], delta=.05)
        self.assertAlmostEqual(cx - left, right - cx, delta=.05,
                               msg="Peer status must not depend on which child shared the ledger column")
        segments = []
        for el in root.iter():
            if el.get("data-from") == parent and el.tag in (SVG + "line", SVG + "polyline"):
                pts = connector_points(el)
                segments.extend((p, q) for p, q in zip(pts, pts[1:]) if p != q)
        horizontal = [(min(p[0], q[0]), max(p[0], q[0]), p[1])
                      for p, q in segments if abs(p[1] - q[1]) < .05]
        self.assertTrue(horizontal, "No fork bar between the parent and its two children")
        bar = horizontal[0][2]
        self.assertLess(bottom, bar)
        self.assertLess(bar, a[1])
        self.assertTrue(all(abs(y-bar) < .05 for _, _, y in horizontal))
        cursor = left
        for lo, hi, _ in sorted(horizontal):
            self.assertAlmostEqual(lo, cursor, delta=.05, msg="Broken, repeated or overhanging fork bar")
            cursor = hi
        self.assertAlmostEqual(cursor, right, delta=.05)
        for x, start, end in ((cx, bottom, bar), (left, bar, a[1]), (right, bar, b[1])):
            vertical = sorted((min(p[1], q[1]), max(p[1], q[1])) for p, q in segments
                              if abs(p[0]-x) < .05 and abs(q[0]-x) < .05)
            self.assertTrue(vertical)
            cursor = start
            for lo, hi in vertical:
                self.assertAlmostEqual(lo, cursor, delta=.05, msg="Broken or duplicated vertical branch")
                cursor = hi
            self.assertAlmostEqual(cursor, end, delta=.05)

    def test_centered_dental_outcome_fork_is_independent_of_child_column_and_order(self):
        for shared_col, reverse in ((0, False), (1, True)):
            with self.subTest(shared_col=shared_col):
                spec = dental_cohort()
                # Start with the trunk aligned to one child; neither outcome
                # should be drawn as the default continuation or an exclusion.
                for n in spec["nodes"]:
                    if n["id"] in {"screen", "entry", "analyzed"}:
                        n["col"] = shared_col
                if reverse:
                    spec["groups"][-1]["children"].reverse()
                visible, audit, path = self.ready(spec)
                boxes = self.assert_arrow_semantics(spec, path)
                root = ET.parse(path).getroot()
                self.assert_centered_fork(root, "analyzed", "recorded", "absent")
                self.assertIn("children", visible)
                self.assertEqual({n["id"]: (n["n"], n["unit"]) for n in audit["nodes"]},
                                 {n["id"]: (n["n"], "children") for n in spec["nodes"]})
                panels = panels_by_id(root)
                for n in spec["nodes"]:
                    heading = panels[n["id"]].find(SVG + "text")
                    self.assertEqual([s.strip() for s, _ in styled_chunks(heading) if s.strip()],
                                     [str(n["n"]), n["label"]])
                for k in ("entry", "analyzed"):
                    self.assertAlmostEqual(boxes[k][0] + boxes[k][2] / 2,
                                           boxes["screen"][0] + boxes["screen"][2] / 2, delta=.05)
                    self.assertAlmostEqual(boxes[k][2], boxes["screen"][2], delta=.05)
                    self.assertAlmostEqual(boxes[k][3], boxes["screen"][3], delta=.05)
                self.assertGreater(boxes["removed"][3], boxes["screen"][3])

    def test_parallel_peer_with_a_wrapped_label_does_not_stretch_the_single_line_peer(self):
        spec = dental_cohort()
        label = "No sealant record in the school dental register during the final term before graduation"
        spec["nodes"][-1]["label"] = label
        _, _, path = self.ready(spec)
        root = ET.parse(path).getroot()
        panels = panels_by_id(root)
        single, multi = panels["recorded"], panels["absent"]
        first = single.findall(SVG + "text")
        wrapped = multi.findall(SVG + "text")
        self.assertEqual(len(first), 1)
        self.assertGreater(len(wrapped), 1)
        self.assertEqual(" ".join(s.strip() for row in wrapped for s, _ in styled_chunks(row) if s.strip()),
                         "326 " + label)
        self.assertEqual(panel_rect(single)[3], panel_rect(panels["analyzed"])[3])
        self.assertGreater(panel_rect(multi)[3], panel_rect(single)[3])
        self.assert_centered_fork(root, "analyzed", "recorded", "absent")
        self.assert_arrow_semantics(spec, path)

    def test_observational_figures_trace_endpoint_and_sampling_denominators(self):
        def load_example(name):
            spec = json.loads((SKILL / "assets" / name).read_text(encoding="utf-8"))
            visible, report, path = self.ready(spec)
            self.assertIs(spec["synthetic"], True)
            self.assertEqual(ET.parse(path).getroot().get("lang"), "en")
            self.assertIn("SYNTHETIC", visible)
            self.assertNotRegex(visible.lower(), r"randomi[sz]ed to|assigned to|treatment arm")
            return {n["id"]: n["n"] for n in report["nodes"]}, spec, visible.lower()

        counts, cohort_spec, _ = load_example("flow-observational-cohort.json")
        self.assertEqual(counts["enrolled"], counts["screened"] - counts["not_enrolled"])
        self.assertEqual(counts["analyzed"], counts["enrolled"] - counts["no_outcome"])
        self.assertLess(counts["analyzed"], counts["enrolled"])
        endpoint = next(n for n in cohort_spec["nodes"] if n["id"] == "analyzed")
        self.assertEqual(endpoint["kind"], "analysis")
        self.assertIn("90", endpoint["label"])

        counts, spec, _ = load_example("flow-case-control.json")
        self.assertEqual(counts["sampled"], counts["registry"] - counts["not_sampled"])
        self.assertEqual(counts["cases"] + counts["controls"], counts["sampled"])
        self.assertEqual({n["id"] for n in spec["nodes"] if n["kind"] == "analysis"}, {"cases", "controls"})
        # Replacing sampled controls with all source noncases must not pass.
        next(n for n in spec["nodes"] if n["id"] == "controls")["n"] = counts["registry"] - counts["cases"]
        self.blocked(spec)

    def test_declared_complete_partition_requires_count_conservation(self):
        spec = cohort()
        spec["nodes"][1]["n"] = 21
        self.blocked(spec)

    def test_followup_groups_below_analyzed_parent_are_both_retained(self):
        spec = dict(title="Follow-up in the analyzed cohort", design="cohort", synthetic=True, unit="patients",
                    nodes=[node("all", "Primary analysis", 80, 0, 1, "analysis"),
                           node("short", "Follow-up <90 days", 51, 1, 0, "analysis"),
                           node("long", "Follow-up ≥90 days", 29, 1, 2, "analysis")],
                    groups=[group("all", "short", "long")])
        _, _, path = self.ready(spec)
        boxes = self.assert_arrow_semantics(spec, path)
        self.assertAlmostEqual(boxes["short"][1], boxes["long"][1], delta=.05)
        self.assertLess(boxes["short"][0] + boxes["short"][2], boxes["long"][0])

    def test_mixed_partition_uses_role_not_child_order_or_lane(self):
        spec = dict(title="Cohort entry", design="cohort", synthetic=True, unit="patients",
                    nodes=[node("source", "Assessed", 93, 0, 1),
                           node("unexposed", "Unexposed at entry", 60, 2, 0, "analysis"),
                           node("excluded", "Ineligible", 13, 1, 3, "exclusion"),
                           node("exposed", "Exposed at entry", 20, 2, 2, "analysis")],
                    groups=[group("source", "exposed", "excluded", "unexposed")])
        _, _, path = self.ready(spec)
        self.assert_arrow_semantics(spec, path)

    def test_terminal_exclusion_without_a_retained_sibling_points_right(self):
        spec = dict(title="Endpoint availability by site", design="cohort", synthetic=True, unit="patients",
                    nodes=[node("eligible", "Eligible", 45, 0, 1),
                           node("site_a", "Site A, primary analysis", 39, 1, 0, "analysis"),
                           node("site_b", "Site B", 6, 1, 2),
                           node("omitted", "Excluded from analysis: records unavailable", 6, 1, 3, "exclusion")],
                    groups=[group("eligible", "site_a", "site_b"), group("site_b", "omitted")])
        for row in (1, 2):  # Either beside the source or in an offset side lane.
            with self.subTest(row=row):
                spec["nodes"][-1]["row"] = row
                _, _, path = self.ready(spec)
                self.assert_arrow_semantics(spec, path)

    def test_hostile_layout_never_yields_a_misleading_checked_or_draft_figure(self):
        for fault in ("same_row_retained", "left_exclusion"):
            spec = cohort()
            if fault == "same_row_retained":
                spec["nodes"][2].update(row=0, col=2)
            else:
                for n in spec["nodes"]:
                    n["col"] = 1 - n["col"]
            for draft in (False, True):
                with self.subTest(fault=fault, draft=draft):
                    proc, report, path = self.invoke(spec, draft)
                    if path.exists():  # A renderer may repair the layout without changing counts.
                        self.assert_arrow_semantics(spec, path)
                    else:
                        self.assertNotEqual(proc.returncode, 0)
                        self.assertNotEqual(report["status"], "ready")
                        self.assertEqual(report["figure"], "withheld")
                        self.assertTrue(any(i.get("location") and i.get("message") for i in report["issues"]))

    def test_inline_counts_and_reasons_are_bold_but_labels_are_not(self):
        spec = cohort()
        spec["nodes"][1].update(label="Excluded", reason_relation="partition", reasons=[
            dict(label="Ineligible", n=12, source="Synthetic log, R1", confirmed=True),
            dict(label="Declined", n=8, source="Synthetic log, R2", confirmed=True)])
        visible, _, path = self.ready(spec)
        root = ET.parse(path).getroot()
        solid_unfilled(root, len(spec["nodes"]))
        self.assertNotRegex(visible.lower(), r"\bn\s*=")
        self.assertIn("patients", visible.lower(), "Counting units disappeared")
        text = list(root.iter(SVG + "text"))
        for number, label in [("120", "Screened"), ("20", "Excluded"), ("12", "Ineligible"), ("8", "Declined")]:
            with self.subTest(number=number, label=label):
                matches = [el for el in text if label in "".join(el.itertext())]
                self.assertEqual(len(matches), 1)
                chunks = [(s.strip(), w) for s, w in styled_chunks(matches[0]) if s.strip()]
                self.assertEqual(chunks[0][0], number, "Count must lead the label on the same line")
                self.assertIn(chunks[0][1], ("bold", "700", "800","900"))
                self.assertTrue(any(label in s and w not in ("bold","700","800","900") for s, w in chunks[1:]))

    def test_dental_exclusion_centers_its_text_block_and_preserves_hanging_indents(self):
        # Known Arial/Helvetica advances (em) for the limited fixture
        # alphabet. An independent measurement catches a mere 'centered' flag
        # with the original left-aligned glyph coordinates.
        letters = {" ": .278, "D": .722, "M": .833, "N": .722, "a": .556,
                   "c": .5, "d": .556, "e": .556, "f": .278, "h": .556,
                   "i": .222, "l": .222, "m": .833, "n": .556, "o": .556,
                   "p": .556, "r": .333, "s": .5, "t": .278, "u": .556,
                   "v": .5, "y": .5}
        def span_extent(x, label, size, anchor):
            width = size * sum(.556 if c.isdecimal() else letters[c] for c in label)
            start = x - {"start": 0, "middle": .5, "end": 1}[anchor] * width
            return start, start + width

        for long_reason in (False, True):
            with self.subTest(long_reason=long_reason):
                spec = dental_cohort()
                reason = ("Declined the school dental visit unless a parent could attend in person"
                          if long_reason else "Declined")
                spec["nodes"][1]["reasons"][1]["label"] = reason
                _, _, path = self.ready(spec)
                panels = panels_by_id(ET.parse(path).getroot())
                screen, excluded = panels["screen"], panels["removed"]
                main_size = float(screen.find(SVG + "text").get("font-size"))
                x, y, w, h = panel_rect(excluded)
                rows = list(excluded.iter(SVG + "text"))
                if long_reason:
                    self.assertGreater(len(rows), 3)
                else:
                    self.assertEqual(len(rows), 3)
                ys, extents, parsed = [], [], []
                for row in rows:
                    rowx = float(row.get("x"))
                    size = float(row.get("font-size"))
                    self.assertEqual(size, main_size, "Excluded counts and reasons use the main body size")
                    self.assertIn(row.get("dominant-baseline"), ("central", "middle"))
                    ys.append(float(row.get("y")))
                    parts = []
                    for span in row.iter(SVG + "tspan"):
                        label = (span.text or "").strip()
                        if not label:
                            continue
                        self.assertEqual(float(span.get("font-size", size)), main_size)
                        bold = span.get("font-weight", row.get("font-weight")) in ("bold","700","800","900")
                        self.assertEqual(bold, label.isdecimal(), (label, "Only leading counts are bold"))
                        left, right = span_extent(float(span.get("x", rowx)), label, size,
                                                  span.get("text-anchor", row.get("text-anchor", "start")))
                        parts.append((label, left, right))
                        extents.append((left, right))
                    parsed.append(parts)
                self.assertEqual([p[0][0] for p in parsed[:3]], ["83", "6", "77"])
                self.assertEqual(" ".join([parsed[2][1][0], *(p[0][0] for p in parsed[3:])]), reason)
                # The short and long reason numbers share a right edge; each
                # continued line starts under the reason text, never the count.
                self.assertAlmostEqual(parsed[1][0][2], parsed[2][0][2], delta=.5)
                self.assertGreater(parsed[1][1][1], parsed[1][0][2])
                label_x = parsed[1][1][1]
                self.assertAlmostEqual(parsed[2][1][1], label_x, delta=.1)
                for parts in parsed[3:]:
                    self.assertEqual(len(parts), 1)
                    self.assertAlmostEqual(parts[0][1], label_x, delta=.1)
                left, right = min(lo for lo, _ in extents), max(hi for _, hi in extents)
                self.assertGreater(left, x)
                self.assertLess(right, x+w)
                self.assertAlmostEqual(left-x, x+w-right, delta=3,
                                       msg="Center the complete measured block, not each reason or its left margin")
                self.assertEqual(ys, sorted(set(ys)))
                self.assertGreater(ys[0]-y, main_size/2)
                self.assertAlmostEqual(ys[0]-y, y+h-ys[-1], delta=1)

    def test_exclusion_arrow_is_horizontal_from_between_two_retained_stages(self):
        for side_row in (0, 1, 2):
            with self.subTest(side_row=side_row):
                spec = cohort()
                spec["nodes"][1]["row"] = side_row
                _, _, path = self.ready(spec)
                root = ET.parse(path).getroot()
                boxes = solid_unfilled(root, len(spec["nodes"]))
                rects = [tuple(float(el.get(k)) for k in ("x","y","width","height")) for el in boxes]
                side = max(rects, key=lambda r:r[0])
                start, retained, _ = sorted((r for r in rects if r != side), key=lambda r:r[1])
                wires = [connector_points(el) for el in root.iter() if el.get("marker-end")]
                branches = [w for w in wires if abs(w[-1][0] - side[0]) < 1 and side[1] < w[-1][1] < side[1]+side[3]]
                self.assertEqual(len(branches),1, "Expected an arrow into the left edge of the excluded box")
                branch = branches[0]
                x, y = branch[0]
                self.assertTrue(all(abs(pt[1]-y)<0.01 for pt in branch), "Avoid an elbow through the exclusion lane")
                self.assertLess(x, branch[-1][0], "Exclusion arrow points to the right")
                self.assertAlmostEqual(x, start[0]+start[2]/2)
                self.assertLess(start[1]+start[3],y)
                self.assertLess(y,retained[1])
                self.assertTrue(any(abs(x-x1)<0.01 and abs(x-x2)<0.01 and min(y1,y2)<=y<=max(y1,y2)
                                    for wire in wires for (x1,y1),(x2,y2) in zip(wire,wire[1:])),
                                "The exclusion arrow must touch the retained vertical trunk")

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
        self.assertNotRegex(shown, r"[nN]\s*=|虚线|点线")
        self.assertIn("重叠", shown)

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

    def test_audit_details_are_not_published_and_a_caption_is_opt_in(self):
        spec = dental_cohort()
        spec["notes"] = ["SYNTH_INTERNAL_MEMO"]
        spec["groups"][-1]["rationale"] = "SYNTH_INTERNAL_PATH"
        for include_caption in (False, True):
            with self.subTest(include_caption=include_caption):
                caption = "A school term ended in June."
                if include_caption:
                    spec["caption"] = caption
                text, report, path = self.ready(spec)
                svg = path.read_text(encoding="utf-8")
                # Check the complete payload, including accessibility metadata
                # and XML attributes, not just what is painted on the canvas.
                for marker in ("SYNTH_INTERNAL", "Synthetic log, row", "SYNTH_LOC_"):
                    self.assertFalse(marker in svg, f"Private marker {marker!r} appeared in the exported SVG")
                self.assertIn("SYNTH_LOC_DECLINED", json.dumps(report))
                self.assertEqual(caption in text, include_caption)
                if not include_caption:
                    root = ET.parse(path).getroot()
                    last_box = max(y+h for _, y, _, h in map(panel_rect, panels_by_id(root).values()))
                    footer = [el for el in root.iter(SVG+"text") if float(el.get("y")) > last_box]
                    self.assertFalse(footer, "A simple partition with no approved caption needs no bottom note")

    def test_overlapping_dental_denominators_are_not_summed_in_the_audit_or_figure(self):
        spec = dental_cohort()
        spec["nodes"][-2].update(label="Offered varnish", n=487)
        spec["nodes"][-1].update(label="Offered sealants", n=532)
        spec["groups"][-1].update(relation="subsets", rationale="SYNTH_INTERNAL_INTERSECTION")
        text, report, path = self.ready(spec)
        last_check = next(g for g in report["checks"] if g["parent"] == "analyzed")
        self.assertEqual(last_check["relation"], "subsets")
        self.assertNotIn("children_sum", last_check)
        self.assertNotIn("1019", text.replace(",", ""))
        self.assertNotIn("SYNTH_INTERNAL_INTERSECTION", path.read_text(encoding="utf-8"))
        for value in ("764", "487", "532"):
            self.assertIn(value, text)
        self.assertRegex(text.lower(), r"overlap|non.?additive|do not add")

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
        visible, audit, path = self.ready(spec)
        self.assertIn("370", visible)
        self.assertIn("120", visible)
        self.assertIn("Unique patient key", json.dumps(audit))
        self.assertFalse("Unique patient key" in path.read_text(encoding="utf-8"),
                         "The figure must not publish the audit rationale")
        self.assertIn("encounters", visible.lower())
        self.assertIn("patients", visible.lower())
        self.assertNotRegex(visible.lower(), r"dashed|dotted|\bn\s*=")
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
