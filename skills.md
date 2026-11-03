# 🧰 Multi-Project Workspace Skills & Engineering Protocols (`v3.16.0`)

This document defines the specialized autonomous engineering skills, forensic verification procedures, universal `skills.json` / `hooks.json` / `hooks.md` lockstep rules, and 5-Tier Google / Gemini / DeepMind model governance enforced across the `AskAIOCE`, `Demoes-GE`, `Zyvoriq`, `PromptCanvas`, `ScoreX`, `customer-tracker`, `a2a-enterprise-gateway`, and enterprise AI workspaces.

---

## 0. 🛡️ Universal Architectural & Cloud Run Deployment Constraints (All Current & New Projects)

You are configured to work on this repository with strict architectural and deployment constraints. Follow these instructions exactly:

1. **Planning & Immediate Same-Turn Execution (`Rule 28A`):** Formulate a concise 3 to 5 bullet execution plan and **immediately execute all file edits, backend syncs, and quality gates in the exact same turn**. NEVER output a plan or diagnostic gap list and stop to ask *"Shall I apply these fixes?"* or *"Would you like me to proceed?"*.
2. **Strict File Boundaries:**
* Only edit files directly required to complete the assigned task.
* Do not reformat, refactor, or delete unrelated files, functions, or utilities.
* Never edit or commit `.env` files, `.git` internals, or package lockfiles (`package-lock.json`, `poetry.lock`).
3. **No Hallucinations:** Use only verified, actively maintained libraries and standard APIs. Do not invent non-existent parameters, SDK methods, or placeholder mocks.
4. **Cloud Run Runtime Compliance:**
* Web services must listen on host `0.0.0.0`.
* Read the port dynamically from the `PORT` environment variable, defaulting to `8080` if not set. Never hardcode port numbers.
* Handle termination signals cleanly so existing connections finish before shutdown:
* In Node.js: `process.on('SIGTERM', ...)`
* In Python: `signal.signal(signal.SIGTERM, ...)`
5. **Quality and Test Gates:**
* Run local linting, type-checking, and unit tests immediately after modifying code.
* Fix all errors before presenting the task as complete.
6. **Deployment Targets:**
* When running deployment commands, strictly target the canonical project/region for the active service:
* **ScoreX (BeyondCorp `google.com` Canonical)**: Project `ramp-portal-dev` (`248990048888`), Region `us-west1`, Service `scorex` (`https://scorex-248990048888.cr.gclb.goog`)
* **ScoreX (Argolis Cloud Run)**: Project `cymbal-control-plane` (`638420508320`), Region `us-central1`, Services `scorex` (`https://scorex-638420508320.us-central1.run.app`) & `scorex-app` (`https://scorex-app-638420508320.us-central1.run.app`)
* **PromptCanvas (BeyondCorp `google.com` Canonical)**: Project `ramp-portal-dev` (`248990048888`), Region `us-west1`, Service `promptcanvas` (`https://promptcanvas-248990048888.cr.gclb.goog`; Artifact Registry build project: `cymbal-build-sandbox`)
```bash
# Rule 56 Mandatory Synchronous 2-Project Cloud Run Deployment Pipeline
bash scripts/deploy_scorex_cloudrun.sh
```

---

## 1. 🛡️ `anti-static-spoofing-and-subject-parity` (Rule 41 Verification Protocol — `v3.4.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying prompt routing (`src/app/api/generate/route.ts`, `src/lib/unifiedDiagramEngine.ts`, `src/lib/promptDrivenDiagramSynthesizer.ts`, `src/app/studio/page.tsx`, `src/lib/spec/livingSpecsGenerator.ts`), adding diagram templates, or handling layout-style keywords (`"infographic"`, `"tiered infographic"`, `"flowchart"`, `"swimlane"`, `"sequence diagram"`).

### Core Invariant (Zero Static Spoofing & Full Studio Sync)
- **Layout Archetype vs. Subject Domain Separation**:
  - Never confuse a **Visual Layout Archetype** (`4-Tier Architectural Infographic` or `L1–L4 Logical Flowchart`) with a **Static Content Template** (`Template #52: Context + Harness + Loop + Graph — Charlie Hills`, `Blueprint #01`, or `NOVACURA Biopharma`).
  - When a user prompt requests a layout style or bespoke domain architecture (e.g., `"Design a full Autonomous Drone Swarm Telemetry, LiDAR Edge Sensor Fusion & Real-Time Collision Avoidance Mesh architecture"` or `"Flowchart for Emergency Hospital Patient Triage, Rapid Blood Diagnostics, Sepsis Risk Gate & Automated ICU Bed Escalation"`), the system MUST NEVER spoof with hidden `1px` transparent divs (`font-size:1px;color:transparent`) or overwrite with static Blueprint `#00`/`#01` upon plan approval.
  - Bespoke architecture prompts in `adaptSavedGoogleCloudTemplateToPrompt` (`src/lib/promptDrivenDiagramSynthesizer.ts`) must extract domain clauses (`extractPromptDomainClauses`) and physically mutate Tier 3, Tier 4, and Tier 5 node cards with word-safe two-line wrapping (`formatTwoLineCardClause`).
  - Bespoke flowchart prompts in `generateLogicalFlowchartDrawioXml` (`src/lib/promptDrivenDiagramSynthesizer.ts`) must dynamically populate `[1]`, `[1a]`, `[2] ◆ Decision Gate`, `[2b]`, `[3]`, `[3a]`, and Tier 1–3 swimlane headers with the user's extracted steps.
  - `generateAll16LivingSpecs(ast, activeXml)` (`src/lib/spec/livingSpecsGenerator.ts`) must dynamically infer the project domain (`inferDomainLabel`), extract live `<mxCell vertex="1">` component titles from `activeXml`, and render a **Section 1.5 Live Synchronized Canvas Component Inventory** table.
  - Generic `"infographic"` requests must route to `generateDynamicTieredInfographicXml(prompt)` (`src/lib/canonical/dynamicTieredInfographic.ts`), which dynamically synthesizes the 4-tier infographic structure (`01 Ingestion` • `02 Harness` • `03 Validation` • `04 Graph`) populated 100% with the user's requested subject domain.

### Operational Verification Command
Run the automated Anti-Static-Spoofing & Subject Domain Parity Quality Gate:
```bash
npx tsx scripts/verify_export_slides_quality_gate.ts
```
This gate executes live synthesis against multiple arbitrary prompts (`"Healthcare FHIR Interoperability Infographic"`, `"Zero-Trust Kubernetes Security Infographic"`) and asserts:
1. Valid 4-tier structure (`TIER 01` through `TIER 04`).
2. 100% semantic subject noun parity in the rendered XML header and tier cards.
3. Zero leaked strings (`charlie hills`, `claude.md`, `novacura`).

---

## 2. 🔄 `governance-doc-lockstep-sync` (Universal Multi-Project Lockstep Gate — `v3.5.0`)

### Purpose & Trigger Conditions
Triggered automatically on every `git commit` (`.git/hooks/pre-commit`), every Jetski `Stop` lifecycle hook (`scripts/stop_quality_gate.mjs`), and `npm run test:tdd-all` (`scripts/tdd/run_governance_and_models_forensic_audit.mjs`).

### Core Protocol & Verification Command
Execute the SHA-256 single-source trinity verification script:
```bash
node scripts/guards/enforce_universal_single_source_trinity.mjs --verify-only
```
Asserts 100% symlink & byte-for-byte SHA-256 identity across all local project workspaces and `~/.gemini/config/`:
- `AGENTS.md` === `GEMINI.md` === `.agents/AGENTS.md` === `CLAUDE.md` === `~/.gemini/config/AGENTS.md`
- `skills.md` === `~/.gemini/config/skills.md`
- `skills.json` === `~/.gemini/config/skills.json` (72/72 installed skills with verified SHA-256 checksums: 21 DataCloud + 51 custom) and standalone `~/.gemini/config/skills/.datacloud_skills_manifest` (21/21 DataCloud-owned skills isolated from `googlecloudtools.datacloud` startup pruning)
- `hooks.json` === `.agents/hooks.json` === `plugins/zyvoriq_guard/hooks.json` === `~/.gemini/config/hooks.json`
- `plugins/zyvoriq_guard/plugin.json` === `~/.gemini/config/plugins/zyvoriq_guard/plugin.json`
- `skills` & `.agents/skills/*/SKILL.md` === `~/.gemini/config/skills/*/SKILL.md` (0 local-vs-global skill file drift, 0 stale `.shadow_backup` files)

---

## 3. 📊 `export-slides-and-docs-vector-parity` & `google-slides-refresh-token-bridge` (Native OpenXML DrawingML, PPTX Engine & Rule 47 Server-Side Google Workspace Bridge — `v3.14.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying `editablePptxCompiler.ts`, `editableDocxCompiler.ts`, `/api/export/cloud-bridge`, `src/lib/server/googleWorkspaceBridge.ts`, `src/data/cloud_viewer_manifest.json`, `src/components/DiagramInlineSlidesPreviewer.tsx`, or any `"Open with Google Slides"` / `"Open with Google Docs"` workflow across `PromptCanvas` and `blogs`.

### Core Protocol
- **PowerPoint / Google Slides (`editablePptxCompiler.ts`)**: 3-slide master deck (Slide 1: 1:1 Master Visual Twin, Slide 2: Decomposed Editable Vector Topology, Slide 3: Component Inventory Matrix).
- **Word / Google Docs (`editableDocxCompiler.ts`)**: 1-page widescreen landscape native OpenXML DrawingML (`<wpg:wgp>`) vector diagram with strict 4-layer back-to-front Z-ordering, `<a:noFill/>` transparent labels, pure vector service badges (`getServiceBadgeInfo`), and neighbor-clamped bottom labels (`minNeighborDist - 4`).
- **Rule 47 — Server-Side `refresh_token` Google Workspace Bridge vs. Browser GIS Popup Ban (`src/lib/server/googleWorkspaceBridge.ts` + `src/data/cloud_viewer_manifest.json`)**:
  - **Root Cause Why `blogs` Worked vs. Legacy `PromptCanvas` Failed**: Desktop/Installed-App OAuth credentials in `.gsheet_oauth_token.json` (`nitinagga@google.com`) cannot be used inside client-side browser GIS `google.accounts.oauth2.initTokenClient` popups due to Authorized JavaScript Origin mismatches (`origin_mismatch` / `popup_closed`) and unset `NEXT_PUBLIC_GOOGLE_CLIENT_ID` blockers.
  - **Mandatory Server-Side Refresh-Token Exchange & In-Place Drive `PATCH`**: Always exchange `grant_type=refresh_token` server-side at `https://oauth2.googleapis.com/token` (`getServerDriveAccessToken()` in `src/lib/server/googleWorkspaceBridge.ts` or `get_drive_access_token()` in `blogs/scripts/sync_google_workspace_bridge.py`), and upload `.pptx` to `https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true` (or `PATCH /upload/drive/v3/files/{preferredId}?uploadType=multipart` to update existing presentations in place) with `mimeType: "application/vnd.google-apps.presentation"` (never use Drive HTML multipart upload for Google Docs per `Rule 49`; always use `drive.files.copy` + `documents.batchUpdate`) and header `x-goog-user-project: "cymbal-build-sandbox"`.
  - **Pre-Warmed Google Drive Manifest (`0ms` Fast Path & Disk-Over-Memory Priority)**: Store verified `https://docs.google.com/presentation/d/<id>/edit` and `https://docs.google.com/document/d/<id>/edit` URLs in `src/data/cloud_viewer_manifest.json` (`GET /api/google-workspace/manifest` & `POST /api/google-workspace/open`), ensuring disk manifests override `globalThis.__pcCloudViewerManifestCache` and `ws1-*..ws5-*` map to `DOC-MT-01..DOC-MT-06`.
  - **Header-Only Action Controls, Zero-Ellipsis 6-Slide Deck & 100% Full-Width Diagram Canvas (`DiagramInlineSlidesPreviewer.tsx` + `editablePptxCompiler.ts`)**: Across `/dashboard`, `/library`, and `/blogs`, render **only** the compact header action controls (`👁️ Cloud Viewer` + `[ S | Open with Google Slides ↗ | ▼ ]` split-dropdown menu via `headerOnly={true}` with `manifestKey || diagramKey` precedence) while displaying the architecture diagram at 100% full width (`52px` intra-spoke connector channel with staggered elbows, zero on-page `1. EDITABLE SLIDE DECK PREVIEWER` box, zero native `title="..."` tooltip on `open-gcp-verify-drawer-btn`), and open the 3-mode Same-Screen Cloud Viewer Modal (`✨ Interactive Slides Studio` rendering all 6 slides `1:1` with `0` `…`/`...` ellipses, `🌐 Live Google Slides Embed`, `📄 Live Google Docs Spec`) on click.


---

## 4. 🖼️ `canonical-22-blueprint-google-cloud-certification` (Rule 43, Rule 53 & Rule 54 Production Google Cloud Catalog — `v3.18.0`)

### Purpose & Trigger Conditions
Triggered whenever creating, modifying, or auditing any of the **29 Production Google Cloud Blueprints** (`14` Core Architecture Blueprints: `#78`–`#84` L100–L400 Agentic Workspace / Principal Sequence / Oracle EBS R12.2 on Exadata X10M, `#00` 2026 Upgraded GCP & Gemini Enterprise Native Architecture, `#38` Cloud Landing Zone, `#42` Modern Data Lakehouse, `#44` Zero-Trust SOC, `#67`–`#69` Official Google Cloud Brand Light 7-Layer Flowcharts + `15` Infographic Templates `#52`–`#66` in `src/lib/canonicalTemplates.ts` and `src/lib/canonical/canonicalContracts.ts`), or updating catalog tile thumbnails in `public/templates/canonical_*.png`.
- **Pure White (`#FFFFFF`) Thumbnail & Canvas Background Invariant (`Rule 54`)**: All 29 `public/templates/canonical_*.png` catalog thumbnails (including `canonical_78.png`..`canonical_84.png`) must be rendered at `2x` resolution from the certified vector blueprints on a pure `#FFFFFF` white background with full unclipped bounds (`0` dark/black `#0A0F1D` backgrounds, `0` left/right margin cropping).
- **Semicolon-Safe RFC 2397 SVG Data-URI Invariant (`Rule 57B`)**: All inline `<img src="data:image/svg+xml,..."/>` and `shape=image;image=data:image/svg+xml,...` icons in `src/lib/canonical/oracleAtGoogleExadataEbsTopology.ts` (`ORACLE_EBS_ICONS`) and `src/lib/canonical/workstreamTopologyRenderers.ts` (`EXTRA_GCP_ICONS`) must use `'data:image/svg+xml,' + encodeURIComponent(svg).replace(/;/g, '%3B')` with `0` `;utf8,` substrings.

### Operational Verification Command
```bash
npx tsx scripts/verify_canonical_certification.ts && node scripts/verify_nav_badge_counts.mjs
```

---

## 5. 🧠 `5-tier-model-stack-and-universal-route-guard` (Rule 44 & Rule 46 — Unified 5-Tier AI Architecture — `v3.4.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying `src/lib/geminiConfig.ts`, `server/services/geminiService.js`, `app/api/swarm/*`, `src/lib/geminiRouteGuard.ts`, or any AI generation/mutation API route.

### Canonical 5-Tier Google / Gemini / DeepMind Model Stack (`GEMINI_MODELS`)
1. **Tier 0 / Tier 1: Omni 1.1 Master Orchestrator, Multi-Turn Video Synthesis & Multimodal Forensic Judge (`google-omni-1.1` / `models/gemini-omni-1.1-flash`)**
2. **Tier 1 / Tier 2: Deep Architectural Reasoning, Vision Decompilation, 16 Living Specs & Creative Surpass Direction (`gemini-3.1-pro-preview` / `models/gemini-3.1-pro-preview` / `gemini-4-argon` with `thinkingConfig: { thinkingLevel: "HIGH" }`)**
3. **Tier 2 / Tier 3: High-Throughput Sub-Second Structured JSON Compiler, Interactive Copilot, Intent Router & Prompt Enhancer (`gemini-3.8-flash` / `models/gemini-3.8-flash` / `models/gemini-3.1-flash` with `thinkingConfig: { thinkingLevel: "LOW" }` (`0` numeric `thinkingBudget` per `Rule 55`))**
4. **Tier 3 / Tier 4: Real-Time Bidirectional Voice & Video Canvas Co-Pilot (`gemini-3.1-flash-live-preview` / `models/gemini-3.1-flash-live-preview`)**
5. **Tier 4 / Tier 5: Native DeepMind Multimodal Media, Embeddings & Enterprise Mesh (`veo-3.1-generate-preview` • `lyria-3.5` • `models/lyria-3-pro-preview` • `gemini-3.1-flash-image-preview` • `models/imagen-3.0-generate-002` • `gemini-3.1-flash-tts-preview` • `text-embedding-005` • `gemini-embedding-001` • `BigQuery Property Graphs ISO GQL` • `Google ADK Sidecar` • `Gemini Data Analytics API` • `Google Cloud Model Armor`)**

### Core Invariants
- **Strict Deprecation Ban**: Zero hardcoded legacy or non-existent model strings in application route handlers, domain services, `.md` docs, `skills.json`, or `SKILL.md` files.
- **Universal Route Guard**: All 14 Gemini-backed API routes (including `POST /api/decompile-image`, `POST /api/generate`, `POST /api/chat`, `POST /api/compose`, `POST /api/diagrams/customize`, `POST /api/audit`, `POST /api/audit/remediate`, `POST /api/docgen/generate`, `POST /api/docgen/copilot`, `POST /api/export/terraform`, `POST /api/infographic-blueprint`, `POST /api/research-infographic`, `POST /api/studio1/generate`, `POST /api/generate/usecases`) must invoke `enforceGeminiRouteGuard(req, { endpoint })`.
- Every prompt-accepting endpoint must enforce the 4-category non-mutation conversational gate (`checkConversationalOrNonMutationIntent`).

---

## 6. 🏛️ `scorex-3-engine-maturity-and-forensic-governance` (ScoreX Enterprise Architecture, 20-Level Forensic Audit, 16 UI Integrity Gates & Zero Dead Code — `v3.8.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying ScoreX assessment routes, navigation (`client/src/components/GlobalNav.js`, `client/src/App.js`), backend assessment engines (`server/routes/dynamicAssessments.js`, `server/routes/dynamicAssessmentsCore.js`, `server/routes/geValueRealization.js`, `server/routes/euAiCompliance.js`, `server/routes/instanceVersions.js`, `server/utils/conversationalIntentGuard.js`), or seed datasets (`data/dynamic_assessments.json`, `data/ge_value_realization_dossiers.json`, `data/assessments.json`, `data/genai_assessments.json`).

