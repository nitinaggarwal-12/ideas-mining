"""Tests for the Production-Hardened MCP Authorization 4:5 Diagram Suite."""

import json
import subprocess
import unittest
import xml.etree.ElementTree as ET

from src.visuals.mcp_authorization_corrected_diagram import (
    CORRECTION_CHANGELOG_MD,
    FRAME_SCHEDULE,
    LINKEDIN_POST_DRAFT,
    OUT_DIR,
    render_corrected_mcp_auth_drawio,
    render_corrected_mcp_auth_svg,
)

FORBIDDEN_TYPOS = (
    "scopped",
    "be-hosted",
    "www-Authenticate",
    "well-know/",
    "IRFC",
    "resourse",
    "CORRECTED ZERO-TRUST",
    "Holds PKCE",
    "grant_type=token-exchange",
    "PKCE discovery",
)

REQUIRED_CORRECTIONS = (
    "RFC 9728",
    "RFC 8414",
    "RFC 8707",
    "RFC 9207",
    "RFC 8693",
    "WWW-Authenticate",
    "/.well-known/oauth-protected-resource",
    "scoped",
    "Pre-reg",
    "CIMD",
    "insufficient_scope",
    "HITL",
    "WIF",
    "Downstream APIs",
    "urn:...:token-exchange",
    "#B45309",
    "#047857",
    "#0F766E",
)


class CorrectedMcpAuthDiagramTests(unittest.TestCase):
    def test_svg_zero_typos_and_exact_canvas(self) -> None:
        svg = render_corrected_mcp_auth_svg(frame_idx=None)
        self.assertIn('viewBox="0 0 1080 1350"', svg)
        for typo in FORBIDDEN_TYPOS:
            self.assertNotIn(typo, svg)
        self.assertNotIn("Upstream APIs", svg)
        for req in REQUIRED_CORRECTIONS:
            self.assertIn(req, svg)

    def test_sequential_frames_cover_all_6_phases(self) -> None:
        self.assertEqual(len(FRAME_SCHEDULE), 28)
        seen_phases = {p for p, _, _, _ in FRAME_SCHEDULE if p is not None}
        self.assertEqual(seen_phases, {1, 2, 3, 4, 5, 6})
        banners = set()
        for idx in range(len(FRAME_SCHEDULE)):
            fsvg = render_corrected_mcp_auth_svg(frame_idx=idx)
            self.assertIn("PHASE ", fsvg) if idx < 26 else self.assertIn("END-TO-END", fsvg)
            if idx < 26:
                for p in range(1, 7):
                    if f"PHASE {p}/6" in fsvg:
                        banners.add(p)
        self.assertEqual(banners, {1, 2, 3, 4, 5, 6})

    def test_drawio_xml_valid_and_typo_free(self) -> None:
        xml_str = render_corrected_mcp_auth_drawio()
        root = ET.fromstring(xml_str)
        self.assertEqual(root.tag, "mxfile")
        model = root.find(".//mxGraphModel")
        self.assertIsNotNone(model)
        self.assertEqual(model.attrib.get("pageWidth"), "1080")
        self.assertEqual(model.attrib.get("pageHeight"), "1350")
        for typo in FORBIDDEN_TYPOS:
            self.assertNotIn(typo, xml_str)

    def test_post_copy_and_bundle_outputs_verified(self) -> None:
        for typo in ("scopped", "be-hosted", "www-Authenticate", "well-know/", "IRFC", "resourse"):
            self.assertNotIn(typo, LINKEDIN_POST_DRAFT)
        self.assertIn("Fixed in Production Version", CORRECTION_CHANGELOG_MD)
        for req in (
            "RFC 9728",
            "RFC 8414",
            "RFC 8707",
            "RFC 9207",
            "RFC 8693",
            "urn:ietf:params:oauth:grant-type:token-exchange",
            "gcp-mcp-zero-bloat-gateway",
        ):
            self.assertIn(req, LINKEDIN_POST_DRAFT)

        audit_json = OUT_DIR / "dom_collision_audit.json"
        gif_path = OUT_DIR / "mcp_authorization_corrected_4x5.gif"
        png_2x_path = OUT_DIR / "mcp_authorization_corrected_4x5_2x.png"
        self.assertTrue(audit_json.exists())
        self.assertTrue(gif_path.exists())
        self.assertTrue(png_2x_path.exists())

        audit = json.loads(audit_json.read_text(encoding="utf-8"))
        self.assertEqual(audit["outOfBoundsCount"], 0)
        self.assertEqual(audit["overlapCount"], 0)
        self.assertEqual(audit["pillViolationCount"], 0)
        self.assertEqual(audit["bandViolationCount"], 0)
        self.assertEqual(audit["foundTypos"], [])

        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(gif_path)],
            capture_output=True, text=True, check=True,
        )
        stream = json.loads(probe.stdout)["streams"][0]
        self.assertEqual(stream["codec_name"], "gif")
        self.assertEqual(stream["width"], 1080)
        self.assertEqual(stream["height"], 1350)
        self.assertEqual(int(stream["nb_frames"]), 28)


if __name__ == "__main__":
    unittest.main()
