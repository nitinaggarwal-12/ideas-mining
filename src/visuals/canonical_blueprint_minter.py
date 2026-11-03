"""5-Signal Canonical Blueprint Isomorphism Router (`S_iso`) & Continuous `T85+` Minter.

Enforces `Law 18` (`Rule 57` & `Rule 60A–60C`):
- Scores candidate topics strictly against the **Non-Legacy Canonical Pool**
  (`T01`, `T53`–`T89` + `PromptCanvas` `#00`, `#52`–`#69`, `#78`, `#79`, `#81`, `#84`).
- Explicitly rejects legacy `Gen-1` Python SVG IDs (`T02`–`T52`) with a fail-closed `ValueError`.
- Implements the 5-signal weighted formula:
    S_iso(I, T) = 0.30*Topology + 0.25*ControlFlow + 0.20*Cardinality + 0.15*FinOpsSlot + 0.10*CognitiveFit
- Decision thresholds:
    * `S_iso >= 80`  -> `REUSE_CANONICAL`
    * `65 <= S_iso < 80` -> `COMPOSE_2VIEW_ZOOM`
    * `S_iso < 65`   -> `MINT_NEW` (`T85+` via `scripts/build_t79_t84_drawio.py` + `viewer-static.min.js @2x`)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

BANNED_LEGACY_GEN1_IDS = {f"T{i:02d}" for i in range(2, 53)}

# Non-Legacy Canonical Pool ONLY (`T01`, `T53`–`T84`, plus `PromptCanvas` Cloud Topologies)
CANONICAL_POOL_SIGNATURES: Dict[str, Dict[str, Any]] = {
    "T01": {
        "topology": "4-tier-breaker-loop-spine",
        "control_flow": "circuit-breaker-dedupe-cap",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "loop-guard-spine",
    },
    "T54": {
        "topology": "3-band-dual-agent-workflow",
        "control_flow": "builder-reviewer-recheck-loop",
        "cardinality": 3,
        "finops_slot": False,
        "cognitive_fit": "dual-agent-coding",
    },
    "T56": {
        "topology": "persona-vs-bubble-governance",
        "control_flow": "blindspot-to-4-control-bar",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "shadow-ai-governance",
    },
    "T57": {
        "topology": "5-pillar-off-vs-on-toggles",
        "control_flow": "stateless-vs-managed-toggle",
        "cardinality": 5,
        "finops_slot": False,
        "cognitive_fit": "runtime-comparison",
    },
    "T58": {
        "topology": "5-stage-3d-compression-funnel",
        "control_flow": "progressive-filter-and-pointer-swap",
        "cardinality": 5,
        "finops_slot": True,
        "cognitive_fit": "context-compression-funnel",
    },
    "T61": {
        "topology": "4-plane-isolated-runtime-topology",
        "control_flow": "microvm-codeact-precompletion-test-gate",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "sandbox-codeact-loop",
    },
    "T62": {
        "topology": "supervisor-federated-delegation-tree",
        "control_flow": "typed-a2a-jsonrpc-blackboard",
        "cardinality": 3,
        "finops_slot": False,
        "cognitive_fit": "multi-agent-delegation",
    },
    "T64": {
        "topology": "3-stage-conditional-decision-tree",
        "control_flow": "yes-no-diamond-routing",
        "cardinality": 3,
        "finops_slot": False,
        "cognitive_fit": "decision-tree-gate",
    },
    "T65": {
        "topology": "5x4-evaluation-matrix",
        "control_flow": "multi-criteria-stack-scoring",
        "cardinality": 5,
        "finops_slot": True,
        "cognitive_fit": "benchmark-matrix",
    },
    "T66": {
        "topology": "4-tier-capability-pyramid",
        "control_flow": "ascending-maturity-tiers",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "capability-maturity",
    },
    "T67": {
        "topology": "4-quadrant-self-healing-torus",
        "control_flow": "generate-test-gate-retry-cycle",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "autonomous-torus-loop",
    },
    "T68": {
        "topology": "4-tier-open-knowledge-spine",
        "control_flow": "format-schema-sha-graph",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "knowledge-format-spine",
    },
    "T73": {
        "topology": "4-tier-11zone-reference-spine",
        "control_flow": "static-zone-reference",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "enterprise-zone-map",
    },
    "T74": {
        "topology": "4-tier-6vendor-sandbox-spine",
        "control_flow": "microvm-isolation-comparison",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "sandbox-vendor-matrix",
    },
    "T79": {
        "topology": "4-tier-a-vs-b-contract-spine",
        "control_flow": "cfg-logit-mask-plus-semantic-span-verifier",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "structured-decoding-contract",
    },
    "T80": {
        "topology": "4-tier-9-decision-cascade-spine",
        "control_flow": "classifier-flash-argon-cascade",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "latency-finops-router",
    },
    "T81": {
        "topology": "4-tier-8phase-curriculum-spine",
        "control_flow": "progressive-harness-maker-checker",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "curriculum-evolution",
    },
    "T82": {
        "topology": "4-tier-replay-audit-spine",
        "control_flow": "seeded-defect-sha-triage-timer",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "pr-review-misses-ledger",
    },
    "T83": {
        "topology": "4-tier-eval-passk-spine",
        "control_flow": "sandbox-reset-and-multi-trial-grader",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "reliability-eval-matrix",
    },
    "T84": {
        "topology": "4-tier-procedural-skill-ledger-spine",
        "control_flow": "trajectory-distill-sha-pin-invalidate",
        "cardinality": 4,
        "finops_slot": True,
        "cognitive_fit": "episodic-to-procedural-memory",
    },
    "#78": {
        "topology": "4-zone-gcp-hub-and-spoke",
        "control_flow": "ingress-governance-compute-data-hub",
        "cardinality": 4,
        "finops_slot": False,
        "cognitive_fit": "cloud-hub-and-spoke",
    },
    "#81": {
        "topology": "16-step-lifeline-sequence",
        "control_flow": "chronological-16hop-hitl-trace",
        "cardinality": 6,
        "finops_slot": False,
        "cognitive_fit": "runtime-lifeline-sequence",
    },
}


def validate_non_legacy_template_id(tid: str) -> None:
    """Fail closed if any caller attempts to score or route to purged legacy Gen-1 IDs (`T02`–`T52`)."""
    if tid in BANNED_LEGACY_GEN1_IDS:
        raise ValueError(
            f"Law 18 / Rule 60A Violation: Legacy Gen-1 Python SVG template '{tid}' is permanently retired."
        )


def _pair_similarity(a: str, b: str) -> float:
    if a == b:
        return 100.0
    toks_a = set(a.replace("-", " ").split())
    toks_b = set(b.replace("-", " ").split())
    if not toks_a or not toks_b:
        return 35.0
    overlap = len(toks_a & toks_b) / max(len(toks_a | toks_b), 1)
    return round(35.0 + 60.0 * overlap, 2)


def compute_canonical_siso(topic_spec: Dict[str, Any], candidate_tid: Optional[str] = None) -> Dict[str, Any]:
    """Compute the 5-signal Canonical Isomorphism Score (`S_iso`) over the Non-Legacy Canonical Pool."""
    if candidate_tid is not None:
        validate_non_legacy_template_id(candidate_tid)

    fv = topic_spec.get("feature_vector") or {}
    t_topo = str(fv.get("topology", "4-tier-spine"))
    t_ctrl = str(fv.get("control_flow", "deterministic-gate"))
    t_card = int(fv.get("cardinality", 4))
    t_fin = bool(fv.get("finops_slot", True))
    t_cog = str(fv.get("cognitive_fit", "systems-spine"))

    pool_items = (
        [(candidate_tid, CANONICAL_POOL_SIGNATURES[candidate_tid])]
        if candidate_tid and candidate_tid in CANONICAL_POOL_SIGNATURES
        else list(CANONICAL_POOL_SIGNATURES.items())
    )

    scored: List[Tuple[str, float, Dict[str, float]]] = []
    for tid, sig in pool_items:
        validate_non_legacy_template_id(tid)
        s_topo = _pair_similarity(t_topo, sig["topology"])
        s_ctrl = _pair_similarity(t_ctrl, sig["control_flow"])
        card_diff = abs(t_card - int(sig["cardinality"]))
        s_card = max(40.0, 100.0 - 22.0 * card_diff)
        s_fin = 100.0 if t_fin == bool(sig["finops_slot"]) else 45.0
        s_cog = _pair_similarity(t_cog, sig["cognitive_fit"])

        total = round(
            0.30 * s_topo + 0.25 * s_ctrl + 0.20 * s_card + 0.15 * s_fin + 0.10 * s_cog,
            1,
        )
        scored.append(
            (
                tid,
                total,
                {
                    "topology": s_topo,
                    "control_flow": s_ctrl,
                    "cardinality": s_card,
                    "finops_slot": s_fin,
                    "cognitive_fit": s_cog,
                },
            )
        )

    scored.sort(key=lambda item: item[1], reverse=True)
    best_tid, best_score, breakdown = scored[0]

    # Honor calibrated topic empirical floor/ceiling if explicitly specified on topic_spec
    if candidate_tid is None and "nearest_prior_siso" in topic_spec and "nearest_prior_template" in topic_spec:
        cal_tid = str(topic_spec["nearest_prior_template"])
        validate_non_legacy_template_id(cal_tid)
        cal_score = float(topic_spec["nearest_prior_siso"])
        best_tid = cal_tid
        best_score = cal_score

    if best_score >= 80.0:
        decision = "REUSE_CANONICAL"
        resolved_tid = best_tid
    elif best_score >= 65.0:
        decision = "COMPOSE_2VIEW_ZOOM"
        resolved_tid = topic_spec.get("canonical_template_id", best_tid)
    else:
        decision = "MINT_NEW"
        resolved_tid = topic_spec.get("canonical_template_id", "T85")

    validate_non_legacy_template_id(resolved_tid)
    return {
        "topic_id": topic_spec.get("id", "CUSTOM"),
        "nearest_prior_template": best_tid,
        "siso_score": best_score,
        "decision": decision,
        "resolved_canonical_template": resolved_tid,
        "cloud_zoom_blueprints": topic_spec.get("cloud_zoom_blueprints", ["#78", "#81"]),
        "signal_breakdown": breakdown,
    }


def mint_or_resolve_topic_blueprint(
    topic_spec: Dict[str, Any], recompile_assets: bool = False
) -> Dict[str, Any]:
    """Resolve or mint the canonical Draw.io + `@2x` PNG + native `.pptx` bundle for a topic."""
    routing = compute_canonical_siso(topic_spec)
    tid = routing["resolved_canonical_template"]
    gallery_dir = WORKSPACE_ROOT / "assets" / "template-gallery"
    drawio_path = gallery_dir / f"{tid}.drawio"
    png_path = gallery_dir / f"{tid}.png"
    pptx_path = gallery_dir / f"{tid}.pptx"

    if recompile_assets or not drawio_path.exists() or not png_path.exists():
        if tid in {"T79", "T80", "T81", "T82", "T83", "T84", "T85", "T86", "T87", "T88", "T89"}:
            subprocess.run(
                [sys.executable, str(WORKSPACE_ROOT / "scripts" / "build_t79_t84_drawio.py")],
                cwd=str(WORKSPACE_ROOT),
                check=True,
            )
            subprocess.run(
                [
                    "node",
                    str(WORKSPACE_ROOT / "scripts" / "sync_canonical_promptcanvas_infographics.mjs"),
                    "--skip-export",
                    tid,
                ],
                cwd=str(WORKSPACE_ROOT),
                check=True,
            )

    if recompile_assets or not pptx_path.exists():
        subprocess.run(
            [
                "node",
                str(WORKSPACE_ROOT / "scripts" / "compile_and_sync_template_slides.mjs"),
                "--local-pptx-only",
                "--only",
                tid,
            ],
            cwd=str(WORKSPACE_ROOT),
            check=True,
        )

    return {
        **routing,
        "drawio_path": str(drawio_path),
        "png_path": str(png_path),
        "pptx_path": str(pptx_path),
        "assets_verified": drawio_path.exists() and png_path.exists() and pptx_path.exists(),
    }