### Core 3-Engine & 20-Level Forensic Architecture Invariants
ScoreX consolidates all technical maturity, business value, and regulatory compliance workflows onto **3 Canonical Assessment Engines** deployed on **Google Cloud Run (Canonical BeyondCorp URL: `https://scorex-248990048888.cr.gclb.goog` in `ramp-portal-dev` / `us-west1`, and Argolis: `https://scorex-638420508320.us-central1.run.app` & `https://scorex-app-638420508320.us-central1.run.app` in `cymbal-control-plane` / `us-central1`)**:
1. **Engine 1: Dynamic Assessment Blueprints Engine** (`/assessments`, `/assessments/hub`, `/assessments/ai-generator`, `/assessments/run/:typeKey`, `/assessments/run/instance/:instanceId`, `/assessments/report/:instanceId`) — Powers all **6 canonical production maturity frameworks** (`enterprise_data_ai_maturity` / `inst_enterprise_data_ai_maturity_demo`, `openai_to_gemini_enterprise_migration` / `inst_openai_to_gemini_enterprise_migration_demo`, `finops_cloud_cost_optimization` / `inst_finops_cloud_cost_optimization_demo`, `agentic_ai_mesh_mcp_banking_readiness` / `inst_agentic_ai_mesh_mcp_banking_readiness_demo`, `edw_lakehouse_to_bigquery_modernization` / `inst_edw_lakehouse_to_bigquery_modernization_demo`, `enterprise_ai_zero_trust_security` / `inst_enterprise_ai_zero_trust_security_demo`) with 6/6 complete `inst_*_demo` executive dossiers (`aiReport`, `executiveReport`, `financialAnalysis`, `slideDeckSynthesis`, `radarChartData`, `dimensionInsights`, `questionReadouts`, `architectureDiagrams`) and 0 phantom `"ScoreX Demo Workspace"` drafts.
2. **Engine 2: GE Value Realization Engine** (`/ge-value-realization`, `/roi-calculator`, `/tco-calculator`, with `/value-realization` redirecting to `/ge-value-realization`) — **82-Question / 10-Module (`C`·`P`·`A`·`W`·`T`·`Q`·`U`·`L`·`R`·`F`) / 8-Source Enterprise Evidence & Value Realization Framework** across all 10 pre-seeded enterprise dossiers (`ACC-1001-AEROVG`..`ACC-1010-BLDRGHT`, including `ACC-1006-VANGUARD` `Vanguard Global Advisory Corp`), featuring the 5-Column CFO Value Realization Matrix, 3-Horizon Roadmap, untruncated workflow pill/table titles, complete KPA `title` labels (`KPA-01`..`KPA-05`), and immutable `v1.0` Master Templates + cloned `v2.0+` Customer Instance Versions (`server/routes/instanceVersions.js`), powered by `Gemini 3.1 Pro` (`models/gemini-3.1-pro-preview`).
3. **Engine 3: EU AI Act Statutory Compliance Engine** (`/eu-ai-compliance/:id`, `/eu-ai-act`, `/eu-ai-act/system/:id`, `server/routes/euAiCompliance.js`) — **20 Statutory Questions** across the EU AI Act Risk Pyramid (Art. 5 Prohibited Practices, Art. 6/Annex III High-Risk AI Systems, Art. 50 Transparency, Art. 51–55 GPAI Systemic Risk), pre-seeded with `EUAIA-2026-HR4902` (`TalentPulse HR Screening & Candidate Ranking AI`) and Annex IV Technical Documentation generator powered by `Gemini 3.1 Pro` (`models/gemini-3.1-pro-preview`) and audited by `Google Omni 1.1` (`google-omni-1.1`).
4. **4-Category Conversational Non-Mutation Guard (`server/utils/conversationalIntentGuard.js`)**: Enforced across all 4 prompt endpoints (`POST /api/dynamic-assessments/generate-framework`, `POST /api/dynamic-assessments/instances/:id/generate-diagrams`, `POST /api/chat/message`, `POST /api/eu-ai-act/systems/:id/copilot`) so greetings (`"Hi"`), identity queries (`"who are you"`), courtesies (`"thanks"`), and short ambiguous prompts (`"scale"`) return `isConversational: true` with zero framework/diagram mutations.
5. **Unblocked Demo Workspace Mutations & Parameter-Preserving Legacy Redirects**: All 7 demo workspace operations (`generate-terraform`, `share-link`, `clone`, `promote-as-type`, `DELETE /instances/:id`, `suggest-questions`, `regenerate-workflow-assets`), `GET /instances` query filtering (`customerName`, `typeKey`, `search`, `status`, `limit`, `offset`), fuzzy portfolio-rollup matching, and parameter-preserving `<LegacyReportRedirect />` / `<LegacyRunnerRedirect />` routes are active with zero dead legacy `navigate()` calls.
6. **Template 05 3-Zone Architecture Diagram Semantic, Logical & Visual Integrity Gate (`server/services/dynamicAssessmentDiagramCompiler.js` ↔ `client/src/services/template05DiagramCompiler.js`)**:
   - **Hyphen-Safe Semantic Compression & Zero `..` Truncations**: `concisePillarLabel()` and `concisePainPoint()` split strictly on whitespace (`/\s+/`), never on intra-word hyphens (`/`[\s-]+`/` is banned), mapping all 36 framework pillars and 36 primary pain badges across all 6 canonical blueprints to complete, untruncated phrases (`0` `..` substrings across all 18 Stage 1/2/3 Draw.io XMLs and all `template05Overrides` keys).
   - **100% Unique As-Is Pain Badges (`l_pain_0..l_pain_5`)**: Pillar-specific `theBad` and `questionsMeta.technicalPainPoints` take strict precedence over global pain pools, followed by a `Set`-backed deduplication pass (`usedPainLabels`) guaranteeing `6/6` unique pain badges per assessment.
   - **Bijective 1-to-1 Horizontal Tier-to-Bridge Alignment (`assignPillarsToArchitecturalTiers`)**: Every assessment's 6 pillars map bijectively onto `L1 CHANNELS` (`01`), `L2 WORKBENCH` (`02`), `L3 DATA & MEM` (`03`), `L4 EVENT MESH` (`04`), `L5 CLOUD INFRA` (`05`), and `L6 ZERO-TRUST` (`06`) so horizontal arrows `m_flow_in_0..5` and `m_flow_out_0..5` connect matching architectural layers left-to-right.
   - **100% Domain-Differentiated Left Zone, Right Zone (`toBeCylinders`, `toBeIntegration`) & Bottom Strips + Unskewed Composite Math**: All 6 canonical frameworks render domain-specific As-Is rows, To-Be Tier 3 cylinders & Tier 4 hexagons, 12 Enablers, and 5 Outcomes; `avgCur`/`avgMid`/`avgTgt` are computed strictly from evaluated rubric dimensions before appending any visual symmetry slot (`isSyntheticSymmetrySlot: true`).
   - **Server ↔ Client Compiler Lockstep**: `server/services/dynamicAssessmentDiagramCompiler.js` and `client/src/services/template05DiagramCompiler.js` are verified byte-identical (normalizing module exports) on every `quality-gate` and `Stop` hook execution.
7. **ScoreX Value Realization Executive UX, Data Grounding, Forensic 5-Subsystem Completeness, Single-Source Framework, Durable GCS State & `CI=true` Build Invariants (`Rule 50A`–`Rule 50L` / `L60-01`..`L60-21` / `UI Integrity Gates 1–20`)**:
   - **100% Fluid Edge-to-Edge Layout Invariant (`Rule 50A` / `Rule 25G`)**: Banning rigid `max-width: 900px..1560px` containers in favor of full-width responsive layouts (`width: 100%; max-width: 100%; padding: ... clamp(16px, 1.8vw, 28px);`) aligned with global navigation across all ScoreX component pages. Available horizontal header space must be filled with live 4-metric Telemetry Grounding clusters (`Grounded`, `Verified`, `Pending`, `Confidence`).
   - **Zero Third-Party Consulting Brand Hallucinations (`Rule 50B` / `Rule 25I`)**: Zero occurrences of `McKinsey & Google`, `McKinsey`, `BCG`, `Bain`, `Stratagem`, `Deloitte`, `Quantiphi`, `Accenture`, `PwC`, `Slalom`, or `KPMG` (`ACC-1006-VANGUARD` `Vanguard Global Advisory Corp` replaces `ACC-1006-STRATGM`) across `client/src/`, `server/`, `data/`, and reports. Always use pure first-party Google Cloud / Gemini Enterprise or neutral executive labels (`2. Executive Readout`).
   - **Strict Sequential Question Ordering & Functional 3-Tab DOM (`Rule 50C` / `Rule 25H`)**: Cards must follow strict numerical order (`C01` $\rightarrow$ `C02` $\rightarrow$ `C03`). All UI tabs (Inputs, Executive Readout, Provenance Ledger) must be active interactive DOM surfaces; print/PDF exports must automatically target the executive readout view.
   - **Verified Cross-Customer Data Isolation (`Rule 50E` / `Rule 25L`)**: Enforcing authentic CRM metrics and accounts for Mars, Inc. (`50,000` seats, `16,500` WAU), H-E-B, LP (`45,000` seats, `14,200` WAU), Elevance Health, Pfizer, and Global Biopharma with zero silent fallbacks or cross-customer data bleed.
   - **Forensic Mathematical, Logical, Factual & Completeness Invariants Across All 5 Subsystems, Single-Source Framework, Durable GCS CAS State & `CI=true` Build (`Rule 50H`–`Rule 50L` / `L60-14`..`L60-21` / `UI Integrity Gates 14–20`)**: (1) Synchronous atomic primary JSON write in `server/utils/dataStore.js` paired with `server/utils/durableGcsPersistence.js` pre-boot cold-start hydration, `?ifGenerationMatch` optimistic CAS preconditions, `HTTP 412` 3-way structural ancestor merge (`threeWayMergeJsonState`), and `DataStore` peer hot-reload (`refreshChangedFilesFromGcs`) to versioned `gs://scorex-durable-state-bbar-138hf0` across all 15 managed JSON stores + `ge_value_realization_dossiers` / `eu_ai_dossiers` PostgreSQL JSONB tables (`Gate 20`); (2) Pure V8-native `require(esm)` single-source `server/data/geValueRealizationFramework.js` on Node 22 LTS (`0` regex transpiler) re-exporting `client/src/data/geValueRealizationFramework.js` (`Gate 19`) and `82/82` answered + option-matched questions across all 10 GE Value Realization customer dossiers (`ACC-1001-AEROVG`..`ACC-1010-BLDRGHT`) and 5 preset keys; (3) All 6 Dynamic Assessments have exact arithmetic-mean `totalScore` (`edw_lakehouse_to_bigquery_modernization === 2.63`) and 6 distinct scores; (4) All 4 Core 6-Pillar Assessments have `6/6` `selectedPillars` and 4 distinct calculated scores (`2.58`, `2.88`, `3.20`, `3.00`); (5) All 3 GenAI Readiness Assessments have `30/30` answered questions and distinct maturity scores (`113/160`, `108/160`, `80/160`); and (6) Strict `CI=true react-scripts build` (`0` ESLint warnings across all client files), `F01 = $120/hr ($187,200/yr fully loaded)` rate parity, dynamic Exhibit 1B financial math, progressive-disclosure skill `scorex-forensic-gate` (`references/rule50_forensic_checklist.md`), Markdown Subagent `scorex-forensic-auditor.md`, and native Jetski lifecycle hook `scripts/guards/jetski_hook_handler.mjs`.

---

## 7. 🎬 `zyvoriq-generative-cinema-and-music-video-swarm` (Zyvoriq 12-Agent Studio Architecture & 10 Cross-Agent Invariants — `v3.5.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying Zyvoriq studio workflows (`app/swarm-MUI/page.tsx`, `app/personas/page.tsx`, `components/LeftIconRail.tsx`), backend swarm routes (`app/api/swarm/*`), or multi-turn video/audio synthesis pipelines (`lib/swarm/*`, `lib/studioCatalog.ts`).

### Core Zero-Hardcoding & 12-Agent Creative Surpass Architecture
1. **3-Stage Creative Surpass Compiler (`Deconstruct -> Elevate -> Surpass`)**:
   - Powered by `POST /api/swarm/synthesize-from-prompt` (`models/gemini-3.8-flash` with `thinkingConfig: { thinkingLevel: "LOW" }` (`0` numeric `thinkingBudget` per `Rule 55`) & Pass 2 Judge `models/gemini-4-argon` with `thinkingLevel: "HIGH"` -> `models/gemini-3.1-pro-preview`) and `POST /api/swarm/jobs` (`models/gemini-3.8-flash-tts` verbatim transcript contract -> `models/gemini-3.1-flash-tts-preview`).
   - Automatically detects YouTube URLs (`youtube.com/watch?v=...`, `youtu.be/...`, `youtube.com/shorts/...`), scrapes real title/channel/keywords/thumbnail, deconstructs the emotional hook, diagnoses 3 reference-specific scene/staging limitations (zero canned parroted boilerplate), and synthesizes a clean 2-Act narrative `storyline` (zero raw URL echo) + 12-Agent Production Bible that surpasses the reference across all 10 Cross-Agent Invariants (`10.0 / 10`).
2. **12-Agent Dance Music Video Swarm & 10 Deterministic Cross-Agent Invariants (`audit12AgentBlueprintConsistency`)**:
   - `01. Script Agent`: Clean 2-Act narrative logline (zero raw URL) + 3 reference-specific scene limitations.
   - `02. Casting Agent`: All 6 personas (`female_lead`, `female_harmony`, `male_lead`, `supporting`, `background`, `audience`) locked with 6 unique culturally-clustered biometric portraits (`PORTRAIT_POOL`).
   - `03. Wardrobe Agent`: All 5 cast tiers evolve from `Act I (0:00–0:30)` $\rightarrow$ `Act II (0:30–1:00)` + Figure-Ground HSV Contrast Lock ($\ge 35\%$ separation).
   - `04. Location Agent`: Dual-Act spatial metamorphosis (`Act I Venue -> Act II Venue`) anchored to reference geography.
   - `05. Prop Agent`: Per-tier footwear, statement jewelry, hair physics, live musician instruments & Act II kinetic props.
   - `06. Choreography Agent`: 6-shot kinetic progression with distinct lead vs. 8-dancer geometric formations and Act II climax elevation.
   - `07. Acting & Facial Agent`: Dual-Mode Active Vocalist Viseme (`r >= 0.72` mouth-aperture-to-audio envelope correlation on singing leads) + Non-Singing Ensemble Closed-Lips (`RMS <= 0.015`, Nayan-Abhinaya eye emotion).
   - `08. Lighting & Camera Agent`: 6-shot focal length (`mm`), T-stop, rig movement & Kelvin/CRI lighting schedule.
   - `09. Narration & Lyric Agent`: 60s lyric sheet with `[Female Lead]`, `[Male Lead]`, and `[Female Co-Lead]` harmony hooks + locked BPM & musical key.
   - `10. Music & Acoustic Agent`: `models/lyria-3-pro-preview` 48kHz `-14.0 LUFS` master with locked BPM/key grid & real instruments.
   - `11. Cinematography & Assembly Agent`: `status = "PRE_FLIGHT_LOCKED"` pre-render (`"COMPLETED"` only after physical `.mp4` render).
   - `12. Forensic QA Judge Agent`: Computes real `10.0 / 10 (10/10 Cross-Agent Invariants Passed)` via `audit12AgentBlueprintConsistency(ctx)` (`status = "PRE_FLIGHT_LOCKED"` pre-render, zero hardcoded `"9.8 / 10"` rubber-stamping).
3. **4 Canonical Active API Routes & 3 Core Studio Workflows + `/personas` Biometric Hub**:
   - Routes: `POST /api/swarm/synthesize-from-prompt`, `POST & GET /api/swarm/jobs`, `POST & GET /api/swarm/avatar-builder`, `GET /api/swarm/library`.
   - Workflows: `create` (4-Step Studio + `Crew (12)` tab), `published` (Published Reels), `wip` (Drafts & Render Jobs), `/personas` (6-Persona Biometric Hub).

---

## 8. 🎓 `demoes-ge-codelabs-and-4-pillar-decision-engine` (Gemini Enterprise L0–L4 Codelab, 4-Pillar Decision Engine, Fresh Version+Timestamp Ledger & Independent LLM-as-a-Judge — `v3.6.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying `/Users/nitinagga/Documents/Demoes-GE` (`src/codelab-generator/*`, `src/demo-generator/*`, `src/mcp-server/*`, `src/veeva-mcp-server/*`), adding enterprise connectors, or planning custom use-case demos across **Enterprise Connectors (`Ingestion` • `Federation` • `MCP`)**, **Agent Designer V2**, **Enterprise SKILLS**, and **NotebookLM Enterprise**.

### Core Invariants
1. **L0–L4 Rollup & Drill-Down Hierarchy & Dedicated Connector Workbenches**:
   - `L0 Enterprise Portfolio` (4 Pillars, 4 Connectors, 60 Globally Unique Screenshots) $\rightarrow$ `L1 Industry Vertical` $\rightarrow$ `L2 Connector [Ingestion | Federation | MCP]` $\rightarrow$ `L3 Chapter (1..6)` $\rightarrow$ `L4 Atomic Step (1..15)`, including dedicated `#tab-jira` (`Atlassian Jira & Confluence Cloud Connector Deep Dive & Live MCP Workbench` across Architecture, Security & Compliance, Functionality, and Execution & 30-60-90 Roadmap with `jira_search_issues`, `confluence_get_page`, `jira_transition_issue`, and `jira_add_comment`).
2. **Real Live GE (`ucs-widget.corp.google.com`) & Google Cloud Console (`console.cloud.google.com`) Light-Mode Screenshots Only — Codelab App is Strictly a Container/Viewer**:
   - The Codelab web app (`http://localhost:4318`) is purely a **container/viewer** that stores and presents **15 real, relevant, accurate, and complete Light-Mode screenshots** captured directly from the **actual Google Cloud Console** (`https://console.cloud.google.com/gen-app-builder/engines` & `data-stores`) and the **actual Gemini Enterprise environment** (`https://ucs-widget.corp.google.com/home/cid/fdd1e98d-1f52-4407-98fd-80e27c61fbc9?e=SparkDogfoodLaunch%3A%3ALaunch`).
   - **Strict Ban on Synthetic HTML Slides & App-Self Screenshots**: Never use synthetic `page.setContent(...)` HTML slides and never screenshot the Codelab App UI (`localhost:4318`) itself as a demo step screenshot. Never switch from Light Mode to Dark Mode mid-way through a walkthrough.
3. **Fresh Demo Generation & Monotonic Version + ISO Timestamp Ledger (`mintFreshDemoVersionWithTimestamp`)**:
   - Whenever generating a new demo or updating an existing one, everything is freshly generated and stamped via `mintFreshDemoVersionWithTimestamp(demoTitleOrTopic, session)` (`src/codelab-generator/engine.mjs`), backed by `data/demo_version_ledger.json` and `screenshots/runs/<slug>_<versionTag>/version_manifest.json` (`v1.0-<ISO_TS>` for new demos; `v2.0-<ISO_TS>`, `v3.0-<ISO_TS>` for updates).
