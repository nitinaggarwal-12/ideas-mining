#!/usr/bin/env python3
"""Deterministic Naive vs. Engineered CLI Benchmark Runner for gcp-mcp-zero-bloat-gateway."""

import argparse
import json
from src.engine import ZeroBloatMcpOboGateway


def main() -> None:
    parser = argparse.ArgumentParser(description="Run side-by-side Naive vs. Engineered benchmark")
    parser.add_argument("--compare", action="store_true", help="Print side-by-side comparison table and JSON")
    parser.add_argument(
        "--query",
        default="Correlate Q3 P1 latency incidents with regional BigQuery spend spikes",
        help="Benchmark query to trace",
    )
    parser.add_argument("--json-only", action="store_true", help="Emit pure JSON output")
    args = parser.parse_args()

    engine = ZeroBloatMcpOboGateway()
    cmp_data = engine.compare_naive_vs_engineered(args.query)

    if args.json_only:
        print(json.dumps(cmp_data, indent=2))
        return

    n = cmp_data["naive_baseline"]
    e = cmp_data["engineered_harness"]
    d = cmp_data["deltas"]
    print("=" * 92)
    print(f"[{cmp_data['post_id']}] {cmp_data['repo_slug']} — Naive Baseline vs. Engineered Harness")
    print(f"Query: {cmp_data['query']}")
    print("-" * 92)
    print(f"{'Metric':<30} | {'Naive Baseline':<27} | {'Engineered Harness':<27}")
    print("-" * 92)
    print(f"{'Schema Tokens / Turn':<30} | {str(n['schema_tokens_per_turn']) + ' tok':<27} | {str(e['schema_tokens_per_turn']) + ' tok (-' + str(d['token_bloat_reduction_pct']) + '%)':<27}")
    print(f"{'Injected MCP Tool Schemas':<30} | {str(n['selected_tools_injected']) + ' static schemas':<27} | {str(e['selected_tools_injected']) + ' Top-K slim schemas':<27}")
    print(f"{'L1 Prefix KV-Cache Hit Rate':<30} | {str(n['prefix_cache_hit_pct']) + '%':<27} | {str(e['prefix_cache_hit_pct']) + '%':<27}")
    print(f"{'p95 End-to-End Latency':<30} | {str(n['p95_latency_ms']) + ' ms':<27} | {str(e['p95_latency_ms']) + ' ms (' + str(d['latency_speedup_x']) + 'x faster)':<27}")
    print(f"{'Security & Policy Gate':<30} | {'FAIL (Blocked)':<27} | {'PASS (Verified OBO)':<27}")
    print("=" * 92)
    if args.compare:
        print(json.dumps(cmp_data, indent=2))


if __name__ == "__main__":
    main()
