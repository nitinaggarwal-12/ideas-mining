"""Master Unit Test Suite for the Ideas-Minting & OpenHands Repo Factory (MINT-01..12 + 10 Tomorrow Morning EST Ideas + 8 Analyzed Posts + 116 Certified Templates)."""

import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from src.catalog.career_minting_catalog import (
    CAREER_MINTING_TOPICS,
    FLAGSHIP_MINT01_24SLIDE_DECK_ID,
    FLAGSHIP_MINT01_24SLIDE_SHEET_ID,
    get_minted_repo_specs,
)
from src.catalog.posts_catalog import CREATOR_MINING_PLAYBOOK, POSTS_CATALOG, USER_PROFILE
from src.catalog.stack_pairings import (
    OSS_GOOGLE_PAIRINGS,
    OSS_STEP_EQUIVALENTS,
    oss_equivalent_for,
    oss_step_equivalent,
    pairing_rows_markdown,
)
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.harvester.idea_miner import AgenticIdeaMiner
from src.slides.slide_deck_compiler import build_12_slide_specs
from src.visuals.canonical_blueprint_minter import BANNED_LEGACY_GEN1_IDS, compute_canonical_siso
from src.visuals.canonical_flow_svg import _flow, audit_zero_origin_svg, generate_dynamic_solution_svg
from src.visuals.canonical_template_registry import (
    TEMPLATE_META,
    TOPIC_POSTS_T79,
    get_gallery_summary,
    list_templates,
    render_template,
)
from src.visuals.diagram_2d_engine import (
    format_nano_banana_3_prompt_markdown,
    generate_gcp_arch_78_drawio,
    generate_gcp_arch_78_svg,
    generate_linkedin_infographic_svg,
)


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
            self.assertIn("glassCardGrad", dyn_svg)
            self.assertIn("archGrid", dyn_svg)
            self.assertNotIn("...", dyn_svg)
            self.assertTrue(audit_zero_origin_svg(dyn_svg)["passed"], f"{idea['id']} dynamic SVG failed zero-origin gate")
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

    def test_template_gallery_renders_116_certified_templates_and_23_t79_topic_posts(self) -> None:
        summary = get_gallery_summary()
        self.assertEqual(summary["template_count"], 116)
        self.assertEqual(summary["best_count"], 72)
        self.assertEqual(summary["high_count"], 44)
        self.assertEqual(summary["medium_low_worst_count"], 0)
        self.assertEqual(summary["t79_topic_posts_count"], 23)
        self.assertEqual(len(TEMPLATE_META), 116)
        self.assertEqual(len(list_templates()), 116)

        all_renderable_ids = list(TEMPLATE_META.keys()) + [tp["id"] for tp in TOPIC_POSTS_T79]
        for tid in all_renderable_ids:
            self.assertNotIn(tid, BANNED_LEGACY_GEN1_IDS, f"Banned legacy Gen-1 ID {tid} must not appear")
            svg_live = render_template(tid)
            svg_frame = render_template(tid, phase=0.5)
            ET.fromstring(svg_live)
            ET.fromstring(svg_frame)
            self.assertIn("animateMotion", svg_live, tid)
            self.assertGreaterEqual(svg_live.count("<animateMotion"), 5, f"{tid} must have >= 5 end-to-end animated packets")
            self.assertGreaterEqual(svg_live.count('class="flow-line"'), 4, f"{tid} must have >= 4 internal animated conduits")
            self.assertEqual(svg_live.count("phase-pill-"), 4, f"{tid} must include 4-phase live telemetry strip")
            self.assertNotIn("M 20.0 2.0 L", svg_live, f"{tid} must not use legacy single top-line conduit at y=2.0")
            self.assertNotIn("animateMotion", svg_frame, tid)
            self.assertNotIn("claude", svg_live.lower(), f"{tid} contains forbidden Claude branding")
            self.assertNotIn("anthropic", svg_live.lower(), f"{tid} contains forbidden Anthropic branding")
            audit_live = audit_zero_origin_svg(svg_live)
            audit_frame = audit_zero_origin_svg(svg_frame)
            self.assertTrue(audit_live["passed"], f"{tid} failed Zero-Origin SVG gate (live): {audit_live}")
            self.assertTrue(audit_frame["passed"], f"{tid} failed Zero-Origin SVG gate (frame): {audit_frame}")

        tbus_svg = _flow([(100, 120), (320, 260)], "#2563EB", phase=0.5, converge_x=220)
        self.assertIn("M 100.0 120.0 L 220.0 120.0 L 220.0 260.0 L 310.0 260.0", tbus_svg)
        self.assertNotIn("transform=", tbus_svg)

    def test_purged_legacy_gen1_files_and_ids_rejected_fail_closed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for purged_mod in (
            "dynamic_diagram_engine.py",
            "template_gallery.py",
            "template_gallery_v2.py",
            "template_gallery_v3.py",
            "template_gallery_v4.py",
        ):
            self.assertFalse(
                (root / "src" / "visuals" / purged_mod).exists(),
                f"Legacy Gen-1 module src/visuals/{purged_mod} must remain permanently deleted",
            )
        gallery_dir = root / "assets" / "template-gallery"
        for legacy_id in BANNED_LEGACY_GEN1_IDS:
            for ext in ("svg", "png", "gif", "pptx", "drawio"):
                self.assertFalse(
                    (gallery_dir / f"{legacy_id}.{ext}").exists(),
                    f"Purged legacy Gen-1 file {legacy_id}.{ext} must not exist in assets/template-gallery/",
                )
        with self.assertRaises(ValueError):
            compute_canonical_siso(CAREER_MINTING_TOPICS[0], candidate_tid="T02")

    def test_career_minting_catalog_12_topics_siso_routing_and_flagship_mint01(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(len(CAREER_MINTING_TOPICS), 12)
        minted_tids = set()
        for idx, topic in enumerate(CAREER_MINTING_TOPICS, start=1):
            self.assertEqual(topic["id"], f"MINT-{idx:02d}")
            for req_key in (
                "title",
                "mnemonic",
                "mnemonic_expansion",
                "analogy",
                "golden_rule",
                "interview_signal",
                "gcp_stack",
                "oss_stack",
                "promo_impact",
                "canonical_template_id",
            ):
                self.assertTrue(topic.get(req_key), f"{topic['id']} missing {req_key}")
            siso = compute_canonical_siso(topic)
            self.assertNotIn(siso["resolved_canonical_template"], BANNED_LEGACY_GEN1_IDS)
            self.assertEqual(siso["resolved_canonical_template"], topic["canonical_template_id"])
            if siso["decision"] == "MINT_NEW":
                minted_tids.add(siso["resolved_canonical_template"])

        self.assertEqual(minted_tids, {"T85", "T86", "T87", "T88", "T89"})
        mint01 = CAREER_MINTING_TOPICS[0]
        self.assertEqual(mint01["mnemonic"], "S.C.O.P.E.")
        self.assertEqual(mint01["canonical_template_id"], "T85")
        self.assertEqual(mint01["flagship_24slide_deck_id"], FLAGSHIP_MINT01_24SLIDE_DECK_ID)
        self.assertEqual(mint01["flagship_24slide_sheet_id"], FLAGSHIP_MINT01_24SLIDE_SHEET_ID)

        vman_path = root / "assets" / "videos" / "MINT-01_video_manifest.json"
        self.assertTrue(vman_path.exists())
        vman = json.loads(vman_path.read_text(encoding="utf-8"))
        self.assertEqual(vman["ffprobe"]["width"], 1920)
        self.assertEqual(vman["ffprobe"]["height"], 1080)
        self.assertEqual(vman["ffprobe"]["video_codec"], "h264")
        self.assertEqual(vman["quality_gates"]["blueprint_occlusion_px2"], 0.0)
        self.assertTrue(vman["quality_gates"]["all_video_gates_passed"])

    def test_creator_mining_playbook_and_openhands_comparison(self) -> None:
        from pathlib import Path
        from src.catalog.posts_catalog import MINED_TEMPLATE_POSTS_CATALOG
        from src.harvester.idea_miner import AgenticIdeaMiner

        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["signal_channels"]), 6)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["diagram_archetypes_2d"]), 4)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["presentation_archetypes_12"]), 12)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["creator_profiles"]), 47)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["reviewed_posts"]), 46)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["omnichannel_platforms"]), 10)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["x_ecosystem_leaders"]), 15)
        self.assertEqual(len(MINED_TEMPLATE_POSTS_CATALOG), 16)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["openhands_superiority"]["comparison"]), 5)
        self.assertIn("nitin-aggarwal-b49786a", USER_PROFILE["linkedin_url"])

        repo_root = Path(__file__).resolve().parent.parent
        public_posts = [p for p in CREATOR_MINING_PLAYBOOK["reviewed_posts"] if p["availability"] == "PUBLIC_VERIFIED"]
        restricted_posts = [p for p in CREATOR_MINING_PLAYBOOK["reviewed_posts"] if p["availability"] != "PUBLIC_VERIFIED"]
        gif_posts = [p for p in public_posts if p.get("gif_url")]
        self.assertEqual(len(public_posts), 44)
        self.assertEqual(len(restricted_posts), 2)
        self.assertEqual(len(gif_posts), 10)
        for p in public_posts:
            img_path = repo_root / p["image_url"].lstrip("/")
            self.assertTrue(img_path.exists() and img_path.stat().st_size > 1000, f"Missing post image: {img_path}")
            if p.get("gif_url"):
                gif_path = repo_root / p["gif_url"].lstrip("/")
                self.assertTrue(gif_path.exists() and gif_path.stat().st_size > 10000, f"Missing post gif: {gif_path}")

        ingested = AgenticIdeaMiner().ingest_custom_post_or_url(
            "https://www.linkedin.com/feed/update/urn:li:activity:7472740776519577601"
        )
        self.assertEqual(ingested["status"], "MATCHED_REVIEWED_CREATOR_POST")
        self.assertEqual(ingested["matched_post_id"], "LI-26")

    def test_2d_visual_generators_produce_valid_light_theme_svg_and_drawio(self) -> None:
        for post in list(get_minted_repo_specs()) + list(POSTS_CATALOG) + list(TOMORROW_TOP10_IDEAS):
            poster_svg = generate_linkedin_infographic_svg(post)
            arch_svg = generate_gcp_arch_78_svg(post)
            drawio_xml = generate_gcp_arch_78_drawio(post)
            dyn_svg = generate_dynamic_solution_svg(post)

            ET.fromstring(poster_svg)
            ET.fromstring(arch_svg)
            ET.fromstring(dyn_svg)
            self.assertIn("#f8fafc", poster_svg.lower())
            self.assertIn("glassCardGrad", poster_svg)
            self.assertIn("glassCardGrad", arch_svg)
            self.assertIn("archGrid", poster_svg)
            self.assertIn("archGrid", arch_svg)
            self.assertNotIn("...", poster_svg)
            self.assertNotIn("...", arch_svg)
            self.assertNotIn("...", dyn_svg)
            self.assertTrue(audit_zero_origin_svg(poster_svg)["passed"], f"{post['id']} poster SVG failed zero-origin gate")
            self.assertTrue(audit_zero_origin_svg(arch_svg)["passed"], f"{post['id']} #78 SVG failed zero-origin gate")
            self.assertTrue(audit_zero_origin_svg(dyn_svg)["passed"], f"{post['id']} dynamic SVG failed zero-origin gate")
            self.assertIn("Proprietary + Confidential", poster_svg)
            self.assertIn("TEMPLATE #78 HUB-AND-SPOKE BLUEPRINT", arch_svg)
            self.assertIn("18/18 CARDS • 23 EDGES", arch_svg)
            self.assertIn("ZONE 5 • PRODUCTION TELEMETRY", arch_svg)
            self.assertIn("<mxGraphModel", drawio_xml)
            self.assertIn("e_alb_to_mid_left", drawio_xml)

    def test_12_slide_story_arc_and_spoken_notes(self) -> None:
        for post in list(get_minted_repo_specs()) + list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG):
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

        matched_t69 = miner.ingest_custom_post_or_url(
            "https://www.linkedin.com/feed/update/urn:li:activity:7518498821123895296/"
        )
        self.assertEqual(matched_t69["status"], "MATCHED_EXISTING_VERIFIED_POST")
        self.assertEqual(matched_t69["template_id"], "T69")

        custom = miner.ingest_custom_post_or_url(
            "https://arxiv.org/abs/2610.99999",
            custom_title="Multi-Agent Context Compaction on Vertex AI",
        )
        self.assertEqual(custom["status"], "SYNTHESIZED_GROUNDED_BLUEPRINT")
        self.assertTrue(custom["repo_slug"].startswith("custom-"))

    def test_tomorrow_top10_template_and_distribution_plan(self) -> None:
        from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_DISTRIBUTION_PLAN

        root = Path(__file__).resolve().parents[1]
        valid_ids = set(TEMPLATE_META.keys()) | {tp["id"] for tp in TOPIC_POSTS_T79}
        self.assertEqual(len(TOMORROW_TOP10_IDEAS), 10)
        self.assertEqual(len(TOMORROW_TOP10_DISTRIBUTION_PLAN), 10)

        for idea in list(get_minted_repo_specs()) + list(TOMORROW_TOP10_IDEAS):
            plan = idea.get("template_and_distribution_plan")
            self.assertIsNotNone(plan, f"{idea['id']} missing template_and_distribution_plan")
            self.assertIn(plan["primary_template_id"], valid_ids, f"{idea['id']} invalid primary_template_id")
            for sec_tid in plan["secondary_template_ids"]:
                self.assertIn(sec_tid, valid_ids, f"{idea['id']} invalid secondary_template_id {sec_tid}")
            for file_key in ("editable_slidedeck_pptx", "pdf_deliverable"):
                self.assertTrue(
                    (root / plan[file_key]).exists(),
                    f"{idea['id']} missing deliverable on disk: {plan[file_key]}",
                )

    def test_t01_and_t53_to_t89_canonical_drawio_alignment_and_proportional_sizing(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drawio_dir = root / "assets" / "canonical-ref" / "drawio"
        spine_4tier_tids = {"T01", "T53", "T68"} | {f"T{i}" for i in range(69, 90)}
        for tid in ["T01"] + [f"T{i}" for i in range(53, 90)]:
            xml_path = drawio_dir / f"{tid}.drawio"
            self.assertTrue(xml_path.exists(), f"Missing canonical Draw.io XML {xml_path}")
            tree = ET.parse(xml_path).getroot()
            gm = tree.find(".//mxGraphModel")
            self.assertIsNotNone(gm)
            pw = float(gm.get("pageWidth", "0"))
            ph = float(gm.get("pageHeight", "0"))
            self.assertLessEqual(pw, 1100.0, f"{tid} pageWidth={pw} exceeds proportional 1100px cap")
            if tid in spine_4tier_tids:
                self.assertEqual((pw, ph), (1020.0, 1040.0), f"{tid} must use proportional 1020x1040 layout")

            cells = {}
            edges = []
            ordered_ids = []
            for c in tree.findall(".//mxCell"):
                cid = c.get("id", "")
                ordered_ids.append(cid)
                g = c.find("mxGeometry")
                if c.get("vertex") == "1" and g is not None:
                    x = float(g.get("x", "0"))
                    y = float(g.get("y", "0"))
                    w = float(g.get("width", "0"))
                    h = float(g.get("height", "0"))
                    cells[cid] = {
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        "cx": x + w / 2.0,
                        "cy": y + h / 2.0,
                        "val": c.get("value", ""),
                    }
                elif c.get("edge") == "1":
                    pt = g.find("mxPoint[@as='offset']") if g is not None else None
                    ox = float(pt.get("x", "0")) if pt is not None else None
                    oy = float(pt.get("y", "0")) if pt is not None else None
                    edges.append((cid, c.get("source", ""), c.get("target", ""), c.get("style", ""), c.get("value", ""), ox, oy))

            edge_map = {eid: (val, ox, oy) for eid, _, _, _, val, ox, oy in edges}
            for eid, s, t, st, _, _, _ in edges:
                if s in cells and t in cells and "orthogonalEdgeStyle" not in st and not eid.startswith("t4_m"):
                    dx = abs(cells[s]["cx"] - cells[t]["cx"])
                    dy = abs(cells[s]["cy"] - cells[t]["cy"])
                    self.assertLessEqual(
                        min(dx, dy),
                        0.5,
                        f"{tid} edge {eid} ({s} -> {t}) is crooked/slanted: dx={dx}, dy={dy}",
                    )

            if tid in spine_4tier_tids:
                self.assertIn("t2_edge_in2", ordered_ids, f"{tid} missing t2_edge_in2 connector from t2_skills_pill")
                for b_idx, t_id in [("badge_01", "t1_title"), ("badge_02", "t2_title"), ("badge_03", "t3_title"), ("badge_04", "t4_title")]:
                    self.assertAlmostEqual(cells[b_idx]["cy"], cells[t_id]["cy"], places=1, msg=f"{tid} {b_idx} misaligned with {t_id}")
                for pbar in ("t1_prompt_bar", "t2_prompt_bar", "t3_prompt_bar", "t4_prompt_bar"):
                    self.assertIn("width:842px", cells[pbar]["val"], f"{tid} {pbar} must use full-width 842px table")
                expected_offsets = {
                    "t1_edge_1": (-5.0, -2.0),
                    "t2_edge_calls": (-5.0, -2.0),
                    "t2_edge_returns": (0.0, -2.0),
                    "t3_e_yes1": (-5.0, -1.5),
                    "t3_e_no1": (0.0, -6.0),
                    "t3_e_yes2": (-5.0, -1.5),
                    "t3_e_no2": (5.0, -1.5),
                    "t4_edge_maps": (-5.0, -2.0),
                }
                for eid, (exp_ox, exp_oy) in expected_offsets.items():
                    val, ox, oy = edge_map[eid]
                    self.assertIn("padding:0 2px;", val, f"{tid} {eid} missing 2px horizontal cushion")
                    self.assertEqual(ox, exp_ox, f"{tid} {eid} x-offset mismatch: got {ox}, expected {exp_ox}")
                    self.assertEqual(oy, exp_oy, f"{tid} {eid} y-offset mismatch: got {oy}, expected {exp_oy}")

    def test_zero_legacy_fallbacks_stale_assets_or_placeholder_urls(self) -> None:
        root = Path(__file__).resolve().parents[1]
        reg_src = (root / "src" / "visuals" / "canonical_template_registry.py").read_text(encoding="utf-8")
        self.assertIn("st_mtime_ns", reg_src, "canonical_template_registry.py must invalidate _B64_CACHE on st_mtime_ns change")

        d2d_src = (root / "src" / "visuals" / "diagram_2d_engine.py").read_text(encoding="utf-8")
        self.assertNotIn('shutil.copyfile(dyn_png, visuals_dir / "linkedin-infographic-2d.png")', d2d_src)
        self.assertNotIn('shutil.copyfile(arch_png, visuals_dir / "gcp-architecture-2d.png")', d2d_src)
        self.assertNotIn('NANO_BANANA_3_PROMPTS.get(pid, NANO_BANANA_3_PROMPTS["POST-08"])', d2d_src)
        self.assertNotIn("visual-templates-gallery", d2d_src)

        for idea in list(get_minted_repo_specs()) + list(TOMORROW_TOP10_IDEAS):
            svg_info = generate_linkedin_infographic_svg(idea)
            self.assertIn(f'id="bespoke-{idea["id"].lower()}"', svg_info)
            self.assertNotIn('id="bespoke-post-08"', svg_info)
            spec_md = format_nano_banana_3_prompt_markdown(idea)
            self.assertIn(idea["post_title"].upper(), spec_md)

        self.assertFalse((root / "assets" / "nano-banana-3").exists())
        self.assertFalse((root / "generated-repos" / "visual-templates-gallery").exists())
        for py_file in (root / "src").rglob("*.py"):
            self.assertNotIn("example.com", py_file.read_text(encoding="utf-8"), f"Placeholder example.com URL found in {py_file}")

        ref_pngs = sorted(p.name for p in (root / "assets" / "canonical-ref").glob("*.png"))
        all_canonical_ids = set(TEMPLATE_META.keys()) | {tp["id"] for tp in TOPIC_POSTS_T79}
        expected_pngs = sorted([f"canonical_{tid}.png" for tid in all_canonical_ids])
        self.assertEqual(ref_pngs, expected_pngs, f"Stale/duplicate PNGs in assets/canonical-ref/: {ref_pngs}")

    def test_t01_and_t53_to_t89_editable_pptx_and_google_slides_manifest(self) -> None:
        root = Path(__file__).resolve().parents[1]
        slides_manifest_path = root / "data" / "template_google_slides_manifest.json"
        gallery_manifest_path = root / "assets" / "template-gallery" / "gallery_manifest.json"
        self.assertTrue(slides_manifest_path.exists())
        self.assertTrue(gallery_manifest_path.exists())

        slides_manifest = json.loads(slides_manifest_path.read_text(encoding="utf-8")).get("slides", {})
        gallery_payload = json.loads(gallery_manifest_path.read_text(encoding="utf-8"))
        gallery_items = {t["id"]: t for t in gallery_payload.get("templates", [])}
        t79_topics = {tp["id"]: tp for tp in gallery_items.get("T79", {}).get("topic_posts", [])}

        for tid in ["T01"] + [f"T{i}" for i in range(53, 90)]:
            drawio_file = root / "assets" / "template-gallery" / f"{tid}.drawio"
            pptx_file = root / "assets" / "template-gallery" / f"{tid}.pptx"
            self.assertTrue(drawio_file.exists(), f"Missing editable Draw.io file {drawio_file}")
            self.assertTrue(pptx_file.exists(), f"Missing editable PowerPoint file {pptx_file}")
            self.assertGreater(pptx_file.stat().st_size, 20000, f"{tid}.pptx is unexpectedly small")

            self.assertIn(tid, slides_manifest, f"{tid} missing from data/template_google_slides_manifest.json")
            sm = slides_manifest[tid]
            self.assertTrue(sm.get("googleSlidesId"), f"{tid} missing googleSlidesId")
            self.assertIn("docs.google.com/presentation/d/", sm.get("googleSlidesEditUrl", ""), f"{tid} invalid googleSlidesEditUrl")
            self.assertGreaterEqual(sm.get("slideCount", 0), 2, f"{tid} must have >= 2 editable slides")

            g_item = gallery_items.get(tid) or t79_topics.get(tid) or {}
            self.assertEqual(g_item.get("files", {}).get("drawio"), f"{tid}.drawio")
            self.assertEqual(g_item.get("files", {}).get("pptx"), f"{tid}.pptx")
            self.assertEqual(g_item.get("google_slides_id"), sm["googleSlidesId"])
            self.assertEqual(g_item.get("google_slides_url"), sm["googleSlidesEditUrl"])

    def test_step_by_step_flow_animator_and_presets(self) -> None:
        from src.visuals.step_by_step_flow_animator import (
            STEP_FLOW_PRESETS,
            generate_step_by_step_flow_svg,
            render_step_flow_bundle,
        )

        self.assertGreaterEqual(len(STEP_FLOW_PRESETS), 3)
        for pid in ("FLOW-01", "FLOW-02", "FLOW-03"):
            bundle = render_step_flow_bundle(preset_id=pid, custom_topic="", theme="light", compile_gif=False)
            self.assertEqual(bundle["status"], "ok")
            self.assertEqual(bundle["preset_id"], pid)
            self.assertEqual(len(bundle["copy_bundle"]["beats"]), 6)
            svg_light = generate_step_by_step_flow_svg(bundle["spec"], theme="light", frame_phase=None)
            svg_dark = generate_step_by_step_flow_svg(bundle["spec"], theme="dark_neon", frame_phase=0.6)
            self.assertIn('viewBox="0 0 1080 1350"', svg_light)
            self.assertIn("#F8FAFC", svg_light)
            self.assertIn("#0B1120", svg_dark)
            self.assertIn("Google Cloud Agentic Architecture Engineering", svg_light)


if __name__ == "__main__":
    unittest.main()