4. **Zero Unrequested Assumptions & Pure Agent Designer + `SKILL.md` Orchestration**:
   - Never assume or inject `MCP`, `ServiceNow`, `SharePoint`, or `Jira` when not requested in the prompt. For the Meeting Lifecycle Agent (*"Build an Agent That Prepares, Summarizes and Follows Up"*), orchestrate strictly via **Agent Designer V2 (Subagents)** + **Enterprise SKILLS** (`gcalendar`, `gdrive`, `gdocs`, `gsheets`, `gslides`, `gmail`, `gchat` + custom `SKILL.md` packages in `.agents/skills/meeting-prep-briefing/SKILL.md`, `.agents/skills/meeting-transcript-summarizer/SKILL.md`, and `.agents/skills/meeting-followup-dispatcher/SKILL.md`).
5. **Independent LLM-as-a-Judge !== Generator Model Separation (Zero Self-Grading)**:
   - **Generator Models (author the report/codelab plan from inputs)**: `models/gemini-3.1-pro-preview` + `models/gemini-3.8-flash` (`locations/global`, `thinkingLevel: "LOW"`).
   - **Independent LLM-as-a-Judge Models (audit the generated report & real screenshots)**: `models/gemini-4-argon` (`thinkingLevel: "HIGH"`, `temp=0.0`) + `google-omni-1.1` (`models/gemini-omni-1.1-flash`) + `models/gemini-3.1-pro-vision`.
6. **8-Pillar Harness Engineering Self-Test (`GET /api/codelab/harness-status`) & 6-Dimension Forensic Gate**:
   - Every change must pass `npm run test:tdd-all` (`Piece 1` + `Piece 2` + `Piece 3` + `run_codelab_forensic_audit.mjs`), verifying 8/8 Harness Engineering Pillars (`L1 Pre-Flight`, `L2 In-Flight`, `L3 Post-Flight`), 60/60 unique assets, zero 2D bounding-box collisions, zero slanted SVG lines, 4-case conversational fuzzing non-mutation, 100% Cloud DLP redaction (`DLP_REDACTED_CERTIFIED`), and 100% local-vs-Gemini governance lockstep.


---

## 9. 🛡️ `customer-lineage-forensic-guard` (GantryPulse / Customer-Tracker 6-Dimension Forensic, Dual-Sheet EAP Governance, Zero-Assumption, Disjoint Judge, Link Provenance & Canonical Google Chat Space ID Gate — `v4.1.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying `/Users/nitinagga/Documents/gantry-pulse` (`src/data/lineageData.ts`, `src/data/eapTrackerData.ts`, `src/data/momaDirectory.ts`, `src/types/lineage.ts`, `src/components/*`, `scripts/pre_tool_lineage_guard.mjs`, `scripts/stop_forensic_gate.mjs`, `scratch/e2e_forensic_audit_runner.mjs`), reconciling Buganizer / Salesforce / Gantry / EAP records, or auditing enterprise customer lineage and EAP preview trackers.

### Core Invariants
1. **Deterministic Buganizer `compId` Role Classification & Detectr Blocklist**:
   - `TAM` (`compId = 1891061`), `CR` (`compId = 841988`), `CB` (`compId = 550983`), `Engg` (`compId ∉ {1891061, 841988, 550983, 2120237}`). Strictly purge `compId = 2120237` (`Detectr` internal static security scanner bot bugs).
2. **Disjoint Report Generator vs. Independent LLM-as-a-Judge Separation of Duties (`governanceRole` & `evaluatedBy`)**:
   - `INDEPENDENT JUDGE`: **Google Omni 1.1** (`google-omni-1.1 / gemini-omni-1.1-flash`, Cross-Family Multimodal Forensic Judge), **Gemini 3.1 Pro Vision** (`gemini-3.1-pro-vision`, Visual & Spatial DOM Judge), and **Google Cloud Model Armor** (`model-armor-v1`, Independent Safety & Isolation Judge). Never author report text; strictly audit generators.
   - `DETERMINISTIC VERIFIER`: **BigQuery Property Graphs (ISO GQL)** (`1-to-1` `primaryId` graph parity verifier), **NotebookLM Enterprise** (citation-locked grounding verifier), **Gemini Embedding 001 & Text Embedding 005** (`>= 0.88` cosine similarity verifier), and **Google ADK 4-Agent Sidecar + Stop Forensic Gate**.
   - `REPORT GENERATOR`: **Gemini 3.1 Pro**, **Gemini 3.8 Flash**, **Gemini Flash Live**, **Gemini Enterprise**, **Agent Designer 2.0**, **AI Co-Scientist**, **Gemini Data Analytics API**, **DeepMind Neural Audio & Lyria 3.5**, **Veo 3.1 & Imagen 3**.
3. **22-Rule Pre-Flight Data, Model, Zero-Assumption, Link Provenance, Canonical Google Chat Space ID & 6-Sensor UI/UX Guardrail Checklist (`v4.1.0`)**:
   - Enforces `202/202` unique primary keys (`0` duplicates), Any-1-Pillar OR Gate (`202/202`), 100% scalar-to-array parity, zero mid-word `...`/`…` truncation across top-level and nested arrays, live Gantry API join (`7` active intakes), 100% 4-Tier `L4 -> L3 -> L2 -> L1` taxonomy coverage, Zero-Assumption financial & system grounding (`$32.64M` ARR / `$97.92M` TCV, `75,000` seats across all `202` rows, `0` fabricated `nativeStatuses.sfdc` on Buganizer-only rows, `0` synthetic `LiveSoT!A1`/`SFDC` sheet refs on direct-API rows with Tab 8 rendering strictly the `100` verified Sheet A/B rows, explicit `Awaiting Eng ETA` when unscheduled), cross-customer `[OtherCustomer]` bracket stripping, 0 confidential git leaks, 17-entry `CANONICAL_GOOGLE_DEEPMIND_MODEL_MATRIX` (`models/lyria-3-pro-preview`, zero legacy preview TTS models), `0px` horizontal table overflow at `1600px`, above-the-fold first data row (`Y <= 360px` on Tab 0 & Tab 11), zero dead-end placeholder controls, single global search input (zero duplicate tab-local search inputs), plain-English UI copy hygiene, **Sensor 5 (`2,520 / 2,520` live DOM deep links verified across all 12 tabs, `0` `example.com` links, `0` empty hrefs)**, and **Sensor 6 (`Dual-Sheet EAP & Preview Governance` on Tab 11 reconciling Link 1 `22` rows + Link 2 `17 + 10 = 27` rows from `.local_backup/local_eap_records.json` with `4 === 4` Wave 1 allowlist parity, `9 === 9` dynamic `DRIFT_OR_GAP` audit log entries, and 100% `/^LIN-\d{4}$/` foreign-key lineage integrity)**.
4. **Lineage Template Ingestion & Scalar-to-Array Isolation Invariant (`Rule 17`)**:
   - When ingesting, scaffolding, or cloning lineage records (`LIN-XXXX`), scalar fields (`enggBugId`, `blockedOn`, `category`, `productComponent`, `hpsScore`) must NEVER be copied blindly from template rows (`LIN-0001`).
   - **Scalar-to-Array Referential Parity**: `enggBugId` can ONLY be populated if there is an active matching engineering ticket in `engBugs` (`r.enggBugId === r.engBugs[i].id`). If `engBugs` is empty, `enggBugId` MUST be `""`. Zero occurrences of ungrounded bug IDs (such as `524778586` across `LIN-0161..LIN-0174`).
   - `blockedOn` must never carry cloned template strings (e.g. `"End User Sharing via WIF Groups UUID in Agent Designer Agent"`) across unrelated tickets. Blocker strings must strictly reflect verified issue-specific blockers (e.g., `LIN-0062` blocked on `b/489866043`, `LIN-0063` blocked on `b/486858596`, both assigned to `ericsma` per ground truth).
5. **EAP POC Anti-Hallucination, Directory Integrity & Storage Key v3 Lockstep (`Rule 18`)**:
   - **Customer POC Protection**: Customer contact fields (`customerBusinessPoc`, `customerItPoc`) must strictly store verified human customer stakeholder names (e.g. `Pema Sherpa`, `Zachary Pinner`, `SathishKumar JaiShankar`) and NEVER undergo LDAP extraction or conversion to `@ldap` handles (`0` occurrences of `@dsciences`, `@zfucik`, `@dteams`, `@cleads`, `@acompliance`).
   - **Zero Synthetic LDAP Slugs**: Directory normalizers (`normalizeToCanonicalLdap`) must reject non-person organizational keywords, headers, and instructions (`"Cloud AI OPM"`, `"See Link 1 Master EAP SoT"`, `"Mobile Client"`, `"Frontend Experience"`, `"Core Developer Platform"`), and NEVER generate synthetic 2-letter slugs (`words[0][0] + words[last]` -> `@copm`, `@smaster`).
   - **Multi-POC Preservation**: Multi-person Google POC strings (e.g., `"Jessica Faibish / Nick Stalf"`, `"Yeye Zhang Adam Fisher"`, `"Eric Peters / Sujay Solomon"`) must parse all constituent contacts and preserve all canonical LDAPs (`@jfaibish, @nstalf`, `@yeyezhang, @adamfisher`), never dropping or truncating secondary contacts.
   - **Client Cache Version Lockstep**: `STORAGE_KEY_EAP_PAYLOAD` must be locked to `'customer_eap_tracker_payload_v4'` (or higher, `0` legacy `v1`/`v2`/`v3` keys per `Rule 30D`) across `src/data/eapTrackerData.ts`, `src/components/EapFeaturesTrackerTab.tsx`, and `src/components/DailyOutreachBriefPanel.tsx` to immediately invalidate legacy client-side caches containing corrupted POC handles.
6. **EAP Proof Link Classification & Valid Moma Base URL (`Rule 19`)**:
   - Enforces strict domain/path validation on EAP proof links (`formatBugOrGantryLinkLabel`, `formatFormLinkLabel`, `isGoogleFormResource`) and valid `https://` `systemUrls.momaBase`.
7. **Permanent Anti-Hallucination, Route Preservation, CustomEvent Parity & Truthful Sync Attestation Gate (`Rule 20`)**:
   - **Zero Synthetic Directory Keys**: Blocks `dsciences`, `zfucik`, `dteams`, `cleads`, `acompliance`, `copm`, `smaster` both as `@`-handles and as object keys across `src/`.
   - **CustomEvent Dispatch ↔ Listener Parity**: Every `new CustomEvent('<name>')` dispatched in `src/` (including `gantry-open-moma-card`, `gantry-open-ticket-logger`, `gantry-ticket-mutation`, `gantry-live-ticket-refreshed`, `gantry-force-refresh-all-caches`, `gantry-gsheet-cell-override-updated`, `gantry-gsheet-external-pull-delta`) must have at least one active `addEventListener('<name>')` in `src/`.
   - **Route Preservation & Workspace 3 Reachability**: `resolveValidTabId` in `src/App.tsx` must preserve all 17 `WorkbookTabId` routes without hijacking `gemini_spec`, `master_lineage`, or `raw_*` to `certified_sot`, and must render both `Master Lineage View Mode Switcher` (`2A–2C`) and `System Pillars Switcher` (`3A–3E`) in the sub-view switcher bar.
   - **Truthful 2-Way Sheet Sync Attestation**: Local UI mutations must initialize with `syncStatus: 'Pending Push (UI Ahead)'` and promote to `'2-Way Synced (UI ↔ Sheet)'` only after `/api/gsheet/push-cell` or `/api/gsheet/changelog` returns `ok: true`.
   - **Zero Hardcoded Seat/Taxonomy/Badge Drift**: Blocks `seats: 5000`, `taxonomyL4_Exec: 'Cloud AI'`, `'6 AI'` / `'6-Model Matrix'`, and dead `confirmingReset` state in `src/App.tsx`.
8. **Link Provenance, Deduplication, Row-Anchor & Target Integrity Gate (`Rule 21`)**:
   - **Gantry Intake URL Purity**: `gantryIntakeUrls` must strictly contain Gantry Portal URLs (`https://gantry-portal-...`), never Buganizer issue links (`issues/...`).
   - **Zero Redundant Array Duplication**: `link1BugLinkSoTUrls` and `link1NominationFormSoTLinks` must have zero overlap with `trackingBugLinks` and `nominationFormLinks`.
   - **Mandatory `&range=A<row>` Coordinate Anchors**: Every Google Sheet link in `nominationFormLinks` and `local_three_pages_records.json` must include an explicit `&range=A<row>` coordinate anchor; `nominationFormLinks` must never contain the main Link 1 Catalog (`gid=605770031`).
   - **Cross-EAP Doc Provenance & Specific Room/Launch Routing**: `1khmkcFqDV0Hi01W5xpEADX1Mgnr1a6OZTqDJc1cu_Ls` belongs exclusively to `EAP-14`, `1UsxqRw_H-e41vIpAjFUQ_BoaL25KgCskTqLtpcyVHAY` belongs exclusively to `EAP-09`, Co-Scientist lineage row is `LIN-0053` (never `LIN-0083`), numeric Launch/Ariane IDs route to `/launch/<id>` URLs, and Google Chat links route to room-specific `https://chat.google.com/room/...` URLs.
9. **Canonical Google Chat Space ID, Upstream Hyperlink Parity & Zero-Synthetic-Slug Gate (`Rule 22`)**:
   - **Canonical 11-Character Space ID Grammar & Chrome-History Allowlist**: Every `chat.google.com` room or thread URL across `src/` and `.local_backup/*.json` must use a verified 11-character base64 Space ID (`AAQANt8nIBk`, `AAQAXtyj_Lg`, `AAQA40Z_m7c`, `AAQAWHhHB1o`, `AAQAn7ayJog`, etc., `0` unvisited/restricted spaces `AAQAkGiKOu4`, `AAQAfZfzOlY`, `AAQAQnUtrsQ`, `AAQAgkYgsq8`, `AAQAMkrhPuA`, `AAQA75yrDS4`, `AAQAel2m3f0`, `AAQA1EdWqJA`, `AAQAauVlkLU`, `AAAAaTuHElQ`) or verified DM thread ID (`0qwryyAAAAE`); synthetic camelCase slugs (`AAAAgantryCbWarRoom`) and invalid `/dm/<email>` URLs are hard-blocked.
   - **100% Upstream Link 1 Hyperlink Parity**: All 10 upstream `chat.google.com` hyperlinks in `.local_backup/eap_rich_links.json` must be present in `.local_backup/local_eap_records.json` (`link1CommunityChatLinks`) and rendered via `formatChatLinkLabel` in `src/components/EapFeaturesTrackerTab.tsx`.
10. **6-Column Domain Isolation, Runtime-First SoT Priority, Full 33-Column `A:AG` Sheet Read & Real `<2m` (`15s`/`30s`/`60s`/`90s`, `0` `5m`) Polling Gate (`Rule 23` & `Rule 30`)**:
    - **6-Column Domain-Isolated Schema (`Option A`: `18% | 15% | 15% | 16% | 16% | 20%`)**: Enforces `1. Topic, Description & Summary`, `2. Customer Environments Status`, `3. Forms, Docs & Proofs`, `4. Emails, Chat Spaces & Owners`, `5. Tickets (SFDC · TAM · CR · CB · ENG · Gantry)`, and `6. Current Status, Ask & Next Steps` in `src/components/EapFeaturesTrackerTab.tsx`.
    - **Zero Fake Refresh Clocks & Real `<2m` Polling**: Bans `setLiveRefreshDate(new Date())` local clock tickers; enforces `pollEapStatusFromServer` (`GET /api/eap-tracker/status` every `60s`) and `pollUpstreamSheetReconciliation` (`POST /api/eap-tracker/sync` every `90s`, `<2m` auto-refresh per `Rule 30` with `0` `5m` intervals), runtime-first field precedence (`r.field || can.field`) in `src/data/eapTrackerData.ts`, full 33-column (`A:AG`) verification in `gsheet_sync_server.py`, and 1-click `"📧 Email Customer (HTML)"` rich 5-column table composer modals across Pages 1–6 (`syncCustomerHtmlWithEditedPlain`, `cleanForCustomerEyes`, `whatToTellCustomerOverride`).
11. **Canonical Moma FQDN, ResourceKey Preservation, `/room/` Chat Normalization, Verified Customer POCs, Zero Fake Spreadsheet/Environment IDs & Top-Level `sfdcUrl` Parity Gate (`Rule 24` & `Rule 30D`)**:
    - Enforces `${systemUrls.momaBase}/person/<ldap>` across all 256 Moma profiles (`0` `https://moma-directory/person/` URLs), bans `http://mb/sf/` and `href="#"` fallbacks, preserves `?resourcekey=` on all 18 restricted Google Workspace file IDs, normalizes all Google Chat URLs to `/room/<id>` (`0` `/app/chat/` or `AAQAyooJqkE`), blocks hallucinated customer contacts (`diantha.ratnayake`, `anissa.meziane`, `Jan Krcmarik`, `Zdenek Fucik`, `Petr Kolar`, `Tomas Krcmarik`, `Dr. Iya Khalil`, `Adrian Jones`, `Dave Maraldo`, `Perez`), fake spreadsheet/environment IDs, and synthetic tickets (`75889102`, `569102441`, `75026353`), enforces `54/54` top-level `sfdcUrl` parity in `.local_backup/local_lineage_records.json`, and maps all URL tab aliases in `resolveValidTabId`.
