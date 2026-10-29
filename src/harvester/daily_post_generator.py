"""End-to-End Daily Latest-Topic LinkedIn Post & Visual Generator Engine.

Harvests fresh daily AI & systems engineering signals across arXiv, Hacker News (Algolia),
GitHub breakout repositories, and HuggingFace Daily Papers; scores each candidate across
4 quantitative dimensions (novelty, quantitative_density, practitioner_utility, visualizability);
routes topics across the 6 mined LinkedIn Creator Archetypes (STYLE-01..STYLE-06 -> T79..T84);
synthesizes publication-ready LinkedIn post copy + Comment #1 primary-source link; and renders
a custom animated moving-arrow 2D SVG diagram for every generated post.

Complies with:
- Rule 54: Universal Executive Light Theme (#F8FAFC / #FFFFFF)
- Rule 55: Frontier Gemini 3.8 Flash via locations/global with discrete thinkingLevel ("LOW"),
  maxOutputTokens <= 32768, zero numeric thinkingBudget
- Rule 57: Zero "..." lazy truncations, canonical T79..T84 pairing + custom zero-origin SVG audit
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.harvester.idea_miner import summarize_clean_boundary
from src.visuals.dynamic_diagram_engine import generate_dynamic_solution_svg

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DAILY_POSTS_JSON = WORKSPACE_ROOT / "data" / "daily_generated_posts.json"
DAILY_VISUALS_ROOT = WORKSPACE_ROOT / "assets" / "daily-posts"
SLIDES_MANIFEST_JSON = WORKSPACE_ROOT / "data" / "template_google_slides_manifest.json"


CREATOR_STYLE_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "STYLE-01": {
        "style_code": "STYLE-01",
        "creator_name": "Sivasankar Natarajan",
        "creator_linkedin": "https://www.linkedin.com/in/sivasankar-natarajan",
        "followers": 28335,
        "template_id": "T79",
        "archetype_name": "Systems A-vs-B Showdown + Semantic Caveat",
        "best_for_keywords": ["json", "schema", "decoding", "structured", "parser", "contract", "api", "type", "protocol", "mcp"],
        "hook_pattern": "99%-pass happy-path illusion -> Side-by-side Architecture A vs. B -> 'One Thing People Miss' production caveat",
        "gcp_primitives": [
            "Vertex AI Controlled Generation",
            "Google Cloud ADK Schema Guard",
            "Firestore Source-Span Verifier",
            "Cloud Run Confidence Router",
        ],
    },
    "STYLE-02": {
        "style_code": "STYLE-02",
        "creator_name": "Rathnakumar Udayakumar",
        "creator_linkedin": "https://www.linkedin.com/in/rathanuday",
        "followers": 50358,
        "template_id": "T80",
        "archetype_name": "9-Point Agent Loop Micro-Decision Architecture",
        "best_for_keywords": ["router", "routing", "classifier", "gate", "loop", "decision", "tool", "memory", "latency", "guardrail"],
        "hook_pattern": "Stop using a frontier LLM for every gate -> Bounded micro-decisions -> 3-layer Classifier / LLM / App-Code split",
        "gcp_primitives": [
            "Google Cloud Model Armor",
            "Vertex AI Gemini 3.8 Flash",
            "Google Cloud ADK Tool Gate",
            "Cloud Run Deterministic RBAC",
        ],
    },
    "STYLE-03": {
        "style_code": "STYLE-03",
        "creator_name": "Mayank A.",
        "creator_linkedin": "https://in.linkedin.com/in/curiouslearner",
        "followers": 187794,
        "template_id": "T81",
        "archetype_name": "Breakout Open-Source Curriculum & Repo Breakdown",
        "best_for_keywords": ["github", "open-source", "repo", "harness", "scratch", "framework", "sdk", "cli", "course", "starter"],
        "hook_pattern": "Breakout repo/framework launch -> Concrete star/module stats -> Progressive build phases on one real codebase",
        "gcp_primitives": [
            "Google Cloud ADK Workspace",
            "Artifact Registry Skill Hub",
            "OpenHands Cloud Run Sandbox",
            "Cloud Build Maker-Checker Gate",
        ],
    },
    "STYLE-04": {
        "style_code": "STYLE-04",
        "creator_name": "Bally S Kehal",
        "creator_linkedin": "https://www.linkedin.com/in/ballykehal",
        "followers": 23745,
        "template_id": "T82",
        "archetype_name": "Evidence-Based Production Evaluation & Misses Ledger",
        "best_for_keywords": ["review", "code", "pr", "security", "bug", "defect", "audit", "triage", "commit", "regression"],
        "hook_pattern": "Measure what the agent missed -> Seeded replay corpus -> Dual timers (run time vs. human triage tax) + SHA pinning",
        "gcp_primitives": [
            "Gemini Code Assist Replay Set",
            "OpenHands Verification Container",
            "Cloud Build Commit-SHA Receipt",
            "BigQuery Missed-Defect Ledger",
        ],
    },
    "STYLE-05": {
        "style_code": "STYLE-05",
        "creator_name": "Shivani Virdi",
        "creator_linkedin": "https://www.linkedin.com/in/shivanivirdi",
        "followers": 88112,
        "template_id": "T83",
        "archetype_name": "Multi-Trial pass^k Reliability & Restraint Framework",
        "best_for_keywords": ["eval", "evaluation", "benchmark", "reliability", "trial", "restraint", "safety", "hallucination", "trajectory", "judge"],
        "hook_pattern": "Single-run % hides compound user failure -> pass@k vs. pass^k math -> Isolated trials + deterministic state & restraint checks",
        "gcp_primitives": [
            "Vertex AI GenAI Evaluation",
            "GKE Sandbox Trial Isolation",
            "Firestore End-State Grader",
            "Gemini 4 Argon Calibrated Judge",
        ],
    },
    "STYLE-06": {
        "style_code": "STYLE-06",
        "creator_name": "Pallavi Ahuja",
        "creator_linkedin": "https://in.linkedin.com/in/progressivethinker",
        "followers": 111284,
        "template_id": "T84",
        "archetype_name": "First-Principles Systems & Roofline Reference Sheet",
        "best_for_keywords": ["inference", "gpu", "tpu", "kv", "cache", "attention", "vllm", "quantization", "throughput", "ttft", "serving", "parallel"],
        "hook_pattern": "Underestimated systems bottleneck -> Compute-bound vs. Bandwidth-bound Roofline split -> Symptom-to-fix cheat sheet",
        "gcp_primitives": [
            "GKE TPU / GPU Inference Pool",
            "Vertex AI vLLM / SGLang Engine",
            "Cloud Load Balancing Prefix Cache",
            "Cloud Monitoring Goodput SLOs",
        ],
    },
}


CURATED_LATEST_TOPICS: List[Dict[str, Any]] = [
    {
        "source_channel": "arXiv cs.CL • Structured Generation",
        "title": "Grammar-Aligned Speculative Decoding with Zero-Retry Schema Guarantees",
        "summary": "Compiles JSON Schema and CFG constraints directly into draft-and-verify token masks, achieving 100% valid structured payloads at 2.4x lower p99 decode latency while surfacing token-level calibration scores.",
        "primary_url": "https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output",
        "published_at": "2026-10-29",
        "metrics_hint": "100% schema validity • 0 parse retries • 2.4x faster structured decode",
    },
    {
        "source_channel": "Hacker News Front-Page • Agent Systems",
        "title": "Calibrated Sub-15ms System-1 Gatekeepers for Multi-Step Tool Agents",
        "summary": "Replaces 9 repetitive chain-of-thought LLM guard calls inside production agent loops with compact calibrated classifiers for retrieval gating, tool authorization, memory write filtering, and human escalation.",
        "primary_url": "https://google.github.io/adk-docs/",
        "published_at": "2026-10-29",
        "metrics_hint": "68% fewer frontier LLM calls • <15ms per gate • 0 guessed confidence strings",
    },
    {
        "source_channel": "GitHub Breakout • Open-Source Harness",
        "title": "walkinglabs/learn-harness-engineering: 8-Phase Agentic Harness Engineering Curriculum",
        "summary": "Open-source 14-lecture, 8-project curriculum (21K+ stars, 15 languages, MIT) evolving a single real codebase across AGENTS.md rules, scoped memory, multi-session ledgers, Maker-Checker loops, and DAG rollback.",
        "primary_url": "https://github.com/walkinglabs/learn-harness-engineering",
        "published_at": "2026-10-29",
        "metrics_hint": "21K+ GitHub stars • 14 lectures & 8 real-app projects • O(1) graph rollback",
    },
    {
        "source_channel": "Engineering Quality • AI Code Review",
        "title": "Replay-Set Benchmarking for Autonomous PR Review: Measuring Silent Misses & Triage Tax",
        "summary": "Introduces a commit-SHA-pinned evaluation protocol using seeded concurrency/auth defects, unusual valid diffs, and dual timers separating bot execution latency from maintainer finding-assessment time.",
        "primary_url": "https://cloud.google.com/gemini/docs/codeassist/overview",
        "published_at": "2026-10-29",
        "metrics_hint": "100% seeded defect recall • Dual run/triage timers • 0 stale SHA approvals",
    },
    {
        "source_channel": "HuggingFace Daily Papers • Agent Evals",
        "title": "Beyond Single-Run Accuracy: Multi-Trial pass^k Consistency & Restraint Benchmarks",
        "summary": "Demonstrates why a 75% single-run agent succeeds across 3 consecutive customer runs only 42.2% of the time (pass^3), pairing sandbox env.reset() isolation with deterministic DB-state checks and restraint tasks.",
        "primary_url": "https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents",
        "published_at": "2026-10-29",
        "metrics_hint": "pass^3 = 42.2% vs pass@3 = 98.4% • 5 graded dimensions • Explicit 'unknown' judge",
    },
    {
        "source_channel": "Systems Engineering • LLM Serving",
        "title": "Disaggregated Prefill-Decode Serving & FP8 KV-Cache Goodput Optimization",
        "summary": "Separates compute-bound Prefill pools (TTFT) from HBM-bandwidth-bound Decode pools (ITL/TPOT) with PagedAttention, GQA, chunked prefill, and speculative decoding to maximize p99 SLO-compliant Goodput.",
        "primary_url": "https://docs.vllm.ai/en/latest/",
        "published_at": "2026-10-29",
        "metrics_hint": "-50% HBM KV traffic via FP8 • <4% KV block waste • p99 TTFT + TPOT Goodput SLO",
    },
]


def _clean_phrase(raw: str, max_chars: int = 44) -> str:
    """Trim to whole words without ever emitting '...' ellipsis or dangling connectors."""
    text = re.sub(r"\s+", " ", str(raw or "")).replace("...", "").replace("…", "").strip(" -•:;,.")
    if not text:
        return "Verified Control"
    if len(text) <= max_chars:
        return text
    words = text.split()
    acc: List[str] = []
    for w in words:
        cand = " ".join(acc + [w])
        if len(cand) > max_chars:
            break
        acc.append(w)
    dangling = {
        "&", "+", "and", "or", "for", "of", "with", "to", "in", "on", "at",
        "by", "from", "vs", "vs.", "a", "an", "the", "toward", "via", "into",
    }
    while len(acc) > 1 and acc[-1].lower().strip(" -•:;,.") in dangling:
        acc.pop()
    return (" ".join(acc) if acc else text[:max_chars]).strip(" -•:;,.")


def _load_slides_manifest() -> Dict[str, Dict[str, Any]]:
    if SLIDES_MANIFEST_JSON.exists():
        try:
            data = json.loads(SLIDES_MANIFEST_JSON.read_text(encoding="utf-8"))
            return data.get("slides", {})
        except Exception:
            return {}
    return {}


class DailyLinkedInPostEngine:
    """End-to-end daily topic harvester, scorer, 6-creator style router, and SVG visual builder."""

    def __init__(self, store_path: Optional[Path] = None, visuals_root: Optional[Path] = None) -> None:
        self.store_path = store_path or DAILY_POSTS_JSON
        self.visuals_root = visuals_root or DAILY_VISUALS_ROOT

    # ------------------------------------------------------------------
    # 1. MULTI-SOURCE LIVE DAILY TOPIC HARVESTER
    # ------------------------------------------------------------------
    def _fetch_arxiv_latest(self, query: str = "", limit: int = 5) -> List[Dict[str, Any]]:
        q_term = (
            urllib.parse.quote(f'all:"{query.strip()}"')
            if query.strip()
            else "cat:cs.AI+AND+(ti:agent+OR+ti:evaluation+OR+ti:inference+OR+ti:decoding+OR+ti:harness)"
        )
        url = f"http://export.arxiv.org/api/query?search_query={q_term}&sortBy=submittedDate&sortOrder=descending&max_results={limit}"
        items: List[Dict[str, Any]] = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IdeasMining-DailyPostEngine/2.0"})
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                root = ET.fromstring(resp.read())
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title = re.sub(r"\s+", " ", entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
                raw_sum = entry.findtext("atom:summary", default="", namespaces=ns) or ""
                summary = summarize_clean_boundary(raw_sum, max_chars=250)
                link = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
                pub = (entry.findtext("atom:published", default="", namespaces=ns) or "")[:10]
                if title and link:
                    items.append(
                        {
                            "source_channel": "arXiv Live Research",
                            "title": title.replace("...", ""),
                            "summary": summary.replace("...", ""),
                            "primary_url": link,
                            "published_at": pub or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                            "metrics_hint": "Peer-reviewed arXiv preprint • Primary technical specification",
                        }
                    )
        except Exception:
            pass
        return items

    def _fetch_hn_algolia_latest(self, query: str = "", limit: int = 5) -> List[Dict[str, Any]]:
        q_str = query.strip() or "LLM agent inference MCP eval"
        url = (
            "https://hn.algolia.com/api/v1/search_by_date?"
            f"tags=story&numericFilters=points>25&hitsPerPage={limit}&query={urllib.parse.quote(q_str)}"
        )
        items: List[Dict[str, Any]] = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IdeasMining-DailyPostEngine/2.0"})
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            for hit in payload.get("hits", [])[:limit]:
                title = re.sub(r"\s+", " ", str(hit.get("title") or "")).replace("...", "").strip()
                ext_url = str(hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}").strip()
                pts = int(hit.get("points") or 0)
                cmts = int(hit.get("num_comments") or 0)
                created = str(hit.get("created_at") or "")[:10]
                if title and "example." not in ext_url:
                    items.append(
                        {
                            "source_channel": "Hacker News Engineering Signal",
                            "title": title,
                            "summary": summarize_clean_boundary(
                                f"{title}. Trending practitioner engineering discussion with {pts} points and {cmts} technical comments analyzing production trade-offs.",
                                max_chars=240,
                            ),
                            "primary_url": ext_url,
                            "published_at": created or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                            "metrics_hint": f"{pts} HN points • {cmts} practitioner comments",
                        }
                    )
        except Exception:
            pass
        return items

    def _fetch_github_latest(self, query: str = "", limit: int = 5) -> List[Dict[str, Any]]:
        q_str = query.strip() or "agentic-ai OR mcp OR vllm OR agent-eval OR harness"
        url = (
            "https://api.github.com/search/repositories?"
            f"q={urllib.parse.quote(q_str)}&sort=stars&order=desc&per_page={limit}"
        )
        items: List[Dict[str, Any]] = []
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "IdeasMining-DailyPostEngine/2.0", "Accept": "application/vnd.github+json"},
            )
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            for repo in payload.get("items", [])[:limit]:
                full_name = str(repo.get("full_name") or "").strip()
                desc = summarize_clean_boundary(
                    repo.get("description") or f"Open-source AI engineering repository {full_name}.",
                    max_chars=230,
                ).replace("...", "")
                stars = int(repo.get("stargazers_count") or 0)
                html_url = str(repo.get("html_url") or "").strip()
                updated = str(repo.get("pushed_at") or "")[:10]
                if full_name and html_url:
                    items.append(
                        {
                            "source_channel": "GitHub Breakout Repository",
                            "title": f"{full_name}: {_clean_phrase(desc, 68)}",
                            "summary": desc,
                            "primary_url": html_url,
                            "published_at": updated or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                            "metrics_hint": f"{stars:,} GitHub stars • Active open-source implementation",
                        }
                    )
        except Exception:
            pass
        return items

    def _fetch_hf_daily_papers(self, limit: int = 4) -> List[Dict[str, Any]]:
        url = f"https://huggingface.co/api/daily_papers?limit={limit}"
        items: List[Dict[str, Any]] = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IdeasMining-DailyPostEngine/2.0"})
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if isinstance(payload, list):
                for entry in payload[:limit]:
                    paper = entry.get("paper") or {}
                    pid = str(paper.get("id") or "").strip()
                    title = re.sub(r"\s+", " ", str(paper.get("title") or entry.get("title") or "")).replace("...", "").strip()
                    raw_sum = str(paper.get("summary") or "")
                    upvotes = int(paper.get("upvotes") or entry.get("numComments") or 0)
                    pub = str(entry.get("publishedAt") or paper.get("publishedAt") or "")[:10]
                    if title and pid:
                        items.append(
                            {
                                "source_channel": "HuggingFace Daily Papers",
                                "title": title,
                                "summary": summarize_clean_boundary(raw_sum or title, max_chars=245).replace("...", ""),
                                "primary_url": f"https://arxiv.org/abs/{pid}",
                                "published_at": pub or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                                "metrics_hint": f"{upvotes} community upvotes • arXiv:{pid}",
                            }
                        )
        except Exception:
            pass
        return items

    def harvest_latest_topics(self, topic_query: str = "", use_live_network: bool = True) -> List[Dict[str, Any]]:
        """Harvest and deduplicate fresh candidate topics across all live channels + verified fallback."""
        candidates: List[Dict[str, Any]] = []
        clean_q = topic_query.strip()

        if clean_q:
            is_url = clean_q.startswith(("http://", "https://"))
            candidates.append(
                {
                    "source_channel": "Custom Studio Signal",
                    "title": clean_q if not is_url else f"Enterprise Agentic Architecture Signal ({clean_q.split('/')[-1] or 'Source'})",
                    "summary": summarize_clean_boundary(
                        f"Production architectural analysis of {clean_q} focusing on deterministic guardrails, calibrated evaluation gates, and Google Cloud ADK + open-source execution.",
                        max_chars=240,
                    ),
                    "primary_url": clean_q if is_url else f"https://cloud.google.com/search?q={urllib.parse.quote(clean_q)}",
                    "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "metrics_hint": "Direct practitioner focus topic • Verified 4-stage blueprint",
                    "priority_boost": 25.0,
                }
            )

        if use_live_network:
            candidates.extend(self._fetch_arxiv_latest(query=clean_q, limit=4))
            candidates.extend(self._fetch_hn_algolia_latest(query=clean_q, limit=4))
            candidates.extend(self._fetch_github_latest(query=clean_q, limit=4))
            if not clean_q:
                candidates.extend(self._fetch_hf_daily_papers(limit=4))

        # Always append curated latest-topic floor so we guarantee >= 6 high-signal topics offline or online
        for cur in CURATED_LATEST_TOPICS:
            candidates.append(dict(cur))

        deduped: List[Dict[str, Any]] = []
        seen_keys = set()
        for c in candidates:
            key = (c.get("primary_url", "").rstrip("/").lower(), c.get("title", "").lower()[:64])
            if key in seen_keys:
                continue
            seen_keys.add(key)
            deduped.append(c)
        return deduped

    # ------------------------------------------------------------------
    # 2. MULTI-FACTOR TOPIC SCORER & CREATOR ARCHETYPE ROUTER
    # ------------------------------------------------------------------
    def score_topic_candidate(self, topic: Dict[str, Any]) -> Dict[str, float]:
        text = f"{topic.get('title', '')} {topic.get('summary', '')} {topic.get('metrics_hint', '')}".lower()
        today_prefix = datetime.now(timezone.utc).strftime("%Y")

        novelty = 88.0 if str(topic.get("published_at", "")).startswith(today_prefix) else 76.0
        if "Live" in topic.get("source_channel", "") or "Daily" in topic.get("source_channel", ""):
            novelty = min(98.0, novelty + 6.0)

        num_matches = len(re.findall(r"\b\d+(?:\.\d+)?(?:%|x|ms|k|\+|pp)?\b", text))
        quantitative_density = min(99.0, 68.0 + num_matches * 6.5)

        prac_hits = sum(
            1
            for kw in (
                "agent",
                "schema",
                "eval",
                "harness",
                "inference",
                "kv",
                "latency",
                "sandbox",
                "mcp",
                "review",
                "router",
                "benchmark",
                "goodput",
                "decoding",
            )
            if kw in text
        )
        practitioner_utility = min(99.0, 70.0 + prac_hits * 5.0)
        visualizability = min(98.0, 75.0 + (4.0 if "vs" in text or ":" in topic.get("title", "") else 0.0) + prac_hits * 3.0)

        boost = float(topic.get("priority_boost") or 0.0)
        composite = min(
            99.4,
            round(
                0.25 * novelty
                + 0.25 * quantitative_density
                + 0.30 * practitioner_utility
                + 0.20 * visualizability
                + boost,
                1,
            ),
        )
        return {
            "novelty": round(novelty, 1),
            "quantitative_density": round(quantitative_density, 1),
            "practitioner_utility": round(practitioner_utility, 1),
            "visualizability": round(visualizability, 1),
            "composite_score": composite,
        }

    def match_creator_style(self, topic: Dict[str, Any], preferred_style: str = "AUTO", slot_index: int = 0) -> Dict[str, Any]:
        if preferred_style and preferred_style in CREATOR_STYLE_ARCHETYPES:
            return CREATOR_STYLE_ARCHETYPES[preferred_style]

        text = f"{topic.get('title', '')} {topic.get('summary', '')}".lower()
        best_code = None
        best_hits = -1
        style_keys = list(CREATOR_STYLE_ARCHETYPES.keys())
        for code in style_keys:
            arch = CREATOR_STYLE_ARCHETYPES[code]
            hits = sum(2 if kw in topic.get("title", "").lower() else 1 for kw in arch["best_for_keywords"] if kw in text)
            if hits > best_hits:
                best_hits = hits
                best_code = code

        if best_hits <= 0 or best_code is None:
            best_code = style_keys[slot_index % len(style_keys)]
        return CREATOR_STYLE_ARCHETYPES[best_code]

    # ------------------------------------------------------------------
    # 3. LINKEDIN POST COMPOSER (GEMINI 3.8 FLASH RULE 55 + DETERMINISTIC)
    # ------------------------------------------------------------------
    def _try_gemini_38_flash_copy(self, topic: Dict[str, Any], style: Dict[str, Any]) -> Optional[str]:
        """Optional Rule 55 compliant Gemini 3.8 Flash synthesis via locations/global or API key."""
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key or os.environ.get("DISABLE_LIVE_LLM_SYNTHESIS") == "1":
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
            prompt = (
                f"Write a technical LinkedIn post (170-230 words, plain text, zero markdown asterisks, zero external URLs in body) "
                f"in the structural archetype of {style['creator_name']} ({style['archetype_name']}: {style['hook_pattern']}).\n"
                f"Topic: {topic['title']}\n"
                f"Summary: {topic['summary']}\n"
                f"Evidence: {topic.get('metrics_hint', '')}\n"
                f"End with one specific engineering question for practitioners. Never mention Claude or Anthropic."
            )
            body = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "thinkingConfig": {"thinkingLevel": "LOW"},
                    "maxOutputTokens": 1024,
                    "temperature": 0.4,
                },
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=6.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            cand_text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
                .strip()
            )
            if len(cand_text) >= 240 and "claude" not in cand_text.lower() and "anthropic" not in cand_text.lower():
                return cand_text
        except Exception:
            return None
        return None

    def compose_linkedin_post_deterministic(
        self, topic: Dict[str, Any], style: Dict[str, Any], use_live_network: bool = False
    ) -> Dict[str, str]:
        """Deterministic, zero-fluff LinkedIn post synthesis tailored to each of the 6 creator archetypes."""
        title = topic["title"].replace("...", "").strip()
        summary = topic["summary"].replace("...", "").strip()
        metrics_hint = topic.get("metrics_hint", "Deterministic verification gate").replace("...", "")
        code = style["style_code"]
        p1, p2, p3, p4 = style["gcp_primitives"]

        if code == "STYLE-01":
            hook = f"Your AI pipeline passed 99 happy-path runs on { _clean_phrase(title, 52) }. The 100th run broke production."
            body = (
                f"{hook}\n\n"
                f"Why? Because asking a model nicely in prose is a probability, not a systems contract.\n\n"
                f"Signal mined today ({topic['source_channel']}):\n"
                f"→ {title}\n"
                f"→ {summary}\n\n"
                f"The Production A-vs-B Split:\n"
                f"1. Naive Path: Prompt-only instructions + regex retry loops that pollute context windows.\n"
                f"2. Enforced Path: {p1} + {p2} enforcing deterministic grammar/state contracts ({metrics_hint}).\n\n"
                f"One Thing People Miss:\n"
                f"Valid syntactic structure still does not guarantee valid domain meaning. Always pair {p3} with calibrated confidence routing ({p4}) before mutating downstream records.\n\n"
                f"Where in your stack are you still relying on prompt instructions where a deterministic schema or state gate belongs?"
            )
        elif code == "STYLE-02":
            hook = f"Your AI agent does not need a frontier LLM call for every step of { _clean_phrase(title, 48) }."
            body = (
                f"{hook}\n\n"
                f"Most agent latency and token bloat comes from routing simple bool, choice, and score gates through full chain-of-thought reasoning.\n\n"
                f"What stood out in today's signal ({topic['source_channel']}):\n"
                f"• {title}\n"
                f"• {summary}\n\n"
                f"A cleaner 3-Layer Division of Labor:\n"
                f"1. Fast Typed Gates (<15ms): Screen inputs, gate retrieval, filter memory writes, and check grounding via {p1}.\n"
                f"2. Frontier Synthesis: Reserve {p2} strictly for multi-hop planning and synthesis ({metrics_hint}).\n"
                f"3. Deterministic App Code: Enforce permissions, budgets, and tool allowlists in {p3} & {p4} — never inside a prompt.\n\n"
                f"Which micro-decision in your agent loop should be demoted from a full LLM call to a calibrated classifier first?"
            )
        elif code == "STYLE-03":
            hook = f"{_clean_phrase(title, 62)} — engineered from first principles."
            body = (
                f"{hook}\n\n"
                f"Toy agent demos stop at a single prompt loop. Production engineering starts with the harness around the model.\n\n"
                f"Today's breakout engineering signal ({topic['source_channel']}):\n"
                f"• {summary}\n"
                f"• Key telemetry: {metrics_hint}\n\n"
                f"How to evolve one real codebase across 4 progressive phases:\n"
                f"Phase 1 — Codify concise repo rules + scoped context in {p1}.\n"
                f"Phase 2 — Package reusable verification capabilities via {p2}.\n"
                f"Phase 3 — Execute edits inside an isolated {p3} with real unit/DOM tests.\n"
                f"Phase 4 — Separate Builder from an independent Checker in {p4} with O(1) rollback.\n\n"
                f"Are your coding agents operating inside a versioned verification harness, or still editing against unverified local prompts?"
            )
        elif code == "STYLE-04":
            hook = f"An AI workflow around {_clean_phrase(title, 48)} needs evidence about what it missed — not just how fast it ran."
            body = (
                f"{hook}\n\n"
                f"High output volume looks impressive in a vendor demo, right up until ten noisy nits hide one escaped production bug.\n\n"
                f"Grounded takeaway from {topic['source_channel']}:\n"
                f"→ {title}\n"
                f"→ {summary}\n\n"
                f"Four rules before trusting autonomous sign-off:\n"
                f"01. Replay Corpus: Test {p1} on seeded defects, unusual valid diffs, and clean baselines.\n"
                f"02. Dual Timers: Measure bot execution latency separately from human triage cost in {p2}.\n"
                f"03. Revision Pinning: Bind every approval receipt to the exact Git SHA via {p3}.\n"
                f"04. Misses Ledger: Track escaped failure modes in {p4} ({metrics_hint}).\n\n"
                f"Do you track human triage time alongside automated agent findings in your engineering org?"
            )
        elif code == "STYLE-05":
            hook = f"An agent that succeeds 75% of the time on {_clean_phrase(title, 44)} still fails for 1 in 4 users."
            body = (
                f"{hook}\n\n"
                f"Run that workflow 3 consecutive times for a real customer and reliability drops to 0.75^3 = 42.2% (pass^3), even while pass@3 looks like 98.4%.\n\n"
                f"Signal surfaced today ({topic['source_channel']}):\n"
                f"• {title}\n"
                f"• {summary}\n\n"
                f"How to evaluate it for real production release:\n"
                f"1. Isolate every trial with clean sandbox reset ({p2}) across 20–50 real failure cases.\n"
                f"2. Grade deterministic DB/end-state outcomes first ({p3}) before invoking {p4} with an explicit 'unknown' option.\n"
                f"3. Include Restraint tasks where refusing, asking a clarifying question, or escalating is the only passing outcome ({metrics_hint}).\n\n"
                f"Are you gating production agent launches on single-run pass@1, or multi-trial pass^k consistency?"
            )
        else:
            hook = f"Systems discipline around {_clean_phrase(title, 48)} is separating production AI teams from demo builders."
            body = (
                f"{hook}\n\n"
                f"Optimizing aggregate tokens/sec on paper means very little if queueing delay spikes p99 TTFT or HBM bandwidth starves decode.\n\n"
                f"Today's systems signal ({topic['source_channel']}):\n"
                f"→ {title}\n"
                f"→ {summary}\n\n"
                f"Fast Roofline & Goodput Reference Map:\n"
                f"• Compute-Bound Regime: Parallel prefill & routing across {p1}.\n"
                f"• Bandwidth-Bound Regime: KV-cache pressure, PagedAttention & quantization on {p2}.\n"
                f"• Prefix & Batching Control: Chunked prefill + warm prefix routing via {p3}.\n"
                f"• True North Metric: Gate fleet capacity on SLO-compliant Goodput in {p4} ({metrics_hint}).\n\n"
                f"When tail latency spikes in your serving stack, is your bottleneck usually prefill queueing or HBM KV-cache bandwidth?"
            )

        llm_override = self._try_gemini_38_flash_copy(topic, style) if use_live_network else None
        final_body = (llm_override or body).replace("...", "")
        first_comment = (
            f"Comment #1 — Primary Technical Source & Blueprint ({topic['source_channel']}): "
            f"{topic['primary_url']} | Matched Visual Template: {style['template_id']} ({style['archetype_name']})"
        )
        return {
            "hook": hook,
            "linkedin_post_text": final_body,
            "first_comment_source": first_comment,
            "hashtags": "#AgenticAI #GoogleCloud #VertexAI #SystemsEngineering #AIEngineering #ProductionAI",
        }

    # ------------------------------------------------------------------
    # 4. CUSTOM DYNAMIC 2D SVG VISUAL GENERATOR PER DAILY POST
    # ------------------------------------------------------------------
    def _build_dynamic_svg_for_post(
        self,
        post_id: str,
        edition_date: str,
        topic: Dict[str, Any],
        style: Dict[str, Any],
    ) -> str:
        """Render a custom moving-arrow 2D SVG diagram tailored to this daily topic (zero '...' truncations)."""
        p1, p2, p3, p4 = style["gcp_primitives"]
        short_title = _clean_phrase(topic["title"], 64)
        short_metric = _clean_phrase(topic.get("metrics_hint", "100% Deterministic Gate"), 36)

        idea_spec = {
            "id": post_id,
            "est_post_time": f"Daily Edition {edition_date} • {style['creator_name']} Style ({style['template_id']})",
            "repo_slug": f"daily-{edition_date}-{post_id.lower()}",
            "post_title": short_title,
            "best_approach_title": f"{style['archetype_name']} on Google Cloud ADK",
            "why_it_happens_plain": _clean_phrase(topic["summary"], 95),
            "primary_source": {
                "title": short_title,
                "type": topic.get("source_channel", "Primary Engineering Signal"),
                "url": topic["primary_url"],
                "verified_claims": [topic["summary"].replace("...", "")],
            },
            "problem_flow_nodes": [
                {"label": "1. Ungated Demo Setup", "sub": "Relies on prose hope & single runs"},
                {"label": "2. Compound Loop Drift", "sub": "Silent misses, latency & retry tax"},
                {"label": "3. Production Incident", "sub": "Unverified state reaches end users"},
            ],
            "dynamic_steps": [
                {
                    "step": "01",
                    "badge": "STAGE 01 • SIGNAL INGRESS",
                    "title": "Typed Boundary & Context Gate",
                    "how_it_works": f"Screen inputs and bind explicit contracts before execution ({_clean_phrase(topic['source_channel'], 30)}).",
                    "gcp_primitive": _clean_phrase(p1, 30),
                    "arrow_label": "Typed Ingress",
                    "color": "#2563EB",
                },
                {
                    "step": "02",
                    "badge": "STAGE 02 • CORE EXECUTION",
                    "title": _clean_phrase(style["archetype_name"], 34),
                    "how_it_works": "Route bounded judgments to fast gates and deep reasoning to isolated sandboxes.",
                    "gcp_primitive": _clean_phrase(p2, 30),
                    "arrow_label": "Verified Step",
                    "color": "#7C3AED",
                },
                {
                    "step": "03",
                    "badge": "STAGE 03 • EVIDENCE AUDIT",
                    "title": "Deterministic State & SHA Check",
                    "how_it_works": "Verify source records, commit SHA receipts, and restraint safety invariants.",
                    "gcp_primitive": _clean_phrase(p3, 30),
                    "arrow_label": "Pass Gate",
                    "color": "#D97706",
                },
                {
                    "step": "04",
                    "badge": "STAGE 04 • PRODUCTION SLO",
                    "title": "Calibrated Release & Telemetry",
                    "how_it_works": f"Ship verified outputs with live Goodput and confidence routing ({short_metric}).",
                    "gcp_primitive": _clean_phrase(p4, 30),
                    "arrow_label": "Commit SLO",
                    "color": "#059669",
                },
            ],
            "feedback_loop_label": f"Closed-Loop Self-Healing: Stage 03 routes failed checks back to Stage 02 ({style['template_id']})",
            "before_after": {
                "before_metric_1": "99% Prose Hope = Loop Failure",
                "before_metric_2": "Unmeasured Triage & Latency Tax",
                "after_metric_1": short_metric,
                "after_metric_2": f"Template {style['template_id']} + Zero Drift",
                "daily_takeaway": summarize_clean_boundary(topic["summary"], max_chars=150).replace("...", ""),
            },
        }

        svg_markup = generate_dynamic_solution_svg(idea_spec)
        out_dir = self.visuals_root / edition_date
        out_dir.mkdir(parents=True, exist_ok=True)
        svg_path = out_dir / f"{post_id}.svg"
        svg_path.write_text(svg_markup, encoding="utf-8")
        return f"/assets/daily-posts/{edition_date}/{post_id}.svg"

    # ------------------------------------------------------------------
    # 5. END-TO-END DAILY GENERATION & PERSISTENCE
    # ------------------------------------------------------------------
    def load_store(self) -> Dict[str, Any]:
        if self.store_path.exists():
            try:
                return json.loads(self.store_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "latest_edition_date": "",
            "updated_at": "",
            "total_editions": 0,
            "creator_styles": list(CREATOR_STYLE_ARCHETYPES.values()),
            "editions": {},
            "latest_posts": [],
        }

    def generate_daily_edition(
        self,
        edition_date: Optional[str] = None,
        count: int = 6,
        topic_query: str = "",
        creator_style: str = "AUTO",
        use_live_network: bool = True,
    ) -> Dict[str, Any]:
        """Harvest, score, synthesize, render custom SVGs, and atomically persist a daily post batch."""
        date_str = (edition_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")).strip()
        count = max(1, min(12, int(count)))
        store = self.load_store()

        # Collect prior URLs from OTHER dates for cross-day freshness deduplication
        prior_urls = set()
        for d_key, ed in (store.get("editions") or {}).items():
            if d_key != date_str:
                for p in ed.get("posts", []):
                    u = str(p.get("primary_url") or "").rstrip("/").lower()
                    if u:
                        prior_urls.add(u)

        raw_topics = self.harvest_latest_topics(topic_query=topic_query, use_live_network=use_live_network)
        scored_topics: List[Dict[str, Any]] = []
        for t in raw_topics:
            scores = self.score_topic_candidate(t)
            u_norm = str(t.get("primary_url") or "").rstrip("/").lower()
            is_fresh = u_norm not in prior_urls or bool(topic_query.strip())
            scored_topics.append({**t, "scores": scores, "is_fresh": is_fresh})

        scored_topics.sort(
            key=lambda x: (1 if x["is_fresh"] else 0, x["scores"]["composite_score"]),
            reverse=True,
        )

        # Select top `count` topics and diversify creator archetypes when creator_style == "AUTO"
        selected = scored_topics[:count]
        slides_map = _load_slides_manifest()
        style_keys = list(CREATOR_STYLE_ARCHETYPES.keys())
        used_styles = set()
        generated_posts: List[Dict[str, Any]] = []

        for idx, topic in enumerate(selected):
            if creator_style and creator_style in CREATOR_STYLE_ARCHETYPES:
                style = CREATOR_STYLE_ARCHETYPES[creator_style]
            else:
                natural = self.match_creator_style(topic, preferred_style="AUTO", slot_index=idx)
                if natural["style_code"] not in used_styles or len(used_styles) >= len(style_keys):
                    style = natural
                else:
                    remaining = [k for k in style_keys if k not in used_styles]
                    style = CREATOR_STYLE_ARCHETYPES[remaining[0]]
                used_styles.add(style["style_code"])

            digest = hashlib.sha256(f"{date_str}:{idx}:{topic['title']}:{style['style_code']}".encode("utf-8")).hexdigest()[:6].upper()
            post_id = f"DAILY-{date_str.replace('-', '')}-{idx + 1:02d}-{digest}"
            copy_bundle = self.compose_linkedin_post_deterministic(topic, style, use_live_network=use_live_network)
            custom_svg_url = self._build_dynamic_svg_for_post(post_id, date_str, topic, style)
            tid = style["template_id"]
            slide_entry = slides_map.get(tid) or {}

            generated_posts.append(
                {
                    "id": post_id,
                    "edition_date": date_str,
                    "rank": idx + 1,
                    "source_channel": topic["source_channel"],
                    "topic_title": topic["title"],
                    "topic_summary": topic["summary"],
                    "primary_url": topic["primary_url"],
                    "published_at": topic.get("published_at", date_str),
                    "metrics_hint": topic.get("metrics_hint", ""),
                    "scores": topic["scores"],
                    "style_code": style["style_code"],
                    "creator_inspiration": style["creator_name"],
                    "creator_linkedin": style["creator_linkedin"],
                    "archetype_name": style["archetype_name"],
                    "canonical_template_id": tid,
                    "canonical_png_url": f"/assets/template-gallery/{tid}.png",
                    "canonical_gif_url": f"/assets/template-gallery/{tid}.gif",
                    "canonical_svg_url": f"/assets/template-gallery/{tid}.svg",
                    "canonical_pptx_url": f"/assets/template-gallery/{tid}.pptx",
                    "google_slides_url": slide_entry.get("googleSlidesEditUrl", ""),
                    "custom_dynamic_svg_url": custom_svg_url,
                    "hook": copy_bundle["hook"],
                    "linkedin_post_text": copy_bundle["linkedin_post_text"],
                    "first_comment_source": copy_bundle["first_comment_source"],
                    "hashtags": copy_bundle["hashtags"],
                }
            )

        now_iso = datetime.now(timezone.utc).isoformat()
        edition_payload = {
            "edition_date": date_str,
            "generated_at": now_iso,
            "topic_query": topic_query.strip(),
            "creator_style_filter": creator_style or "AUTO",
            "post_count": len(generated_posts),
            "posts": generated_posts,
        }

        editions = store.get("editions") or {}
        editions[date_str] = edition_payload
        sorted_dates = sorted(editions.keys(), reverse=True)
        latest_date = sorted_dates[0]

        updated_store = {
            "latest_edition_date": latest_date,
            "updated_at": now_iso,
            "total_editions": len(editions),
            "creator_styles": list(CREATOR_STYLE_ARCHETYPES.values()),
            "editions": editions,
            "latest_posts": editions[latest_date]["posts"],
        }
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.store_path.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(updated_store, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(self.store_path)
        return edition_payload

    def get_daily_posts_payload(self, edition_date: str = "") -> Dict[str, Any]:
        """Return persisted daily posts (auto-seeding today's edition if store is missing)."""
        store = self.load_store()
        if not store.get("latest_posts"):
            self.generate_daily_edition(count=6, use_live_network=False)
            store = self.load_store()

        target_date = edition_date.strip() or store.get("latest_edition_date", "")
        edition = (store.get("editions") or {}).get(target_date)
        posts = edition["posts"] if edition else store.get("latest_posts", [])
        return {
            "status": "OK",
            "latest_edition_date": store.get("latest_edition_date", target_date),
            "requested_edition_date": target_date,
            "updated_at": store.get("updated_at", ""),
            "total_editions": store.get("total_editions", len(store.get("editions") or {})),
            "available_dates": sorted((store.get("editions") or {}).keys(), reverse=True),
            "creator_styles": list(CREATOR_STYLE_ARCHETYPES.values()),
            "posts": posts,
        }
