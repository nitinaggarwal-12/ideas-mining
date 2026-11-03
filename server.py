"""HTTP Server for the Agentic AI Ideas-Minting & Ideas-Mining Studio (`ideas-minting` / `ideas-mining`)."""

import json
import mimetypes
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from src.catalog.career_minting_catalog import (
    CAREER_MINTING_TOPICS,
    FLAGSHIP_MINT01_24SLIDE_DECK_ID,
    FLAGSHIP_MINT01_24SLIDE_SHEET_ID,
    FLAGSHIP_MINT01_24SLIDE_URL,
    get_minted_repo_specs,
)
from src.catalog.posts_catalog import (
    CREATOR_MINING_PLAYBOOK,
    MINED_TEMPLATE_POSTS_CATALOG,
    POSTS_CATALOG,
    USER_PROFILE,
)
from src.catalog.stack_pairings import OSS_GOOGLE_PAIRINGS
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.harvester.daily_post_generator import DailyLinkedInPostEngine
from src.harvester.idea_miner import AgenticIdeaMiner
from src.unified_feedback_engine import (
    ADMIN_EMAIL,
    list_feedback,
    submit_feedback,
    update_feedback_status,
    verify_admin_access,
)
from src.visuals.canonical_blueprint_minter import compute_canonical_siso
from src.visuals.canonical_template_registry import get_gallery_summary, list_templates


WORKSPACE_ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = WORKSPACE_ROOT / "public"
REPOS_ROOT = WORKSPACE_ROOT / "generated-repos"
ASSETS_ROOT = WORKSPACE_ROOT / "assets"
FEEDBACK_STORE_PATH = WORKSPACE_ROOT / ".local_backup" / "app_feedback_messages.json"
MINER = AgenticIdeaMiner()
DAILY_ENGINE = DailyLinkedInPostEngine()
MINTED_REPO_SPECS = list(get_minted_repo_specs())
ALL_CATALOG_ITEMS = MINTED_REPO_SPECS + list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG)


def _build_minting_studio_payload() -> dict:
    video_manifest_path = ASSETS_ROOT / "videos" / "MINT-01_video_manifest.json"
    video_manifest = (
        json.loads(video_manifest_path.read_text(encoding="utf-8"))
        if video_manifest_path.exists()
        else {}
    )
    slides_manifest_path = WORKSPACE_ROOT / "data" / "template_google_slides_manifest.json"
    slides_map = (
        json.loads(slides_manifest_path.read_text(encoding="utf-8")).get("slides", {})
        if slides_manifest_path.exists()
        else {}
    )
    enriched_topics = []
    for t in CAREER_MINTING_TOPICS:
        tid = t["canonical_template_id"]
        slide_entry = slides_map.get(tid) or {}
        siso = compute_canonical_siso(t)
        enriched_topics.append(
            {
                **t,
                "siso_audit": siso,
                "template_google_slides_url": t.get("template_slides_url")
                or slide_entry.get("googleSlidesEditUrl", ""),
                "template_svg_url": f"/assets/template-gallery/{tid}.svg",
                "template_png_url": f"/assets/template-gallery/{tid}.png",
                "template_pptx_url": f"/assets/template-gallery/{tid}.pptx",
                "template_drawio_url": f"/assets/template-gallery/{tid}.drawio",
            }
        )
    return {
        "status": "ok",
        "project": "ideas-minting",
        "project_alias": "ideas-mining",
        "workspace_dir": str(WORKSPACE_ROOT),
        "flagship_24slide_deck_id": FLAGSHIP_MINT01_24SLIDE_DECK_ID,
        "flagship_24slide_sheet_id": FLAGSHIP_MINT01_24SLIDE_SHEET_ID,
        "flagship_24slide_url": FLAGSHIP_MINT01_24SLIDE_URL,
        "mint01_video_manifest": video_manifest,
        "gallery_summary": get_gallery_summary(),
        "live_slides_count": len(slides_map),
        "topics_count": len(enriched_topics),
        "topics": enriched_topics,
    }


class StudioRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def _send_json(self, status: int, data: dict) -> None:
        raw = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_file(self, file_path: Path, head_only: bool = False) -> None:
        if not file_path.exists() or not file_path.is_file():
            self._send_json(404, {"error": f"File not found: {file_path.name}"})
            return
        ctype, _ = mimetypes.guess_type(str(file_path))
        suffix = file_path.suffix.lower()
        if suffix == ".svg":
            ctype = "image/svg+xml"
        elif suffix == ".gif":
            ctype = "image/gif"
        elif suffix == ".drawio":
            ctype = "application/xml"
        elif suffix == ".pptx":
            ctype = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        elif suffix == ".mp4":
            ctype = "video/mp4"
        elif suffix == ".mp3":
            ctype = "audio/mpeg"

        total_size = file_path.stat().st_size
        range_header = self.headers.get("Range")
        if range_header:
            m = re.match(r"bytes=(\d*)-(\d*)", range_header.strip())
            if m:
                start_str, end_str = m.group(1), m.group(2)
                start = int(start_str) if start_str else 0
                end = int(end_str) if end_str else total_size - 1
                if start >= total_size:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{total_size}")
                    self.end_headers()
                    return
                end = min(end, total_size - 1)
                chunk_len = (end - start) + 1
                self.send_response(206)
                self.send_header("Content-Type", ctype or "application/octet-stream")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", f"bytes {start}-{end}/{total_size}")
                self.send_header("Content-Length", str(chunk_len))
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                self.end_headers()
                if not head_only:
                    with file_path.open("rb") as fh:
                        fh.seek(start)
                        self.wfile.write(fh.read(chunk_len))
                return

        self.send_response(200)
        self.send_header("Content-Type", ctype or "application/octet-stream")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Content-Length", str(total_size))
        self.end_headers()
        if not head_only:
            with file_path.open("rb") as fh:
                self.wfile.write(fh.read())

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path in ("/", "/index.html", "/admin/feedback"):
            self._send_file(PUBLIC_DIR / "index.html", head_only=True)
            return
        if path == "/styles.css":
            self._send_file(PUBLIC_DIR / "styles.css", head_only=True)
            return
        if path == "/app.js":
            self._send_file(PUBLIC_DIR / "app.js", head_only=True)
            return
        if path.startswith("/assets/"):
            rel = path.replace("/assets/", "", 1)
            target = (ASSETS_ROOT / rel).resolve()
            if str(target).startswith(str(ASSETS_ROOT.resolve())):
                self._send_file(target, head_only=True)
                return
        if path.startswith("/repos/"):
            rel = path.replace("/repos/", "", 1)
            target = (REPOS_ROOT / rel).resolve()
            if str(target).startswith(str(REPOS_ROOT.resolve())):
                self._send_file(target, head_only=True)
                return
        self.send_response(404)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = parse_qs(parsed.query)
        if path in ("/", "/index.html", "/admin/feedback"):
            self._send_file(PUBLIC_DIR / "index.html")
            return
        if path == "/api/health":
            summary = get_gallery_summary()
            self._send_json(
                200,
                {
                    "status": "ok",
                    "service": "ideas-minting",
                    "service_alias": "ideas-mining",
                    "template_count": summary["template_count"],
                    "best_count": summary["best_count"],
                    "high_count": summary["high_count"],
                    "t79_topic_posts_count": summary["t79_topic_posts_count"],
                    "repos_count": len(ALL_CATALOG_ITEMS),
                    "minting_topics_count": len(CAREER_MINTING_TOPICS),
                    "flagship_24slide_deck_id": FLAGSHIP_MINT01_24SLIDE_DECK_ID,
                    "creator_profiles_count": len(CREATOR_MINING_PLAYBOOK.get("creator_profiles", [])),
                    "mined_template_posts_count": len(MINED_TEMPLATE_POSTS_CATALOG),
                },
            )
            return
        if path == "/api/minting-studio":
            self._send_json(200, _build_minting_studio_payload())
            return
        if path == "/universal_feedback_widget.js":
            self._send_file(PUBLIC_DIR / "universal_feedback_widget.js")
            return
        if path == "/api/feedback/messages":
            headers_dict = {k: v for k, v in self.headers.items()}
            client_ip = self.client_address[0] if self.client_address else ""
            is_auth, resolved_email, auth_mode = verify_admin_access(
                headers=headers_dict, remote_addr=client_ip, query_params=qs
            )
            if not is_auth:
                self._send_json(
                    403,
                    {
                        "ok": False,
                        "authorized": False,
                        "resolvedEmail": resolved_email,
                        "authMode": auth_mode,
                        "error": f"Admin access restricted to {ADMIN_EMAIL}",
                    },
                )
                return
            res = list_feedback(
                default_app_id="ideas-mining",
                local_store_path=FEEDBACK_STORE_PATH,
                scope=(qs.get("scope") or ["all"])[0],
                category_filter=(qs.get("category") or [""])[0],
                priority_filter=(qs.get("priority") or [""])[0],
                status_filter=(qs.get("status") or [""])[0],
                search_query=(qs.get("search") or qs.get("q") or [""])[0],
                force_sheet_refresh=(qs.get("force") or ["0"])[0] in ("1", "true"),
            )
            res["authorized"] = True
            res["resolvedEmail"] = resolved_email
            res["authMode"] = auth_mode
            self._send_json(200, res)
            return
        if path == "/styles.css":
            self._send_file(PUBLIC_DIR / "styles.css")
            return
        if path == "/app.js":
            self._send_file(PUBLIC_DIR / "app.js")
            return

        if path == "/api/workspace-state":
            enriched_repos = []
            for p in ALL_CATALOG_ITEMS:
                r_dir = REPOS_ROOT / p["repo_slug"]
                receipt_file = r_dir / "openhands_verification_receipt.json"
                receipt = {}
                if receipt_file.exists():
                    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
                item = dict(p)
                if p["id"].startswith("MINT-"):
                    item["category"] = "CAREER_MINTING"
                elif p["id"].startswith("IDEA-"):
                    item["category"] = "TOMORROW_TOP10"
                else:
                    item["category"] = "ANALYZED_POSTS"
                item["git_commit_sha"] = receipt.get("openhands_trajectory", {}).get("git_commit_sha", "verified")
                item["verification"] = receipt.get("verification", {})
                item["openhands_trajectory"] = receipt.get("openhands_trajectory", {})
                enriched_repos.append(item)

            self._send_json(
                200,
                {
                    "user_profile": USER_PROFILE,
                    "playbook": CREATOR_MINING_PLAYBOOK,
                    "mined_template_posts": MINED_TEMPLATE_POSTS_CATALOG,
                    "minted_repos_count": len(MINTED_REPO_SPECS),
                    "tomorrow_top10_count": len(TOMORROW_TOP10_IDEAS),
                    "analyzed_posts_count": len(POSTS_CATALOG),
                    "flagship_24slide_url": FLAGSHIP_MINT01_24SLIDE_URL,
                    "minting_topics": CAREER_MINTING_TOPICS,
                    "repos": enriched_repos,
                },
            )
            return

        if path.startswith("/api/repo-detail/"):
            slug = path.replace("/api/repo-detail/", "").strip("/")
            matched = next((p for p in ALL_CATALOG_ITEMS if p["repo_slug"] == slug), None)
            if not matched:
                self._send_json(404, {"error": "Unknown repository slug"})
                return
            r_dir = REPOS_ROOT / slug
            tf_main = (r_dir / "terraform" / "main.tf").read_text(encoding="utf-8") if (r_dir / "terraform" / "main.tf").exists() else ""
            engine_py = (r_dir / "src" / "engine.py").read_text(encoding="utf-8") if (r_dir / "src" / "engine.py").exists() else ""
            li_draft = (r_dir / "linkedin_post_draft.md").read_text(encoding="utf-8") if (r_dir / "linkedin_post_draft.md").exists() else ""
            nb3_prompt = (r_dir / "visuals" / "nano_banana_3_prompt.md").read_text(encoding="utf-8") if (r_dir / "visuals" / "nano_banana_3_prompt.md").exists() else ""
            slides_manifest = {}
            if (r_dir / "slides" / "slide_manifest.json").exists():
                slides_manifest = json.loads((r_dir / "slides" / "slide_manifest.json").read_text(encoding="utf-8"))
            receipt = {}
            if (r_dir / "openhands_verification_receipt.json").exists():
                receipt = json.loads((r_dir / "openhands_verification_receipt.json").read_text(encoding="utf-8"))

            detail = dict(matched)
            detail["git_commit_sha"] = receipt.get("openhands_trajectory", {}).get("git_commit_sha", "verified")
            detail["terraform_main"] = tf_main
            detail["engine_py"] = engine_py
            detail["linkedin_post_draft"] = li_draft
            detail["nano_banana_3_prompt"] = nb3_prompt
            detail["slides"] = slides_manifest.get("slides", [])
            self._send_json(200, detail)
            return

        if path == "/api/live-mining-feeds":
            self._send_json(
                200,
                {
                    "arxiv": MINER.fetch_live_arxiv_signals(max_results=4),
                    "github": MINER.fetch_live_github_breakouts(max_results=4),
                },
            )
            return

        if path == "/api/daily-posts":
            edition_date = (qs.get("date") or [""])[0]
            self._send_json(200, DAILY_ENGINE.get_daily_posts_payload(edition_date=edition_date))
            return

        if path in ("/api/template-gallery", "/api/templates"):
            manifest_file = WORKSPACE_ROOT / "assets" / "template-gallery" / "gallery_manifest.json"
            if manifest_file.exists():
                self._send_json(200, json.loads(manifest_file.read_text(encoding="utf-8")))
            else:
                templates = [
                    {**m, "files": {"svg": f"{m['id']}.svg", "gif": f"{m['id']}.gif", "png": f"{m['id']}.png"}}
                    for m in list_templates()
                ]
                self._send_json(200, {"template_count": len(templates), "templates": templates})
            return

        if path == "/api/stack-pairings":
            self._send_json(200, {"pairings": OSS_GOOGLE_PAIRINGS})
            return

        if path.startswith("/assets/"):
            rel = path.replace("/assets/", "", 1)
            target = (ASSETS_ROOT / rel).resolve()
            if str(target).startswith(str(ASSETS_ROOT.resolve())):
                self._send_file(target)
                return

        if path.startswith("/repos/"):
            rel = path.replace("/repos/", "", 1)
            target = (REPOS_ROOT / rel).resolve()
            if str(target).startswith(str(REPOS_ROOT.resolve())):
                self._send_file(target)
                return

        self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = parse_qs(parsed.query)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        payload = json.loads(raw) if raw else {}
        if path == "/api/feedback/submit":
            headers_dict = {k: v for k, v in self.headers.items()}
            res = submit_feedback(
                payload=payload,
                default_app_id=payload.get("appId") or "ideas-mining",
                default_app_name=payload.get("appName") or "Ideas Minting & Repo Factory",
                local_store_path=FEEDBACK_STORE_PATH,
                headers=headers_dict,
            )
            self._send_json(200, res)
            return
        if path == "/api/feedback/status":
            headers_dict = {k: v for k, v in self.headers.items()}
            client_ip = self.client_address[0] if self.client_address else ""
            is_auth, resolved_email, auth_mode = verify_admin_access(
                headers=headers_dict, remote_addr=client_ip, query_params=qs
            )
            if not is_auth:
                self._send_json(
                    403,
                    {
                        "ok": False,
                        "authorized": False,
                        "resolvedEmail": resolved_email,
                        "authMode": auth_mode,
                        "error": f"Admin access restricted to {ADMIN_EMAIL}",
                    },
                )
                return
            fid = str(payload.get("id") or payload.get("feedbackId") or "").strip()
            new_status = str(payload.get("status") or "").strip() or None
            do_delete = bool(payload.get("delete")) or str(payload.get("action") or "").lower() == "delete"
            res = update_feedback_status(
                feedback_id=fid,
                new_status=new_status,
                delete=do_delete,
                local_store_path=FEEDBACK_STORE_PATH,
            )
            self._send_json(200, res)
            return
        if path == "/api/daily-posts/generate":
            topic_query = str(payload.get("topic_query") or payload.get("topic") or "").strip()
            creator_style = str(payload.get("creator_style") or payload.get("style") or "AUTO").strip()
            count = int(payload.get("count") or 6)
            edition_date = str(payload.get("edition_date") or "").strip() or None
            use_live = payload.get("use_live_network")
            if use_live is None:
                use_live = True
            edition = DAILY_ENGINE.generate_daily_edition(
                edition_date=edition_date,
                count=count,
                topic_query=topic_query,
                creator_style=creator_style,
                use_live_network=bool(use_live),
            )
            self._send_json(
                200,
                {
                    "status": "GENERATED",
                    "edition": edition,
                    "posts": edition["posts"],
                },
            )
            return
        if path == "/api/ingest-url":
            res = MINER.ingest_custom_post_or_url(
                url=payload.get("url", ""),
                custom_title=payload.get("title", ""),
            )
            self._send_json(200, res)
            return
        self._send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8765"))
    httpd = ThreadingHTTPServer((host, port), StudioRequestHandler)
    print(f"Ideas-Minting & Ideas-Mining Studio listening on http://{host}:{port}", flush=True)
    httpd.serve_forever()
