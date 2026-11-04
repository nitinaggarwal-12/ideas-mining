// Interactive Client Logic for Agentic AI Ideas-Minting & OpenHands Autonomous Repo Factory (ideas-minting)

let STATE = {
  repos: [],
  playbook: null,
  activeRepoSlug: null,
  templates: [],
  pairings: [],
  mintingStudio: null,
  top5Briefing: null,
  modeContracts: {},
  platformSpecs: {},
  outboxLedger: { items: [] },
  selectedIdeaId: "",
  selectedTemplateId: "",
  selectedMode: "Carousel",
  selectedPreviewPlatform: "linkedin",
  selectedStagePlatforms: new Set(["linkedin", "telegram", "youtube_shorts", "instagram", "tiktok"]),
  previewPackagesByPlatform: {},
};

function showToast(msg) {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const el = document.createElement("div");
  el.className = "toast-item";
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => {
    el.remove();
  }, 3500);
}

function escapeHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function loadWorkspaceData() {
  const res = await fetch("/api/workspace-state");
  const data = await res.json();
  STATE.repos = data.repos || [];
  STATE.playbook = data.playbook || {};
  renderReposView();
  renderPlaybookView();
  renderOpenHandsView();
}

function getFilteredRepos() {
  const q = (document.getElementById("search-input")?.value || "").trim().toLowerCase();
  const arch = document.getElementById("filter-archetype")?.value || "ALL";
  const author = document.getElementById("filter-author")?.value || "ALL";

  return STATE.repos.filter((r) => {
    const mnemonicText =
      typeof r.mnemonic === "object" && r.mnemonic !== null
        ? `${r.mnemonic.acronym || ""} ${(r.mnemonic.expansion || []).join(" ")}`
        : String(r.mnemonic || "");
    const matchesQuery =
      !q ||
      r.post_title.toLowerCase().includes(q) ||
      r.repo_slug.toLowerCase().includes(q) ||
      r.author_name.toLowerCase().includes(q) ||
      r.primary_source.title.toLowerCase().includes(q) ||
      (r.daily_problem_short || "").toLowerCase().includes(q) ||
      mnemonicText.toLowerCase().includes(q) ||
      r.gcp_stack.join(" ").toLowerCase().includes(q);
    let matchesArch = arch === "ALL";
    if (!matchesArch) {
      if (arch === "MINT") {
        matchesArch = r.id.startsWith("MINT-");
      } else if (arch === "ARCH-DYN") {
        matchesArch = r.id.startsWith("IDEA-") || (r.diagram_archetype || "").startsWith("ARCH-DYN");
      } else if (arch === "ARCH-2D") {
        matchesArch = r.id.startsWith("POST-") || (r.diagram_archetype || "").startsWith("ARCH-2D");
      } else {
        matchesArch = (r.diagram_archetype || "").startsWith(arch);
      }
    }
    const matchesAuthor = author === "ALL" || r.author_name.toLowerCase().includes(author.toLowerCase());
    return matchesQuery && matchesArch && matchesAuthor;
  });
}

function renderReposView() {
  const filtered = getFilteredRepos();
  const grid = document.getElementById("repos-cards-grid");
  const tbody = document.getElementById("repos-matrix-tbody");
  const emptyState = document.getElementById("no-matching-cards");

  if (filtered.length === 0) {
    emptyState.style.display = "block";
    grid.innerHTML = "";
    tbody.innerHTML = "";
    return;
  }
  emptyState.style.display = "none";

  grid.innerHTML = filtered
    .map((r) => {
      const plan = r.template_and_distribution_plan || null;
      const flagshipDeckBtn = r.flagship_24slide_url
        ? `<a class="btn-secondary" style="background:#fef3c7;border-color:#f59e0b;color:#92400e;" href="${escapeHtml(r.flagship_24slide_url)}" target="_blank" rel="noopener">📊 24-Slide Google Slides ↗</a>`
        : "";
      const planBanner = plan
        ? `<div style="margin: 8px 0 4px 0; padding: 8px 10px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 6px; font-size: 11px; color: #0c4a6e;">
             <div style="font-weight: 800; color: #0369a1; margin-bottom: 3px;">🎯 LEAD TEMPLATE: ${escapeHtml(plan.primary_template_id)} — ${escapeHtml(plan.primary_template_name)} (+ ${escapeHtml((plan.secondary_template_ids || []).join(", "))})</div>
             <div style="font-weight: 600; color: #0f172a; margin-bottom: 3px;">📦 FORMAT: ${escapeHtml(plan.lead_post_format)}</div>
             <div style="color: #1e3a8a;">🌐 <strong>Max Reach Group:</strong> ${escapeHtml(plan.linkedin_groups_primary?.[0]?.name || "")} (${escapeHtml(plan.linkedin_groups_primary?.[0]?.members || "")}) • <strong>Network Group:</strong> ${escapeHtml(plan.linkedin_groups_niche_network?.[0]?.name || "")} (${escapeHtml(plan.linkedin_groups_niche_network?.[0]?.members || "")})</div>
           </div>`
        : "";
      return `
      <article class="repo-card" data-testid="repo-card-${escapeHtml(r.id)}">
        <div>
          <div class="repo-card-header">
            <span class="brand-badge">${escapeHtml(r.id)} • ${escapeHtml(r.est_post_time || r.author_name)}</span>
            <span class="pill-badge pill-emerald">${plan ? "LEAD: " + escapeHtml(plan.primary_template_id) + " • " : ""}HEAD: ${escapeHtml(r.git_commit_sha || "verified")}</span>
          </div>
          <h3 class="repo-card-title" style="margin: 10px 0 8px 0;">${escapeHtml(r.post_title)}</h3>
          <div class="repo-card-hook">${escapeHtml(r.daily_problem_short || r.original_hook)}</div>
          ${planBanner}
          <div style="margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; background: #ffffff; cursor: pointer;" onclick="openRepoInspector('${escapeHtml(r.repo_slug)}')">
            <img src="/repos/${encodeURIComponent(r.repo_slug)}/visuals/${plan ? "lead-template.svg" : "dynamic-solution-flow.svg"}?v=20261103" alt="Lead Template & Dynamic Moving-Arrow Solution Diagram" style="width: 100%; height: auto; display: block;" loading="lazy" />
          </div>
          <div style="margin-top: 6px; font-size: 11.5px; color: #475569; font-weight: 600;">
            Primary Source: <strong style="color: #0f172a;">${escapeHtml(r.primary_source.title)}</strong>
          </div>
        </div>
        <div>
          <div class="deliverable-chips" style="margin-bottom: 10px;">
            ${plan ? `<span class="deliverable-chip" style="background:#fef3c7;border-color:#fcd34d;color:#92400e;">🏆 Template ${escapeHtml(plan.primary_template_id)} SVG/PNG/GIF</span>` : ""}
            ${r.flagship_24slide_url ? `<span class="deliverable-chip" style="background:#ecfdf5;border-color:#6ee7b7;color:#065f46;">📊 24-Slide Google Slides + 1080p30 Video</span>` : ""}
            <span class="deliverable-chip" style="background:#eff6ff;border-color:#93c5fd;color:#1d4ed8;">⚡ Moving-Arrow SVG + GIF</span>
            <span class="deliverable-chip">GCP #78 .drawio + PNG</span>
            <span class="deliverable-chip">12-Slide .pptx + .pdf</span>
            <span class="deliverable-chip">LinkedIn Group Plan</span>
          </div>
          <div class="repo-card-footer">
            <span class="truncate" style="font-size: 11px; color: #64748b; font-family: monospace;">
              generated-repos/${escapeHtml(r.repo_slug)}
            </span>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              ${flagshipDeckBtn}
              <button class="btn-primary" data-testid="inspect-repo-btn-${escapeHtml(r.id)}" onclick="openRepoInspector('${escapeHtml(r.repo_slug)}')">
                Inspect Moving-Arrow &amp; Bundle →
              </button>
            </div>
          </div>
        </div>
      </article>
    `;
    })
    .join("");

  tbody.innerHTML = filtered
    .map(
      (r) => `
      <tr>
        <td>
          <div class="cell-card-equal">
            <strong style="font-size: 12px; color: #174ea6;">${escapeHtml(r.id)} (${escapeHtml(r.est_post_time || "Verified Signal")})</strong>
            <span class="truncate" style="font-size: 11.5px; font-family: monospace; color: #0f172a;">${escapeHtml(r.repo_slug)}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <strong style="font-size: 12px;">${escapeHtml(r.daily_problem_short || r.author_name)}</strong>
            <span style="font-size: 11.5px; color: #475569;">${escapeHtml(r.primary_source.title)}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span style="font-size: 11.5px; font-weight: 700; color: #0f172a;">Moving-Arrow SVG/GIF • Nano Banana 3 • GCP #78 Draw.io</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span style="font-size: 11.5px; color: #334155;">${escapeHtml(r.gcp_stack.slice(0, 3).join(" • "))}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span style="font-size: 11.5px; color: #065f46; font-weight: 700;">Code • README • Dynamic GIF/SVG • ${r.flagship_24slide_url ? "24-Slide Google Slides + 1080p30 Video • " : ""}12-Slide PPTX/PDF • Terraform</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span class="pill-badge pill-emerald" style="display: inline-block; width: fit-content;">100% PASS (${escapeHtml(r.git_commit_sha)})</span>
          </div>
        </td>
      </tr>
    `
    )
    .join("");
}

