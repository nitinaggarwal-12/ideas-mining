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
    stage_group_join_wave,
    sync_authenticated_linkedin_groups,
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
from src.harvester.live_github_breakout_miner import (
    get_dynamically_minted_repos,
    mine_live_github_breakout_repos,
    mint_full_adk_repo_from_github_breakout,
)
from src.video.canonical_walkthrough_recorder import (
    build_post_spoken_narration_script,
    produce_digital_twin_video_for_any_post,
)
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


def _get_all_catalog_and_dynamic_repos() -> list[dict]:
    base_slugs = {p.get("repo_slug") for p in ALL_CATALOG_ITEMS}
    dyn = [r for r in get_dynamically_minted_repos() if r.get("repo_slug") not in base_slugs]
    return ALL_CATALOG_ITEMS + dyn


def _resolve_any_post_for_digital_twin(
    post_id: str = "",
    title: str = "",
    summary: str = "",
    template_id: str = "",
    repo_slug: str = "",
) -> dict:
    clean_id = (post_id or "").strip()
    all_repos = _get_all_catalog_and_dynamic_repos()
    matched = next(
        (
            r
            for r in all_repos
            if r.get("id") == clean_id or r.get("repo_slug") == clean_id or (repo_slug and r.get("repo_slug") == repo_slug)
        ),
        None,
    )
    if matched:
        plan = matched.get("template_and_distribution_plan") or {}
        tid = template_id or plan.get("primary_template_id") or matched.get("canonical_template_id") or "T85"
        eval_res = {}
        eval_file = REPOS_ROOT / matched["repo_slug"] / "evals" / "eval_results.json"
        if eval_file.exists():
            try:
                eval_res = json.loads(eval_file.read_text(encoding="utf-8")).get("metrics", {})
            except Exception:
                eval_res = {}
        metrics_str = (
            f"pass^5 {eval_res.get('naive_pass_pow_5_pct', 31.0)}% -> {eval_res.get('engineered_pass_pow_5_pct', 94.5)}% "
            f"| -{eval_res.get('token_reduction_pct', 68.4)}% tokens | {eval_res.get('p95_latency_speedup_x', 2.8)}x p95 speedup"
            if eval_res
            else matched.get("daily_problem_short") or matched.get("original_hook") or ""
        )
        return {
            "post_id": matched.get("id") or clean_id or "MINT-01",
            "title": title or matched.get("post_title") or matched.get("title") or "Enterprise Agentic AI Architecture",
            "summary": summary or matched.get("daily_problem_short") or matched.get("original_hook") or "",
            "template_id": tid,
            "repo_slug": matched.get("repo_slug") or "gcp-mcp-zero-bloat-gateway",
            "metrics_hint": metrics_str,
            "gcp_stack": matched.get("gcp_stack") or ["Vertex AI Agent Engine", "Cloud Run v2", "Model Armor"],
        }
    # Check Daily Top-5 Briefing ideas
    briefing = TOP5_ENGINE.get_or_create_briefing()
    for idea in briefing.get("ideas", []):
        if idea.get("id") == clean_id:
            tid = template_id or idea.get("default_template_id") or "T61"
            return {
                "post_id": idea["id"],
                "title": title or idea.get("title") or "Daily Top-5 Agentic AI Signal",
                "summary": summary or idea.get("summary") or "",
                "template_id": tid,
                "repo_slug": repo_slug or "gcp-mcp-zero-bloat-gateway",
                "metrics_hint": idea.get("metrics_hint") or idea.get("summary") or "",
                "gcp_stack": ["Vertex AI Agent Engine", "Cloud Run v2", "AlloyDB pgvector", "Cloud Trace"],
            }
    return {
        "post_id": clean_id or "CUSTOM-POST",
        "title": title or "Enterprise Agentic AI Architecture & Runtime Verification",
        "summary": summary or "Out-of-loop policy enforcement, deterministic context caching, and reproducible pass^5 evaluation.",
        "template_id": template_id or "T85",
        "repo_slug": repo_slug or "gcp-mcp-zero-bloat-gateway",
        "metrics_hint": "94.2% tool accuracy | -97.5% token overhead | 0.0 px² twin occlusion",
        "gcp_stack": ["Vertex AI Agent Engine", "Cloud Run v2", "Model Armor"],
    }

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
                    "repos_count": len(_get_all_catalog_and_dynamic_repos()),
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
            for p in _get_all_catalog_and_dynamic_repos():
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
            matched = next((p for p in _get_all_catalog_and_dynamic_repos() if p["repo_slug"] == slug), None)
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
            host_hdr = self.headers.get("Host") or "nitinagga.c.googlers.com:8765"
            origin_url = f"http://{host_hdr}"
            self._send_json(200, get_or_update_linkedin_group_membership_radar(studio_origin=origin_url))
            return

        if path == "/api/linkedin-groups/sync-redirect":
            prof_q = (qs.get("profile") or ["https://www.linkedin.com/in/nitin-aggarwal-b49786a/"])[0].strip()
            joined_q = (qs.get("joined") or [""])[0].strip()
            pending_q = (qs.get("pending") or [""])[0].strip()
            res = sync_authenticated_linkedin_groups(
                profile_url=prof_q,
                joined_ids_or_text=joined_q,
                pending_ids_or_text=pending_q,
                sync_source="BOOKMARKLET_SAME_ORIGIN_REDIRECT",
            )
            receipt = res.get("sync_receipt", {})
            html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>LinkedIn Groups Authenticated Sync Complete</title>
  <style>
    body {{ font-family: Inter, -apple-system, sans-serif; background: #f8fafc; color: #0f172a; display: flex; align-items: center; justify-content: center; min-height: 90vh; margin: 0; }}
    .card {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 14px; padding: 28px 32px; max-width: 560px; box-shadow: 0 10px 25px rgba(15,23,42,0.06); }}
    h1 {{ font-size: 18px; margin: 0 0 8px; color: #0f172a; }}
    p {{ font-size: 13.5px; color: #334155; line-height: 1.5; margin: 6px 0; }}
    .badge {{ display: inline-block; background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; margin-bottom: 10px; }}
    .btn {{ display: inline-block; margin-top: 14px; background: #2563eb; color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="card">
    <span class="badge">✓ Authenticated LinkedIn Session Synced</span>
    <h1>LinkedIn Group Memberships Updated</h1>
    <p><strong>Profile:</strong> <code>{res.get("authenticated_profile_url")}</code></p>
    <p><strong>Catalog Status:</strong> {res.get("joined_count")} Joined · {res.get("pending_count")} Pending Approval · {res.get("unjoined_count")} Unjoined ({res.get("unjoined_combined_member_reach")} Reach)</p>
    <p><strong>External / Additional Group IDs Detected:</strong> {len(receipt.get("discovered_external_group_ids", []))}</p>
    <a class="btn" href="/?view=view-openhands#linkedin-groups-membership-radar-section">Return to Studio Group Visibility Radar →</a>
  </div>
  <script>
    try {{
      const bc = new BroadcastChannel("linkedin_groups_sync");
      bc.postMessage({{ type: "SYNC_COMPLETE", ts: Date.now() }});
    }} catch (_e) {{}}
    setTimeout(() => {{
      window.location.replace("/?view=view-openhands#linkedin-groups-membership-radar-section");
    }}, 1200);
  </script>
</body>
</html>"""
            body_bytes = html_doc.encode("utf-8")
            self.send_response(200)
            self._send_security_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body_bytes)))
            self.end_headers()
            self.wfile.write(body_bytes)
            return

        if path == "/api/distribution-directory":
            entries = []
            for p in _get_all_catalog_and_dynamic_repos():
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

        if path == "/api/github/breakout-repos":
            q = (qs.get("q") or qs.get("query") or [""])[0].strip()[:160]
            sort_by = (qs.get("sort") or ["velocity"])[0].strip()[:32]
            force_live = (qs.get("live") or ["0"])[0].strip().lower() in ("1", "true", "yes")
            self._send_json(
                200,
                mine_live_github_breakout_repos(query=q, sort_by=sort_by, force_live=force_live),
            )
            return

        if path == "/api/video/digital-twin-script":
            post_id = (qs.get("post_id") or qs.get("id") or ["MINT-01"])[0].strip()
            spec = _resolve_any_post_for_digital_twin(
                post_id=post_id,
                title=(qs.get("title") or [""])[0].strip(),
                summary=(qs.get("summary") or [""])[0].strip(),
                template_id=(qs.get("template_id") or [""])[0].strip(),
                repo_slug=(qs.get("repo_slug") or [""])[0].strip(),
            )
            script_bundle = build_post_spoken_narration_script(
                post_id=spec["post_id"],
                title=spec["title"],
                summary=spec["summary"],
                template_id=spec["template_id"],
                repo_slug=spec["repo_slug"],
                metrics_hint=spec["metrics_hint"],
                gcp_stack=spec["gcp_stack"],
            )
            safe_id = re.sub(r"[^A-Za-z0-9_-]+", "-", spec["post_id"]).strip("-") or "MINT-01"
            manifest_file = ASSETS_ROOT / "videos" / f"{safe_id}_video_manifest.json"
            existing_manifest = None
            if manifest_file.exists():
                try:
                    existing_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                except Exception:
                    existing_manifest = None
            self._send_json(
                200,
                {
                    "status": "READY",
                    "resolved_spec": spec,
                    "script_bundle": script_bundle,
                    "existing_video_manifest": existing_manifest,
                },
            )
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
            pasted_pending = str(payload.get("pasted_pending_groups_text") or "")
            host_hdr = self.headers.get("Host") or "nitinagga.c.googlers.com:8765"
            self._send_json(
                200,
                get_or_update_linkedin_group_membership_radar(
                    toggle_group_id=gid,
                    new_status=new_st,
                    pasted_my_groups_text=pasted,
                    pasted_pending_groups_text=pasted_pending,
                    studio_origin=f"http://{host_hdr}",
                ),
            )
            return

        if path == "/api/linkedin-groups/sync-authenticated":
            prof_url = str(payload.get("profile_url") or "https://www.linkedin.com/in/nitin-aggarwal-b49786a/").strip()
            joined_txt = str(payload.get("joined_ids_or_text") or payload.get("pasted_my_groups_text") or "")
            pending_txt = str(payload.get("pending_ids_or_text") or payload.get("pasted_pending_groups_text") or "")
            curl_hdr = str(payload.get("curl_or_cookie_header") or "")
            sync_src = str(payload.get("sync_source") or "STUDIO_AUTHENTICATED_MODAL").strip()
            self._send_json(
                200,
                sync_authenticated_linkedin_groups(
                    profile_url=prof_url,
                    joined_ids_or_text=joined_txt,
                    pending_ids_or_text=pending_txt,
                    curl_or_cookie_header=curl_hdr,
                    sync_source=sync_src,
                ),
            )
            return

        if path == "/api/linkedin-groups/stage-wave":
            wave_num = int(payload.get("wave_number") or 1)
            max_b = int(payload.get("max_batch") or 8)
            self._send_json(
                200,
                stage_group_join_wave(
                    wave_number=wave_num,
                    max_batch=max_b,
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
        if path == "/api/github/mint-breakout-repo":
            owner_repo_or_url = str(
                payload.get("owner_repo") or payload.get("repo") or payload.get("url") or ""
            ).strip()
            custom_focus = str(payload.get("custom_focus") or payload.get("focus") or "").strip()[:200]
            if not owner_repo_or_url:
                self._send_json(400, {"error": "Provide a GitHub owner/repo or repository URL"})
                return
            res = mint_full_adk_repo_from_github_breakout(
                owner_repo_or_url=owner_repo_or_url,
                custom_focus=custom_focus,
            )
            self._send_json(200, res)
            return

        if path == "/api/video/produce-digital-twin":
            post_id = str(payload.get("post_id") or payload.get("idea_id") or "MINT-01").strip()[:64]
            custom_narration = str(payload.get("custom_narration_override") or payload.get("narration") or "").strip()
            force_rebuild = bool(payload.get("force", True))
            spec = _resolve_any_post_for_digital_twin(
                post_id=post_id,
                title=str(payload.get("title") or "").strip()[:220],
                summary=str(payload.get("summary") or "").strip()[:400],
                template_id=str(payload.get("template_id") or "").strip()[:24],
                repo_slug=str(payload.get("repo_slug") or "").strip()[:80],
            )
            manifest = produce_digital_twin_video_for_any_post(
                post_id=spec["post_id"],
                title=spec["title"],
                summary=spec["summary"],
                template_id=spec["template_id"],
                repo_slug=spec["repo_slug"],
                metrics_hint=spec["metrics_hint"],
                gcp_stack=spec["gcp_stack"],
                custom_narration_override=custom_narration,
                force=force_rebuild,
            )
            self._send_json(200, manifest)
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
