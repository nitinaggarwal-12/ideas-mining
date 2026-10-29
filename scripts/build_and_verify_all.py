"""Master OpenHands Autonomous Builder: Generates all 18 standalone Git repos (8 Original Posts + 10 Tomorrow Morning EST Ideas), Dynamic Moving-Arrow GIFs/SVGs, Nano Banana 3 Visuals, and 12-Slide Decks."""

from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.catalog.posts_catalog import POSTS_CATALOG
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.generator.repo_factory import generate_and_verify_single_repo
from src.openhands_harness.autonomous_agent import OpenHandsAutonomousHarness
from src.visuals.dynamic_diagram_engine import generate_dynamic_solution_svg, render_animated_gif_for_idea


CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render_dynamic_asset(item: dict) -> None:
    """Render Dynamic Moving-Arrow SVG, 6-frame looping Animated GIF, and PNG for an idea/post."""
    dyn_dir = WORKSPACE_ROOT / "assets" / "dynamic-top10"
    dyn_dir.mkdir(parents=True, exist_ok=True)
    pid = item["id"]
    svg_path = dyn_dir / f"{pid}.svg"
    gif_path = dyn_dir / f"{pid}.gif"
    png_path = dyn_dir / f"{pid}.png"
    svg_path.write_text(generate_dynamic_solution_svg(item), encoding="utf-8")
    skip_existing = "--skip-existing" in sys.argv
    if not skip_existing or not gif_path.exists() or not png_path.exists() or gif_path.stat().st_size == 0:
        render_animated_gif_for_idea(item, gif_path, png_path, num_frames=6)


def render_png_and_pdf_for_repo(repo_dir: Path) -> None:
    """Use Headless Chrome to render 12-slide HTML to linkedin_carousel.pdf and always render fresh PNGs from vector SVGs."""
    chrome = Path(CHROME_BIN)
    if not chrome.exists():
        return

    infographic_svg = repo_dir / "visuals" / "linkedin-infographic-2d.svg"
    infographic_png = repo_dir / "visuals" / "linkedin-infographic-2d.png"
    arch_svg = repo_dir / "visuals" / "gcp-architecture-2d.svg"
    arch_png = repo_dir / "visuals" / "gcp-architecture-2d.png"
    carousel_html = repo_dir / "slides" / "linkedin_carousel.html"
    carousel_pdf = repo_dir / "slides" / "linkedin_carousel.pdf"

    for stale_jpg in ("nano-banana-3-infographic.jpg", "nano-banana-3-gcp-arch-78.jpg"):
        sp = repo_dir / "visuals" / stale_jpg
        if sp.exists():
            sp.unlink()

    subprocess.run(
        [
            str(chrome),
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1600,1200",
            f"--screenshot={infographic_png}",
            f"file://{infographic_svg}",
        ],
        check=False,
        capture_output=True,
    )
    subprocess.run(
        [
            str(chrome),
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1600,1020",
            f"--screenshot={arch_png}",
            f"file://{arch_svg}",
        ],
        check=False,
        capture_output=True,
    )
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

    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "--amend", "--no-edit"],
        cwd=str(repo_dir),
        check=False,
        capture_output=True,
    )


def main() -> None:
    all_items = list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG)

    print("==> [Dynamic Diagram Engine] Compiling 18 Moving-Arrow Animated GIFs & SVGs in parallel...")
    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(render_dynamic_asset, all_items))

    repos_root = WORKSPACE_ROOT / "generated-repos"
    repos_root.mkdir(parents=True, exist_ok=True)
    harness = OpenHandsAutonomousHarness(WORKSPACE_ROOT)

    results = []
    repo_dirs = []
    for item in all_items:
        print(f"==> [OpenHands Factory] Building & verifying {item['id']} -> {item['repo_slug']}...")
        res = generate_and_verify_single_repo(item, repos_root, harness)
        results.append(res)
        repo_dirs.append(Path(res["repo_path"]))

    print("==> [Headless Chrome] Rendering 18 12-slide PDF carousels in parallel...")
    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(render_png_and_pdf_for_repo, repo_dirs))

    summary = {
        "total_repos_generated": len(results),
        "tomorrow_top10_count": len(TOMORROW_TOP10_IDEAS),
        "analyzed_posts_count": len(POSTS_CATALOG),
        "all_repos_verified": all(r["verification"]["all_passed"] for r in results),
        "repositories": results,
    }
    report_path = WORKSPACE_ROOT / "verification_report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"==> Completed {len(results)}/{len(results)} standalone repositories! Report written to {report_path}")


if __name__ == "__main__":
    main()
