#!/usr/bin/env python3
"""Audit an aggregate participant-flow ledger and draw an original editable SVG (standard library only)."""

import argparse
from collections import Counter, defaultdict, deque, namedtuple
import heapq
import json
from pathlib import Path
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET


def text(x):
    return isinstance(x, str) and bool(x.strip()) and not any(
        ord(c) < 32 and c not in "\t\r\n" or 0xD800 <= ord(c) <= 0xDFFF or ord(c) in (65534, 65535) for c in x)


def integer(x):
    return type(x) is int and x >= 0


def audit(data):
    issues, checks = [], []
    report = {"status": "invalid", "issues": issues, "checks": checks, "nodes": []}

    def issue(code, location, message, structural=False):
        issues.append(dict(code=code, location=location, message=message,
                           severity="invalid" if structural else "confirm"))

    def check_count(item, loc):
        if item.get("n") is None:
            issue("missing_count", loc, "Count not supplied; do not infer it by subtraction.")
        elif not integer(item["n"]):
            issue("invalid_count", loc, "Use a nonnegative integer or null.", True)
        if not text(item.get("source")):
            issue("missing_source", loc, "Supply the aggregate source locator.")
        if item.get("confirmed") is not True:
            issue("unconfirmed", loc, "The source/count is not confirmed.")

    if not isinstance(data, dict):
        issue("schema", "input", "Expected a JSON object.", True)
        return report
    for k in ("title", "design", "unit"):
        if not text(data.get(k)):
            issue("required_text", k, "Supply a nonblank " + k + ".", True)
    if text(data.get("design")):
        report["design"] = data["design"]
    if type(data.get("synthetic", False)) is not bool:
        issue("schema", "synthetic", "Expected a boolean.", True)
    if data.get("language", "en") not in ("en", "zh"):
        issue("schema", "language", "Use en or zh for generated figure labels.", True)
    if not isinstance(data.get("notes", []), list) or not all(text(n) for n in data.get("notes", [])):
        issue("schema", "notes", "Expected a list of text notes.", True)
    elif "notes" in data:
        report["notes"] = data["notes"]  # Private working notes, never copied to the SVG.
    if "caption" in data and not text(data["caption"]):
        issue("schema", "caption", "Omit the caption or supply nonblank publication-facing text.", True)
    raw, groups = data.get("nodes"), data.get("groups")
    if not isinstance(raw, list) or not 2 <= len(raw) <= 96 or not isinstance(groups, list):
        issue("schema", "input", "Expected 2–96 aggregate nodes and an array of relationship groups.", True)
        return report
    nodes, slots = {}, set()
    for i, n in enumerate(raw):
        location = "nodes[" + str(i) + "]"
        if not isinstance(n, dict) or not isinstance(n.get("id"), str) or not re.fullmatch(r"[A-Za-z][\w.-]{0,63}", n["id"], re.ASCII):
            issue("node_id", location, "Use a short unique ID beginning with a letter.", True)
            continue
        k = n["id"]
        if k in nodes:
            issue("duplicate_id", k, "The ID occurs twice.", True)
            continue
        nodes[k] = n
        for field in ("label", "unit"):
            if not text(n.get(field, data.get("unit") if field == "unit" else None)):
                issue("required_text", k, "Missing or invalid " + field + ".", True)
        if n.get("kind") not in ("main", "analysis", "exclusion"):
            issue("kind", k, "Choose main, exclusion or analysis.", True)
        if not all(integer(n.get(f)) and n[f] <= 99 for f in ("row", "col")):
            issue("layout", k, "row and col must be integers from 0 to 99.", True)
        else:
            slot = (n["row"], n["col"])
            if slot in slots:
                issue("layout", k, "Two boxes occupy the same grid cell.", True)
            slots.add(slot)
        check_count(n, k)
        rec = {f: n.get(f) for f in ("id", "label", "n", "source", "confirmed")}
        rec["unit"] = n.get("unit", data.get("unit"))
        report["nodes"].append(rec)
        if "reasons" in n or "reason_relation" in n:
            reasons, relation = n.get("reasons"), n.get("reason_relation")
            if not isinstance(reasons, list) or not reasons or relation not in ("partition", "subsets"):
                issue("reasons", k, "Give a nonempty reason list and declare partition or subsets.", True)
                continue
            rec.update(reasons=[], reason_relation=relation)
            for ri, r in enumerate(reasons):
                loc = f"{k}.reasons[{ri}]"
                if not isinstance(r, dict) or not text(r.get("label")) or r.get("unit", rec["unit"]) != rec["unit"]:
                    issue("reason_label_unit", loc, "Give each reason a label and use the node's unit.", True)
                    continue
                check_count(r, loc)
                rec["reasons"].append({f: r.get(f) for f in ("label", "n", "source", "confirmed")})
                if relation == "subsets" and integer(r.get("n")) and integer(n.get("n")) and r["n"] > n["n"]:
                    issue("subset_exceeds_parent", loc, "A reason count exceeds this node's denominator.")
            if relation == "partition" and integer(n.get("n")) and all(isinstance(r,dict) and integer(r.get("n")) for r in reasons):
                total = sum(r["n"] for r in reasons)
                if total != n["n"]:
                    issue("reason_partition_mismatch", k, f"Reported {n['n']}; complete disjoint reasons total {total}.")
    if not any(n.get("kind") == "analysis" for n in nodes.values()):
        issue("missing_analysis", "nodes", "Identify the final named analysis population and its count.")
    children, parents, edges = defaultdict(list), Counter(), set()
    for i, group in enumerate(groups):
        loc = "groups[" + str(i) + "]"
        if not isinstance(group, dict):
            issue("group", loc, "Expected a relationship object.", True)
            continue
        p, kids, rel = group.get("parent"), group.get("children"), group.get("relation")
        if not isinstance(p, str) or p not in nodes or not isinstance(kids, list) or not kids or not all(
                isinstance(k, str) and k in nodes for k in kids):
            issue("unknown_node", loc, "Parent and every child must exist.", True)
            continue
        if rel not in ("partition", "subsets", "unit_change"):
            issue("relation", loc, "Specify partition, subsets or unit_change.", True)
            continue
        if rel == "unit_change" and not text(group.get("rationale")):
            issue("unit_rationale", loc, "Explain the mapping between the counting units.",
                  group.get("rationale") is not None and not isinstance(group.get("rationale"), str))
        parent = nodes[p]
        pu = parent.get("unit", data.get("unit"))
        for k in kids:
            child = nodes[k]
            if (p, k) in edges:
                issue("duplicate_edge", loc, "A connection is repeated.", True)
            edges.add((p, k)); children[p].append(k); parents[k] += 1
            if integer(parent.get("row")) and integer(child.get("row")):
                if child.get("kind") != "exclusion" and child["row"] <= parent["row"]:
                    issue("retained_layout", k, f"Place retained stage {k} below {p} (a later row); put parallel groups in separate columns. Do not change the disposition.", True)
                elif child["row"] < parent["row"]:
                    issue("backwards_layout", k, "Place the exclusion at its source stage or in a later row.", True)
            if (child.get("kind") == "exclusion" and integer(parent.get("col")) and
                    integer(child.get("col")) and child["col"] <= parent["col"]):
                issue("exclusion_layout", k, f"Place the exclusion {k} in a column to the right of {p}. Do not change the disposition.", True)
            cu = child.get("unit", data.get("unit"))
            if (rel == "unit_change") == (cu == pu):
                issue("unit_mismatch", p + " -> " + k, "Use unit_change only where units actually change.", True)
            if rel == "subsets" and pu == cu and integer(child.get("n")) and integer(parent.get("n")) and child["n"] > parent["n"]:
                issue("subset_exceeds_parent", k, "A subset exceeds its own denominator.")
        entry = {"parent": p, "children": kids, "relation": rel}
        if rel == "partition" and all(integer(nodes[k].get("n")) for k in [p, *kids]):
            total = sum(nodes[k]["n"] for k in kids)
            entry.update(parent_n=parent["n"], children_sum=total)
            if total != parent["n"]:
                issue("partition_mismatch", loc, f"{p}: reported {parent['n']}, complete disjoint children total {total}.")
        if "rationale" in group:
            entry["rationale"] = group.get("rationale")
        checks.append(entry)
    roots = [k for k in nodes if not parents[k]]
    for k in nodes:
        if parents[k] > 1:
            issue("pooled_denominator", k, "Cannot infer a pooled denominator; keep separate terminal nodes and document a source-confirmed pooled total separately.", True)
    if len(roots) != 1:
        issue("root", "groups", "Expected one connected starting population.", True)
    order = deque(roots)
    count = 0
    while order:
        node = order.popleft(); count += 1
        for k in children[node]:
            parents[k] -= 1
            if not parents[k]:
                order.append(k)
    if count != len(nodes):
        issue("cycle", "groups", "Participant-flow stages must not contain cycles.", True)
    for k, n in nodes.items():
        if not children[k] and n.get("kind") == "main":
            issue("unresolved_branch", k, "The branch ends without disposition or a named analysis population.")
    report["status"] = ("invalid" if any(x["severity"] == "invalid" for x in issues) else
                        "needs_confirmation" if issues else "ready")
    return report


