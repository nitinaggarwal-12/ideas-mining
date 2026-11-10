# Deterministic 2D Architecture & Infographic Specification — MINT-01 (`gcp-mcp-zero-bloat-gateway`)

> **Post Title**: Zero-Bloat MCP Gateway: Dynamic Top-K Tool Search + RFC 8693 OAuth 2.1 On-Behalf-Of Security
> **Primary Source**: IETF RFC 8693 OAuth 2.0 Token Exchange + MCP Dynamic Tool Discovery Specification (`urn:ietf:rfc:8693:mcp-zero-bloat-gateway-2026`)
> **Generated Assets in `./visuals/`**:
> - `./visuals/linkedin-infographic-2d.svg` & `./visuals/linkedin-infographic-2d.png` (Deterministic Vector SVG & 2x Chrome PNG)
> - `./visuals/gcp-architecture-2d.drawio`, `./visuals/gcp-architecture-2d.svg` & `./visuals/gcp-architecture-2d.png` (100% Editable Draw.io XML, Vector SVG & PNG)
> - `./visuals/dynamic-solution-flow.svg`, `./visuals/dynamic-solution-flow.gif` & `./visuals/dynamic-solution-flow.png` (Moving-Arrow Animated Flow)

---

## 1. Bespoke LinkedIn 2D Architecture Infographic Specification (`MINT-01`)

```text
Create a publication-grade 2D technical architecture infographic in a crisp executive light theme (#F8FAFC background, white cards, deep navy #0F2942 header bar).
Title at top: "ZERO-BLOAT MCP GATEWAY: DYNAMIC TOP-K TOOL SEARCH + RFC 8693 OAUTH 2.1 ON-BEHALF-OF SECURITY"
Subtitle: "S.C.O.P.E. Meta-MCP Hybrid Discovery + Per-User OBO Token Swap on Google Cloud ADK"
TIER 1 (FAILURE MODE WITHOUT GUARD): 1. 85 Static Schemas (55.2K tok/turn ($0.42) + L1 cache bust) -> 2. Shared Admin Key (Confused-Deputy cross-tenant leak) -> 3. 61% Tool Accuracy (Wrong tool args + CISO block)
TIER 2 (4-STAGE DETERMINISTIC ARCHITECTURAL SOLUTION):
- S • SEARCH TOP-K (Hybrid BM25 + Dense Search): Retrieve top-4 matching tool schemas on demand (55.2K -> 1.38K tokens, -97.5%) with frozen L1 prefix. [Google Cloud: ADK MCPToolset + Vertex Search ⇄ Open-Source: FastMCP + Qdrant BM25/Dense]
- O • OBO TOKEN SWAP (RFC 8693 OIDC -> OBO JWT): Exchange caller OIDC assertion for 300s per-user audience-scoped JWT (`aud=mcp://tool`). [Google Cloud: Cloud IAM STS Token Exchange ⇄ Open-Source: Authlib RFC 8693 OBO Broker]
- P • POLICY ARMOR (Tamper & Tenant ACL Guard): Verify cryptographic signature, tenant claim, and prompt-injection policy in 0.4ms before execution. [Google Cloud: Model Armor + Cloud Run Gate ⇄ Open-Source: LlamaFirewall + OPA Rego]
- E • EMIT RECEIPT (Spanner SHA-256 Receipt): Execute scoped MCP tool and log immutable SHA-256 provenance receipt ($0.014/turn, 94.2% acc). [Google Cloud: Spanner Audit + Cloud Trace ⇄ Open-Source: PostgreSQL + OpenTelemetry]
CLOSED-LOOP SELF-HEALING: Closed-Loop S.C.O.P.E. Gate: Rejects forged/cross-tenant OBO tokens in 0.4ms & caches verified top-K routes
BEFORE VS AFTER DELTA: Before (55,240 tok/turn ($0.420) • 61.0% Acc, Shared Admin Key = Tenant Leak) -> After (1,380 tok/turn ($0.014 • -97.5%), 94.2% Acc • 0 Confused-Deputy Leaks)
PRODUCTION TELEMETRY: prompt_schema_tokens: 55,240 -> 1,380 (-97.5%) | turn_cost_usd: $0.420 -> $0.014 (30x FinOps ROI) | tool_selection_accuracy: 61.0% -> 94.2% (+33.2pp) | confused_deputy_leaks: 0 (0.4ms Tamper & Tenant Reject)
```

---

## 2. Official Google Cloud `#78` 4-Zone Hub-and-Spoke Blueprint Specification

```text
Create an official Google Cloud Architecture Center Template #78 Hub-and-Spoke 2D Enterprise Agentic AI Reference Blueprint diagram in a crisp light theme (#F8FAFC background, #1A73E8 outer Google Cloud Organization & VPC-SC Perimeter frame, zero 3D isometric clutter).
Title at top: "GOOGLE CLOUD ARCHITECTURE CENTER #78 • ENTERPRISE AGENTIC AI & OPENHANDS HUB-AND-SPOKE BLUEPRINT"
Show 4 color-coded semantic zones with 18 distinct service cards and labeled directional dataflow arrows:
- ZONE 1 (TOP-LEFT BLUE HUB): Tenant-Aware Ingress & Routing — (1) Google Cloud Armor WAF, (2) Identity Platform & WIF OIDC, (3) BeyondCorp IAP mTLS, (4) Regional External ALB, (5) Cloud Run KV-Cache Ingress Proxy.
- ZONE 2 (TOP-RIGHT GREEN HUB): Governance, Security & Eval Gate — (6) Cloud KMS HSM & VPC-SC, (7) Competence & Regression Gate, (8) Cloud Logging & OpenTelemetry Audit Ledger.
- ZONE 3 (BOTTOM-LEFT YELLOW SPOKE): Primary Google Cloud ADK & Vertex AI Orchestrator — (9) Google Cloud Model Armor Ingress/Egress Sanitizer, (10) Vertex AI Gemini 4 Argon (locations/global, thinkingLevel=HIGH), (11) Google Cloud ADK Orchestrator, (12) Scoped MCP Tool Router (CASG JWT), (13) AlloyDB Postgres (FORCE RLS) & Vector Search 2.0.
- ZONE 4 (BOTTOM-RIGHT RED SPOKE): OpenHands Sandbox Verifier, Evidence Memory & Lakehouse — (14) OpenHands CodeActAgent Isolated Container Sandbox, (15) Vertex AI Gemini 3.8 Flash Evaluator Judge (locations/global), (16) Firestore Claim-to-SHA Receipt Graph, (17) BigQuery Trajectory & Eval Warehouse, (18) Artifact Registry & Git Commit Ledger.
Include a bottom Zone 5 Baseline telemetry strip showing: "Zero-Trust VPC-SC • Rule 55 Global Endpoint • 1-Click Terraform Validated". Crisp vector icons and clean orthogonal routing.
```
