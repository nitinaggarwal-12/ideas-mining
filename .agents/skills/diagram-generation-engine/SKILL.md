---
name: diagram-generation-engine
description: Comprehensive enterprise skill for compiling, generating, styling, and verifying 100% collision-free Draw.io architecture diagrams, canonical master templates, and high-contrast cloud topologies across Light and Dark themes.
---

# 📐 Diagram Generation Engine & Universal Quality Standard (SKILL.md)

This skill is the master blueprint and universal quality standard for generating, compiling, validating, styling, and repairing Draw.io architecture diagrams across **all diagramming projects, AI prompt generators, canonical master templates, and dynamic customizers**.

Every diagram generated across any system MUST strictly follow these core pillars:

---

## 🏛️ Pillar 1: Technical Invariants & Document Envelopes

1. **Mandatory XML Document Envelope**:
   - Every generated diagram string MUST be wrapped in a standard `<mxfile><diagram><mxGraphModel>` structure. Never emit bare `<mxGraphModel>` or unparented `<mxCell>` fragments.
   ```xml
   <mxfile host="embed.diagrams.net">
     <diagram id="<unique_diagram_id>" name="<Diagram Title>">
       <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" background="#FFFFFF" math="0" shadow="0">
         <root>
           <mxCell id="0"/>
           <mxCell id="1" parent="0"/>
           <!-- All diagram vertex and edge cells go here with parent="1" -->
         </root>
       </mxGraphModel>
     </diagram>
   </mxfile>
   ```

2. **16:9 Ultra-Wide Responsive Viewport Geometry**:
   - Default canvas dimensions are $1600 \times 960\text{px}$ to $1680 \times 1040\text{px}$ (16:9 aspect ratio). Never squash templates into narrow 4:3 or 21:9 viewports in embeds.

