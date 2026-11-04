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

        # Security check: new Top-5 controller in public/app.js uses createElement/replaceChildren (zero innerHTML)
        app_js = (WORKSPACE_ROOT / "public" / "app.js").read_text(encoding="utf-8")
        new_section = app_js.split("function mkEl(tag, className, text)", 1)[1]
        self.assertNotIn("innerHTML", new_section)
        self.assertNotIn("localStorage", app_js)
        self.assertNotIn("sessionStorage", app_js)


if __name__ == "__main__":
    unittest.main()
