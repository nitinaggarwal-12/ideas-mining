"""Step-by-Step Phased Dynamic Flow Diagram & 6-Beat LinkedIn Content Engine (`1080x1350` 4:5 Portrait).

Deconstructs and generalizes the high-converting 4:5 Phased State-Machine Architecture Flow pattern
(exemplified by Brij Kishore Pandey's 7523949736547086336 'Approved Tool. Unapproved Action by AI.'):

1. 6-Beat Step-by-Step Narrative Compiler:
   - Beat 1: Paradoxical 1-Line Failure Hook ("Approved tool -> unapproved action")
   - Beat 2: Concrete 4-Line Artifact A vs. Artifact B Mismatch Scenario
   - Beat 3: The Missing Architectural Question ("Can it call the tool?" vs. "Was THIS action approved?")
   - Beat 4: Out-of-Loop Enforcement Point + 4 Deterministic Temporal / State Rules
   - Beat 5: 3 Built-In Architecture Pillars (Security · Performance · Cost)
   - Beat 6: Closing Litmus Test & 3-Choice Practitioner Debate Question + Comment #1 Link

2. 4:5 Portrait (`1080x1350`) 4-Phase State-Machine Visual Compiler (SVG + Looping GIF89a):
   - Phase 1 (0.00 - 0.25): Mismatch Scanline Sweep + Agent-to-Model Reasoning + Tool Call Ingress
   - Phase 2 (0.25 - 0.50): Gateway Enforcement Point Activation + Trusted Approval Lookup + 4 Sequential Policy Checks
   - Phase 3 (0.50 - 0.75): ALLOW Branch Execution Stream + Session History / Trace Telemetry + 3 Built-In Controls Pulse
   - Phase 4 (0.75 - 1.00): DENY Branch Circuit-Breaker Block ("Action Blocked: No unapproved call is made")

Supports both:
- `light` (Default per Rule 54: Executive Light Blueprint `#F8FAFC` / `#FFFFFF` with crisp slate grid)
- `dark_neon` (High-Contrast Dark Blueprint Grid `#0B1120` matching PRES-05 / Brij Pandey dark-grid aesthetic)
"""

from __future__ import annotations

import hashlib
import html
import subprocess
import tempfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.visuals.canonical_flow_svg import resolve_chrome_bin, resolve_ffmpeg_bin

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
STEP_FLOW_ASSETS_DIR = WORKSPACE_ROOT / "assets" / "step-flows"


STEP_FLOW_PRESETS: Dict[str, Dict[str, Any]] = {
    "FLOW-01": {
        "preset_id": "FLOW-01",
        "name": "Temporal Approval Binding (Approved Tool ≠ Approved Action)",
        "inspiration_urn": "urn:li:activity:7523949736547086336",
        "matched_template_id": "T85",
        "title_line_1": "APPROVED TOOL.",
        "title_line_2": "UNAPPROVED ACTION BY AI.",
        "subtitle": "Bind human approval to the exact artifact & environment that executes.",
        "mismatch_kicker": "THE MISMATCH",
        "approved_label": "HUMAN APPROVED",
        "approved_primary": "Artifact A",
        "approved_secondary": "Environment: staging",
        "requested_label": "AGENT REQUESTED",
        "requested_primary": "Artifact B",
        "requested_secondary": "Environment: production",
        "mismatch_caption": "Tool permission alone cannot detect this parameter swap.",
        "agent_title": "Deployment Agent",
        "agent_sub": "Google Cloud ADK · AgentCore",
        "model_title": "Frontier LLM",
        "model_sub": "Vertex AI Gemini · Bedrock",
        "conduit_label": "Tool call + authenticated identity + policy session",
        "gateway_title": "Policy Gateway",
        "gateway_sub": "ADK BeforeToolCallback · Gateway",
        "gateway_badge": "ENFORCEMENT POINT",
        "policy_kicker": "ENFORCED OUTSIDE THE AGENT",
        "policy_title": "Temporal Policy",
        "policy_sub": "Session-bound state rules",
        "policy_rules": [
            "Artifact matches approval",
            "Environment matches",
            "Approval is still fresh",
            "Approval is unused (1-shot)",
        ],
        "deny_label": "DENY: artifact or environment mismatch",
        "blocked_title": "Action blocked",
        "blocked_sub": "No deployment call is made",
        "approver_title": "Authenticated human approver",
        "approver_note": "Creates cryptographic approval record. The agent only reads its verified status.",
        "approval_svc_title": "Approval service",
        "approval_svc_sub": "Trusted approval lookup",
        "allow_label": "ALLOW: exact approved action",
        "exec_svc_title": "Deployment service",
        "exec_svc_sub": "Execute authorized deployment",
        "exec_side_note": "Service authorization + idempotency key",
        "history_title": "Policy session history",
        "history_sub": "Earlier tool requests & state",
        "trace_title": "Cloud Trace & Audit",
        "trace_sub": "Policy metrics & trace spans",
        "controls": [
            ("SECURITY", "Model Armor PII & prompt shields"),
            ("PERFORMANCE", "Low-latency regional routing"),
            ("COST", "Prefix KV-cache + FinOps tags"),
        ],
        "footer_takeaway": "Approval must match the action that executes.",
        "footer_sub": "Deterministic policy gates run outside the probabilistic reasoning loop.",
        "hook_line_1": "Your AI agent can use an approved tool to perform an unapproved action.",
        "scenario_setup": "A human approves Artifact A for staging. Seconds later, the agent calls deploy(Artifact B, production). Valid identity. Permitted tool. Valid JSON schema. Wrong deployment.",
        "core_question": "“Can this agent call deploy?” leaves the real production question unanswered: “Was THIS artifact approved for THIS environment?”",
        "closing_question": "If an agent changes its parameters after human approval, where does your architecture catch it: inside the agent, at the policy gateway, or inside the downstream service?",
        "primary_url": "https://github.com/nitinaggarwal-12/ideas-mining",
    },
    "FLOW-02": {
        "preset_id": "FLOW-02",
        "name": "Zero-Trust OBO Token Exchange (Confused-Deputy Prevention)",
        "inspiration_urn": "urn:li:activity:7523131357552762882",
        "matched_template_id": "T85",
        "title_line_1": "VALID AGENT IDENTITY.",
        "title_line_2": "UNAUTHORIZED TENANT LEAK.",
        "subtitle": "Exchange narrow-audience OBO tokens on every MCP tool hop.",
        "mismatch_kicker": "THE PRIVILEGE ESCALATION",
        "approved_label": "CALLER SCOPE",
        "approved_primary": "Role: Sales_Reader",
        "approved_secondary": "Tenant: EMEA_Region",
        "requested_label": "AGENT TOOL CALL",
        "requested_primary": "Role: Global_Admin",
        "requested_secondary": "Tenant: All_Payroll_DB",
        "mismatch_caption": "Static service-account keys make the agent a confused deputy.",
        "agent_title": "Enterprise Research Agent",
        "agent_sub": "Google Cloud ADK + MCP Client",
        "model_title": "Reasoning Model",
        "model_sub": "Vertex AI Gemini 3.8 Flash",
        "conduit_label": "MCP tool request + caller OIDC JWT + session context",
        "gateway_title": "Zero-Trust MCP Gateway",
        "gateway_sub": "RFC 8693 Token Exchange · OpenBao",
        "gateway_badge": "OBO ENFORCEMENT POINT",
        "policy_kicker": "ENFORCED AT NETWORK EGRESS",
        "policy_title": "Identity Broker",
        "policy_sub": "Zero secrets in prompts",
        "policy_rules": [
            "Caller OIDC signature verified",
            "Audience narrowed to MCP tool",
            "Tenant matches row-level ACL",
            "Short-lived token (<5m) minted",
        ],
        "deny_label": "DENY: cross-tenant scope violation",
        "blocked_title": "Egress blocked",
        "blocked_sub": "Zero credentials injected",
        "approver_title": "Enterprise Workforce IAM",
        "approver_note": "Issues signed user OIDC identity. Agent never holds raw downstream secrets.",
        "approval_svc_title": "Token Exchange STS",
        "approval_svc_sub": "RFC 8693 OBO attenuation",
        "allow_label": "ALLOW: scoped tenant query",
        "exec_svc_title": "Protected Data API",
        "exec_svc_sub": "Row-level tenant enforcement",
        "exec_side_note": "mTLS workload identity + audit receipt",
        "history_title": "Delegation ledger",
        "history_sub": "Actor -> Agent -> Tool lineage",
        "trace_title": "Security Telemetry",
        "trace_sub": "Per-hop OBO token audit",
        "controls": [
            ("SECURITY", "Zero static API keys in agent env"),
            ("PERFORMANCE", "Sub-8ms local STS token cache"),
            ("COST", "Per-tenant quota & circuit breaker"),
        ],
        "footer_takeaway": "Inject narrow OBO tokens on egress.",
        "footer_sub": "Identity attenuation happens in the gateway — never inside the LLM prompt.",
        "hook_line_1": "If your AI agent authenticates to tools with a shared service account, every prompt is one hop from a cross-tenant breach.",
        "scenario_setup": "An EMEA sales rep asks the agent for Q4 pipeline metrics. A poisoned document tricks the agent into querying Global_Payroll_DB. Because the agent uses a static service key, the database says yes.",
        "core_question": "“Is the agent authenticated?” is the wrong question. The right question is: “Does this specific tool call carry the caller's attenuated tenant scope?”",
        "closing_question": "How do your MCP servers verify who initiated the request: shared API keys, pass-through headers, or RFC 8693 On-Behalf-Of token exchange?",
        "primary_url": "https://github.com/nitinaggarwal-12/ideas-mining",
    },
    "FLOW-03": {
        "preset_id": "FLOW-03",
        "name": "Orthogonal Pre-Completion Sandbox Verification (Maker ≠ Checker)",
        "inspiration_urn": "urn:li:activity:7521164027662721024",
        "matched_template_id": "T82",
        "title_line_1": "CONFIDENT AGENT SUMMARY.",
        "title_line_2": "BROKEN PRODUCTION BUILD.",
        "subtitle": "Gate autonomous code commits on deterministic sandbox execution.",
        "mismatch_kicker": "THE SELF-GRADING ILLUSION",
        "approved_label": "AGENT SELF-REPORT",
        "approved_primary": "“All tests pass!”",
        "approved_secondary": "Confidence: 99% (Unrun)",
        "requested_label": "SANDBOX REALITY",
        "requested_primary": "2 Failing Tests",
        "requested_secondary": "ImportError in auth.py",
        "mismatch_caption": "LLMs grade plausibility of prose, not runtime execution.",
        "agent_title": "Autonomous Coding Agent",
        "agent_sub": "OpenHands / ADK Code Writer",
        "model_title": "Generator Model",
        "model_sub": "Long-horizon patch synthesis",
        "conduit_label": "Candidate git diff + proposed completion signal",
        "gateway_title": "Verify Gate",
        "gateway_sub": "gVisor Sandbox · Orthogonal Judge",
        "gateway_badge": "COMMIT ENFORCEMENT",
        "policy_kicker": "ENFORCED BEFORE PR CREATION",
        "policy_title": "Verify Harness",
        "policy_sub": "Zero self-certified runs",
        "policy_rules": [
            "AST syntax & build = PASS",
            "Unit + regression suite = 100%",
            "SAST & secret scan = 0 hits",
            "Judge != Generator model",
        ],
        "deny_label": "DENY: failing test or SAST hit",
        "blocked_title": "Commit rejected",
        "blocked_sub": "Stderr fed back for repair",
        "approver_title": "Golden Replay Corpus",
        "approver_note": "Pinned commit SHAs and seeded defects measure what the agent missed.",
        "approval_svc_title": "gVisor Sandbox",
        "approval_svc_sub": "Isolated test runner",
        "allow_label": "ALLOW: verified green diff",
        "exec_svc_title": "GitHub / Critique PR",
        "exec_svc_sub": "Signed SHA verification receipt",
        "exec_side_note": "Idempotent commit + test log artifact",
        "history_title": "Trajectory repair log",
        "history_sub": "Attempt #1..#N stderr diffs",
        "trace_title": "Pass^k Telemetry",
        "trace_sub": "Multi-trial consistency score",
        "controls": [
            ("SECURITY", "Air-gapped gVisor container"),
            ("PERFORMANCE", "Incremental test selection (<12s)"),
            ("COST", "Halt identical tool failures at N=2"),
        ],
        "footer_takeaway": "Prose is not a test receipt. Verify outside the loop.",
        "footer_sub": "Separate the Maker model from the deterministic Checker harness.",
        "hook_line_1": "The most dangerous sentence in autonomous software engineering is an LLM saying: “I have verified that all tests pass.”",
        "scenario_setup": "A coding agent edits 6 files, writes a polished PR summary, and declares victory — without ever running pytest on the final diff.",
        "core_question": "“Did the agent explain its fix?” is irrelevant if the pre-completion hook never executed the test binary in an isolated sandbox.",
        "closing_question": "In your coding agent workflow, what blocks a broken diff from reaching human review: prompt instructions, or a hard pre-completion sandbox gate?",
        "primary_url": "https://github.com/nitinaggarwal-12/ideas-mining",
    },
}


