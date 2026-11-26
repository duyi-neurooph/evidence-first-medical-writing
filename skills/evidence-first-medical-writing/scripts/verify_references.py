#!/usr/bin/env python3
"""Read public bibliography fields from JSON; print an identity audit, never edit sources.

Portions adapted from Aperivue/medsci-skills, skills/verify-refs/scripts/verify_refs.py
at e0ea3b0be3bf529aa0b94ee5fd8450e78848932c (MIT, Copyright (c) 2026 Aperivue).
Specifically: normalize_doi_for_dup, crossref_year, crossref_titles, collective-author
recognition and identifier duplicate grouping. The decision logic is replaced:
no fuzzy title pass, guessed identifiers, or automatic claim-support classification.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import html
from http.client import HTTPException
import json
import re
import sys
import time
import unicodedata
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


def doi_key(value):
    # Preserve legal DOI suffix punctuation in structured input (including parentheses).
    s = str(value or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/",
                   "http://dx.doi.org/", "doi:"):
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return s


def title_key(text):
    """Compare ordered lexical tokens; retain signs, decimals, ranges and ordinals."""
    s = html.unescape(str(text or ""))
    s = re.sub(r"</?(?:jats:)?(?:i|b|em|strong|sub|sup|italic|bold)(?:\s[^>]*)?>", "", s, flags=re.I)
    s = unicodedata.normalize("NFKC", s).casefold()
    # An em dash introducing a subtitle is typographic punctuation, not a
    # unary minus, a numeric range, or trailing serostatus notation.
    s = re.sub(r"(?<=[^\W\d_])\s*[—–]\s*(?=[^\W\d_])", " ", s)
    s = re.sub(r"[‐‑‒–—−]", "-", s)
    # A word-joining hyphen is ordinary punctuation; a trailing or unary minus isn't.
    s = re.sub(r"(?<=[^\W_])-(?=[^\W\d_])", " ", s)
    return tuple(re.findall(r"\d+(?:[.,]\d+)*|\.\d+|[^\W\d_]+|[+\-±%<>≤≥=/×:]",
                            re.sub(r"(?<!\d):|:(?!\d)", " ", s), re.UNICODE))


def name_key(s):
    s = unicodedata.normalize("NFKD", s.casefold())
    return " ".join(re.findall(r"[^\W_]+", "".join(c for c in s if not unicodedata.combining(c))))


ORG = re.compile(r"\b(?:group|committee|society|association|collaborat\w+|consortium|network|"
                 r"panel|initiative|organi[sz]ation|investigators|trialists|task force|"
                 r"foundation|institute|council|federation|college)\b", re.I)


def author_equal(a, b):
    if name_key(a) == name_key(b):
        return True
    if ORG.search(a) or ORG.search(b):
        return name_key(a).removeprefix("the ") == name_key(b).removeprefix("the ")
    # Structured registry names carry a reliable family/given boundary; permit
    # the reverse display order only from that boundary, never permute all tokens.
    for structured, printed in ((a, b), (b, a)):
        if "," in structured:
            family, given = structured.split(",", 1)
            if name_key(given + " " + family) == name_key(printed):
                return True

    def split(s):
        if "," in s:
            family, given = s.split(",", 1)
        else:
            parts = s.strip().split()
            # Unambiguous Vancouver family + initials; uncertain spellings need review.
            if len(parts) > 1 and re.fullmatch(r"[A-Z.\-]{1,7}", parts[-1]):
                family, given = " ".join(parts[:-1]), parts[-1]
            else:
                return (name_key(s), "", "")
        compact = re.sub(r"[.\s-]", "", given.strip())
        full = bool(compact) and not (compact.isupper() and len(compact) <= 6)
        initials = "".join(x[0] for x in name_key(given).split()) if full else compact.casefold()
        return name_key(family), initials, name_key(given) if full else ""

    af, ai, ag = split(a)
    bf, bi, bg = split(b)
    return bool(af and af == bf and (not ai or not bi or ai == bi)
                and (not ag or not bg or ag == bg))


def match_fields(entry, rec):
    conflicts, missing = {}, []
    def compare(field, given, actual, ok):
        if not given:
            return
        if not actual:
            missing.append(field)
        elif not ok:
            conflicts[field] = {"cited": given, "record": actual}
    titles = [t for t in [rec.get("title"), *rec.get("alt_titles", [])] if t]
    kt = title_key(entry.get("title"))
    compare("title", entry.get("title"), titles, kt and any(kt == title_key(t) for t in titles))
    journals = rec.get("journals", [])
    compare("journal", entry.get("journal"), journals,
            any(name_key(entry.get("journal", "")) == name_key(j) for j in journals))
    years = [str(y) for y in rec.get("years", [])]
    compare("year", entry.get("year"), years, str(entry.get("year")) in years)
    authors = list(entry.get("authors") or [])
    truncated = entry.get("authors_truncated") is True
    if authors and re.search(r"(?:^|[,;\s]+)et\s+al\.?$", authors[-1], re.I):
        truncated = True
        authors[-1] = re.sub(r"(?:^|[,;\s]+)et\s+al\.?$", "", authors[-1], flags=re.I).strip()
        if not authors[-1]:
            authors.pop()
    actual = rec.get("authors") or []
    if entry.get("authors") and not authors:
        missing.append("authors")
    compare("authors", authors, actual,
            len(authors) <= len(actual) and (truncated or len(authors) == len(actual))
            and all(author_equal(a, b) for a, b in zip(authors, actual)))
    for k, fn in (("doi", doi_key), ("pmid", str)):
        if entry.get(k) and rec.get(k) and fn(entry[k]) != fn(rec[k]):
            conflicts[k] = {"cited": entry[k], "record": rec[k]}
    return conflicts, missing


PUB = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CR = "https://api.crossref.org/works"
LIMIT = 5


class Backend:
    def __init__(self):
        self.last = {}

    def read(self, url):
        api = "NCBI" if url.startswith(PUB) else "Crossref"
        delay = (0.36 if api == "NCBI" else 0.1) - (time.monotonic() - self.last.get(api, 0))
        if delay > 0:
            time.sleep(delay)
        self.last[api] = time.monotonic()
        with urlopen(Request(url, headers={"User-Agent": "EvidenceFirstMedicalWriting/ReferenceAudit"}),
                     timeout=8) as response:
            result = response.read(2097153)
        if len(result) > 2097152:
            raise ValueError("registry response exceeds size limit")
        return result

    @lru_cache(maxsize=512)
    def fetch_doi(self, doi):
        url = CR + "/" + quote(doi, safe="")
        try:
            m = json.loads(self.read(url))["message"]
        except HTTPError as exc:
            if exc.code == 404:
                return None
            raise
        if doi_key(m.get("DOI")) != doi:
            raise ValueError("Crossref identifier mismatch")
        if m.get("type") != "journal-article":
            raise ValueError("Not a Crossref journal article; review the source type")
        main = m.get("title") or []
        sub = m.get("subtitle") or []
        titles = [f"{t}: {s}" for t in main for s in sub] if sub else main
        years = set()
        for field in ("published-print", "published-online", "issued"):
            parts = ((m.get(field) or {}).get("date-parts") or [[]])[0]
            if parts and parts[0]:
                years.add(str(parts[0]))
        authors = []
        for a in m.get("author", []):
            authors.append(a.get("name") or ", ".join(filter(None, (a.get("family"), a.get("given")))))
        return {"title": next(iter(titles), ""), "alt_titles": titles[1:] + (m.get("original-title") or []),
                "journals": (m.get("container-title") or []) + (m.get("short-container-title") or []),
                "years": sorted(years), "authors": authors, "doi": doi, "url": url}

    @lru_cache(maxsize=512)
    def fetch_pmid(self, pmid):
        url = PUB + "efetch.fcgi?" + urlencode({"db": "pubmed", "id": pmid, "retmode": "xml"})
        root = ET.fromstring(self.read(url))
        art = root.find("PubmedArticle")
        if art is None:
            return None
        if art.findtext("MedlineCitation/PMID") != pmid:
            raise ValueError("PubMed identifier mismatch")
        details = art.find("MedlineCitation/Article")
        def tx(path):
            el = details.find(path)
            return "".join(el.itertext()).strip() if el is not None else ""
        authors = [a.findtext("CollectiveName") or ", ".join(filter(None, (a.findtext("LastName"),
                   a.findtext("ForeName") or a.findtext("Initials")))) for a in details.findall("AuthorList/Author")]
        years = {y.text for y in details.findall("ArticleDate/Year") if y.text}
        year = tx("Journal/JournalIssue/PubDate/Year") or tx("Journal/JournalIssue/PubDate/MedlineDate")
        if re.match(r"\d{4}", year):
            years.add(year[:4])
        return {"title": tx("ArticleTitle"), "alt_titles": [tx("VernacularTitle")],
                "authors": authors, "journals": list(filter(None, [tx("Journal/Title"), tx("Journal/ISOAbbreviation"),
                        art.findtext("MedlineCitation/MedlineJournalInfo/MedlineTA")])), "years": sorted(years),
                "pmid": pmid, "doi": doi_key(art.findtext('PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"}

    def _pubsearch(self, term):
        r = json.loads(self.read(PUB + "esearch.fcgi?" + urlencode(
            {"db": "pubmed", "term": term, "retmode": "json", "retmax": LIMIT})))["esearchresult"]
        return r["idlist"], int(r["count"]) > LIMIT

    def search_pubmed(self, title):
        # Full-title queries containing typographical punctuation or subtitles may
        # return zero even for indexed papers. A bounded set of separate title
        # terms sidesteps PubMed's incomplete phrase index for discovery only.
        words = re.findall(r"[^\W_]+", html.unescape(title), re.UNICODE)
        phrase = " ".join(words)
        found = self._pubsearch('"' + phrase + '"[Title]')
        if not found[0]:
            stop = {"a", "an", "the", "of", "to", "in", "after", "with", "from", "and", "or", "for"}
            terms = list(dict.fromkeys(w.casefold() for w in words if w.casefold() not in stop))[:9]
            if len(terms) >= 2:
                return self._pubsearch(" AND ".join(w + "[Title]" for w in terms))
        return found

    def pubmed_for_doi(self, doi):
        return self._pubsearch('"' + doi.replace('"', ' ') + '"[AID]')

    def search_crossref(self, title):
        # Crossref query.title is a ranked candidate generator, not an exact-count index.
        m = json.loads(self.read(CR + "?" + urlencode({"query.title": title, "rows": LIMIT + 1,
                              "filter": "type:journal-article", "select": "DOI,title,subtitle"})))["message"]
        return [r["DOI"] for r in m["items"][:LIMIT]], len(m["items"]) > LIMIT


ROUTES = {"journal": "PubMed / Crossref", "guideline": "issuing society or original journal",
          "consensus": "issuing society or original journal", "registry": "official trial registry",
          "who": "WHO publication or official repository", "label": "issuing regulator / approved label",
          "journal_instructions": "target journal author instructions", "other": "issuing institution"}


def same_work(a, b):
    for key in ("pmid", "doi"):
        if a.get(key) and b.get(key) and str(a[key]).casefold() != str(b[key]).casefold():
            return False
    return any(a.get(k) and b.get(k) and str(a[k]).casefold() == str(b[k]).casefold()
               for k in ("doi", "pmid"))


def outstanding_conflicts(g, r):
    """One linked index can omit the subtitle, alias or one publication date."""
    relevant = dict(r["conflicts"])
    if "title" in relevant and r["source"] == "Crossref":
        short = r.get("title", "").rstrip(". ")
        if short and any(re.match(re.escape(short) + r"\s*[:.\u2014]\s*\S", t, re.I)
                         for t in [g["title"], *g.get("alt_titles", [])]):
            del relevant["title"]
    if "year" in relevant and set(map(str, r.get("years", []))) & set(map(str, g.get("years", []))):
        del relevant["year"]
    if "journal" in relevant and ({name_key(j) for j in r["journals"]} & {name_key(j) for j in g["journals"]}):
        del relevant["journal"]
    return relevant


def explain_verified(g, rows, out):
    out["verified_by"] = g["url"]
    explains = {"title": "A linked record gives the complete title, including subtitle.",
                "year": "Linked records share a publication year; cited online/issue year appears in the complete record.",
                "journal": "Linked records share an official journal name; the cited alias appears in the complete record."}
    for r in rows:
        if not same_work(g, r):
            continue
        cleared = set(r["conflicts"]) - set(outstanding_conflicts(g, r))
        if cleared:
            r["reconciled"] = {k: {"reason": explains[k], "confirmed_by": g["url"]} for k in sorted(cleared)}


def verify_one(e, backend, offline):
    kind = e.get("type", "journal")
    out = {"id": e["id"], "identity": "pending", "route": ROUTES.get(kind, ROUTES["other"]),
           "candidates": [], "source_urls": [], "reasons": [], "duplicate_ids": []}
    notes = out["reasons"]
    if kind != "journal":
        notes.append("Inspect original issuer document: confirm title, issuing body, version/date and locator.")
        return out
    if offline:
        notes.append("Offline: no authoritative record retrieved.")
        return out
    title, doi, pmid = e.get("title", ""), doi_key(e.get("doi")), str(e.get("pmid") or "").strip()
    if not title_key(title) or not any(c.isalnum() for c in title):
        notes.append("Missing identifiable title; an identifier alone is not a match.")
        return out
    if doi and not re.fullmatch(r"10\.\d{4,9}/[^\s]+", doi) or pmid and not re.fullmatch(r"[1-9]\d*", pmid):
        notes.append("Malformed DOI or PMID.")
        return out
    refs, checked = [], {}
    errors = (OSError, HTTPException, ValueError, TypeError, AttributeError, KeyError, IndexError, ET.ParseError)
    def get(source, ident):
        key = (source, ident)
        if key in checked:
            return checked[key]
        try:
            r = (backend.fetch_pmid if source == "PubMed" else backend.fetch_doi)(ident)
            if not r:
                notes.append(f"{source}: no formal record for {ident}.")
            else:
                if str(r.get("pmid" if source == "PubMed" else "doi", "")).casefold() != ident.casefold():
                    raise ValueError("retrieved record does not match requested identifier")
                r = dict(r)
                r["source"] = source
                r["conflicts"], r["missing"] = match_fields(e, r)
                refs.append(r)
                out["source_urls"].append(r["url"])
            checked[key] = r
        except errors as ex:
            notes.append(f"{source}: could not verify {ident} ({type(ex).__name__}: {ex}).")
            checked[key] = None
        return checked[key]

    if doi or pmid:
        p = get("PubMed", pmid) if pmid else None
        c = get("Crossref", doi) if doi else None
        if doi and not pmid and (not c or c["conflicts"] or c["missing"]) and hasattr(backend, "pubmed_for_doi"):
            try:
                ids, more = backend.pubmed_for_doi(doi)
                for i in ids:
                    get("PubMed", i)
                if more:
                    notes.append("DOI lookup has unresolved additional records.")
                    out["candidates"] = refs
                    return out
            except errors as ex:
                notes.append(f"PubMed DOI lookup unavailable ({type(ex).__name__}).")
        if pmid and not doi and p and (p["missing"] or p["conflicts"]) and p.get("doi"):
            get("Crossref", p["doi"])
        # A single complete authority can corroborate both IDs explicitly. A pair of
        # successful but unlinked resolutions is not sufficient proof of co-identity.
        linked = [r for r in refs if (not doi or doi_key(r.get("doi")) == doi)
                  and (not pmid or str(r.get("pmid", "")) == pmid)]
        good = [r for r in refs if not r["conflicts"] and not r["missing"]
                and any(same_work(r, l) for l in linked)]
        for r in refs:
            if not good:
                break
            # A shared identifier is not sufficient to waive a contradictory year,
            # author, journal, or full title. A shortened title or missing online year
            # is missing detail only when another linked authority supplies it.
            g = good[0]
            if not same_work(g, r):
                good = []
                break
            if outstanding_conflicts(g, r):
                good = []
        if good:
            out["identity"] = "verified"
            explain_verified(good[0], refs, out)
        else:
            notes.append("Identifiers not cross-linked or no unique record confirms all supplied fields without conflict.")
    else:
        coverage = {}
        for source, search in [("PubMed", backend.search_pubmed), ("Crossref", backend.search_crossref)]:
            try:
                ids, more = search(title)
                complete = not more
                for i in ids:
                    if not get(source, i):
                        complete = False
                coverage[source] = complete
                if not complete:
                    notes.append(f"{source}: candidate set incomplete; no uniqueness claim from this search.")
            except errors as ex:
                coverage[source] = False
                notes.append(f"{source}: search unavailable ({type(ex).__name__}: {ex}).")
        good = [r for r in refs if not r["missing"] and not r["conflicts"]]
        if good:
            g = good[0]
            # Missing metadata cannot eliminate a rival; a different exact-title record
            # is excluded only when it positively contradicts another supplied field.
            ambiguous = any(not same_work(g, r) and not r["conflicts"] for r in refs)
            conflict = any(same_work(g, r) and outstanding_conflicts(g, r) for r in refs)
            if not ambiguous and not conflict and any(coverage.get(r["source"]) for r in good):
                out["identity"] = "verified"
                explain_verified(next(r for r in good if coverage.get(r["source"])), refs, out)
            else:
                notes.append("Unresolved competing records, metadata conflict, or incomplete candidate retrieval.")
        else:
            notes.append("No unique formal title with matching available metadata.")
    out["candidates"] = refs
    return out


def verify_batch(entries, backend=None, offline=False):
    if not isinstance(entries, list):
        raise ValueError("Input must be a JSON array of bibliography entries.")
    backend = backend or Backend()
    rows, indexes = [], defaultdict(list)
    for idx, raw in enumerate(entries, 1):
        e = {"id": idx}
        if isinstance(raw, dict):
            e.update(raw)
        if not all(isinstance(e.get(k, ""), str) for k in ("title", "journal", "type")) or not (
            isinstance(e.get("authors", []), list) and all(isinstance(a, str) for a in e.get("authors", []))
        ):
            row = {"id": e["id"], "identity": "pending", "reasons": ["Invalid bibliography field format."],
                   "candidates": [], "duplicate_ids": [], "source_urls": [], "route": "author verification"}
        else:
            row = verify_one(e, backend, offline)
        rows.append(row)
        for field, ident in [("doi", doi_key(e.get("doi"))), ("pmid", str(e.get("pmid") or "").strip())]:
            if ident:
                indexes[(field, ident)].append(len(rows)-1)
    duplicates = []
    for (field, value), indices in indexes.items():
        if len(indices) > 1:
            duplicates.append({"field": field, "value": value, "entries": [rows[i]["id"] for i in indices]})
            for i in indices:
                rows[i]["duplicate_ids"].append(f"{field}:{value}")
    return {"checked_at": datetime.now(timezone.utc).isoformat(), "offline": bool(offline),
            "results": rows, "duplicates": duplicates, "claim_support": "not assessed by bibliographic lookup"}


def citation_order(inventory):
    """Audit one journal-defined numbering series, in reading order, without lookups."""
    if not isinstance(inventory, dict):
        raise ValueError("Expected a callout inventory object")
    style = inventory.get("style")
    if style in ("author-date", "alphabetical"):
        return {"status": "not_applicable", "reason": style}
    if style != "first-appearance":
        return {"status": "cannot_verify", "reason": "numbering convention not established"}
    if inventory.get("complete") is not True:
        return {"status": "cannot_verify", "reason": "full ordered manuscript callouts unavailable"}
    rows = inventory.get("callouts")
    if not isinstance(rows, list) or not rows:
        return {"status": "cannot_verify", "reason": "no ordered citation callouts supplied"}
    # All values below 'expected' have already appeared; seeing one again is a back-citation.
    expected = 1
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("location"), str) or not row["location"].strip():
            raise ValueError("Each callout needs an exact manuscript location")
        loc, expression = row["location"], row.get("labels")
        if not isinstance(expression, str):
            return {"status": "cannot_verify", "location": loc, "reason": "unreadable callout"}
        for token in expression.split(","):
            match = re.fullmatch(r"\s*([1-9][0-9]{0,5})(?:\s*[-–]\s*([1-9][0-9]{0,5}))?\s*", token)
            if not match:
                return {"status": "cannot_verify", "location": loc, "reason": "unreadable callout"}
            lo = int(match[1])
            hi = int(match[2] or lo)
            if hi < lo:
                return {"status": "cannot_verify", "location": loc, "reason": "descending citation range"}
            if lo > expected:
                return {"status": "out_of_order", "location": loc, "expected": expected, "actual": lo}
            expected = max(expected, hi + 1)
    return {"status": "pass", "distinct_first_mentions": expected - 1}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--offline", action="store_true", help="never query external databases")
    ap.add_argument("--citation-order", action="store_true", help="check an ordered callout inventory offline instead of looking up references")
    ap.add_argument("input", help="JSON bibliography or callout inventory; use - for stdin")
    args = ap.parse_args()
    try:
        if args.input == "-":
            entries = json.load(sys.stdin)
        else:
            with open(args.input, encoding="utf-8-sig") as stream:
                entries = json.load(stream)
        report = citation_order(entries) if args.citation_order else verify_batch(entries, offline=args.offline)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (ValueError, OSError) as ex:
        ap.exit(2, f"Input error: {ex}\n")


if __name__ == "__main__":
    main()
