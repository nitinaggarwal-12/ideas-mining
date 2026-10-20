"""Render the 20 Dynamic Visual Template Gallery (animated SVG + 6-frame looping GIF + PNG) and write gallery_manifest.json."""

from concurrent.futures import ThreadPoolExecutor
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.visuals.template_gallery import TEMPLATE_META, list_templates, render_template, render_template_gif

OUT_DIR = WORKSPACE_ROOT / "assets" / "template-gallery"


def build_one(tid: str) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = OUT_DIR / f"{tid}.svg"
    gif_path = OUT_DIR / f"{tid}.gif"
    png_path = OUT_DIR / f"{tid}.png"
    svg_path.write_text(render_template(tid), encoding="utf-8")
    ok = render_template_gif(tid, gif_path, png_path, frames=6)
    print(f"==> [Template Gallery] {tid} {TEMPLATE_META[tid]['name']}: svg={svg_path.stat().st_size}B gif={'ok' if ok else 'skipped'}")
    return {"id": tid, "svg": svg_path.name, "gif": gif_path.name if ok else None, "png": png_path.name if png_path.exists() else None}


def main() -> None:
    force = "--force" in sys.argv
    ids = list(TEMPLATE_META.keys())
    if not force:
        ids = [t for t in ids if not (OUT_DIR / f"{t}.gif").exists()] or ids
    with ThreadPoolExecutor(max_workers=5) as pool:
        rendered = {r["id"]: r for r in pool.map(build_one, ids)}
    manifest = []
    for meta in list_templates():
        tid = meta["id"]
        files = rendered.get(tid) or {"svg": f"{tid}.svg", "gif": f"{tid}.gif", "png": f"{tid}.png"}
        manifest.append({**meta, "files": {k: v for k, v in files.items() if k != "id"}})
    (OUT_DIR / "gallery_manifest.json").write_text(json.dumps({"template_count": len(manifest), "templates": manifest}, indent=2), encoding="utf-8")
    print(f"==> Wrote {OUT_DIR / 'gallery_manifest.json'} ({len(manifest)} templates)")


if __name__ == "__main__":
    main()