# Nominal Helvetica advances in thousandths of an em, ASCII space through ~.
# Arial shares these metrics for ordinary Latin text; CJK glyphs occupy one em.
# The SVG still contains live text, not outlines or stretched textLength runs.
ASCII_ADVANCES = (
    278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,
    556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,
    1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,
    667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,
    333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,
    556,556,333,500,278,556,500,722,500,500,500,334,260,334,584)


def measure(s):
    total = 0
    for c in unicodedata.normalize("NFD", s):
        if 32 <= ord(c) <= 126:
            total += ASCII_ADVANCES[ord(c)-32]
        elif unicodedata.combining(c) or unicodedata.category(c) == "Cf":
            continue
        elif unicodedata.east_asian_width(c) in "WF" or c in "—…":
            total += 1000
        else:
            total += 278 if c.isspace() else 600
    return total / 1000


def wrap(s, width):
    out = []
    for paragraph in s.splitlines() or [""]:
        line = ""
        for token in re.findall(r"\s+|[\u3400-\u9fff\uf900-\ufaff]|[^\s\u3400-\u9fff\uf900-\ufaff]+", paragraph):
            if measure(line + token) > width and line.strip():
                out.append(line.rstrip()); line = ""
            if not line and token.isspace():
                continue
            for c in token:
                if line and measure(line + c) > width:
                    out.append(line.rstrip()); line = ""
                line += c
        if line.strip():
            out.append(line.rstrip())
    return out or [""]


