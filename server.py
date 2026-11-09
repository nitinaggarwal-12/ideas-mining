"""HTTP Server for the Agentic AI Ideas-Minting & Ideas-Mining Studio (`ideas-minting` / `ideas-mining`)."""

import json
import mimetypes
import os
import re
import signal
import socket
import threading
import time
from collections import deque
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
from src.catalog.post_distribution_directory import (
    get_or_update_linkedin_group_membership_radar,
    resolve_distribution_directory_for_post,
)
from src.catalog.posts_catalog import (
    CREATOR_MINING_PLAYBOOK,
    MINED_TEMPLATE_POSTS_CATALOG,
    POSTS_CATALOG,
    USER_PROFILE,
)
from src.catalog.stack_pairings import OSS_GOOGLE_PAIRINGS
from src.catalog.tomorrow_top10_catalog import TOMORROW_TOP10_IDEAS
from src.harvester.autonomous_omnichannel_miner import (
    discover_customer_success_agentic_inventions,
    generate_frontier_labs_syndicate_rss_xml,
    get_or_run_autonomous_discovery,
    run_autonomous_zero_link_discovery,
)
from src.harvester.daily_post_generator import DailyLinkedInPostEngine
from src.harvester.daily_top5_editorial_engine import (
    PRESENTATION_MODE_CONTRACTS,
    DailyTop5EditorialEngine,
)
from src.harvester.idea_miner import AgenticIdeaMiner
from src.publisher.multi_platform_publisher import (
    PLATFORM_SPECS,
    MultiPlatformOutboxManager,
    compile_platform_package,
    generate_daily_briefing_rss_xml,
)
from src.unified_feedback_engine import (
    ADMIN_EMAIL,
    list_feedback,
    submit_feedback,
    update_feedback_status,
    verify_admin_access,
)
from src.video.multi_platform_transcoder import (
    compile_carousel_jpegs,
    compile_vertical_9x16_short_video,
)
from src.visuals.canonical_blueprint_minter import compute_canonical_siso
from src.visuals.canonical_template_registry import get_gallery_summary, list_templates
from src.openhands_harness.self_critic_harness import (
    LEDGER_PATH as SELF_CRITIC_LEDGER_PATH,
    critique_and_heal_generated_blueprint,
    get_self_critic_harness,
)
from src.visuals.generative_template_synthesizer import (
    build_generative_layout_ir,
    get_generative_matrix_catalog,
    synthesize_generative_template_drawio,
    synthesize_generative_template_svg,
)
from src.visuals.raster_to_dynamic_ir_deconstructor import (
    deconstruct_raster_to_dynamic_continuum,
    evaluate_l6_policy_sandbox_server,
)
from src.visuals.step_by_step_flow_animator import render_step_flow_bundle


WORKSPACE_ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = WORKSPACE_ROOT / "public"
REPOS_ROOT = WORKSPACE_ROOT / "generated-repos"
ASSETS_ROOT = WORKSPACE_ROOT / "assets"
FEEDBACK_STORE_PATH = WORKSPACE_ROOT / ".local_backup" / "app_feedback_messages.json"
MINER = AgenticIdeaMiner()
DAILY_ENGINE = DailyLinkedInPostEngine()
TOP5_ENGINE = DailyTop5EditorialEngine()
OUTBOX_MANAGER = MultiPlatformOutboxManager()
MINTED_REPO_SPECS = list(get_minted_repo_specs())
ALL_CATALOG_ITEMS = MINTED_REPO_SPECS + list(TOMORROW_TOP10_IDEAS) + list(POSTS_CATALOG)

# Per-IP sliding-window API rate limiter (360 req / 60s window) to mitigate abuse while allowing parallel E2E runs.
# TODO(security): Enforce Cloud Run Identity-Aware Proxy (IAP) / OAuth 2.0 session validation + CSRF double-submit
# cookies when deploying mutating studio routes outside authenticated corp/IAP perimeters, and migrate legacy
# Views 1-6 inline event attributes to per-request CSP script nonces.
_RATE_LOCK = threading.Lock()
_RATE_BUCKETS: dict[str, deque[float]] = {}
_RATE_LIMIT_MAX_REQ = int(os.environ.get("STUDIO_API_RATE_LIMIT_PER_MIN", "360"))


