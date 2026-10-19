"""HTTP Server for the Agentic AI Ideas Mining & OpenHands Autonomous Repo Factory Studio."""

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote

from src.catalog.posts_catalog import CREATOR_MINING_PLAYBOOK, POSTS_CATALOG, USER_PROFILE
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.harvester.idea_miner import AgenticIdeaMiner


WORKSPACE_ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = WORKSPACE_ROOT / "public"
REPOS_ROOT = WORKSPACE_ROOT / "generated-repos"
MINER = AgenticIdeaMiner()
ALL_CATALOG_ITEMS = list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG)


class StudioRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def _send_json(self, status: int, data: dict) -> None:
        raw = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
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
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        path = unquote(self.path.split("?")[0])
        if path in ("/", "/index.html"):
            self._send_file(PUBLIC_DIR / "index.html")
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

        if path.startswith("/repos/"):
            rel = path.replace("/repos/", "", 1)
            target = (REPOS_ROOT / rel).resolve()
            if str(target).startswith(str(REPOS_ROOT.resolve())):
                self._send_file(target)
                return

        self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self) -> None:
        if self.path == "/api/ingest-url":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            payload = json.loads(raw)
            res = MINER.ingest_custom_post_or_url(
                url=payload.get("url", ""),
                custom_title=payload.get("title", ""),
            )
            self._send_json(200, res)
            return
        self._send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8765"))
    httpd = HTTPServer(("127.0.0.1", port), StudioRequestHandler)
    print(f"OpenHands Ideas Mining Studio listening on http://127.0.0.1:{port}")
    httpd.serve_forever()
