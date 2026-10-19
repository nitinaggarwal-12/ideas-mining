"""Master Unit Test Suite for the Ideas Mining & OpenHands Repo Factory (8 Analyzed Posts + 10 Tomorrow Morning EST Daily Pain-Point Ideas)."""

import unittest
import xml.etree.ElementTree as ET

from src.catalog.posts_catalog import CREATOR_MINING_PLAYBOOK, POSTS_CATALOG, USER_PROFILE
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.harvester.idea_miner import AgenticIdeaMiner
from src.slides.slide_deck_compiler import build_12_slide_specs
from src.visuals.diagram_2d_engine import (
    generate_gcp_arch_78_drawio,
    generate_gcp_arch_78_svg,
    generate_linkedin_infographic_svg,
)
from src.visuals.dynamic_diagram_engine import generate_dynamic_solution_svg


class TestIdeasMiningFactory(unittest.TestCase):
    def test_catalog_contains_all_8_posts_and_primary_sources(self) -> None:
        self.assertEqual(len(POSTS_CATALOG), 8)
        for post in POSTS_CATALOG:
            self.assertTrue(post["id"].startswith("POST-0"))
            self.assertTrue(post["activity_urn"].startswith("urn:li:activity:"))
            self.assertGreaterEqual(len(post["primary_source"]["verified_claims"]), 3)
            self.assertEqual(len(post["core_steps"]), 6)

    def test_tomorrow_top10_daily_pain_point_ideas_and_dynamic_moving_arrow_svgs(self) -> None:
        self.assertEqual(len(TOMORROW_TOP10_IDEAS), 10)
        for idx, idea in enumerate(TOMORROW_TOP10_IDEAS, start=1):
            self.assertEqual(idea["id"], f"IDEA-{idx:02d}")
            self.assertIn("EST", idea["est_post_time"])
            self.assertEqual(len(idea["problem_flow_nodes"]), 3)
            self.assertEqual(len(idea["dynamic_steps"]), 4)
            self.assertEqual(len(idea["core_steps"]), 6)

            dyn_svg = generate_dynamic_solution_svg(idea)
            ET.fromstring(dyn_svg)
            self.assertIn("moving-arrow-line", dyn_svg)
            self.assertIn("animateMotion", dyn_svg)
            self.assertIn("CLOSED-LOOP FEEDBACK", dyn_svg)
            self.assertIn("#F8FAFC", dyn_svg)

    def test_creator_mining_playbook_and_openhands_comparison(self) -> None:
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["signal_channels"]), 4)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["diagram_archetypes_2d"]), 4)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["openhands_superiority"]["comparison"]), 3)
        self.assertIn("nitin-aggarwal-b49786a", USER_PROFILE["linkedin_url"])

    def test_2d_visual_generators_produce_valid_light_theme_svg_and_drawio(self) -> None:
        for post in POSTS_CATALOG:
            poster_svg = generate_linkedin_infographic_svg(post)
            arch_svg = generate_gcp_arch_78_svg(post)
            drawio_xml = generate_gcp_arch_78_drawio(post)

            self.assertIn("#f8fafc", poster_svg.lower())
            self.assertIn("Proprietary + Confidential", poster_svg)
            self.assertIn(f'id="bespoke-{post["id"].lower()}"', poster_svg)
            self.assertIn("TEMPLATE #78 HUB-AND-SPOKE BLUEPRINT", arch_svg)
            self.assertIn("18/18 CARDS • 23 EDGES", arch_svg)
            self.assertIn("ZONE 5 • PRODUCTION TELEMETRY", arch_svg)
            self.assertIn("<mxGraphModel", drawio_xml)
            self.assertIn("e_alb_to_mid_left", drawio_xml)

    def test_12_slide_story_arc_and_spoken_notes(self) -> None:
        for post in list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG):
            slides = build_12_slide_specs(post)
            self.assertEqual(len(slides), 12)
            for s in slides:
                self.assertEqual(len(s["spoken_notes"]), 3)

    def test_idea_miner_url_ingestion_matches_catalog_and_custom_urls(self) -> None:
        miner = AgenticIdeaMiner()
        matched = miner.ingest_custom_post_or_url(
            "https://www.linkedin.com/feed/update/urn:li:activity:7517563942492196864/"
        )
        self.assertEqual(matched["status"], "MATCHED_EXISTING_VERIFIED_POST")
        self.assertEqual(matched["matched_post_id"], "POST-01")

        custom = miner.ingest_custom_post_or_url(
            "https://arxiv.org/abs/2610.99999",
            custom_title="Multi-Agent Context Compaction on Vertex AI",
        )
        self.assertEqual(custom["status"], "SYNTHESIZED_GROUNDED_BLUEPRINT")
        self.assertTrue(custom["repo_slug"].startswith("custom-"))


if __name__ == "__main__":
    unittest.main()
