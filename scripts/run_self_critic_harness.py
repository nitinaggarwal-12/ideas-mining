#!/usr/bin/env python3
"""CLI Entrypoint for the Autonomous Self-Critic, Self-Evaluating & Self-Correcting Harness (`Harness²`)."""

import argparse
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from src.openhands_harness.self_critic_harness import get_self_critic_harness


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Autonomous Self-Critic & Auto-Healing Harness.")
    parser.add_argument("--auto-heal", action="store_true", default=True, help="Automatically remediate any detected drift or missing exemplars.")
    parser.add_argument("--no-auto-heal", dest="auto_heal", action="store_false", help="Run read-only evaluation without auto-healing.")
    parser.add_argument("--refresh-discovery", action="store_true", default=False, help="Poll live upstream RSS/API feeds during discovery.")
    parser.add_argument("--strict", action="store_true", default=True, help="Exit non-zero if any gate fails after auto-healing.")
    parser.add_argument("--json", action="store_true", default=False, help="Print full JSON receipt.")
    args = parser.parse_args()

    harness = get_self_critic_harness()
    result = harness.run_full_self_critic_cycle(
        auto_heal=args.auto_heal,
        refresh_discovery=args.refresh_discovery,
        trigger_source="cli_self_critic_gate",
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"[{result['harness_version']}] Status={result['status']} | "
            f"Score={result['overall_score']}/100 | "
            f"Gates={result['gates_passed']}/{result['gates_total']} PASS | "
            f"AutoHealed={ len(result.get('latest_auto_healed_actions', [])) } actions | "
            f"Duration={result['duration_ms']}ms"
        )
        for act in result.get("latest_auto_healed_actions", []):
            print(f"  [AUTO-HEALED] {act}")
        for gate in result.get("gates", []):
            print(f"  [{gate['status']}] {gate['gate_id']} ({gate['score']}%): {gate['metrics']}")

    if args.strict and not result.get("all_gates_passed"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