12. **Executive IA, Table Cell Containment, Unified Upstream Portal Synchronizer, 5-Sheet Google Sheets v4 Reconciliation, 6-Hop Direct-SoT Sync (18-Char SFDC Record ID Resolution + Per-Row & Global Buganizer/SFDC Refresh + Subprocess Mutex Coalescing + Scoped CORS + IPI Sanitization) Across All 18 Pages, Zero Umbrella-EAP Environment Bleed-Through, Dual-Track Multi-Thread Communication Studio, 1-Click Pre-Filled Gmail/Chat/Buganizer/SFDC Draft & Auto-Injection Pipeline, 10-Point Multi-Channel Communication Copy Sanitization, Zero Automated Buganizer/Meet/Calendar Notifications in Email Trails, 107/107 Unique Bespoke Natural Human 3-Part Answers, 24-Hour Chronological Timestamp Reconciliation (`toSortableTimestampKey`), Authentic Google Sheets Visual & Functional Parity (`Rule 30P`: Single-Row 11-Col Header Default, Column Letters `A–I`, Row Numbers `1–107`, Full-Width Formula Bar, `#1a73e8` Active Cell Box + Fill Handle, Bottom Sheet-Tab & Live Aggregate Status Bar & Legacy UI Purge), Roadmap 90-Day Horizon Forward Date Rollover & Symbolic Bucket Parity (`rollActiveDateForwardIfPastAsOf`), Per-Cell LLM-as-a-Judge Proof & 7-Source Oct 15–21 Freshness (`Rules 25–30P`)**:
    - Enforces zero duplicate horizontal page navigation rails (`Rule 25`), global table cell clipping and inline `span.truncate` block containment (`Rule 26`), zero client-side fake clock tickers, 5-sheet Google Sheets v4 reconciliation (`pull_changes_from_google_sheet()` + `extra_tab_ranges`), and 7-source watermark persistence (`Rule 27`), 6-hop end-to-end Direct-SoT harvesting (`_SFDC_RECORD_ID_TO_CASE_MAP` resolving all 18-char `500Kf...` Salesforce Record IDs to 8-digit `CaseNumber` + `Subject` + `/lightning/r/Case/500Kf.../view`, `_PORTAL_SYNC_LOCK` + `run_unified_portal_sync_coalesced` 8-second subprocess coalescing, `_deduplicate_lineage_records` by `lineageId` and `primaryId`, `_resolve_allowed_cors_origin` scoped CORS, `_sanitize_untrusted_text_for_llm` IPI defense + full Multi-Source/Roadmap AI Chat context, read-only `GET /api/gsheet/status`, `/api/gsheet-sync?action=row-refresh` resolving `hint_lineage_id`/`hint_eap_id`/`hint_bug_ids`/`hint_sfdc_case` for `CQ-*`, `GAP-*`, and `AutomatedFeatureRequestCrStudioTab.tsx` rows and returning `upstreamTickets`, and `GET /api/roadmap-plx?rowId=` reconciling `table3Live` against live `RECORDS` and updating `OfficialRoadmapDashboardTab.tsx`), multi-store search stitching, live 7-source telemetry bars (`data-testid="page-live-buganizer-sfdc-telemetry-bar"` and `data-testid="eap-live-buganizer-sfdc-telemetry-bar"`) + interactive `<LiveMultiSourceSotExplorer />` (`data-testid="live-sot-by-date-and-source-explorer"`, `sot-by-date-and-source-table` loaded via Node/Vite-safe `try { return import.meta.glob(...); } catch { return {}; }` and scrubbed via `sanitizeFeedItemList` across `Buganizer 95 · SFDC 32 · Gmail 71 · Chat 66 · Drive 15 · Sheets 5 · Gantry 32`, wired to `POST /api/portal/refresh-all`), and `< 2m` (`15s`/`30s`/`60s`/`90s`) reactive polling across all 18 `WorkbookTabId` pages (`EapFeaturesTrackerTab.tsx` serialized `localStorage` guard, `GeminiSpecLineageTab.tsx` 15s deduplicated sheet polling, `MultiSourceTrackerPageTab.tsx`, `CertifiedForensicLineageTab.tsx` `getLiveEapTrackerRecords()`, `DailyOutreachBriefPanel.tsx`, `AutomatedFeatureRequestCrStudioTab.tsx`, `OfficialRoadmapDashboardTab.tsx` `Array.isArray(payload.table3Live)`) without permission-stalling (`Rule 28`), **zero parent umbrella-EAP environment bleed-through (`Rule 29`)** so unshipped Feature Requests (`FR-0176` / `CR b/572808626`), open Product Bugs (`BUG-*`), Customer Questions (`CQ-*` / `ASK-*`), and Lineage Process Gaps (`GAP-0*`) never inherit parent EAP `🟢 Available` / `Configurable` / `No Longer Allowlisted` readiness from `.local_backup/local_eap_records.json` (`EAP-11`), rendering `⚪ Not Available (FR Open — Unbuilt)` and `Not Yet Configurable (Unbuilt Feature Request — Pending Eng)` with negation-first `getEnvBadgeStyle` styling, **7-source Oct 15–21 freshness, 24-hour chronological `toSortableTimestampKey` sorting, Authentic Google Sheets Visual & Functional Parity + Excel Formatting Palette Ribbon + Custom Views + 1-Click Restore Full View (`Rule 30O` & `Rule 30P`: single-row `<thead>` default when `0` dossiers expanded, `A..I` column letters, `1..107` row numbers `cq-excel-rownum-*`, `#dadce0` gridlines `cq-excel-gridlines-toggle-btn`, `#1a73e8` active cell selection box + fill handle, dedicated full-width Formula Bar `cq-excel-formula-bar` with live `=COUNTA`/`=COUNTIF`/`=SUM`/`=AVERAGE` evaluator `cq-excel-formula-eval-badge`, bottom sheet-tab & live aggregate status bar `cq-excel-bottom-status-bar`, `0` legacy `⊞ 4-Col | ▦ 6-Col` toggles, `cq-excel-formatting-palette`, `cq-custom-views-bar`, `cq-restore-full-view-btn`, `cq-autosave-status-badge`), Roadmap 90-day horizon date parity & 23-Slide Chat/Drive Cross-Check + Daily 12 AM / 8 AM EST Auto-Refresh (`Rule 30N` & `Rule 30O`: `rollActiveDateForwardIfPastAsOf`, `parseDateUtc` optional 4-digit year + `"Oct (Rollover)"` -> `2026-10-31` + `"Q4"`/`"Q3/Q4"` quarter bucket preservation, `asOfDate >= '2026-10-21'`, `refresh_roadmap_deck_est_schedule.py` `42` deduplicated items, `_start_roadmap_deck_est_daily_scheduler`) & uncapped `activitySortEngine.ts` (`Rule 30`, `Rule 30B`, `Rule 30C`, `Rule 30N`, `Rule 30O` & `Rule 30P`)** across `106` human corporate Gmail threads (`commsLinkResolver.ts`, `0` automated `Issue <bugId>:`, `Notes: “...”`, `Gemini notes:`, `Transcript:`, or `Invitation:` emails via `AUTOMATED_BUGANIZER_SUBJECT_RE` and `scrub_confidential_customer_tokens` in `scripts/auto_gmail_eap_scanner.py`), `107` verified customer inquiries (`customerQuestionsData.ts`, `107/107` unique bespoke 3-part human answers with `0` shared canned templates and `0` duplicate `(b/...) (b/...)` substrings, live `discoveredGmailThreads` timestamp promotion onto existing rows via `discoveredByThreadId`/`discoveredByNormSubj` + 24-hour `toSortableTimestampKey`, topic-routed `CQ-LIVE-*` threads, full multi-bug lineage indexing across scalar & array bug fields, `75` distinct human Gmail threads + `14/14` distinct Chat Space URLs), `77` verified Chrome-History-visited Chat Spaces (`34` real thread paths, `0` `AAQAkGiKOu4`), `15` Oct 15–19 Google Drive Docs/Slides/Sheets (`local_war_room_and_drive_index.json` + `proofLinks` on `LIN-0176`/`LIN-0188`/`LIN-0189`/`LIN-0028`/`LIN-0050`/`LIN-0196`/`LIN-0191`), `32` SFDC Cases (`76330739`, `76291571`), `95` Buganizer issues, `227`+ `unifiedMultiSourceFeed` items with direct Grounding Links, and `MIN_OPERATIONAL_HORIZON_ISO = '2026-10-16'` in `src/utils/activitySortEngine.ts`, **Dual-Track Multi-Thread Communication Studio & 1-Click Pre-Filled Gmail/Chat/Buganizer/SFDC Draft & Auto-Injection Pipeline & 10-Point Multi-Channel Communication Copy Sanitization (`Rule 30E`, `Rule 30F` & `Rule 30K`)** across `src/utils/communicationTemplateManager.ts` (`buildPrefilledGmailComposeUrl`, `triggerBackendDraftAndTabAutoInject`, `dispatchDirectChannelAction` with `engToEmails`/`engCcEmails` for `1b`, `@handle` `engGreetingNames` for `2a`/`2b`/`3`, and customer POC `toEmailsDisplay` + row-scoped `ccEmails` for `1a`, preserved `Re: {generalEmailSubject}` subject & concise internal engineering body on `1b` `email_general_question_ask`, concise 3-part `chat_general_question_ask` [`2b`] & internal-audience `chat_account_status_update` [`2a`], non-duplicate `@`-mentions & ticket IDs via `engineeringQuestionBody` across `3. Buganizer` & `4a/4b. Salesforce`, dynamic `Rule 29`-compliant `{envDevStatus}`/`{envTestStatus}`/`{envProdStatus}` in `email_env_handoff`, `rec.productArea || rec.topic` workstream resolution, space-separated `@`-mentions, zero `@nitinagga` self-tags), `src/components/UnifiedCommunicationModal.tsx` (`emailActionMode` subject toggling, `handleChannelSwitch` & `handleTemplateSelectChange` track synchronization, `handleCopy()` + `triggerBackendDraftAndTabAutoInject()` on all card links & footer buttons), `src/utils/customerEmailHtmlFormatter.ts` (synchronous `execCommand('copy')` before `window.open` + `@nitinagga` & synthetic project ID stripping + expanded `VERIFIED_CUSTOMER_POC_MAP`), and `POST /api/comms/prepare-draft` in `gsheet_sync_server.py` (native `/usr/bin/pbcopy` + AppleScript Chrome tab reply-box auto-injection), and **Per-Cell & Per-Link LLM-as-a-Judge Verification Proof (`Rule 30I`)** across `src/utils/cellLinkJudgeEngine.ts`, `src/components/RowCellLlmJudgeModal.tsx`, `scripts/llm_judge_row_cell_verifier.mjs` (`134` rows / `804` cells audited, `100/100` PASS), `src/components/MultiSourceTrackerPageTab.tsx` (`cell-llm-judge-proof-*`, `link-judge-rationale-*`), and `src/components/EapFeaturesTrackerTab.tsx`.

---

## 10. 🔭 `live-product-intelligence-and-grounding` (5-Channel Live Product/Feature/Bug-Fix Grounding & Anti-Infinite-Loop Circuit Breaker — `v3.4.0`)

### Purpose & Trigger Conditions
Triggered whenever generating diagrams, Living Specifications, codelabs, or UI screenshots involving newly released products, features, capabilities, cloud SKUs, or bug fixes/issues across all projects (`PromptCanvas`, `Demoes-GE`, `customer-tracker`, `scorex`, `zyvoriq`).

### Core Invariants
1. **5-Channel Pre-Flight Intelligence Discovery**:
   - **Channel 1 (Local Codebase & Docs)**: Inspect `node_modules/next/dist/docs/`, `package.json`, `git log -n 20`, and `src/lib/geminiConfig.ts`.
   - **Channel 2 (Live Issue & Buganizer/Gantry Delta Ledger)**: Query `KNOWN_BLOCKERS_CATALOG`, `lineageData.ts`, Gantry API, and test harness failure logs to distinguish `OPEN` blockers (route to Path B/C) from `FIXED` issues (route to Path A).
   - **Channel 3 (Live Google Search Grounding)**: Invoke `search_web` / `read_url_content` and runtime `fetchLiveGoogleSearchGroundingBrief` (`tools: [{ googleSearch: {} }]` in `src/lib/research/deepDomainResearcher.ts`) before synthesizing Draw.io XML or 16 Living Specs.
   - **Channel 4 (Automatic SKU & Model Normalization)**: Run `normalizeLatestGoogleAndCloudNomenclature` to replace deprecated product/model names (`Cloud DLP` $\rightarrow$ `Sensitive Data Protection`, `Stackdriver` $\rightarrow$ `Cloud Monitoring & Logging`, legacy 1.x / 2.x / 3.x model aliases $\rightarrow$ `Gemini 3.1 Pro / 3.8 Flash`).
   - **Channel 5 (Root-Cause Delta Circuit Breaker — `MAX_CONVERGENCE_LOOPS = 3`)**: Never retry a failing render with the same unverified hypothesis; enforce a mandatory Re-Research & Grounding Refresh after Attempt 2.

---

## 11. 🌐 `live-upstream-sot-engine` (Direct Upstream Systems-of-Record Ingestion & Zero-Lag Lineage Reconciler — `v3.11.0`)

### Purpose & Trigger Conditions
Triggered whenever syncing, querying, intaking, or reconciling enterprise customer issues, blockers, Buganizer tickets, Salesforce cases, or Gantry escalations.

### Core Directives & Invariants
1. **Direct Upstream Ingestion First**: Always query authoritative upstream APIs directly:
   - **Buganizer / Issue Tracker**: Real-time ticket state, assignees, priorities (P0–P4), and components (`compId:550983` CB, `compId:841988` CR, `compId:1891061` TAM, `compId:1456103` SWE).
   - **Salesforce / Vector**: Account case numbers, customer contacts, SLAs, and severity.
   - **Gantry OPM Intake API**: Deal cards (`GANTRY-XXXXX`), review statuses (`ENG REVIEWING`, `FIX IN-FLIGHT`), and triagers.
2. **Zero-Lag App-Launch Handshake**: Trigger `/api/upstream/refresh` immediately when the app mounts and on `window.focus`, updating client state with live deltas without requiring page reloads.
3. **Dynamic Unindexed Ticket Auto-Stitching**: When a user queries, searches, or inputs any untracked ticket (e.g. `b/568354707` or `Case 12345678`), immediately fetch live metadata and synthesize a new lineage node (`LIN-XXXX`) on the fly.
4. **Google Sheets as Downstream Mirror Only**: Google Sheets is strictly an outbound export projection for stakeholders; it must never block or serve as the prerequisite for application state.

---

## 12. 🛡️ `oce-agentic-bi-ground-truth` (AskAIOCE Permanent Zero-Hallucination, Workflow Truthfulness, Logical UI/IA, Hyperlink Integrity & Google Chat Provenance Quality Gate — `v3.15.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying `/Users/nitinagga/Documents/AskAIOCE` (`scratch/agentic_bi_studio.py`, `scratch/build_ui_hub.py`, `scratch/studio_interactive.py`, `scratch/report_generator.py`, `scratch/sor_upstream_connector.py`, or `scratch/serve_hub.js`).

### Core 3-Layer Fail-Closed Quality Gate Architecture
1. **Layer 1: 20-Point Compile-Time Anti-Hallucination, IA, Link & Chat Space Firewall (`verify_account_boundary_firewall`)**:
   - Aborts HTML compilation (`RuntimeError`) if any of the 20 invariants fail:
     1. Zero fabricated 3P vendor names (`Snowflake`, `Splunk`, `Okta OIDC`).
     2. Zero cross-account retail tickets (`b/559146821`), unverified `b/519168184`, `BYOMCP`, `CA cert`, or synthetic Workload IDs.
     3. 100% of customer POC emails strictly belong to the 8 verbatim ground-truth addresses.
     4. Honest persistence badge (`Saved (Browser & SoR Mirror)`; bans fake `Saved to Drive` claims).
     5. Latest-first period selector (`2026_10_09_live_sor` at index `0`) and Side-by-Side Compare defaults (`Latest` on Left vs. `Previous` on Right).
     6. Manual OCE review & selection (`0 / 51 Lines Checked` initialized unchecked by default on load per `L50-11`; only checked lines copy into Gmail).
     7. Cloud-safe `🟢 Verified Doc Mirror (Frame-Safe)` default (`window.__gdocEmbedMode = 'bridge'`) and `isLocalWorkstationHost()` guard.
     8. BI `📑 All-in-One` DOM pane order strictly follows `1 → 2 → 3 → 4 → 5` (`overview` → `granular-inspector` → `week-plan` → `enablement` → `governance`).
     9. Deduplicated `⚡ More Actions ▾` (`#bi-granular-actions-select`) in `🔍 Use Cases & Blockers`.
     10. `📝 Markdown` view includes `← Back to Report Template` (`#md-back-to-preview-btn`), `📊 Back to 360° BI` (`#md-back-to-bi-btn`), and active `#tab-markdown` pill highlighting.
     11. Always-accessible `🔗 SoR Links ▾` (`#subtoolbar-sor-quicklinks-select`) in `.period-QuickBar` (`10` links: `6` SoR + `4` verified Google Chat Spaces) synchronized `1:1` with `#sidebar-quick-links-list`.
     12. 100% `Oct 9, 2026 Live SoR` label alignment across all BI controls and hidden duplicate drawer button (`#bi-toggle-monday-week-plan-btn`).
     13. Zero dead legacy `/escalations/` URLs (must route to `gantry-portal-<org>.cr.gclb.goog`).
     14. Zero plain-HTTP `http://goto.google.com/` or `http://go/` shortlinks and zero boilerplate `screenshot.googleplex.com` links.
     15. Zero cross-account external Google Doc IDs (`1sgLEhxYI...`) in Live Doc picker (`6` verified account-only docs).
     16. `BUGANIZER_TRANSPOSITION_CANONICAL_MAP` present and resolving `542580842 -> 542518042` and `553529886 -> 555529886`.
     17. `#sec-links` (`Attachments / Quick Links`) contains `15/15` distinct verbatim URLs (`0` overwritten duplicates).
     18. Row 5 Top Quick-Links Bar contains `6/6` distinct verbatim URLs (`0` overwritten duplicates).
     19. Zero synthetic camelCase Google Chat room slugs (`/room/AAAA[a-zA-Z]{10,}`), zero `chat.google.com/dm/` redirects, and zero bare `chat.google.com/` root links.
     20. 100% of `https://chat.google.com/...` URLs (`>= 10` distinct spaces/threads) strictly match `^https://chat\.google\.com/room/(?:AAQA|AAAA)[A-Za-z0-9_-]{7}(?:/[A-Za-z0-9_-]{11}/[A-Za-z0-9_-]{11})?(?:\?cls=\d+)?$`.
2. **Layer 2: Multi-Tier Automated Headless Chromium Forensic Gates (`npm run quality-gate`)**:
   - `scratch/run_level30_deep_forensic_audit.js` (`30/30` Ground-Truth & Account-Boundary Gate).
   - `scratch/run_level40_deep_forensic_audit.js` (`20/20` Upstream-Only Zero-Trust Provenance Gate).
   - `scratch/run_level50_anti_hallucination_and_ia_quality_gate.js` (`67/67` Anti-Hallucination, Workflow Truthfulness, Logical UI/IA, Hyperlink Integrity, Authentic 11-Character Google Chat Space/Thread Provenance, 3-Tab Report/Comparison Focus & 4-Week Report Synthesis Gate, `L50-01`..`L50-67`).
3. **Layer 3: Pre-Deploy Cloud Run Gate (`scripts/gcp/deploy-gcp-argolis-demo.sh`)**:
   - Executes `sor_upstream_connector.py --verify`, `run_level30_deep_forensic_audit.js`, `run_level40_deep_forensic_audit.js`, and `run_level50_anti_hallucination_and_ia_quality_gate.js` before `gcloud builds submit` / `gcloud run deploy`, blocking any Cloud Run deployment if a single check fails.

---

## 11. 🎬 `omni-digital-twin-voice-and-video-invariants` (Rule 48 Omni 1.1 Digital Twin Video Continuity, 60fps Lip-Sync Canvas Overlay, Full-Deck Pre-Baking & Strict Accent Isolation — `v3.19.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying digital twin persona generation, audio/video synthesis, slide presentation theaters, narrator voice controls, or background prebaking workers across `Demoes-GE`, `AskAIOCE`, and presentation portals (`src/mcp-server/server.mjs`, `src/mcp-server/customPersonaStore.mjs`, `src/portal-views/slides-fullscreen.html`).

