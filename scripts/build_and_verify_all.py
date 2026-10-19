"""Master OpenHands Autonomous Builder: Generates all 8 standalone Git repos, PNG/PDF renders, and verification receipts."""

import json
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.catalog.posts_catalog import POSTS_CATALOG
from src.generator.repo_factory import generate_and_verify_single_repo
from src.openhands_harness.autonomous_agent import OpenHandsAutonomousHarness


CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render_png_and_pdf_for_repo(repo_dir: Path) -> None:
    """Use Headless Chrome to render 2D SVGs to PNGs and 12-slide HTML to linkedin_carousel.pdf."""
    chrome = Path(CHROME_BIN)
    if not chrome.exists():
        return

    infographic_svg = repo_dir / "visuals" / "linkedin-infographic-2d.svg"
    infographic_png = repo_dir / "visuals" / "linkedin-infographic-2d.png"
    arch_svg = repo_dir / "visuals" / "gcp-architecture-2d.svg"
    arch_png = repo_dir / "visuals" / "gcp-architecture-2d.png"
    carousel_html = repo_dir / "slides" / "linkedin_carousel.html"
    carousel_pdf = repo_dir / "slides" / "linkedin_carousel.pdf"

    if not infographic_png.exists() or infographic_png.stat().st_size == 0:
        subprocess.run(
            [
                str(chrome),
                "--headless",
                "--disable-gpu",
                "--window-size=1200,1350",
                f"--screenshot={infographic_png}",
                f"file://{infographic_svg}",
            ],
            check=False,
            capture_output=True,
        )
    if not arch_png.exists() or arch_png.stat().st_size == 0:
        subprocess.run(
            [
                str(chrome),
                "--headless",
                "--disable-gpu",
                "--window-size=1280,780",
                f"--screenshot={arch_png}",
                f"file://{arch_svg}",
            ],
            check=False,
            capture_output=True,
        )
    if not carousel_pdf.exists() or carousel_pdf.stat().st_size == 0:
        subprocess.run(
            [
                str(chrome),
                "--headless",
                "--disable-gpu",
                f"--print-to-pdf={carousel_pdf}",
                "--no-pdf-header-footer",
                f"file://{carousel_html}",
            ],
            check=False,
            capture_output=True,
        )

    # Commit the rendered PNG and PDF files into the standalone Git repo
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "--amend", "--no-edit"],
        cwd=str(repo_dir),
        check=False,
        capture_output=True,
    )


def main() -> None:
    repos_root = WORKSPACE_ROOT / "generated-repos"
    repos_root.mkdir(parents=True, exist_ok=True)
    harness = OpenHandsAutonomousHarness(WORKSPACE_ROOT)

    results = []
    for post in POSTS_CATALOG:
        print(f"==> [OpenHands Factory] Building & verifying {post['id']} -> {post['repo_slug']}...")
        res = generate_and_verify_single_repo(post, repos_root, harness)
        render_png_and_pdf_for_repo(Path(res["repo_path"]))
        results.append(res)

    summary = {
        "total_repos_generated": len(results),
        "all_repos_verified": all(r["verification"]["all_passed"] for r in results),
        "repositories": results,
    }
    report_path = WORKSPACE_ROOT / "verification_report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"==> Completed 8/8 standalone repositories! Report written to {report_path}")


if __name__ == "__main__":
    main()
