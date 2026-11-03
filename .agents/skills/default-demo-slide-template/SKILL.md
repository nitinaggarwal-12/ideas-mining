---
name: default-demo-slide-template
description: >-
  Default Golden Master Google Slides template and 100% native editable Draw.io
  vector compiler for all new demo decks, enablement sessions, customer
  architecture briefings, and end-to-end use-case presentations. Clones the
  starred 24-slide Cloudstyle 2.0 Master Template (L100->L400 6-View
  PromptCanvas progressive-disclosure architecture blueprints compiled into
  100% native editable Google Slides shapes/lines/textboxes/icons, 3 live linked
  Google Sheets charts, 4 native executive tables, Google Quad-Color section
  dividers, opening cover, 60-min TOC, BLUF summary, appendices, and grounded
  references) without asking generic style-picker questions unless the user
  explicitly requests a different slide theme.
---

# Default Demo Slide Deck Template (`24-Slide L100–L400 Native Editable Master`)

Whenever the user asks to create a **new demo presentation, enablement deck, customer architecture briefing, or use-case slide deck**, use this Golden Master Template by default—**skip** generic style-engine `ask_question` prompts unless the user explicitly asks for an alternative visual theme.

---

## 1. Canonical Google Drive Template & Companion Identifiers

| Asset Role | Drive / Presentation ID | Direct URL | Rules |
| :--- | :--- | :--- | :--- |
| **Golden Master Slide Template** *(Clone This)* | `1nUMBLuFpuBZjIt5W3TqK734uK_m2L7gbhBW8gnkscgY` | `https://docs.google.com/presentation/d/1nUMBLuFpuBZjIt5W3TqK734uK_m2L7gbhBW8gnkscgY/edit?usp=drivesdk` | **Immutable Master** (Starred in Drive). Always `gslides mutate copy` into a new deck; never overwrite in place. |
| **Companion Linked Charts Sheet Template** *(Clone This)* | `1tku_U2YdGdJOLPgI6ab3_LS5h-inxAZXnmq5BjOVEoQ` | `https://docs.google.com/spreadsheets/d/1tku_U2YdGdJOLPgI6ab3_LS5h-inxAZXnmq5BjOVEoQ/edit?usp=drivesdk&resourcekey=0-gz4pnup-wGuP62BLOm4zWw` | **Immutable Master** (Starred in Drive). Contains `Chart_Slide_8` (`2008`), `Chart_Slide_16` (`2016`), `Chart_Slide_19` (`2019`). |
| **Reference Exemplar 1 (Merck AskHR 2.0)** *(Read-Only Reference)* | `11BezxbRYY9gZ5hk6c18q-xF9WzOznh02stxlMktJYB0` | `https://docs.google.com/presentation/d/11BezxbRYY9gZ5hk6c18q-xF9WzOznh02stxlMktJYB0/edit?usp=drivesdk&resourcekey=0-5n2KLt5hFxc2AenX6zdijQ` | Live Merck AskHR 2.0 deliverable (`1MVa6ugnjqIRRiy4AXNNL5xgNccozkkjkvpGUWLlkpf8`). **Never mutate.** |
| **Reference Exemplar 2 (Atlassian Jira & Confluence 4-Pillar)** *(Read-Only Reference)* | `14CaQ0eUvNXN9PJc0ZudJ4ioMHRJtZI8v1YcWPIUTcOY` | `https://docs.google.com/presentation/d/14CaQ0eUvNXN9PJc0ZudJ4ioMHRJtZI8v1YcWPIUTcOY/edit?usp=drivesdk&resourcekey=0-noBw88PO2zLqLKduoWZP-g` | Live `jira-confluence-24slide` deliverable (`1ZUYLgGCX9qRVT0PWoiz8F5t1oPQc8J_3zvbI-zoLwBo`). **Never mutate.** |