def unit_is_named(unit, *labels):
    """Suppress a redundant legend only for recognizable unit wording."""
    unit = unit.casefold().strip()
    if not unit.isascii():
        # A single Han character such as 人 also occurs in unrelated words.
        # For such counters require a delimited or numeric use, not 人工….
        if len(unit) == 1:
            return any(re.search(r"(?:^|[\s（(：:\d])" + re.escape(unit) +
                                 r"(?:$|[\s）)，。,:：])", s) for s in labels)
        return any(unit in s.casefold() for s in labels)
    words = unit.split()
    last = words[-1]
    pairs = (("child","children"), ("person","people"), ("woman","women"), ("man","men"),
             ("analysis","analyses"), ("tooth","teeth"), ("foot","feet"))
    forms = {last}
    for pair in pairs:
        if last in pair:
            forms.update(pair)
            break
    else:
        if last.endswith("ies"):
            forms.add(last[:-3]+"y")
        elif last.endswith(("ches", "shes", "xes", "sses")):
            forms.add(last[:-2])
        elif last.endswith("s") and not last.endswith(("ss", "is", "us")):
            forms.add(last[:-1])
        elif last.endswith("y") and len(last) > 1 and last[-2] not in "aeiou":
            forms.add(last[:-1]+"ies")
        else:
            forms.add(last+("es" if last.endswith(("ch", "sh", "x", "ss")) else "s"))
    pattern = r"(?<!\w)(?:" + "|".join(re.escape(" ".join(words[:-1]+[x])) for x in forms) + r")(?!\w)"
    return any(re.search(pattern, s.casefold()) for s in labels)


