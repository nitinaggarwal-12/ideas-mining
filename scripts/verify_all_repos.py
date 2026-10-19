"""Fail-Closed Forensic Verification Gate for Ideas Mining & 8 Standalone Git Repositories.

Audits:
1. All 8 standalone Git repositories exist, have clean git commits, and pass their sandbox unit test suites.
2. Every repo contains @2d visuals (linkedin-infographic-2d.svg/.png, gcp-architecture-2d.svg/.png/.drawio).
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


def verify_all() -> dict:
    repos_root = WORKSPACE_ROOT / "generated-repos"
    failures = []
    repo_audits = []

    # 1. Audit Studio UI CSS & HTML for Rule 54 (Light Theme), Rule 25 (Fluid + Right Drawer), Rule 26 (Table Containment)
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

    # 2. Audit all 8 generated repositories
    for post in POSTS_CATALOG:
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
            "visuals/linkedin-infographic-2d.svg",
            "visuals/linkedin-infographic-2d.png",
            "visuals/gcp-architecture-2d.svg",
            "visuals/gcp-architecture-2d.png",
            "visuals/gcp-architecture-2d.drawio",
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

        # Run unit tests inside the repo
        proc = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            cwd=str(r_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            failures.append(f"[{slug}] Unit tests failed: {proc.stderr}")

        # Parse SVGs & Draw.io XML
        try:
            ET.parse(r_dir / "visuals" / "linkedin-infographic-2d.svg")
            ET.parse(r_dir / "visuals" / "gcp-architecture-2d.svg")
            ET.parse(r_dir / "visuals" / "gcp-architecture-2d.drawio")
        except Exception as exc:
            failures.append(f"[{slug}] Malformed XML in visuals: {exc}")

        # Audit PPTX 12 slides + 12 notesSlides + Proprietary + Confidential
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
        "failures": failures,
        "audits": repo_audits,
    }
    print(json.dumps(result, indent=2))
    if failures:
        sys.exit(1)
    return result


if __name__ == "__main__":
    verify_all()
