"""HTTP Server for the Agentic AI Ideas Mining & OpenHands Autonomous Repo Factory Studio."""

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

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
from src.visuals.template_gallery import list_templates


WORKSPACE_ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = WORKSPACE_ROOT / "public"
REPOS_ROOT = WORKSPACE_ROOT / "generated-repos"
ASSETS_ROOT = WORKSPACE_ROOT / "assets"
FEEDBACK_STORE_PATH = WORKSPACE_ROOT / ".local_backup" / "app_feedback_messages.json"
MINER = AgenticIdeaMiner()
DAILY_ENGINE = DailyLinkedInPostEngine()
ALL_CATALOG_ITEMS = list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG)


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

    def _send_file(self, file_path: Path) -> None:
        if not file_path.exists() or not file_path.is_file():
            self._send_json(404, {"error": f"File not found: {file_path.name}"})
            return
        ctype, _ = mimetypes.guess_type(str(file_path))
        if file_path.suffix == ".svg":
            ctype = "image/svg+xml"
        elif file_path.suffix == ".gif":
            ctype = "image/gif"
        elif file_path.suffix == ".drawio":
            ctype = "application/xml"
        elif file_path.suffix == ".pptx":
            ctype = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype or "application/octet-stream")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = parse_qs(parsed.query)
        if path in ("/", "/index.html", "/admin/feedback"):
            self._send_file(PUBLIC_DIR / "index.html")
            return
        if path == "/api/health":
            manifest_file = WORKSPACE_ROOT / "assets" / "template-gallery" / "gallery_manifest.json"
            t_count = (
                json.loads(manifest_file.read_text(encoding="utf-8")).get("template_count", 0)
                if manifest_file.exists()
                else len(list_templates())
            )
            self._send_json(
                200,
                {
                    "status": "ok",
                    "service": "ideas-mining",
                    "template_count": t_count,
                    "repos_count": len(ALL_CATALOG_ITEMS),
                    "creator_profiles_count": len(CREATOR_MINING_PLAYBOOK.get("creator_profiles", [])),
                    "mined_template_posts_count": len(MINED_TEMPLATE_POSTS_CATALOG),
                },
            )
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
                item["category"] = "TOMORROW_TOP10" if p["id"].startswith("IDEA-") else "ANALYZED_POSTS"
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
                    "tomorrow_top10_count": len(TOMORROW_TOP10_IDEAS),
                    "analyzed_posts_count": len(POSTS_CATALOG),
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
                templates = [{**m, "files": {"svg": f"{m['id']}.svg", "gif": f"{m['id']}.gif", "png": f"{m['id']}.png"}} for m in list_templates()]
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
                default_app_name=payload.get("appName") or "Ideas Mining & Repo Factory",
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
    print(f"OpenHands Ideas Mining Studio listening on http://{host}:{port}", flush=True)
    httpd.serve_forever()