class LayoutError(ValueError):
    """A direction-preserving drawing needs different layout cells."""


def ortho(a, b, boxes, edge):
    """Route on channels around boxes; a bend costs a little more than a shared straight segment."""
    obstacles = [(x-6, y-6, x+w+6, y+h+6) for x, y, w, h in boxes]
    xs = sorted({a[0], b[0], *(x for l, t, r, d in obstacles for x in (l, r))})
    ys = sorted({a[1], b[1], *(y for l, t, r, d in obstacles for y in (t, d))})
    start, end = (xs.index(a[0]), ys.index(a[1])), (xs.index(b[0]), ys.index(b[1]))
    heap = [(0, *start, 0)]; prev = {}; distances = {(*start, 0): 0}
    while heap:
        cost, i, j, axis = heapq.heappop(heap)
        state = (i, j, axis)
        if cost != distances[state]:
            continue
        if (i, j) == end:
            line = []
            while state is not None:
                line.append((xs[state[0]], ys[state[1]])); state = prev.get(state)
            line.reverse()
            return line
        x, y = xs[i], ys[j]
        for ni, nj, direction in ((i-1,j,1),(i+1,j,1),(i,j-1,2),(i,j+1,2)):
            if not (0 <= ni < len(xs) and 0 <= nj < len(ys)):
                continue
            xx, yy = xs[ni], ys[nj]
            if any((t < y < d and max(x,xx) > l and min(x,xx) < r if direction == 1 else
                    l < x < r and max(y,yy) > t and min(y,yy) < d) for l,t,r,d in obstacles):
                continue
            next_cost = cost + abs(xx-x) + abs(yy-y) + (28 if axis and axis != direction else 0)
            new = (ni, nj, direction)
            if next_cost < distances.get(new, float("inf")):
                distances[new] = next_cost; prev[new] = (i,j,axis)
                heapq.heappush(heap, (next_cost, *new))
    raise LayoutError(edge)


def clear_segment(a, b, boxes, skip):
    """Test a candidate straight connector against non-endpoint box interiors."""
    for key, (x, y, w, h) in boxes.items():
        if key in skip:
            continue
        lo, hi = 0.0, 1.0
        for origin, delta, low, high in ((a[0], b[0]-a[0], x-2, x+w+2),
                                         (a[1], b[1]-a[1], y-2, y+h+2)):
            if not delta:
                if not low <= origin <= high:
                    lo, hi = 1.0, 0.0
                    break
                continue
            t, u = sorted(((low-origin)/delta, (high-origin)/delta))
            lo, hi = max(lo, t), min(hi, u)
        if lo <= hi:
            return False
    return True