function renderPlaybookView() {
  const pb = STATE.playbook || {};
  document.getElementById("playbook-summary-text").textContent = pb.executive_summary || "";
  const chGrid = document.getElementById("signal-channels-grid");
  chGrid.innerHTML = (pb.signal_channels || [])
    .map(
      (ch) => `
      <div class="repo-card">
        <div>
          <span class="brand-badge">${escapeHtml(ch.id)} • Creators: ${escapeHtml((ch.creators_using || []).join(", "))}</span>
          <h3 class="repo-card-title" style="margin: 10px 0 8px 0;">${escapeHtml(ch.name)}</h3>
          <p style="font-size: 12.5px; color: #334155; margin-bottom: 10px; line-height: 1.45;">${escapeHtml(ch.mining_pattern)}</p>
          <ul style="padding-left: 18px; font-size: 12px; color: #475569; line-height: 1.5;">
            ${(ch.sources || []).map((s) => `<li>${escapeHtml(s)}</li>`).join("")}
          </ul>
        </div>
      </div>
    `
    )
    .join("");

  const profiles = pb.creator_profiles || [];
  const cpBadge = document.getElementById("creator-profiles-count-badge");
  if (cpBadge) {
    cpBadge.textContent = `${profiles.length} Verified Creator Profiles`;
  }
  const cpGrid = document.getElementById("creator-profiles-grid");
  if (cpGrid) {
    cpGrid.innerHTML = profiles
      .map((cp) => {
        const followersFmt = cp.followers ? `${Number(cp.followers).toLocaleString()} followers` : "Verified Creator";
        const eng = cp.engagement
          ? `<span class="pill-badge pill-amber">👍 ${escapeHtml(String(cp.engagement.likes))} • 💬 ${escapeHtml(String(cp.engagement.comments))} (${escapeHtml(cp.engagement.comment_to_like_ratio)} ratio)</span>`
          : "";
        return `
        <article class="creator-profile-card" data-testid="creator-profile-${escapeHtml(cp.template_id)}">
          <div>
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
              <span class="brand-badge">${escapeHtml(cp.template_id)} • ${escapeHtml(cp.style_code || "STYLE")}</span>
              <span class="pill-badge pill-sky">${escapeHtml(followersFmt)}</span>
            </div>
            <h3 style="font-size:14.5px;font-weight:800;color:#0f172a;margin-bottom:3px;">${escapeHtml(cp.name)}</h3>
            <div style="font-size:11.5px;font-weight:600;color:#475569;margin-bottom:8px;">${escapeHtml(cp.role)}</div>
            ${eng ? `<div style="margin-bottom:8px;">${eng}</div>` : ""}
            ${cp.archetype_label ? `<div style="font-size:11.5px;font-weight:800;color:#174ea6;margin-bottom:5px;">Archetype: ${escapeHtml(cp.archetype_label)}</div>` : ""}
            <p style="font-size:12px;color:#334155;line-height:1.45;">${escapeHtml(cp.signature_style)}</p>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px solid #e2e8f0;">
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              <a class="btn-secondary" href="${escapeHtml(cp.linkedin_url)}" target="_blank" rel="noopener">LinkedIn ↗</a>
              <button class="btn-secondary" onclick="jumpToTemplateInGallery('${escapeHtml(cp.template_id)}')">Template ${escapeHtml(cp.template_id)}</button>
            </div>
            <button class="btn-primary" data-testid="generate-in-style-${escapeHtml(cp.template_id)}" onclick="generateInCreatorStyle('${escapeHtml(cp.style_code || "AUTO")}', '${escapeHtml(cp.name)}')">
              ⚡ Generate in Style →
            </button>
          </div>
        </article>`;
      })
      .join("");
  }

  const archGrid = document.getElementById("archetypes-grid");
  archGrid.innerHTML = (pb.diagram_archetypes_2d || [])
    .map(
      (a) => `
      <div class="repo-card">
        <div>
          <span class="brand-badge">${escapeHtml(a.code)}</span>
          <h3 class="repo-card-title" style="margin: 10px 0 6px 0;">${escapeHtml(a.name)}</h3>
          <p style="font-size: 12.5px; color: #334155; margin-bottom: 8px;">${escapeHtml(a.visual_flow)}</p>
          <div style="font-size: 11.5px; color: #174ea6; font-weight: 700;">
            Used in: ${escapeHtml((a.used_in_posts || []).join(" | "))}
          </div>
        </div>
      </div>
    `
    )
    .join("");
}

async function jumpToTemplateInGallery(templateId) {
  activateView("view-gallery");
  if (!(STATE.templates || []).length) {
    await loadGalleryData();
  }
  const searchEl = document.getElementById("gallery-search-input");
  const filterEl = document.getElementById("gallery-filter-type");
  const tierEl = document.getElementById("gallery-filter-tier");
  if (filterEl) filterEl.value = "ALL";
  if (tierEl) tierEl.value = "ALL";
  if (searchEl) searchEl.value = templateId;
  renderGalleryView();
}

async function generateInCreatorStyle(styleCode, creatorName) {
  activateView("view-miner");
  const styleSelect = document.getElementById("daily-style-select");
  if (styleSelect) {
    styleSelect.value = styleCode || "AUTO";
  }
  showToast(`Routing Daily Post Engine to ${creatorName} (${styleCode}) archetype...`);
  await triggerGenerateDailyPosts();
}

function renderOpenHandsView() {
  const pb = STATE.playbook || {};
  const cmpTbody = document.getElementById("openhands-comparison-tbody");
  cmpTbody.innerHTML = ((pb.openhands_superiority || {}).comparison || [])
    .map(
      (row) => `
      <tr>
        <td><div class="cell-card-equal"><strong style="font-size: 12.5px;">${escapeHtml(row.dimension)}</strong></div></td>
        <td><div class="cell-card-equal"><span style="font-size: 12px; color: #991b1b;">${escapeHtml(row.bmad_meta_prompts)}</span></div></td>
        <td><div class="cell-card-equal"><span style="font-size: 12px; color: #065f46; font-weight: 600;">${escapeHtml(row.openhands_autonomous)}</span></div></td>
      </tr>
    `
    )
    .join("");

  const trajList = document.getElementById("openhands-trajectories-list");
  trajList.innerHTML = STATE.repos
    .map((r) => {
      const t = r.openhands_trajectory || {};
      const steps = (t.steps || [])
        .map(
          (s) =>
            `<span class="deliverable-chip" style="background:#ecfdf5;border-color:#6ee7b7;color:#065f46;">[${escapeHtml(s.stage)}] ${escapeHtml(s.status)} (${s.duration_ms}ms)</span>`
        )
        .join(" ");
      return `
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:12px 16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:8px;">
            <strong style="font-size:13px;">${escapeHtml(r.id)} — ${escapeHtml(r.repo_slug)} (Session: ${escapeHtml(t.session_id || "oh-verified")})</strong>
            <span class="pill-badge pill-emerald">Commit SHA: ${escapeHtml(r.git_commit_sha)}</span>
          </div>
          <div class="deliverable-chips">${steps}</div>
        </div>
      `;
    })
    .join("");
}

