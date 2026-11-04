---
name: ui-first-design-system
description: Principal Design Systems Engineer & WCAG 2.2 AAA Accessibility Architect skill combining Anthropic's <frontend_aesthetics> anti-convergence principles (distinctive typography, cohesive CSS variable themes, atmospheric depth, purposeful staggered motion) with the 16-Pillar UX/UI & WCAG 2.2 AAA audit, remediation protocol, and automated Puppeteer contrast/DOM verification scripts.
---

# UI-First Design System, `<frontend_aesthetics>` & 16-Pillar WCAG 2.2 AAA Architect

This skill combines **anti-convergence frontend aesthetics** (inspired by Anthropic's *"Improving frontend design through Skills"* engineering guide) with a rigorous **16-Pillar UX/UI & WCAG 2.2 AAA Accessibility Audit and Remediation Protocol** and executable verification scripts (`scripts/verify_ui_ux_and_contrast.mjs`).

---

## 1. Defeating Distributional Convergence (`<frontend_aesthetics>`)

Without explicit steering, LLMs converge on the high-probability center of web training data: `Inter`/`Roboto` fonts, purple/indigo gradients on flat white backgrounds, timid evenly-distributed badge colors, and static unstyled grids ("AI slop"). Every frontend built or refactored with this skill MUST actively defeat distributional convergence across four concrete code axes:

```xml
<frontend_aesthetics>
Avoid generic, "on-distribution" AI-generated aesthetics. Build distinctive, high-craft frontends engineered for the specific domain and user workflow:

1. Typography (<use_interesting_fonts>):
   - Typography immediately signals craft. Avoid defaulting to plain Inter, Roboto, Open Sans, or system-ui for application chrome.
   - Select intentional, high-contrast font pairings loaded from Google Fonts:
     • Executive BI, Finance & Analytics: 'Plus Jakarta Sans' or 'IBM Plex Sans' (UI/headers) + 'Newsreader' or 'Fraunces' (editorial callouts) + 'JetBrains Mono' or 'IBM Plex Mono' (metrics, IDs, deltas).
     • Developer, Agentic & Cloud Studio: 'Bricolage Grotesque' or 'Space Grotesk' (display headers) + 'IBM Plex Sans' (body) + 'JetBrains Mono' / 'Fira Code' (code, tickets, logs).
     • Editorial, Research & Knowledge Portals: 'Fraunces' or 'Playfair Display' (display) + 'Source Sans 3' or 'Plus Jakarta Sans' (body) + 'JetBrains Mono' (citations).
     • 1:1 Native Cloud Document Canvas Exception: Keep 'Google Sans' / 'Arial' strictly inside 1:1 Google Docs/Sheets paper emulation sheets where literal cloud-editor fidelity is required.
   - Pairing & Scale Extremes: Use high weight contrast (300/400 body vs 700/800 headers) and decisive size hierarchy jumps (2.5x–3.5x between hero KPI counters and supporting labels).
   - Numeric Discipline: Always enforce `font-variant-numeric: tabular-nums;` on KPI counters, financial columns, percentages, dates, and sortable data tables.

2. Color & Theme Cohesion (CSS Custom Properties):
   - Commit to a cohesive palette defined via `:root` CSS custom properties (`--theme-bg-*`, `--theme-surface-*`, `--theme-text-*`, `--theme-border-*`, `--theme-accent-*`).
   - Dominant surface tones (e.g., deep obsidian `#090D16` / `#0F172A` shell + crisp alabaster `#F8FAFC` / `#FFFFFF` workspace) paired with sharp, intentional semantic accents outperform timid rainbow palettes or clichéd purple-on-white gradients.
   - Enforce mathematical contrast compliance:
     • Standard body text (<18px): >= 4.5:1 (WCAG AA) / >= 7.0:1 (WCAG AAA target: `#0F172A` primary, `#334155` secondary on light surfaces).
     • Semantic status pills: High-contrast text on tinted fills (Emerald `#065F46` on `#D1FAE5`, Amber `#9A3412` on `#FFEDD5`, Crimson `#991B1B` on `#FEE2E2`, Sapphire `#1E40AF` on `#DBEAFE`).
     • Never pair semantic meaning with color alone—always include a distinct icon, prefix symbol (`✓`, `⚠️`, `🔴`, `↗`), or text label.

3. Atmospheric Backgrounds & Surface Depth:
   - Never rely on flat, lifeless solid fills for hero headers or primary studio chrome.
   - Layer subtle CSS radial/mesh gradients (`radial-gradient(at 15% 20%, ...)`), fine geometric dot/grid matrices, crisp `1px solid` structural borders, and multi-stage elevation shadows.

4. Purposeful Motion & Tactile Micro-Interactions:
   - Prioritize one well-orchestrated page/view entrance with staggered card reveals (`animation: surfaceReveal 0.35s cubic-bezier(0.22, 1, 0.36, 1) both;` with `animation-delay`) over scattered, noisy animations.
   - Provide tactile physical feedback on all interactive controls: hover elevation, active press state (`transform: translateY(1px)`), and unmistakable `:focus-visible` rings (`outline: 2px solid var(--theme-focus-ring); outline-offset: 2px`).
   - Always include `@media (prefers-reduced-motion: reduce)` to disable non-essential animations and transitions for motion-sensitive users.
</frontend_aesthetics>
```

---

## 2. Strict Execution Rules & Anti-Laziness Protocol

1. **No Placeholders**: Never output `// ... rest of code unchanged`, `/* existing logic */`, or truncated snippets. Always implement complete, production-ready components and functions.
2. **Real Tokens & Native DOM APIs Only**: Never hallucinate uninstalled packages or non-existent utility classes. Rely on verified `:root` CSS variables, existing framework tokens, and standard Web APIs.
3. **Wired Reactive State**: Never hardcode static ARIA attributes (`aria-expanded="false"`, `aria-selected="true"`, `aria-sort="none"`) without wiring them to the actual reactive state hooks or DOM event handlers that mutate them.
4. **Full Desktop Viewport Utilization (`max-w-8xl` / `1600px`)**: Never trap desktop dashboards or studios inside narrow centered containers (`max-w-4xl` / `max-w-5xl`) that leave dead side gutters.

---

## 3. The 16-Pillar UX/UI & WCAG 2.2 AAA Audit Checklist

When auditing or building any frontend interface, evaluate and remediate across all 16 pillars:

| Pillar | Mandatory Engineering & Accessibility Requirements |
| :--- | :--- |
| **1. Visual Hierarchy, Layout & Spacing** | Clear F/Z-pattern scanning; 4px/8px spatial rhythm; card density capped at $\le 4$ distinct data points per card; zero horizontal overflow (`320px` to `2560px`); sticky table/column headers (`position: sticky; top: 0`). |
| **2. Typography & Scannability** | Distinctive font pairings; `font-variant-numeric: tabular-nums` on all numeric/KPI/table columns; `60ch–75ch` reading measure for prose; line-height `1.5+` for body and `1.15–1.25` for headings; minimum `12px` (`0.75rem`) for supporting labels. |
| **3. Color Theory, Contrast & Semantic Tokens** | WCAG 2.2 AA (`4.5:1` normal / `3:1` large & UI boundaries) and AAA (`7:1` body text target); non-color secondary indicators (icons/badges) on all status states; component-scoped dark shell + light workspace separation. |
| **4. Component States & Micro-Affordances** | All 8 interactive states implemented for every button/input/row/card: `default`, `hover`, `focus-visible` (`2px solid` high-contrast ring with `2px` offset), `active` (`translateY(1px)`), `disabled` (`opacity: 0.5; cursor: not-allowed`), `loading`, `error`, `selected`. |
| **5. Information Architecture & Wayfinding** | Persistent "Where am I?" indicators (`aria-current="page"` or `aria-current="step"`); semantic `<nav aria-label="...">` breadcrumbs with clickable `<button>` steps; URL query parameter synchronization (`history.replaceState` + `popstate`) for tabs, filters, and drill-downs. |
| **6. Cognitive Load & Progressive Disclosure** | Hick's Law & Miller's Law compliance; primary action clusters limited to $\le 5$ top-level items; `<5` visible options rendered as segmented pills (`role="radiogroup"`), $\ge 5$ options rendered as searchable popovers (`<input type="search">` type-ahead filter). |
| **7. Interaction Design & Task Efficiency** | Inline editing or slide-over drawers (`role="dialog"`) instead of full-page context switches; single-click copy with visual `✓ Copied` feedback; inline `✕` clear buttons on search/NLQ inputs; global keyboard shortcuts (`?` cheat sheet, `Cmd/Ctrl+K`, `Escape`). |
| **8. Forms, Inputs & Validation Ergonomics** | Explicit `<label for="...">` or `aria-label` on 100% of inputs/selects/textareas (placeholders are never labels); `font-size: 16px` on mobile (`@media (max-width: 768px)`) to prevent iOS Safari auto-zoom; programmatic `aria-invalid` + `aria-describedby` error messages. |
| **9. WCAG 2.2 AAA Accessibility & Keyboard** | Semantic landmarks (`<header>`, `<nav>`, `<main id="main-workspace" tabindex="-1">`, `<aside>`) + `.skip-to-main-link`; WAI-ARIA roving `tabindex` on `role="tablist"`, `role="menubar"`, and `role="radiogroup"`; full modal focus trapping (`Tab`/`Shift+Tab` loop, `Escape` dismissal, return focus to trigger); `role="status" aria-live="polite"` on toasts and dynamic banners; `<svg role="img" aria-label="...">` + `<title>`. |
| **10. Responsive & Touch/Pointer Ergonomics** | WCAG 2.2 Target Size (`2.5.5 AAA: 44×44px` on primary FABs/actions; `2.5.8 AA: >= 24×24px` / `28×28px` on dense toolbar buttons and swatches); responsive `min(..., calc(100vw - 24px))` widths on all modals, popovers, and drawers. |
| **11. Motion, Transitions & Reduced-Motion** | Purposeful spatial transitions (`150ms–300ms`); staggered entrance reveals; mandatory `@media (prefers-reduced-motion: reduce)` override setting animation/transition durations to `0.01ms`. |
| **12. Error Prevention, Recovery & Undo** | Destructive actions (delete row/column/table/template/account, reset canvas) must either provide an inline **`↶ Undo` toast callback** (`showToast(msg, undoFn)`) or a confirmation step; unsaved drawer/modal form edits must persist in session cache across accidental dismissal. |
| **13. Data-Dense UI, Tables, Charts & BI** | Interactive column sorting (`<button class="sort-btn">` inside `<th>` updating `aria-sort="ascending|descending|none"`); sticky headers; right-aligned or `tabular-nums` numbers; empty-filter state rows with a 1-click `"↺ Reset All Filters"` CTA; keyboard-operable chart bars and KPI cards (`role="button" tabindex="0"` + `Enter`/`Space`). |
| **14. Microcopy, Content Design & Tone** | Action-oriented button verbs (`"💾 Save Template"`, `"🚀 Create in Chrome"`, `"🔄 Push Updates to Report"` instead of vague `"Submit"`/`"OK"`); transparent provenance badges (`✓ Verified Actuals`, `🔮 Holt-Winters + CI`, `[Rubric: xx/100]`). |
| **15. Perceived Performance & Optimistic UI** | Immediate optimistic DOM updates on status/filter changes; layout stability (`min-height` reservations on chart containers to prevent CLS jumps). |
| **16. Design System & Token Governance** | Centralized `:root` CSS custom properties for surfaces, typography, borders, focus rings, and semantic status tokens; zero competing inline style overrides on stateful tabs or buttons. |

---

## 4. Two-Phase Audit & Remediation Workflow

When asked to run a comprehensive UI/UX & Accessibility Audit on any project:

1. **Phase 1 — Exhaustive Findings Registry**:
   - Inspect all UI routes/components and run `node <skill_dir>/scripts/verify_ui_ux_and_contrast.mjs <url>`.
   - Catalog every defect with a unique ID (`[UX-001]`, `[UX-002]`, ...), Severity (`P1-Critical`, `P2-Major`, `P3-Minor`), Pillar (`1`–`16`), File & Line Numbers, Current Broken Pattern, and Concrete Fix Specification.
2. **Phase 2 — Production Code Remediation & Visual Verification**:
   - Implement 100% of cataloged fixes directly in the source files with zero placeholders.
   - Re-run the project build and `verify_ui_ux_and_contrast.mjs` to confirm **zero contrast violations**, **zero unlabeled controls**, **100% keyboard/ARIA compliance**, and capture Before & After Retina screenshots (`1600×980 @ 2x`).

---

## 5. 3-Level Deep Forensic Slide Studio, Fullscreen Theater Zero-Overlap & Google Slides–Style Docked `🎛️ Customize` Side Panel Mandate (`Rule 55`)

1. **Zero PiP Footer Clipping & Zero Slide Occlusion (`0 px²`)**:
   - `.pip-footer-controls` must maintain `scrollWidth <= clientWidth` (`0px` horizontal clipping across all 5 controls), and `#aiPresenterVideoPip` must dock in a dedicated `264px` gutter (`0 px²` overlap with `#slide-img`) across Normal Mode, Edit Mode (`body.slide-edit-mode-active`), Customize Mode (`body.customize-panel-open`), and Fullscreen Theater Mode (`body.google-slides-theater`).
2. **Aspect-Ratio Locked `.visual-frame` (`3420 / 1810`) & Modal-First `Escape` Precedence**:
   - Lock `.visual-frame` to `aspect-ratio: 3420 / 1810` so `%`-positioned `#slideObjectsLayer` wireframes align `1:1` with the rendered image rect in both Normal and Fullscreen Theater modes, and ensure `executeEscapeAction()` dismisses open modals/grid views before exiting `google-slides-theater`.
3. **Google Slides–Style Docked Right-Hand `🎛️ Customize` Side Panel & Collapsible Accordion Headers**:
   - Keep `.presenter-topbar` clean and uncluttered (`🔊 Narrate`, `⛶ Fullscreen`, `◧ Notes`, **`🎛️ Customize`** `#btnToggleCustomizePanel`, and `📤 Share / Export ▾`, with `#voiceSettingsRibbon` hidden), organize all individual presentation controls inside the docked right-hand `345px` `#slidesCustomizeSidePanel` under **6 Collapsible Accordion Headers (`<details class="gslides-customize-accordion">`)**, organize `#slideEditStudioPanel` under **4 Collapsible Accordion Headers**, and organize `#leftSlideNarrativeCard` under **2 Collapsible Accordion Headers** with `0 px²` overlap over `#slide-img`.

---

## 6. 20-Level Deep Forensic Portal, Zero-Broken-Screenshot & 100% WCAG Input-Labeling Mandate (`Rule 60`)

1. **100% On-Disk Screenshot & Thumbnail Verification (`L20-01`..`L20-04`)**:
   - Every `/screenshots/...` image path referenced in `codelab-view.html`, `live-demo-narrator.html`, `create-new-demo.html`, and `liveGoogleExecutor.mjs` must exist on disk with zero `404` responses, and filmstrip thumbnails in `cloud-preview.html` must load eagerly (`0` `loading="lazy"` attributes inside overflow containers).
2. **100% Programmatic `aria-label` Coverage & Unclipped Responsive Controls (`L20-11`, `L20-12`, `L20-22`..`L20-24`)**:
   - Every non-hidden `<input>`, `<select>`, and `<textarea>` across all portal views and server templates must carry an explicit `aria-label`, all catalog cards must render aligned 4-button `.demo-actions` footers (`.demo-card-footer { margin-top: auto }`), `#btnVerifyGeMcpConnection` must remain unclipped inside `.top-shell`, and `/demo-generator` must collapse multi-column grids below `1100px`/`640px` with `0px` horizontal overflow at `390×844`.



## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).

## 7. Multi-Persona Studio & Anti-Monolith Architecture Mandate (`v3.0`)
- **Zero Vertical-Monolith & Zero Spec-Dump Clutter (`Rule 25`)**: Never stack 4–5 distinct operational workflows into a single 5,000px vertical page or print internal schema/compliance debug codes (`S_iso = ...`, `BIO_LINK_NO_RAW_URLS`) onto primary human surfaces. Segment workflows via dedicated top-level views + sub-navigation tabs (`Today's Top 5` | `Publishing Queue` | `Batch & Signal Radar`).
- **3-Persona Experience Switcher (`Creator` · `Executive` · `Builder`)**: Serve distinct user archetypes via progressive disclosure (`Creator`: visual 5-blueprint thumbnail strip + native social/device preview; `Executive`: 4-card Morning KPI & Queue Review strip; `Builder`: 4-card Engineering & Pipeline strip + `.drawio`/`.pptx`/`SVG` vector chips + live JSON API payload preview), paired with a `⌘K` Command Palette, Full-Resolution Lightbox, `0` `innerHTML`/`localStorage`/`sessionStorage`, and `22/22` Puppeteer E2E + 16-Pillar WCAG 2.2 AA/AAA contrast/landmark/mobile-`390×844` gates.
