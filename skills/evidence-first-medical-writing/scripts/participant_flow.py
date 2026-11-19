#!/usr/bin/env python3
"""Audit an aggregate participant-flow ledger and draw an original editable SVG (standard library only)."""

import argparse
from collections import Counter, defaultdict, deque
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
    if type(data.get("synthetic", False)) is not bool:
        issue("schema", "synthetic", "Expected a boolean.", True)
    if data.get("language", "en") not in ("en", "zh"):
        issue("schema", "language", "Use en or zh for generated figure labels.", True)
    if not isinstance(data.get("notes", []), list) or not all(text(n) for n in data.get("notes", [])):
        issue("schema", "notes", "Expected a list of text notes.", True)
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
        if rel == "unit_change":
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


def measure(s):
    # Approximate sans-serif advances in em; modest guard space accommodates
    # font substitution without leaving half-empty lines in English figures.
    def advance(c):
        if unicodedata.combining(c):
            return 0
        if unicodedata.east_asian_width(c) in "WF":
            return 1.03
        if c.isspace() or c in "ilI!.,:;'|":
            return .29
        if c in "frt()[]-/":
            return .37
        if c in "mwMW@%":
            return .92
        if c.isupper():
            return .74
        return .58
    return sum(map(advance, s))


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
    w, margin, gap = 280, 22, 32

    def entries(n):
        # The label hangs from the bold number, with no redundant second count line.
        result = []
        def numbered(item, size, indent):
            number = str(item["n"]) if item.get("n") is not None else "?"
            label = item["label"]
            node_unit = item.get("unit", unit)
            if node_unit != unit and node_unit.casefold() not in label.casefold():
                label = node_unit + ("，" if zh else " — ") + label
            if item.get("confirmed") is not True:
                label += unconfirmed
            hang = size*(measure(number)+.45)
            lines = wrap(label, max(5, (w-24-indent-hang)/size))
            for i, line in enumerate(lines):
                result.append((number if i == 0 else None, line, size,
                               indent if i == 0 else indent+hang))
        numbered(n, 15, 0)
        if n.get("reason_relation") == "subsets":
            result.extend((None, s, 13, 14) for s in wrap(
                "原因可重叠或未列全：" if zh else "Reasons may overlap or be incomplete:", (w-40)/13))
        for r in n.get("reasons", []):
            numbered(r, 14, 15)
        return result

    lines = {n["id"]: entries(n) for n in nodes}
    heights = {k: 15 + sum(size+4 for _,_,size,_ in vals) for k, vals in lines.items()}
    cols = {c:i for i,c in enumerate(sorted({n["col"] for n in nodes}))}
    row_rank = {r:2*i for i,r in enumerate(sorted({n["row"] for n in nodes}))}
    row = {n["id"]:row_rank[n["row"]] for n in nodes}
    occupied = {(row[k], by_id[k]["col"]) for k in by_id}
    outgoing = defaultdict(list)
    for g in data["groups"]:
        outgoing[g["parent"]].extend(g["children"])
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
    # Where only the two outer lanes share a row, the center column is an
    # anchor for the stem, not another full-width unused column of space.
    stride = w/2 + gap
    for ks in bands.values():
        ranks = sorted(cols[by_id[k]["col"]] for k in ks)
        for a,b in zip(ranks,ranks[1:]):
            stride = max(stride, (w+gap)/(b-a))
    plot = w + (len(cols)-1)*stride
    width = max(500, int(2*margin + plot + .5))
    top = wrap(data["title"], (width-2*margin)/20)
    mixed_units = any(n.get("unit", unit) != unit for n in nodes)
    unit_caption = ("计数单位：" if zh else "Counts: ") + unit
    if mixed_units:
        unit_caption += "（另有注明者除外）" if zh else " unless otherwise specified"
    meta = wrap(" · ".join(filter(None, [draft_label if draft else "",
                teaching_label if data.get("synthetic") else "", data["design"],
                unit_caption])), (width-2*margin)/12)
    pos = 26 + 25*len(top) + 17*len(meta) + 7
    boxes, compact = {}, set()
    for band in sorted(bands):
        h = max(heights[k] for k in bands[band])
        # Equal-depth arm panels share top and bottom edges even when one has
        # more lines. This keeps the two allocation arrows truly symmetric.
        parallel = len(bands[band]) > 1 and all(by_id[k]["kind"] != "exclusion" for k in bands[band])
        for k in bands[band]:
            x = (width-plot)/2 + cols[by_id[k]["col"]]*stride
            hh = h if parallel else heights[k]
            ww = w
            # Fit a short, solitary stage to its count + label. Keep parallel
            # panels and detailed lists aligned, and keep the stage on its lane.
            if len(bands[band]) == 1 and by_id[k]["kind"] != "exclusion" and len(lines[k]) == 1:
                count, label, size, _ = lines[k][0]
                ww = min(w, max(64, round(26 + size*(1.08*measure(count) + measure(" " + label)))))
                compact.add(k)
            boxes[k] = (x+(w-ww)/2, pos + (h-hh)/2, ww, hh)
        pos += h+24

    foot = []
    for g in data["groups"]:
        if g["relation"] == "subsets":
            name = by_id[g["parent"]]["label"]
            scope = (f"“{name}”的子集可能重叠或未覆盖全部对象，不应相加。" if zh else
                     f"Subsets of “{name}” may overlap or be incomplete; do not add their counts.")
        elif g["relation"] == "unit_change":
            p = by_id[g["parent"]]
            start = p.get("unit",unit)
            end = ", ".join(dict.fromkeys(by_id[k].get("unit",unit) for k in g["children"]))
            desc = g.get("rationale") or ("转换方式待确认。" if zh else "Mapping unconfirmed.")
            scope = (f"单位转换（{start} → {end}）：{desc}" if zh else f"Unit change ({start} → {end}): {desc}")
        else:
            continue
        foot.extend(wrap(scope,(width-2*margin)/12))
    for note in data.get("notes", []):
        foot.extend(wrap(note, (width-2*margin)/12))
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
    forks, tees = {}, {}
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

    for g in data["groups"]:
        p = g["parent"]
        x,y,bw,bh = boxes[p]
        for k in g["children"]:
            xx,yy,cw,ch = boxes[k]
            if by_id[k]["kind"] == "exclusion":
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
            el(canvas,"polyline",{"data-from":p,"data-to":k,
                  "points":" ".join(f"{u:g},{v:g}" for u,v in points), "fill":"none",
                  "stroke":"#444","stroke-width":1.05,"stroke-linejoin":"round","marker-end":"url(#tip)"})

    for n in nodes:
        k = n["id"]; x,y,ww,hh = boxes[k]
        box = el(canvas,"g",{"data-node":k})
        el(box,"rect",{"x":x,"y":y,"width":ww,"height":hh,"fill":"none","stroke":"#555","stroke-width":1})
        if k in compact:
            number, label, size, _ = lines[k][0]
            # Anchor the complete text chunk (not its spans) at the box center
            # so the viewer uses the actual advances of its bold and plain fonts.
            t = el(box,"text",{"x":x+ww/2,"y":y+hh/2,"font-size":size,
                               "text-anchor":"middle","dominant-baseline":"central",
                               "{http://www.w3.org/XML/1998/namespace}space":"preserve"})
            el(t,"tspan",{"font-weight":"bold"},number).tail = " "
            el(t,"tspan",{},label)
            continue
        line_y = y+6
        for number, line, size, indent in lines[k]:
            line_y += size
            t = el(box,"text",{"x":x+12+indent,"y":line_y,"font-size":size,
                               "{http://www.w3.org/XML/1998/namespace}space":"preserve"})
            if number is not None:
                el(t,"tspan",{"font-weight":"bold"},number).tail = " "
                # An explicit label anchor also fixes the hanging indent if
                # the viewer substitutes a wider or narrower numeric font.
                anchor = x+12+indent+size*(measure(number)+.45)
                el(t,"tspan",{"x":anchor},line)
            else:
                el(t,"tspan",{},line)
            line_y += 4
    for i,s in enumerate(foot):
        el(canvas,"text",{"x":margin,"y":pos+16*i,"font-size":12,"fill":"#444"},s)
    return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"


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