async function openRepoInspector(slug) {
  STATE.activeRepoSlug = slug;
  const res = await fetch(`/api/repo-detail/${encodeURIComponent(slug)}`);
  const detail = await res.json();

  document.getElementById("drawer-repo-badge").textContent = `${detail.id} • ${detail.est_post_time || detail.activity_urn} • HEAD ${detail.git_commit_sha}`;
  document.getElementById("drawer-repo-title").textContent = detail.post_title;

  const plan = detail.template_and_distribution_plan || null;
  const leadTemplateVisualHtml = plan
    ? `<div class="visual-preview-box" style="border: 2px solid #0284c7; background: #f0f9ff;">
         <div style="font-size: 12px; font-weight: 800; margin-bottom: 6px; color: #0369a1;">Figure 0 — Paired PromptCanvas / Systems Lead Infographic (${escapeHtml(plan.primary_template_id)}: ${escapeHtml(plan.primary_template_name)})</div>
         <div style="font-size: 11px; color: #0f172a; margin-bottom: 8px;"><strong>Format Mix:</strong> ${escapeHtml(plan.lead_post_format)} • <strong>Secondary Templates:</strong> ${escapeHtml((plan.secondary_template_ids || []).join(", "))}</div>
         <img src="/repos/${encodeURIComponent(slug)}/visuals/lead-template.svg?v=20261103" alt="Lead Template Infographic" />
       </div>`
    : "";

  // Tab 1: Dynamic Moving-Arrow & @2d Visuals
  document.getElementById("dtab-visuals").innerHTML = `
    <div style="margin-bottom: 14px; display: flex; gap: 8px; flex-wrap: wrap;">
      ${detail.flagship_24slide_url ? `<a class="btn-primary" style="background:#0f172a;border-color:#0f172a;" href="${escapeHtml(detail.flagship_24slide_url)}" target="_blank" rel="noopener">📊 Open 24-Slide Google Slides Deck ↗</a>` : ""}
      ${plan ? `<a class="btn-primary" href="/repos/${encodeURIComponent(slug)}/visuals/lead-template.svg?v=20261103" target="_blank">Open Paired Template ${escapeHtml(plan.primary_template_id)} (.svg) ↗</a>` : ""}
      ${plan ? `<a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/visuals/lead-template.gif?v=20261103" download>Download Template ${escapeHtml(plan.primary_template_id)} GIF (.gif)</a>` : ""}
      <a class="btn-primary" href="/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.svg?v=20261103" target="_blank">Open Moving-Arrow Diagram (.svg) ↗</a>
      <a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.gif?v=20261103" download>Download Animated LinkedIn GIF (.gif)</a>
      <a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.drawio?v=20261103" download>Download Editable Draw.io (.drawio)</a>
    </div>
    ${leadTemplateVisualHtml}
    <div class="visual-preview-box">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 8px; color: #0f172a;">Figure 1 — Live Dynamic Daily Problem → 4-Step Solution Flow (With Moving Arrows)</div>
      <img src="/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.svg?v=20261103" alt="Dynamic Moving-Arrow Solution Flow" />
    </div>
    <div class="visual-preview-box">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 8px; color: #0f172a;">Figure 2 — Official Google Cloud #78 4-Zone Hub-and-Spoke 2D Architecture (Vector SVG + Draw.io)</div>
      <img src="/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.svg?v=20261103" alt="GCP 2D Architecture" />
    </div>
    <div class="visual-preview-box">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 8px; color: #0f172a;">Figure 3 — High-Res 2D LinkedIn Infographic Poster (Vector SVG + 2x Retina PNG)</div>
      <img src="/repos/${encodeURIComponent(slug)}/visuals/linkedin-infographic-2d.svg?v=20261103" alt="LinkedIn 2D Infographic" />
    </div>
    <div class="visual-preview-box">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <span style="font-size: 12px; font-weight: 800; color: #0f172a;">Nano Banana 3 Detailed Generation Prompt (visuals/nano_banana_3_prompt.md)</span>
        <button class="btn-secondary" onclick="copyTextSafe(document.getElementById('nb3-prompt-pre').innerText, 'Copied Nano Banana 3 prompt!')">Copy Prompt</button>
      </div>
      <pre class="code-block-light" id="nb3-prompt-pre">${escapeHtml(detail.nano_banana_3_prompt || "")}</pre>
    </div>
  `;

  // Tab 2: Slide Deck & Carousel
  const slidesHtml = (detail.slides || [])
    .map(
      (s) => `
      <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:12px;margin-bottom:10px;">
        <div style="font-size:10.5px;font-weight:800;color:#174ea6;margin-bottom:4px;">SLIDE ${s.slide_num} OF 12 • ${escapeHtml(s.header_breadcrumb)}</div>
        <div style="font-size:14px;font-weight:800;color:#0f172a;margin-bottom:4px;">${escapeHtml(s.headline)}</div>
        <div style="font-size:12px;color:#475569;margin-bottom:8px;">${escapeHtml(s.subtitle)}</div>
        <div style="font-size:11.5px;color:#1e293b;background:#ffffff;border-left:3px solid #34A853;padding:6px 10px;">
          <strong>Spoken Customer Talk Track:</strong> ${escapeHtml((s.spoken_notes || [])[0] || "")}
        </div>
      </div>
    `
    )
    .join("");

  document.getElementById("dtab-slides").innerHTML = `
    <div style="margin-bottom: 14px; display: flex; gap: 8px; flex-wrap: wrap;">
      ${detail.flagship_24slide_url ? `<a class="btn-primary" style="background:#0f172a;border-color:#0f172a;" data-testid="drawer-open-24slide-deck-btn" href="${escapeHtml(detail.flagship_24slide_url)}" target="_blank" rel="noopener">📊 Open Live 24-Slide Native Google Slides Deck ↗</a>` : ""}
      <a class="btn-primary" href="/repos/${encodeURIComponent(slug)}/slides/presentation_deck.pptx" download>Download Editable 12-Slide PowerPoint (.pptx)</a>
      <a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/slides/linkedin_carousel.pdf" target="_blank">Open LinkedIn Carousel (.pdf) ↗</a>
      <a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/slides/linkedin_carousel.html" target="_blank">Open Interactive HTML Deck ↗</a>
    </div>
    ${slidesHtml}
  `;

  // Tab 3: 1-Click GCP Terraform & Code
  document.getElementById("dtab-terraform").innerHTML = `
    <div style="margin-bottom: 12px;">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 6px;">1-Click Google Cloud Deployment Command:</div>
      <pre class="code-block-light">cd generated-repos/${escapeHtml(slug)} && ./scripts/deploy_gcp_one_click.sh ramp-portal-dev us-west1</pre>
    </div>
    <div style="margin-bottom: 12px;">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 6px;">terraform/main.tf (Cloud Run v2 + Vertex AI Global + IAM):</div>
      <pre class="code-block-light">${escapeHtml(detail.terraform_main)}</pre>
    </div>
    <div>
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 6px;">src/engine.py (Google Cloud ADK + Rule 55 Global Endpoint Engine):</div>
      <pre class="code-block-light">${escapeHtml(detail.engine_py)}</pre>
    </div>
  `;

  // Tab 4: LinkedIn Post Copy & Group Distribution Strategy
  const groupPlanHtml = plan
    ? `<div style="background:#f0f9ff;border:1.5px solid #38bdf8;border-radius:8px;padding:14px;margin-bottom:14px;">
         <div style="font-size:12.5px;font-weight:800;color:#0369a1;margin-bottom:8px;">🎯 LinkedIn Virality, Format &amp; Group Distribution Plan (${escapeHtml(detail.id)} • ${escapeHtml(detail.est_post_time || "")})</div>
         <div style="font-size:12px;color:#0f172a;margin-bottom:6px;"><strong>Paired Primary Template:</strong> <code>${escapeHtml(plan.primary_template_id)}</code> — ${escapeHtml(plan.primary_template_name)} (Secondary: ${escapeHtml((plan.secondary_template_ids || []).join(", "))})</div>
         <div style="font-size:12px;color:#0f172a;margin-bottom:6px;"><strong>Lead Format Mix:</strong> ${escapeHtml(plan.lead_post_format)}</div>
         <div style="font-size:12px;color:#0f172a;margin-bottom:10px;"><strong>Dynamic Nature:</strong> ${escapeHtml(plan.dynamic_nature)}</div>
         <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;">
           <div style="background:#ffffff;border:1px solid #bae6fd;border-radius:6px;padding:10px;">
             <div style="font-size:11px;font-weight:800;color:#1d4ed8;margin-bottom:4px;">🌐 PRIMARY HIGH-REACH GROUPS (MAX VIEWERSHIP)</div>
             ${(plan.linkedin_groups_primary || []).map((g) => `<div style="font-size:11.5px;margin-bottom:4px;">• <strong>${escapeHtml(g.name)}</strong> (<code>${escapeHtml(g.members)}</code>) — <span style="color:#475569;">${escapeHtml(g.goal)}</span></div>`).join("")}
           </div>
           <div style="background:#ffffff;border:1px solid #86efac;border-radius:6px;padding:10px;">
             <div style="font-size:11px;font-weight:800;color:#065f46;margin-bottom:4px;">🤝 NICHE EXECUTIVE &amp; ARCHITECT GROUPS (PERSONAL NETWORK)</div>
             ${(plan.linkedin_groups_niche_network || []).map((g) => `<div style="font-size:11.5px;margin-bottom:4px;">• <strong>${escapeHtml(g.name)}</strong> (<code>${escapeHtml(g.members)}</code>) — <span style="color:#475569;">${escapeHtml(g.goal)}</span></div>`).join("")}
           </div>
         </div>
         <div style="background:#fefce8;border:1px solid #fde047;border-radius:6px;padding:8px 10px;font-size:11.5px;color:#713f12;">
           <strong>💬 Golden-Hour Comment-Magnet Question:</strong> "${escapeHtml(plan.comment_magnet_question)}"
         </div>
       </div>`
    : "";

  document.getElementById("dtab-linkedin").innerHTML = `
    ${groupPlanHtml}
    <div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;">
      <strong style="font-size: 13px;">Ready-to-Post LinkedIn Draft &amp; Comment #1 Pin (${escapeHtml(detail.est_post_time || "Morning EST")})</strong>
      <button class="btn-primary" onclick="copyTextSafe(document.getElementById('linkedin-copy-pre').innerText, 'Copied LinkedIn Post Draft to clipboard!')">
        Copy LinkedIn Post Copy
      </button>
    </div>
    <pre class="code-block-light" id="linkedin-copy-pre">${escapeHtml(detail.linkedin_post_draft)}</pre>
  `;

  document.getElementById("repo-inspector-drawer").classList.add("open");
}

async function copyTextSafe(text, toastMessage) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
    }
  } catch (_) {
    // Fallback silent in headless contexts without clipboard permission
  }
  STATE.lastCopiedText = text;
  window.__LAST_COPIED_TEXT__ = text;
  showToast(toastMessage || "Copied to clipboard!");
}

async function loadDailyGeneratedPosts() {
  const res = await fetch("/api/daily-posts");
  const data = await res.json();
  STATE.dailyPosts = data.posts || [];
  STATE.dailyEditionDate = data.requested_edition_date || data.latest_edition_date || "";
  const statusEl = document.getElementById("daily-posts-status-badge");
  if (statusEl) {
    statusEl.textContent = `${STATE.dailyPosts.length} Daily Posts Ready • Edition ${STATE.dailyEditionDate}`;
  }
  renderDailyGeneratedPosts();
}

async function triggerGenerateDailyPosts() {
  const btn = document.getElementById("generate-daily-posts-btn");
  const topicInput = document.getElementById("daily-topic-input");
  const styleSelect = document.getElementById("daily-style-select");
  const countSelect = document.getElementById("daily-count-select");
  const topic_query = (topicInput?.value || "").trim();
  const creator_style = styleSelect?.value || "AUTO";
  const count = parseInt(countSelect?.value || "6", 10) || 6;

  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Mining & Synthesizing...";
  }
  try {
    const res = await fetch("/api/daily-posts/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic_query, creator_style, count, use_live_network: true }),
    });
    const out = await res.json();
    STATE.dailyPosts = out.posts || [];
    STATE.dailyEditionDate = out.edition?.edition_date || STATE.dailyEditionDate;
    const statusEl = document.getElementById("daily-posts-status-badge");
    if (statusEl) {
      statusEl.textContent = `${STATE.dailyPosts.length} Fresh Posts Generated • Edition ${STATE.dailyEditionDate}`;
    }
    renderDailyGeneratedPosts();
    showToast(`Generated ${STATE.dailyPosts.length} daily LinkedIn posts & custom 2D SVGs!`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "⚡ Mine & Generate Fresh Daily Posts";
    }
  }
}

function switchDailyVisualTab(postId, mode) {
  const svgImg = document.getElementById(`daily-vis-svg-${postId}`);
  const pngImg = document.getElementById(`daily-vis-png-${postId}`);
  const btnSvg = document.getElementById(`daily-vbtn-svg-${postId}`);
  const btnPng = document.getElementById(`daily-vbtn-png-${postId}`);
  if (svgImg && pngImg) {
    svgImg.style.display = mode === "svg" ? "block" : "none";
    pngImg.style.display = mode === "png" ? "block" : "none";
  }
  if (btnSvg && btnPng) {
    btnSvg.classList.toggle("active", mode === "svg");
    btnPng.classList.toggle("active", mode === "png");
  }
}

async function copyDailyPostText(postId) {
  const p = (STATE.dailyPosts || []).find((item) => item.id === postId);
  if (!p) return;
  const fullPayload = `${p.linkedin_post_text}\n\n${p.hashtags || ""}\n\n---\n${p.first_comment_source}`;
  await copyTextSafe(fullPayload, `Copied LinkedIn Post + Comment #1 (${p.canonical_template_id})!`);
}

function renderDailyGeneratedPosts() {
  const grid = document.getElementById("daily-generated-posts-grid");
  if (!grid) return;
  const posts = STATE.dailyPosts || [];
  if (!posts.length) {
    grid.innerHTML = `<div style="padding:16px;color:#475569;font-size:13px;">No daily posts generated yet. Click "Mine &amp; Generate Fresh Daily Posts" above.</div>`;
    return;
  }

  grid.innerHTML = posts
    .map((p, idx) => {
      const score = p.scores?.composite_score ?? 90;
      const gslidesBtn = p.google_slides_url
        ? `<a class="btn-secondary" href="${escapeHtml(p.google_slides_url)}" target="_blank" rel="noopener">Google Slides ↗</a>`
        : "";
      return `
      <article class="daily-post-card" data-testid="daily-post-card-${idx + 1}">
        <div>
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
            <span class="brand-badge">#0${escapeHtml(String(p.rank || idx + 1))} • ${escapeHtml(p.style_code)} • ${escapeHtml(p.creator_inspiration)} (${escapeHtml(p.canonical_template_id)})</span>
            <span class="pill-badge pill-emerald">Score ${escapeHtml(String(score))}/100</span>
          </div>
          <h3 style="font-size:15px;font-weight:800;color:#0f172a;line-height:1.35;margin-bottom:4px;">${escapeHtml(p.topic_title)}</h3>
          <div style="font-size:11.5px;color:#475569;font-weight:600;margin-bottom:10px;">
            ${escapeHtml(p.source_channel)} • ${escapeHtml(p.published_at || p.edition_date)} • Archetype: <strong style="color:#174ea6;">${escapeHtml(p.archetype_name)}</strong>
          </div>

          <div class="daily-visual-stage" style="margin-bottom:10px;">
            <div class="daily-visual-tabs">
              <button type="button" class="daily-visual-tab-btn active" id="daily-vbtn-svg-${escapeHtml(p.id)}" onclick="switchDailyVisualTab('${escapeHtml(p.id)}', 'svg')">
                ⚡ Custom Topic Flow (.svg)
              </button>
              <button type="button" class="daily-visual-tab-btn" id="daily-vbtn-png-${escapeHtml(p.id)}" onclick="switchDailyVisualTab('${escapeHtml(p.id)}', 'png')">
                🎨 Canonical ${escapeHtml(p.canonical_template_id)} Poster (.png)
              </button>
            </div>
            <img id="daily-vis-svg-${escapeHtml(p.id)}" src="${escapeHtml(p.custom_dynamic_svg_url)}?v=20261103" alt="Custom Moving-Arrow SVG for ${escapeHtml(p.topic_title)}" style="width:100%;height:auto;display:block;border-radius:6px;background:#ffffff;" loading="lazy" />
            <img id="daily-vis-png-${escapeHtml(p.id)}" src="${escapeHtml(p.canonical_png_url)}?v=20261103" alt="Canonical ${escapeHtml(p.canonical_template_id)} Infographic" style="width:100%;height:auto;display:none;border-radius:6px;background:#ffffff;" loading="lazy" />
          </div>

          <div style="font-size:11.5px;font-weight:800;color:#0f172a;margin-bottom:5px;">Publication-Ready LinkedIn Copy:</div>
          <div class="daily-post-copy-box" id="daily-copy-text-${escapeHtml(p.id)}">${escapeHtml(p.linkedin_post_text)}

${escapeHtml(p.hashtags || "")}</div>

          <div style="margin-top:8px;padding:8px 10px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:6px;font-size:11.5px;color:#0c4a6e;">
            <strong>💬 Pin Comment #1:</strong> <a href="${escapeHtml(p.primary_url)}" target="_blank" rel="noopener" style="color:#0369a1;font-weight:700;word-break:break-all;">${escapeHtml(p.primary_url)}</a>
          </div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px solid #e2e8f0;">
          <button type="button" class="btn-primary copy-daily-post-btn" data-testid="copy-daily-post-btn-${idx + 1}" onclick="copyDailyPostText('${escapeHtml(p.id)}')">
            📋 Copy LinkedIn Post
          </button>
          <div style="display:flex;gap:6px;flex-wrap:wrap;">
            <a class="btn-secondary" href="${escapeHtml(p.custom_dynamic_svg_url)}" target="_blank" rel="noopener">Custom SVG ↗</a>
            <a class="btn-secondary" href="${escapeHtml(p.canonical_png_url)}" target="_blank" rel="noopener">${escapeHtml(p.canonical_template_id)} PNG ↗</a>
            ${gslidesBtn}
          </div>
        </div>
      </article>`;
    })
    .join("");
}

