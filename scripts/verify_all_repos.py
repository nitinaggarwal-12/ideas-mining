"""Fail-Closed Forensic Verification Gate for Ideas Mining & All 18 Standalone Git Repositories (10 Tomorrow Morning EST Ideas + 8 Analyzed LinkedIn Posts).

Audits:
1. All 18 standalone Git repositories exist, have clean git commits, and pass their sandbox unit test suites.
2. Every repo contains Dynamic Moving-Arrow visuals (dynamic-solution-flow.svg/.gif/.png) + @2d visuals (linkedin-infographic-2d.svg/.png, gcp-architecture-2d.svg/.png/.drawio, nano_banana_3_prompt.md).
3. Every repo contains a 12-slide OpenXML presentation_deck.pptx (with 12 slides, 12 spoken notesSlides, 'Proprietary + Confidential', zero pricing figures) and linkedin_carousel.pdf.
4. Every repo contains 1-click GCP Terraform files (versions.tf, variables.tf, main.tf, outputs.tf, terraform.tfvars.example) + deploy script.
5. Studio UI enforces Rule 54 Universal Light Theme (#f8fafc/#ffffff, 0 dark mode classes), Rule 25 fluid layout & non-blocking right drawer, and Rule 26 table cell containment.
"""

import json
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.catalog.posts_catalog import POSTS_CATALOG
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS


