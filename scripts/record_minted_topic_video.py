#!/usr/bin/env python3
"""CLI entrypoint to record and verify a multi-scene 1080p30 walkthrough video for a minted topic."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.video.canonical_walkthrough_recorder import record_minted_topic_walkthrough


def main() -> None:
    parser = argparse.ArgumentParser(description="Record 1080p30 multi-scene walkthrough video for a minted topic.")
    parser.add_argument("--topic-id", default="MINT-01", help="Topic ID from career_minting_catalog (default: MINT-01)")
    args = parser.parse_args()

    print(f"==> [Video Studio] Recording 6-scene 1080p30 walkthrough + Omni 1.1 Digital Twin for {args.topic_id}...")
    manifest = record_minted_topic_walkthrough(topic_id=args.topic_id)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