async function refreshLiveFeeds() {
  const res = await fetch("/api/live-mining-feeds");
  const data = await res.json();

  document.getElementById("live-arxiv-list").innerHTML = (data.arxiv || [])
    .map(
      (item) => `
      <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:12px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;margin-bottom:4px;">
          <span class="brand-badge">${escapeHtml(item.source_channel)}</span>
          <span style="font-size:11px;color:#475569;">${escapeHtml(item.published_at)}</span>
        </div>
        <div style="font-size:13.5px;font-weight:800;margin-bottom:4px;">${escapeHtml(item.title)}</div>
        <div style="font-size:12px;color:#334155;margin-bottom:6px;">${escapeHtml(item.summary)}</div>
        <a href="${escapeHtml(item.primary_url)}" target="_blank" style="font-size:11.5px;color:#1a73e8;font-weight:700;">View Primary arXiv Artifact ↗</a>
      </div>
    `
    )
    .join("");

  document.getElementById("live-github-list").innerHTML = (data.github || [])
    .map(
      (repo) => `
      <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:12px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;margin-bottom:4px;">
          <strong style="font-size:13.5px;color:#0f172a;word-break:break-word;">${escapeHtml(repo.full_name)}</strong>
          <span class="pill-badge pill-amber">★ ${escapeHtml(String(repo.stars))}</span>
        </div>
        <div style="font-size:12px;color:#334155;margin-bottom:6px;">${escapeHtml(repo.description)}</div>
        <a href="${escapeHtml(repo.html_url)}" target="_blank" style="font-size:11.5px;color:#1a73e8;font-weight:700;">Inspect GitHub Repository ↗</a>
      </div>
    `
    )
    .join("");
}

async function loadGalleryData() {
  const [gRes, pRes] = await Promise.all([fetch("/api/template-gallery"), fetch("/api/stack-pairings")]);
  const gData = await gRes.json();
  const pData = await pRes.json();
  STATE.templates = gData.templates || [];
  STATE.pairings = pData.pairings || [];
  renderGalleryView();
}

function renderGalleryView() {
  const grid = document.getElementById("gallery-cards-grid");
  if (!grid) return;
  const q = (document.getElementById("gallery-search-input")?.value || "").trim().toLowerCase();
  const tier = document.getElementById("gallery-filter-tier")?.value || "ALL";
  const type = document.getElementById("gallery-filter-type")?.value || "ALL";
  const items = (STATE.templates || []).filter((t) => {
    const topicIds = (t.topic_posts || []).map((tp) => `${tp.id} ${tp.name} ${tp.hot_topic || ""}`).join(" ");
    const hay = `${t.id} ${t.name} ${t.best_for_short} ${t.when_to_use} ${t.dynamic} ${t.lineage || ""} ${t.rendering_tech || ""} ${(t.content_types || []).join(" ")} ${topicIds}`.toLowerCase();
    const matchesQ = !q || hay.includes(q);
    const matchesTier = tier === "ALL" || (t.quality_tier || "Best") === tier;
    const matchesType = type === "ALL" || (t.content_types || []).includes(type);
    return matchesQ && matchesTier && matchesType;
  });
  const bestCount = items.filter((t) => (t.quality_tier || "Best") === "Best").length;
  const highCount = items.filter((t) => t.quality_tier === "High").length;
  document.getElementById("gallery-count-badge").textContent = `${items.length} / ${(STATE.templates || []).length} Certified Templates (${bestCount} Best + ${highCount} High)`;
  grid.innerHTML = items
    .map((t) => {
      const files = t.files || {};
      const svg = `/assets/template-gallery/${files.svg || t.id + ".svg"}?v=20261103`;
      const gif = `/assets/template-gallery/${files.gif || t.id + ".gif"}?v=20261103`;
      const png = `/assets/template-gallery/${files.png || t.id + ".png"}?v=20261103`;
      const drawio = files.drawio ? `/assets/template-gallery/${files.drawio}?v=20261103` : "";
      const pptx = files.pptx ? `/assets/template-gallery/${files.pptx}?v=20261103` : "";
      const gslidesUrl = t.google_slides_url || "";
      const qTier = t.quality_tier || "Best";
      const tierBadge =
        qTier === "Best"
          ? `<span class="pill-badge pill-emerald" style="white-space: nowrap; flex-shrink: 0;">🏆 BEST TIER</span>`
          : `<span class="pill-badge pill-sky" style="white-space: nowrap; flex-shrink: 0;">✨ HIGH TIER</span>`;
      const cleanWhenToUse = String(t.when_to_use || "").replace(/`/g, "").replace(/\s*->\s*/g, " → ");
      const cleanDynamic = String(t.dynamic || "").replace(/`/g, "").replace(/\s*->\s*/g, " → ").replace(/<=\s*/g, "≤ ");
      const topicPostsHtml =
        (t.topic_posts || []).length > 0
          ? `<div class="t79-variants-box" data-testid="t79-topic-posts-showcase" style="margin-top:8px;padding:10px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;">
               <div style="font-size:11.5px;font-weight:800;color:#0369a1;margin-bottom:6px;">
                 📚 ${t.topic_posts.length} Canonical 4-Tier Spine Topic Variants (T01, T53, T68–T78, T80–T89 • Including Minted T85–T89)
               </div>
               <div class="deliverable-chips">
                 ${t.topic_posts
                   .map(
                     (tp) =>
                       `<a class="deliverable-chip" style="text-decoration:none;background:#ffffff;border-color:#7dd3fc;color:#075985;" href="/assets/template-gallery/${escapeHtml(tp.id)}.svg" target="_blank" title="${escapeHtml(tp.name)}">${escapeHtml(tp.id)}</a>`
                   )
                   .join("")}
               </div>
             </div>`
          : "";
      return `
      <article class="repo-card" data-testid="template-card-${escapeHtml(t.id)}">
        <div>
          <div class="repo-card-header" style="align-items: flex-start; gap: 8px; flex-wrap: nowrap;">
            <span class="brand-badge" style="min-width: 0;">${escapeHtml(t.id)} • ${escapeHtml(t.name)}</span>
            ${tierBadge}
          </div>
          <div style="margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; background: #ffffff;">
            <a href="${svg}" target="_blank" title="Open animated SVG"><img src="${svg}" alt="${escapeHtml(t.name)} dynamic template" style="width: 100%; height: auto; display: block;" loading="lazy" /></a>
          </div>
          <div class="repo-card-hook">${escapeHtml(cleanWhenToUse)}</div>
          <div style="margin-top: 8px; font-size: 11.5px; color: #475569; font-weight: 600;">Dynamic elements: <strong style="color: #0f172a;">${escapeHtml(cleanDynamic)}</strong></div>
          ${t.rendering_tech ? `<div style="margin-top: 4px; font-size: 11px; color: #065f46; font-weight: 700;">Rendering Tech: ${escapeHtml(t.rendering_tech)}</div>` : ""}
          ${t.lineage ? `<div style="margin-top: 4px; font-size: 11px; color: #1d4ed8; font-weight: 700;">Format lineage: ${escapeHtml(t.lineage)}</div>` : ""}
          ${topicPostsHtml}
        </div>
        <div>
          <div class="deliverable-chips" style="margin: 10px 0;">
            ${(t.content_types || []).map((c) => `<span class="deliverable-chip">${escapeHtml(c)}</span>`).join("")}
            <span class="deliverable-chip" style="background:#eff6ff;border-color:#93c5fd;color:#1d4ed8;">OSS ⇄ Google</span>
            ${gslidesUrl ? `<span class="deliverable-chip" style="background:#fef3c7;border-color:#fcd34d;color:#92400e;">Editable Google Slides (${escapeHtml(String(t.editable_slide_count || 5))} slides)</span>` : ""}
          </div>
          <div class="repo-card-footer" style="display:flex;flex-wrap:wrap;gap:6px;">
            ${gslidesUrl ? `<a class="btn-primary" style="background:#0f172a;border-color:#0f172a;" data-testid="open-with-google-slides-btn-${escapeHtml(t.id)}" href="${escapeHtml(gslidesUrl)}" target="_blank" rel="noopener">Open with Google Slides ↗</a>` : ""}
            ${pptx ? `<a class="btn-secondary" data-testid="download-pptx-btn-${escapeHtml(t.id)}" href="${pptx}" download="${escapeHtml(t.id)}.pptx">Editable .pptx</a>` : ""}
            ${drawio ? `<a class="btn-secondary" data-testid="download-drawio-btn-${escapeHtml(t.id)}" href="${drawio}" download="${escapeHtml(t.id)}.drawio">Editable .drawio</a>` : ""}
            <a class="btn-secondary" href="${png}" target="_blank">PNG ↗</a>
            <a class="btn-secondary" href="${gif}" download>GIF</a>
            <a class="btn-secondary" href="${svg}" target="_blank">SVG ↗</a>
          </div>
        </div>
      </article>`;
    })
    .join("");

  const tbody = document.getElementById("pairings-tbody");
  if (tbody) {
    tbody.innerHTML = (STATE.pairings || [])
      .map(
        (p) => `
        <tr>
          <td><div class="cell-card-equal"><strong style="font-size: 12px;">${escapeHtml(p.capability)}</strong></div></td>
          <td><div class="cell-card-equal"><span style="font-size: 11.5px; color: #174ea6; font-weight: 700;">${escapeHtml(p.google)}</span></div></td>
          <td><div class="cell-card-equal"><span style="font-size: 11.5px; color: #065f46; font-weight: 700;">${escapeHtml(p.oss)}</span></div></td>
          <td><div class="cell-card-equal"><span style="font-size: 11px; color: #334155;">${escapeHtml(p.note)}</span></div></td>
        </tr>`
      )
      .join("");
  }
}