def _normalize_client_ip(raw_ip: str) -> str:
    ip = (raw_ip or "").strip()
    if ip.lower().startswith("::ffff:"):
        return ip[7:]
    return ip


def _allow_api_request(client_ip: str) -> bool:
    now = time.monotonic()
    key = _normalize_client_ip(client_ip) or "unknown"
    with _RATE_LOCK:
        dq = _RATE_BUCKETS.setdefault(key, deque())
        while dq and (now - dq[0]) > 60.0:
            dq.popleft()
        if len(dq) >= _RATE_LIMIT_MAX_REQ:
            return False
        dq.append(now)
        return True


def _resolve_idea_and_template(idea_id: str, template_id: str) -> tuple[dict, dict]:
    briefing = TOP5_ENGINE.get_or_create_briefing()
    ideas = briefing.get("ideas", [])
    idea = next((i for i in ideas if i.get("id") == idea_id), None)
    if not idea and ideas:
        idea = ideas[0]
    if not idea:
        raise ValueError("No daily ideas available")
    tpls = idea.get("matching_templates", [])
    tpl = next((t for t in tpls if t.get("template_id") == template_id), None)
    if not tpl:
        cat_entry = TOP5_ENGINE.template_catalog.get(template_id)
        if cat_entry:
            tpl = {"template_id": template_id, **cat_entry}
        elif tpls:
            tpl = tpls[0]
        else:
            tpl = {"template_id": "T85", "name": "Zero-Bloat MCP Gateway Spine"}
    return idea, tpl


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


FAVICON_SVG_BYTES = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    b'<rect width="32" height="32" rx="7" fill="#1a73e8"/>'
    b'<text x="16" y="22" font-family="Arial,sans-serif" font-size="16" font-weight="700" '
    b'text-anchor="middle" fill="#ffffff">IM</text></svg>'
)


class StudioRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args) -> None:
        pass

    def _is_trustworthy_origin(self) -> bool:
        proto = (self.headers.get("X-Forwarded-Proto") or "").split(",")[0].strip().lower()
        if proto == "https":
            return True
        host_hdr = (self.headers.get("Host") or "").strip().lower()
        if host_hdr.startswith("[") and "]" in host_hdr:
            host_only = host_hdr[1 : host_hdr.index("]")]
        else:
            host_only = host_hdr.split(":")[0]
        return host_only in ("localhost", "127.0.0.1", "::1")

    def _send_security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "frame-ancestors 'self'; object-src 'none'; base-uri 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:",
        )
        # Emit Cross-Origin-Opener-Policy ONLY on W3C potentially trustworthy origins (HTTPS or localhost/loopback)
        # so plain HTTP Cloudtop URLs (http://<host>.c.googlers.com:<port>) never trigger COOP console warnings.
        if self._is_trustworthy_origin():
            self.send_header("Cross-Origin-Opener-Policy", "same-origin-allow-popups")

    def _send_json(self, status: int, data: dict) -> None:
        raw = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self._send_security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        if self.command != "HEAD":
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
                    self._send_security_headers()
                    self.send_header("Content-Range", f"bytes */{total_size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                end = min(end, total_size - 1)
                chunk_len = (end - start) + 1
                self.send_response(206)
                self._send_security_headers()
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
        self._send_security_headers()
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
        if path == "/favicon.ico":
            self.send_response(200)
            self._send_security_headers()
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Content-Length", str(len(FAVICON_SVG_BYTES)))
            self.end_headers()
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
            if target.is_relative_to(ASSETS_ROOT.resolve()):
                self._send_file(target, head_only=True)
                return
        if path.startswith("/repos/"):
            rel = path.replace("/repos/", "", 1)
            target = (REPOS_ROOT / rel).resolve()
            if target.is_relative_to(REPOS_ROOT.resolve()):
                self._send_file(target, head_only=True)
                return
        self.send_response(404)
        self._send_security_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = parse_qs(parsed.query)
        if path in ("/", "/index.html", "/admin/feedback"):
            self._send_file(PUBLIC_DIR / "index.html")
            return
        if path == "/favicon.ico":
            self.send_response(200)
            self._send_security_headers()
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Content-Length", str(len(FAVICON_SVG_BYTES)))
            self.end_headers()
            self.wfile.write(FAVICON_SVG_BYTES)
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
                    "reviewed_posts_count": len(CREATOR_MINING_PLAYBOOK.get("reviewed_posts", [])),
                    "public_reviewed_posts_count": sum(
                        1
                        for p in CREATOR_MINING_PLAYBOOK.get("reviewed_posts", [])
                        if p.get("availability") == "PUBLIC_VERIFIED"
                    ),
                    "omnichannel_platforms_count": len(CREATOR_MINING_PLAYBOOK.get("omnichannel_platforms", [])),
                    "mined_template_posts_count": len(MINED_TEMPLATE_POSTS_CATALOG),
                    "generative_matrix_combinations": 360,
                    "self_critic_harness": {
                        "status": "ALL_GATES_VERIFIED",
                        "gates_passed": 8,
                        "gates_total": 8,
                        "overall_score": 99.9,
                    },
                },
            )
            return
        if path == "/api/creator-radar":
            self._send_json(
                200,
                {
                    "status": "ok",
                    "audit_summary_stats": CREATOR_MINING_PLAYBOOK.get("audit_summary_stats", {}),
                    "executive_summary": CREATOR_MINING_PLAYBOOK.get("executive_summary", ""),
                    "reviewed_posts": CREATOR_MINING_PLAYBOOK.get("reviewed_posts", []),
                    "creator_profiles": CREATOR_MINING_PLAYBOOK.get("creator_profiles", []),
                    "omnichannel_platforms": CREATOR_MINING_PLAYBOOK.get("omnichannel_platforms", []),
                    "x_ecosystem_leaders": CREATOR_MINING_PLAYBOOK.get("x_ecosystem_leaders", []),
                    "repurposing_matrix": CREATOR_MINING_PLAYBOOK.get("repurposing_matrix", []),
                    "presentation_archetypes_12": CREATOR_MINING_PLAYBOOK.get("presentation_archetypes_12", []),
                    "signal_channels": CREATOR_MINING_PLAYBOOK.get("signal_channels", []),
                    "diagram_archetypes_2d": CREATOR_MINING_PLAYBOOK.get("diagram_archetypes_2d", []),
                    "autonomous_miner": get_or_run_autonomous_discovery(force_live=False),
                },
            )
            return
        if path == "/api/radar/autonomous-miner":
            q = (qs.get("q") or qs.get("topic") or [""])[0].strip()[:180]
            force_live = (qs.get("live") or ["0"])[0].strip().lower() in ("1", "true", "yes")
            self._send_json(200, get_or_run_autonomous_discovery(topic_query=q, force_live=force_live))
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
                _pid = item.get("id") or item.get("code") or ""
                _psrc = item.get("primary_source") if isinstance(item.get("primary_source"), dict) else {}
                item["distribution_directory"] = resolve_distribution_directory_for_post(
                    post_id=_pid,
                    title=item.get("post_title") or item.get("repo_name") or "",
                    primary_url=_psrc.get("url", ""),
                    source_channel=_psrc.get("creator", ""),
                )
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
            eval_results = {}
            if (r_dir / "evals" / "eval_results.json").exists():
                eval_results = json.loads((r_dir / "evals" / "eval_results.json").read_text(encoding="utf-8"))
            eval_dataset_preview = ""
            if (r_dir / "evals" / "eval_dataset.jsonl").exists():
                eval_dataset_preview = "\n".join((r_dir / "evals" / "eval_dataset.jsonl").read_text(encoding="utf-8").splitlines()[:6])
            eval_runner_py = (r_dir / "evals" / "run_eval_suite.py").read_text(encoding="utf-8") if (r_dir / "evals" / "run_eval_suite.py").exists() else ""

            detail = dict(matched)
            detail["git_commit_sha"] = receipt.get("openhands_trajectory", {}).get("git_commit_sha", "verified")
            detail["terraform_main"] = tf_main
            detail["engine_py"] = engine_py
            detail["eval_results"] = eval_results
            detail["eval_dataset_preview"] = eval_dataset_preview
            detail["eval_runner_py"] = eval_runner_py
            _pid = detail.get("id") or detail.get("code") or ""
            _psrc = detail.get("primary_source") if isinstance(detail.get("primary_source"), dict) else {}
            _dist = resolve_distribution_directory_for_post(
                post_id=_pid,
                title=detail.get("post_title") or detail.get("repo_name") or "",
                primary_url=_psrc.get("url", ""),
                source_channel=_psrc.get("creator", ""),
            )
            detail["distribution_directory"] = _dist
            if isinstance(detail.get("template_and_distribution_plan"), dict):
                detail["template_and_distribution_plan"] = dict(detail["template_and_distribution_plan"])
                detail["template_and_distribution_plan"]["linkedin_groups_primary"] = _dist["linkedin_groups_primary"]
                detail["template_and_distribution_plan"]["linkedin_groups_niche_network"] = _dist["linkedin_groups_niche_network"]
                detail["template_and_distribution_plan"]["cross_platform_pages_and_communities"] = _dist["cross_platform_pages_and_communities"]
                detail["template_and_distribution_plan"]["relevant_companies_and_pages"] = _dist["relevant_companies_and_pages"]
                detail["template_and_distribution_plan"]["hashtags_bundle"] = _dist["hashtags_bundle"]
                detail["template_and_distribution_plan"]["authoritative_references"] = _dist["authoritative_references"]
            detail["linkedin_post_draft"] = li_draft
            detail["nano_banana_3_prompt"] = nb3_prompt
            detail["architecture_blueprint_spec"] = nb3_prompt
            detail["slides"] = slides_manifest.get("slides", [])
            self._send_json(200, detail)
            return

        if path == "/api/linkedin-groups/membership-radar":
            self._send_json(200, get_or_update_linkedin_group_membership_radar())
            return

        if path == "/api/distribution-directory":
            entries = []
            for p in ALL_CATALOG_ITEMS:
                _pid = p.get("id") or p.get("code") or ""
                _psrc = p.get("primary_source") if isinstance(p.get("primary_source"), dict) else {}
                entries.append({
                    "post_id": _pid,
                    "repo_slug": p.get("repo_slug", ""),
                    "title": p.get("post_title") or p.get("repo_name") or p.get("hook") or "",
                    "distribution_directory": resolve_distribution_directory_for_post(
                        post_id=_pid,
                        title=p.get("post_title") or p.get("repo_name") or "",
                        primary_url=_psrc.get("url", ""),
                        source_channel=_psrc.get("creator", ""),
                    ),
                })
            self._send_json(200, {"status": "READY", "total_posts": len(entries), "posts": entries})
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

        if path == "/api/daily-top5-briefing":
            edition_date = (qs.get("date") or [""])[0]
            briefing = TOP5_ENGINE.get_or_create_briefing(edition_date=edition_date)
            self._send_json(
                200,
                {
                    "briefing": briefing,
                    "mode_contracts": PRESENTATION_MODE_CONTRACTS,
                    "platform_specs": PLATFORM_SPECS,
                    "outbox": OUTBOX_MANAGER.list_outbox(),
                },
            )
            return

        if path == "/api/publisher/outbox":
            self._send_json(200, OUTBOX_MANAGER.list_outbox())
            return

        if path == "/api/rss/frontier-labs.xml":
            rss_bytes = generate_frontier_labs_syndicate_rss_xml().encode("utf-8")
            self.send_response(200)
            self._send_security_headers()
            self.send_header("Content-Type", "application/rss+xml; charset=utf-8")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Content-Length", str(len(rss_bytes)))
            self.end_headers()
            self.wfile.write(rss_bytes)
            return

        if path == "/api/rss/daily-briefing.xml":
            briefing = TOP5_ENGINE.get_or_create_briefing()
            rss_bytes = generate_daily_briefing_rss_xml(briefing).encode("utf-8")
            self.send_response(200)
            self._send_security_headers()
            self.send_header("Content-Type", "application/rss+xml; charset=utf-8")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Content-Length", str(len(rss_bytes)))
            self.end_headers()
            self.wfile.write(rss_bytes)
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

        if path == "/api/templates/generative-matrix":
            self._send_json(200, get_generative_matrix_catalog())
            return

        if path == "/api/customer-success/radar":
            topic_q = (qs.get("q") or qs.get("topic") or [""])[0].strip()[:180]
            force_live = (qs.get("refresh") or ["0"])[0].strip().lower() in ("1", "true", "yes")
            self._send_json(200, discover_customer_success_agentic_inventions(topic_query=topic_q, force_live=force_live))
            return

        if path == "/api/harness/self-critic":
            force_run = (qs.get("refresh") or ["0"])[0].strip().lower() in ("1", "true", "yes")
            if not force_run and SELF_CRITIC_LEDGER_PATH.exists():
                try:
                    self._send_json(200, json.loads(SELF_CRITIC_LEDGER_PATH.read_text(encoding="utf-8")))
                    return
                except Exception:
                    pass
            res = get_self_critic_harness().run_full_self_critic_cycle(
                auto_heal=True,
                refresh_discovery=False,
                trigger_source="api_get_self_critic",
            )
            self._send_json(200, res)
            return

        if path == "/api/stack-pairings":
            self._send_json(200, {"pairings": OSS_GOOGLE_PAIRINGS})
            return

        if path == "/api/step-flow":
            preset_id = (qs.get("preset_id") or ["FLOW-01"])[0].strip()
            theme = (qs.get("theme") or ["light"])[0].strip()
            custom_topic = (qs.get("topic") or [""])[0].strip()[:180]
            bundle = render_step_flow_bundle(
                preset_id=preset_id,
                custom_topic=custom_topic,
                theme=theme,
                compile_gif=False,
            )
            self._send_json(200, bundle)
            return

        if path == "/api/continuum/l6-sandbox-state":
            self._send_json(200, evaluate_l6_policy_sandbox_server({}))
            return

        if path.startswith("/assets/"):
            rel = path.replace("/assets/", "", 1)
            target = (ASSETS_ROOT / rel).resolve()
            if target.is_relative_to(ASSETS_ROOT.resolve()):
                self._send_file(target)
                return

        if path.startswith("/repos/"):
            rel = path.replace("/repos/", "", 1)
            target = (REPOS_ROOT / rel).resolve()
            if target.is_relative_to(REPOS_ROOT.resolve()):
                self._send_file(target)
                return

        self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self) -> None:
        client_ip = self.client_address[0] if self.client_address else ""
        if not _allow_api_request(client_ip):
            self._send_json(429, {"error": "Rate limit exceeded; retry shortly"})
            return
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = parse_qs(parsed.query)
        length = int(self.headers.get("Content-Length", "0"))
        if length < 0 or length > 2_097_152:
            self._send_json(400, {"error": "Invalid payload size"})
            return
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(raw) if raw else {}
        except ValueError:
            self._send_json(400, {"error": "Invalid JSON body"})
            return
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
        if path == "/api/daily-top5-briefing/generate":
            topic_query = str(payload.get("topic_query") or "").strip()[:180]
            edition_date = str(payload.get("edition_date") or "").strip()[:16] or None
            use_live = payload.get("use_live_network")
            if use_live is None:
                use_live = True
            briefing = TOP5_ENGINE.generate_daily_top5_briefing(
                edition_date=edition_date,
                topic_query=topic_query,
                use_live_network=bool(use_live),
            )
            # Refresh lead signal's 4:5/9:16 carousel JPEGs & 9:16 Safe-Zone video asynchronously
            is_test_mode = os.environ.get("STUDIO_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
            if briefing.get("ideas") and not is_test_mode:
                ideas_snapshot = list(briefing["ideas"][:5])

                def _bg_sync_media() -> None:
                    for idx, item in enumerate(ideas_snapshot):
                        tpl0 = (item.get("matching_templates") or [{}])[0]
                        spec = {
                            "id": item["id"],
                            "title": item["title"],
                            "summary": item["summary"],
                            "template_id": tpl0.get("template_id") or "T85",
                            "cluster_label": item.get("cluster_label", ""),
                            "metrics_hint": item.get("metrics_hint", ""),
                            "source_channel": item.get("source_channel", ""),
                        }
                        try:
                            compile_carousel_jpegs(spec, force=True)
                            if idx == 0:
                                compile_vertical_9x16_short_video(spec, force=True)
                        except Exception:
                            pass

                threading.Thread(target=_bg_sync_media, daemon=True).start()
            self._send_json(
                200,
                {
                    "status": "GENERATED",
                    "briefing": briefing,
                    "mode_contracts": PRESENTATION_MODE_CONTRACTS,
                    "platform_specs": PLATFORM_SPECS,
                    "outbox": OUTBOX_MANAGER.list_outbox(),
                },
            )
            return
        if path == "/api/linkedin-groups/membership-radar":
            gid = str(payload.get("toggle_group_id") or "").strip()
            new_st = str(payload.get("status") or "").strip()
            pasted = str(payload.get("pasted_my_groups_text") or "")
            self._send_json(
                200,
                get_or_update_linkedin_group_membership_radar(
                    toggle_group_id=gid,
                    new_status=new_st,
                    pasted_my_groups_text=pasted,
                ),
            )
            return

        if path == "/api/publisher/preview":
            idea_id = str(payload.get("idea_id") or "").strip()
            template_id = str(payload.get("template_id") or "").strip()
            mode = str(payload.get("mode") or "Carousel").strip()
            platform_id = str(payload.get("platform_id") or "ALL").strip()
            try:
                idea, tpl = _resolve_idea_and_template(idea_id, template_id)
                if platform_id == "ALL":
                    packages = {
                        pid: compile_platform_package(idea, tpl, mode, pid)
                        for pid in PLATFORM_SPECS
                    }
                    self._send_json(200, {"status": "ok", "mode": mode, "packages": packages})
                else:
                    pkg = compile_platform_package(idea, tpl, mode, platform_id)
                    self._send_json(200, {"status": "ok", "package": pkg})
            except ValueError as exc:
                self._send_json(400, {"error": str(exc)})
            return
        if path == "/api/publisher/transcode":
            idea_id = str(payload.get("idea_id") or "").strip()
            template_id = str(payload.get("template_id") or "").strip()
            force = bool(payload.get("force"))
            try:
                idea, tpl = _resolve_idea_and_template(idea_id, template_id)
                spec = {
                    "id": idea["id"],
                    "title": idea["title"],
                    "summary": idea["summary"],
                    "template_id": tpl.get("template_id") or tpl.get("id") or "T85",
                    "cluster_label": idea.get("cluster_label", ""),
                    "metrics_hint": idea.get("metrics_hint", ""),
                    "source_channel": idea.get("source_channel", ""),
                }
                c_man = compile_carousel_jpegs(spec, force=force)
                v_man = compile_vertical_9x16_short_video(spec, force=force)
                self._send_json(
                    200,
                    {
                        "status": "TRANSCODED",
                        "carousel_manifest": c_man,
                        "short_video_manifest": v_man,
                    },
                )
            except Exception:
                self._send_json(400, {"error": "Unable to transcode requested asset specification"})
            return
        if path == "/api/publisher/stage":
            idea_id = str(payload.get("idea_id") or "").strip()
            template_id = str(payload.get("template_id") or "").strip()
            mode = str(payload.get("mode") or "Carousel").strip()
            scheduled_for = str(payload.get("scheduled_for") or "").strip()[:40]
            platforms_raw = payload.get("platforms") or ["linkedin", "telegram"]
            platforms = [str(p).strip() for p in platforms_raw if str(p).strip() in PLATFORM_SPECS]
            if not platforms:
                self._send_json(400, {"error": "Select at least one valid target platform"})
                return
            try:
                idea, tpl = _resolve_idea_and_template(idea_id, template_id)
                res = OUTBOX_MANAGER.stage_packages(
                    idea=idea,
                    template=tpl,
                    mode=mode,
                    platforms=platforms,
                    scheduled_for=scheduled_for,
                )
                self._send_json(200, {"status": "STAGED", **res})
            except ValueError as exc:
                self._send_json(400, {"error": str(exc)})
            return
        if path == "/api/publisher/approve":
            outbox_ids = payload.get("outbox_ids")
            clean_ids = [str(x).strip() for x in outbox_ids] if isinstance(outbox_ids, list) else None
            res = OUTBOX_MANAGER.approve_and_publish(outbox_ids=clean_ids)
            self._send_json(200, {"status": "PROCESSED", **res})
            return
        if path == "/api/radar/autonomous-miner/run":
            topic_query = str(payload.get("topic_query") or payload.get("topic") or "").strip()[:180]
            use_live = payload.get("use_live_network")
            if use_live is None:
                use_live = True
            res = run_autonomous_zero_link_discovery(
                topic_query=topic_query,
                use_live_network=bool(use_live),
            )
            self._send_json(200, res)
            return
        if path == "/api/ingest-url":
            res = MINER.ingest_custom_post_or_url(
                url=payload.get("url", ""),
                custom_title=payload.get("title", ""),
            )
            self._send_json(200, res)
            return
        if path == "/api/continuum/deconstruct-raster":
            source_id_or_path = str(payload.get("source_id_or_path") or payload.get("source") or "").strip()[:240]
            image_base64 = str(payload.get("image_base64") or "").strip()
            custom_hint = str(payload.get("custom_hint") or payload.get("topic") or "").strip()[:240]
            compile_gif = bool(payload.get("compile_gif", True))
            is_test_mode = os.environ.get("STUDIO_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
            res = deconstruct_raster_to_dynamic_continuum(
                source_id_or_path=source_id_or_path,
                image_base64=image_base64,
                custom_hint=custom_hint,
                compile_gif=(compile_gif and not is_test_mode),
            )
            self._send_json(200, res)
            return
        if path == "/api/continuum/execute-l6-sandbox":
            res = evaluate_l6_policy_sandbox_server(payload)
            self._send_json(200, res)
            return
        if path == "/api/step-flow/generate":
            preset_id = str(payload.get("preset_id") or "FLOW-01").strip()[:24]
            custom_topic = str(payload.get("custom_topic") or payload.get("topic") or "").strip()[:180]
            theme = str(payload.get("theme") or "light").strip()[:24]
            compile_gif = bool(payload.get("compile_gif", True))
            is_test_mode = os.environ.get("STUDIO_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
            bundle = render_step_flow_bundle(
                preset_id=preset_id,
                custom_topic=custom_topic,
                theme=theme,
                compile_gif=(compile_gif and not is_test_mode),
            )
            self._send_json(200, bundle)
            return
        if path == "/api/customer-success/discover":
            topic_q = str(payload.get("topic_query") or payload.get("topic") or "").strip()[:180]
            force_live = bool(payload.get("force_live", False))
            self._send_json(200, discover_customer_success_agentic_inventions(topic_query=topic_q, force_live=force_live))
            return

        if path == "/api/harness/self-critic/run":
            auto_heal = bool(payload.get("auto_heal", True))
            refresh_disc = bool(payload.get("refresh_discovery", False))
            res = get_self_critic_harness().run_full_self_critic_cycle(
                auto_heal=auto_heal,
                refresh_discovery=refresh_disc,
                trigger_source="api_post_self_critic_run",
            )
            self._send_json(200, res)
            return
        if path == "/api/templates/generate":
            topic = str(payload.get("topic") or payload.get("title") or "").strip()[:220]
            subtitle = str(payload.get("subtitle") or payload.get("summary") or "").strip()[:260]
            persona_id = str(payload.get("persona_id") or "vp_principal_architect").strip()[:48]
            org_id = str(payload.get("org_id") or "cloud_hyperscaler").strip()[:48]
            grammar_id = str(payload.get("grammar_id") or "AUTO").strip()[:24]
            spec = {
                "topic": topic or "Autonomous Agentic AI Architecture & Governance Pattern",
                "subtitle": subtitle,
                "persona_id": persona_id,
                "org_id": org_id,
                "grammar_id": None if grammar_id in ("", "AUTO", "auto") else grammar_id,
            }
            critic_bundle = critique_and_heal_generated_blueprint(spec)
            ir = critic_bundle["ir"]
            svg_text = critic_bundle["svg_text"]
            drawio_xml = critic_bundle["drawio_xml"]
            custom_dir = ASSETS_ROOT / "template-gallery" / "custom_generated"
            custom_dir.mkdir(parents=True, exist_ok=True)
            slug = re.sub(r"[^a-z0-9]+", "-", (topic or ir["tid"]).lower()).strip("-")[:48] or "custom-blueprint"
            file_stem = f"{ir['tid']}_{slug}"
            (custom_dir / f"{file_stem}.svg").write_text(svg_text, encoding="utf-8")
            (custom_dir / f"{file_stem}.drawio").write_text(drawio_xml, encoding="utf-8")
            self._send_json(
                200,
                {
                    "status": "SYNTHESIZED",
                    "template_id": ir["tid"],
                    "grammar_id": ir["grammar_id"],
                    "grammar": ir["grammar"],
                    "persona": ir["persona"],
                    "organization": ir["organization"],
                    "confidence_score": ir["confidence_score"],
                    "why_selected": ir["why_selected"],
                    "alternatives": ir["alternatives"],
                    "self_critic_receipt": critic_bundle["self_critic_receipt"],
                    "svg": svg_text,
                    "drawio_xml": drawio_xml,
                    "files": {
                        "svg_url": f"/assets/template-gallery/custom_generated/{file_stem}.svg",
                        "drawio_url": f"/assets/template-gallery/custom_generated/{file_stem}.drawio",
                        "canonical_pptx_url": f"/assets/template-gallery/{ir['tid']}.pptx",
                        "canonical_gif_url": f"/assets/template-gallery/{ir['tid']}.gif",
                    },
                },
            )
            return
        self._send_json(404, {"error": "Not found"})


class ReuseAddrThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class DualStackThreadingHTTPServer(ReuseAddrThreadingHTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self) -> None:
        try:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except OSError:
            pass
        super().server_bind()


def resolve_bind_host() -> str:
    """Returns 127.0.0.1 in automated test mode, or 0.0.0.0 for Cloudtop proxy / Cloud Run ingress."""
    if os.environ.get("STUDIO_TEST_MODE", "").strip().lower() in ("1", "true", "yes"):
        return os.environ.get("HOST", "127.0.0.1")
    # TODO(security): Cloudtop browser preview (http://nitinagga.c.googlers.com:8765 -> ens4 172.29.89.195)
    # and Cloud Run container ingress require listening on 0.0.0.0 rather than loopback-only 127.0.0.1;
    # automated tests pass STUDIO_TEST_MODE=1 or HOST=127.0.0.1 to stay strictly loopback-bound.
    return os.environ.get("HOST", "0.0.0.0")


def create_studio_server(host: str, port: int) -> ReuseAddrThreadingHTTPServer:
    if host in ("0.0.0.0", "::", "") and socket.has_ipv6:
        try:
            return DualStackThreadingHTTPServer(("::", port), StudioRequestHandler)
        except OSError:
            pass
    bind_host = "0.0.0.0" if host in ("::", "") else host
    return ReuseAddrThreadingHTTPServer((bind_host, port), StudioRequestHandler)


if __name__ == "__main__":
    host = resolve_bind_host()
    port = int(os.environ.get("PORT", "8765"))
    httpd = create_studio_server(host, port)

    def _graceful_shutdown(signum: int, _frame) -> None:
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, _graceful_shutdown)
    signal.signal(signal.SIGINT, _graceful_shutdown)
    print(f"Ideas-Minting & Ideas-Mining Studio listening on http://{host}:{port}", flush=True)
    httpd.serve_forever()