3. **Official Multi-Vendor Vector Icon Catalogs & RFC 2397 Mandate**:
   - For all cloud, multi-agent, enterprise SaaS, and database architectures, every recognized vendor service node MUST feature its official vector SVG icon embedded as an inline RFC 2397 `data:image/svg+xml` data URI (`image=data:image/svg+xml,...;imageWidth=24-26;imageHeight=24-26;imageAlign=left;spacingLeft=38-44;`).
   - Reference [`src/lib/gcpIcons.ts`](file:///Users/nitinagga/Documents/PromptCanvas/src/lib/gcpIcons.ts) for Google Cloud and [`src/lib/sapIcons.ts`](file:///Users/nitinagga/Documents/PromptCanvas/src/lib/sapIcons.ts) for SAP Ecosystem (Joule, BTP, APIM, Datasphere, HANA, S/4HANA, SuccessFactors, Concur, Ariba, SAC, Fiori, Cloud Connector).
   - **Zero Generic Boxes**: Never render vendor services as plain text boxes or substitute enterprise platforms with toy emojis.
   - **Zero External URLs**: Never reference `https://api.iconify.design/...` or external HTTP image URLs which fail in headless or air-gapped environments.

4. **Zero-Mutation Preflight Passthrough for Master Blueprints**:
   - Layout engines and repair sanitizers must recognize structured canonical master blueprints and pass them through with **zero coordinate or geometric mutation**.

5. **Top-Right Brand Block Balance**:
   - Master architecture templates must include the top-right brand block (`🧬 NOVACURA | Transforming Therapies. Improving Lives.`) to maintain balanced visual margins against left titles.

---

## 🔀 Pillar 2: Arrows, Connectors & Routing Geometry

1. **Point-to-Point Connector Straightness & Zero Stepped Jogs**:
   - When connecting between shapes with different heights, widths, or center coordinates, never rely on default `exitY=0.5;entryY=0.5;` with `edgeStyle=orthogonalEdgeStyle;` across narrow gaps, which forces ugly $90^\circ$ steps along container borders.
   - Always compute exact matching entry/exit coordinates ($Y_{\text{exit}} = Y_{\text{entry}}$ or $X_{\text{exit}} = X_{\text{entry}}$) and enforce `edgeStyle=none;` for direct straight point-to-point connectors.

2. **Geometric Waypoint Highway Planning & Zero Text Intersection**:
   - Cross-tier connector lines spanning across columns MUST route through designated open inter-row channels (e.g. gaps between cards) with explicit intermediate waypoints (`<mxPoint x="..." y="...">`).
   - Line paths must maintain a minimum **$12\text{px}$ safety margin** from all card boundaries, container headers, subheaders, and character descenders. Never route lines through the text bounding box of a card or container title.

3. **High-Contrast Label Pill Badges**:
   - All edge labels crossing container boundaries MUST use solid white or high-contrast pill badges:
     `labelBackgroundColor=#FFFFFF;labelBorderColor=#CBD5E1;padding=3;fontSize=8;fontStyle=1;fontColor=#0F172A;`

4. **Decision Diamond & Rhombus Offset Geometry**:
   - Horizontal lines entering a Rhombus shape: `lblX = -50, lblY = -18` (positions text 50px before the left tip in 100% open space).
   - Horizontal lines exiting a Rhombus shape: `lblX = 50, lblY = -18` (positions text 50px after the right tip in 100% open space).

5. **Vertical Line Side Offsets**:
   - Position vertical edge labels 28px to the right of connector lines with `lblX = 28, lblY = -10; align=left; spacingLeft=8;` so vertical arrow lines never cut through or cross text.

6. **Mandatory Typed 6-Color Connector Palette**:
   - **Synchronous / Direct Ingestion**: Solid blue (`strokeColor=#2563EB;strokeWidth=1.5;endArrow=block;endFill=1;`)
   - **Asynchronous / Event Stream / CDC**: Dashed orange (`strokeColor=#EA580C;strokeWidth=1.5;dashed=1;dashPattern=6 4;endArrow=block;endFill=1;`)
   - **AI Copilot / Vertex RAG Grounding**: Dashed purple (`strokeColor=#7C3AED;strokeWidth=1.5;dashed=1;dashPattern=4 4;endArrow=block;endFill=1;`)
   - **External Ecosystem / Partner Protocols**: Green (`strokeColor=#16A34A;strokeWidth=1.5;endArrow=classic;endFill=1;`) with protocol labels (`IDMP`, `FHIR`, `SFTP`, `REST`)
   - **Governance & Policy Oversight**: Dashed slate (`strokeColor=#64748B;strokeWidth=1.2;dashed=1;dashPattern=2 4;endArrow=open;`)
   - **Closed-Loop Feedback Returns**: Dashed teal/green (`strokeColor=#0D9488;strokeWidth=1.5;dashed=1;dashPattern=5 5;endArrow=block;`) looping back to source systems.

7. **Sequential Step Number Badges (❶..❻ / 1..6)**:
   - All process flows and data pipelines must feature explicit sequential step number badges showing execution sequence with vertical drop-lines into storage/processing tiers.

8. **Open Routing Corridors & Zero Slicing**:
   - Maintain minimum $140\text{px}$ horizontal column pitch ($gapX$) and $80\text{px}$ inter-row channel pitch ($gapY$). Connector paths must NEVER slice through intermediate cards or table vertices.

---

## 🛡️ Pillar 3: Shapes, Containers & 2D Collision Safety

1. **Strict Container Fill & Void Elimination Law ($\ge 85\%$ Fill Ratio)**:
   - Every container column (e.g. Ingress, VPC Subnets, On-Prem Core) must maintain a vertical fill ratio $\ge 85\%$:
     $$\text{Fill Ratio} = \frac{\sum \text{Child Heights} + \sum \text{Gaps}}{\text{Container Inner Height}} \ge 0.85$$
   - Never leave $>40\text{px}$ of dead void at the bottom of any container column.
   - If child elements stop short, either scale card heights/gaps proportionally or populate the complete production infrastructure baseline (such as HA System Replication, Dedicated Interconnect, Certificate Manager, Security Command Center, and Web Dispatcher).

2. **Zero Surrounding Empty Space & Full Viewport Breadth Law**:
   - Diagram viewports and parent container wrappers must utilize 100% of available screen width (`w-full max-w-none` or `max-w-8xl` (1440px) / `max-w-[1600px]`) with responsive padding (`p-6 md:p-8`). Never constrain main containers with narrow centered grids (`max-w-4xl`, `max-w-5xl`) that introduce empty white side gutters on desktop monitors.
   - Internal zone boxes and cards must scale proportionally in height and width to eliminate awkward empty dead voids inside containers and across the screen.

3. **Rounded Container Corner Insetting ($\ge 20\text{px}$ Margin)**:
   - Any child element or card positioned in the 4 corners of a rounded container (`rounded=1`, border radius $\ge 20\text{px}$) MUST maintain a minimum **$20\text{px} - 24\text{px}$ inset margin** from the container's outer bounds.
   - Never place rectangular child boxes $< 16\text{px}$ from rounded container corners to prevent sharp border clipping over rounded arcs.

4. **2D Bounding Box Collision Auto-Healing**:
   - Layout engines must perform 2D bounding box intersection checks (with 30px safety padding margin) and push overlapping nodes rightward (for same-tier overlaps) or downward (for vertical overlaps).

5. **Container Padding Standards**:
   - Maintain a minimum of $24\text{px} - 32\text{px}$ top padding in outer containers to provide clearance for container headers and icons.

---

## ⏱️ Pillar 4: Sequence Diagrams, Interaction Enclaves & Activity Loops

1. **Discrete $\ge 26\text{px}$ Channel Pitch in Flow Enclaves (`ALT`, `OPT`, `LOOP`, `PAR`)**:
   - In alternative, optional, or loop flow boxes, never combine multi-line text and connector arrows into an ambiguous shared block.
   - Every step inside an enclave MUST use discrete mxCells with exact mathematical vertical offsets ($\ge 26\text{px}$ channel between text top and connector line) so connector lines NEVER slice through text letters or descenders.

2. **Opaque Background Shielding for Enclaves / Floating Containers**:
   - Any floating sub-box, ALT container, or overlay card that sits on top of background lifelines or grid tracks MUST enforce a solid opaque background (`fillColor=#FFFFFF;` or dark mode equivalent `#0B111E`) to prevent background dashed lines from bleeding through and cutting across foreground text and icons.
   - Enforce `verticalAlign=top;` on all enclave text cells to lock character baselines.

3. **Self-Referential Activity Loops (Step ⓳ Style)**:
   - Self-referential processing steps on lifeline activation bars (e.g. `Write logs`, `Compute Embeddings`, `Cache Lookup`) MUST use orthogonal rounded loops exiting and entering the same activation bar edge with high-contrast label pills (`labelBackgroundColor=#FFFFFF;labelBorderColor=#CBD5E1;padding=2.5;`).

---

## 📊 Pillar 5: Analytical Summary Cards, Semantic Step Badges & Tech Matrix

1. **Zero-Void Proportional Card Item Scaling**:
   - Vertical item padding and bottom margins must be dynamically adjusted according to item count:
     - 4 items: `itemPadding: 6px 8px; itemMargin: 5.5px; fontSize: 9px;`
     - 5 items: `itemPadding: 4px 8px; itemMargin: 4px; fontSize: 8.5px;`
     - 6 items: `itemPadding: 2.5px 6px; itemMargin: 2.5px; fontSize: 8px;`
   - Cards fill their parent container height evenly with zero awkward empty white voids at the bottom.

2. **Semantic Step Badge Palette in Summaries**:
   - Sequence and workflow summary tables MUST use semantic flow coloring for step number badges (❶..⑳) matching the diagram's architecture tiers:
     - **User / Frontend**: Blue (`#1D4ED8`)
     - **Gateway / Network**: Teal (`#0D9488`)
     - **Orchestration / LLM**: Purple (`#7C3AED`)
     - **Policy / Guardrails**: Dark Violet (`#6D28D9`)
     - **Data Services / DB**: Green (`#059669`) / Sky (`#0284C7`)
     - **Audit / Logging**: Cyan / Sky (`#0284C7`)
     - **Returns / Responses**: Slate (`#64748B`)
     - **Error / Policy Block**: Red (`#DC2626`)

3. **Exact Technology Matrix Density Match**:
   - When replicating canonical reference cards (e.g. `TECHNOLOGY STACK`), match the exact reference icon count and 2-row layout (e.g., 4 on top, 2 centered below) with large vector icons (`20px`) and proportional spacing rather than cramming excessive small icons that leave awkward voids.

4. **HTML Entity Encoding & Plain Text Values**:
   - Always escape dynamic text strings: `&` $\to$ `&amp;`, `<` $\to$ `&lt;`, `>` $\to$ `&gt;`, `"` $\to$ `&quot;`.
   - Never wrap edge `value` attributes in unescaped HTML tags.

---

## 🔁 Pillar 6: Automated E2E Headless Chrome Visual Audit Protocol

Before declaring any diagram complete across any project, execute the automated headless Chrome test harness:
```bash
npx tsx scratch/test_canonical_11_20_perfect.ts
```
Verify the generated 2x Retina PNG screenshot:
1. Canvas is 100% visible with valid SVG elements.
2. All labels are collision-free, legible, and use high-contrast pill badges.
3. Zero jagged connector jogs along container borders.
4. Zero corner clipping over rounded container boundaries.
5. No cards or text truncated at container boundaries.
6. Zero empty white voids at the bottom of cards.
7. Opaque background shielding on all flow enclaves (`ALT`, `OPT`, `LOOP`).

---

## 🏛️ Pillar 7: Ground-Truth Structural Parity Quality Gate (Master Blueprints 01–37)

Never declare any canonical master template complete based solely on compilation (`tsc`) or non-crashing headless renders (`svg.length > 0`).

Every master template MUST undergo a structural ground-truth feature audit against its master reference in `images/*.png`:
1. **Matrix Density Parity**: Verify exact microservice/card grid counts in each tier (e.g. 5x2 grid in Template 14).
2. **Sub-diagram Enclaves**: Confirm all sub-diagram modules are present (e.g., 3 Deployment Patterns: Blue/Green, Canary, Rolling in Template 20; Failover Flow in Template 19; Privilege Pyramid in Template 17).
3. **Decision Diamonds & Feedback Loops**: Ensure decision diamonds have both `Yes` forward paths and `No` failover/return loops with closed-loop feedback routing to source nodes.
4. **Cross-Cutting Control Bars & CIDR Annotations**: Confirm all full-width enabler banners, VPC CIDRs (`10.10.0.0/16`), and subnet annotations are fully articulated.
5. **Direct Visual Review**: Inspect the rendered PNG against the reference image before marking complete.

---

## 🏛️ Pillar 8: Official Google Cloud Architecture Center Vector Icons Mandate

For all Google Cloud Platform (GCP) architectures, diagrams, and components:
1. **Zero Generic Emoji Substitution**: Never use generic emojis (such as `👑`, `⚡`, `🔑`, `🛡️`, `📊`, `🚀`, `🗄️`, `✨`) as service icons.
2. **Mandatory Official Vector SVGs**: Import and use authentic vector SVGs from `src/lib/gcpIcons.ts` (`GCP_OFFICIAL_ICONS` / `renderGcpIconHtml`):
   - **Gemini / DeepMind Core**: Official 4-point gradient Gemini diamond (`gemini`).
   - **Vertex AI / Vector Search**: Official Vertex AI (`vertex_ai`) and ScaNN Vector Search (`vertex_vector_search`).
   - **Document AI / GCS**: Official Document AI (`document_ai`) and Cloud Storage (`cloud_storage`).
   - **Compute & Orchestration**: Official GKE Autopilot (`gke_autopilot`), Cloud Run (`cloud_run`), and Compute Engine (`compute_engine`).
   - **Databases & Cache**: Official BigQuery (`bigquery`), Cloud Spanner (`spanner`), and Cloud Memorystore (`memorystore`).
   - **Security & Zero Trust**: Official Cloud Armor (`cloud_armor`), Identity-Aware Proxy (`iap`), Sensitive Data Protection / DLP (`cloud_dlp`), VPC Service Controls (`vpc_sc`), and Security Command Center (`scc`).
   - **Operations & CI/CD**: Official Cloud Logging (`cloud_logging`), Cloud Monitoring (`cloud_monitoring`), and Google Cloud Deploy (`cloud_deploy`).

---

## 🧭 Pillar 9: Client-Side Edge Router Override & Deterministic Waypoint Law

1. **Prohibition of `orthogonalEdgeStyle` with Manual Waypoints**:
   - When manual intermediate waypoints (`<Array as="points">`) are defined on an edge, **NEVER** use `edgeStyle=orthogonalEdgeStyle;`.
   - Draw.io's client-side JavaScript engine (`mxGraph` / `viewer-static.min.js`) treats `orthogonalEdgeStyle` as an automatic Manhattan auto-router that will discard explicit waypoints if it detects obstacles, auto-routing straight through child nodes or intermediate containers.
2. **Mandatory `edgeStyle=none;rounded=1;` for Deterministic Waypoints**:
   - Always enforce `edgeStyle=none;rounded=1;` whenever intermediate waypoints are specified.
   - This locks the path to strict point-to-point rectilinear segments with smooth rounded corners and prevents client-side algorithmic path deviation.

---

## 🏷️ Pillar 10: Edge Label AABB Safety Margins & Container Header Collision Prevention

1. **Header Clearance ($\ge 20\text{px}$)**:
   - All connector edge label pills (`<mxPoint as="offset"/>` or relative labels) MUST maintain a minimum vertical clearance of **$20\text{px}$** from all container headers (e.g., VPC networks, subnets, swimlanes, and edge ingress boxes).
   - Connector labels must NEVER hover directly over, intersect, or obscure container title text or CIDR annotations.
2. **Dedicated Corridor Waypoint Routing**:
   - Cross-container ingress lines (e.g. Ingress → Private VPC) must route through dedicated external corridors (e.g., a $25\text{px}$ open gap between the ingress box and VPC border) so that horizontal segments and label badges float in 100% open white space outside container title bars.

---

## 📏 Pillar 11: Inter-Card Clearance & Badge Channel Pitch Law ($\ge \text{Badge Width} + 20\text{px}$)

1. **Zero-Collision Channel Pitch**:
   - Sibling node spacing cannot be validated solely by bounding box non-overlap ($A_x + A_w \le B_x$).
   - If a connector between two adjacent cards carries a label badge, the horizontal or vertical gap between them MUST strictly accommodate the badge:
     $$\text{Channel Gap} = X_{\text{target}} - (X_{\text{source}} + W_{\text{source}}) \ge \text{Badge Width} + 20\text{px}$$
2. **Channel Width Minimums**:
   - Never place a $70\text{px}-100\text{px}$ wide label badge (such as `GPUDirect RDMA 3.2 Tbps` or `TLS 1.3 Handshake`) in a narrow $20\text{px}-25\text{px}$ gap. Expand card gaps to at least $40\text{px}-75\text{px}$ to guarantee collision-free visual margins.

---

## 🧪 Pillar 12: SVG DOM Coordinate & Bounding Box Inspection Mandate

1. **Prohibition of Text-Only DOM Assertions**:
   - E2E tests (Puppeteer / Playwright) MUST NOT declare a diagram or UI state verified based solely on `innerText.includes(...)` or screenshot generation.
2. **Physical SVG Inspection**:
   - Automated test scripts must inspect the rendered SVG DOM elements inside `#diagram-canvas-card iframe`:
     - Query rendered `<text>` and `<rect>` elements via `page.evaluate()` or `page.$$()`.
     - Call `getBoundingClientRect()` on edge label text elements and verify zero mathematical intersection with adjacent container headers or node cards.
     - Assert that line paths (`<path d="...">`) do not penetrate the inner bounding boxes of non-target child components.

---

## 🎯 Pillar 13: Anti-Static-Spoofing, Layout Archetype vs. Subject Domain Separation & Universal Dynamic Infographic Synthesis (`Rule 41`)

1. **Strict Separation of Layout Archetype vs. Subject Domain**:
   - Never confuse a **Visual Layout Archetype** (`Tiered Architectural Infographic`, `Infographic`, `Swimlane`, `Sequence Diagram`, `C4 Topology`) with a **Static Content Template** (`Charlie Hills / Context + Harness + Loop + Graph`, `NOVACURA Biopharma`).
   - When a user prompt requests a layout archetype for a **new or arbitrary subject topic** (e.g., `"Open Knowledge format Infographic"`, `"Healthcare FHIR Infographic"`, `"Zero-Trust Security Infographic"`, `"FinOps Cloud Cost Infographic"`), the prompt router and diagram generator MUST NEVER spoof or return a static template belonging to an unrelated subject domain (`Context + Harness + Loop + Graph` or `Charlie Hills`).
2. **Universal Dynamic Tiered Infographic Engine (`src/lib/canonical/dynamicTieredInfographic.ts`)**:
   - Any prompt containing `"infographic"` that is not an explicit named reference template MUST route to `generateDynamicTieredInfographicXml(prompt)`, which dynamically synthesizes a complete 16:9 4-Tier Architectural Infographic (`01 Ingestion` • `02 Harness` • `03 Validation` • `04 Graph` with numbered spine, dashed enclaves, decision gates, and bottom rule/prompt bars) customized 100% to the user's subject domain.
3. **Mandatory Semantic Subject Parity Audit**:
   - Before certifying any generated diagram, verify that the rendered canvas header title, tier subtitles, node labels, and footer pill explicitly contain the subject domain nouns from the user's prompt and contain **zero** leaked strings from unrelated templates (`Charlie Hills`, `CLAUDE.md`, `NOVACURA`).


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