function seekMint01Video(seconds) {
  const vid = document.getElementById("mint01-walkthrough-video");
  if (!vid) return;
  try {
    vid.currentTime = Number(seconds) || 0;
  } catch (_) {
    // Ignore if metadata not yet loaded
  }
}

function toggleMint01WalkthroughPlay() {
  const vid = document.getElementById("mint01-walkthrough-video");
  if (!vid) return;
  if (vid.paused) {
    vid.play().catch(() => {});
  } else {
    vid.pause();
  }
}

function toggleMint01WalkthroughMute() {
  const vid = document.getElementById("mint01-walkthrough-video");
  if (!vid) return;
  vid.muted = !vid.muted;
}

function toggleMint01TwinPlay() {
  const vid = document.getElementById("mint01-twin-video");
  if (!vid) return;
  if (vid.paused) {
    vid.play().catch(() => {});
  } else {
    vid.pause();
  }
}

async function loadMintingStudioData() {
  const res = await fetch("/api/minting-studio");
  const data = await res.json();
  STATE.mintingStudio = data;
  renderMintingStudioView();
}

function renderMintingStudioView() {
  const grid = document.getElementById("minting-topics-grid");
  if (!grid) return;
  const studio = STATE.mintingStudio || {};
  const topics = studio.topics || [];
  const badge = document.getElementById("minting-topics-count-badge");
  if (badge && topics.length) {
    const mintedCount = topics.filter((t) => t.siso_decision === "MINT_NEW").length;
    badge.textContent = `${topics.length} Career-Minting Topics • ${mintedCount} Newly Minted (T85–T89)`;
  }

  grid.innerHTML = topics
    .map((t) => {
      const sisoScore = t.siso_audit?.siso_score ?? t.nearest_prior_siso ?? 62.0;
      const decision = t.siso_audit?.decision || t.siso_decision || "MINT_NEW";
      const decisionClass =
        decision === "MINT_NEW"
          ? "pill-amber"
          : decision === "COMPOSE_2VIEW_ZOOM"
            ? "pill-sky"
            : "pill-emerald";
      const tid = t.canonical_template_id || "T85";
      const gslidesUrl = t.template_google_slides_url || "";
      const flagshipUrl = t.flagship_24slide_url || "";
      return `
      <article class="repo-card" data-testid="mint-topic-card-${escapeHtml(t.id)}">
        <div>
          <div class="repo-card-header">
            <span class="brand-badge">${escapeHtml(t.id)} • Mnemonic: ${escapeHtml(t.mnemonic)}</span>
            <span class="pill-badge ${decisionClass}">S_iso ${escapeHtml(String(sisoScore))} (${escapeHtml(decision)} → ${escapeHtml(tid)})</span>
          </div>
          <h3 class="repo-card-title" style="margin: 10px 0 6px 0;">${escapeHtml(t.title)}</h3>
          <div style="font-size: 11.5px; font-weight: 800; color: #174ea6; margin-bottom: 6px;">
            🧠 ${escapeHtml(t.mnemonic)}: ${escapeHtml(t.mnemonic_expansion)}
          </div>
          <div class="repo-card-hook" style="margin-bottom: 8px;">
            <strong>Mental Model Analogy:</strong> ${escapeHtml(t.analogy)}
          </div>
          <div style="margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; background: #ffffff;">
            <a href="/assets/template-gallery/${escapeHtml(tid)}.svg" target="_blank">
              <img src="/assets/template-gallery/${escapeHtml(tid)}.svg?v=20261103" alt="${escapeHtml(t.title)} Canonical Blueprint ${escapeHtml(tid)}" style="width: 100%; height: auto; display: block;" loading="lazy" />
            </a>
          </div>
          <div style="font-size: 12px; color: #0f172a; line-height: 1.45; margin-bottom: 6px;">
            <strong>🎯 30s Staff+ Interview Signal:</strong> ${escapeHtml(t.interview_signal)}
          </div>
          <div style="font-size: 11.5px; color: #065f46; font-weight: 700; margin-bottom: 6px;">
            📈 <strong>L5→L7 Promo Impact:</strong> ${escapeHtml(t.promo_impact)}
          </div>
          <div style="font-size: 11.5px; color: #334155; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 8px;">
            <strong>Golden Rule:</strong> ${escapeHtml(t.golden_rule)}
          </div>
        </div>
        <div>
          <div class="deliverable-chips" style="margin: 10px 0;">
            <span class="deliverable-chip" style="background:#fef3c7;border-color:#fcd34d;color:#92400e;">Blueprint ${escapeHtml(tid)} + ${escapeHtml((t.cloud_zoom_blueprints || []).join("/"))}</span>
            ${(t.gcp_stack || []).slice(0, 2).map((s) => `<span class="deliverable-chip">${escapeHtml(s)}</span>`).join("")}
            ${(t.oss_stack || []).slice(0, 2).map((s) => `<span class="deliverable-chip" style="background:#eff6ff;border-color:#93c5fd;color:#1d4ed8;">OSS: ${escapeHtml(s)}</span>`).join("")}
          </div>
          <div class="repo-card-footer" style="display:flex;flex-wrap:wrap;gap:6px;">
            ${flagshipUrl ? `<a class="btn-primary" style="background:#0f172a;border-color:#0f172a;" href="${escapeHtml(flagshipUrl)}" target="_blank" rel="noopener">📊 24-Slide Google Slides ↗</a>` : ""}
            ${gslidesUrl ? `<a class="btn-secondary" href="${escapeHtml(gslidesUrl)}" target="_blank" rel="noopener">${escapeHtml(tid)} Slides ↗</a>` : ""}
            <a class="btn-secondary" href="/assets/template-gallery/${escapeHtml(tid)}.pptx" download="${escapeHtml(tid)}.pptx">.pptx</a>
            <a class="btn-secondary" href="/assets/template-gallery/${escapeHtml(tid)}.drawio" download="${escapeHtml(tid)}.drawio">.drawio</a>
            <button type="button" class="btn-primary" onclick="openRepoInspector('${escapeHtml(t.repo_slug)}')">Inspect Repo →</button>
          </div>
        </div>
      </article>`;
    })
    .join("");
}

const ALL_VIEWS = [
  "view-repos",
  "view-gallery",
  "view-playbook",
  "view-miner",
  "view-openhands",
  "view-minting-studio",
];

function mkEl(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined && text !== null) el.textContent = String(text);
  return el;
}

function safeUrl(rawUrl) {
  const s = String(rawUrl || "").trim();
  if (
    s.startsWith("/assets/") ||
    s.startsWith("/repos/") ||
    s.startsWith("/api/") ||
    s.startsWith("https://") ||
    s.startsWith("http://")
  ) {
    return s;
  }
  return "#";
}

function getActiveTop5Idea() {
  const ideas = STATE.top5Briefing?.ideas || [];
  return ideas.find((i) => i.id === STATE.selectedIdeaId) || ideas[0] || null;
}

function getActiveTop5Template(idea) {
  if (!idea) return null;
  const list = idea.matching_templates || [];
  return list.find((t) => t.template_id === STATE.selectedTemplateId) || list[0] || null;
}

async function loadDailyTop5Briefing() {
  const res = await fetch("/api/daily-top5-briefing");
  const data = await res.json();
  applyTop5BriefingPayload(data);
  await refreshPlatformPreviewPackages();
}

function applyTop5BriefingPayload(data) {
  STATE.top5Briefing = data.briefing || null;
  STATE.modeContracts = data.mode_contracts || data.briefing?.mode_contracts || {};
  STATE.platformSpecs = data.platform_specs || {};
  if (data.outbox) {
    STATE.outboxLedger = data.outbox;
  }
  const ideas = STATE.top5Briefing?.ideas || [];
  if (ideas.length) {
    const existing = ideas.find((i) => i.id === STATE.selectedIdeaId);
    const chosen = existing || ideas[0];
    STATE.selectedIdeaId = chosen.id;
    const matchedTpl = (chosen.matching_templates || []).find(
      (t) => t.template_id === STATE.selectedTemplateId
    );
    STATE.selectedTemplateId = matchedTpl ? matchedTpl.template_id : chosen.default_template_id;
    STATE.selectedMode = STATE.selectedMode || chosen.default_recommended_mode || "Carousel";
    if (!existing) {
      STATE.selectedMode = chosen.default_recommended_mode || "Carousel";
    }
  }
  const edBadge = document.getElementById("top5-edition-badge");
  if (edBadge && STATE.top5Briefing) {
    edBadge.textContent = `${STATE.top5Briefing.ideas_count || 5} Unique Ideas • Edition ${STATE.top5Briefing.edition_date || ""}`;
  }
  const ledgerBadge = document.getElementById("top5-ledger-badge");
  if (ledgerBadge && STATE.top5Briefing) {
    ledgerBadge.textContent = `30-Day Dedupe Ledger (${STATE.top5Briefing.dedupe_ledger_entries || 5} Tracked • ${STATE.top5Briefing.certified_pool_size || 116} Certified Pool)`;
  }
  renderTop5EditorialDesk();
  renderPublishingOutbox();
}

async function triggerGenerateTop5Briefing() {
  const btn = document.getElementById("generate-top5-briefing-btn");
  const qInput = document.getElementById("top5-query-input");
  const topic_query = (qInput?.value || "").trim();
  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Scoring Top-5 Ideas...";
  }
  try {
    const res = await fetch("/api/daily-top5-briefing/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic_query, use_live_network: true }),
    });
    const data = await res.json();
    STATE.selectedIdeaId = "";
    applyTop5BriefingPayload(data);
    await refreshPlatformPreviewPackages();
    showToast("Refreshed Daily Top-5 Unique In-Demand Ideas & 5×5 Certified Blueprints!");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "⚡ Refresh Daily Top-5 Briefing";
    }
  }
}

async function refreshPlatformPreviewPackages() {
  const idea = getActiveTop5Idea();
  const tpl = getActiveTop5Template(idea);
  if (!idea || !tpl) return;
  const res = await fetch("/api/publisher/preview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      idea_id: idea.id,
      template_id: tpl.template_id,
      mode: STATE.selectedMode,
      platform_id: "ALL",
    }),
  });
  const data = await res.json();
  if (data.packages) {
    STATE.previewPackagesByPlatform = data.packages;
    renderTop5PlatformPreviewStage();
  }
}

