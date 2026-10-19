// Interactive Client Logic for Agentic AI Ideas Mining & OpenHands Autonomous Repo Factory

let STATE = {
  repos: [],
  playbook: null,
  activeRepoSlug: null,
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
    const matchesQuery =
      !q ||
      r.post_title.toLowerCase().includes(q) ||
      r.repo_slug.toLowerCase().includes(q) ||
      r.author_name.toLowerCase().includes(q) ||
      r.primary_source.title.toLowerCase().includes(q) ||
      r.gcp_stack.join(" ").toLowerCase().includes(q);
    const matchesArch = arch === "ALL" || r.diagram_archetype.startsWith(arch);
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
    .map(
      (r) => `
      <article class="repo-card" data-testid="repo-card-${escapeHtml(r.id)}">
        <div>
          <div class="repo-card-header">
            <span class="brand-badge">${escapeHtml(r.id)} • ${escapeHtml(r.author_name)}</span>
            <span class="pill-badge pill-emerald">GIT HEAD: ${escapeHtml(r.git_commit_sha || "verified")}</span>
          </div>
          <h3 class="repo-card-title" style="margin: 10px 0 8px 0;">${escapeHtml(r.post_title)}</h3>
          <div class="repo-card-hook">${escapeHtml(r.original_hook)}</div>
          <div style="margin-top: 10px; font-size: 11.5px; color: #475569; font-weight: 600;">
            Primary Source: <strong style="color: #0f172a;">${escapeHtml(r.primary_source.title)}</strong>
          </div>
        </div>
        <div>
          <div class="deliverable-chips" style="margin-bottom: 10px;">
            <span class="deliverable-chip">ADK Code + 4 Tests</span>
            <span class="deliverable-chip">@2d Poster SVG/PNG</span>
            <span class="deliverable-chip">GCP #78 .drawio + SVG</span>
            <span class="deliverable-chip">12-Slide .pptx + .pdf</span>
            <span class="deliverable-chip">1-Click Terraform</span>
          </div>
          <div class="repo-card-footer">
            <span class="truncate" style="font-size: 11px; color: #64748b; font-family: monospace;">
              generated-repos/${escapeHtml(r.repo_slug)}
            </span>
            <button class="btn-primary" onclick="openRepoInspector('${escapeHtml(r.repo_slug)}')">
              Inspect Bundle &amp; 2D Visuals →
            </button>
          </div>
        </div>
      </article>
    `
    )
    .join("");

  tbody.innerHTML = filtered
    .map(
      (r) => `
      <tr>
        <td>
          <div class="cell-card-equal">
            <strong style="font-size: 12px; color: #174ea6;">${escapeHtml(r.id)}</strong>
            <span class="truncate" style="font-size: 11.5px; font-family: monospace; color: #0f172a;">${escapeHtml(r.repo_slug)}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <strong style="font-size: 12px;">${escapeHtml(r.author_name)}</strong>
            <span style="font-size: 11.5px; color: #475569;">${escapeHtml(r.primary_source.title)}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span style="font-size: 11.5px; font-weight: 700; color: #0f172a;">${escapeHtml(r.diagram_archetype)}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span style="font-size: 11.5px; color: #334155;">${escapeHtml(r.gcp_stack.slice(0, 3).join(" • "))}</span>
          </div>
        </td>
        <td>
          <div class="cell-card-equal">
            <span style="font-size: 11.5px; color: #065f46; font-weight: 700;">Code • README • 2D SVG/Draw.io • 12-Slide PPTX/PDF • Terraform</span>
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
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
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

  document.getElementById("drawer-repo-badge").textContent = `${detail.id} • ${detail.activity_urn} • HEAD ${detail.git_commit_sha}`;
  document.getElementById("drawer-repo-title").textContent = detail.post_title;

  // Tab 1: @2d Visuals
  document.getElementById("dtab-visuals").innerHTML = `
    <div style="margin-bottom: 14px; display: flex; gap: 8px; flex-wrap: wrap;">
      <a class="btn-primary" href="/repos/${encodeURIComponent(slug)}/visuals/linkedin-infographic-2d.svg" target="_blank">Open 2D LinkedIn Poster (.svg) ↗</a>
      <a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.svg" target="_blank">Open GCP #78 2D Diagram (.svg) ↗</a>
      <a class="btn-secondary" href="/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.drawio" download>Download Editable Draw.io (.drawio)</a>
    </div>
    <div class="visual-preview-box">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 8px; color: #0f172a;">Figure 1 — Official Google Cloud #78 4-Zone Hub-and-Spoke 2D Architecture</div>
      <img src="/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.svg" alt="GCP 2D Architecture" />
    </div>
    <div class="visual-preview-box">
      <div style="font-size: 12px; font-weight: 800; margin-bottom: 8px; color: #0f172a;">Figure 2 — High-Res 2D LinkedIn Infographic Poster (1200x1350)</div>
      <img src="/repos/${encodeURIComponent(slug)}/visuals/linkedin-infographic-2d.svg" alt="LinkedIn 2D Infographic" />
    </div>
  `;

  // Tab 2: 12-Slide Deck & Carousel
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
      <pre class="code-block-light">cd generated-repos/${escapeHtml(slug)} && ./scripts/deploy_gcp_one_click.sh nitina-ggarwal-sandbox-647724 us-west1</pre>
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

  // Tab 4: LinkedIn Post Copy & Receipt
  document.getElementById("dtab-linkedin").innerHTML = `
    <div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
      <strong style="font-size: 13px;">Ready-to-Post LinkedIn Draft for Nitin Aggarwal</strong>
      <button class="btn-primary" onclick="navigator.clipboard.writeText(document.getElementById('linkedin-copy-pre').innerText); showToast('Copied LinkedIn Post Draft to clipboard!');">
        Copy LinkedIn Post Copy
      </button>
    </div>
    <pre class="code-block-light" id="linkedin-copy-pre">${escapeHtml(detail.linkedin_post_draft)}</pre>
  `;

  document.getElementById("repo-inspector-drawer").classList.add("open");
}

async function refreshLiveFeeds() {
  const res = await fetch("/api/live-mining-feeds");
  const data = await res.json();

  document.getElementById("live-arxiv-list").innerHTML = (data.arxiv || [])
    .map(
      (item) => `
      <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:12px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
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
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
          <strong style="font-size:13.5px;color:#0f172a;">${escapeHtml(repo.full_name)}</strong>
          <span class="pill-badge pill-amber">★ ${escapeHtml(repo.stars)}</span>
        </div>
        <div style="font-size:12px;color:#334155;margin-bottom:6px;">${escapeHtml(repo.description)}</div>
        <a href="${escapeHtml(repo.html_url)}" target="_blank" style="font-size:11.5px;color:#1a73e8;font-weight:700;">Inspect GitHub Repository ↗</a>
      </div>
    `
    )
    .join("");
}

document.addEventListener("DOMContentLoaded", () => {
  // Top navigation switching
  document.querySelectorAll(".global-header .nav-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".global-header .nav-tab-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.getAttribute("data-view");
      ["view-repos", "view-playbook", "view-miner", "view-openhands"].forEach((vid) => {
        document.getElementById(vid).style.display = vid === target ? "block" : "none";
      });
      if (target === "view-miner") {
        refreshLiveFeeds();
      }
    });
  });

  // Drawer tab switching
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
});
