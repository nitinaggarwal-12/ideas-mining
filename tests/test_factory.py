"""Master Unit Test Suite for the Ideas Mining & OpenHands Repo Factory (8 Analyzed Posts + 10 Tomorrow Morning EST Daily Pain-Point Ideas)."""

import unittest
import xml.etree.ElementTree as ET

from src.catalog.posts_catalog import CREATOR_MINING_PLAYBOOK, POSTS_CATALOG, USER_PROFILE
from src.catalog.stack_pairings import OSS_GOOGLE_PAIRINGS, OSS_STEP_EQUIVALENTS, oss_equivalent_for, oss_step_equivalent, pairing_rows_markdown
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.harvester.idea_miner import AgenticIdeaMiner
from src.slides.slide_deck_compiler import build_12_slide_specs
from src.visuals.diagram_2d_engine import (
    generate_gcp_arch_78_drawio,
    generate_gcp_arch_78_svg,
    generate_linkedin_infographic_svg,
)
from src.visuals.dynamic_diagram_engine import generate_dynamic_solution_svg
from src.visuals.template_gallery import TEMPLATE_META, list_templates, render_template


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
            self.assertEqual(dyn_svg.count("GOOGLE: "), 4)
            self.assertEqual(dyn_svg.count("OSS: "), 4)

    def test_oss_google_stack_pairings_are_complete_and_grounded(self) -> None:
        self.assertEqual(len(OSS_GOOGLE_PAIRINGS), 12)
        for pairing in OSS_GOOGLE_PAIRINGS:
            for key in ("capability", "google", "oss", "note"):
                self.assertTrue(pairing[key].strip())
        for idea in TOMORROW_TOP10_IDEAS:
            self.assertEqual(len(OSS_STEP_EQUIVALENTS[idea["id"]]), 4)
            for st in idea["dynamic_steps"]:
                self.assertTrue(oss_step_equivalent(idea["id"], st["step"], st["gcp_primitive"]).strip())
        self.assertIn("LangGraph", oss_equivalent_for("Google Cloud ADK (BeforeToolCallback)"))
        self.assertIn("Llama Guard", oss_equivalent_for("Google Cloud Model Armor"))
        self.assertIn("OpenTelemetry", oss_equivalent_for("Cloud Trace OpenTelemetry"))
        self.assertIn("| **Agent orchestration", pairing_rows_markdown())

    def test_template_gallery_renders_20_valid_dynamic_templates_with_oss_and_google(self) -> None:
        self.assertEqual(len(TEMPLATE_META), 20)
        self.assertEqual([t["id"] for t in list_templates()], [f"T{i:02d}" for i in range(1, 21)])
        oss_markers = ("LangGraph", "OpenHands", "vLLM", "PostgreSQL", "OpenTelemetry", "Llama Guard", "Temporal", "Promptfoo", "MCP", "Knative", "pgvector", "Redis", "Qdrant", "LiteLLM")
        google_markers = ("Google", "Vertex", "Gemini", "Firestore", "Cloud Run", "ADK", "Model Armor", "BigQuery", "AlloyDB", "Cloud Trace")
        for tid, meta in TEMPLATE_META.items():
            self.assertGreaterEqual(len(meta["content_types"]), 2)
            svg_live = render_template(tid)
            svg_frame = render_template(tid, phase=0.5)
            ET.fromstring(svg_live)
            ET.fromstring(svg_frame)
            self.assertIn("animateMotion", svg_live, tid)
            self.assertIn("#F8FAFC", svg_live, tid)
            self.assertIn("Proprietary + Confidential", svg_live, tid)
            self.assertTrue(any(m in svg_live for m in oss_markers), f"{tid} missing open-source stack mention")
            self.assertTrue(any(m in svg_live for m in google_markers), f"{tid} missing Google Cloud stack mention")
            self.assertNotIn("animateMotion", svg_frame, tid)

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