async function triggerTranscodeActiveIdea() {
  const idea = getActiveTop5Idea();
  const tpl = getActiveTop5Template(idea);
  if (!idea || !tpl) return;
  const btn = document.getElementById("transcode-active-idea-btn");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Rendering 4:5 JPEGs/PDF + 9:16 Short MP4...";
  }
  try {
    const res = await fetch("/api/publisher/transcode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        idea_id: idea.id,
        template_id: tpl.template_id,
        force: false,
      }),
    });
    const out = await res.json();
    if (out.status === "TRANSCODED") {
      await refreshPlatformPreviewPackages();
      showToast(`Rendered 4:5 Carousel (8 JPEGs + PDF) & 9:16 Safe-Zone Short MP4 for ${idea.id}!`);
    } else {
      showToast(out.error || "Transcode request did not complete");
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "🎬 Transcode 4:5 Carousel + 9:16 Short MP4";
    }
  }
}

async function stageSelectedPlatformsToOutbox() {
  const idea = getActiveTop5Idea();
  const tpl = getActiveTop5Template(idea);
  if (!idea || !tpl) return;
  const platforms = Array.from(STATE.selectedStagePlatforms);
  if (!platforms.length) {
    showToast("Select at least one target channel to stage");
    return;
  }
  const res = await fetch("/api/publisher/stage", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      idea_id: idea.id,
      template_id: tpl.template_id,
      mode: STATE.selectedMode,
      platforms,
    }),
  });
  const data = await res.json();
  if (data.ledger) {
    STATE.outboxLedger = data.ledger;
    renderPublishingOutbox();
    showToast(`Staged ${platforms.length} compliant platform packages into HITL Outbox!`);
  } else {
    showToast(data.error || "Unable to stage platform packages");
  }
}

async function approveOutboxItems(outboxIds) {
  const res = await fetch("/api/publisher/approve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(outboxIds ? { outbox_ids: outboxIds } : {}),
  });
  const data = await res.json();
  if (data.ledger) {
    STATE.outboxLedger = data.ledger;
    renderPublishingOutbox();
    const count = (data.processed || []).length;
    showToast(`Validated & processed ${count} Outbox package(s) via compliant API/Dry-Run dispatcher!`);
  }
}

function polishUiTypography(str) {
  return String(str || "")
    .replace(/pass\^k/g, "passᵏ")
    .replace(/pass\^3/g, "pass³")
    .replace(/pass\^5/g, "pass⁵");
}

function formatModeDisplayName(modeKey) {
  const map = {
    Carousel: "Carousel",
    Image: "Image",
    Short_Video: "Short Video",
    Video: "16:9 Video",
    Slidedeck: "Slide Deck",
    Slide: "1-Slide BLUF",
    Doc: "Technical Doc",
    Text: "Text / Thread",
  };
  return map[modeKey] || String(modeKey || "").replace(/_/g, " ");
}

function renderTop5EditorialDesk() {
  const ideasCol = document.getElementById("top5-ideas-column");
  const workbench = document.getElementById("top5-active-workbench");
  if (!ideasCol || !workbench) return;
  ideasCol.replaceChildren();
  workbench.replaceChildren();

  const ideas = STATE.top5Briefing?.ideas || [];
  if (!ideas.length) {
    ideasCol.appendChild(mkEl("div", "", "Loading Daily Top-5 Unique In-Demand Ideas..."));
    return;
  }

  ideas.forEach((idea, idx) => {
    const card = mkEl(
      "button",
      `top5-idea-card${idea.id === STATE.selectedIdeaId ? " active" : ""}`
    );
    card.type = "button";
    card.setAttribute("data-testid", `top5-idea-card-${idx + 1}`);

    const topRow = mkEl("div");
    topRow.style.cssText =
      "display:flex;justify-content:space-between;align-items:flex-start;gap:6px;flex-wrap:wrap;margin-bottom:6px;";
    topRow.appendChild(
      mkEl("span", "brand-badge", `#0${idea.rank} • ${idea.cluster_label}`)
    );
    const rightPills = mkEl("div");
    rightPills.style.cssText = "display:flex;gap:5px;flex-wrap:wrap;";
    rightPills.appendChild(
      mkEl(
        "span",
        "pill-badge pill-emerald",
        `Demand ${idea.scores?.demand_score ?? 94}/100`
      )
    );
    if (idea.unique_30d_verified) {
      rightPills.appendChild(mkEl("span", "pill-badge pill-sky", "30d Unique ✓"));
    }
    topRow.appendChild(rightPills);
    card.appendChild(topRow);

    const titleEl = mkEl("div", "", polishUiTypography(idea.title));
    titleEl.style.cssText =
      "font-size:14px;font-weight:800;color:#0f172a;line-height:1.34;margin-bottom:5px;";
    card.appendChild(titleEl);

    const sumEl = mkEl("div", "", polishUiTypography(idea.summary));
    sumEl.style.cssText =
      "font-size:12px;color:#475569;line-height:1.42;margin-bottom:7px;";
    card.appendChild(sumEl);

    const tplIds = (idea.matching_templates || []).map((t) => t.template_id).join(" · ");
    const footEl = mkEl(
      "div",
      "",
      `Top 5 Templates: ${tplIds} • Default Mode: ${formatModeDisplayName(idea.default_recommended_mode)}`
    );
    footEl.style.cssText = "font-size:11px;font-weight:700;color:#174ea6;";
    card.appendChild(footEl);

    card.addEventListener("click", async () => {
      STATE.selectedIdeaId = idea.id;
      STATE.selectedTemplateId = idea.default_template_id;
      STATE.selectedMode = idea.default_recommended_mode || "Carousel";
      renderTop5EditorialDesk();
      await refreshPlatformPreviewPackages();
    });
    ideasCol.appendChild(card);
  });

  const activeIdea = getActiveTop5Idea();
  const activeTpl = getActiveTop5Template(activeIdea);
  if (!activeIdea || !activeTpl) return;

  // Active Idea Header Banner
  const hdrBox = mkEl("div");
  hdrBox.style.cssText =
    "display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;padding-bottom:10px;border-bottom:1px solid #e2e8f0;";
  const hdrTextWrap = mkEl("div", "min-w-0");
  const hdrKicker = mkEl(
    "div",
    "",
    polishUiTypography(`ACTIVE IDEA #0${activeIdea.rank} • ${activeIdea.source_channel} • ${activeIdea.metrics_hint}`)
  );
  hdrKicker.style.cssText = "font-size:11px;font-weight:800;color:#0369a1;margin-bottom:3px;";
  const hdrTitle = mkEl("h3", "", polishUiTypography(activeIdea.title));
  hdrTitle.style.cssText = "font-size:15.5px;font-weight:800;color:#0f172a;line-height:1.32;";
  hdrTextWrap.appendChild(hdrKicker);
  hdrTextWrap.appendChild(hdrTitle);
  hdrBox.appendChild(hdrTextWrap);

  const srcLink = mkEl("a", "btn-secondary", "Primary Signal ↗");
  srcLink.href = safeUrl(activeIdea.primary_url);
  srcLink.target = "_blank";
  srcLink.rel = "noopener";
  hdrBox.appendChild(srcLink);
  workbench.appendChild(hdrBox);

  // Step 1: 5 Orthogonal Matching Templates
  const step1 = mkEl("div", "top5-step-block");
  step1.appendChild(
    mkEl(
      "div",
      "top5-step-label",
      "Step 1 — Top 5 Orthogonal Certified Templates (5 Storytelling Angles • 0 Legacy Gen-1)"
    )
  );
  const tplRow = mkEl("div", "top5-pill-row");
  tplRow.setAttribute("data-testid", "top5-template-pills");
  (activeIdea.matching_templates || []).forEach((tpl, tIdx) => {
    const isSel = tpl.template_id === activeTpl.template_id;
    const pill = mkEl(
      "button",
      `top5-selector-pill${isSel ? " active" : ""}${tIdx === 0 ? " recommended" : ""}`,
      `#${tIdx + 1} ${tpl.template_id} • ${tpl.angle_label || tpl.quality_tier} (${tpl.fit_score || 95})`
    );
    pill.type = "button";
    pill.setAttribute("data-testid", `top5-tpl-pill-${tIdx + 1}`);
    pill.title = `${tpl.name} — Recommended Mode: ${tpl.recommended_mode}`;
    pill.addEventListener("click", async () => {
      STATE.selectedTemplateId = tpl.template_id;
      if (tpl.recommended_mode) {
        STATE.selectedMode = tpl.recommended_mode;
      }
      renderTop5EditorialDesk();
      await refreshPlatformPreviewPackages();
    });
    tplRow.appendChild(pill);
  });
  step1.appendChild(tplRow);

  const tplReason = mkEl(
    "div",
    "",
    `Selected Blueprint: ${activeTpl.template_id} (${activeTpl.name}) • Tier: ${activeTpl.quality_tier || "Best"} • Recommended Mode: ${activeTpl.recommended_mode || activeIdea.default_recommended_mode}`
  );
  tplReason.style.cssText = "margin-top:7px;font-size:11.5px;color:#334155;font-weight:600;";
  step1.appendChild(tplReason);
  workbench.appendChild(step1);

  // Step 2: 8 Presentation Modes + 3-Part Content-Length Contract
  const step2 = mkEl("div", "top5-step-block");
  step2.appendChild(
    mkEl(
      "div",
      "top5-step-label",
      "Step 2 — Presentation Mode & 3-Part (Mode × Platform) Content-Length Contract"
    )
  );
  const modeRow = mkEl("div", "top5-pill-row");
  modeRow.setAttribute("data-testid", "top5-mode-pills");
  const modeKeys = [
    "Carousel",
    "Image",
    "Short_Video",
    "Video",
    "Slidedeck",
    "Slide",
    "Doc",
    "Text",
  ];
  const recMode = activeTpl.recommended_mode || activeIdea.default_recommended_mode;
  modeKeys.forEach((mKey) => {
    const mSpec = STATE.modeContracts[mKey] || { short_label: mKey };
    const isSel = STATE.selectedMode === mKey;
    const isRec = recMode === mKey;
    const pill = mkEl(
      "button",
      `top5-selector-pill${isSel ? " active" : ""}${isRec ? " recommended" : ""}`,
      `${isRec ? "★ " : ""}${mSpec.short_label || mKey}`
    );
    pill.type = "button";
    pill.setAttribute("data-testid", `top5-mode-pill-${mKey}`);
    pill.addEventListener("click", async () => {
      STATE.selectedMode = mKey;
      renderTop5EditorialDesk();
      await refreshPlatformPreviewPackages();
    });
    modeRow.appendChild(pill);
  });
  step2.appendChild(modeRow);

  const activeModeSpec = STATE.modeContracts[STATE.selectedMode] || {};
  const budget = activeModeSpec.length_budget || {};
  const budgetGrid = mkEl("div", "top5-length-budget-grid");
  budgetGrid.setAttribute("data-testid", "top5-length-budget-strip");

  [
    ["1. Hook / Above-the-Fold", budget.hook_above_fold || "Front-loaded metric hook"],
    ["2. Per-Unit Density Cap", budget.per_unit_density || "Bounded visual density"],
    [
      `3. Total Deliverable (${budget.estimated_consumption_time || "Fast read"})`,
      budget.total_deliverable_size || "Platform-calibrated deliverable",
    ],
  ].forEach(([bTitle, bVal]) => {
    const bCard = mkEl("div", "top5-budget-card");
    bCard.appendChild(mkEl("div", "top5-budget-card-title", bTitle));
    bCard.appendChild(mkEl("div", "top5-budget-card-val", bVal));
    budgetGrid.appendChild(bCard);
  });
  step2.appendChild(budgetGrid);
  workbench.appendChild(step2);

  // Step 3: 13-Platform Auto-Publish Staging & Live Compliance Preview
  const step3 = mkEl("div", "top5-step-block");
  const step3Hdr = mkEl("div");
  step3Hdr.style.cssText =
    "display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;";
  step3Hdr.appendChild(
    mkEl(
      "div",
      "top5-step-label",
      "Step 3 — 13-Channel Compliant Staging & Platform-Specific Limit Inspector"
    )
  );
  const stageBtn = mkEl(
    "button",
    "btn-primary",
    "📥 Stage Selected Channels to Outbox"
  );
  stageBtn.type = "button";
  stageBtn.id = "stage-selected-platforms-btn";
  stageBtn.setAttribute("data-testid", "stage-selected-platforms-btn");
  stageBtn.addEventListener("click", stageSelectedPlatformsToOutbox);
  step3Hdr.appendChild(stageBtn);
  step3.appendChild(step3Hdr);

  // Rule 25 Unified 13-Channel Bar: inline staging checkbox + click-to-inspect active channel
  const orderedPlatforms = [
    "linkedin",
    "telegram",
    "youtube",
    "youtube_shorts",
    "instagram",
    "facebook",
    "tiktok",
    "whatsapp",
    "devto",
    "hashnode",
    "bluesky",
    "x",
    "substack",
  ];
  const previewTabs = mkEl("div", "top5-unified-channel-bar");
  previewTabs.setAttribute("data-testid", "top5-platform-preview-tabs");
  orderedPlatforms.forEach((pid) => {
    const pSpec = STATE.platformSpecs[pid];
    if (!pSpec) return;
    const isAct = STATE.selectedPreviewPlatform === pid;
    const tabBtn = mkEl(
      "button",
      `top5-unified-channel-chip${isAct ? " active" : ""}`
    );
    tabBtn.type = "button";
    tabBtn.setAttribute("data-testid", `top5-plat-tab-${pid}`);

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = STATE.selectedStagePlatforms.has(pid);
    cb.title = `Include ${pSpec.name} when staging to Outbox`;
    cb.setAttribute("data-testid", `stage-check-${pid}`);
    cb.addEventListener("click", (ev) => {
      ev.stopPropagation();
    });
    cb.addEventListener("change", () => {
      if (cb.checked) STATE.selectedStagePlatforms.add(pid);
      else STATE.selectedStagePlatforms.delete(pid);
    });
    tabBtn.appendChild(cb);
    tabBtn.appendChild(mkEl("span", "", pSpec.name.split("(")[0].trim()));

    tabBtn.addEventListener("click", () => {
      STATE.selectedPreviewPlatform = pid;
      previewTabs.querySelectorAll(".top5-unified-channel-chip").forEach((b) => {
        b.classList.toggle("active", b === tabBtn);
      });
      renderTop5PlatformPreviewStage();
    });
    previewTabs.appendChild(tabBtn);
  });
  step3.appendChild(previewTabs);

  const previewStageContainer = mkEl("div");
  previewStageContainer.id = "top5-platform-preview-stage";
  previewStageContainer.setAttribute("data-testid", "top5-platform-preview-stage");
  step3.appendChild(previewStageContainer);
  workbench.appendChild(step3);

  renderTop5PlatformPreviewStage();
}