Full per-slide `objectId`, archetype, and design-token metadata lives in [`resources/template_manifest.json`](resources/template_manifest.json).

---

## 2. The 24-Slide Executive & Technical Narrative Arc

Every deck cloned from `1nUMBLuFpuBZjIt5W3TqK734uK_m2L7gbhBW8gnkscgY` inherits `24` widescreen (`720pt × 405pt`) Google Cloudstyle 2.0 Light-Theme slides (`#FFFFFF` / `#F8FAFC`):

1. **Opening & Framing (`Slides 01–03`)**:
   - `Slide 01` (`p`): Google Cloudstyle 2.0 Cover (`Proprietary & Confidential` pill, Google Cloud wordmark, 4-color bar, subtitle, presenter/date metadata).
   - `Slide 02`: Session Roadmap / 60-Minute Table of Contents (6 timed chapters).
   - `Slide 03`: Executive Summary (`BOTTOM LINE UP FRONT`) + 4 Hero KPI Callout Cards.
2. **Chapter 01 — Platform Foundation (`Slides 04–06`, Google Blue `#4285F4`)**:
   - `Slide 04`: Section 01 Divider (`#4285F4` background, white display typography).
   - `Slide 05`: Platform Evolution & Portable Runtime Architecture (Before vs. After comparison).
   - `Slide 06`: Core Platform Primitives (2×3 Bento Card Grid).