### Core Protocols & Architectural Contracts
1. **Zero-Blank-Video Resilient Fallback Chain & Custom Twin 60fps Lip-Sync Canvas Overlay (`L30-04`, `L30-05`, `L30-13`, `L30-14`)**:
   - Presenter video elements (`#aiPresenterOmniVideo`) must NEVER have `src` stripped or be left blank.
   - `resolveLocalOmniCohesiveVideo` executes an unbreakable 4-tier fallback:
     `Target Slide MP4 -> Slide 1 MP4 Loop -> Any Rendered Clip for Twin -> 60fps Animated Avatar Canvas`
   - All `90/90` (`18` slides × `5` decks) `custom-nitin-aggarwal-live` `.mp4` files are untouched native `models/gemini-omni-1.1-flash` cohesive audio+video bundles (`0` `Lavf62.29` static-portrait muxes, `0` `studio-loop` or `slide_01` substitutions). When `#aiPresenterOmniVideo` has an active studio video (`hasActiveStudioVideo`), `#aiPresenterAvatarCanvas` stays 100% transparent over the video body (`L30-17`, `L30-19`), and `syncFacePresenterWithSlide()` keeps `omniVid` paused on a closed-mouth frame when `!isNarrating`.
   - `customPersonaToCatalogEntry(m)` preserves calibrated facial landmarks (`{ mouthX: 0.500, mouthY: 0.701, mouthW: 0.194, chinY: 0.798, eyeY: 0.458 }` for `custom-nitin-aggarwal-live`) so `/api/persona/custom` refreshes never overwrite calibrated mouth/chin coordinates with generic defaults.
2. **Deck-Agnostic, Full-Deck Automatic Background Pre-Baking (`L30-01`..`L30-03` & `L30-11`)**:
   - `enqueueAllSlidesPrebakeForCustomPersona` handles arbitrary deck keys and arbitrary slide counts ($N = 1..\text{totalSlides}$).
   - Creating a custom twin (`POST /api/persona/custom`) enqueues all slides ($0..N-1$) in the background worker.
   - Polling status (`GET /api/persona/custom/:id/status`) self-heals by enqueuing unrendered slides whenever `readyCount < totalSlides`.
   - Switching demo decks (`switchSlidesDemo`) triggers lookahead prefetching (`triggerOmniBackgroundPrefetch(pId, 0)`) and refreshes custom twin status.
3. **Strict Voice & Accent Isolation (`L30-06`)**:
   - Candidate twins in prebaked audio lookups (`candidateTwins`) strictly isolate persona, gender, and regional accent.
   - Indian English (`indian-male-aarav` or `en-IN` / `custom-nitin-aggarwal-live`) is strictly banned from falling back to American male (`sundar-puck`) or Indian female (`indra-diya`). Unbaked slides fall through to dynamic Google Cloud TTS synthesis (`en-IN-Neural2-B`).
4. **Quota Project & Regional Language Derivation (`L30-07` & `L30-08`)**:
   - `synthesizeGoogleCloudSegment` preserves `'x-goog-user-project': 'cymbal-build-sandbox'` across all plain text and SSML retries, preventing HTTP 403 quota errors on local and Cloud Run ADC.
   - Regional neural voices derive `languageCode` directly from the model name (e.g., `en-IN-Neural2-B` -> `en-IN`, `en-GB-Neural2-B` -> `en-GB`).
5. **Bidirectional Persona <-> Language Auto-Sync (`L30-09` & `L30-10`)**:
   - `selectFamousPersonaById` auto-syncs `selectedSpeakerLang` and all language dropdowns (`#narratorLangSelect`, `#theaterHeaderLangSelect`) to the persona's regional accent (`en-IN`, `en-GB`).
   - Browser `speechSynthesis` fallback prioritizes authentic regional voices (`/India|Rishi|Veena|Neerja|Kavya|Aarav|Diya|en[-_]IN/i`).
6. **Dynamic Filesystem Catalog Discovery (`GET /api/omni-catalog`) & Full Deck Pre-Baking (`L30-12`)**:
   - Backend MCP server dynamically scans `screenshots/omni-video/` on startup and exposes `GET /api/omni-catalog`, returning the exact per-deck, per-persona MP4/MP3 counts (`allSlidesPersonas`, `slide1Personas`).
   - Frontend UI (`slides-fullscreen.html`) invokes `window.__syncOmniCatalogWithLocalState()` on initialization, automatically registering dynamic and custom personas without hardcoded client set limitations.
   - 100% of all 18 slides for `a2a-enterprise-gateway` with `custom-nitin-aggarwal-live` are pre-rendered on disk with matching `en-IN-Neural2-B` audio waveforms (`slide_01`..`slide_18`).
7. **Single-Environment `@google.com` Screenshot & Architecture Diagram Purity (`L30-15`)**:
   - `screenshots/a2a-enterprise-gateway/` and `screenshots/merck-aws-mcp-consent/` and all `a2a-enterprise-gateway` / `merck-aws-mcp-consent` deck/codelab references (`data/a2a_enterprise_gateway_deck.json`, `data/a2a_enterprise_gateway_codelab.json`, `data/merck_aws_mcp_consent_deck.json`, `data/merck_aws_mcp_consent_codelab.json`, `src/portal-views/slides-fullscreen.html`, `src/mcp-server/merckMicrosoftValidatorAndPptx.mjs`, `src/portal-views/codelab-view.html`, `src/portal-views/live-demo-narrator.html`) strictly use `.jpg` architecture diagrams and real `@google.com` (`ramp-portal-dev` `#248990048888`) GCP Console & Gemini Enterprise screenshots (`real_*.png`, including `real_ge_aws_mcp_consent_biomarker_card.png`), with zero custom mock-app PNGs and zero Argolis (`cymbal-control-plane`) cross-combination screenshots.
8. **All 5 Omni Decks $\times$ 9 Digital Twin Personas $\times$ 18 Slides Animated Talking-Head Videos (810 MP4s + 810 MP3s, 90/90 Native Omni 1.1 Cohesive Bundles), Chirp 3: HD Prosody, Transparent Studio Video Canvas, WebAudio Suspension Guard & Live Flyout Playback (`L30-16`..`L30-20`)**:
   - `screenshots/omni-video/a2a-enterprise-gateway/`, `screenshots/omni-video/merck-aws-mcp-consent/`, `screenshots/omni-video/merck-agentgateway-policy/`, `screenshots/omni-video/merck-adk-a2a-a2ui-playbook/`, and `screenshots/omni-video/merck-skills-workflow-playbook/` contain all 9 Digital Twin personas (`custom-nitin-aggarwal-live`, `sundar-puck`, `indra-diya`, `satya-aarav`, `mira-aoede`, `jensen-fenrir`, `feifei-kore`, `demis-charon`, `attenborough-david`) $\times$ 18 slides $\times$ 5 decks = `810` 24fps animated talking-head `.mp4` videos and `810` expressive **Google Cloud Chirp 3: HD** (`en-IN-Chirp3-HD-Orus`, `en-IN-Chirp3-HD-Aoede`, `en-US-Chirp3-HD-Puck`, `en-US-Chirp3-HD-Aoede`, `en-US-Chirp3-HD-Fenrir`, `en-US-Chirp3-HD-Kore`, `en-GB-Chirp3-HD-Charon`, `en-GB-Chirp3-HD-Orus`) `.mp3` tracks with `90/90` untouched native `models/gemini-omni-1.1-flash` bundles (`0` `Lavf62.29` muxes, `0` `studio-loop` or `slide_01` fallback substitutions), archived in `gs://ge-demos-omni-scripts-248990048888/`.
   - Whenever `#aiPresenterOmniVideo` has an active studio video (`hasActiveStudioVideo`), `#aiPresenterAvatarCanvas` stays 100% transparent over the video body (rendering only top-right audio spectrum bars while preserving 60fps `window.__avatarLipSyncActive`), `startSlideNarration()` immediately synchronizes `applyOmniVidMetadataDuration()` when cached `blob:` video metadata is already loaded (`readyState >= 1`), and `window.attachOmniAudioAnalyser` never attaches `createMediaElementSource` to `<video id="aiPresenterOmniVideo">` or while `omniAudioCtx.state === 'suspended'`.
   - `lookupPreRenderedOmniSlideVideo` and `compileOmniAvSyncManifest` preserve `personaId`, ignore 18-word truncated script prefixes (`hasCustomOverride` false positive), and ban cross-persona hijacking (`mira-aoede` strictly resolves to `slide_XX_mira-aoede.mp4`, never `slide_XX_sundar-puck.mp4`).
   - Clicking any speaker card in `#theaterPresenterHoverFlyout` invokes `window.selectFamousPersonaById(id, true)` and clicking `🔊` (`window.previewVoiceSample`) invokes `startSlideNarration()`, immediately playing live neural narration + talking-head video.

### Operational Verification Command
Run the Level 30 Deep Forensic & Governance Audit:
```bash
npm run quality-gate
```
Asserts 100% pass across all 73 checks: Level 10 (28/28), Level 20 (24/24), and Level 30 (21/21).

---

## 12. 📄 `google-docs-native-cloning-and-html-ban` (Rule 49 Native Document Geometry Preservation & Drive HTML Multipart Upload Ban — `v3.16.0`)

### Purpose & Trigger Conditions
Triggered whenever generating, updating, syncing, or exporting Google Docs across any enterprise workspace (`AskAIOCE`, `customer-tracker`, `Demoes-GE`, `PromptCanvas`, or new tools).

### Core Protocols & Architectural Contracts
1. **Drive Multipart HTML-to-Docs Upload Ban (`L50-51`)**:
   - Strictly bans using Google Drive API multipart upload (`uploadType=multipart` with `mimeType: "application/vnd.google-apps.document"`) with raw HTML content to create or update Google Docs.
   - Prevents Drive's server-side HTML parser from injecting massive `minRowHeight` on table headers (`<th>`), eliminating 2-inch tall blue blocks and preventing tables from overflowing 468pt printable page widths.
2. **Native Document Cloning via `files.copy` (`L50-52`)**:
   - Always clone an authentic, natively created and styled Google Doc template (`drive.files.copy`) rather than converting HTML.
   - Preserves 100% of native Google Docs table styling, explicit column widths, compact row heights (~24pt), single-page table boundaries, and margins.
3. **In-Place Mutation via Docs API `batchUpdate` (`L50-53`)**:
   - Execute all mutations (dates, seat counts, active users, activation percentages, ticket links, workstream names, owners) directly against the cloned document's native structural tree using Google Docs API `documents.batchUpdate`.
   - Use `replaceAllText` with `matchCase: true` for surgical text replacements and `updateTextStyle` with `fields: "link"` for hyperlink updates.
4. **Zero-Placeholder & Zero-Prompt Cleanliness Standards (`L50-54`)**:
   - Strip all developer guidance, pink/yellow instruction boxes (`🚩 Please write your update via...`, `NB: 1. Contracted...`), and unverified placeholder tickets (`b/559146821`, `BYOMCP`, `CA cert`).
5. **Headless Chrome / PDF Visual Export Verification (`L50-55`)**:
   - Verify document layout via headless Chrome or PDF export before attesting completion:
     - Header row heights are compact (`<= 32pt`).
     - Zero duplicate table headers across page breaks.
     - 100% of metric numbers match active SoR snapshots verbatim.

### Operational Verification Command
Run the Level 50 Anti-Hallucination & Document Quality Gate:
```bash
npm test
```
Asserts 100% pass across all 67 Level 50 checks (`L50-01`..`L50-67`), including zero banned terms and verified document IDs.

---

## 13. 🛡️ `askaioce-studio-workflow-and-simplification-guard` (Rule 51 Executive Review Mode, Smart Presets, Sticky Dispatch Dock & Customer Modal Localization — `v3.17.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying, generating, styling, or refactoring the AskAIOCE specification studio (`reports/*_AI_OCE_Deployment_Update_Studio.html`, `scratch/build_merck_ui_hub.py`, `scratch/merck_studio_interactive.py`, `scratch/merck_agentic_bi_studio.py`, `scratch/serve_merck_hub.js`), document toolbars, dispatch triggers, or modal dialogs.

### Core Protocols & Architectural Contracts
1. **Review Mode Default & Canvas Positioning (`L50-56`)**:
   - In `#view-preview` (Report Template), the workspace must default to Review Mode with the canvas top positioned at $Y \le 120\text{px}$ (production: $Y = 94\text{px}$), eliminating the top 7-bar chrome clutter and recovering $\ge 170\text{px}$ of vertical space above the fold.
2. **Collapsible Editor Tools on Demand (`L50-57`)**:
   - The Google Docs menubar, formatting toolbar, ruler, and callout strip must be wrapped inside `#gdocs-editor-tools-wrapper.collapsed` by default. It must smoothly expand and collapse via `#toggle-editor-tools-btn` (`🛠️ Editor Tools ▾`) in `.sub-toolbar`, preserving 100% of formatting capabilities without consuming permanent screen real estate.
3. **⚡ Smart Selection Presets & Section Automation (`L50-58`)**:
   - `.sub-toolbar` must provide `#subtoolbar-selection-preset-select` (`⚡ Smart Presets ▾`) with 5 batch presets (`exec_summary`, `blockers_risks`, `in_progress`, `use_cases`, `metrics_only`).
   - All 7 primary section headers (`sec-health`, `sec-accomplishments`, `sec-planned`, `sec-usecases`, `sec-metrics`, `sec-por`, `sec-risks`) must provide interactive `.section-select-btn` (`+ Select Section`) controls that toggle section lines in 1 click and synchronize state dynamically.
   - Baseline DOM FNV-1a hash calculation (`extractCleanElementTextForSig`) and HTML cleanup (`getCleanHtmlFromElement`, `stripUiArtifactsFromIncomingClone`) must cleanly strip `.section-select-btn` so hashes and copied email tables remain 100% unpolluted.
4. **🛡️ Floating Sticky Dispatch Dock (`L50-59`)**:
   - `#oce-sticky-dispatch-dock` must remain fixed at bottom-center whenever $\ge 1$ items are selected, displaying real-time counts (`🛡️ X / 51 Items Selected (Y%)`) and a 1-click `✉️ Preview & Send in Gmail →` dispatch trigger (`requestSendReportWithAttestation('header')`), hiding automatically when 0 items are checked or when navigating away from `#view-preview`.
5. **Customer Profile Dynamic Modal Localization & Functional Bookmarks (`L50-60`)**:
   - All modal dialogs (`openShareDocModal`, `openVersionHistoryModal`, `openDriveFolderModal`, `openGoogleMeetPresentModal`, `openAppsScriptMacroModal`) must query `window.getCurrentActiveCustomer()` to bind to the active customer's assigned OCE name/email, account name, Salesforce ID, and authentic Drive status folder with zero cross-customer tenant leaks.
   - `insertBookmarkAtCursor()` must execute real DOM insertion of `<span class="gdoc-bookmark-anchor">` anchors.
6. **Customer Partitioned Causal Datamart Storage**:
   - Causal annotations, root-cause tags, and why/why-not explanations must be partitioned in `localStorage` under `oce_bi_causal_overlay_v5_<custId>`, guaranteeing zero cross-customer annotation contamination while dual-writing to `v4` for backward-compatible test runners.

### Operational Verification Command
Run the unified 187-check test suite:
```bash
npm test
```
Asserts 100% pass across all 187 checks: 20 compile-time invariants, Phase 1 (50/50), Level 30 (30/30), Level 40 (20/20), and Level 50 (67/67).

---

## 14. 📐 `table-cell-containment-and-truncate-safety-guard` (Rule 26 Rigid Table Cell Containment, Inline Truncate Safety & Zero Text-Overlap Invariant — `v3.18.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying tables, grid columns, status pills, email/chat links, truncate classes, or flexbox layouts across `customer-tracker` (`gantry-pulse`), `AskAIOCE`, `scorex`, or any operational dashboard.

### Core Protocols & Architectural Contracts
1. **Strict Ban on Naked Inline `span.truncate` (`Rule 26A`)**:
   - Under W3C CSS specifications, `overflow: hidden` and `text-overflow: ellipsis` are ignored on inline elements (`display: inline`), while `white-space: nowrap` remains active. Applying Tailwind's `truncate` to a standard `<span>` forces text into an unbreakable single horizontal line that never clips or shows an ellipsis.
   - All truncated elements must be block containers (`display: inline-block` or `display: block`) with bounded maximum widths (`max-w-full` or explicit width).
2. **Mandatory Flexbox Floor Reset via `min-w-0` (`Rule 26B`)**:
   - Flex children default to `min-width: auto` per CSS Flexbox specification.
   - Any flex container or child hosting truncated text must declare `min-w-0` (`min-width: 0px`) to break the intrinsic text content floor and permit container shrinkage.
3. **Mandatory Global Table Cell Containment (`Rule 26C`)**:
   - All fixed-grid and operational data tables (`table.table-fixed tbody td`, `.gp-blue-grid-table tbody td`) must enforce `overflow: hidden; max-width: 0;` in `src/index.css`.
   - Establishes an impenetrable bounding box for fixed-table columns in CSS table layout algorithms, preventing child text from physically escaping cell borders or painting over adjacent columns.
4. **Multi-Line Wrapping for Dense Operational Status (`Rule 26D`)**:
   - When column width is narrow (<25% or <250px) but row height is available, operational gate requirements, blockers, and configuration status must use `leading-tight break-words` instead of single-line truncation.
5. **Mandatory CI Fail-Closed Quality Gate (`Rule 26E`)**:
   - `scripts/stop_forensic_gate.mjs` must assert both global cell clipping (`max-width: 0; overflow: hidden;`) and span normalization (`span.truncate { display: inline-block; max-width: 100%; }`) in `src/index.css`.
6. **Unified Upstream Portal Synchronizer, Direct Buganizer/SFDC SoT Harvester, 7-Source Sync Watermark Ledger & Zero-Fake-Clock Gate (`Rule 27`)**:
   - Permanently bans client-side fake clock tickers (`setLiveRefreshDate(new Date())`, 15-second `window.setInterval` loops) and the `= new Date()` default parameter in `src/utils/estTimestamp.ts` (`getRowRefreshTimestampEst(rawSourceDate, verifiedSyncDate)`) across **all** `src/**/*.{ts,tsx}` files (`AutomatedFeatureRequestCrStudioTab.tsx`, `OfficialRoadmapDashboardTab.tsx`, `CertifiedForensicLineageTab.tsx`, `MultiSourceTrackerPageTab.tsx`, `EapFeaturesTrackerTab.tsx`).
   - Replaces gitignored `scratch/` sync script dependencies in `gsheet_sync_server.py` and `Dockerfile` with `scripts/upstream_portal_synchronizer.py` and `scripts/direct_sot_harvester.py`, persists 7 upstream source watermarks in `.local_backup/portal_sync_watermarks.json`, rolling cycle proofs in `.local_backup/direct_sot_sync_audit_log.json`, and the `sync_watermarks` STRICT table in `.local_backup/gantrypulse_sot.db`, and exposes `POST /api/portal/refresh-all`, `GET /api/portal/watermarks`, and `GET /api/portal/direct-sot-proof`.

### Operational Verification Command
Run the GantryPulse forensic quality gate:
```bash
python3 scripts/direct_sot_harvester.py
python3 scripts/upstream_portal_synchronizer.py
npm run quality-gate
```

---