def _esc(val: Any) -> str:
    return html.escape("" if val is None else str(val), quote=True)


def _wrap(text: str, width: int, max_lines: int = 2) -> List[str]:
    clean = " ".join(str(text or "").split())
    if not clean:
        return [""]
    lines = textwrap.wrap(clean, width=max(10, width))
    return lines[:max_lines] if lines else [clean[:width]]


def build_step_flow_spec_from_topic(
    preset_id: str = "FLOW-01",
    custom_topic: str = "",
) -> Dict[str, Any]:
    """Return a preset spec or adapt it dynamically to a user-provided engineering topic."""
    base = dict(STEP_FLOW_PRESETS.get(preset_id) or STEP_FLOW_PRESETS["FLOW-01"])
    topic = " ".join(str(custom_topic or "").split()).strip()
    if not topic:
        return base

    # Adapt headline & scenario cleanly when user supplies a custom topic
    words = [w for w in topic.replace("—", " ").replace(":", " ").split() if len(w) > 2]
    key_phrase = " ".join(words[:4]).upper() if words else "AGENT WORKFLOW"
    base["name"] = f"Dynamic Step-by-Step Flow: {topic[:72]}"
    base["title_line_1"] = f"APPROVED {key_phrase[:22]}."
    base["title_line_2"] = "UNVERIFIED RUNTIME EXECUTION."
    base["subtitle"] = f"Enforce deterministic out-of-loop policy checks for: {topic[:68]}"
    base["hook_line_1"] = f"Why most production teams get burned by {topic[:70]}: checking permission without verifying runtime state."
    base["scenario_setup"] = (
        f"In a standard implementation of {topic[:65]}, the agent passes static schema validation "
        f"on Step 1, then mutates target parameters on Step 2 without re-verifying authorization."
    )
    base["footer_takeaway"] = f"Out-of-loop policy gates make {words[0] if words else 'agent'} execution deterministic."
    return base