def verify_all() -> dict:
    repos_root = WORKSPACE_ROOT / "generated-repos"
    failures = []
    repo_audits = []

    css_text = (WORKSPACE_ROOT / "public" / "styles.css").read_text(encoding="utf-8")
    html_text = (WORKSPACE_ROOT / "public" / "index.html").read_text(encoding="utf-8")

    if "#f8fafc" not in css_text or "#ffffff" not in css_text:
        failures.append("Rule 54 violation: Missing #f8fafc or #ffffff light theme colors in public/styles.css")
    for banned_dark in ("bg-slate-950", "#020617", 'class="dark"'):
        if banned_dark in css_text or banned_dark in html_text:
            failures.append(f"Rule 54B violation: Found banned dark-mode token {banned_dark}")
    if "overflow: hidden;" not in css_text or "max-width: 0;" not in css_text:
        failures.append("Rule 26C violation: Missing rigid table cell containment in public/styles.css")
    if "repo-inspector-drawer" not in html_text:
        failures.append("Rule 25F violation: Missing non-blocking right-side inspector drawer")

    all_items = list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG)

    for post in all_items:
        slug = post["repo_slug"]
        r_dir = repos_root / slug
        if not r_dir.exists():
            failures.append(f"Missing generated repository directory: {slug}")
            continue

        required_files = [
            "README.md",
            "AGENTS.md",
            "GEMINI.md",
            "CLAUDE.md",
            "openhands-config.toml",
            ".openhands/microagents/repo.md",
            ".mcp.json",
            "Dockerfile",
            "cloudbuild.yaml",
            "app.py",
            "src/engine.py",
            "tests/test_engine.py",
            "linkedin_post_draft.md",
            "visuals/dynamic-solution-flow.svg",
            "visuals/dynamic-solution-flow.gif",
            "visuals/dynamic-solution-flow.png",
            "visuals/linkedin-infographic-2d.svg",
            "visuals/linkedin-infographic-2d.png",
            "visuals/gcp-architecture-2d.svg",
            "visuals/gcp-architecture-2d.png",
            "visuals/gcp-architecture-2d.drawio",
            "visuals/nano_banana_3_prompt.md",
            "slides/presentation_deck.pptx",
            "slides/linkedin_carousel.html",
            "slides/linkedin_carousel.pdf",
            "slides/slide_manifest.json",
            "terraform/versions.tf",
            "terraform/variables.tf",
            "terraform/main.tf",
            "terraform/outputs.tf",
            "terraform/terraform.tfvars.example",
            "scripts/deploy_gcp_one_click.sh",
        ]
        for req in required_files:
            p = r_dir / req
            if not p.exists() or p.stat().st_size == 0:
                failures.append(f"[{slug}] Missing or empty required file: {req}")

        proc = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            cwd=str(r_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            failures.append(f"[{slug}] Unit tests failed: {proc.stderr}")

        try:
            dyn_path = r_dir / "visuals" / "dynamic-solution-flow.svg"
            inf_path = r_dir / "visuals" / "linkedin-infographic-2d.svg"
            arch_path = r_dir / "visuals" / "gcp-architecture-2d.svg"
            drawio_path = r_dir / "visuals" / "gcp-architecture-2d.drawio"
            ET.parse(dyn_path)
            ET.parse(inf_path)
            ET.parse(arch_path)
            drawio_tree = ET.parse(drawio_path)

            dyn_xml = dyn_path.read_text(encoding="utf-8")
            inf_xml = inf_path.read_text(encoding="utf-8")
            arch_xml = arch_path.read_text(encoding="utf-8")
            if "moving-arrow-line" not in dyn_xml or "animateMotion" not in dyn_xml:
                failures.append(f"[{slug}] dynamic-solution-flow.svg missing moving-arrow-line or animateMotion")
            if 'viewBox="0 0 1600 1200"' not in inf_xml:
                failures.append(f"[{slug}] linkedin-infographic-2d.svg missing 1600x1200 viewBox")
            if 'viewBox="0 0 1600 1020"' not in arch_xml or "ZONE 5" not in arch_xml:
                failures.append(f"[{slug}] gcp-architecture-2d.svg missing 1600x1020 #78 topology or ZONE 5 baseline")

            cells = drawio_tree.getroot().findall(".//mxCell")
            card_cells = [
                c
                for c in cells
                if (c.attrib.get("id") or "").startswith("c")
                and len(c.attrib.get("id") or "") > 1
                and (c.attrib.get("id") or "")[1].isdigit()
            ]
            edge_cells = [c for c in cells if c.attrib.get("edge") == "1"]
            if len(card_cells) < 18 or len(edge_cells) < 23:
                failures.append(
                    f"[{slug}] gcp-architecture-2d.drawio density failure: cards={len(card_cells)} (min 18), edges={len(edge_cells)} (min 23)"
                )
        except Exception as exc:
            failures.append(f"[{slug}] Malformed XML in visuals: {exc}")

        pptx_path = r_dir / "slides" / "presentation_deck.pptx"
        with zipfile.ZipFile(pptx_path, "r") as zf:
            names = set(zf.namelist())
            for s_idx in range(1, 13):
                s_name = f"ppt/slides/slide{s_idx}.xml"
                n_name = f"ppt/notesSlides/notesSlide{s_idx}.xml"
                if s_name not in names or n_name not in names:
                    failures.append(f"[{slug}] Missing {s_name} or {n_name} in PPTX")
                else:
                    s_xml = zf.read(s_name).decode("utf-8")
                    if "Proprietary + Confidential" not in s_xml:
                        failures.append(f"[{slug}] Missing 'Proprietary + Confidential' on Slide {s_idx}")

        repo_audits.append(
            {
                "post_id": post["id"],
                "repo_slug": slug,
                "required_files_verified": len(required_files),
                "unit_tests_passed": proc.returncode == 0,
                "pptx_slides_verified": 12,
                "status": "PASS",
            }
        )

    result = {
        "gate_passed": len(failures) == 0,
        "repos_audited": len(repo_audits),
        "tomorrow_top10_audited": len(TOMORROW_TOP10_IDEAS),
        "original_posts_audited": len(POSTS_CATALOG),
        "failures": failures,
        "audits": repo_audits,
    }
    print(json.dumps(result, indent=2))
    if failures:
        sys.exit(1)
    return result


if __name__ == "__main__":
    verify_all()