## 15. 🏛️ `multi-tenant-workstream-topologies-and-gcp-verification-gate` (Rule 53 Mandatory Official Google Cloud Architecture Center Hub-and-Spoke Template `#78` Across `WS1`–`WS5`, 9-Guide Tile Catalog Hub `DOC-MT-01`..`DOC-REF-09`, 1:1 Google Cloud Whitepaper PDF Reader, First-Principles Value Pruning `Rule 25`, Consulting Brand Ban `Rule 50B`, Inline/New-Tab Draw.io Studio, 56-Shape Editable Slides, 12 Provisioned GCP Resources & 27-File E2E Pattern Workbench — `v3.24.0`)

### Purpose & Trigger Conditions
Triggered whenever modifying `/blogs` (`src/app/blogs/page.tsx`, `src/app/blogs/[docId]/page.tsx`), `src/lib/blogs/googleCloudDocumentationSeries.ts`, `src/components/DiagramInlineSlidesPreviewer.tsx`, `src/app/drawio-editor/page.tsx`, `src/lib/blogs/useCaseBlogEngine.ts`, `src/lib/canonical/templateOfficialGcpArchCenterHubSpoke.ts`, `src/app/api/blogs/gcp-verify/route.ts`, `src/data/gcpPatternCodebaseAndExecutionBundle.json`, `scripts/evaluate_blogs_llm_judge.ts`, or `scripts/provision_and_verify_gcp_workstreams.ts`.

### Core Protocols & Architectural Contracts
1. **Mandatory Official Google Cloud Architecture Center Hub-and-Spoke Template (`#78`) Across All Presets & Workflow Tabs (`templateOfficialGcpArchCenterHubSpoke.ts`, `workstreamTopologyRenderers.ts`, `useCaseBlogEngine.ts` & `src/app/blogs/page.tsx`)**:
   - All 9 Canonical `BLOG_USE_CASE_PRESETS` (`primaryTemplateId: '78'`, `ingestionTemplateId: '78'`, `searchTemplateId: '78'`), `/api/blogs/generate` (`templateId = '78'`), `localStorage` blog hydration, all 3 workflow tabs (`1️⃣ High-Level Topology (#78)`, `2️⃣ Data Ingestion / MCP Flow (#78)`, `3️⃣ Hybrid GraphRAG & Action Flow (#78)`), and the single authoritative inline figure (`Figure 1`, `secondaryInlineDiagram: undefined`, `0` duplicate `Figure 2`) strictly render the **Official Google Cloud Architecture Center Hub-and-Spoke Template (`#78`)** (`#1a73e8` outer Google Cloud frame, `#aecbfa` Routing Hub, `#ceead6` Governance Hub, `#feefc3` Left Spoke, `#fad2cf` Right Spoke, and numbered callouts `①`–`⑦` with `4` & `6` under `Model Armor` and `5` under `Vertex AI Gemini 2.5 Pro`), with `56` vertices, `23` explicit `source`/`target` vertex-bound Draw.io edges, and title-first `resolveArchIconUri` (`EXTRA_GCP_ICONS[iconKey]` + `titleLower` only, never `sub`).
   - Strictly ban legacy template fallbacks (`#51`, `#27`, `#67`, `#68`, `#24`, `#25`, `#40`, `#72`, `#76`), purge `renderWorkstreamSpecificSvg` from `workstreamTopologyRenderers.ts`, and remove legacy `Choose Template (78)` dropdowns and `Quick Styles:` override chip bars from `/blogs`.
2. **Inline Draw.io Editor (`referrerPolicy="no-referrer"`), New-Tab Draw.io Studio, 15-Deck Cohesive 3-Act Pure Technical Executive Story Arc Google Slides (`WS1` at `11` Slides + `WS2`–`WS5` at `12` Slides Each + `ALL` `25`-Slide Master Deck + `9` Dedicated `6`-Slide DevSite Guide Decks `DOC-MT-01`..`DOC-REF-09` Across `15` Distinct `googleSlidesId`s, `0` Pricing Slides, `0` `<a:tr h="0">` Auto-Collapsing Table Rows, `0.10"–0.22"` Table-to-Card Gap, Pure First-Person Spoken Talk Tracks, Rule 53F Per-Workstream Content Grounding — 5/5 Distinct Slide 4/6/7 Copy, `0` Ungrounded Facts, `0` Palette Hex Leaks), Rule-49 In-Place `documents.batchUpdate` Sync for All `6` Live Google Docs, Official Google Cloud Architecture Center 5-Part Blog Anatomy (`blogs/ws1..ws5-*.md`) & Full-Width Interactive E2E Flow Card (`DiagramInlineSlidesPreviewer.tsx`, `src/app/drawio-editor/page.tsx`, `/Users/nitinagga/Documents/blogs/scripts/build_arch_center_blogs.mjs`, `/Users/nitinagga/Documents/blogs/scripts/build_editable_slide_decks.ts`, `/Users/nitinagga/Documents/blogs/scripts/sync_google_workspace_bridge.py`, `/Users/nitinagga/Documents/blogs/scripts/build_diagram_e2e_flows.mjs`, `/Users/nitinagga/Documents/blogs/index.html` & `src/data/cloud_viewer_manifest.json`)**:
   - Every diagram on `/blogs` (both top workflow studio and inline figures) exposes `[ 🖼️ 1:1 Official SVG | ✏️ Edit Inline (Draw.io) ]`, `Open in Draw.io Tab ↗`, `👁️ Cloud Viewer`, and `[ S | Open with Google Slides ↗ | ▼ ]`.
   - `InteractiveDrawioInlineEditor` embeds `https://embed.diagrams.net/?embed=1&ui=min&spin=1&proto=json&configure=1&noSaveBtn=0` with `referrerPolicy="no-referrer"` (preventing Cloudflare `403` blocks on local `127.0.0.1` referers) and bidirectional `BroadcastChannel('promptcanvas_drawio_sync')` synchronization.
   - Pre-warmed native 100% Light-Theme (`#FFFFFF` / `#F8FAFC`) editable Google Slides & PowerPoint decks (`WS1`: `11` slides; `WS2`–`WS5`: `12` slides each in Customer-First Logical Order `Slides 1–3: TITLE-COVER -> THREE-PILLAR -> COMPARISON-GRID • MATRIX`, `Slides 4–7: L1 ARCHITECTURE-ZONE-TOPOLOGY -> L2 Figure 1 4-ZONE HUB-AND-SPOKE -> L3 UML-SEQUENCE-SWIMLANE -> L4 PAYLOAD-TRANSFORMATION`, `Slides 8–12: ASYNC-STATE-FLOW-PIPELINE -> COMPARISON-GRID • MATRIX -> LIVE-SCREENSHOT-CALLOUT -> STRATEGIC-OPERATING-MODEL -> NEXT-STEPS`; `ALL`: `25` slides ordering each 4-slide chapter `WS1..WS5` as `Section Divider -> Figure 1 Blueprint [4, 8, 12, 16, 20] -> Deep-Dive Mechanism [5, 9, 13, 17, 21] -> Verification Matrix [6, 10, 14, 18, 22]`, followed by `Slide 23: LIVE-SCREENSHOT-CALLOUT -> Slide 24: STRATEGIC-OPERATING-MODEL -> Slide 25: COMPARISON-GRID • LINEAGE`; and `DOC-MT-01`..`DOC-REF-09`: `9` dedicated `6`-slide DevSite `<article>` + `#78` Editable Diagram decks across `15` distinct `googleSlidesId`s in `slides/*.pptx`, `slides/*.deck.json`, and `slides/cloud_viewer_manifest.json`) weave the canonical editable architectural visual archetypes (`architecture-zone-topology`, `payload-transformation-triptych`, `uml-sequence-swimlane`, `async-state-flow-pipeline`, `strategic-operating-model-pillars`) and `live-screenshot-callout` native DrawingML CLI telemetry receipt slides (`0` `<p:pic>`) with `56` individual editable shapes + `23` connectors per `#78` diagram, full-height DrawingML table geometry (`0` `<a:tr h="0">` rows, explicit `h` and `rowH`, `valign: 'middle'`, and `0.10" <= (stripTopIn - tableBottomIn) <= 0.22"` gap above the 4 bottom synthesis cards), and pure first-person spoken customer talk tracks (`0` `"Why / What"` headings or stage directions, `100/100` PASS in `evaluate_google_slides_deck_all_dimensions.ts`).
   - In `/Users/nitinagga/Documents/blogs`, enforce the **Zero-Duplicate 4-File Diagram Quartet** (`diagrams/<id>.drawio`, `.drawio.png`, `.svg`, `vision_metadata/<id>.vision.json` with `0` duplicate `workstream-*/diagrams/` copies, `0` `.drawio.xml`, `0` non-`.drawio.png` PNGs, and `0` duplicate `2.7/3.7/4.7/5.2` blogs in `F-11`/`F-12`), structure the **5-Part Canonical Blog Series (`blogs/ws1..ws5-*.md`)** in the exact format of `https://docs.cloud.google.com/architecture/multi-tenant-agentic-ai-system?hl=en` (`Lead Overview` + unified `.gcp-arch-callout` for `Key point:`, `## Architecture` with 4 Hub-and-Spoke zones and `<ol class="gcp-arch-steps">` blue circular badges `1`–`7`, `## Products used`, `## Use cases`, `## Design alternatives`, `## Design considerations` mapped to the 5 Google Cloud Well-Architected Framework pillars, `## What's next`, and collapsible `<details class="e2e-inline-details">` flow accordions), and render `index.html` as an **Executive 4-Tab Series Reader** (`#tab-hub`, `#tab-guide`, `#tab-screenshots` with 5th sub-tab `#e2e-pane-deliverables`, `#tab-runbook`; 1-tier Header + 6-card Workstream Stepper + single Header-Only Slides/Cloud Viewer bar + `⬇ Export Diagram ▾` dropdown + 100% full-width Diagram Studio & `#hub-diag-e2e-flow-card` + 100% full-width `270px` sticky left TOC `#hub-blog-toc` + `1fr` natural-flow `#hub-blog-reader` with `.gcp-doc-breadcrumbs` & `.gcp-figure-card` + `#hub-series-footer`), certified at **`98.4 / 100 PASS_CERTIFIED`** by LLM-as-a-Judge Pass 2 and **`12/12 PASS • 20/20 SIMULATIONS PASS`** by `scripts/run_deep_forensic_audit.py`.
3. **9-Guide Tile Catalog Hub (`DOC-MT-01`..`DOC-REF-09`), Strict 1:1 Preset Deduplication (`0` 4x Format Multiplication), 1-Line AppHeader & Streamlined Catalog Toolbar, Direct Permalinks (`/blogs/[docId]`), Single-Diagram 1:1 Google Cloud Architecture Center 8-Section DevSite Reader, Blueprint-True Component Tables, Role-Label-Only Contributors & 1:1 Single-Column White DevSite `<article>` UI 6-Slide Google Slides Export (`docs.cloud.google.com/architecture/multi-tenant-agentic-ai-system`), First-Principles Value Pruning (`Rule 25`), Consulting Brand Ban (`Rule 50B`) & Social Kit Removal (`googleCloudDocumentationSeries.ts`, `useCaseBlogEngine.ts`, `src/components/AppHeader.tsx`, `src/components/DiagramInlineSlidesPreviewer.tsx`, `src/lib/export/editablePptxCompiler.ts`, `src/app/api/google-workspace/open/route.ts`, `src/data/cloud_viewer_manifest.json`, `scripts/sync_blog_editable_slides_with_content.ts`, `src/app/blogs/page.tsx`, `src/app/blogs/[docId]/page.tsx` & `scripts/evaluate_blogs_llm_judge.ts`)**:
   - Default `/blogs` view presents the **9-Blog Tile Catalog Hub** (`data-testid="blogs-tile-catalog-grid"`, `firstCardTopPx <= 220px`, `headerCardHeightPx <= 130px`) with a **single 1-line `AppHeader`** (`[ 9-Blog Catalog ]` + `[ 🛠️ 27-File Codebase & Diagram Studio ]` in `meta`, `[ ☁️ GCP Verified (20/20 PASS) ]` in `actions`, `0` `Refresh` button in `AppHeader.tsx`, `0` duplicate top-bar `DiagramInlineSlidesPreviewer` in `catalog` mode, and single-blog Studio editing buttons gated strictly behind `studioLayoutMode === 'legacy-studio'`), a **compact 1-row Catalog Toolbar** (Title + `All (9)` / `6-Part Multi-Tenant Series (6)` / `3 Reference Architectures (3)` filter pills + Search + `🖨️ Print / PDF`, with `0` duplicate `catalog-reading-order-strip` P1..P6 strip, `0` marketing boast badges, and `0` parenthetical table/key names on card service pills), and **9 streamlined Catalog Tile Cards** (`DOC-MT-01`..`DOC-REF-09`, showing Official `#78` SVG preview + asset counts + 3 clean service pills + title + 2-line subtitle + `🔗 Copy Link` + 1-click `[ S | Google Slides (Editable Diagram + Blog Content) ↗ | ▼ ]` `data-testid="tile-slides-export-${doc.docId}"` + `📖 Open Guide →`, with `0` duplicate `doc.executiveSummary` paragraph, `0` inline `SECTIONS & INLINE DIAGRAMS` list, and `0` duplicate `/blogs/DOC-MT-XX` footer slug).
   - Clicking any tile or navigating to `/blogs/[docId]` opens the **1:1 Google Cloud Architecture Center DevSite Reader** (`data-testid="blog-pdf-style-document-reader"` matching `https://docs.cloud.google.com/architecture/multi-tenant-agentic-ai-system?hl=en`: streamlined `AppHeader` with `← 9-Guide Catalog`, `☁️ GCP Verified (20/20 PASS)`, 1-click `[ S | Export Blog to Google Slides ↗ ]` `data-testid="doc-reader-export-blog-slides-btn"`, `Print / PDF`, `Copy Markdown`, `Codebase Workbench ▾`; `Home › Documentation › Cloud Architecture Center` `data-testid="doc-reader-breadcrumb"`, `#202124` `28px` Google Sans `H1`, `Last reviewed 2026-10-15 UTC`, 3-paragraph lead intro with `#deployment` link, sticky right `"On this page"` TOC `data-testid="doc-reader-toc"`, `0` duplicate top breadcrumb/action card, `0` `doc-reader-quick-assets-bar` strip, and the exact **8-Section Cloud Architecture Center Hierarchy** across all 4 blog formats: `1. Architecture` `#architecture` with strictly **1** authoritative Official `#78` diagram [`Figure 1`, `secondaryInlineDiagram: undefined`, `0` duplicate `Figure 2`, single header toolbar with `👁️ Cloud Viewer`, `[ S | Open with Google Slides ↗ | ▼ ]`, and `✏️ Edit in Draw.io`] + blueprint-true 2-column `Component | Description` table [`0` `"Google Cloud Armor (Tier 1: Pooled)"` or `"Identity-Aware Proxy (IAP) (Tier 2: Bridge)"` slot-mismatch parentheticals] + `### Agentic flow` `#agentic_flow` numbered `1.`–`7.` with `a, b, c, d` sub-steps under step `4`, `2. Products used` `#products_used` with clean service names, `3. Use case` `#use_case`, `4. Design alternatives` `#design_alternatives`, `5. Design considerations` `#design_considerations` across 4 concise Well-Architected sub-tables [`3` rows per pillar], `6. Deployment` `#deployment`, `7. What's next` `#whats_next`, and `8. Contributors` `#contributors` with role/team labels only [`Authors: Principal AI Architect • Cloud Solutions Architecture • Enterprise AI Field Engineering` and `Other contributors: Principal AI Architect & Field Deployment Engineering • Google Cloud Architecture Center Engineering Team`, `0` personal names]), while the UI Cloud Viewer (`DiagramInlineSlidesPreviewer.tsx`), `.pptx` download, and 1-click Google Slides export (`exportDrawioToEditablePptx`) compile a **Cohesive 6-Slide 1:1 Single-Column White DevSite `<article>` UI Slide Deck** (`Slide 1: Lead Overview & Architecture Intro`, `Slide 2: Figure 1 Full-Width Native Editable #78 Diagram with 56 shapes + 23 connectors`, `Slide 3: Component Table + Agentic Flow`, `Slide 4: Products Used + Use Case`, `Slide 5: Design Alternatives + Well-Architected Table`, `Slide 6: Deployment + What's Next + Contributors`, with `0` 4-color top ribbons, `0` green pill badges, `0` 4-zone bento sidebars, and `0` rainbow left-border bento boxes), certified at `100/100` (`11/11` checks, `0` issues) by `scripts/evaluate_blogs_llm_judge.ts --pass=2` and `scripts/verify_export_slides_quality_gate.ts`.
   - Across all **9 Canonical Blogs (`1:1` with `DOC-MT-01`..`DOC-REF-09`)**, enforce `0` third-party consulting brands (`Deloitte`, `Quantiphi`, `McKinsey`, `Accenture`, `Capgemini`, `Wipro`, `Cognizant`, `PwC`, `KPMG`, `Infosys`, `"System Integrator (SI)"` — `Rule 50B`), `0` duplicate `Editable Architecture & Slide Assets Index` or `OKF v0.1 Executive Synthesis` blocks (`Rule 25`), `0` `Ready-to-Publish Social & Community Promotion Kit` sections, and `0` unverified internal acronyms (`GEAP`, `ARD`, `NLC`, `Redis`).
4. **Live 20/20 Google Cloud Implementation, 12 Provisioned Pattern A/B/C Resources, Executive Light-Theme 4-Tab E2E Pattern Execution & 27-File Codebase Workbench & 21 Pure Multi-Tenant Cloud Console Visual Proof Screenshots (`0` Cross-Project Merck Screenshots) (`GET & POST /api/blogs/gcp-verify`, `src/data/gcpPatternCodebaseAndExecutionBundle.json` & `/blogs`)**:
   - Verified against real provisioned resources in `ramp-portal-dev` (`248990048888`), `cymbal-control-plane` (`638420508320`, `https://cymbal-multi-tenant-patterns-638420508320.us-central1.run.app`), and `cymbal-build-sandbox` (`887605034827`) (Pattern A `cymbal_agentic_finops_otel.pattern_a_pooled_rls_entities` with `ROW ACCESS POLICY tenant_pooled_rls_policy`, Pattern B `cymbal_silo_finvault_usw1.pattern_b_silo_finvault_cmek_vault` encrypted with Cloud KMS `finvault-silo-cmek` + ECDSA P-256 signature via `adk-agent-signing-key`, Pattern C `cymbal-pattern-c-hub-vpc`, `/28` `PRIVATE_SERVICE_CONNECT` NAT subnet `cymbal-psc-nat-us-west1`, `cymbal-pattern-c-finvault-spoke-vpc`, and `pattern_c_psc_endpoints_registry`).
   - `/blogs` enforces a 100% full-width layout (`data-testid="use-case-catalog-top-bar"`, horizontal `data-testid="official-arch-center-variant-bar"`, zero 25% left empty column), embeds the Executive Light-Theme (`Rule 54`) 4-tab `#blog-e2e-pattern-execution-and-codebase-workbench`, and embeds **exclusively the 21 pure multi-tenant Google Cloud Console & Gemini Enterprise screenshots** in `public/blogs-verification-screenshots/` (`9` live Cloud Console & Gemini Enterprise code/deploy/execute captures `gcp_console_01`..`09`, `1` live Docked Cloud Shell SSH capture `pantheon_live_user_capture_ssh_verify.png`, and `11` pure multi-tenant `@google.com` captures `real_gcp_*`, `real_ge_*`, with **0** cross-project Merck screenshots and **0** custom/composite/before-after screenshots).