def compile_step_by_step_linkedin_post(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Compile the 6-Beat Step-by-Step LinkedIn Post Copy + Comment #1 Link (Brij / Posta / Rathi pattern)."""
    rules_bullets = "\n".join(f"• {r}" for r in spec["policy_rules"])
    controls_bullets = "\n".join(f"• {k.title()}: {v}" for k, v in spec["controls"])

    body = (
        f"{spec['hook_line_1']}\n"
        f"That is the failure mode I put at the top of every production architecture review.\n\n"
        f"Consider how this happens in practice:\n"
        f"{spec['scenario_setup']}\n\n"
        f"Coming from systems engineering, I care about what happens between those hops.\n"
        f"{spec['core_question']}\n\n"
        f"A human or policy approval must remain cryptographically bound to the exact action it authorized.\n\n"
        f"In this step-by-step architecture ({spec['gateway_title']}), enforcement runs strictly outside the agent's reasoning loop:\n\n"
        f"1️⃣ Step 1 — Detect the Mismatch Early\n"
        f"Compare {spec['approved_label']} ({spec['approved_primary']} · {spec['approved_secondary']}) against {spec['requested_label']} ({spec['requested_primary']} · {spec['requested_secondary']}).\n\n"
        f"2️⃣ Step 2 — Enforce 4 Temporal Rules at the Gateway ({spec['gateway_badge']})\n"
        f"{rules_bullets}\n\n"
        f"3️⃣ Step 3 — Deterministic ALLOW vs. DENY Routing\n"
        f"• If any check fails → {spec['blocked_title']} ({spec['blocked_sub']}).\n"
        f"• If all 4 pass → {spec['exec_svc_title']} ({spec['exec_svc_sub']}) with {spec['exec_side_note']}.\n\n"
        f"4️⃣ Step 4 — Apply Built-In Controls Across the Stack\n"
        f"{controls_bullets}\n\n"
        f"Golden Rule: {spec['footer_takeaway']}\n\n"
        f"{spec['closing_question']}\n\n"
        f"#AgenticAI #SystemDesign #GoogleCloud #AIArchitecture #SecurityEngineering"
    )
    comment_1 = (
        f"Interactive 4:5 step-by-step blueprint ({spec['matched_template_id']}) & reference implementation: "
        f"{spec.get('primary_url', 'https://github.com/nitinaggarwal-12/ideas-mining')}"
    )
    return {
        "post_copy": body,
        "char_count": len(body),
        "line_count": len(body.splitlines()),
        "comment_1": comment_1,
        "beats": [
            {"beat": "1. Paradoxical Failure Hook", "text": spec["hook_line_1"]},
            {"beat": "2. Concrete Mismatch Scenario", "text": spec["scenario_setup"]},
            {"beat": "3. Core Architectural Question", "text": spec["core_question"]},
            {"beat": "4. Out-of-Loop 4-Rule Policy Gate", "text": " · ".join(spec["policy_rules"])},
            {"beat": "5. Built-In 3-Pillar Controls", "text": " | ".join(f"{k}: {v}" for k, v in spec["controls"])},
            {"beat": "6. Closing Litmus Test CTA", "text": spec["closing_question"]},
        ],
    }


def build_serial_parallel_execution_trace(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Build a millisecond-accurate End-to-End Serial & Parallel Execution DAG + Waterfall Trace (`0ms..320ms`).

    Explicitly models:
    - WHERE each hop executes (Component / Service boundary)
    - WHEN it starts and ends (`start_ms`, `end_ms`, `duration_ms`)
    - WHETHER it runs in `SERIAL` sequence or `PARALLEL` fan-out (`fork_group` + `barrier_join_ms`)
    - WHAT exact payload / policy state is inspected or mutated at that millisecond
    """
    rules = spec.get("policy_rules") or []
    return {
        "total_duration_ms": 320,
        "serial_equivalent_ms": 408,
        "parallel_speedup_label": "2.8× faster gate (30ms parallel fan-out vs. 88ms serial)",
        "barrier_join_ms": 165,
        "spans": [
            {
                "span_id": "S1",
                "order": "Step 1",
                "mode": "SERIAL",
                "lane": "1. Human / IdP Trust Root",
                "where": f"{spec['approver_title']} → {spec['approval_svc_title']}",
                "start_ms": 0,
                "end_ms": 45,
                "duration_ms": 45,
                "color": "#2563EB",
                "what": f"Mint signed approval record: ({spec['approved_primary']} · {spec['approved_secondary']}, nonce=1-shot)",
                "payload_allow": f'{{"approved_item": "{spec["approved_primary"]}", "scope": "{spec["approved_secondary"]}", "ttl_s": 300, "used": false}}',
                "payload_deny": f'{{"approved_item": "{spec["approved_primary"]}", "scope": "{spec["approved_secondary"]}", "ttl_s": 300, "used": false}}',
            },
            {
                "span_id": "S2",
                "order": "Step 2",
                "mode": "SERIAL",
                "lane": "2. Agent ⇄ LLM Reasoning",
                "where": f"{spec['agent_title']} ⇄ {spec['model_title']}",
                "start_ms": 45,
                "end_ms": 115,
                "duration_ms": 70,
                "color": "#0D9488",
                "what": "Synthesize tool call + attach caller identity & session context",
                "payload_allow": f'{{"tool": "execute_action", "target": "{spec["approved_primary"]}", "ctx": "{spec["approved_secondary"]}"}}',
                "payload_deny": f'{{"tool": "execute_action", "target": "{spec["requested_primary"]}", "ctx": "{spec["requested_secondary"]}", "warning": "PARAMETER_SWAP"}}',
            },
            {
                "span_id": "S3",
                "order": "Step 3",
                "mode": "SERIAL",
                "lane": "3. Gateway Intercept",
                "where": f"{spec['agent_title']} → {spec['gateway_title']} ({spec['gateway_badge']})",
                "start_ms": 115,
                "end_ms": 135,
                "duration_ms": 20,
                "color": "#D97706",
                "what": "Hold tool call at out-of-loop enforcement point; fork 4 parallel verification lanes",
                "payload_allow": '{"gateway_state": "HOLD_FOR_PARALLEL_VERIFY", "fork_lanes": 4, "barrier": "ALL_MUST_PASS"}',
                "payload_deny": '{"gateway_state": "HOLD_FOR_PARALLEL_VERIFY", "fork_lanes": 4, "barrier": "ALL_MUST_PASS"}',
            },
            {
                "span_id": "P4A",
                "order": "Step 4A ∥",
                "mode": "PARALLEL",
                "fork_group": "GATEWAY_FANOUT_4",
                "lane": "4A. Trusted Approval Lookup",
                "where": f"{spec['gateway_title']} ⇉ {spec['approval_svc_title']}",
                "start_ms": 135,
                "end_ms": 153,
                "duration_ms": 18,
                "color": "#2563EB",
                "what": f"Parallel Lane 1: Read verified approval status ({rules[0] if rules else 'Digest check'})",
                "payload_allow": f'{{"lookup": "FOUND", "expected": "{spec["approved_primary"]}", "actual": "{spec["approved_primary"]}", "match": true}}',
                "payload_deny": f'{{"lookup": "FOUND", "expected": "{spec["approved_primary"]}", "actual": "{spec["requested_primary"]}", "match": false}}',
            },
            {
                "span_id": "P4B",
                "order": "Step 4B ∥",
                "mode": "PARALLEL",
                "fork_group": "GATEWAY_FANOUT_4",
                "lane": "4B. 4-Rule Temporal Policy",
                "where": f"{spec['gateway_title']} ⇉ {spec['policy_title']}",
                "start_ms": 135,
                "end_ms": 159,
                "duration_ms": 24,
                "color": "#059669",
                "what": "Parallel Lane 2: Evaluate all 4 session-bound state rules outside agent loop",
                "payload_allow": '{"rule_1_digest": "PASS", "rule_2_env": "PASS", "rule_3_fresh": "PASS", "rule_4_unused": "PASS"}',
                "payload_deny": '{"rule_1_digest": "FAIL_MISMATCH", "rule_2_env": "FAIL_MISMATCH", "rule_3_fresh": "PASS", "rule_4_unused": "PASS"}',
            },
            {
                "span_id": "P4C",
                "order": "Step 4C ∥",
                "mode": "PARALLEL",
                "fork_group": "GATEWAY_FANOUT_4",
                "lane": "4C. Security & Guardrails",
                "where": f"{spec['gateway_title']} ⇉ Built-In Security Control",
                "start_ms": 135,
                "end_ms": 165,
                "duration_ms": 30,
                "color": "#DC2626",
                "what": f"Parallel Lane 3: {spec['controls'][0][1]}",
                "payload_allow": '{"pii_redaction": "CLEAN", "prompt_shield": "NO_INJECTION", "latency_ms": 30}',
                "payload_deny": '{"parameter_tamper_alert": "HIGH_SEVERITY", "blocked_before_egress": true}',
            },
            {
                "span_id": "P4D",
                "order": "Step 4D ∥",
                "mode": "PARALLEL",
                "fork_group": "GATEWAY_FANOUT_4",
                "lane": "4D. Session State Ledger",
                "where": f"{spec['gateway_title']} ⇉ {spec['history_title']}",
                "start_ms": 135,
                "end_ms": 151,
                "duration_ms": 16,
                "color": "#7C3AED",
                "what": f"Parallel Lane 4: Record tool call attempt in {spec['history_title']}",
                "payload_allow": '{"session_seq": 4, "replay_protection": "NONCE_LOCKED", "state": "COMMITTED"}',
                "payload_deny": '{"session_seq": 4, "violation_logged": "PARAMETER_SWAP_ATTEMPT", "state": "ABORTED"}',
            },
            {
                "span_id": "S5",
                "order": "Step 5 (Join)",
                "mode": "SERIAL",
                "lane": "5. Barrier Join → Execution / Block",
                "where": f"{spec['gateway_title']} → {spec['exec_svc_title']} | {spec['blocked_title']}",
                "start_ms": 165,
                "end_ms": 265,
                "duration_ms": 100,
                "color": "#059669",
                "what": f"Barrier Join @ 165ms: Route ALLOW to {spec['exec_svc_title']} or circuit-break DENY to {spec['blocked_title']}",
                "payload_allow": f'{{"decision": "ALLOW", "service": "{spec["exec_svc_title"]}", "status": "200_EXECUTED_EXACT_MATCH"}}',
                "payload_deny": f'{{"decision": "DENY", "action": "{spec["blocked_title"]}", "downstream_calls_made": 0}}',
            },
            {
                "span_id": "P6",
                "order": "Step 6 ∥",
                "mode": "PARALLEL",
                "fork_group": "POST_DECISION_ASYNC",
                "lane": "6. Async Trace & FinOps Stream",
                "where": f"{spec['gateway_title']} ⇉ {spec['trace_title']}",
                "start_ms": 165,
                "end_ms": 320,
                "duration_ms": 155,
                "color": "#DB2777",
                "what": f"Async Parallel Stream: Emit OpenTelemetry spans + {spec['controls'][2][1]}",
                "payload_allow": '{"otel_trace": "EXPORTED", "kv_cache_hit": true, "finops_cost_usd": 0.00042}',
                "payload_deny": '{"otel_trace": "SECURITY_AUDIT_SPAN", "prevented_prod_incident": true}',
            },
        ],
    }


def generate_step_by_step_flow_svg(
    spec: Dict[str, Any],
    theme: str = "light",
    frame_phase: Optional[float] = None,
) -> str:
    """Render a 1080x1350 (4:5 Portrait) 4-Phase Step-by-Step Dynamic Flow SVG.

    - When `frame_phase is None`: embeds smooth CSS/SMIL animations across all 4 phases for instant live UI playback.
    - When `frame_phase` is float in `[0.0, 1.0)`: renders deterministic keyframe state for FFmpeg GIF89a/MP4 compilation.
    """
    is_dark = str(theme or "light").lower() in ("dark", "dark_neon", "brij")
    if is_dark:
        bg = "#0B1120"
        grid_line = "#1E293B"
        card_bg = "#131C2E"
        card_bg_alt = "#0F172A"
        card_border = "#334155"
        text_main = "#F8FAFC"
        text_sub = "#94A3B8"
        text_muted = "#64748B"
        amber = "#F59E0B"
        emerald = "#10B981"
        rose = "#EF4444"
        cyan = "#14B8A6"
        purple = "#A855F7"
        pink = "#EC4899"
        blue = "#3B82F6"
        footer_bar_bg = "#0F172A"
    else:
        # Rule 54 Executive Light Theme Default (#F8FAFC / #FFFFFF)
        bg = "#F8FAFC"
        grid_line = "#E2E8F0"
        card_bg = "#FFFFFF"
        card_bg_alt = "#F1F5F9"
        card_border = "#CBD5E1"
        text_main = "#0F172A"
        text_sub = "#334155"
        text_muted = "#475569"
        amber = "#D97706"
        emerald = "#059669"
        rose = "#DC2626"
        cyan = "#0D9488"
        purple = "#7C3AED"
        pink = "#DB2777"
        blue = "#1E40AF"
        footer_bar_bg = "#FFFFFF"

    # Determine active phase (0..3) when rendering discrete frames for GIF
    # Phase 0: [0.00, 0.25) Mismatch Scan + Agent Call
    # Phase 1: [0.25, 0.50) Gateway Enforcement + Approval Lookup + 4 Policy Checks
    # Phase 2: [0.50, 0.75) ALLOW Execution Stream + Session History / Trace + Controls
    # Phase 3: [0.75, 1.00) DENY Branch Block + Mismatch Stamp
    p_val = 0.0 if frame_phase is None else (float(frame_phase) % 1.0)
    active_phase = int(p_val * 4.0) if frame_phase is not None else -1
    sub_t = (p_val * 4.0) - active_phase if frame_phase is not None else 0.5

    dash_offset = 0.0 if frame_phase is None else -p_val * 64.0

    out: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">',
        "<defs>",
        f'  <pattern id="bgGrid" width="36" height="36" patternUnits="userSpaceOnUse">'
        f'<path d="M 36 0 L 0 0 0 36" fill="none" stroke="{grid_line}" stroke-width="1" stroke-opacity="0.65"/></pattern>',
        '  <filter id="glowAmber" x="-15%" y="-15%" width="130%" height="130%">'
        '<feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="#F59E0B" flood-opacity="0.28"/></filter>',
        '  <filter id="glowEmerald" x="-15%" y="-15%" width="130%" height="130%">'
        '<feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="#10B981" flood-opacity="0.28"/></filter>',
        '  <filter id="glowRose" x="-15%" y="-15%" width="130%" height="130%">'
        '<feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="#EF4444" flood-opacity="0.28"/></filter>',
        "  <style>",
        "    @keyframes flowDash { from { stroke-dashoffset: 48; } to { stroke-dashoffset: 0; } }",
        "    @keyframes scanSweep { 0%, 100% { transform: translateX(0px); opacity: 0.85; } 50% { transform: translateX(132px); opacity: 0.95; } }",
        "    @keyframes pulseAllow { 0%, 45%, 100% { opacity: 0.28; } 55%, 80% { opacity: 1.0; } }",
        "    @keyframes pulseDeny { 0%, 70%, 100% { opacity: 0.32; } 78%, 96% { opacity: 1.0; } }",
        "    @keyframes checkPop1 { 0%, 20% { opacity: 0.35; } 28%, 100% { opacity: 1; } }",
        "    @keyframes checkPop2 { 0%, 30% { opacity: 0.35; } 38%, 100% { opacity: 1; } }",
        "    @keyframes checkPop3 { 0%, 40% { opacity: 0.35; } 48%, 100% { opacity: 1; } }",
        "    @keyframes checkPop4 { 0%, 50% { opacity: 0.35; } 58%, 100% { opacity: 1; } }",
        "    .anim-dash { animation: flowDash 1.4s linear infinite; }",
        "    .scan-bar { animation: scanSweep 3.2s ease-in-out infinite; }",
        "    .allow-stream { animation: pulseAllow 6s ease-in-out infinite; }",
        "    .deny-stream { animation: pulseDeny 6s ease-in-out infinite; }",
        "    .chk-1 { animation: checkPop1 6s ease-in-out infinite; }",
        "    .chk-2 { animation: checkPop2 6s ease-in-out infinite; }",
        "    .chk-3 { animation: checkPop3 6s ease-in-out infinite; }",
        "    .chk-4 { animation: checkPop4 6s ease-in-out infinite; }",
        "  </style>",
        "</defs>",
        f'<rect width="1080" height="1350" fill="{bg}"/>',
        '<rect width="1080" height="1350" fill="url(#bgGrid)"/>',
    ]

    # --- ZONE 1: HEADER (y=36..172) ---
    out.extend(
        [
            f'<rect x="36" y="28" width="248" height="26" rx="13" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>',
            f'<circle cx="52" cy="41" r="5" fill="{emerald}"/>',
            f'<text x="66" y="45" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="{text_sub}">STEP-BY-STEP FLOW · {spec["matched_template_id"]}</text>',
            # Role-Label Attribution Pill (Rule 53: 0 personal names on generated blueprints)
            f'<rect x="688" y="28" width="356" height="28" rx="14" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>',
            f'<text x="866" y="46" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="{blue if not is_dark else amber}" text-anchor="middle">Google Cloud Agentic Architecture Engineering</text>',
            f'<text x="36" y="96" font-family="Inter, sans-serif" font-size="44" font-weight="900" fill="{text_main}" letter-spacing="-0.8">{_esc(spec["title_line_1"])}</text>',
            f'<text x="36" y="144" font-family="Inter, sans-serif" font-size="42" font-weight="900" fill="{amber}" letter-spacing="-0.6">{_esc(spec["title_line_2"])}</text>',
            f'<text x="36" y="176" font-family="Inter, sans-serif" font-size="19" font-weight="600" fill="{text_sub}">{_esc(spec["subtitle"])}</text>',
        ]
    )

    # Phase Progress Indicator Pill Bar (y=192..220)
    phase_labels = [
        "Phase 1: Mismatch & Call",
        "Phase 2: Gateway & 4 Rules",
        "Phase 3: Verified ALLOW",
        "Phase 4: Circuit-Breaker DENY",
    ]
    for p_idx, p_lbl in enumerate(phase_labels):
        px = 36 + p_idx * 254
        is_p_act = (active_phase == p_idx) or (frame_phase is None and p_idx == 1)
        p_stroke = amber if is_p_act else card_border
        p_fill = (amber if is_dark else "#FEF3C7") if is_p_act else card_bg
        p_txt = ("#0F172A" if is_p_act else text_sub)
        out.extend(
            [
                f'<rect x="{px}" y="192" width="242" height="26" rx="13" fill="{p_fill}" stroke="{p_stroke}" stroke-width="{2.0 if is_p_act else 1.2}"/>',
                f'<text x="{px + 121}" y="209" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="{p_txt}" text-anchor="middle">{_esc(p_lbl)}</text>',
            ]
        )

    # --- ZONE 2: UPPER-LEFT "THE MISMATCH" BOX (x=36..396, y=236..512) ---
    mismatch_border = rose if active_phase == 3 else card_border
    out.extend(
        [
            f'<rect x="36" y="236" width="360" height="276" rx="14" fill="{card_bg_alt}" stroke="{mismatch_border}" stroke-width="1.8" stroke-dasharray="6 4"/>',
            f'<text x="54" y="262" font-family="Inter, sans-serif" font-size="12.5" font-weight="900" fill="{amber}" letter-spacing="0.6">{_esc(spec["mismatch_kicker"])}</text>',
            # Left Sub-card: Approved (Emerald)
            f'<rect x="52" y="276" width="150" height="148" rx="10" fill="{card_bg}" stroke="{emerald}" stroke-width="2.2"/>',
            f'<circle cx="72" cy="300" r="10" fill="{emerald}" fill-opacity="0.18"/>',
            f'<text x="72" y="304" font-family="Inter, sans-serif" font-size="11" font-weight="900" fill="{emerald}" text-anchor="middle">✓</text>',
            f'<text x="64" y="328" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="{emerald}">{_esc(spec["approved_label"])}</text>',
            f'<text x="64" y="354" font-family="Inter, sans-serif" font-size="18" font-weight="900" fill="{text_main}">{_esc(spec["approved_primary"])}</text>',
            f'<text x="64" y="380" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">{_esc(spec["approved_secondary"].split(":")[0])}:</text>',
            f'<text x="64" y="398" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="{text_main}">{_esc(spec["approved_secondary"].split(":")[-1].strip())}</text>',
            # Right Sub-card: Requested (Rose)
            f'<rect x="230" y="276" width="150" height="148" rx="10" fill="{card_bg}" stroke="{rose}" stroke-width="2.2"/>',
            f'<circle cx="250" cy="300" r="10" fill="{rose}" fill-opacity="0.18"/>',
            f'<text x="250" y="304" font-family="Inter, sans-serif" font-size="11" font-weight="900" fill="{rose}" text-anchor="middle">!</text>',
            f'<text x="242" y="328" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="{rose}">{_esc(spec["requested_label"])}</text>',
            f'<text x="242" y="354" font-family="Inter, sans-serif" font-size="18" font-weight="900" fill="{text_main}">{_esc(spec["requested_primary"])}</text>',
            f'<text x="242" y="380" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">{_esc(spec["requested_secondary"].split(":")[0])}:</text>',
            f'<text x="242" y="398" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="{text_main}">{_esc(spec["requested_secondary"].split(":")[-1].strip())}</text>',
            # Center != badge
            f'<circle cx="216" cy="350" r="15" fill="{rose}"/>',
            '<text x="216" y="356" font-family="Inter, sans-serif" font-size="18" font-weight="900" fill="#FFFFFF" text-anchor="middle">≠</text>',
        ]
    )

    # Scanline in Phase 0 or interactive SVG
    if frame_phase is None:
        out.append(
            f'<rect class="scan-bar" x="58" y="278" width="4" height="144" fill="{cyan}" fill-opacity="0.75"/>'
        )
    elif active_phase == 0:
        scan_x = 60 + sub_t * 130.0
        out.extend(
            [
                f'<rect x="{scan_x - 16:.1f}" y="278" width="18" height="144" fill="{emerald}" fill-opacity="0.18"/>',
                f'<rect x="{scan_x:.1f}" y="278" width="3.5" height="144" fill="#FFFFFF"/>',
            ]
        )

    mm_lines = _wrap(spec["mismatch_caption"], width=36, max_lines=2)
    for m_i, ml in enumerate(mm_lines):
        out.append(
            f'<text x="54" y="{452 + m_i * 20}" font-family="Inter, sans-serif" font-size="14" font-weight="800" fill="{text_main}">{_esc(ml)}</text>'
        )

    if active_phase in (2, 3) or frame_phase is None:
        out.extend(
            [
                f'<rect x="268" y="468" width="110" height="28" rx="6" fill="{card_bg}" stroke="{rose}" stroke-width="1.8" transform="rotate(-4 323 482)"/>',
                f'<text x="323" y="487" font-family="Inter, sans-serif" font-size="12" font-weight="900" fill="{rose}" text-anchor="middle" transform="rotate(-4 323 482)">MISMATCH</text>',
            ]
        )

    # --- ZONE 3A: TOP AGENT & MODEL BOXES (x=436..1044, y=236..356) ---
    agent_glow = 'filter="url(#glowEmerald)"' if active_phase == 0 else ""
    out.extend(
        [
            f'<rect x="436" y="236" width="292" height="112" rx="14" fill="{card_bg}" stroke="{cyan}" stroke-width="2.2" {agent_glow}/>',
            f'<rect x="454" y="256" width="46" height="46" rx="10" fill="{cyan}" fill-opacity="0.18" stroke="{cyan}" stroke-width="1.5"/>',
            f'<text x="477" y="285" font-family="Inter, sans-serif" font-size="18" font-weight="900" fill="{cyan}" text-anchor="middle">AI</text>',
            f'<text x="514" y="276" font-family="Inter, sans-serif" font-size="21" font-weight="900" fill="{text_main}">{_esc(spec["agent_title"])}</text>',
            f'<text x="514" y="302" font-family="Inter, sans-serif" font-size="13.5" font-weight="600" fill="{text_sub}">{_esc(spec["agent_sub"])}</text>',
            # Reasoning arrows between Agent (x=728) and Model (x=808)
            f'<text x="768" y="268" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="{text_sub}" text-anchor="middle">Reasoning</text>',
            f'<line x1="728" y1="282" x2="804" y2="282" stroke="{cyan}" stroke-width="2.2"/>',
            f'<polygon points="808,282 798,277 798,287" fill="{cyan}"/>',
            f'<line x1="808" y1="304" x2="732" y2="304" stroke="{text_muted}" stroke-width="2.0"/>',
            f'<polygon points="728,304 738,299 738,309" fill="{text_muted}"/>',
            f'<circle cx="{746 + (sub_t * 44 if active_phase == 0 else 22):.1f}" cy="282" r="5.5" fill="#FFFFFF" stroke="{cyan}" stroke-width="2.5"/>',
            # Model Inference Box (x=808..1044)
            f'<rect x="808" y="246" width="236" height="94" rx="14" fill="{card_bg}" stroke="{cyan if active_phase in (0, 2) else card_border}" stroke-width="2.0"/>',
            f'<rect x="824" y="266" width="42" height="42" rx="10" fill="{cyan}" fill-opacity="0.18" stroke="{cyan}" stroke-width="1.4"/>',
            f'<text x="845" y="293" font-family="Inter, sans-serif" font-size="15" font-weight="900" fill="{cyan}" text-anchor="middle">LLM</text>',
            f'<text x="878" y="284" font-family="Inter, sans-serif" font-size="18.5" font-weight="900" fill="{text_main}">{_esc(spec["model_title"])}</text>',
            f'<text x="878" y="308" font-family="Inter, sans-serif" font-size="12.5" font-weight="600" fill="{text_sub}">{_esc(spec["model_sub"])}</text>',
        ]
    )

    # Conduit from Agent (x=582, y=348) down to Gateway (x=582, y=506)
    conduit_col = amber if active_phase in (0, 1) else text_muted
    out.extend(
        [
            f'<line x1="582" y1="348" x2="582" y2="502" stroke="{conduit_col}" stroke-width="3.2"/>',
            f'<polygon points="582,508 575,496 589,496" fill="{conduit_col}"/>',
            f'<text x="566" y="408" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{text_sub}" text-anchor="end">Tool call +</text>',
            f'<text x="566" y="426" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{text_sub}" text-anchor="end">authenticated identity +</text>',
            f'<text x="566" y="444" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{text_sub}" text-anchor="end">policy session</text>',
            # Payload Pill above conduit
            f'<rect x="496" y="362" width="172" height="28" rx="14" fill="{card_bg}" stroke="{emerald if active_phase != 3 else rose}" stroke-width="2.0"/>',
            f'<circle cx="512" cy="376" r="5" fill="{emerald if active_phase != 3 else rose}"/>',
            f'<text x="590" y="380" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="{text_main}" text-anchor="middle">{_esc(spec["approved_primary"] if active_phase != 3 else spec["requested_primary"])}</text>',
        ]
    )

    # --- ZONE 3B: CENTRAL GATEWAY ENFORCEMENT POINT (x=436..728, y=510..666) ---
    gw_stroke = emerald if active_phase == 2 else amber
    gw_filter = 'filter="url(#glowEmerald)"' if active_phase == 2 else 'filter="url(#glowAmber)"'
    out.extend(
        [
            f'<rect x="436" y="510" width="292" height="156" rx="16" fill="{card_bg}" stroke="{gw_stroke}" stroke-width="3.0" {gw_filter}/>',
            f'<rect x="458" y="534" width="48" height="48" rx="12" fill="{cyan}" fill-opacity="0.20" stroke="{cyan}" stroke-width="1.6"/>',
            f'<text x="482" y="564" font-family="Inter, sans-serif" font-size="16" font-weight="900" fill="{cyan}" text-anchor="middle">GW</text>',
            f'<text x="520" y="554" font-family="Inter, sans-serif" font-size="22" font-weight="900" fill="{text_main}">{_esc(spec["gateway_title"])}</text>',
            f'<text x="520" y="578" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="{text_sub}">{_esc(spec["gateway_sub"])}</text>',
            f'<rect x="486" y="604" width="192" height="38" rx="10" fill="{amber}"/>',
            f'<text x="582" y="628" font-family="Inter, sans-serif" font-size="14" font-weight="900" fill="#0F172A" text-anchor="middle" letter-spacing="0.5">{_esc(spec["gateway_badge"])}</text>',
        ]
    )

    if active_phase == 2 or frame_phase is None:
        allow_cls = 'class="allow-stream"' if frame_phase is None else ""
        out.extend(
            [
                f'<rect {allow_cls} x="614" y="484" width="104" height="28" rx="14" fill="{emerald}"/>',
                f'<text {allow_cls} x="666" y="503" font-family="Inter, sans-serif" font-size="12.5" font-weight="900" fill="#FFFFFF" text-anchor="middle">✓ ALLOW</text>',
            ]
        )

    # --- ZONE 3C: RIGHT RAIL — TEMPORAL POLICY RULES (x=804..1044, y=428..646) ---
    pol_stroke = amber if active_phase == 1 else (emerald if active_phase == 2 else card_border)
    out.extend(
        [
            f'<text x="804" y="416" font-family="Inter, sans-serif" font-size="11.5" font-weight="900" fill="{amber}" letter-spacing="0.5">{_esc(spec["policy_kicker"])}</text>',
            f'<rect x="804" y="428" width="240" height="218" rx="14" fill="{card_bg}" stroke="{pol_stroke}" stroke-width="2.2"/>',
            f'<rect x="820" y="444" width="36" height="36" rx="9" fill="{cyan}" fill-opacity="0.18" stroke="{cyan}" stroke-width="1.4"/>',
            f'<text x="838" y="467" font-family="Inter, sans-serif" font-size="14" font-weight="900" fill="{cyan}" text-anchor="middle">§</text>',
            f'<text x="866" y="460" font-family="Inter, sans-serif" font-size="17" font-weight="900" fill="{text_main}">{_esc(spec["policy_title"])}</text>',
            f'<text x="866" y="480" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">{_esc(spec["policy_sub"])}</text>',
            # Evaluate / decision arrows between Gateway (728) and Policy (804)
            f'<text x="766" y="528" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="{text_sub}" text-anchor="middle">Evaluate /</text>',
            f'<text x="766" y="542" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="{text_sub}" text-anchor="middle">decision</text>',
            f'<line x1="728" y1="556" x2="800" y2="556" stroke="{amber}" stroke-width="2.4"/>',
            f'<polygon points="804,556 794,551 794,561" fill="{amber}"/>',
            f'<line x1="804" y1="580" x2="732" y2="580" stroke="{emerald if active_phase == 2 else text_muted}" stroke-width="2.2"/>',
            f'<polygon points="728,580 738,575 738,585" fill="{emerald if active_phase == 2 else text_muted}"/>',
        ]
    )

    for r_idx, rule_txt in enumerate(spec["policy_rules"][:4]):
        ry = 498 + r_idx * 34
        is_checked = (
            (frame_phase is None)
            or (active_phase == 2)
            or (active_phase == 1 and sub_t >= (r_idx * 0.22))
        )
        chk_col = emerald if is_checked else text_muted
        chk_cls = f'class="chk-{r_idx + 1}"' if frame_phase is None else ""
        out.extend(
            [
                f'<g {chk_cls}>',
                f'  <rect x="818" y="{ry}" width="212" height="26" rx="6" fill="{emerald if is_checked else card_bg_alt}" fill-opacity="{0.14 if is_checked else 0.5}"/>',
                f'  <rect x="822" y="{ry + 3}" width="20" height="20" rx="5" fill="{chk_col}"/>',
                '  <text x="832" y="' + str(ry + 17) + '" font-family="Inter, sans-serif" font-size="12" font-weight="900" fill="#FFFFFF" text-anchor="middle">✓</text>',
                f'  <text x="848" y="{ry + 17}" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="{text_main}">{_esc(rule_txt)}</text>',
                "</g>",
            ]
        )

    # --- ZONE 3D: LEFT DENY BRANCH -> ACTION BLOCKED (x=36..270, y=580..682) ---
    deny_active = (active_phase == 3) or (frame_phase is None)
    deny_cls = 'class="deny-stream"' if frame_phase is None else ""
    out.extend(
        [
            f'<text x="422" y="556" font-family="Inter, sans-serif" font-size="13" font-weight="900" fill="{rose}" text-anchor="end">DENY:</text>',
            f'<text x="422" y="574" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}" text-anchor="end">artifact or</text>',
            f'<text x="422" y="590" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}" text-anchor="end">environment mismatch</text>',
            f'<line {deny_cls} x1="436" y1="632" x2="276" y2="632" stroke="{rose}" stroke-width="{3.2 if deny_active else 2.0}"/>',
            f'<polygon {deny_cls} points="270,632 282,626 282,638" fill="{rose}"/>',
            f'<rect x="36" y="586" width="234" height="94" rx="14" fill="{card_bg}" stroke="{rose}" stroke-width="{2.8 if active_phase == 3 else 2.0}" {"filter=\"url(#glowRose)\"" if active_phase == 3 else ""}/>',
            f'<circle cx="74" cy="633" r="20" fill="{rose}"/>',
            '<rect x="63" y="630" width="22" height="6" rx="2" fill="#FFFFFF"/>',
            f'<text x="108" y="626" font-family="Inter, sans-serif" font-size="18.5" font-weight="900" fill="{text_main}">{_esc(spec["blocked_title"])}</text>',
            f'<text x="108" y="648" font-family="Inter, sans-serif" font-size="12.5" font-weight="600" fill="{text_sub}">{_esc(spec["blocked_sub"])}</text>',
        ]
    )

    # --- ZONE 3E: TELEMETRY BOXES (Policy Session History + CloudWatch/Trace, x=804..1044, y=664..848) ---
    out.extend(
        [
            # Dashed purple/pink lines from Gateway to History & Trace
            f'<path d="M 728 624 L 776 624 L 776 704 L 804 704" fill="none" stroke="{purple}" stroke-width="2.2" stroke-dasharray="6 5" stroke-dashoffset="{dash_offset:.1f}" class="anim-dash"/>',
            f'<path d="M 728 644 L 762 644 L 762 798 L 804 798" fill="none" stroke="{pink}" stroke-width="2.2" stroke-dasharray="6 5" stroke-dashoffset="{dash_offset:.1f}" class="anim-dash"/>',
            f'<circle cx="776" cy="672" r="6" fill="{purple}"/>',
            f'<circle cx="762" cy="742" r="6" fill="{pink}"/>',
            # Box 1: Policy session history
            f'<rect x="804" y="666" width="240" height="76" rx="12" fill="{card_bg}" stroke="{purple}" stroke-width="1.8"/>',
            f'<rect x="818" y="684" width="38" height="38" rx="9" fill="{purple}"/>',
            '<text x="837" y="709" font-family="Inter, sans-serif" font-size="16" font-weight="900" fill="#FFFFFF" text-anchor="middle">↺</text>',
            f'<text x="868" y="698" font-family="Inter, sans-serif" font-size="15" font-weight="900" fill="{text_main}">{_esc(spec["history_title"])}</text>',
            f'<text x="868" y="718" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">{_esc(spec["history_sub"])}</text>',
            # Box 2: Cloud Trace / CloudWatch
            f'<rect x="804" y="758" width="240" height="82" rx="12" fill="{card_bg}" stroke="{pink}" stroke-width="2.0"/>',
            f'<rect x="818" y="778" width="38" height="38" rx="9" fill="{pink}"/>',
            '<text x="837" y="803" font-family="Inter, sans-serif" font-size="15" font-weight="900" fill="#FFFFFF" text-anchor="middle">◎</text>',
            f'<text x="868" y="790" font-family="Inter, sans-serif" font-size="15" font-weight="900" fill="{text_main}">{_esc(spec["trace_title"])}</text>',
            f'<text x="868" y="810" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">{_esc(spec["trace_sub"])}</text>',
        ]
    )

    # --- ZONE 3F: BOTTOM APPROVAL LOOKUP & DEPLOYMENT EXECUTION (y=848..986) ---
    # Left: Read verified approval (x=468 & x=498 between y=666 and y=848)
    out.extend(
        [
            f'<text x="450" y="746" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{text_sub}" text-anchor="end">Read verified</text>',
            f'<text x="450" y="764" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{text_sub}" text-anchor="end">approval</text>',
            f'<line x1="468" y1="666" x2="468" y2="842" stroke="{blue}" stroke-width="2.4"/>',
            f'<polygon points="468,848 462,836 474,836" fill="{blue}"/>',
            f'<line x1="498" y1="848" x2="498" y2="672" stroke="{blue}" stroke-width="2.4"/>',
            f'<polygon points="498,666 492,678 504,678" fill="{blue}"/>',
            f'<circle cx="468" cy="{710 + (sub_t * 95 if active_phase == 1 else 45):.1f}" r="6" fill="#FFFFFF" stroke="{blue}" stroke-width="2.5"/>',
        ]
    )
    approver_title_lines = _wrap(spec["approver_title"], width=18, max_lines=2)
    approver_note_lines = _wrap(spec["approver_note"], width=42, max_lines=2)
    out.extend(
        [
            # Authenticated human approver (x=36..240, y=854..948)
            f'<rect x="36" y="854" width="204" height="94" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.8"/>',
            f'<circle cx="66" cy="892" r="14" fill="{blue}" fill-opacity="0.15" stroke="{blue}" stroke-width="1.8"/>',
            f'<text x="66" y="897" font-family="Inter, sans-serif" font-size="13" font-weight="900" fill="{blue}" text-anchor="middle">✓</text>',
            f'<text x="90" y="890" font-family="Inter, sans-serif" font-size="13.5" font-weight="900" fill="{text_main}">{_esc(approver_title_lines[0])}</text>',
            f'<text x="90" y="910" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{text_sub}">{_esc(approver_title_lines[1] if len(approver_title_lines) > 1 else "")}</text>',
            f'<line x1="240" y1="900" x2="266" y2="900" stroke="{blue}" stroke-width="2.2"/>',
            f'<polygon points="272,900 262,895 262,905" fill="{blue}"/>',
            f'<text x="40" y="972" font-family="Inter, sans-serif" font-size="11.5" font-weight="600" fill="{text_sub}">{_esc(approver_note_lines[0])}</text>',
            f'<text x="40" y="988" font-family="Inter, sans-serif" font-size="11.5" font-weight="600" fill="{text_sub}">{_esc(approver_note_lines[1] if len(approver_note_lines) > 1 else "")}</text>',
            # Approval Service (x=272..560, y=848..958)
            f'<rect x="272" y="848" width="288" height="110" rx="14" fill="{card_bg}" stroke="{blue if active_phase == 1 else card_border}" stroke-width="2.4"/>',
            f'<rect x="292" y="876" width="52" height="52" rx="12" fill="{rose}" fill-opacity="0.18" stroke="{rose}" stroke-width="1.6"/>',
            f'<text x="318" y="908" font-family="Inter, sans-serif" font-size="20" font-weight="900" fill="{rose}" text-anchor="middle">🛡</text>',
            f'<text x="360" y="892" font-family="Inter, sans-serif" font-size="21" font-weight="900" fill="{text_main}">{_esc(spec["approval_svc_title"])}</text>',
            f'<text x="360" y="920" font-family="Inter, sans-serif" font-size="13.5" font-weight="600" fill="{text_sub}">{_esc(spec["approval_svc_sub"])}</text>',
        ]
    )

    # Right: ALLOW conduit (x=678, y=666..848) -> Deployment Service (x=612..896, y=848..958)
    allow_active = (active_phase == 2) or (frame_phase is None)
    out.extend(
        [
            f'<line x1="678" y1="666" x2="678" y2="842" stroke="{emerald}" stroke-width="{3.6 if allow_active else 2.4}"/>',
            f'<polygon points="678,848 671,836 685,836" fill="{emerald}"/>',
            f'<text x="694" y="742" font-family="Inter, sans-serif" font-size="13.5" font-weight="900" fill="{emerald}">ALLOW:</text>',
            f'<text x="694" y="762" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="{text_main}">exact approved</text>',
            f'<text x="694" y="780" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="{text_main}">action</text>',
        ]
    )
    if allow_active:
        pkt_cls = 'class="allow-stream"' if frame_phase is None else ""
        for pkt_i in range(3):
            py = 706 + pkt_i * 44 + (sub_t * 24 if frame_phase is not None else 0)
            out.extend(
                [
                    f'<circle {pkt_cls} cx="678" cy="{py:.1f}" r="11" fill="{emerald}" fill-opacity="0.24"/>',
                    f'<circle {pkt_cls} cx="678" cy="{py:.1f}" r="5.5" fill="#FFFFFF" stroke="{emerald}" stroke-width="2.5"/>',
                ]
            )

    out.extend(
        [
            f'<rect x="612" y="848" width="284" height="110" rx="14" fill="{card_bg}" stroke="{emerald if active_phase == 2 else card_border}" stroke-width="2.4" {"filter=\"url(#glowEmerald)\"" if active_phase == 2 else ""}/>',
            f'<rect x="632" y="876" width="52" height="52" rx="12" fill="{purple}" fill-opacity="0.18" stroke="{purple}" stroke-width="1.6"/>',
            f'<text x="658" y="908" font-family="Inter, sans-serif" font-size="20" font-weight="900" fill="{purple}" text-anchor="middle">⚙</text>',
            f'<text x="700" y="892" font-family="Inter, sans-serif" font-size="21" font-weight="900" fill="{text_main}">{_esc(spec["exec_svc_title"])}</text>',
            f'<text x="700" y="920" font-family="Inter, sans-serif" font-size="13.5" font-weight="600" fill="{text_sub}">{_esc(spec["exec_svc_sub"])}</text>',
            # Side note dashed box (x=912..1044, y=854..952)
            f'<rect x="912" y="854" width="132" height="98" rx="12" fill="{card_bg_alt}" stroke="{card_border}" stroke-width="1.5" stroke-dasharray="5 4"/>',
            f'<text x="926" y="886" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="{text_main}">Service</text>',
            f'<text x="926" y="906" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="{text_main}">authorization</text>',
            f'<text x="926" y="926" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">+ idempotency</text>',
        ]
    )

    # --- ZONE 4: BUILT-IN CONTROLS 3-PILLAR STRIP (y=1024..1156) ---
    out.append(
        f'<text x="36" y="1038" font-family="Inter, sans-serif" font-size="12.5" font-weight="900" fill="{text_sub}" letter-spacing="0.8">BUILT-IN CONTROLS Across SECURITY · PERFORMANCE · COST</text>'
    )
    ctrl_colors = [rose, purple, emerald]
    for c_idx, (c_title, c_sub) in enumerate(spec["controls"][:3]):
        cx = 36 + c_idx * 342
        ccol = ctrl_colors[c_idx % 3]
        is_c_hi = (active_phase == c_idx) or (frame_phase is None and c_idx == 2)
        out.extend(
            [
                f'<rect x="{cx}" y="1052" width="324" height="96" rx="14" fill="{card_bg}" stroke="{ccol if is_c_hi else card_border}" stroke-width="{2.4 if is_c_hi else 1.6}"/>',
                f'<rect x="{cx + 18}" y="1074" width="48" height="48" rx="10" fill="{ccol}" fill-opacity="0.18" stroke="{ccol}" stroke-width="1.6"/>',
                f'<text x="{cx + 42}" y="1104" font-family="Inter, sans-serif" font-size="16" font-weight="900" fill="{ccol}" text-anchor="middle">0{c_idx + 1}</text>',
                f'<text x="{cx + 80}" y="1092" font-family="Inter, sans-serif" font-size="16" font-weight="900" fill="{text_main}">{_esc(c_title)}</text>',
                f'<text x="{cx + 80}" y="1116" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="{text_sub}">{_esc(c_sub)}</text>',
            ]
        )

    # --- ZONE 5: FOOTER GOLDEN RULE BANNER (y=1182..1318) ---
    out.extend(
        [
            f'<rect x="36" y="1182" width="68" height="6" rx="3" fill="{amber}"/>',
            f'<text x="36" y="1234" font-family="Inter, sans-serif" font-size="33" font-weight="900" fill="{text_main}" letter-spacing="-0.4">{_esc(spec["footer_takeaway"])}</text>',
            f'<text x="36" y="1272" font-family="Inter, sans-serif" font-size="16" font-weight="600" fill="{text_sub}">{_esc(spec["footer_sub"])}</text>',
            f'<rect x="36" y="1294" width="1008" height="32" rx="16" fill="{footer_bar_bg}" stroke="{card_border}" stroke-width="1.2"/>',
            f'<text x="540" y="1315" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="{text_sub}" text-anchor="middle">STEP-BY-STEP DYNAMIC ARCHITECTURE  •  Blueprint {spec["matched_template_id"]}  •  Google Cloud Agentic Architecture Engineering</text>',
            "</svg>",
        ]
    )
    return "\n".join(out)


def render_step_flow_bundle(
    preset_id: str = "FLOW-01",
    custom_topic: str = "",
    theme: str = "light",
    compile_gif: bool = True,
    num_frames: int = 12,
) -> Dict[str, Any]:
    """Compile the complete Step-by-Step Dynamic Flow Bundle (4:5 SVG + 4:5 GIF89a + 4:5 H.264 MP4 + Serial/Parallel Trace + 6-Beat Copy)."""
    spec = build_step_flow_spec_from_topic(preset_id=preset_id, custom_topic=custom_topic)
    copy_bundle = compile_step_by_step_linkedin_post(spec)
    execution_trace = build_serial_parallel_execution_trace(spec)
    theme_key = "dark_neon" if str(theme or "light").lower() in ("dark", "dark_neon", "brij") else "light"

    slug_seed = f"{spec['preset_id']}|{custom_topic.strip()}|{theme_key}"
    short_hash = hashlib.sha256(slug_seed.encode("utf-8")).hexdigest()[:8].upper()
    stem = f"{spec['preset_id']}-{theme_key}-{short_hash}"

    STEP_FLOW_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = STEP_FLOW_ASSETS_DIR / f"{stem}.svg"
    gif_path = STEP_FLOW_ASSETS_DIR / f"{stem}.gif"
    mp4_path = STEP_FLOW_ASSETS_DIR / f"{stem}.mp4"
    png_path = STEP_FLOW_ASSETS_DIR / f"{stem}.png"

    svg_text = generate_step_by_step_flow_svg(spec, theme=theme_key, frame_phase=None)
    svg_path.write_text(svg_text, encoding="utf-8")

    gif_ready = gif_path.exists() and gif_path.stat().st_size > 10000
    mp4_ready = mp4_path.exists() and mp4_path.stat().st_size > 10000
    ffmpeg = resolve_ffmpeg_bin()
    if compile_gif and not gif_ready:
        chrome = resolve_chrome_bin()
        if chrome is not None and ffmpeg is not None:
            with tempfile.TemporaryDirectory(prefix="step_flow_gif_") as tmp_dir:
                tmp_path = Path(tmp_dir)
                for f_idx in range(num_frames):
                    phase = f_idx / float(num_frames)
                    f_svg = tmp_path / f"frame_{f_idx:02d}.svg"
                    f_png = tmp_path / f"frame_{f_idx:02d}.png"
                    f_svg.write_text(
                        generate_step_by_step_flow_svg(spec, theme=theme_key, frame_phase=phase),
                        encoding="utf-8",
                    )
                    subprocess.run(
                        [
                            str(chrome),
                            "--headless=new",
                            "--no-sandbox",
                            "--disable-setuid-sandbox",
                            "--disable-gpu",
                            "--window-size=1080,1350",
                            f"--screenshot={f_png}",
                            f"file://{f_svg}",
                        ],
                        check=False,
                        capture_output=True,
                    )
                    if f_idx == 6 and f_png.exists():
                        png_path.write_bytes(f_png.read_bytes())

                subprocess.run(
                    [
                        str(ffmpeg),
                        "-y",
                        "-framerate",
                        "3",
                        "-i",
                        str(tmp_path / "frame_%02d.png"),
                        "-vf",
                        "split[s0][s1];[s0]palettegen=max_colors=192:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4",
                        "-loop",
                        "0",
                        str(gif_path),
                    ],
                    check=False,
                    capture_output=True,
                )
                gif_ready = gif_path.exists() and gif_path.stat().st_size > 10000

    if compile_gif and gif_ready and not mp4_ready and ffmpeg is not None:
        subprocess.run(
            [
                str(ffmpeg),
                "-y",
                "-stream_loop",
                "2",
                "-i",
                str(gif_path),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-vf",
                "scale=1080:1350:flags=lanczos",
                "-r",
                "30",
                "-movflags",
                "+faststart",
                str(mp4_path),
            ],
            check=False,
            capture_output=True,
        )
        mp4_ready = mp4_path.exists() and mp4_path.stat().st_size > 10000

    return {
        "status": "ok",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "preset_id": spec["preset_id"],
        "preset_name": spec["name"],
        "theme": theme_key,
        "aspect_ratio": "4:5 (1080×1350 Portrait)",
        "matched_template_id": spec["matched_template_id"],
        "svg_url": f"/assets/step-flows/{svg_path.name}",
        "gif_url": f"/assets/step-flows/{gif_path.name}" if gif_ready else "",
        "mp4_url": f"/assets/step-flows/{mp4_path.name}" if mp4_ready else "",
        "png_url": f"/assets/step-flows/{png_path.name}" if png_path.exists() else "",
        "gif_ready": gif_ready,
        "mp4_ready": mp4_ready,
        "spec": spec,
        "copy_bundle": copy_bundle,
        "execution_trace": execution_trace,
        "available_presets": [
            {"id": k, "name": v["name"], "template_id": v["matched_template_id"]}
            for k, v in STEP_FLOW_PRESETS.items()
        ],
    }
