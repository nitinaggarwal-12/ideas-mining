"""Unit & Live HTTP Integration Tests for the Daily Latest-Topic LinkedIn Post & Visual Generator."""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
import urllib.request
import xml.etree.ElementTree as ET
from http.server import ThreadingHTTPServer
from pathlib import Path

from server import StudioRequestHandler
from src.harvester.daily_post_generator import CREATOR_STYLE_ARCHETYPES, DailyLinkedInPostEngine
from src.harvester.idea_miner import summarize_clean_boundary
from src.visuals.template_gallery import audit_zero_origin_svg


class TestDailyPostGenerator(unittest.TestCase):
    def test_summarize_clean_boundary_never_cuts_mid_word(self) -> None:
        raw = (
            "Grammar-aligned speculative decoding compiles JSON Schema finite-state machines directly "
            "into draft token masks so malformed output tokens are impossible at runtime. "
            "Second sentence verifies downstream foreign-key constraints across production databases."
        )
        short = summarize_clean_boundary(raw, max_chars=125)
        self.assertLessEqual(len(short), 125)
        self.assertFalse(short.endswith("..."))
        # Every word in `short` (stripped of punctuation) must appear intact in `raw`
        raw_words = {w.strip(".,;:()") for w in raw.split()}
        for word in short.rstrip(".").split():
            self.assertIn(word.strip(".,;:()"), raw_words, f"Mid-word cut detected: {word}")

    def test_all_6_creator_styles_and_custom_zero_origin_svgs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            engine = DailyLinkedInPostEngine(
                store_path=tmp_root / "daily_generated_posts.json",
                visuals_root=tmp_root / "daily-posts",
            )
            edition = engine.generate_daily_edition(
                edition_date="2026-10-29",
                count=6,
                creator_style="AUTO",
                use_live_network=False,
            )
            self.assertEqual(edition["post_count"], 6)
            seen_styles = {p["style_code"] for p in edition["posts"]}
            seen_templates = {p["canonical_template_id"] for p in edition["posts"]}
            self.assertEqual(seen_styles, set(CREATOR_STYLE_ARCHETYPES.keys()))
            self.assertEqual(seen_templates, {"T79", "T80", "T81", "T82", "T83", "T84"})

            for post in edition["posts"]:
                scores = post["scores"]
                self.assertGreaterEqual(scores["composite_score"], 50.0)
                self.assertLessEqual(scores["composite_score"], 100.0)
                self.assertNotIn("...", post["linkedin_post_text"])
                self.assertNotIn("claude", post["linkedin_post_text"].lower())
                self.assertNotIn("anthropic", post["linkedin_post_text"].lower())
                self.assertIn("Comment #1", post["first_comment_source"])
                self.assertTrue(post["google_slides_url"].startswith("https://docs.google.com/presentation/d/"))

                svg_name = Path(post["custom_dynamic_svg_url"]).name
                svg_file = tmp_root / "daily-posts" / "2026-10-29" / svg_name
                self.assertTrue(svg_file.exists())
                svg_xml = svg_file.read_text(encoding="utf-8")
                ET.fromstring(svg_xml)
                self.assertNotIn("...", svg_xml)
                audit = audit_zero_origin_svg(svg_xml)
                self.assertTrue(audit["passed"], f"Custom daily SVG failed zero-origin audit: {audit}")

    def test_cross_day_deduplication_prioritizes_unseen_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            engine = DailyLinkedInPostEngine(
                store_path=tmp_root / "daily_generated_posts.json",
                visuals_root=tmp_root / "daily-posts",
            )
            day1 = engine.generate_daily_edition(edition_date="2026-10-28", count=3, use_live_network=False)
            day1_urls = {p["primary_url"] for p in day1["posts"]}
            day2 = engine.generate_daily_edition(edition_date="2026-10-29", count=3, use_live_network=False)
            day2_urls = {p["primary_url"] for p in day2["posts"]}
            # Since CURATED_LATEST_TOPICS has 6 distinct URLs, Day 2's top 3 must be 100% disjoint from Day 1's top 3
            self.assertEqual(len(day1_urls & day2_urls), 0)

    def test_http_endpoints_health_templates_and_daily_posts(self) -> None:
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            isolated_engine = DailyLinkedInPostEngine(
                store_path=tmp_root / "daily_generated_posts.json",
                visuals_root=tmp_root / "daily-posts",
            )
            with patch("server.DAILY_ENGINE", isolated_engine):
                httpd = ThreadingHTTPServer(("127.0.0.1", 0), StudioRequestHandler)
                port = httpd.server_address[1]
                thread = threading.Thread(target=httpd.serve_forever, daemon=True)
                thread.start()
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=5) as resp:
                        health = json.loads(resp.read().decode("utf-8"))
                    self.assertEqual(health["status"], "ok")
                    self.assertEqual(health["template_count"], 84)
                    self.assertEqual(health["creator_profiles_count"], 16)
                    self.assertEqual(health["mined_template_posts_count"], 16)

                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/templates", timeout=5) as resp:
                        tpl = json.loads(resp.read().decode("utf-8"))
                    self.assertEqual(tpl["template_count"], 84)

                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/daily-posts", timeout=5) as resp:
                        daily = json.loads(resp.read().decode("utf-8"))
                    self.assertEqual(daily["status"], "OK")
                    self.assertEqual(len(daily["posts"]), 6)

                    req = urllib.request.Request(
                        f"http://127.0.0.1:{port}/api/daily-posts/generate",
                        data=json.dumps(
                            {
                                "topic_query": "constrained decoding schema",
                                "creator_style": "STYLE-01",
                                "count": 2,
                                "edition_date": "2026-10-29",
                                "use_live_network": False,
                            }
                        ).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        gen = json.loads(resp.read().decode("utf-8"))
                    self.assertEqual(gen["status"], "GENERATED")
                    self.assertEqual(len(gen["posts"]), 2)
                    self.assertTrue(all(p["style_code"] == "STYLE-01" for p in gen["posts"]))
                finally:
                    httpd.shutdown()
                    httpd.server_close()


if __name__ == "__main__":
    unittest.main()