3. **Chapter 02 — Business Case, CUJs & L100 Conceptual View (`Slides 07–10`, Google Green `#34A853`)**:
   - `Slide 07`: Section 02 Divider (`#34A853` background, white display typography).
   - `Slide 08`: Business Baseline & Adoption Catalyst (**Live Linked Google Sheets Chart #1**, `chartId: 2008` + KPI rail).
   - `Slide 09`: Personas, Behavioral Guardrails & 4 Critical User Journeys (**Native Table #1**).
   - `Slide 10` (`s10`): **Blueprint — L100 Conceptual Multi-Agent System Model** (`bp_01_conceptual.drawio` compiled to native shapes/lines/textboxes/icons + 3-card right Executive Design Rail + `NEXT ZOOM →` bridge).
4. **Chapter 03 — End-to-End Working Architecture (`Slides 11–17`, Google Yellow `#FBBC04` + `#202124` Ink)**:
   - `Slide 11`: Section 03 Divider (`#FBBC04` background with high-contrast `#202124` ink—never white text on yellow).
   - `Slide 12` (`s12`): **Blueprint — L200 Logical Multi-Agent Subsystems** (`bp_02_logical.drawio`).
   - `Slide 13` (`s13`): **Blueprint — L250 Official `` Cloud Hub-and-Spoke Topology** (`bp_03_hubspoke78.drawio`: `#1A73E8` frame, `#AECBFA` Routing Hub, `#CEEAD6` Governance Hub, `#FEEFC3` Left Spoke, `#FAD2CF` Right Spoke).
   - `Slide 14` (`s14`): **Blueprint — L300 C4 Hexagonal ADK Pod (``)** (`bp_04_technical_g07.drawio`).
   - `Slide 15` (`s15`): **Blueprint — L350 16-Step Runtime Lifeline Sequence (``)** (`bp_05_sequence81.drawio`).
   - `Slide 16`: Zero-Trust Identity & Multi-Backend OAuth 2.0 / OBO Token Brokering (Today vs. Target dual cards).
   - `Slide 17`: Enterprise Networking — Dual-NIC VPC-SC & Split-Horizon Firewall Routing.
5. **Chapter 04 — Evaluation, L400 Deployment & Scale (`Slides 18–21`, Google Red `#EA4335`)**:
   - `Slide 18`: Section 04 Divider (`#EA4335` background, white display typography).
   - `Slide 19`: Evaluation Rigor & Golden Dataset Benchmarking (**Live Linked Google Sheets Chart #2**, `chartId: 2016`).
   - `Slide 20` (`s20`): **Blueprint — L400 Deployment, GitOps, VPC-SC & Dual-NIC (``)** (`bp_06_deployment79.drawio`).
   - `Slide 21`: Path to Production & Multi-Agent Enterprise Expansion Roadmap (3-Phase Horizon).
6. **Appendices & Grounded References (`Slides 22–24`)**:
   - `Slide 22`: Appendix A — Deep-Dive Technical Specifications, Endpoints & BigQuery/Spanner Schemas (**Native Table #2**).
   - `Slide 23`: Appendix B — White Glove Sprint Watchpoints & Security Governance (**Native Table #3** + **Live Linked Google Sheets Chart #3**, `chartId: 2019`).
   - `Slide 24`: References — Verified Documentation, Repositories & Environment Identifiers (**Native Table #4**).

---

## 3. End-to-End Execution Workflow for Any New Demo

### Step 1: Clone Both Master Templates (Preserving Slide & Chart Object IDs)
`gslides mutate copy` and `gdrive mutate cp` preserve every slide `objectId` and Sheets `chartId` (`2008`, `2016`, `2019`):

```bash
# 1. Clone the 24-slide Golden Master Deck
/google/bin/releases/gemini-agents-gslides/gslides mutate copy \
  1nUMBLuFpuBZjIt5W3TqK734uK_m2L7gbhBW8gnkscgY \
  "<Customer / Product> — End-to-End Architecture & Enablement"

# 2. Clone the Companion Linked Charts Data Sheet
/google/bin/releases/gemini-agents-gdrive/gdrive mutate cp \
  1tku_U2YdGdJOLPgI6ab3_LS5h-inxAZXnmq5BjOVEoQ \
  "<Customer / Product> — Enablement Chart Data"
```

### Step 2: Update Companion Sheet Data & Re-Link Live Charts
1. Update the numeric series and labels in `<NEW_SHEET_ID>` (`Chart_Slide_8`, `Chart_Slide_16`, `Chart_Slide_19`) via `/google/bin/releases/gemini-agents-gsheets/gsheets` so the 3 charts reflect grounded metrics for the new demo.
2. Run the bundled chart re-linker so `Slides 08, 19, 23` (and speaker notes) point to `<NEW_SHEET_ID>` (`linkingMode: "LINKED"`):

```bash
node ~/.gemini/config/skills/default-demo-slide-template/scripts/relink_template_sheets_charts.mjs \
  --pres-id <NEW_DECK_ID> \
  --sheet-id <NEW_SHEET_ID>
```

### Step 3: Adapt the 6 PromptCanvas `.drawio` Blueprints & Compile to 100% Native Editable Slides
**NEVER insert raster screenshot PNGs for architecture diagrams.** Every diagram on `Slides 10, 12, 13, 14, 15, 20` (and any added diagram slide) MUST be compiled into 100% native editable Google Slides shapes, lines, textboxes, and crisp service icons:

1. Copy the 6 reference `.drawio` exemplars into your **conversation artifact scratch directory** (never inside a CitC `/google/src/cloud/...` workspace!):
   ```bash
   mkdir -p "<ARTIFACT_SCRATCH_DIR>/blueprints"
   cp ~/.gemini/config/skills/default-demo-slide-template/examples/merck_askhr_blueprints/bp_0*.drawio \
      "<ARTIFACT_SCRATCH_DIR>/blueprints/"
   ```
2. Adapt `bp_01_conceptual.drawio` through `bp_06_deployment79.drawio` to the new demo's personas, agents, MCP/A2A/REST tools, identity broker, GCP/multi-cloud topology, 16-step runtime flow, and CI/CD environments.
3. Run the bundled native vector compiler (which automatically deletes the old `ed_sXX_*` shapes/lines/textboxes inside `pc_sXX_bp_frame`, preserves the right-hand 3-card Executive Design Rail frame, canonicalizes all orthogonal connectors to `scaleX=+1, scaleY=+1` so arrowheads never invert 180°, and uploads deduplicated transparent service icons):
   ```bash
   node ~/.gemini/config/skills/default-demo-slide-template/scripts/compile_drawio_to_native_slides.mjs \
     --pres-id <NEW_DECK_ID> \
     --blueprints-dir "<ARTIFACT_SCRATCH_DIR>/blueprints"
   ```
   *(If you reordered, added, or removed blueprint slides, pass `--config <custom_slides.json>` and `--ensure-frame`.)*

### Step 4: Customize Narrative Copy, Native Tables, Right-Rail Callouts & Speaker Notes
- Update action titles, eyebrows, KPI cards, right-hand 3-card Executive Design Rails + `NEXT ZOOM →` bridges (`Slides 10, 12, 13, 14, 15, 20`), the 4 native tables (`Slides 09, 22, 23, 24`), and structured speaker notes (`[TALK TRACK]`, `[KEY TAKEAWAY]`, `[TRANSITION]`, `[DATA SOURCE / QUERY]`) via `gslides mutate raw-batch` / `update-text` / `set-table-cell` / `set-notes`.
- If the new demo requires fewer or more slides than 24, duplicate an existing archetype slide (`gslides mutate duplicate`) or remove unneeded slides only after adapting all retained slides cleanly.

### Step 5: Mandatory Post-Build Native Editability, Domain-Purge & Visual Audit
1. Run the deterministic audit gate (passing `--forbid "Merck,AskHR,GPTeal"` whenever the new demo is NOT for Merck AskHR so zero template strings leak!):
   ```bash
   node ~/.gemini/config/skills/default-demo-slide-template/scripts/audit_native_slide_deck.mjs \
     --pres-id <NEW_DECK_ID> \
     --expect-sheet-id <NEW_SHEET_ID> \
     --forbid "Merck,AskHR,GPTeal"
   ```
2. Export thumbnails or PDF to `<ARTIFACT_SCRATCH_DIR>` (`gslides readonly export <NEW_DECK_ID> <ARTIFACT_SCRATCH_DIR>/deck.pdf --format pdf`), inspect rendered slide PNGs visually (`read_file`) to confirm zero text overlaps, zero clipped labels, and crisp arrowhead alignment, and create a `UserFacing: true` `.url.json` artifact with the full `webViewLink` (including `?resourcekey=...` from `gdrive readonly info <NEW_DECK_ID> --json` if present).

---

## 4. `ge-demos` Portal Integration (`Demoes-GE` / `https://ge-demos-248990048888.cr.gclb.goog`)

The 24-Slide Master Template is bundled as the default slide deck template (`default-24slide-l100-l400`) inside `/usr/local/google/home/nitinagga/Documents/Demoes-GE/`:
- **Self-Contained Manifest & 6 L100–L400 Blueprints**: `data/slide_templates/default-24slide-l100-l400/template_manifest.json` + `blueprints/bp_01..06_*.drawio` + `data/google_slides_manifest.json` (`defaultDemoTemplate`).
- **Bundled Compiler, Chart Re-Linker & Deck Auditor**: `scripts/slide_template/{compile_drawio_to_native_slides,relink_template_sheets_charts,audit_native_slide_deck}.mjs` (`npm run template:compile-drawio`, `npm run template:relink-charts`, `npm run template:audit-deck`, `npm run test:slide-template`).
- **REST APIs & Portal Surfaces (`src/mcp-server/slideDeckTemplatesRegistry.mjs`)**: `GET /api/templates/slide-decks`, `GET /api/templates/slide-decks/blueprint`, `POST /api/templates/slide-decks/clone` (`Rule 47` server-side refresh-token `files.copy` + `/copy` fallback), `GET /api/slides/manifest`, and UI integration across `/catalog`, `/create-demo`, `/slides`, and `/demo-generator`.


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
