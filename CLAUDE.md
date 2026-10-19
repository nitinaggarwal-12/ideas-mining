# CLAUDE.md — Cross-Agent Engineering & Verification Guide

> Synchronized with `AGENTS.md`, `GEMINI.md`, and `.openhands/microagents/repo.md`.

## Commands
- **Generate & Verify All 8 Standalone Repos**: `python3 scripts/build_and_verify_all.py`
- **Run Deterministic Quality & Zero-Hallucination Gate**: `python3 scripts/verify_all_repos.py`
- **Start Interactive OpenHands Studio & Idea Mining Server**: `python3 server.py`

## Architecture
- `src/catalog/posts_catalog.py`: Ground-truth primary sources, creator mining intelligence, and per-post specifications for all 8 LinkedIn posts.
- `src/openhands_harness/autonomous_agent.py`: OpenHands autonomous software engineering harness (Explore -> Plan -> Synthesize -> Sandbox Test -> Git Commit).
- `src/visuals/diagram_2d_engine.py`: Deterministic `@2d` SVG, PNG, and Draw.io XML generator (LinkedIn 2D Infographics + Google Cloud `#78` 2D Architectures).
- `src/slides/slide_deck_compiler.py`: 12-Slide 3-Act OpenXML `.pptx` and LinkedIn PDF Carousel compiler with spoken speaker notes.
- `src/terraform_gen/terraform_builder.py`: 1-Click GCP Terraform & Cloud Run deployment generator.
- `src/generator/repo_factory.py`: End-to-end standalone Git repository assembler and verifier.
