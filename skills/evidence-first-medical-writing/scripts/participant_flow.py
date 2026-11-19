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
            if integer(parent.get("row")) and integer(child.get("row")) and child["row"] < parent["row"]:
                issue("backwards_layout", k, "Arrange successive stages down the page or beside their parent.", True)
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
    # Conservative em widths keep text editable without measuring local fonts.
    return sum(0 if unicodedata.combining(c) else 1.05 if unicodedata.east_asian_width(c) in "WF" or c in "MW@%"
               else .8 if c.isupper() else .64 if not c.isspace() else .35 for c in s)


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


def ortho(a, b, boxes):
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
    raise ValueError("No clear channel for a connector; change the row/column arrangement.")


def svg(data, draft=False):
    nodes = data["nodes"]
    zh = data.get("language", "en") == "zh"
    unconfirmed = "（待确认）" if zh else " (unconfirmed)"
    draft_label = "草稿：不可投稿" if zh else "DRAFT — NOT FOR SUBMISSION"
    teaching_label = "虚构数据示例" if zh else "SYNTHETIC EXAMPLE"
    cols = sorted({n["col"] for n in nodes}); rows = sorted({n["row"] for n in nodes})
    w, margin, gap = 252, 36, 40
    width = max(560, 2*margin + len(cols)*w + (len(cols)-1)*gap)
    plot = len(cols)*w + (len(cols)-1)*gap
    unit = data["unit"]
    labels = {n["id"]: wrap(n["label"], (w-32)/16) for n in nodes}
    counts = {n["id"]: wrap(("n = " + (str(n["n"]) if n.get("n") is not None else "?") + " " +
                              n.get("unit", unit) + (unconfirmed if n.get("confirmed") is not True else "")),
                             (w-32)/15) for n in nodes}
    reasons = {}
    for n in nodes:
        rs = []
        if n.get("reason_relation") == "subsets":
            rs.extend(wrap("原因可重叠或未列全：" if zh else "Reasons (may overlap or be incomplete):", (w-32)/14))
        for r in n.get("reasons", []):
            value = str(r["n"]) if r.get("n") is not None else "?"
            rs.extend(wrap(value + " — " + r["label"] + (unconfirmed if r.get("confirmed") is not True else ""), (w-32)/14))
        reasons[n["id"]] = rs
    top = wrap(data["title"], (width-2*margin)/22)
    meta = wrap(" · ".join(filter(None, [draft_label if draft else "",
                teaching_label if data.get("synthetic") else "", data["design"]])), (width-2*margin)/14)
    position = 28 + 18*len(meta) + 12 + 28*len(top) + 23
    boxes = {}
    for row in rows:
        yy = position; heights = []
        for n in [v for v in nodes if v["row"] == row]:
            k = n["id"]; h = 27 + 21*len(labels[k]) + 19*len(counts[k]) + 18*len(reasons[k])
            boxes[k] = ((width-plot)//2 + cols.index(n["col"])*(w+gap), yy, w, h)
            heights.append(h)
        position += max(heights) + 46
    foot = []
    if any(g["relation"] == "subsets" for g in data["groups"]):
        foot.extend(wrap("虚线：子集可能重叠或未覆盖全部对象，各项计数不能相加。" if zh else
                         "Dashed connectors: subsets may overlap or be incomplete; do not add their counts.", (width-2*margin)/13))
    for g in data["groups"]:
        if g["relation"] == "unit_change":
            prefix, unknown = ("点线：", "计数单位的转换方式待确认。") if zh else ("Dotted connector: ", "unit mapping unconfirmed")
            foot.extend(wrap(prefix + (g["rationale"] if text(g.get("rationale")) else unknown), (width-2*margin)/13))
    for note in data.get("notes", []):
        foot.extend(wrap(note, (width-2*margin)/13))
    height = position + len(foot)*18 + 12
    root = ET.Element("svg", {"xmlns":"http://www.w3.org/2000/svg", "lang":"zh" if zh else "en", "width":str(width), "height":str(height),
                             "viewBox":f"0 0 {width} {height}", "role":"img", "aria-labelledby":"figure-title figure-desc"})
    def el(parent, tag, attrs=None, value=None):
        child = ET.SubElement(parent, tag, {k:str(v) for k,v in (attrs or {}).items()})
        child.text = value
        return child
    el(root, "title", {"id":"figure-title"}, data["title"])
    el(root, "desc", {"id":"figure-desc"}, ("原创研究对象流程图。" if zh else "Original participant disposition diagram. ") + " ".join(meta + foot))
    defs = el(root, "defs")
    marker = el(defs, "marker", {"id":"tip","viewBox":"0 0 8 8","refX":7.2,"refY":4,
                                 "markerWidth":7,"markerHeight":7,"orient":"auto"})
    el(marker,"path",{"d":"M0 0 L8 4 L0 8 Z","fill":"#4b5258"})
    el(root,"rect",{"width":width,"height":height,"fill":"white"})
    canvas = el(root,"g",{"font-family":"Arial, Helvetica, sans-serif","fill":"#202428"})
    def txt(x,y,v,size,weight="normal",color="#202428"):
        el(canvas,"text",{"x":x,"y":y,"font-size":size,"font-weight":weight,"fill":color},v)
    for i,s in enumerate(meta):
        txt(margin, 26+18*i, s, 14, "bold")
    for i,s in enumerate(top):
        txt(margin, 26+18*len(meta)+13+i*28, s, 22, "bold")
    for g in data["groups"]:
        x,y,bw,bh = boxes[g["parent"]]
        for k in g["children"]:
            xx,yy,cw,ch = boxes[k]
            if yy == y:
                sign = 1 if xx > x else -1
                a=(x+(bw if sign>0 else 0), y+bh//2); b=(xx+(0 if sign>0 else cw), yy+ch//2)
                aa=(a[0]+12*sign,a[1]); bb=(b[0]-12*sign,b[1])
            else:
                a=(x+bw//2,y+bh); b=(xx+cw//2,yy)
                aa=(a[0],a[1]+12); bb=(b[0],b[1]-12)
            points = [a, *ortho(aa,bb,boxes.values()), b]
            attrs = {"points":" ".join(f"{x0},{y0}" for x0,y0 in points), "fill":"none",
                     "stroke":"#4b5258","stroke-width":"1.5","stroke-linejoin":"round","marker-end":"url(#tip)"}
            if g["relation"] != "partition":
                attrs["stroke-dasharray"] = "6 3" if g["relation"] == "subsets" else "2 3"
            el(canvas,"polyline",attrs)
    for n in nodes:
        k = n["id"]; x,y,ww,hh = boxes[k]
        attrs = {"x":x,"y":y,"width":ww,"height":hh,"fill":"#f3f5f6" if n["kind"]=="analysis" else "#fff",
                 "stroke":"#394149","stroke-width":1.4}
        el(canvas,"rect",attrs)
        for i,s in enumerate(labels[k]):
            txt(x+15, y+24+21*i, s, 16)
        for i,s in enumerate(counts[k]):
            txt(x+15, y+26+21*len(labels[k])+19*i, s, 15, "bold")
        for i,s in enumerate(reasons[k]):
            txt(x+15, y+26+21*len(labels[k])+19*len(counts[k])+18*i, s, 14)
    for i,s in enumerate(foot):
        txt(margin, position+18*i, s, 13, color="#424950")
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
            diagram = svg(data,args.draft)
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
