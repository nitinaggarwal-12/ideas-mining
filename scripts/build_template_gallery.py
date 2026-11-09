"""Render the Consolidated 116-Template Certified Gallery (84 Best + 44 High, plus 23 T79 Topic Posts) and write gallery_manifest.json."""

from concurrent.futures import ThreadPoolExecutor
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.visuals.canonical_template_registry import (
    TEMPLATE_META,
    TOPIC_POSTS_T79,
    get_gallery_summary,
    list_templates,
    render_template,
    render_template_gif,
)

OUT_DIR = WORKSPACE_ROOT / "assets" / "template-gallery"

ALL_RENDERABLE_IDS = list(TEMPLATE_META.keys()) + [tp["id"] for tp in TOPIC_POSTS_T79]
TOPIC_NAME_MAP = {tp["id"]: tp.get("title") or tp.get("name", tp["id"]) for tp in TOPIC_POSTS_T79}


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
    name = TEMPLATE_META.get(tid, {}).get("name") or TOPIC_NAME_MAP.get(tid, tid)
    print(f"==> [Template Gallery] {tid} {name}: svg={svg_path.stat().st_size}B gif={'ok' if ok else 'skipped'}")
    out_files = {
        "id": tid,
        "svg": svg_path.name,
        "gif": gif_path.name if (ok or gif_path.exists()) else None,
        "png": png_path.name if png_path.exists() else None,
    }
    if drawio_path.exists():
        out_files["drawio"] = drawio_path.name
    if pptx_path.exists():
        out_files["pptx"] = pptx_path.name
    return out_files


def main() -> None:
    skip_existing = "--skip-existing" in sys.argv
    manifest_only = "--manifest-only" in sys.argv
    explicit_ids = [a for a in sys.argv[1:] if a.startswith("T") and a in ALL_RENDERABLE_IDS]
    ids = explicit_ids or list(ALL_RENDERABLE_IDS)
    if skip_existing and not explicit_ids:
        ids = [
            t
            for t in ids
            if not (OUT_DIR / f"{t}.gif").exists() or not (OUT_DIR / f"{t}.svg").exists()
        ]
    rendered = {}
    if ids and not manifest_only:
        with ThreadPoolExecutor(max_workers=6) as pool:
            rendered = {r["id"]: r for r in pool.map(build_one, ids)}

    slides_manifest_path = WORKSPACE_ROOT / "data" / "template_google_slides_manifest.json"
    slides_by_tid = {}
    if slides_manifest_path.exists():
        try:
            slides_by_tid = json.loads(slides_manifest_path.read_text(encoding="utf-8")).get("slides", {})
        except Exception:
            slides_by_tid = {}

    def _resolve_files(tid: str) -> dict:
        files = rendered.get(tid) or {
            "svg": f"{tid}.svg" if (OUT_DIR / f"{tid}.svg").exists() else None,
            "gif": f"{tid}.gif" if (OUT_DIR / f"{tid}.gif").exists() else None,
            "png": f"{tid}.png" if (OUT_DIR / f"{tid}.png").exists() else None,
        }
        if (OUT_DIR / f"{tid}.drawio").exists():
            files["drawio"] = f"{tid}.drawio"
        if (OUT_DIR / f"{tid}.pptx").exists():
            files["pptx"] = f"{tid}.pptx"
        return {k: v for k, v in files.items() if k != "id" and v}

    manifest = []
    for meta in list_templates():
        tid = meta["id"]
        entry = {**meta, "files": _resolve_files(tid)}
        sm = slides_by_tid.get(tid)
        if sm:
            entry["google_slides_id"] = sm.get("googleSlidesId")
            entry["google_slides_url"] = sm.get("googleSlidesEditUrl")
            entry["google_slides_preview_url"] = sm.get("googleSlidesPreviewUrl")
            entry["editable_slide_count"] = sm.get("slideCount", 4)
        if tid == "T79":
            enriched_topics = []
            for tp in entry.get("topic_posts", []):
                tp_id = tp["id"]
                tp_copy = {**tp, "files": _resolve_files(tp_id)}
                tp_sm = slides_by_tid.get(tp_id)
                if tp_sm:
                    tp_copy["google_slides_id"] = tp_sm.get("googleSlidesId")
                    tp_copy["google_slides_url"] = tp_sm.get("googleSlidesEditUrl")
                    tp_copy["google_slides_preview_url"] = tp_sm.get("googleSlidesPreviewUrl")
                    tp_copy["editable_slide_count"] = tp_sm.get("slideCount", 4)
                enriched_topics.append(tp_copy)
            entry["topic_posts"] = enriched_topics
        manifest.append(entry)

    summary = get_gallery_summary()
    payload = {
        "template_count": len(manifest),
        "best_count": summary["best_count"],
        "high_count": summary["high_count"],
        "medium_low_worst_count": summary["medium_low_worst_count"],
        "topic_posts_collapsed_under_T79": summary["t79_topic_posts_count"],
        "purged_legacy_gen1_count": 53,
        "purged_boxy_session_count": 19,
        "refactored_to_best_count": 33,
        "templates": manifest,
    }
    manifest_json = json.dumps(payload, indent=2)
    (OUT_DIR / "gallery_manifest.json").write_text(manifest_json, encoding="utf-8")
    print(
        f"==> Wrote {OUT_DIR / 'gallery_manifest.json'} "
        f"({len(manifest)} unique templates: {summary['best_count']} Best + {summary['high_count']} High)"
    )


if __name__ == "__main__":
    main()