### Operational Verification Command
```bash
python3 -B /Users/nitinagga/Documents/blogs/scripts/run_deep_forensic_audit.py && npx tsx scripts/verify_blogs_and_gcp_workstreams.ts && npx tsx scripts/verify_export_slides_quality_gate.ts && npx tsx scripts/evaluate_blogs_llm_judge.ts --pass=2
```

---

## 16. ☀️ `mandatory-light-theme-default-gate` (Rule 54 / Law 15 Universal Executive Light Theme Default & Zero Unrequested Dark Mode Invariant — `v1.0.0`)

### Purpose & Trigger Conditions
Triggered whenever creating, styling, refactoring, or auditing any frontend application, SaaS platform, clinical suite, dashboard, or portal across any workspace.

### Core Protocols & Architectural Contracts
1. **Universal Executive Light Theme Default (`Rule 54A`)**:
   - All applications must default to a high-contrast light palette (`bg-slate-50` `#f8fafc` canvas, `bg-white` `#ffffff` cards/tables/headers/drawers, `text-slate-900` `#0f172a` primary text, `text-slate-600` `#475569` secondary text, `border-slate-200` `#e2e8f0` borders, and light semantic badges `bg-cyan-50 text-cyan-900`, `bg-emerald-50 text-emerald-900`, `bg-amber-50 text-amber-900`, `bg-rose-50 text-rose-900`).
2. **Zero Unrequested Dark Mode (`Rule 54B` & `Rule 54C`)**:
   - Strictly ban `class="dark"`, `bg-slate-950`, `bg-slate-900`, and `#020617` on root containers and primary UI surfaces unless dark mode is explicitly requested by the user.

---

## 17. 🎭 `omni-digital-twin-voice-and-video-invariants` (Rule 48 Omni 1.1 Digital Twin Studio Video, 810 MP4s + 810 MP3s, Native Omni 1.1 Cohesive AV Bundle Purity, Transparent Studio Canvas, WebAudio Guard, On-Screen Health Inspector, 13-Project Menu Parity & Zero Legacy Code Execution Paths — `L30-01`..`L30-21`)

### Purpose & Trigger Conditions
Triggered whenever modifying `/slides` (`src/portal-views/slides-fullscreen.html`), `src/portal-views/live-demo-narrator.html`, `src/mcp-server/server.mjs`, `src/mcp-server/omniManifestLoader.mjs`, `src/mcp-server/customPersonaStore.mjs`, `custom-personas/*.json`, `scripts/generate_omni_cohesive_slide_videos.mjs`, `scripts/generate_nitin_native_omni_bundles.mjs`, or `scripts/prebake_a2a_gateway_omni_assets.mjs` in `Demoes-GE`.

### Core Protocols & Architectural Contracts
1. **5-Deck Full Pre-Baking (`810 MP4s + 810 MP3s`), Native Gemini Omni 1.1 Cohesive AV Bundle Purity (`90/90 custom-nitin-aggarwal-live MP4s`), Real 1280x720 Studio Loop & Transparent Studio Video Canvas (`L30-16`, `L30-17`, `L30-19`)**:
   - All 5 Omni decks (`a2a-enterprise-gateway`, `merck-aws-mcp-consent`, `merck-agentgateway-policy`, `merck-adk-a2a-a2ui-playbook`, `merck-skills-workflow-playbook`) $\times$ 9 Digital Twin personas $\times$ 18 slides = `810` 24fps `.mp4` videos and `810` `.mp3` tracks, backed by `screenshots/avatars/custom/custom-nitin-aggarwal-live-studio-loop.mp4` (`1280x720`, `24fps` Gemini Omni 1.1 studio video) and zero `(voice of <Name>)` prompt triggers.
   - All `90/90` (`18` slides $\times$ `5` decks) `custom-nitin-aggarwal-live` `.mp4` files must be generated directly by `models/gemini-omni-1.1-flash` (`https://generativelanguage.googleapis.com/v1beta/interactions`) as untouched native Gemini Omni 1.1 cohesive audio+video bundles (`0` `Lavf62.29` `ffmpeg`-patched audio/video muxes, `0` `studio-loop` or `slide_01` fallback substitutions) with companion `.mp3` files extracted directly from the native Omni bundle, and `syncFacePresenterWithSlide()` must keep `omniVid` paused on a closed-mouth frame when `!isNarrating` so the presenter's lips never move during silence (`L30-19`).
   - Whenever `#aiPresenterOmniVideo` has an active studio video (`hasActiveStudioVideo`), `#aiPresenterAvatarCanvas` stays 100% transparent over the video body, and `window.attachOmniAudioAnalyser` never attaches `createMediaElementSource` to `<video id="aiPresenterOmniVideo">` or while `omniAudioCtx.state === 'suspended'`.
2. **On-Screen Digital Twin Health Inspector, Honest Status Polling & 1-Click Self-Healing (`L30-18`, `L30-19`)**:
   - Never hardcode `'Authentic 60fps Twin · Ready ✅'` in `renderMyPresenterList()`; poll `GET /api/persona/custom/:id/status?demoKey=<deck>&totalSlides=<N>` for real-time MP4/MP3 counts (`🟢 18/18 MP4 · 18/18 MP3 Ready ✅`).
   - Expose `#pipHealthStatusBadge` in the top-left of `#aiPresenterVideoPip` and `#digitalTwinHealthInspectorCard` in **🎛️ Customize → 3. Face Host & Digital Twin** (`GET /api/digital-twin/health`, verifying `video.nativeBundleCount === 18` and `video.lipSyncMode === 'native_omni_1_1_bundle'`), with 4 1-click self-healing buttons (`🔊 Heal & Unmute Audio`, `🪄 Sanitize & Repair Twin` via `POST /api/persona/custom/:id/sanitize-and-retry`, `⚡ Pre-Bake All 18`, and `🎬 Mode: Studio MP4 / 🖼️ Mode: 2D Avatar`).
3. **Zero Legacy Code Execution Paths & Merck AWS MCP Consent Dual-Path + Standalone Zero-Code AgentGateway Runtime Routing Policy (`L30-20`..`L30-21`, `merck-aws-mcp-consent`, `merck-agentgateway-policy`)**:
   - `scratch/audio_cache/omni-video/` must contain `0` stale single-shot `.mp4` files; `lookupPreRenderedOmniSlideVideo` (`src/mcp-server/server.mjs`) and `resolveLocalOmniCohesiveVideo` (`src/portal-views/slides-fullscreen.html`) must prioritize canonical `screenshots/omni-video/<demoKey>/slide_XX_<videoTwin>.mp4` over dynamic cache.
   - `MERCK_ADK_A2UI_OMNI_MANIFEST_BY_SLIDE` (`slides-fullscreen.html`) and `CANONICAL_OMNI_SLIDE_SCRIPTS_BY_DEMO['merck-adk-a2a-a2ui-playbook']` (`omniManifestLoader.mjs`) must match the full 3-shot spoken scripts; `resolveInitialDemoKey()` must default to `'merck-adk-a2a-a2ui-playbook'`; `enqueueAllSlidesPrebakeForCustomPersona` must guard with `if (!resolveDeckOmniScripts(demoKey)) return;` and `ACTIVE_CUSTOM_PREBAKE_JOBS`; `computeAndCacheClipSpeechEndSec` must skip canonical `/screenshots/omni-video/` bundles; and `live-demo-narrator.html` must never invoke `window.speechSynthesis.speak(`.
   - The Merck AWS Bedrock AgentCore MCP Gateway Secondary Tool Auth & Consent Orchestration (`src/a2a-crosscloud/`, `/Users/nitinagga/aws/`, `/slides?demo=merck-aws-mcp-consent` [18 slides], `/codelab?demo=merck-aws-mcp-consent` [10 steps], and standalone Zero-Code AgentGateway Runtime Routing Policy demo `DEMO-MERCK-AGENTGATEWAY-POLICY` at `/slides?demo=merck-agentgateway-policy` [18 slides], `/codelab?demo=merck-agentgateway-policy` [10 steps], `/live-demo?demo=merck-agentgateway-policy` [4 cues], and `/api/merck-agentgateway-policy/*`, deployed and executed on Google Cloud Run in `ramp-portal-dev` / `us-west1` across `a2a-remote-peer`, `a2a-ge-orchestrator`, and `ge-demos` on `cr-infra-vpc-network` / `cr-infra-subnetwork`, and live on AWS Account `393036065405` / `us-east-1` across Lambda `cymbal-a2a-mcp-remote-peer` + Bedrock AgentCore Gateway `cymbal-a2a-mcp-gateway-suyxm3caof`) must intercept `-32042 elicitation/create (mode="url")` across `ServiceNow` (`CHG0049218` / `INC0948211`), `Muse` (`FV-GXP-2026-04` Cohort-B clinical biomarkers), and `SharePoint`, sanitize unconstrained JSON Schema 2020-12 `inputSchema.properties.body: {}` (`G9`), isolate parallel tool calls sharing `contextId` via composite `(context_id, task_id, connector_id)` keys (`G10`), block LLM orchestrator consent spoofing via HMAC-SHA256 `stateToken` verification (`G11`), scale tool discovery across `1,250` enterprise tools via `POST /mcp/tools/search` with zero-LLM model flexibility and bidirectional GCP/AWS `X-Correlation-Id` logging (`G12`), provide the Zero-Code AgentGateway Runtime Routing Policy (`G13`–`G15` / `AWS-G13`–`AWS-G15`: `POST /mcp`, `GET /mcp/gateway-policy/config`, `POST /mcp/gateway-policy/route/{domain}` partitioning `1,250` tools into `25` domain tools $\le 128$ limit), pass all 15 E2E gates (`G1–G15` in `src/a2a-crosscloud/e2e_report_cloudrun.json` & `AWS-G1–AWS-G15` in `/Users/nitinagga/aws/merck_aws_agentcore_e2e_report.json`), and pass the Cloud Run Multimodal LLM-as-a-Judge & Accuracy/Correctness/Faithfulness evaluations (`data/llm_judge_merck_aws_mcp_consent_iter_3.json` & `data/merck_agentgateway_policy_15gate_evaluation.json`, `PASS`).

### Operational Verification Command
```bash
npm run quality-gate
```
Asserts 100% pass across all 73 checks (`28/28` Level 10, `24/24` Level 20, `21/21` Level 30).


### Merck Omnichannel Spoke Doc Sync (`sync_merck_omnichannel_spoke.py` & `L50-61`)
- **7-Step Omnichannel Sync, Deduplication, Merck-Only Filter (`Step 3A`), Strict Nitin Aggarwal Involvement Filter (`Step 3B`) & Teammate Sanitization Protocol (`Step 6`)**:
  - `scripts/sync_merck_omnichannel_spoke.py` synchronizes **ONLY** Merck workstreams, meetings, trackers (`1X9321KNfRdjuQb9rfmlp9oExXc0RkWo7S2db_CnoFMU`, `1y7kt8gB7XNwtmLG3hIxgNGVki5e1tt3Aifk29LmixJY`, `1O9mmw3hcGk4U6BcQhKrH5EQUBM0VXz8gNlffsEx_IrA` Row 6, `1xLQdm3U4jpHcVpGN8nRSytO9GsVLOvqQ3u-gjjvuX28`, `1L-uRJySb8m4iOfdyQ64uPY3-f6hj4MTnnjIjasHHhEU` Row 90, `17SBQiySZ9FrHOtVr6eS3CnbCUrC9jn3SW8HgXdY9PTw` Row 27, `1w2CFGNFfSDfozwOrbi3a4y_njSM7XdtQ4XmT4m0pME4` Status Rows 14..103 & `ASK-002..004`), `33+` Buganizer tickets owned by `nitinagga`, Google Chat Spaces (Rule 22 11-char IDs), and GCP/AWS/Gemini Enterprise engineering deliverables where **Nitin Aggarwal (`nitinagga@google.com`)** is directly doing/owning/building the work or directly a participant into the Federated Meeting Notes Spoke Doc (`1Djo0dKVprT_X7M1QTrPJniMbm8sDMDKX3W8Exon4NCw`, or Test Clone `1Jk3G_gsdo_gOUXGaaOzr5RLK_EV3GmnsYtrbYWy17EA`) across Overview Tab `t.trgr53jsi0l2` and Raw Meetings Notes Tab `t.bui7oulgwhkw` via Rule 49 native `drive.files.copy` + `documents.batchUpdate` (`0` Drive HTML multipart uploads).
  - Scheduled for weekday 6:00 PM EST (`CRON_TZ=America/New_York 0 18 * * 1-5`) via `/Users/nitinagga/.gemini/config/sidecars/merck_omnichannel_notes_sync/sidecar.json` and writes audit receipts to `reports/merck_omnichannel_spoke_sync_receipt.json`.

---

## 18. 🛡️ `direct-sot-6hop-end-to-end-sync-and-zero-permission-stalling` (Rule 28 / Law 17 Verification Protocol)

### Purpose & Trigger Conditions
Triggered whenever modifying upstream portal harvesters (`scripts/direct_sot_harvester.py`, `scripts/upstream_portal_synchronizer.py`), backend search/lookup/sync routes (`gsheet_sync_server.py`), or frontend polling and search handlers (`src/App.tsx`, `src/data/lineageData.ts`, `src/components/MultiSourceTrackerPageTab.tsx`, `src/components/AutomatedFeatureRequestCrStudioTab.tsx`, `src/components/OfficialRoadmapDashboardTab.tsx`).

### Core Protocols & Architectural Contracts
1. **Strict Ban on Diagnose-and-Ask-Permission Stalling (`Rule 28A`)**:
   - Whenever the user asks a verification question (*"what will happen if I search X?"*, *"is this good enough?"*, *"is this complete, accurate, relevant, and grounded now?"*) or points out a flaw, and your diagnostic audit discovers **any** gap, bug, truncation, stale cache, or unwired UI/backend path, you MUST **fix all discovered gaps immediately in the exact same turn** without asking *"Shall I apply these fixes?"*.
2. **Mandatory 6-Hop 360° End-to-End Data-Path Verification (`Rule 28B`)**:
   - **Hop 1 (Producer Completeness)**: `scripts/direct_sot_harvester.py` must persist all discovered Buganizer (`verifiedBuganizerTickets`) and SFDC (`verifiedSfdcCases`) entries without `[:30]`/`[:20]` slicing.
   - **Hop 2 (Multi-Store Atomic Disk Sync)**: `scripts/direct_sot_harvester.py` must atomically update `.local_backup/local_lineage_records.json`, `.local_backup/runtime_lineage_records.json`, AND `.local_backup/gantrypulse_sot.db` (`lineage_records` table) in lockstep.
   - **Hop 3 (Backend In-Memory Mtime Parity)**: `load_lineage_records()` in `gsheet_sync_server.py` must compare `max(db_mtime, json_mtime, rt_mtime)` and read `_RECORDS_FILE` whenever `json_mtime >= db_mtime`.
   - **Hop 4 (Unified Multi-Store Search & Lookup Stitching)**: `build_ticket_lookup_payload()`, `execute_federated_search()`, and `execute_live_buganizer_sfdc_search()` must invoke `lookup_direct_sot_ticket_across_all_stores()` across Master Lineage + Direct-SoT + EAP + Multi-Source + live IssueTracker REST API (`_probe_live_buganizer_api_issue`), returning forensic-compliant `LIN-DSOT-<id>` records.
   - **Hop 5 (Frontend Reactive State, Equal-Width/Height Row Grid, 3-Stage Excel Tree-Grid & Row/Column Merge [`Rule 30M`], 8-Point Customer Email & Google Chat Space Copy Sanitization & Polling)**: `src/App.tsx` (`runGlobalBackgroundSync`, `customer_asks_excel` / `5.1 Asks (Excel Tree)`) diffs `lastVerifiedSyncAt` and `lastDirectSotVisitedAt`; `MultiSourceTrackerPageTab.tsx` (`Rule 30M` 40px Compact Excel Rows across 11 resizable columns, `Expand All / Collapse All`, 4 dossier sub-section toggles, 3-level Tree-Grid with `→`/`←` Indent/Outdent + `Group By` + `Context Parent` filtering, Floating Action Bar row merge/unmerge, vertical `rowSpan` cell merge with `cq-col3-linked-rowspan-digest-*`, and horizontal `colSpan={2}` cell merge verified by `scripts/verify_customer_asks_excel_treegrid_merge_e2e.mjs`), `UnifiedCommunicationModal.tsx` (`recordKey`-stabilized `useEffect` hooks across 30s polls, exact mixed-case Base64 Space IDs, `formatChatPlainTextWithMode` thread-mode formatting), `communicationTemplateManager.ts` (concise 3-part `chat_general_question_ask` & internal-audience `chat_account_status_update`, space-separated `@`-mentions, zero `@nitinagga` self-tags), `customerEmailHtmlFormatter.ts` (`sanitizeEmailThreadSubject`, `formatHumanFirstNameList`, `cleanInternalSyntheticJargon`), `AutomatedFeatureRequestCrStudioTab.tsx`, and `OfficialRoadmapDashboardTab.tsx` dynamically poll `/api/eap-tracker/status`, `/api/three-pages-index` (`/api/multi-source/records`), and `/api/roadmap-plx`.
   - **Hop 6 (Automated Fail-Closed Quality Gate)**: Enforced in `scripts/stop_forensic_gate.mjs` (`Rule 28C`).

---

## 19. 🎨 `slide-design` (`google-slides-design` Enterprise Google Slides Design, 6 Native Architectural Visual Archetypes & Grounded Screenshot Hybrid Plugin — `v2.0.0`)

### Purpose & Trigger Conditions
Triggered whenever the user asks to create, design, draft, or outline Google Slides, pitch decks, or technical demos (`~/.gemini/config/plugins/google-slides-design/` and `~/.gemini/config/skills/slide-design/SKILL.md`). Also pairs with `deepmind-emotional-audio-engine` (`compileSSML`, `computeHumanWordTimings`, `COACHING_PERSONA_CONFIG`) when slide decks are narrated in `/slides` and `/live-demo`.

### Core Brand Rules, 6 Native Editable Visual Archetypes & Grounded Screenshot Hybrid (`rules/AGENTS.md`, `skills/slide-design/SKILL.md`, `hooks.json`)
1. **Google Brand Color Sequence & Enterprise Architecture Palette**:
   - Sequential use of Google brand colors must strictly follow `1. Blue (#4285F4)` -> `2. Red (#EA4335)` -> `3. Yellow (#FBBC04)` -> `4. Green (#34A853)`.
   - Enterprise architecture diagrams combine the Quad-Color sequence with Deep Navy (`#0F2942` / `#0B2545`), Deep Teal (`#0D7A75` / `#137369` / `#1B5E7B`), Slate Blue (`#54728C`), Warm Amber (`#CA8A04`), Alert Red (`#D93025`), and Success Green (`#1E8E3E`).
