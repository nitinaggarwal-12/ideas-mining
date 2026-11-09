"""Unit, Compliance & Security Verification Suite for Daily Top-5 Editorial & 13-Channel Auto-Publisher."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from src.harvester.daily_top5_editorial_engine import (
    PRESENTATION_MODE_CONTRACTS,
    DailyTop5EditorialEngine,
)
from src.publisher.multi_platform_publisher import (
    PLATFORM_SPECS,
    MultiPlatformOutboxManager,
    compile_platform_package,
    generate_daily_briefing_rss_xml,
)


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class TestDailyTop5EditorialAndMultiPlatformPublisher(unittest.TestCase):
    def test_daily_top5_deduplication_clusters_and_certified_templates(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            temp_ledger = td_path / "daily_idea_history_ledger.json"
            temp_briefing = td_path / "daily_top5_editorial_briefing.json"
            with (
                patch("src.harvester.daily_top5_editorial_engine.HISTORY_LEDGER_JSON", temp_ledger),
                patch("src.harvester.daily_top5_editorial_engine.DAILY_TOP5_BRIEFING_JSON", temp_briefing),
            ):
                engine = DailyTop5EditorialEngine()
                day1 = engine.generate_daily_top5_briefing(edition_date="2026-11-04", use_live_network=False)
                self.assertEqual(day1["ideas_count"], 5)
                self.assertEqual(len(day1["ideas"]), 5)

                day1_fps = {i["fingerprint"] for i in day1["ideas"]}
                self.assertEqual(len(day1_fps), 5)

                # Verify 5 distinct engineering clusters on Day 1
                day1_clusters = {i["cluster_id"] for i in day1["ideas"]}
                self.assertGreaterEqual(len(day1_clusters), 4)

                # Verify 5 orthogonal certified templates per idea with ZERO legacy T02..T52
                legacy_ids = {f"T{n:02d}" for n in range(2, 53)}
                for idea in day1["ideas"]:
                    tpls = idea["matching_templates"]
                    self.assertEqual(len(tpls), 5)
                    tids = [t["template_id"] for t in tpls]
                    self.assertEqual(len(set(tids)), 5)
                    for t in tpls:
                        self.assertNotIn(t["template_id"], legacy_ids)
                        self.assertIn(t["recommended_mode"], PRESENTATION_MODE_CONTRACTS)

                # Day 2 must select 5 NEW unseen fingerprints from the 30-day rolling ledger
                day2 = engine.generate_daily_top5_briefing(edition_date="2026-11-05", use_live_network=False)
                day2_fps = {i["fingerprint"] for i in day2["ideas"]}
                self.assertEqual(len(day2_fps), 5)
                self.assertEqual(len(day1_fps.intersection(day2_fps)), 0)

    def test_all_8_presentation_modes_expose_3part_length_contracts(self) -> None:
        expected_modes = {
            "Carousel",
            "Image",
            "Short_Video",
            "Video",
            "Slidedeck",
            "Slide",
            "Doc",
            "Text",
        }
        self.assertEqual(set(PRESENTATION_MODE_CONTRACTS.keys()), expected_modes)
        for mode_id, spec in PRESENTATION_MODE_CONTRACTS.items():
            budget = spec["length_budget"]
            self.assertTrue(budget.get("hook_above_fold"), mode_id)
            self.assertTrue(budget.get("per_unit_density"), mode_id)
            self.assertTrue(budget.get("total_deliverable_size"), mode_id)
            self.assertTrue(budget.get("estimated_consumption_time"), mode_id)

    def test_all_13_platforms_pass_preflight_compliance_across_modes(self) -> None:
        self.assertEqual(len(PLATFORM_SPECS), 13)
        sample_idea = {
            "id": "MINT-01",
            "title": "Zero-Bloat MCP Gateway: Dynamic Tool Search + OAuth 2.1 OBO",
            "summary": "Replaces 55,000-token static MCP dumps with Top-4 hybrid discovery and 5-minute OBO tokens.",
            "metrics_hint": "-97.5% schema tokens ($0.42 -> $0.014/turn) • 94.2% tool accuracy • 0 OBO leaks",
            "primary_url": "https://github.com/nitinaggarwal-12/ideas-mining",
            "source_channel": "Google Cloud ADK • Verified Exemplar",
        }
        sample_tpl = {"template_id": "T85", "name": "Zero-Bloat MCP Gateway Spine"}

        for mode_id in PRESENTATION_MODE_CONTRACTS:
            for pid in PLATFORM_SPECS:
                pkg = compile_platform_package(sample_idea, sample_tpl, mode_id, pid)
                checks = pkg["compliance_checks"]
                self.assertTrue(
                    checks["all_passed"],
                    f"Compliance failed for ({mode_id}, {pid}): {checks}",
                )
                if pid in ("instagram", "tiktok"):
                    self.assertNotEqual(pkg["media"]["container_format"], "PDF")
                    self.assertIsNone(re.search(r"https?://\S+", pkg["body"]))
                if pid == "telegram" and pkg["media"]["container_format"] != "TEXT":
                    self.assertLessEqual(len(pkg["body"]), 1024)
                if pid == "bluesky":
                    self.assertLessEqual(len(pkg["body"]), 300)
                if pid == "x":
                    self.assertLessEqual(len(pkg["body"]), 280)
                    self.assertIn("https://", pkg["follow_up_comment"])
                if pid == "linkedin":
                    self.assertIsNone(re.search(r"https?://\S+", pkg["body"]))
                    self.assertIn("https://", pkg["follow_up_comment"])

    def test_outbox_staging_dry_run_approval_and_rss_xml(self) -> None:
        sample_idea = {
            "id": "MINT-01",
            "title": "Zero-Bloat MCP Gateway: Dynamic Tool Search + OAuth 2.1 OBO",
            "summary": "Replaces 55,000-token static MCP dumps with Top-4 hybrid discovery and 5-minute OBO tokens.",
            "metrics_hint": "-97.5% schema tokens • 94.2% tool accuracy",
            "primary_url": "https://github.com/nitinaggarwal-12/ideas-mining",
            "cluster_label": "MCP, A2A & Zero-Trust Identity",
            "default_recommended_mode": "Carousel",
            "matching_templates": [{"template_id": "T85", "name": "Zero-Bloat MCP Gateway Spine"}],
        }
        sample_tpl = {"template_id": "T85", "name": "Zero-Bloat MCP Gateway Spine"}

        with tempfile.TemporaryDirectory() as td:
            temp_outbox = Path(td) / "publishing_outbox_ledger.json"
            clean_env = {
                k: v
                for k, v in os.environ.items()
                if not k.startswith(("LINKEDIN_", "TELEGRAM_", "DEVTO_", "WHATSAPP_", "X_USER_"))
            }
            with (
                patch("src.publisher.multi_platform_publisher.OUTBOX_LEDGER_JSON", temp_outbox),
                patch.dict(os.environ, clean_env, clear=True),
            ):
                mgr = MultiPlatformOutboxManager()
                staged = mgr.stage_packages(
                    idea=sample_idea,
                    template=sample_tpl,
                    mode="Carousel",
                    platforms=["linkedin", "instagram", "whatsapp", "substack"],
                )
                self.assertEqual(len(staged["staged"]), 4)
                self.assertEqual(staged["ledger"]["pending_count"], 4)

                approved = mgr.approve_and_publish()
                statuses = {item["platform_id"]: item["status"] for item in approved["processed"]}
                self.assertEqual(statuses["linkedin"], "DRY_RUN_VALIDATED")
                self.assertEqual(statuses["instagram"], "DRY_RUN_VALIDATED")
                self.assertEqual(statuses["whatsapp"], "SHARE_PACKET_READY")
                self.assertEqual(statuses["substack"], "SHARE_PACKET_READY")

        rss_xml = generate_daily_briefing_rss_xml({"ideas": [sample_idea]})
        root = ET.fromstring(rss_xml)
        self.assertEqual(root.tag, "rss")
        items = root.findall("./channel/item")
        self.assertEqual(len(items), 1)

    def test_prebaked_multi_platform_media_and_web_security_invariants(self) -> None:
        mint_mp = WORKSPACE_ROOT / "assets" / "multi-platform" / "MINT-01"
        self.assertTrue((mint_mp / "carousel_4x5.pdf").exists())
        self.assertTrue((mint_mp / "vertical_short_9x16.mp4").exists())
        self.assertEqual(len(list((mint_mp / "carousel_4x5").glob("slide_*.jpg"))), 8)
        self.assertEqual(len(list((mint_mp / "carousel_9x16").glob("slide_*.jpg"))), 8)

        short_manifest = json.loads((mint_mp / "short_video_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(short_manifest["width"], 1080)
        self.assertEqual(short_manifest["height"], 1920)
        self.assertTrue(short_manifest["gates_passed"])

        # Security & Cloudtop reachability check: STUDIO_TEST_MODE binds 127.0.0.1, Cloudtop/Cloud Run binds 0.0.0.0,
        # enforces is_relative_to, nosniff, SIGTERM graceful shutdown, and trustworthy-origin COOP gating
        server_src = (WORKSPACE_ROOT / "server.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.get("HOST", "127.0.0.1")', server_src)
        self.assertIn('os.environ.get("HOST", "0.0.0.0")', server_src)
        self.assertIn("signal.SIGTERM", server_src)
        self.assertIn("allow_reuse_address = True", server_src)
        self.assertIn("is_relative_to(", server_src)
        self.assertIn("X-Content-Type-Options", server_src)

        # Live socket verification on loopback (127.0.0.1) per mandatory-secure-web-skills testing rule
        import http.client
        import threading
        from server import create_studio_server, resolve_bind_host

        with patch.dict(os.environ, {"STUDIO_TEST_MODE": "1"}, clear=False):
            self.assertEqual(resolve_bind_host(), "127.0.0.1")
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(resolve_bind_host(), "0.0.0.0")

        srv = create_studio_server("127.0.0.1", 0)
        port = srv.server_address[1]
        t = threading.Thread(target=srv.serve_forever, daemon=True)
        t.start()
        try:
            # 1. Plain HTTP non-localhost Host (e.g. http://nitinagga.c.googlers.com:8765) -> 200 OK, NO COOP header
            conn1 = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            conn1.request("GET", "/?view=view-miner", headers={"Host": "nitinagga.c.googlers.com:8765"})
            resp1 = conn1.getresponse()
            resp1.read()
            self.assertEqual(resp1.status, 200)
            self.assertIsNone(resp1.getheader("Cross-Origin-Opener-Policy"))
            self.assertEqual(resp1.getheader("X-Content-Type-Options"), "nosniff")
            conn1.close()

            # 2. HTTPS forwarded origin or localhost -> 200 OK, emits COOP header
            conn2 = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            conn2.request(
                "GET",
                "/?view=view-miner",
                headers={"Host": "nitinagga.c.googlers.com:8765", "X-Forwarded-Proto": "https"},
            )
            resp2 = conn2.getresponse()
            resp2.read()
            self.assertEqual(resp2.status, 200)
            self.assertEqual(resp2.getheader("Cross-Origin-Opener-Policy"), "same-origin-allow-popups")
            conn2.close()
        finally:
            srv.shutdown()
            srv.server_close()

        # Security & UI regression check: 100% of public/app.js uses pure DOM construction (zero innerHTML),
        # zero Web Storage, and Slidedeck mode always provides high-res preview_image_url + slide_urls
        app_js = (WORKSPACE_ROOT / "public" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", app_js)
        self.assertNotIn("localStorage", app_js)
        self.assertNotIn("sessionStorage", app_js)

        deck_pkg = compile_platform_package(
            {"id": "MINT-01", "title": "Deck Check", "summary": "S", "metrics_hint": "M"},
            {"template_id": "T61", "name": "Executive Trade-Off Matrix"},
            "Slidedeck",
            "linkedin",
        )
        self.assertTrue(deck_pkg["media"]["preview_image_url"].endswith(".png"))
        self.assertGreaterEqual(len(deck_pkg["media"]["slide_urls"]), 5)

    def test_autonomous_zero_link_omnichannel_miner(self) -> None:
        from src.harvester.autonomous_omnichannel_miner import run_autonomous_zero_link_discovery

        payload = run_autonomous_zero_link_discovery(use_live_network=False)
        self.assertEqual(payload["status"], "READY")
        self.assertTrue(payload["zero_manual_links_required"])
        self.assertGreaterEqual(payload["total_discovered_signals"], 10)
        self.assertEqual(len(payload["format_duration_matrix"]), 5)
        self.assertEqual(len(payload["distribution_channels_and_groups"]), 5)
        self.assertGreaterEqual(len(payload["creator_syndicate_feeds"]), 8)

        first_sig = payload["discovered_signals"][0]
        self.assertIn("prescription", first_sig)
        pres = first_sig["prescription"]
        self.assertIn("recommended_primary_format", pres)
        self.assertIn("optimal_duration_and_fps", pres)
        self.assertIn("target_groups_and_communities", pres)
        self.assertGreaterEqual(len(pres["target_groups_and_communities"]), 3)

    def test_raster_to_ir_deconstructor_and_server_l6_policy_sandbox(self) -> None:
        from src.visuals.raster_to_dynamic_ir_deconstructor import (
            deconstruct_raster_to_dynamic_continuum,
            evaluate_l6_policy_sandbox_server,
        )

        # 1. Deconstruct audited raster post into 4 spatial bounding boxes + direct raster pixel overlay SVG + vector IR
        dec = deconstruct_raster_to_dynamic_continuum(source_id_or_path="LI-01", compile_gif=False)
        self.assertEqual(dec["status"], "DECONSTRUCTED")
        seg = dec["raster_segmentation"]
        self.assertEqual(len(seg["zones"]), 4)
        self.assertGreaterEqual(seg["width"], 400)
        self.assertTrue(dec["direct_raster_overlay_svg_url"].endswith(".svg"))
        self.assertEqual(dec["vector_ir_bundle"]["status"], "ok")

        # 2. Server-side L6 policy gate evaluation: DENY on parameter swap, ALLOW on valid match + live ADK engine output
        deny_res = evaluate_l6_policy_sandbox_server(
            {"requested_artifact": "Artifact B", "requested_environment": "production", "reset_nonce": True}
        )
        self.assertEqual(deny_res["verdict"], "DENY")
        self.assertFalse(deny_res["parallel_rule_results"]["rule_1_artifact_match"]["passed"])
        self.assertIn("engineered_harness", deny_res["adk_repository_runtime"]["live_engine_output"])

        allow_res = evaluate_l6_policy_sandbox_server(
            {
                "requested_artifact": "Artifact A",
                "requested_environment": "staging",
                "token_age_sec": 12,
                "nonce_id": "NONCE-UNITTEST-001",
                "reset_nonce": True,
                "consume_nonce_on_allow": True,
            }
        )
        self.assertEqual(allow_res["verdict"], "ALLOW")
        self.assertEqual(len(allow_res["decision_receipt_hmac_sha256"]), 64)

        # 3. Replay of consumed 1-shot nonce must fail closed on Rule 4
        replay_res = evaluate_l6_policy_sandbox_server(
            {
                "requested_artifact": "Artifact A",
                "requested_environment": "staging",
                "token_age_sec": 14,
                "nonce_id": "NONCE-UNITTEST-001",
            }
        )
        self.assertEqual(replay_res["verdict"], "DENY")
        self.assertFalse(replay_res["parallel_rule_results"]["rule_4_one_shot_unused"]["passed"])

    def test_10_november_2026_nitin_aggarwal_attribution_and_per_topic_video_routing(self) -> None:
        gallery_dir = WORKSPACE_ROOT / "assets" / "template-gallery"
        for p in gallery_dir.glob("*.drawio"):
            txt = p.read_text(encoding="utf-8")
            self.assertNotIn("SEPTEMBER 2026", txt, f"Stale month in {p.name}")
            self.assertNotIn("SEP 2026", txt, f"Stale month in {p.name}")
            self.assertIn("NITIN AGGARWAL", txt.upper(), f"Missing author attribution in {p.name}")
            self.assertIn("NOVEMBER 2026", txt.upper(), f"Missing November 2026 date in {p.name}")

        briefing = json.loads(
            (WORKSPACE_ROOT / "data" / "daily_top5_editorial_briefing.json").read_text(encoding="utf-8")
        )
        for idea in briefing["ideas"]:
            iid = idea["id"]
            tpl = idea["matching_templates"][0]
            vid_pkg = compile_platform_package(
                idea,
                template=tpl,
                mode="Video",
                platform_id="linkedin",
            )
            self.assertEqual(
                vid_pkg["media"]["primary_asset_url"],
                f"/assets/multi-platform/{iid}/walkthrough_16x9.mp4",
            )
            self.assertNotIn("MINT-01_walkthrough.mp4", vid_pkg["media"]["primary_asset_url"])
            self.assertTrue((WORKSPACE_ROOT / "assets" / "multi-platform" / iid / "walkthrough_16x9.mp4").exists())
            self.assertTrue((WORKSPACE_ROOT / "assets" / "multi-platform" / iid / "vertical_short_9x16.mp4").exists())

    def test_11_all_139_templates_and_flow_presets_drawio_pptx_and_google_slides_ready(self) -> None:
        import xml.etree.ElementTree as ET
        import zipfile
        from src.visuals.step_by_step_flow_animator import render_step_flow_bundle

        gallery_dir = WORKSPACE_ROOT / "assets" / "template-gallery"
        manifest = json.loads((gallery_dir / "gallery_manifest.json").read_text(encoding="utf-8"))
        templates = manifest.get("templates", [])
        self.assertEqual(len(templates), 128)

        all_checked_ids = []
        for t in templates:
            tid = t["id"]
            all_checked_ids.append(tid)
            self.assertTrue(
                str(t.get("google_slides_url") or "").startswith("https://docs.google.com/presentation/d/"),
                f"Missing google_slides_url for {tid}",
            )
            drawio_path = gallery_dir / t["files"]["drawio"]
            pptx_path = gallery_dir / t["files"]["pptx"]
            self.assertTrue(drawio_path.exists(), f"Missing .drawio for {tid}")
            self.assertTrue(pptx_path.exists(), f"Missing .pptx for {tid}")
            root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))
            self.assertEqual(root.tag, "mxfile", f"Invalid .drawio XML root for {tid}")
            with zipfile.ZipFile(pptx_path, "r") as zf:
                slide_xml = zf.read("ppt/slides/slide1.xml").decode("utf-8", errors="ignore")
                self.assertNotIn("SEPTEMBER 2026", slide_xml, f"Stale month in {pptx_path.name}")
                self.assertIn("NOVEMBER 2026", slide_xml.upper(), f"Missing November 2026 in {pptx_path.name}")
                self.assertIn("NITIN AGGARWAL", slide_xml.upper(), f"Missing author in {pptx_path.name}")

            for tp in t.get("topic_posts", []):
                v_id = tp["id"]
                all_checked_ids.append(v_id)
                self.assertTrue(
                    str(tp.get("google_slides_url") or "").startswith("https://docs.google.com/presentation/d/"),
                    f"Missing google_slides_url for {v_id}",
                )
                self.assertTrue((gallery_dir / tp["files"]["drawio"]).exists())
                self.assertTrue((gallery_dir / tp["files"]["pptx"]).exists())

        self.assertEqual(len(all_checked_ids), 151)

        for preset_id in ("FLOW-01", "FLOW-02", "FLOW-03", "FLOW-04"):
            bundle = render_step_flow_bundle(preset_id=preset_id, theme="light", compile_gif=False)
            self.assertTrue(str(bundle.get("drawio_url") or "").endswith(".drawio"))
            self.assertTrue(str(bundle.get("pptx_url") or "").endswith(".pptx"))
            self.assertTrue(
                str(bundle.get("google_slides_url") or "").startswith("https://docs.google.com/presentation/d/")
            )
            drawio_file = WORKSPACE_ROOT / bundle["drawio_url"].lstrip("/")
            self.assertTrue(drawio_file.exists())
            self.assertEqual(ET.fromstring(drawio_file.read_text(encoding="utf-8")).tag, "mxfile")



    def test_12_autonomous_self_critic_and_auto_healing_harness(self) -> None:
        from src.openhands_harness.self_critic_harness import (
            critique_and_heal_generated_blueprint,
            get_self_critic_harness,
        )

        harness = get_self_critic_harness()
        report = harness.run_full_self_critic_cycle(
            auto_heal=True,
            refresh_discovery=False,
            trigger_source="unit_test_verification",
        )
        self.assertEqual(report["status"], "ALL_GATES_VERIFIED")
        self.assertEqual(report["gates_passed"], 8)
        self.assertEqual(report["gates_total"], 8)
        self.assertTrue(report["all_gates_passed"])
        self.assertGreaterEqual(report["overall_score"], 99.0)
        self.assertEqual(len(report["six_closed_loops"]), 6)
        self.assertEqual(len(report["persona_critics"]), 4)
        self.assertEqual(
            len(report["discovery_and_gap_radar"]["auto_synthesized_gap_exemplars"]),
            6,
        )

        # Verify pre-render & post-render blueprint self-critic auto-heals overly long copy
        long_topic = " ".join(["Enterprise Agentic FinOps Governance and Recursive Self-Critic Loop"] * 3)
        bundle = critique_and_heal_generated_blueprint(
            {
                "topic": long_topic,
                "persona_id": "ciso_governance",
                "org_id": "regulated_enterprise",
            }
        )
        rc = bundle["self_critic_receipt"]
        self.assertEqual(rc["status"], "CERTIFIED_BY_SELF_CRITIC")
        self.assertGreaterEqual(rc["overall_score"], 98.0)
        self.assertGreaterEqual(len(rc["auto_healed_adjustments"]), 1)
        self.assertTrue(rc["geometry_check"]["zero_collision"])
        self.assertEqual(len(rc["persona_critiques"]), 4)

    def test_13_raster_deconstructor_post_code_and_customer_success_radar(self) -> None:
        from scripts.verify_all_repos import verify_all
        from src.harvester.autonomous_omnichannel_miner import discover_customer_success_agentic_inventions
        from src.visuals.raster_to_dynamic_ir_deconstructor import deconstruct_raster_to_dynamic_continuum

        res_li16 = deconstruct_raster_to_dynamic_continuum(source_id_or_path="LI-16", compile_gif=False)
        self.assertIn("7523000944440008704", res_li16["source_image_name"])
        self.assertIn("5 layers of agent memory", res_li16["post_title"])

        res_li49 = deconstruct_raster_to_dynamic_continuum(source_id_or_path="LI-49", compile_gif=False)
        self.assertIn("7524855506109267968", res_li49["source_image_name"])
        self.assertIn("One Architecture Diagram", res_li49["post_title"])

        cs_radar = discover_customer_success_agentic_inventions(force_live=False)
        self.assertEqual(cs_radar["status"], "READY")
        self.assertGreaterEqual(len(cs_radar["inventions"]), 6)
        for inv in cs_radar["inventions"]:
            self.assertTrue(inv.get("invention_id"))
            self.assertTrue(inv.get("customer_pain_point"))
            self.assertTrue(inv.get("customer_success_prescription"))
            self.assertTrue(inv.get("quantified_value_kpis"))
            self.assertTrue(inv.get("recommended_template_id"))
            self.assertTrue(inv.get("reference_repo_slug"))

        from src.harvester.autonomous_omnichannel_miner import (
            fetch_rss_less_frontier_lab_sitemaps_live,
            generate_frontier_labs_syndicate_rss_xml,
        )

        sitemap_items = fetch_rss_less_frontier_lab_sitemaps_live(allow_network=False)
        self.assertGreaterEqual(len(sitemap_items), 3)
        self.assertTrue(any("anthropic.com/engineering" in it["primary_url"] for it in sitemap_items))

        frontier_rss_xml = generate_frontier_labs_syndicate_rss_xml()
        self.assertEqual(ET.fromstring(frontier_rss_xml).tag, "rss")
        self.assertIn("Anthropic", frontier_rss_xml)

        repo_gate = verify_all()
        self.assertTrue(repo_gate["gate_passed"], f"verify_all_repos failures: {repo_gate['failures']}")
        self.assertEqual(len(repo_gate["failures"]), 0)



        from src.catalog.post_distribution_directory import get_or_update_linkedin_group_membership_radar
        radar0 = get_or_update_linkedin_group_membership_radar()
        self.assertEqual(radar0["total_catalog_groups"], 25)
        self.assertTrue(len(radar0["groups"]) == 25)

        # Test paste-to-diff auto-detection for Google Cloud Platform group (3050257)
        radar_diff = get_or_update_linkedin_group_membership_radar(
            pasted_my_groups_text="My Groups: Google Cloud Platform (GCP) Architects, Developers & Vertex AI Builders https://www.linkedin.com/groups/3050257/"
        )
        self.assertIn("GRP-16-GCP-ARCHITECTS", radar_diff["auto_matched_from_paste"])
        # Reset back to NOT_JOINED_YET so ledger stays clean
        get_or_update_linkedin_group_membership_radar(toggle_group_id="GRP-16-GCP-ARCHITECTS", new_status="NOT_JOINED_YET")

if __name__ == "__main__":
    unittest.main()
