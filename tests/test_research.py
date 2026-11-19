import json
import tempfile
import unittest
from pathlib import Path

from studio.config import load_config
from studio.errors import ConfigError
from studio.research import (DEFAULT_RESEARCH_CONFIG, load_research_config, select_topics, similarity, slugify,
                             validate_research, weighted_score)
from tests.research_fixtures import TODAY, candidate, research, source

CFG = load_config()
RCFG = load_research_config()


def validate(data):  # type: ignore[no-untyped-def]
    return validate_research(data, RCFG, CFG.languages, TODAY)


class ResearchConfigTests(unittest.TestCase):
    def test_weights_match_content_strategy(self) -> None:
        self.assertEqual(RCFG.weights, {"freshness": 0.2, "relevance": 0.2, "usefulness": 0.2,
                                        "evidence": 0.2, "visual": 0.1, "distinctiveness": 0.1})
        self.assertEqual((RCFG.min_candidates, RCFG.max_candidates, RCFG.max_selected), (8, 12, 2))

    def test_bad_weights_rejected(self) -> None:
        d = json.loads(DEFAULT_RESEARCH_CONFIG.read_text(encoding="utf-8"))
        d["weights"]["visual"] = 0.5
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "r.json"
            p.write_text(json.dumps(d), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "sum"):
                load_research_config(p)


class ValidationTests(unittest.TestCase):
    def test_valid_research_has_no_errors(self) -> None:
        self.assertEqual(validate(research()), ([], []))

    def test_count_limits(self) -> None:
        errors, warnings = validate(research([candidate(1)]))
        self.assertEqual(errors, [])
        self.assertTrue(warnings)
        errors, _ = validate(research([candidate(i) | {"id": f"X{i}"} for i in range(1, 14)]))
        self.assertTrue(any("maximum" in e for e in errors))

    def test_source_fields_required(self) -> None:
        bad = candidate(1, sources=[source(url="example.com", publisher="", claim="", kind="blog", accessed="yesterday")])
        joined = " ".join(validate(research([bad]))[0])
        for needle in ("url", "publisher", "claim", "kind", "accessed"):
            self.assertIn(needle, joined)

    def test_no_sources_is_error(self) -> None:
        self.assertTrue(any("source" in e for e in validate(research([candidate(1, sources=[])]))[0]))

    def test_future_and_inconsistent_dates(self) -> None:
        errs = validate(research([candidate(1, sources=[source(published="2026-12-01")])]))[0]
        self.assertTrue(any("future" in e for e in errs))
        errs = validate(research([candidate(1, sources=[source(published="2026-11-19", accessed="2026-11-18")])]))[0]
        self.assertTrue(any("after accessed" in e for e in errs))

    def test_null_published_allowed(self) -> None:
        self.assertEqual(validate(research([candidate(1, evergreen=True, sources=[source(published=None)])]))[0], [])

    def test_language_bucket_scores_and_ids(self) -> None:
        bad = [candidate(1, language="Hindi", bucket="crypto"), candidate(1)]
        bad[1]["scores"]["visual"] = 7
        joined = " ".join(validate(research(bad))[0])
        for needle in ("language", "bucket", "scores.visual", "duplicate candidate ids"):
            self.assertIn(needle, joined)

    def test_cautions_do_not_reject_but_must_be_strings(self) -> None:
        ok = candidate(1, cautions=["attribute cost claim to vendor"])
        self.assertEqual(validate(research([ok]))[0], [])
        self.assertTrue(select_topics(research([ok]), RCFG, TODAY)[0].selected)
        self.assertTrue(validate(research([candidate(1, cautions="x")]))[0])

    def test_research_date_must_match(self) -> None:
        data = research() | {"research_date": "2026-11-19"}
        self.assertTrue(any("research_date" in e for e in validate(data)[0]))


class SelectionTests(unittest.TestCase):
    def test_weighted_score(self) -> None:
        scores = {"freshness": 5, "relevance": 5, "usefulness": 5, "evidence": 5, "visual": 0, "distinctiveness": 0}
        self.assertEqual(weighted_score(scores, RCFG), 4.0)

    def test_selects_top_two_deterministically(self) -> None:
        picks = [d.id for d in select_topics(research(), RCFG, TODAY) if d.selected]
        self.assertEqual(picks, ["C01", "C02"])
        again = [d.id for d in select_topics(research(), RCFG, TODAY) if d.selected]
        self.assertEqual(picks, again)

    def test_ties_break_on_id(self) -> None:
        data = research([candidate(i, score=4) for i in (3, 1, 2)])
        self.assertEqual([d.id for d in select_topics(data, RCFG, TODAY) if d.selected], ["C01", "C02"])

    def test_evidence_rejections(self) -> None:
        cands = [
            candidate(1, sources=[source(kind="secondary")]),
            candidate(2, evidence="low"),
            candidate(3, sources=[source(published="2026-10-01")]),
            candidate(4, sources=[source(published=None)]),
            candidate(5, reject_flags=["footage rights unclear"]),
            candidate(6, score=2),
        ]
        cands[5]["scores"]["evidence"] = 5
        decisions = {d.id: d for d in select_topics(research(cands), RCFG, TODAY)}
        self.assertFalse(any(d.selected for d in decisions.values()))
        self.assertIn("no primary source", decisions["C01"].reasons[0])
        self.assertIn("low evidence", decisions["C02"].reasons[0])
        self.assertIn("window", decisions["C03"].reasons[0])
        self.assertIn("no dated primary", decisions["C04"].reasons[0])
        self.assertIn("footage rights", decisions["C05"].reasons[0])
        self.assertIn("below", decisions["C06"].reasons[0])

    def test_old_evergreen_topic_allowed(self) -> None:
        data = research([candidate(1, evergreen=True, sources=[source(published="2024-01-01")])])
        self.assertTrue(select_topics(data, RCFG, TODAY)[0].selected)

    def test_returns_fewer_than_two_when_weak(self) -> None:
        data = research([candidate(1, score=4), candidate(2, score=1)])
        self.assertEqual(sum(d.selected for d in select_topics(data, RCFG, TODAY)), 1)

    def test_near_duplicates_skipped(self) -> None:
        a = candidate(1, score=5, title="Prompt caching cuts repeated context cost")
        b = candidate(2, score=4.5, title="Prompt caching cuts context cost")
        c = candidate(3, score=4)
        picks = [d.id for d in select_topics(research([a, b, c]), RCFG, TODAY) if d.selected]
        self.assertEqual(picks, ["C01", "C03"])

    def test_prior_topics_block_repeats(self) -> None:
        data = research([candidate(1, title="Prompt caching cuts repeated context cost")])
        d = select_topics(data, RCFG, TODAY, prior_titles=["prompt caching cuts repeated context cost"])[0]
        self.assertFalse(d.selected)
        self.assertIn("near-duplicate", d.reasons[0])


class TextHelperTests(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(slugify("MCP 2.0: What's New?"), "mcp-2-0-what-s-new")
        self.assertLessEqual(len(slugify("word " * 40)), 60)
        self.assertEqual(slugify("!!!"), "topic")

    def test_similarity(self) -> None:
        self.assertEqual(similarity("The MCP spec", "mcp spec"), 1.0)
        self.assertEqual(similarity("", "x"), 0.0)


if __name__ == "__main__":
    unittest.main()