2. **Typography & Containers**:
   - Slide Titles & Display Numbers: `Google Sans` / `Google Sans Display` (`#3C4043` / `#0F2942`).
   - Body Copy & Captions: `Roboto` or `Google Sans Text` (`#5F6368`); Wire Payloads: `Roboto Mono` (`7.5pt–10pt`).
   - Containers: Light gray (`#F8F9FA`) or white (`#FFFFFF`) with subtle borders (`#DADCE0`) and `8px` border-radius; `"Proprietary + Confidential"` footer on every slide; Widescreen `16:9` (`720pt x 405pt`).
3. **13 Canonical Semantic Layouts (6 Core Brand + 6 Native Editable Visual Archetypes + 1 Grounded Screenshot Proof)**:
   - Core Brand Layouts: `title-cover`, `quad-metrics`, `three-pillar`, `comparison-grid`, `section-divider`, `next-steps`.
   - `three-zone-architecture` (`architecture-zone-topology`): 3-Zone End-to-End Architecture (`Client/AI Zone` -> `Cloud Run / Gateway Engine Zone` -> `Enterprise Internal VPC Zone` in `#0B2545` dark navy with nested white component cards and directional arrows).
   - `payload-transformation` (`payload-transformation-triptych`): 3-Stage Wire Payload Transformation (`Incoming Contaminated/Error Request` [`#D93025` border] -> `Normalization / Policy Engine` [`#1B5E7B` teal container with 3 inner stage pills] -> `Clean Compliant Payload` [`#1E8E3E` border]).
   - `swimlane-sequence` (`uml-sequence-swimlane`): 5-Actor UML Lifeline & Numbered Sequence Diagram (`1..6`) with actor headers, vertical lifelines, activation bars, horizontal request/response arrows, and dormant scale-to-0 hold band.
   - `roadmap-timeline` (`phased-roadmap-timeline`): 3-Phase Connected Horizon Roadmap (`Phase 1` `#0F2942`, `Phase 2` `#0D7A75`, `Phase 3` `#54728C`) with top header bands and dual circular inter-card connectors (`● ●`).
   - `async-state-machine` (`async-state-flow-pipeline`): 4-Node Horizontal State Machine & Feedback Loop (`Node 1` Navy -> `Node 2` Amber `#CA8A04` -> `Node 3` Teal `#137369` -> `Node 4` Dark Teal `#0F766E`) with numbered callouts (`1..5`) and a bottom return feedback loop arrow.
   - `operating-model-pillars` (`strategic-operating-model-pillars`): 3-Pillar Executive Operating Model Cards with top & bottom colored accent bars (`#0F2942`, `#0D7A75`, `#54728C`), top icon badge (`01`, `02`, `</>`), centered bold header, and 3 grounded bullet points per card.
   - `grounded-screenshot-proof` (`live-screenshot-callout`): Embeds real Google Cloud Console / Gemini Enterprise / AWS screenshots (`<p:pic>` / `createImage`) paired with a 4-card Quad-Color editable verification callout rail and full speaker notes.

---

## 20. ⚡ `jetski-slash-commands-and-budget-guard` (`go/jetski-slash-commands` 4-Tier Slash Command Harness, 72 Dynamic `/<skill-name>` Commands, 5 Native `.agents/workflows/*.md` Workflows, 28 Native `.md` Subagents & `<user_rules>` Token Budget Guard — `v3.18.0`)

### Purpose & Trigger Conditions
Triggered whenever invoking or configuring Jetski System Slash Commands (`/review-agent`, `/plan`, `/grill-me`, `/goal`, `/schedule`, `/learn`, `/compact`, `/btw`, `/browser`), Multi-Agent Orchestrator Slash Commands (`/owl`, `/swarm`, `/teamwork-preview`, `/run-workflow`, `/deepagent`), Built-in Jetski Commands (`/automation`, `/plugin`, `/jetski-customizations`, `/ui-plugin-development`, `/generative_ui`), or any of the **72 Dynamic Skill Slash Commands (`/<skill-name>`)**, **5 Native Workspace Workflows (`.agents/workflows/*.md`)**, and **28 Native Markdown Subagents (`~/.gemini/config/agents/*.md`)**.

### Core Invariants & Architectural Contracts
1. **Zero Duplicate Global `AGENTS.md` Symlinks & Progressive-Disclosure Rule Frontmatter (`tokens.GetCustomizationBudget` Guard)**:
   - `~/.gemini/config/` must contain strictly **1** top-level rule file (`~/.gemini/config/AGENTS.md` `< 24,000 bytes`, with `0` duplicate `~/.gemini/config/GEMINI.md`, `~/.gemini/config/CLAUDE.md`, `~/.gemini/AGENTS.md`, or `~/.gemini/GEMINI.md` symlinks) so `language_server` (`topLevelFileCustomization`) injects `<RULE[user_global]>` & `<RULE[~/.gemini/config/AGENTS.md]>` without `4x` (`95,564 bytes`) symlink duplication.
   - Every rule file in `~/.gemini/config/rules/*.md` (`15/15`) must begin with valid YAML frontmatter (`trigger: always_on` for the 1 universal visual proof rule `before-and-after-screenshots.md` [`1,396 B`] and `trigger: model_decision` + `description:` for the 14 project-specific rules [`99,992 B`]), cutting unconditional `<user_rules>` prompt consumption by **`-88.3%`** (`216,892 bytes` $\rightarrow$ `25,287 bytes`, saving **`~47,901 tokens/turn`**) and preventing `<skills>` eviction.
2. **28 Native Markdown Custom Agents (`~/.gemini/config/agents/*.md`)**:
   - Every custom agent in `~/.gemini/config/agents/` (`28/28`, including `review-agent-verifier.md`, `gantrypulse-6hop-sot-auditor.md`, `gantrypulse-link-and-chat-verifier.md`, `gantrypulse-ui-table-auditor.md`, `blogs-arch-center-auditor.md`, `scorex-forensic-auditor.md`, `demoes-ge-omni-twin-av-auditor.md`, `release-deploy-verify.md`, etc.) must be defined as a native `.md` file with YAML frontmatter (`name`, `description`, `mainAgent: true`, `subagent: true`, `commandExecutionPolicy: auto`) so `invoke_subagent`, `/owl`, `/swarm`, and `/teamwork-preview` can spawn them directly.
3. **72 Dynamic `/<skill-name>` Slash Commands, Isolated `.datacloud_skills_manifest` & Cross-Workspace `/review-workspace` Fallback**:
   - All 72 skills in `~/.gemini/config/skills/*/SKILL.md` (with SHA-256 checksums locked in `~/.gemini/config/skills.json` and the 21 DataCloud-owned skills isolated in standalone `~/.gemini/config/skills/.datacloud_skills_manifest`) expose native `/<skill-name>` slash commands across all project workspaces (`GantryPulse`, `AskAIOCE`, `PromptCanvas`, `ScoreX`, `Demoes-GE`, `a2a-enterprise-gateway`, `DossierHarmonizer`, `book`, `ideas-mining`).
   - Because `/review-agent` Mendel Arm 3 (`Review Loop`) requires a `google3` CitC workspace, `/review-workspace` (`~/.gemini/config/skills/review-workspace/SKILL.md`), `/review-agent` (`.agents/workflows/review-agent.md`), and `review-agent-verifier` (`~/.gemini/config/agents/review-agent-verifier.md`) provide deterministic 3-Arm Staged Specification + Adversarial Critique + Domain Quality Gate verification across both local Git repositories and CitC workspaces (including `Rule 30P` Default Wrap-Text `wrap_auto` everywhere across GantryPulse).

---

## 21. 🎯 `rule57-inked-pixel-arrow-centering-and-canonical-infographic-gate` (`Rule 57` / `Law 18` — `diagram-generation-engine`, `diagram-decompilation-and-geometry`, `automated-visual-regression-and-viewport-gate`, `promptcanvas-blueprint-cert`)

### Purpose & Trigger Conditions
Triggered whenever creating, modifying, syncing, or auditing Draw.io / SVG infographics and architectural diagrams across `PromptCanvas` (`src/lib/canonical/openKnowledgeInfographic.ts`, `src/lib/canonical/infographicBlueprints52to66.ts`) and `ideas-mining` (`T01` + `T53`–`T78`, `scripts/sync_canonical_promptcanvas_infographics.mjs`, `scripts/verify_arrow_label_inked_pixel_centering.mjs`, `tests/test_factory.py`).

### Core Invariants & Architectural Contracts
1. **Inked-Pixel (`ctx.getImageData`) Vertical ("Mid") & Horizontal ("Center") Arrow-Label Calibration (`Rule 57C`)**:
   - Never rely solely on DOM `div` `getBoundingClientRect()` to certify inline arrow labels (`parses`, `enriches`, `verifies types`, `yes`, `no`, `federates` in `T68`; `uses`, `calls`, `returns results`, `yes`, `no`, `maps` in `T53`; and all 8 inline arrow labels across `T01` and `T69`–`T78`), because CSS `line-height` (`1.2`) and font ascender headroom push lowercase `x`-height letters `2px–2.5px` (`4–5` Retina pixels) below the `div` center.
   - Wrap all inline arrow labels in `<span style='padding:0 2px;'>...</span>` with `labelBackgroundColor=#ffffff` so a `2px` white cushion separates the arrow shaft from the first and last letters.
   - Apply calibrated `<mxPoint as="offset">` coordinates (`t1_edge_1`: `x="-5" y="-2"`, `t2_edge_calls`: `x="-5" y="-2"`, `t2_edge_returns`: `x="0" y="-2"`, `t3_e_yes1`: `x="-5" y="-1.5"`, `t3_e_no1`: `x="0" y="-6"` + `line-height:0.9`, `t3_e_yes2`: `x="-5" y="-1.5"`, `t3_e_no2`: `x="5" y="-1.5"`, `t4_edge_maps`: `x="-5" y="-2"`) so that `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|left_visible_shaft - right_visible_shaft| <= 1.0px` at `2x` Retina.
2. **Fresh Puppeteer `browser.newPage()` Per `viewer-static.min.js` Render**:
   - Sequential Draw.io renders in `scripts/sync_canonical_promptcanvas_infographics.mjs` must open and close a fresh `browser.newPage()` per diagram so `window.GraphViewer` never retains stale DOM state across `page.setContent()` calls.
3. **100% Native Editable `.pptx` & Google Slides Sync for All 27 Draw.io Templates (`T01` + `T53`–`T78` — `Rule 47` & `Rule 57`)**:
   - `scripts/compile_and_sync_template_slides.mjs` compiles all 27 Draw.io templates (`T01` + `T53`–`T78`) into multi-slide 100% native editable PowerPoint files (`assets/template-gallery/<tid>.pptx`: Slide 1 = Full Editable Poster + Executive Summary Rail; Slides 2..N = Full-Width `16:9` Widescreen Editable Section Deep-Dive Slides) and syncs them via Google Drive v3 API (`grant_type=refresh_token`, `x-goog-user-project: "ramp-portal-dev"`) into `data/template_google_slides_manifest.json` and `assets/template-gallery/gallery_manifest.json`.
4. **Rule 30R & Rule 30T — GantryPulse 18-Route E2E Forensic UI/UX, Workflow, Non-Technical Usability, Unclamped Oct 20–27 Customer Questions Freshness (`114` Threads / `115` Items) & Live-Truth Certification (`GP-WF-01..04`, `GP-UI-01..03`, `GP-UX-01..09`, `GP-SOT-01..04`)**:
   - Enforces `normalizeChangeLogEntryShape()` across `App.tsx`, `ConfigAndChangeLogTabs.tsx`, and `scripts/direct_sot_harvester.py` (`GP-WF-01`), `beforeunload`/`pagehide` SSE cleanup (`GP-WF-02`), `data-testid="sidebar-tab-<id>"` across all 18 sidebar tabs (`GP-WF-03`), `seenIds` deduplication in `LiveMultiSourceSotExplorer.tsx` (`GP-WF-04`), `firstRowTopPx <= 380px` above-the-fold table positioning (`GP-UI-01`), Light-Theme `#ffffff` sidebar (`GP-UI-02`), zero 1-character vertical pill wrapping (`GP-UI-03`), right-side slide-over drawers (`GP-UX-01`), consolidated `#ask-gantrypulse-trigger` header trigger (`GP-UX-02`), 5-card plain-English "What Are You Looking For Today?" Guided Task Launcher (`data-testid="non-tech-guided-task-launcher"`) on `?tab=dashboard` (`GP-UX-03`), `0/7` truncated sidebar labels & `0` duplicate `← KPI Dashboard` sub-view buttons (`GP-UX-04`), `0` raw `compId=`/`LIVE_CHROME_ACTIVE_TAB`/`Vector #0014M` internal ID leaks (`GP-UX-05`), Light-Theme control bar + progressive-disclosure `🔍 Filter Slicers (6) ▾` (`GP-UX-06`), plain-English Official Roadmap filter pills (`0` `Table 3/8/11/14`) & `@ldap` Ticket Owner formatting (`GP-UX-07`), `0` duplicate bottom sheet-view tabs + plain-English quick guide badge (`GP-UX-08`), `WeakMap` memoization (`RESOLVED_COMMS_WEAK_CACHE` & `ROW_JUDGE_REPORT_WEAK_CACHE`) in `MultiSourceTrackerPageTab.tsx` (`GP-UX-09`), zero passive-tab `now_iso` / `today_date` timestamp clobbering, deterministic `lineageFileSha256`, union-merged `>= 14` `.local_backup/local_changelog.json` entries, `POST /api/gantrypulse/run-live-audit` (`GP-SOT-01..04`), and `Rule 30T` (`114` corporate Gmail threads in `commsLinkResolver.ts`, `115` Customer Questions through `2026-10-27` in `customerQuestionsData.ts` with `0` `<= '2026-10-19 23:59'` ceilings or `void dynamicQuestions;` loops, and outbound HTTPS push from `force_realtime_sot_sync.py` & `auto_gmail_eap_scanner.py` to `POST /api/portal/push-live-sot`).
5. **29 Certified Canonical Blueprints (`#78`–`#84`, `#00`, `#38`, `#42`, `#44`, `#67`–`#69` + `#52`–`#66`) & Lean 8 Pharma Regulatory Rigor Document Studio (`DOC 01`, `02`, `03`, `05`, `13`, `07`, `09`, `17`)**:
   - Enforces `22/22` certified canonical blueprints (`14` Core Reference/Architecture/Flow `#78`–`#84`, `#00`, `#38`, `#42`, `#44`, `#67`–`#69` + `15` Infographics `#52`–`#66`) in `CANONICAL_TEMPLATES` & `CANONICAL_CONTRACTS`, and consolidates `/docgen` & `/docgen/[id]` into the Lean 8 Pharma Regulatory Rigor surviving archetypes (`brd`, `prd`, `sdd`, `tdd`, `ai_system_card`, `threat_model`, `security_package`, `sre_resilience`) while purging all 9 redundant archetypes (`fdd`, `exec_brief`, `api_spec`, `workshop`, `interview_defense`, `cloud_migration`, `vendor_rfp`, `cloud_finops`, `golive_runbook`).
6. **`ge-blogs` 10-SaaS × 3-Pattern (`30/30`) Cloud Run $\leftrightarrow$ AWS AgentCore MCP + S3 + GCP BigQuery/KMS Live Verification (`Rule 53` & `Rule 56`)**:
   - Enforces live execution of all `30` cross-cloud flows (`SAAS-01`..`SAAS-10` across `Pattern A`, `Pattern B`, and `Pattern C`; `60/60` positive + negative security assertions) directly from Google Cloud Run `ge-blogs` (`ramp-portal-dev` `#248990048888`, `GET /api/saas-5-live-verify` in `gate5_self_verify_entrypoint.py` emitting `CLOUDRUN_10SAAS_30FLOW_RECEIPT`) to AWS Cognito (`us-east-1_blP4L37sS`) $\rightarrow$ AWS Bedrock AgentCore MCP Gateway `cymbal-a2a-mcp-gateway-suyxm3caof` (`HXGGFMZBKE`..`C7EYM614F2`) $\rightarrow$ AWS Lambda `cymbal-a2a-mcp-remote-peer` $\rightarrow$ `s3://cymbal-aws-federation-393036065405-us-east-1` (`30` distinct S3 `ETag`s) plus GCP BigQuery RLS/CMEK/PSC and Cloud KMS ECDSA-P256 21 CFR Part 11 signing (`cymbal-multi-tenant-kr/cryptoKeys/adk-agent-signing-key` in `bbar-138hf0`).


---

## 20. 📑 `default-demo-slide-template` (`24-Slide L100–L400 Native Editable Google Cloudstyle 2.0 Master Template` — `v1.0.0`)

### Purpose & Trigger Conditions
Triggered automatically whenever the user asks to create a new demo slide deck, enablement session presentation, customer architecture briefing, or end-to-end use-case presentation in Google Slides (`~/.gemini/config/skills/default-demo-slide-template/SKILL.md` & `~/.gemini/config/rules/default_demo_slide_deck_template.md`).

### Core Protocols & Canonical Assets
1. **Immutable Starred Master Template Pair in Google Drive**:
   - **Golden Master Slide Template**: `1nUMBLuFpuBZjIt5W3TqK734uK_m2L7gbhBW8gnkscgY` (`24` slides, `1,293` native elements, Cloudstyle 2.0 `#FFFFFF`/`#F8FAFC` Light Theme). Always clone via `gslides mutate copy` into a fresh presentation ID; never overwrite in place.
   - **Companion Linked Charts Sheet Template**: `1tku_U2YdGdJOLPgI6ab3_LS5h-inxAZXnmq5BjOVEoQ` (`?resourcekey=0-gz4pnup-wGuP62BLOm4zWw`; `chartId: 2008, 2016, 2019` bound via `scripts/relink_template_sheets_charts.mjs`).
   - **Read-Only Reference Exemplar (Merck AskHR 2.0)**: `11BezxbRYY9gZ5hk6c18q-xF9WzOznh02stxlMktJYB0` (`?resourcekey=0-5n2KLt5hFxc2AenX6zdijQ`) + `1MVa6ugnjqIRRiy4AXNNL5xgNccozkkjkvpGUWLlkpf8`.
2. **100% Native Editable 6-View L100→L400 PromptCanvas Blueprint Arc (`0` Raster Diagram PNGs)**:
   - Compiles `Slides 10 (L100 Conceptual), 12 (L200 Logical), 13 (L250 #78 Hub-and-Spoke), 14 (L300 #90 C4 Hexagonal ADK Pod), 15 (L350 #81 16-Step Lifeline Sequence), 20 (L400 #79 Deployment & Dual-NIC VPC-SC)` from `.drawio` XML into native Google Slides shapes, canonical `scaleX=+1, scaleY=+1` lines, textboxes, and deduplicated transparent service icons via `scripts/compile_drawio_to_native_slides.mjs`, verified by `scripts/audit_native_slide_deck.mjs`.