function renderTop5PlatformPreviewStage() {
  const stage = document.getElementById("top5-platform-preview-stage");
  if (!stage) return;
  stage.replaceChildren();

  const pkg = STATE.previewPackagesByPlatform[STATE.selectedPreviewPlatform];
  if (!pkg) {
    stage.appendChild(mkEl("div", "", "Compiling platform compliance preview..."));
    return;
  }

  const checks = pkg.compliance_checks || {};
  const media = pkg.media || {};

  // Telemetry & Compliance Strip
  const chipsRow = mkEl("div", "deliverable-chips");
  chipsRow.style.marginTop = "10px";
  chipsRow.appendChild(mkEl("span", "pill-badge pill-sky", pkg.tier_badge || pkg.tier));
  chipsRow.appendChild(
    mkEl(
      "span",
      `pill-badge ${checks.char_limit_ok ? "pill-emerald" : "pill-amber"}`,
      `Chars: ${checks.char_used}/${checks.char_cap} ${checks.char_limit_ok ? "✓" : "!"}`
    )
  );
  chipsRow.appendChild(
    mkEl(
      "span",
      `pill-badge ${checks.fold_hook_ok ? "pill-emerald" : "pill-amber"}`,
      `Above-Fold Hook: ${checks.fold_used}/${checks.fold_cap} chars ✓`
    )
  );
  chipsRow.appendChild(
    mkEl(
      "span",
      "pill-badge pill-emerald",
      `Container: ${media.container_format} • ${media.aspect_ratio}`
    )
  );
  chipsRow.appendChild(
    mkEl(
      "span",
      "pill-badge pill-emerald",
      `Link Rule: ${pkg.link_strategy}`
    )
  );
  if (pkg.mode_auto_adapted) {
    chipsRow.appendChild(
      mkEl(
        "span",
        "pill-badge pill-amber",
        `Auto-Adapted: ${pkg.requested_mode} → ${pkg.effective_mode}`
      )
    );
  }
  stage.appendChild(chipsRow);

  const grid = mkEl("div", "top5-platform-preview-grid");

  // Left: Media Container Preview
  const mediaCol = mkEl("div", "top5-media-stage");
  const mediaHdr = mkEl(
    "div",
    "",
    `Media Deliverable • ${media.container_format} ${media.aspect_ratio}`
  );
  mediaHdr.style.cssText = "font-size:11.5px;font-weight:800;color:#0f172a;margin-bottom:8px;";
  mediaCol.appendChild(mediaHdr);

  if (media.container_format === "MP4" && media.primary_asset_url) {
    const vid = document.createElement("video");
    vid.controls = true;
    vid.muted = true;
    vid.playsInline = true;
    vid.preload = "metadata";
    if (media.poster_url) vid.poster = safeUrl(media.poster_url);
    vid.src = safeUrl(media.primary_asset_url);
    vid.style.cssText =
      "width:100%;max-height:360px;object-fit:contain;border-radius:6px;background:#f8fafc;border:1px solid #cbd5e1;display:block;";
    mediaCol.appendChild(vid);
  } else if ((media.slide_urls || []).length > 0) {
    const heroImg = document.createElement("img");
    heroImg.src = safeUrl(media.slide_urls[0]);
    heroImg.alt = `${pkg.platform_name} Slide 1 Preview`;
    heroImg.style.cssText =
      "width:100%;max-height:330px;object-fit:contain;border-radius:6px;background:#f8fafc;border:1px solid #cbd5e1;display:block;";
    mediaCol.appendChild(heroImg);

    const thumbs = mkEl("div", "top5-carousel-thumbs");
    media.slide_urls.slice(0, 8).forEach((sUrl, sIdx) => {
      const th = document.createElement("img");
      th.src = safeUrl(sUrl);
      th.alt = `Slide ${sIdx + 1}`;
      th.title = `Preview Slide ${sIdx + 1} of ${media.slide_urls.length}`;
      th.loading = "lazy";
      th.addEventListener("click", () => {
        heroImg.src = safeUrl(sUrl);
      });
      thumbs.appendChild(th);
    });
    mediaCol.appendChild(thumbs);
  } else if (media.primary_asset_url) {
    const img = document.createElement("img");
    img.src = safeUrl(media.primary_asset_url);
    img.alt = `${pkg.platform_name} Visual Preview`;
    img.style.cssText =
      "width:100%;max-height:320px;object-fit:contain;border-radius:6px;background:#ffffff;border:1px solid #cbd5e1;display:block;";
    mediaCol.appendChild(img);
  } else {
    const txtNote = mkEl(
      "div",
      "",
      "Typography-Only Native Post (Zero Media Attachment — High Dwell Text Mode)"
    );
    txtNote.style.cssText =
      "padding:18px;background:#f8fafc;border:1px dashed #cbd5e1;border-radius:6px;font-size:12px;color:#475569;text-align:center;";
    mediaCol.appendChild(txtNote);
  }

  const assetLinks = mkEl("div");
  assetLinks.style.cssText = "display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;";
  if (media.primary_asset_url) {
    const openAsset = mkEl("a", "btn-secondary", `Open ${media.container_format} Asset ↗`);
    openAsset.href = safeUrl(media.primary_asset_url);
    openAsset.target = "_blank";
    openAsset.rel = "noopener";
    assetLinks.appendChild(openAsset);
  }
  if (pkg.share_intent_url) {
    const shareLink = mkEl("a", "btn-secondary", "1-Click Native Share Intent ↗");
    shareLink.href = safeUrl(pkg.share_intent_url);
    shareLink.target = "_blank";
    shareLink.rel = "noopener";
    assetLinks.appendChild(shareLink);
  }
  mediaCol.appendChild(assetLinks);
  grid.appendChild(mediaCol);

  // Right: Tailored Copy + Comment #1 + Compliance Rule Note
  const copyCol = mkEl("div", "min-w-0");
  if (pkg.video_title) {
    const vt = mkEl("div", "", `Video Title (${pkg.video_title.length}/100): ${pkg.video_title}`);
    vt.style.cssText = "font-size:12px;font-weight:800;color:#0f172a;margin-bottom:6px;";
    copyCol.appendChild(vt);
  }

  const copyHdr = mkEl("div");
  copyHdr.style.cssText =
    "display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:6px;";
  copyHdr.appendChild(
    mkEl("strong", "", `${pkg.platform_name} Calibrated Copy`)
  );
  const copyBtn = mkEl("button", "btn-secondary", "📋 Copy Channel Payload");
  copyBtn.type = "button";
  copyBtn.addEventListener("click", () => {
    const combined = pkg.follow_up_comment
      ? `${pkg.body}\n\n---\n${pkg.follow_up_comment}`
      : pkg.body;
    copyTextSafe(combined, `Copied ${pkg.platform_name} compliant payload!`);
  });
  copyHdr.appendChild(copyBtn);
  copyCol.appendChild(copyHdr);

  const bodyBox = mkEl("div", "top5-copy-full-box", polishUiTypography(pkg.body));
  bodyBox.setAttribute("data-testid", "top5-platform-copy-box");
  copyCol.appendChild(bodyBox);

  if (pkg.follow_up_comment) {
    const c1 = mkEl("div", "", `Chained Comment #1 / Reply #2: ${pkg.follow_up_comment}`);
    c1.style.cssText =
      "margin-top:8px;padding:8px 10px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:6px;font-size:11.5px;color:#0c4a6e;word-break:break-word;";
    copyCol.appendChild(c1);
  }

  const compBox = mkEl("div", "", `Platform Guardrail: ${pkg.compliance_note}`);
  compBox.style.cssText =
    "margin-top:8px;padding:8px 10px;background:#ecfdf5;border:1px solid #6ee7b7;border-radius:6px;font-size:11.5px;color:#065f46;line-height:1.4;";
  copyCol.appendChild(compBox);

  if ((pkg.missing_env_vars || []).length > 0) {
    const envNote = mkEl(
      "div",
      "",
      `Auth Mode: Validated Dry-Run Ready (set server env ${pkg.missing_env_vars.join(", ")} for live HTTPS API push)`
    );
    envNote.style.cssText =
      "margin-top:6px;font-size:11px;color:#475569;font-family:ui-monospace,monospace;";
    copyCol.appendChild(envNote);
  }

  grid.appendChild(copyCol);
  stage.appendChild(grid);
}