def svg(data, draft=False):
    nodes = data["nodes"]
    by_id = {n["id"]: n for n in nodes}
    zh = data.get("language", "en") == "zh"
    unit = data["unit"]
    unconfirmed = "（待确认）" if zh else " (unconfirmed)"
    draft_label = "草稿：不可投稿" if zh else "DRAFT — NOT FOR SUBMISSION"
    teaching_label = "虚构数据示例" if zh else "SYNTHETIC EXAMPLE"
    margin, gap, size, leading, pad = 22, 32, 15, 20, 14
    Line = namedtuple("Line", "number label number_end label_start")

    def number(item):
        return str(item["n"]) if item.get("n") is not None else "?"

    def advance(s):
        return size * measure(s)

    # One column measure for the entire figure, including short solitary stages.
    # Leave room for a long reported count instead of ever truncating its digits.
    w = max(280, 2*pad+size*6+max(advance(number(i)) for n in nodes for i in [n, *n.get("reasons", [])]))

    def entries(n):
        result = []
        reasons = n.get("reasons", [])
        reason_indent = 12
        def numbered(item, count_end, item_unit):
            label = item["label"]
            if item_unit != unit and item_unit.casefold() not in label.casefold():
                label = item_unit + ("，" if zh else " — ") + label
            if item.get("confirmed") is not True:
                label += unconfirmed
            start = count_end + advance(" ")
            for i, line in enumerate(wrap(label, (w-2*pad-start)/size)):
                result.append(Line(number(item) if i == 0 else None, line, count_end, start))
        node_unit = n.get("unit", unit)
        numbered(n, advance(number(n)), node_unit)
        if n.get("reason_relation") == "subsets":
            for s in wrap("原因可重叠或未列全：" if zh else "Reasons may overlap or be incomplete:",
                          (w-2*pad-reason_indent)/size):
                result.append(Line(None, s, 0, reason_indent))
        if reasons:
            count_end = reason_indent + max(advance(number(r)) for r in reasons)
            for r in reasons:
                # All counts share a right edge, including 1 vs. 3 digits;
                # wrapped labels continue under their own word, not the number.
                numbered(r, count_end, r.get("unit", node_unit))
        return result

    lines = {n["id"]: entries(n) for n in nodes}
    heights = {k: 36 + leading*(len(vals)-1) for k, vals in lines.items()}
    row_rank = {r:2*i for i,r in enumerate(sorted({n["row"] for n in nodes}))}
    row = {n["id"]:row_rank[n["row"]] for n in nodes}
    occupied = {(row[k], by_id[k]["col"]) for k in by_id}
    outgoing, parent_of = defaultdict(list), {}
    for g in data["groups"]:
        outgoing[g["parent"]].extend(g["children"])
        parent_of.update((k, g["parent"]) for k in g["children"])
    # Put a side exclusion between its source and the next retained stage even
    # for older ledgers that positioned it on the source or destination row.
    tee_candidates = defaultdict(list)
    for p, kids in outgoing.items():
        retained = [k for k in kids if by_id[k]["kind"] != "exclusion"]
        if not retained:
            continue
        first = min(row[k] for k in retained)
        for k in kids:
            c = by_id[k]["col"]
            if by_id[k]["kind"] != "exclusion" or k in outgoing or not row[p] <= row[k] <= first:
                continue
            mid = row[k] if row[p] < row[k] < first else (row[p]+first)//2
            if mid != row[k] and (mid,c) in occupied:
                continue
            occupied.remove((row[k],c)); row[k] = mid; occupied.add((mid,c))
            tee_candidates[p].append(k)

    bands = defaultdict(list)
    for k in by_id:
        bands[row[k]].append(k)
    # A ledger column orders siblings; it is not the physical center of an
    # upstream population. Anchor every single-retained-stage chain on the
    # downstream fork's midpoint, even when its input col equals a child's.
    # Work from the leaves up so a nested split has room for its own exits.
    def subtree(p):
        centers = {p: 0}
        kids = sorted(outgoing.get(p, ()), key=lambda k: (by_id[k]["col"], row[k], k))
        retained = [k for k in kids if by_id[k]["kind"] != "exclusion"]
        sides = [k for k in kids if by_id[k]["kind"] == "exclusion"]
        positions, branches = [], []
        for k in retained:
            branch = subtree(k)
            x = (positions[-1] + max(branches[-1].values()) - min(branch.values()) + w + gap
                 if branches else 0)
            positions.append(x); branches.append(branch)
        if positions:
            middle = (positions[0] + positions[-1])/2
            for x, branch in zip(positions, branches):
                centers.update((k, x+dx-middle) for k,dx in branch.items())
        for k in sides:
            branch = subtree(k)
            x = w+gap
            # A right-hand exit may occupy the space above its downstream
            # arm, but it must not share a band with any overlapping frame.
            # If a later exclusion lies between a retained parent and child,
            # also leave that direct vertical lane clear.
            for v, dx in branch.items():
                for other, ox in centers.items():
                    if row[other] == row[v]:
                        x = max(x, ox+w+gap-dx)
                    par = parent_of.get(other)
                    if (par in centers and row[par] < row[v] < row[other]
                            and centers[par] == ox and by_id[other]["kind"] != "exclusion"):
                        x = max(x, ox+w+gap-dx)
            centers.update((v, x+dx) for v,dx in branch.items())
        return centers

    root_id = next(k for k in by_id if k not in parent_of)
    centers = subtree(root_id)
    left, right = min(centers.values())-w/2, max(centers.values())+w/2
    width = max(500, int(2*margin + right-left + .99))
    origin = (width-right-left)/2
    top = wrap(data["title"], (width-2*margin)/20)
    mixed_units = any(n.get("unit", unit) != unit for n in nodes)
    unit_caption = ""
    if mixed_units or not unit_is_named(unit, data["title"], by_id[root_id]["label"]):
        unit_caption = ("计数单位：" if zh else "Counts: ") + unit
    if mixed_units:
        unit_caption += "（另有注明者除外）" if zh else " unless otherwise specified"
    metadata = " · ".join(filter(None, [draft_label if draft else "",
                         teaching_label if data.get("synthetic") else "", unit_caption]))
    meta = wrap(metadata, (width-2*margin)/12) if metadata else []
    pos = 26 + 25*len(top) + 17*len(meta) + 7
    boxes = {}
    for band in sorted(bands):
        # Top-align retained siblings for equal downward legs. If an exit must
        # sit beside its source in this band, align their text/box midpoints.
        def offset(k):
            p = parent_of.get(k)
            if p is not None and row[p] == band:
                return offset(p) + (heights[p]-heights[k])/2
            return 0
        offsets = {k:offset(k) for k in bands[band]}
        minimum = min(offsets.values())
        h = max(offsets[k]+heights[k] for k in bands[band]) - minimum
        for k in bands[band]:
            boxes[k] = (origin+centers[k]-w/2, pos+offsets[k]-minimum, w, heights[k])
        pos += h+24

    foot = wrap(data["caption"], (width-2*margin)/12) if data.get("caption") else []
    for g in data["groups"]:
        if g["relation"] == "subsets":
            name = by_id[g["parent"]]["label"]
            scope = (f"“{name}”的子集可能重叠或未覆盖全部对象，不应相加。" if zh else
                     f"Subsets of “{name}” may overlap or be incomplete; do not add their counts.")
        elif g["relation"] == "unit_change":
            p = by_id[g["parent"]]
            start = p.get("unit",unit)
            end = ", ".join(dict.fromkeys(by_id[k].get("unit",unit) for k in g["children"]))
            scope = (f"计数单位由{start}变为{end}，不能相减。" if zh else
                     f"Counts change from {start} to {end}; the difference is not attrition.")
        else:
            continue
        foot.extend(wrap(scope,(width-2*margin)/12))
    height = int(pos + 16*len(foot) + 5)
    root = ET.Element("svg", {"xmlns":"http://www.w3.org/2000/svg", "lang":"zh" if zh else "en", "width":str(width), "height":str(height),
                             "viewBox":f"0 0 {width} {height}", "role":"img", "aria-labelledby":"figure-title figure-desc"})
    def el(parent, tag, attrs=None, value=None):
        child = ET.SubElement(parent, tag, {k:str(v) for k,v in (attrs or {}).items()})
        child.text = value
        return child
    el(root, "title", {"id":"figure-title"}, data["title"])
    el(root, "desc", {"id":"figure-desc"}, ("原创研究对象流程图。" if zh else "Original participant disposition diagram. ") + " ".join(meta + foot))
    defs = el(root, "defs")
    marker = el(defs, "marker", {"id":"tip","viewBox":"0 0 8 8","refX":8,"refY":4,
                                 "markerWidth":7,"markerHeight":7,"orient":"auto"})
    el(marker,"path",{"d":"M0 0 L8 4 L0 8 L2 4 Z","fill":"#444"})
    el(root,"rect",{"width":width,"height":height,"fill":"white"})
    canvas = el(root,"g",{"font-family":"Arial, Helvetica, sans-serif","fill":"#161616"})
    for i,s in enumerate(top):
        el(canvas,"text",{"x":margin,"y":25+25*i,"font-size":20,"font-weight":"bold"},s)
    for i,s in enumerate(meta):
        el(canvas,"text",{"x":margin,"y":25*len(top)+20+17*i,"font-size":12,"fill":"#444"},s)

    # Give retained children a common stem before the horizontal fork. Take
    # side exits off this stem only if the line really meets the retained path.
    def wire(p, points, child=None, role=None):
        attrs = {"data-from":p, "points":" ".join(f"{u:g},{v:g}" for u,v in points),
                 "fill":"none", "stroke":"#444", "stroke-width":1.05, "stroke-linejoin":"round"}
        if child is not None:
            attrs.update({"data-to":child, "marker-end":"url(#tip)"})
        if role:
            attrs["data-role"] = role
        el(canvas,"polyline",attrs)

    forks, tees, legs = {}, {}, {}
    for p, kids in outgoing.items():
        retained = [k for k in kids if by_id[k]["kind"] != "exclusion"]
        if not retained:
            continue
        x,y,bw,bh = boxes[p]; a = (x+bw/2,y+bh)
        first = min(boxes[k][1] for k in retained)
        side_exits = {}
        for k in tee_candidates[p]:
            xx,yy,cw,ch = boxes[k]; ty = yy+ch/2
            stem, side = (a[0],ty), (xx,ty)
            if a[1] < ty < first and xx > a[0] and clear_segment(stem,side,boxes,{k}):
                side_exits[p,k] = [stem,side]
        after = max([a[1]] + [path[0][1] for path in side_exits.values()])
        fork = (a[0],(after+first)/2)
        if clear_segment(a,fork,boxes,{p}):
            forks[p] = fork
            tees.update(side_exits)
            # Draw the bar and upper stem ONCE, without arrowheads. The only
            # arrowheads are at actual dispositions, never at a junction.
            tops = [(boxes[k][0]+boxes[k][2]/2, boxes[k][1]) for k in retained]
            ends = [(b[0], fork[1]) for b in tops]
            if (len(retained) >= 2 and len({b[1] for b in tops}) == 1
                    and clear_segment(min(ends),max(ends),boxes,set())
                    and all(clear_segment(end,b,boxes,{k}) for k,end,b in zip(retained,ends,tops))):
                wire(p, [a,fork], role="stem")
                wire(p, [min(ends),max(ends)], role="bus")
                for k,end,b in zip(retained,ends,tops):
                    legs[p,k] = [end,b]

    for g in data["groups"]:
        p = g["parent"]
        x,y,bw,bh = boxes[p]
        for k in g["children"]:
            xx,yy,cw,ch = boxes[k]
            if (p,k) in legs:
                points = legs[p,k]
            elif by_id[k]["kind"] == "exclusion":
                a, b = (x+bw,y+bh/2), (xx,yy+ch/2)
                if (p,k) in tees:
                    points = tees[p,k]
                elif a[1] == b[1] and a[0] < b[0] and clear_segment(a,b,boxes,{p,k}):
                    points = [a,b]
                else:
                    # An off-spine exit still enters the left edge facing right.
                    aa, bb = (a[0]+8,a[1]), (b[0]-8,b[1])
                    points = [a,*ortho(aa,bb,boxes.values(),(p,k)),b]
            else:
                a, b = (x+bw/2,y+bh), (xx+cw/2,yy)
                if a[0] == b[0] and clear_segment(a,b,boxes,{p,k}):
                    points = [a,b]
                else:
                    fork = forks.get(p,(a[0],a[1]+8)); turn = (b[0],fork[1])
                    if (clear_segment(fork,turn,boxes,{p,k}) and
                            clear_segment(turn,b,boxes,{p,k})):
                        points = [a,fork,turn,b]
                    else:
                        # End with a vertical segment even when boxes obstruct
                        # the usual fork; never replace it with a diagonal.
                        points = [a,*ortho(fork,(b[0],b[1]-8),boxes.values(),(p,k)),b]
            wire(p, points, child=k)

    for n in nodes:
        k = n["id"]; x,y,ww,hh = boxes[k]
        box = el(canvas,"g",{"data-node":k})
        el(box,"rect",{"x":x,"y":y,"width":ww,"height":hh,"fill":"none","stroke":"#555","stroke-width":1})
        if len(lines[k]) == 1:
            item = lines[k][0]
            # Anchor the complete text chunk (not its spans) at the box center
            # so the viewer uses the actual advances of its bold and plain fonts.
            t = el(box,"text",{"x":x+ww/2,"y":y+hh/2,"font-size":size,
                               "text-anchor":"middle","dominant-baseline":"central",
                               "{http://www.w3.org/XML/1998/namespace}space":"preserve"})
            el(t,"tspan",{"font-weight":"bold"},item.number).tail = " "
            el(t,"tspan",{},item.label)
            continue
        # Center the bounding block, not a guessed-width column and not each
        # line separately. Counts, labels and continuations stay aligned inside it.
        rows = lines[k]
        left = min(item.number_end-advance(item.number) if item.number else item.label_start for item in rows)
        right = max(item.label_start+advance(item.label) for item in rows)
        block_x = x+(ww-left-right)/2
        first_y = y+(hh-(len(rows)-1)*leading)/2
        for i,item in enumerate(rows):
            count_start = block_x+item.number_end-advance(item.number) if item.number is not None else None
            t = el(box,"text",{"x":count_start if count_start is not None else block_x+item.label_start,
                               "y":first_y+i*leading,
                               "dominant-baseline":"central", "font-size":size,
                               "{http://www.w3.org/XML/1998/namespace}space":"preserve"})
            if item.number is not None:
                # Align the end of the tabular digits using their advances.
                # Mixing end/start anchoring inside one editable text element
                # can make SVG importers apply the end anchor to its labels.
                el(t,"tspan",{"x":count_start,"font-weight":"bold"},item.number).tail = " "
            el(t,"tspan",{"x":block_x+item.label_start},item.label)
    for i,s in enumerate(foot):
        el(canvas,"text",{"x":margin,"y":pos+16*i,"font-size":12,"fill":"#444"},s)
    # Keep the gallery's XML declaration byte-identical across Python versions.
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True).decode("utf-8") + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--svg", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--draft", action="store_true", help="draw an explicitly marked working figure even with unresolved counts")
    args = parser.parse_args(argv)
    try:
        if args.svg.resolve() == args.audit.resolve() or any(p.exists() or p.is_symlink() for p in (args.svg, args.audit)):
            parser.error("Choose two separate new output filenames; no file is overwritten.")
        data = json.loads(args.input.read_text(encoding="utf-8"))
        report = audit(data)
        diagram = None
        if report["status"] == "ready" or args.draft and report["status"] == "needs_confirmation":
            try:
                diagram = svg(data,args.draft)
            except LayoutError as exc:
                p,k = exc.args[0]
                report["status"] = "invalid"
                report["issues"].append(dict(code="blocked_connector", location=f"{p} -> {k}",
                    message="Leave a clear lane for the connector: retained groups below, exclusions to the right. Change layout cells, not dispositions or counts.",
                    severity="invalid"))
        report["figure"] = ("draft" if args.draft else "checked") if diagram else "withheld"
        with args.audit.open("x", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False); f.write("\n")
        if diagram:
            with args.svg.open("x", encoding="utf-8") as f:
                f.write(diagram)
        print(report["status"] + ": " + str(len(report["issues"])) + " issue(s); figure " + report["figure"])
        return 0 if report["status"] == "ready" else 2
    except (OSError, ValueError) as exc:
        parser.exit(2, "Participant flow: " + str(exc) + "\n")


if __name__ == "__main__":
    sys.exit(main())
