"""Offline acceptance tests. Candidate hits are IDs only; records are fetched separately.

The 5/15-year ONTT titles and 15-year record are bibliographic facts from
https://pubmed.ncbi.nlm.nih.gov/9400788/ and https://pubmed.ncbi.nlm.nih.gov/17976727/.
Other test records are synthetic, not citations for use in a manuscript.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "evidence-first-medical-writing" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import verify_references as verifier


TITLE5 = ("Visual function 5 years after optic neuritis: experience of the Optic "
          "Neuritis Treatment Trial. The Optic Neuritis Study Group")
TITLE15 = ("Visual function 15 years after optic neuritis: a final follow-up "
           "report from the Optic Neuritis Treatment Trial")
PMID15 = "17976727"
DOI15 = "10.1016/j.ophtha.2007.08.004"
GROUP = "Optic Neuritis Study Group"


def official(**updates):
    return dict(dict(title=TITLE15, pmid=PMID15, doi=DOI15, authors=[GROUP],
                     journals=["Ophthalmology"], years=[2007, 2008],
                     url="https://pubmed.ncbi.nlm.nih.gov/17976727/"), **updates)


def cited(**updates):
    return dict(dict(id="R1", title=TITLE15, authors=[GROUP], journal="Ophthalmology", year=2008), **updates)


class Indexes:
    """Fake transport, not fake decision logic. None = not found, OSError = unreachable."""
    def __init__(self, pmids=None, dois=None, pm_hits=(), cr_hits=(), broken=(), overflow=False):
        self.pmids = pmids or {}
        self.dois = dois or {}
        self.pm_hits, self.cr_hits = list(pm_hits), list(cr_hits)
        self.broken = set(broken)
        self.overflow = overflow
        self.calls = []

    def _call(self, name, query):
        self.calls.append((name, query))
        if name in self.broken:
            raise OSError("test transport: source unavailable")

    def fetch_doi(self, doi):
        self._call("doi", doi)
        return copy.deepcopy(self.dois.get(doi))

    def fetch_pmid(self, pmid):
        self._call("pmid", pmid)
        return copy.deepcopy(self.pmids.get(pmid))

    def search_crossref(self, title):
        self._call("cr_search", title)
        return self.cr_hits, self.overflow

    def search_pubmed(self, title):
        self._call("pm_search", title)
        return self.pm_hits, self.overflow


class IdentityAcceptance(unittest.TestCase):
    def one(self, entry, db, offline=False):
        original = copy.deepcopy(entry)
        result = verifier.verify_batch([entry], backend=db, offline=offline)["results"][0]
        self.assertEqual(entry, original, "audit must not rewrite source fields")
        return result

    def test_punctuation_case_space_match_after_record_fetch(self):
        db = Indexes(pmids={PMID15: official()}, pm_hits=[PMID15])
        r = self.one(cited(title=TITLE15.upper().replace(": ", " —    ") + "."), db)
        self.assertEqual(r["identity"], "verified", r)
        self.assertIn(("pmid", PMID15), db.calls)
        self.assertTrue(r["source_urls"])

    def test_display_case_does_not_replace_record_or_hide_a_different_follow_up(self):
        # Synthetic publisher-style metadata and manuscript-style rendering.
        published = "Five-Year Outcomes in Chinese Adults With HIV"
        display = "Five-year outcomes in Chinese adults with HIV"
        record = official(title=published)
        for identifiers in ({}, {"pmid": PMID15, "doi": DOI15}):
            with self.subTest(identifiers=identifiers):
                db = Indexes(pmids={PMID15: record}, dois={DOI15: record},
                             pm_hits=[PMID15], cr_hits=[DOI15])
                entry = cited(title=display, **identifiers)
                match = self.one(entry, db)
                self.assertEqual(match["identity"], "verified", match)
                self.assertEqual({c["title"] for c in match["candidates"]}, {published})
                self.assertEqual(entry["title"], display)
                different = self.one(dict(entry, title=display.replace("Five", "Ten")), db)
                self.assertEqual(different["identity"], "pending", different)
                self.assertTrue(all("title" in c["conflicts"] for c in different["candidates"]))

    def test_5_year_citation_rejects_15_year_top_hit(self):
        db = Indexes(pmids={PMID15: official()}, pm_hits=[PMID15])
        r = self.one(cited(title=TITLE5, year=1997, journal="Arch Ophthalmol"), db)
        self.assertEqual(r["identity"], "pending", r)
        self.assertIn(("pmid", PMID15), db.calls)
        self.assertEqual(r["candidates"][0]["title"], TITLE15)
        self.assertIn("title", r["candidates"][0]["conflicts"])

    def test_resolvable_but_wrong_doi_has_title_conflict(self):
        db = Indexes(dois={DOI15: official()})
        r = self.one(cited(doi=DOI15, title=TITLE5, year=1997), db)
        self.assertEqual(r["identity"], "pending", r)
        self.assertIn(("doi", DOI15), db.calls)
        self.assertIn("title", r["candidates"][0]["conflicts"])

    def test_medical_differences_survive_normalization(self):
        for submitted, retrieved in [
                ("Outcomes in AQP4+ cases", "Outcomes in AQP4- cases"),
                ("Outcomes in AQP4-positive cases", "Outcomes in AQP4-negative cases"),
                ("Outcomes with 1.5 mg dosing", "Outcomes with 15 mg dosing"),
                ("Outcomes with .5 mg dosing", "Outcomes with 5 mg dosing"),
                ("Effect at −5 degrees", "Effect at 5 degrees"),
                ("Exposure and stroke: trial protocol", "Exposure and stroke: trial results"),
                ("Visual function at 5 years", "Visual function at 15 years")]:
            with self.subTest(submitted=submitted):
                db = Indexes(pmids={PMID15: official(title=retrieved)}, pm_hits=[PMID15])
                r = self.one(cited(title=submitted), db)
                self.assertEqual(r["identity"], "pending", r)
                self.assertIn("title", r["candidates"][0]["conflicts"])

    def test_indistinguishable_exact_titles_are_not_unique(self):
        second = official(pmid="12345678", doi="10.1234/synthetic.2",
                          url="https://pubmed.ncbi.nlm.nih.gov/12345678/")
        db = Indexes(pmids={PMID15: official(), second["pmid"]: second},
                     pm_hits=[second["pmid"], PMID15])
        r = self.one(cited(), db)
        self.assertEqual(r["identity"], "pending", r)
        self.assertEqual({c["pmid"] for c in r["candidates"]}, {second["pmid"], PMID15})
        self.assertTrue(r["reasons"])

    def test_author_journal_year_conflicts_are_not_discarded(self):
        for field, value in [("authors", ["Invented Consortium"]),
                             ("journal", "An entirely different journal"), ("year", 2006)]:
            with self.subTest(field=field):
                db = Indexes(pmids={PMID15: official()}, pm_hits=[PMID15])
                r = self.one(cited(**{field: value}), db)
                self.assertEqual(r["identity"], "pending", r)
                self.assertTrue(r["candidates"][0]["conflicts"])

    def test_disagreeing_formal_titles_on_linked_records_are_not_ignored(self):
        conflict = official(title=TITLE15.replace("15 years", "5 years"),
                            url="https://api.crossref.org/works/" + DOI15)
        db = Indexes(pmids={PMID15: official()}, dois={DOI15: conflict},
                     pm_hits=[PMID15], cr_hits=[DOI15])
        r = self.one(cited(), db)
        self.assertEqual(r["identity"], "pending", r)
        self.assertTrue(any("title" in c["conflicts"] for c in r["candidates"]))

    def test_unfetched_single_candidate_is_not_identity(self):
        # Search metadata/ID are not the formal record, even if there is just one hit.
        db = Indexes(pm_hits=[PMID15], broken=["pmid"])
        r = self.one(cited(), db)
        self.assertEqual(r["identity"], "pending", r)
        self.assertIn(("pmid", PMID15), db.calls)
        self.assertTrue(r["reasons"])

    def test_real_backend_ignores_crossref_search_preview_fetches_actual_doi(self):
        # Exercise production request + JSON parsing with no HTTP. The search preview
        # deceptively matches; the retrieved formal record belongs to the other report.
        requests = []
        def read(url):
            requests.append(url)
            if "/esearch.fcgi?" in url:
                return b'{"esearchresult":{"count":"0","idlist":[]}}'
            if "/works?" in url:
                obj = {"items": [{"DOI": DOI15, "title": [TITLE5]}]}
            elif "/works/" in url:
                obj = {"type": "journal-article", "DOI": DOI15, "title": [TITLE15],
                       "author": [{"name": GROUP}], "container-title": ["Ophthalmology"],
                       "published-print": {"date-parts": [[2008]]}}
            else:
                self.fail("Unexpected endpoint: " + url)
            return json.dumps({"message": obj}).encode()
        backend = verifier.Backend()
        with patch.object(backend, "read", side_effect=read):
            row = self.one(cited(title=TITLE5), backend)
        self.assertEqual(row["identity"], "pending", row)
        self.assertEqual(row["candidates"][0]["title"], TITLE15)
        self.assertIn("title", row["candidates"][0]["conflicts"])
        self.assertTrue(any("/works/" in url for url in requests))

    def test_real_pubmed_xml_parser_uses_collective_author_and_online_date(self):
        xml = f"""<PubmedArticleSet><PubmedArticle><MedlineCitation>
          <PMID>{PMID15}</PMID><Article><Journal><JournalIssue><PubDate><Year>2008</Year>
          </PubDate></JournalIssue><Title>Ophthalmology</Title></Journal><ArticleTitle>{TITLE15}</ArticleTitle>
          <AuthorList><Author><CollectiveName>{GROUP}</CollectiveName></Author></AuthorList>
          <ArticleDate DateType="Electronic"><Year>2007</Year></ArticleDate></Article></MedlineCitation>
          <PubmedData><ArticleIdList><ArticleId IdType="doi">{DOI15}</ArticleId>
          </ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>"""
        def read(url):
            self.assertIn("/efetch.fcgi?", url)
            self.assertEqual(parse_qs(urlsplit(url).query)["id"], [PMID15])
            return xml.encode()
        backend = verifier.Backend()
        with patch.object(backend, "read", side_effect=read):
            row = self.one(cited(pmid=PMID15, year=2007), backend)
        self.assertEqual(row["identity"], "verified", row)

    def test_single_authority_suffices_without_other_index(self):
        db = Indexes(pmids={PMID15: official()}, pm_hits=[PMID15], broken=["cr_search"])
        r = self.one(cited(), db)
        self.assertEqual(r["identity"], "verified", r)

    def test_dual_identifiers_pointing_to_different_articles(self):
        wrong = official(pmid="9400788", doi="10.1001/synthetic.5", title=TITLE5,
                         years=[1997], url="https://pubmed.ncbi.nlm.nih.gov/9400788/")
        db = Indexes(pmids={"9400788": wrong}, dois={DOI15: official()})
        r = self.one(cited(doi=DOI15, pmid="9400788"), db)
        self.assertEqual(r["identity"], "pending", r)
        self.assertIn(("pmid", "9400788"), db.calls)
        self.assertIn(("doi", DOI15), db.calls)
        self.assertTrue(r["reasons"] or any(c["conflicts"] for c in r["candidates"]))

    def test_dual_identifiers_consistent_and_group_author_online_year(self):
        db = Indexes(pmids={PMID15: official()}, dois={DOI15: official()})
        r = self.one(cited(doi=DOI15, pmid=PMID15, year=2007), db)
        self.assertEqual(r["identity"], "verified", r)

    def test_truncated_prefix_and_verified_journal_alias(self):
        data = official(authors=["Lee AB", "Wong CD", "Davis EF"],
                        journals=["Fictional Journal of Testing", "Fict J Test"])
        db = Indexes(pmids={PMID15: data})
        r = self.one(cited(pmid=PMID15, authors=["Lee AB", "Wong CD", "et al."],
                           journal="Fict J Test"), db)
        self.assertEqual(r["identity"], "verified", r)
        wrong = self.one(cited(pmid=PMID15, authors=["Lee AB", "Davis EF", "et al."],
                               journal="Fict J Test"), db)
        self.assertEqual(wrong["identity"], "pending", wrong)

    def test_same_ids_flagged_for_all_input_rows(self):
        db = Indexes(pmids={PMID15: official()}, dois={DOI15: official()})
        entries = [cited(id="R1", doi=DOI15, pmid=PMID15),
                   cited(id="R2", doi=DOI15.upper(), pmid=PMID15)]
        rows = verifier.verify_batch(entries, backend=db)["results"]
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertTrue(row["duplicate_ids"], row)

    def test_network_outage_preserves_row_and_reason(self):
        db = Indexes(broken=["pm_search", "cr_search", "pmid", "doi"])
        for entry in [cited(), cited(pmid=PMID15)]:
            r = self.one(entry, db)
            self.assertEqual(r["identity"], "pending", r)
            self.assertTrue(r["reasons"])
        self.assertTrue(db.calls)

    def test_offline_switch_makes_no_calls(self):
        db = Indexes()
        r = self.one(cited(pmid=PMID15), db, offline=True)
        self.assertEqual(r["identity"], "pending")
        self.assertTrue(r["reasons"])
        self.assertEqual(db.calls, [])

    def test_real_cli_offline_stdio(self):
        p = subprocess.run([sys.executable, "-B", str(SCRIPTS / "verify_references.py"), "--offline", "-"],
                           input=json.dumps([cited(pmid=PMID15)]), text=True,
                           capture_output=True, timeout=10)
        self.assertEqual(p.returncode, 0, p.stderr)
        row = json.loads(p.stdout)["results"][0]
        self.assertEqual((row["id"], row["identity"]), ("R1", "pending"))
        self.assertTrue(row["reasons"])


if __name__ == "__main__":
    unittest.main()