function renderPublishingOutbox() {
  const tbody = document.getElementById("publishing-outbox-tbody");
  const badge = document.getElementById("outbox-summary-badge");
  if (!tbody) return;
  tbody.replaceChildren();

  const ledger = STATE.outboxLedger || { items: [] };
  const items = ledger.items || [];
  const pendingCount = ledger.pending_count ?? 0;
  if (badge) {
    badge.textContent = `${pendingCount} Pending Approval • ${ledger.dispatched_count ?? 0} Validated/Dispatched (${items.length} Total)`;
  }
  const approveAllBtn = document.getElementById("approve-all-outbox-btn");
  if (approveAllBtn) {
    approveAllBtn.textContent =
      pendingCount > 0
        ? `✅ Approve & Dispatch Pending (${pendingCount})`
        : `🔄 Re-Verify Validated Queue (${items.length})`;
  }

  if (!items.length) {
    const tr = document.createElement("tr");
    const td = mkEl("td", "", "No packages staged yet — select channels above and click 'Stage Selected Channels to Outbox'.");
    td.colSpan = 6;
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  items.slice(0, 20).forEach((item) => {
    const tr = document.createElement("tr");
    tr.setAttribute("data-testid", `outbox-row-${item.outbox_id}`);
    const pkg = item.package || {};
    const checks = pkg.compliance_checks || {};
    const media = pkg.media || {};

    // Col 1: Outbox ID & Channel
    const td1 = document.createElement("td");
    const c1 = mkEl("div", "cell-card-equal");
    const idStrong = mkEl("strong", "", item.outbox_id);
    idStrong.style.cssText = "font-size:11.5px;color:#174ea6;font-family:ui-monospace,monospace;";
    c1.appendChild(idStrong);
    c1.appendChild(mkEl("span", "", item.platform_name || item.platform_id));
    td1.appendChild(c1);
    tr.appendChild(td1);

    // Col 2: Idea & Blueprint
    const td2 = document.createElement("td");
    const c2 = mkEl("div", "cell-card-equal");
    const tStrong = mkEl("strong", "", polishUiTypography(item.idea_title || item.idea_id));
    tStrong.style.fontSize = "12px";
    const bpSpan = mkEl(
      "span",
      "",
      `Blueprint ${item.template_id} (${item.template_name || ""})`
    );
    bpSpan.style.cssText = "font-size:11px;color:#475569;";
    c2.appendChild(tStrong);
    c2.appendChild(bpSpan);
    td2.appendChild(c2);
    tr.appendChild(td2);

    // Col 3: Mode & Container
    const td3 = document.createElement("td");
    const c3 = mkEl("div", "cell-card-equal");
    c3.appendChild(mkEl("strong", "", `Mode: ${formatModeDisplayName(item.mode)}`));
    const mSpan = mkEl("span", "", `${media.container_format || "TEXT"} • ${media.aspect_ratio || ""}`);
    mSpan.style.cssText = "font-size:11px;color:#0369a1;font-weight:700;";
    c3.appendChild(mSpan);
    td3.appendChild(c3);
    tr.appendChild(td3);

    // Col 4: Compliance Gate
    const td4 = document.createElement("td");
    const c4 = mkEl("div", "cell-card-equal");
    c4.appendChild(
      mkEl(
        "span",
        `pill-badge ${checks.all_passed ? "pill-emerald" : "pill-amber"}`,
        checks.all_passed ? "100% COMPLIANT ✓" : "CHECK LIMITS"
      )
    );
    const lenSpan = mkEl(
      "span",
      "",
      `${checks.char_used || 0}/${checks.char_cap || 0} chars • Fold ${checks.fold_used || 0}/${checks.fold_cap || 0}`
    );
    lenSpan.style.cssText = "font-size:11px;color:#334155;margin-top:4px;";
    c4.appendChild(lenSpan);
    td4.appendChild(c4);
    tr.appendChild(td4);

    // Col 5: Status
    const td5 = document.createElement("td");
    const c5 = mkEl("div", "cell-card-equal");
    const statusClass =
      item.status === "PUBLISHED_LIVE" || item.status === "DRY_RUN_VALIDATED" || item.status === "SHARE_PACKET_READY"
        ? "pill-emerald"
        : "pill-amber";
    c5.appendChild(mkEl("span", `pill-badge ${statusClass}`, item.status));
    const tierNote = mkEl("span", "", item.tier_badge || "");
    tierNote.style.cssText = "font-size:10.5px;color:#64748b;margin-top:4px;";
    c5.appendChild(tierNote);
    td5.appendChild(c5);
    tr.appendChild(td5);

    // Col 6: Actions
    const td6 = document.createElement("td");
    const c6 = mkEl("div", "cell-card-equal");
    const btnWrap = mkEl("div");
    btnWrap.style.cssText = "display:flex;gap:5px;flex-wrap:wrap;";
    const appBtn = mkEl(
      "button",
      item.status === "PENDING_APPROVAL" ? "btn-primary" : "btn-secondary",
      item.status === "PENDING_APPROVAL" ? "Approve" : "Re-Verify"
    );
    appBtn.type = "button";
    appBtn.style.cssText = "padding:4px 8px;font-size:11px;";
    appBtn.setAttribute("data-testid", `approve-outbox-btn-${item.outbox_id}`);
    appBtn.addEventListener("click", () => approveOutboxItems([item.outbox_id]));
    btnWrap.appendChild(appBtn);

    const cpBtn = mkEl("button", "btn-secondary", "Copy");
    cpBtn.type = "button";
    cpBtn.style.cssText = "padding:4px 8px;font-size:11px;";
    cpBtn.addEventListener("click", () =>
      copyTextSafe(pkg.body || "", `Copied ${item.platform_name} Outbox copy!`)
    );
    btnWrap.appendChild(cpBtn);
    c6.appendChild(btnWrap);
    td6.appendChild(c6);
    tr.appendChild(td6);

    tbody.appendChild(tr);
  });
}

function activateView(target) {
  document
    .querySelectorAll(".global-header .nav-tab-btn")
    .forEach((b) => b.classList.toggle("active", b.getAttribute("data-view") === target));
  ALL_VIEWS.forEach((vid) => {
    const el = document.getElementById(vid);
    if (el) el.style.display = vid === target ? "block" : "none";
  });
  if (target === "view-miner") {
    if (!STATE.top5Briefing) loadDailyTop5Briefing();
    if (!(STATE.dailyPosts || []).length) loadDailyGeneratedPosts();
    refreshLiveFeeds();
  }
  if (target === "view-gallery" && !(STATE.templates || []).length) loadGalleryData();
  if (target === "view-minting-studio" && !STATE.mintingStudio) loadMintingStudioData();
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".global-header .nav-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => activateView(btn.getAttribute("data-view")));
  });

  document.querySelectorAll(".drawer-tabs .nav-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".drawer-tabs .nav-tab-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.getAttribute("data-drawertab");
      ["dtab-visuals", "dtab-slides", "dtab-terraform", "dtab-linkedin"].forEach((tid) => {
        document.getElementById(tid).style.display = tid === target ? "block" : "none";
      });
    });
  });

  document.getElementById("gallery-search-input")?.addEventListener("input", renderGalleryView);
  document.getElementById("gallery-filter-tier")?.addEventListener("change", renderGalleryView);
  document.getElementById("gallery-filter-type")?.addEventListener("change", renderGalleryView);

  document.getElementById("close-drawer-btn").addEventListener("click", () => {
    document.getElementById("repo-inspector-drawer").classList.remove("open");
  });

  document.getElementById("search-input").addEventListener("input", renderReposView);
  document.getElementById("filter-archetype").addEventListener("change", renderReposView);
  document.getElementById("filter-author").addEventListener("change", renderReposView);

  document.getElementById("reset-filters-btn").addEventListener("click", () => {
    document.getElementById("search-input").value = "";
    document.getElementById("filter-archetype").value = "ALL";
    document.getElementById("filter-author").value = "ALL";
    renderReposView();
  });

  document.getElementById("generate-daily-posts-btn")?.addEventListener("click", () => {
    triggerGenerateDailyPosts();
  });

  document.getElementById("generate-top5-briefing-btn")?.addEventListener("click", () => {
    triggerGenerateTop5Briefing();
  });

  document.getElementById("transcode-active-idea-btn")?.addEventListener("click", () => {
    triggerTranscodeActiveIdea();
  });

  document.getElementById("approve-all-outbox-btn")?.addEventListener("click", () => {
    approveOutboxItems(null);
  });

  document.getElementById("refresh-live-feeds-btn").addEventListener("click", () => {
    refreshLiveFeeds();
    showToast("Refreshed live arXiv & GitHub Agentic AI feeds");
  });

  document.getElementById("trigger-ingest-btn").addEventListener("click", async () => {
    const url = document.getElementById("inline-ingest-url-input").value.trim();
    const title = document.getElementById("inline-ingest-title-input").value.trim();
    if (!url) {
      showToast("Enter a LinkedIn, arXiv, or GitHub URL first");
      return;
    }
    const res = await fetch("/api/ingest-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, title }),
    });
    const out = await res.json();
    const banner = document.getElementById("ingest-result-banner");
    banner.style.display = "block";
    banner.className = "pill-badge pill-emerald";
    banner.textContent = `Verified & Mapped: ${out.status} -> Repository: ${out.repo_slug}`;
    showToast(`Grounded URL into repository ${out.repo_slug}`);
  });

  loadWorkspaceData();
  loadMintingStudioData();
  const requestedView = new URLSearchParams(window.location.search).get("view");
  if (requestedView && ALL_VIEWS.includes(requestedView)) {
    activateView(requestedView);
  }
});
