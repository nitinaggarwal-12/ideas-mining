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
from src.visuals.template_gallery import TEMPLATE_META, _flow, audit_zero_origin_svg, list_templates, render_template


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

    def test_template_gallery_renders_84_valid_dynamic_templates_with_oss_and_google(self) -> None:
        self.assertEqual(len(TEMPLATE_META), 84)
        self.assertEqual([t["id"] for t in list_templates()], [f"T{i:02d}" for i in range(1, 85)])
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
            self.assertIn("glassCardGrad", svg_live, tid)
            self.assertIn("glassSheen", svg_live, tid)
            self.assertIn("archGrid", svg_live, tid)
            self.assertIn("Proprietary + Confidential", svg_live, tid)
            self.assertTrue(any(m in svg_live for m in oss_markers), f"{tid} missing open-source stack mention")
            self.assertTrue(any(m in svg_live for m in google_markers), f"{tid} missing Google Cloud stack mention")
            self.assertNotIn("animateMotion", svg_frame, tid)
            # Zero-Origin W3C SVG Flattener & Official Google Cloud Brand Gate (b/571807152)
            audit_live = audit_zero_origin_svg(svg_live)
            audit_frame = audit_zero_origin_svg(svg_frame)
            self.assertTrue(audit_live["passed"], f"{tid} failed Zero-Origin SVG gate (live): {audit_live}")
            self.assertTrue(audit_frame["passed"], f"{tid} failed Zero-Origin SVG gate (frame): {audit_frame}")
            if int(tid[1:]) >= 21:
                self.assertTrue(meta.get("lineage"), f"{tid} must declare its creator/source lineage")
                self.assertIn("FORMAT LINEAGE:", svg_live, tid)

        # Verify T-Bus convergence helper in _flow produces zero-origin baked polygon arrowheads
        tbus_svg = _flow([(100, 120), (320, 260)], "#2563EB", phase=0.5, converge_x=220)
        self.assertIn("M 100.0 120.0 L 220.0 120.0 L 220.0 260.0 L 310.0 260.0", tbus_svg)
        self.assertNotIn("transform=", tbus_svg)

    def test_t31_demo_code_really_runs_and_matches_the_printed_output(self) -> None:
        import contextlib
        import io
        from src.visuals.template_gallery_v2 import DEMO_CODE_T31, DEMO_OUTPUT_T31

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec("\n".join(DEMO_CODE_T31), {})
        self.assertEqual(buf.getvalue().strip().splitlines(), DEMO_OUTPUT_T31)
        self.assertLessEqual(len(DEMO_CODE_T31), 26)

    def test_t29_kappa_worked_example_is_arithmetically_correct(self) -> None:
        from src.visuals.template_gallery_v2 import demo_specs_v2

        items = demo_specs_v2()["T29"]["items"]
        n = len(items)
        a = sum(1 for it in items if it["human"] == "PASS" and it["judge"] == "PASS")
        d = sum(1 for it in items if it["human"] == "FAIL" and it["judge"] == "FAIL")
        po = (a + d) / n
        ph = sum(1 for it in items if it["human"] == "PASS") / n
        pj = sum(1 for it in items if it["judge"] == "PASS") / n
        pe = ph * pj + (1 - ph) * (1 - pj)
        kappa = (po - pe) / (1 - pe)
        self.assertEqual(n, 10)
        self.assertAlmostEqual(po, 0.8)
        self.assertAlmostEqual(pe, 0.52)
        self.assertAlmostEqual(kappa, 0.5833, places=3)

    def test_creator_mining_playbook_and_openhands_comparison(self) -> None:
        from src.catalog.posts_catalog import MINED_TEMPLATE_POSTS_CATALOG

        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["signal_channels"]), 4)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["diagram_archetypes_2d"]), 4)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["creator_profiles"]), 16)
        self.assertEqual(len(MINED_TEMPLATE_POSTS_CATALOG), 16)
        self.assertEqual(len(CREATOR_MINING_PLAYBOOK["openhands_superiority"]["comparison"]), 5)
        self.assertIn("nitin-aggarwal-b49786a", USER_PROFILE["linkedin_url"])

    def test_2d_visual_generators_produce_valid_light_theme_svg_and_drawio(self) -> None:
        for post in list(POSTS_CATALOG) + list(TOMORROW_TOP10_IDEAS):
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
            if post["id"].startswith("POST-"):
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
        from pathlib import Path
        from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_DISTRIBUTION_PLAN

        root = Path(__file__).resolve().parents[1]
        catalog_ids = set(TEMPLATE_META.keys())
        self.assertEqual(len(TOMORROW_TOP10_IDEAS), 10)
        self.assertEqual(len(TOMORROW_TOP10_DISTRIBUTION_PLAN), 10)

        for idea in TOMORROW_TOP10_IDEAS:
            plan = idea.get("template_and_distribution_plan")
            self.assertIsNotNone(plan, f"{idea['id']} missing template_and_distribution_plan")
            self.assertIn(plan["primary_template_id"], catalog_ids, f"{idea['id']} invalid primary_template_id")
            for sec_tid in plan["secondary_template_ids"]:
                self.assertIn(sec_tid, catalog_ids, f"{idea['id']} invalid secondary_template_id {sec_tid}")
            for required_key in (
                "primary_template_name",
                "lead_post_format",
                "visual_type",
                "carousel_spec",
                "dynamic_nature",
                "editable_slidedeck_pptx",
                "pdf_deliverable",
                "linkedin_groups_primary",
                "linkedin_groups_niche_network",
                "comment_magnet_question",
            ):
                self.assertTrue(plan.get(required_key), f"{idea['id']} missing {required_key}")
            self.assertGreaterEqual(len(plan["linkedin_groups_primary"]), 2)
            self.assertGreaterEqual(len(plan["linkedin_groups_niche_network"]), 2)
            for file_key in (
                "editable_slidedeck_pptx",
                "pdf_deliverable",
            ):
                self.assertTrue(
                    (root / plan[file_key]).exists(),
                    f"{idea['id']} missing deliverable on disk: {plan[file_key]}",
                )

    def test_t01_to_t05_publication_grade_density_and_zero_claude_branding(self) -> None:
        for tid in TEMPLATE_META:
            svg = render_template(tid)
            self.assertNotIn("claude", svg.lower(), f"{tid} contains forbidden Claude branding")
            self.assertNotIn("anthropic", svg.lower(), f"{tid} contains forbidden Anthropic branding")
        t02 = render_template("T02")
        self.assertIn("THREAT VECTOR • OWASP LLM01", t02)
        self.assertIn("RUNTIME TRACE • CLEAN", t02)
        self.assertIn("BLOCKS STEP 1", t02)
        t03 = render_template("T03")
        self.assertIn("HARNESS KERNEL", t03)
        self.assertIn("ADK • LANGGRAPH BUS", t03)
        self.assertIn("ARCHITECTURAL FORMULA", t03)
        t04 = render_template("T04")
        self.assertIn("① REQUEST IN", t04)
        self.assertIn("② L5 VERIFIED GUARANTEE", t04)
        self.assertIn("OSS: DeepSeek-R1 vLLM", t04)
        t05 = render_template("T05")
        self.assertIn("CONTEXT ENVELOPE -&gt; STEP 2", t05)
        self.assertIn("DETERMINISTIC AGENT EXECUTION FLYWHEEL", t05)
        self.assertIn("exit_code == 0", t05)

    def test_t53_to_t84_canonical_drawio_alignment_and_proportional_sizing(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        drawio_dir = root / "assets" / "canonical-ref" / "drawio"
        spine_4tier_tids = {"T01", "T53", "T68"} | {f"T{i}" for i in range(69, 85)}
        for tid in ["T01"] + [f"T{i}" for i in range(53, 85)]:
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
                    cells[cid] = {"x": x, "y": y, "w": w, "h": h, "cx": x + w / 2.0, "cy": y + h / 2.0, "val": c.get("value", "")}
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
                # Verify visible-shaft centering gaps (>= 76px horizontal, >= 44px vertical)
                self.assertGreaterEqual(cells["t1_model_circle"]["x"] - (cells["t1_loaded_box"]["x"] + cells["t1_loaded_box"]["w"]), 76.0)
                self.assertGreaterEqual(cells["t2_tools_card"]["x"] - (cells["t2_model_circle"]["x"] + cells["t2_model_circle"]["w"]), 80.0)
                self.assertGreaterEqual(cells["t3_done_pill"]["x"] - (cells["t3_gate_pass"]["x"] + cells["t3_gate_pass"]["w"]), 76.0)
                self.assertGreaterEqual(cells["t3_gate_tries"]["x"] - (cells["t3_fix_box"]["x"] + cells["t3_fix_box"]["w"]), 76.0)
                self.assertGreaterEqual(cells["t3_gate_tries"]["y"] - (cells["t3_gate_pass"]["y"] + cells["t3_gate_pass"]["h"]), 44.0)
                self.assertGreaterEqual(cells["t4_map_card"]["x"] - (cells["t4_folder_box"]["x"] + cells["t4_folder_box"]["w"]), 88.0)
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

            if tid == "T54":
                self.assertLess(
                    ordered_ids.index("band53_3"),
                    ordered_ids.index("e53_m_C"),
                    "T54 band53_3 must precede collector edge e53_m_C so the arrow is not occluded",
                )
                self.assertAlmostEqual(cells["pil53_yes2"]["cx"], 545.0, places=1)
                self.assertAlmostEqual(cells["pil53_no2"]["cx"], 876.5, places=1)
                self.assertAlmostEqual(cells["pil53_rec"]["cx"], 792.5, places=1)

            if tid == "T64":
                self.assertAlmostEqual(cells["p63_no1"]["cx"], 290.0, places=1)
                self.assertAlmostEqual(cells["p63_no2"]["cx"], 288.0, places=1)
                self.assertAlmostEqual(cells["p63_yes2"]["cx"], 475.0, places=1)
                self.assertAlmostEqual(cells["p63_no3"]["cx"], 578.0, places=1)
                self.assertAlmostEqual(cells["p63_no4"]["cx"], 291.0, places=1)

    def test_zero_legacy_fallbacks_stale_assets_or_placeholder_urls(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        v4_src = (root / "src" / "visuals" / "template_gallery_v4.py").read_text(encoding="utf-8")
        for banned_token in ("_FALLBACK_RENDERERS_V4", "def render_t5", "def render_t6", "def _num_badge", "def _toggle_switch"):
            self.assertNotIn(banned_token, v4_src, f"Legacy hand-rolled fallback token '{banned_token}' found in template_gallery_v4.py")
        self.assertIn("st_mtime_ns", v4_src, "template_gallery_v4.py must invalidate _B64_CACHE on st_mtime_ns change")

        d2d_src = (root / "src" / "visuals" / "diagram_2d_engine.py").read_text(encoding="utf-8")
        self.assertNotIn('shutil.copyfile(dyn_png, visuals_dir / "linkedin-infographic-2d.png")', d2d_src)
        self.assertNotIn('shutil.copyfile(arch_png, visuals_dir / "gcp-architecture-2d.png")', d2d_src)
        self.assertNotIn('NANO_BANANA_3_PROMPTS.get(pid, NANO_BANANA_3_PROMPTS["POST-08"])', d2d_src)
        self.assertNotIn("visual-templates-gallery", d2d_src)

        from src.visuals.diagram_2d_engine import format_nano_banana_3_prompt_markdown
        for idea in TOMORROW_TOP10_IDEAS:
            svg_info = generate_linkedin_infographic_svg(idea)
            self.assertIn(f'id="bespoke-{idea["id"].lower()}"', svg_info)
            self.assertNotIn('id="bespoke-post-08"', svg_info)
            spec_md = format_nano_banana_3_prompt_markdown(idea)
            self.assertIn(idea["post_title"].upper(), spec_md)
            self.assertNotIn("HOW AN AI AGENT ACTUALLY WORKS END-TO-END IN PRODUCTION", spec_md)

        build_all_src = (root / "scripts" / "build_and_verify_all.py").read_text(encoding="utf-8")
        self.assertNotIn("if not infographic_png.exists():", build_all_src)
        self.assertNotIn("if not arch_png.exists():", build_all_src)

        self.assertFalse((root / "assets" / "nano-banana-3").exists(), "Distorted diffusion directory assets/nano-banana-3 must remain purged")
        self.assertFalse((root / "generated-repos" / "visual-templates-gallery").exists(), "Legacy mirror directory generated-repos/visual-templates-gallery must remain purged")
        self.assertEqual(list((root / "generated-repos").glob("*/visuals/gcp-architecture-78.drawio")), [])

        for py_file in (root / "src").rglob("*.py"):
            self.assertNotIn("example.com", py_file.read_text(encoding="utf-8"), f"Placeholder example.com URL found in {py_file}")

        ref_pngs = sorted(p.name for p in (root / "assets" / "canonical-ref").glob("*.png"))
        expected_pngs = sorted(["canonical_T01.png"] + [f"canonical_T{i}.png" for i in range(53, 85)])
        self.assertEqual(ref_pngs, expected_pngs, f"Stale/duplicate PNGs in assets/canonical-ref/: {ref_pngs}")

    def test_t01_and_t53_to_t84_editable_pptx_and_google_slides_manifest(self) -> None:
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        slides_manifest_path = root / "data" / "template_google_slides_manifest.json"
        gallery_manifest_path = root / "assets" / "template-gallery" / "gallery_manifest.json"
        self.assertTrue(slides_manifest_path.exists(), "Missing data/template_google_slides_manifest.json")
        self.assertTrue(gallery_manifest_path.exists(), "Missing assets/template-gallery/gallery_manifest.json")

        slides_manifest = json.loads(slides_manifest_path.read_text(encoding="utf-8")).get("slides", {})
        gallery_items = {
            t["id"]: t for t in json.loads(gallery_manifest_path.read_text(encoding="utf-8")).get("templates", [])
        }

        for tid in ["T01"] + [f"T{i}" for i in range(53, 85)]:
            drawio_file = root / "assets" / "template-gallery" / f"{tid}.drawio"
            pptx_file = root / "assets" / "template-gallery" / f"{tid}.pptx"
            self.assertTrue(drawio_file.exists(), f"Missing editable Draw.io file {drawio_file}")
            self.assertTrue(pptx_file.exists(), f"Missing editable PowerPoint file {pptx_file}")
            self.assertGreater(pptx_file.stat().st_size, 40000, f"{tid}.pptx is unexpectedly small")

            self.assertIn(tid, slides_manifest, f"{tid} missing from data/template_google_slides_manifest.json")
            sm = slides_manifest[tid]
            self.assertTrue(sm.get("googleSlidesId"), f"{tid} missing googleSlidesId")
            self.assertIn("docs.google.com/presentation/d/", sm.get("googleSlidesEditUrl", ""), f"{tid} invalid googleSlidesEditUrl")
            self.assertGreaterEqual(sm.get("slideCount", 0), 2, f"{tid} must have >= 2 editable slides")

            g_item = gallery_items.get(tid, {})
            self.assertEqual(g_item.get("files", {}).get("drawio"), f"{tid}.drawio")
            self.assertEqual(g_item.get("files", {}).get("pptx"), f"{tid}.pptx")
            self.assertEqual(g_item.get("google_slides_id"), sm["googleSlidesId"])
            self.assertEqual(g_item.get("google_slides_url"), sm["googleSlidesEditUrl"])


if __name__ == "__main__":
    unittest.main()


