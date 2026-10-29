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
    canonical_png = WORKSPACE_ROOT / "assets" / "canonical-ref" / f"canonical_{tid}.png"
    canonical_drawio = WORKSPACE_ROOT / "assets" / "canonical-ref" / "drawio" / f"{tid}.drawio"
    if canonical_png.exists():
        png_path.write_bytes(canonical_png.read_bytes())
    if canonical_drawio.exists():
        (OUT_DIR / f"{tid}.drawio").write_bytes(canonical_drawio.read_bytes())
    drawio_path = OUT_DIR / f"{tid}.drawio"
    pptx_path = OUT_DIR / f"{tid}.pptx"
    print(f"==> [Template Gallery] {tid} {TEMPLATE_META[tid]['name']}: svg={svg_path.stat().st_size}B gif={'ok' if ok else 'skipped'}")
    out_files = {
        "id": tid,
        "svg": svg_path.name,
        "gif": gif_path.name if ok else None,
        "png": png_path.name if png_path.exists() else None,
    }
    if drawio_path.exists():
        out_files["drawio"] = drawio_path.name
    if pptx_path.exists():
        out_files["pptx"] = pptx_path.name
    return out_files


def main() -> None:
    skip_existing = "--skip-existing" in sys.argv
    explicit_ids = [a for a in sys.argv[1:] if a.startswith("T") and a in TEMPLATE_META]
    ids = explicit_ids or list(TEMPLATE_META.keys())
    if skip_existing and not explicit_ids:
        ids = [t for t in ids if not (OUT_DIR / f"{t}.gif").exists()]
    rendered = {}
    if ids:
        with ThreadPoolExecutor(max_workers=5) as pool:
            rendered = {r["id"]: r for r in pool.map(build_one, ids)}
    slides_manifest_path = WORKSPACE_ROOT / "data" / "template_google_slides_manifest.json"
    slides_by_tid = {}
    if slides_manifest_path.exists():
        try:
            slides_by_tid = json.loads(slides_manifest_path.read_text(encoding="utf-8")).get("slides", {})
        except Exception:
            slides_by_tid = {}
    manifest = []
    for meta in list_templates():
        tid = meta["id"]
        files = rendered.get(tid) or {"svg": f"{tid}.svg", "gif": f"{tid}.gif", "png": f"{tid}.png"}
        if (OUT_DIR / f"{tid}.drawio").exists():
            files["drawio"] = f"{tid}.drawio"
        if (OUT_DIR / f"{tid}.pptx").exists():
            files["pptx"] = f"{tid}.pptx"
        entry = {**meta, "files": {k: v for k, v in files.items() if k != "id" and v}}
        sm = slides_by_tid.get(tid)
        if sm:
            entry["google_slides_id"] = sm.get("googleSlidesId")
            entry["google_slides_url"] = sm.get("googleSlidesEditUrl")
            entry["google_slides_preview_url"] = sm.get("googleSlidesPreviewUrl")
            entry["editable_slide_count"] = sm.get("slideCount", 4)
        manifest.append(entry)
    manifest_json = json.dumps({"template_count": len(manifest), "templates": manifest}, indent=2)
    (OUT_DIR / "gallery_manifest.json").write_text(manifest_json, encoding="utf-8")
    print(f"==> Wrote {OUT_DIR / 'gallery_manifest.json'} ({len(manifest)} templates)")


if __name__ == "__main__":
    main()

