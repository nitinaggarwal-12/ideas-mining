// Ideas Minting Studio — Multi-Persona Interactive Client Controller (v3.0)
// Pure DOM construction (createElement / textContent / replaceChildren) across all dynamic views.

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

function polishUiTypography(str) {
  return String(str || "")
    .replace(/pass\^k/g, "passᵏ")
    .replace(/pass\^3/g, "pass³")
    .replace(/pass\^5/g, "pass⁵");
}

const ALL_VIEWS = [
  "view-miner",
  "view-gallery",
  "view-repos",
  "view-minting-studio",
  "view-playbook",
  "view-openhands",
];

const MINER_PANELS = [
  "miner-panel-composer",
  "miner-panel-outbox",
  "miner-panel-radar",
];

const PLAYBOOK_PANELS = [
  "playbook-panel-posts",
  "playbook-panel-creators",
  "playbook-panel-platforms",
  "playbook-panel-archetypes",
];

const STATE = {
  persona: "creator",
  repoLayout: "cards",
  activeView: "view-miner",
  activeMinerPanel: "miner-panel-composer",
  activePlaybookPanel: "playbook-panel-posts",
  activeOmnichannelPlatformId: "x_twitter",
  repos: [],
  playbook: null,
  activeRepoSlug: null,
  templates: [],
  pairings: [],
  mintingStudio: null,
  dailyPosts: [],
  dailyEditionDate: "",
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
  activeCarouselIndex: 0,
  mockupCopyExpanded: false,
  showSafeZoneOverlay: true,
  cmdkActiveIdx: 0,
  cmdkFilteredItems: [],
  lastCopiedText: "",
};

function showToast(msg) {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const el = mkEl("div", "toast-item", msg);
  container.appendChild(el);
  setTimeout(() => {
    el.remove();
  }, 3400);
}

async function copyTextSafe(text, toastMessage) {
  const val = String(text ?? "");
  let copied = false;
  try {
    if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(val);
      copied = true;
    }
  } catch (_) {
    copied = false;
  }
  if (!copied) {
    try {
      const ta = document.createElement("textarea");
      ta.value = val;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:fixed;left:-9999px;top:0;opacity:0;";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    } catch (_) {
      // Headless fallback
    }
  }
  STATE.lastCopiedText = val;
  window.__LAST_COPIED_TEXT__ = val;
  showToast(toastMessage || "Copied to clipboard!");
}

function syncUrlState() {
  try {
    const nextUrl = new URL(window.location.href);
    nextUrl.searchParams.set("view", STATE.activeView);
    if (STATE.persona && STATE.persona !== "creator") {
      nextUrl.searchParams.set("persona", STATE.persona);
    } else {
      nextUrl.searchParams.delete("persona");
    }
    window.history.replaceState(null, "", `${nextUrl.pathname}${nextUrl.search}`);
  } catch (_) {
    // Ignore history state errors
  }
}

/* ==========================================================================
   Persona Switcher, Lightbox & Command Palette (⌘K)
   ========================================================================== */
function setPersonaMode(mode) {
  const valid = ["creator", "executive", "builder"];
  const next = valid.includes(mode) ? mode : "creator";
  STATE.persona = next;
  document.body.setAttribute("data-persona", next);
  document.querySelectorAll("[data-persona].persona-radio").forEach((btn) => {
    const isAct = btn.getAttribute("data-persona") === next;
    btn.classList.toggle("active", isAct);
    btn.setAttribute("aria-checked", isAct ? "true" : "false");
  });
  syncUrlState();
  renderTop5EditorialDesk();
  renderGalleryView();
  renderReposView();
  renderPlaybookView();
  renderMintingStudioView();
}

function setRepoLayoutMode(layout) {
  const next = layout === "matrix" ? "matrix" : "cards";
  STATE.repoLayout = next;
  document.body.setAttribute("data-repo-layout", next);
  document.querySelectorAll("[data-repo-layout]").forEach((btn) => {
    const isAct = btn.getAttribute("data-repo-layout") === next;
    btn.classList.toggle("active", isAct);
    btn.setAttribute("aria-checked", isAct ? "true" : "false");
  });
}

function openLightbox({ kicker, title, imgUrl, actions = [] }) {
  const backdrop = document.getElementById("lightbox-backdrop");
  const kickerEl = document.getElementById("lightbox-kicker");
  const titleEl = document.getElementById("lightbox-title");
  const imgEl = document.getElementById("lightbox-img");
  const actionsEl = document.getElementById("lightbox-actions");
  if (!backdrop || !imgEl || !actionsEl) return;

  if (kickerEl) kickerEl.textContent = kicker || "CERTIFIED BLUEPRINT";
  if (titleEl) titleEl.textContent = polishUiTypography(title || "Blueprint Preview");
  imgEl.src = safeUrl(imgUrl);
  imgEl.alt = polishUiTypography(title || "Blueprint Preview");

  actionsEl.replaceChildren();
  actions.forEach((act) => {
    if (!act || !act.href) return;
    const a = mkEl("a", act.primary ? "btn-primary" : "btn-secondary", act.label);
    a.href = safeUrl(act.href);
    if (act.download) {
      a.setAttribute("download", act.download);
    } else {
      a.target = "_blank";
      a.rel = "noopener";
    }
    actionsEl.appendChild(a);
  });

  const closeBtn = mkEl("button", "btn-secondary", "Close ✕");
  closeBtn.type = "button";
  closeBtn.setAttribute("aria-label", "Close blueprint preview");
  closeBtn.addEventListener("click", closeLightbox);
  actionsEl.appendChild(closeBtn);

  backdrop.style.display = "flex";
  closeBtn.focus();
}

function closeLightbox() {
  const backdrop = document.getElementById("lightbox-backdrop");
  if (backdrop) backdrop.style.display = "none";
}

function buildCmdkCatalog() {
  const items = [];
  (STATE.top5Briefing?.ideas || []).forEach((idea, idx) => {
    items.push({
      kind: `Daily #${idx + 1}`,
      title: polishUiTypography(idea.title),
      sub: `${idea.cluster_label} · Demand ${idea.scores?.demand_score ?? 95}`,
      run: async () => {
        activateView("view-miner");
        activateMinerPanel("miner-panel-composer");
        STATE.selectedIdeaId = idea.id;
        STATE.selectedTemplateId = idea.default_template_id;
        STATE.selectedMode = idea.default_recommended_mode || "Carousel";
        renderTop5EditorialDesk();
        await refreshPlatformPreviewPackages();
      },
    });
  });

  (STATE.templates || []).slice(0, 116).forEach((t) => {
    items.push({
      kind: `Blueprint ${t.id}`,
      title: `${t.id} — ${t.name}`,
      sub: `${t.quality_tier || "Best"} Tier · ${(t.content_types || []).slice(0, 2).join(", ")}`,
      run: () => jumpToTemplateInGallery(t.id),
    });
  });

  (STATE.repos || []).forEach((r) => {
    items.push({
      kind: `Repo ${r.id}`,
      title: r.post_title,
      sub: `generated-repos/${r.repo_slug}`,
      run: () => {
        activateView("view-repos");
        openRepoInspector(r.repo_slug);
      },
    });
  });

  (STATE.mintingStudio?.topics || []).forEach((m) => {
    items.push({
      kind: `Deck ${m.id}`,
      title: `${m.id} — ${m.title}`,
      sub: `Mnemonic ${m.mnemonic} · Blueprint ${m.canonical_template_id}`,
      run: () => activateView("view-minting-studio"),
    });
  });

  (STATE.playbook?.creator_profiles || []).forEach((cp) => {
    items.push({
      kind: "Creator",
      title: cp.name,
      sub: `${cp.role} · Blueprint ${cp.template_id}`,
      run: () => {
        activateView("view-playbook");
        activatePlaybookPanel("playbook-panel-creators");
        openCreatorPortfolioDrawer(cp.name);
      },
    });
  });

  (STATE.playbook?.reviewed_posts || []).forEach((rp) => {
    if (rp.availability !== "PUBLIC_VERIFIED") return;
    items.push({
      kind: rp.post_code,
      title: `${rp.author_name} — ${rp.hook_line_1}`,
      sub: `${rp.reactions.toLocaleString()} reactions · ${rp.comments} comments · ${rp.presentation_archetype_code}`,
      run: () => {
        activateView("view-playbook");
        activatePlaybookPanel("playbook-panel-posts");
        openPostAnatomyDrawer(rp.activity_id);
      },
    });
  });

  (STATE.playbook?.omnichannel_platforms || []).forEach((plat) => {
    items.push({
      kind: "Platform",
      title: `${plat.name} Playbook`,
      sub: plat.badge,
      run: () => {
        activateView("view-playbook");
        activatePlaybookPanel("playbook-panel-platforms");
        STATE.activeOmnichannelPlatformId = plat.id;
        renderOmnichannelPlaybooks();
      },
    });
  });

  return items;
}

function renderCmdkResults() {
  const listEl = document.getElementById("cmdk-results-list");
  const q = (document.getElementById("cmdk-search-input")?.value || "").trim().toLowerCase();
  if (!listEl) return;
  listEl.replaceChildren();

  const all = buildCmdkCatalog();
  const filtered = all
    .filter((item) => !q || `${item.kind} ${item.title} ${item.sub}`.toLowerCase().includes(q))
    .slice(0, 18);

  STATE.cmdkFilteredItems = filtered;
  if (STATE.cmdkActiveIdx >= filtered.length) STATE.cmdkActiveIdx = 0;

  if (!filtered.length) {
    const empty = mkEl("div", "", "No matching ideas, blueprints, repositories, or creators.");
    empty.style.cssText = "padding:18px;text-align:center;color:#475569;font-size:13px;";
    listEl.appendChild(empty);
    return;
  }

  filtered.forEach((item, idx) => {
    const btn = mkEl("button", `cmdk-result-item${idx === STATE.cmdkActiveIdx ? " active" : ""}`);
    btn.type = "button";
    btn.setAttribute("role", "option");
    btn.setAttribute("aria-selected", idx === STATE.cmdkActiveIdx ? "true" : "false");

    const left = mkEl("div", "min-w-0");
    const tEl = mkEl("div", "", item.title);
    tEl.style.cssText = "font-size:13px;font-weight:700;color:#0f172a;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;";
    const sEl = mkEl("div", "", item.sub);
    sEl.style.cssText = "font-size:11.5px;color:#475569;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;";
    left.appendChild(tEl);
    left.appendChild(sEl);

    btn.appendChild(left);
    btn.appendChild(mkEl("span", "cmdk-result-kind", item.kind));
    btn.addEventListener("click", () => {
      closeCmdk();
      item.run();
    });
    listEl.appendChild(btn);
  });
}

async function openCmdk() {
  const backdrop = document.getElementById("cmdk-backdrop");
  const input = document.getElementById("cmdk-search-input");
  if (!backdrop || !input) return;
  if (!(STATE.templates || []).length) {
    loadGalleryData();
  }
  backdrop.style.display = "flex";
  input.value = "";
  STATE.cmdkActiveIdx = 0;
  renderCmdkResults();
  input.focus();
}

function closeCmdk() {
  const backdrop = document.getElementById("cmdk-backdrop");
  if (backdrop) backdrop.style.display = "none";
}

/* ==========================================================================
   View & Sub-View Navigation + Roving Keyboard Support
   ========================================================================== */
function activateMinerPanel(panelId) {
  const next = MINER_PANELS.includes(panelId) ? panelId : "miner-panel-composer";
  STATE.activeMinerPanel = next;
  document.querySelectorAll("[data-miner-panel]").forEach((btn) => {
    const isAct = btn.getAttribute("data-miner-panel") === next;
    btn.classList.toggle("active", isAct);
    btn.setAttribute("aria-selected", isAct ? "true" : "false");
  });
  MINER_PANELS.forEach((pid) => {
    const el = document.getElementById(pid);
    if (el) el.style.display = pid === next ? "block" : "none";
  });
}

function activateView(target) {
  const next = ALL_VIEWS.includes(target) ? target : "view-miner";
  STATE.activeView = next;
  document.querySelectorAll(".global-header .nav-tab-btn").forEach((b) => {
    const isAct = b.getAttribute("data-view") === next;
    b.classList.toggle("active", isAct);
    b.setAttribute("aria-selected", isAct ? "true" : "false");
  });
  ALL_VIEWS.forEach((vid) => {
    const el = document.getElementById(vid);
    if (el) el.style.display = vid === next ? "block" : "none";
  });
  syncUrlState();

  if (next === "view-miner") {
    if (!STATE.top5Briefing) loadDailyTop5Briefing();
    if (!(STATE.dailyPosts || []).length) loadDailyGeneratedPosts();
    refreshLiveFeeds();
  }
  if (next === "view-gallery" && !(STATE.templates || []).length) {
    loadGalleryData();
  }
  if (next === "view-minting-studio" && !STATE.mintingStudio) {
    loadMintingStudioData();
  }
}

function wireRovingKeyboardGroup(containerSelector, itemSelector) {
  const container = document.querySelector(containerSelector);
  if (!container) return;
  container.addEventListener("keydown", (ev) => {
    if (!["ArrowRight", "ArrowLeft", "Home", "End"].includes(ev.key)) return;
    const items = Array.from(container.querySelectorAll(itemSelector));
    if (!items.length) return;
    const idx = items.indexOf(document.activeElement);
    if (idx === -1) return;
    ev.preventDefault();
    let nextIdx = idx;
    if (ev.key === "ArrowRight") nextIdx = (idx + 1) % items.length;
    if (ev.key === "ArrowLeft") nextIdx = (idx - 1 + items.length) % items.length;
    if (ev.key === "Home") nextIdx = 0;
    if (ev.key === "End") nextIdx = items.length - 1;
    items[nextIdx].focus();
    items[nextIdx].click();
  });
}

/* ==========================================================================
   View 1: 19 Verified Google Cloud ADK Repositories & Inspector Drawer
   ========================================================================== */
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
  if (!grid || !tbody || !emptyState) return;

  grid.replaceChildren();
  tbody.replaceChildren();

  if (filtered.length === 0) {
    emptyState.style.display = "block";
    return;
  }
  emptyState.style.display = "none";

  filtered.forEach((r) => {
    const plan = r.template_and_distribution_plan || null;
    const card = mkEl("article", "repo-card");
    card.setAttribute("data-testid", `repo-card-${r.id}`);

    const topGroup = mkEl("div");
    const artStage = mkEl("div", "card-artwork-stage");
    artStage.style.marginBottom = "12px";
    const imgUrl = `/repos/${encodeURIComponent(r.repo_slug)}/visuals/${plan ? "lead-template.svg" : "dynamic-solution-flow.svg"}?v=20261104`;
    const img = document.createElement("img");
    img.src = imgUrl;
    img.alt = `${r.post_title} solution architecture`;
    img.loading = "lazy";
    artStage.appendChild(img);
    artStage.appendChild(mkEl("span", "card-zoom-pill", "Inspect Bundle →"));
    artStage.addEventListener("click", () => openRepoInspector(r.repo_slug));
    topGroup.appendChild(artStage);

    const hdr = mkEl("div", "repo-card-header");
    hdr.style.marginBottom = "6px";
    hdr.appendChild(mkEl("span", "brand-badge", `${r.id} · ${r.author_name}`));
    if (STATE.persona === "builder") {
      hdr.appendChild(
        mkEl(
          "span",
          "pill-badge pill-emerald tabular-nums",
          `${plan ? plan.primary_template_id + " · " : ""}${r.git_commit_sha || "verified"}`
        )
      );
    } else if (plan) {
      hdr.appendChild(mkEl("span", "pill-badge pill-sky", `Blueprint ${plan.primary_template_id}`));
    }
    topGroup.appendChild(hdr);

    const titleEl = mkEl("h3", "repo-card-title", polishUiTypography(r.post_title));
    titleEl.style.marginBottom = "6px";
    topGroup.appendChild(titleEl);

    topGroup.appendChild(
      mkEl("p", "repo-card-hook", polishUiTypography(r.daily_problem_short || r.original_hook))
    );

    if (STATE.persona === "builder") {
      const srcLine = mkEl("div", "", `Source: ${r.primary_source?.title || ""}`);
      srcLine.style.cssText = "margin-top:8px;font-size:11.5px;color:#475569;font-weight:600;";
      topGroup.appendChild(srcLine);
    }
    card.appendChild(topGroup);

    const bottomGroup = mkEl("div");
    const chips = mkEl("div", "deliverable-chips");
    chips.style.marginBottom = "10px";
    if (r.flagship_24slide_url) {
      chips.appendChild(mkEl("span", "deliverable-chip chip-emerald", "24-Slide Google Slides"));
    }
    chips.appendChild(mkEl("span", "deliverable-chip chip-blue", "Moving-Arrow SVG/GIF"));
    chips.appendChild(mkEl("span", "deliverable-chip", "12-Slide PPTX"));
    chips.appendChild(mkEl("span", "deliverable-chip", "ADK + Terraform"));
    bottomGroup.appendChild(chips);

    const footer = mkEl("div", "repo-card-footer");
    const slugSpan = mkEl("span", "truncate builder-only-inline", r.repo_slug);
    slugSpan.style.cssText = "font-size:11.5px;color:#475569;font-family:var(--theme-font-mono,monospace);max-width:140px;";
    footer.appendChild(slugSpan);

    const btnRow = mkEl("div", "studio-toolbar-actions");
    if (r.flagship_24slide_url) {
      const deckLink = mkEl("a", "btn-secondary", "24-Slide Deck ↗");
      deckLink.href = safeUrl(r.flagship_24slide_url);
      deckLink.target = "_blank";
      deckLink.rel = "noopener";
      btnRow.appendChild(deckLink);
    }
    const inspectBtn = mkEl("button", "btn-primary", "Inspect Bundle →");
    inspectBtn.type = "button";
    inspectBtn.setAttribute("data-testid", `inspect-repo-btn-${r.id}`);
    inspectBtn.addEventListener("click", () => openRepoInspector(r.repo_slug));
    btnRow.appendChild(inspectBtn);
    footer.appendChild(btnRow);
    bottomGroup.appendChild(footer);

    card.appendChild(bottomGroup);
    grid.appendChild(card);

    // Populate Matrix Row
    const tr = document.createElement("tr");
    const td1 = document.createElement("td");
    const c1 = mkEl("div", "cell-card-equal");
    const idStrong = mkEl("strong", "", `${r.id} (${r.est_post_time || "Verified"})`);
    idStrong.style.cssText = "font-size:12px;color:#1e40af;";
    const slugCell = mkEl("span", "truncate", r.repo_slug);
    slugCell.style.cssText = "font-size:11.5px;font-family:var(--theme-font-mono,monospace);color:#0f172a;";
    c1.appendChild(idStrong);
    c1.appendChild(slugCell);
    td1.appendChild(c1);

    const td2 = document.createElement("td");
    const c2 = mkEl("div", "cell-card-equal");
    c2.appendChild(mkEl("strong", "", r.daily_problem_short || r.author_name));
    const srcSpan = mkEl("span", "", r.primary_source?.title || "");
    srcSpan.style.cssText = "font-size:11.5px;color:#475569;";
    c2.appendChild(srcSpan);
    td2.appendChild(c2);

    const td3 = document.createElement("td");
    const c3 = mkEl("div", "cell-card-equal");
    c3.appendChild(mkEl("span", "", "Moving-Arrow SVG/GIF · GCP #78 Draw.io"));
    td3.appendChild(c3);

    const td4 = document.createElement("td");
    const c4 = mkEl("div", "cell-card-equal");
    c4.appendChild(mkEl("span", "", (r.gcp_stack || []).slice(0, 3).join(" · ")));
    td4.appendChild(c4);

    const td5 = document.createElement("td");
    const c5 = mkEl("div", "cell-card-equal");
    c5.appendChild(
      mkEl(
        "span",
        "",
        `${r.flagship_24slide_url ? "24-Slide Deck + Video · " : ""}ADK Code · 12-Slide PPTX · Terraform`
      )
    );
    td5.appendChild(c5);

    const td6 = document.createElement("td");
    const c6 = mkEl("div", "cell-card-equal");
    c6.appendChild(mkEl("span", "pill-badge pill-emerald tabular-nums", `PASS (${r.git_commit_sha || "ok"})`));
    td6.appendChild(c6);

    tr.append(td1, td2, td3, td4, td5, td6);
    tbody.appendChild(tr);
  });
}

async function openRepoInspector(slug) {
  STATE.activeRepoSlug = slug;
  const res = await fetch(`/api/repo-detail/${encodeURIComponent(slug)}`);
  const detail = await res.json();

  const badgeEl = document.getElementById("drawer-repo-badge");
  const titleEl = document.getElementById("drawer-repo-title");
  if (badgeEl) {
    badgeEl.textContent = `${detail.id} · ${detail.est_post_time || detail.activity_urn || "Verified"} · HEAD ${detail.git_commit_sha}`;
  }
  if (titleEl) {
    titleEl.textContent = polishUiTypography(detail.post_title);
  }

  const plan = detail.template_and_distribution_plan || null;

  // Tab 1: Visuals
  const visTab = document.getElementById("dtab-visuals");
  if (visTab) {
    visTab.replaceChildren();
    const actBar = mkEl("div", "studio-toolbar-actions");
    actBar.style.marginBottom = "14px";
    if (detail.flagship_24slide_url) {
      const a = mkEl("a", "btn-primary", "Open 24-Slide Google Slides ↗");
      a.href = safeUrl(detail.flagship_24slide_url);
      a.target = "_blank";
      a.rel = "noopener";
      actBar.appendChild(a);
    }
    if (plan) {
      const aSvg = mkEl("a", "btn-secondary", `Open Blueprint ${plan.primary_template_id} (.svg) ↗`);
      aSvg.href = `/repos/${encodeURIComponent(slug)}/visuals/lead-template.svg?v=20261104`;
      aSvg.target = "_blank";
      actBar.appendChild(aSvg);
    }
    const aFlow = mkEl("a", "btn-secondary", "Moving-Arrow SVG ↗");
    aFlow.href = `/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.svg?v=20261104`;
    aFlow.target = "_blank";
    actBar.appendChild(aFlow);

    const aDrawio = mkEl("a", "btn-secondary", "Editable .drawio");
    aDrawio.href = `/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.drawio?v=20261104`;
    aDrawio.setAttribute("download", "");
    actBar.appendChild(aDrawio);
    visTab.appendChild(actBar);

    const figures = [];
    if (plan) {
      figures.push([
        `Paired Blueprint (${plan.primary_template_id}: ${plan.primary_template_name})`,
        `/repos/${encodeURIComponent(slug)}/visuals/lead-template.svg?v=20261104`,
      ]);
    }
    figures.push(
      [
        "Figure 1 — Problem → 4-Step Moving-Arrow Solution Flow",
        `/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.svg?v=20261104`,
      ],
      [
        "Figure 2 — Google Cloud #78 4-Zone Hub-and-Spoke Architecture",
        `/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.svg?v=20261104`,
      ],
      [
        "Figure 3 — High-Resolution 2D Infographic Poster",
        `/repos/${encodeURIComponent(slug)}/visuals/linkedin-infographic-2d.svg?v=20261104`,
      ]
    );

    figures.forEach(([caption, src]) => {
      const box = mkEl("div", "visual-preview-box");
      const cap = mkEl("div", "", caption);
      cap.style.cssText = "font-size:12.5px;font-weight:700;color:#0f172a;margin-bottom:8px;";
      const im = document.createElement("img");
      im.src = src;
      im.alt = caption;
      box.append(cap, im);
      visTab.appendChild(box);
    });

    const promptBox = mkEl("div", "visual-preview-box");
    const pHdr = mkEl("div", "composer-section-hdr");
    pHdr.style.marginBottom = "8px";
    pHdr.appendChild(mkEl("strong", "", "Visual Generation Specification (nano_banana_3_prompt.md)"));
    const cpBtn = mkEl("button", "btn-secondary", "Copy Spec");
    cpBtn.type = "button";
    cpBtn.addEventListener("click", () =>
      copyTextSafe(detail.nano_banana_3_prompt || "", "Copied visual generation prompt!")
    );
    pHdr.appendChild(cpBtn);
    const pre = mkEl("pre", "code-block-light", detail.nano_banana_3_prompt || "");
    pre.id = "nb3-prompt-pre";
    promptBox.append(pHdr, pre);
    visTab.appendChild(promptBox);
  }

  // Tab 2: Slide Deck
  const slidesTab = document.getElementById("dtab-slides");
  if (slidesTab) {
    slidesTab.replaceChildren();
    const sBar = mkEl("div", "studio-toolbar-actions");
    sBar.style.marginBottom = "14px";
    if (detail.flagship_24slide_url) {
      const dBtn = mkEl("a", "btn-primary", "Open Live 24-Slide Google Slides Deck ↗");
      dBtn.setAttribute("data-testid", "drawer-open-24slide-deck-btn");
      dBtn.href = safeUrl(detail.flagship_24slide_url);
      dBtn.target = "_blank";
      dBtn.rel = "noopener";
      sBar.appendChild(dBtn);
    }
    const pptxBtn = mkEl("a", "btn-primary", "Download 12-Slide .pptx");
    pptxBtn.href = `/repos/${encodeURIComponent(slug)}/slides/presentation_deck.pptx`;
    pptxBtn.setAttribute("download", "");
    sBar.appendChild(pptxBtn);

    const pdfBtn = mkEl("a", "btn-secondary", "Open Carousel .pdf ↗");
    pdfBtn.href = `/repos/${encodeURIComponent(slug)}/slides/linkedin_carousel.pdf`;
    pdfBtn.target = "_blank";
    sBar.appendChild(pdfBtn);
    slidesTab.appendChild(sBar);

    (detail.slides || []).forEach((s) => {
      const sCard = mkEl("div", "feed-item-card");
      sCard.style.marginBottom = "10px";
      const k = mkEl("div", "eyebrow-label", `SLIDE ${s.slide_num} OF 12 • ${s.header_breadcrumb}`);
      k.style.marginBottom = "4px";
      const h = mkEl("div", "", s.headline);
      h.style.cssText = "font-size:14px;font-weight:800;color:#0f172a;margin-bottom:3px;";
      const sub = mkEl("div", "", s.subtitle);
      sub.style.cssText = "font-size:12.5px;color:#475569;margin-bottom:8px;";
      const note = mkEl("div", "", `Talk Track: ${(s.spoken_notes || [])[0] || ""}`);
      note.style.cssText = "font-size:12px;color:#0f172a;background:#ffffff;border-left:3px solid #059669;padding:7px 10px;border-radius:4px;";
      sCard.append(k, h, sub, note);
      slidesTab.appendChild(sCard);
    });
  }

  // Tab 3: Terraform & ADK Code
  const tfTab = document.getElementById("dtab-terraform");
  if (tfTab) {
    tfTab.replaceChildren();
    [
      ["1-Click Google Cloud Deployment", `cd generated-repos/${slug} && ./scripts/deploy_gcp_one_click.sh ramp-portal-dev us-west1`],
      ["terraform/main.tf (Cloud Run v2 + Vertex AI Global + IAM)", detail.terraform_main || ""],
      ["src/engine.py (Google Cloud ADK + Global Endpoint)", detail.engine_py || ""],
    ].forEach(([label, code]) => {
      const wrap = mkEl("div");
      wrap.style.marginBottom = "14px";
      const lbl = mkEl("div", "", label);
      lbl.style.cssText = "font-size:12.5px;font-weight:700;color:#0f172a;margin-bottom:6px;";
      wrap.append(lbl, mkEl("pre", "code-block-light", code));
      tfTab.appendChild(wrap);
    });
  }

  // Tab 4: LinkedIn Copy & Distribution
  const liTab = document.getElementById("dtab-linkedin");
  if (liTab) {
    liTab.replaceChildren();
    if (plan) {
      const planCard = mkEl("div", "golden-rule-card");
      planCard.style.marginBottom = "14px";
      planCard.appendChild(
        mkEl("div", "eyebrow-label", `Distribution Strategy · Template ${plan.primary_template_id}`)
      );

      const cols = mkEl("div", "miner-feeds-grid");
      cols.style.marginTop = "10px";

      const pBox = mkEl("div", "feed-item-card");
      pBox.style.background = "#ffffff";
      pBox.appendChild(mkEl("div", "eyebrow-label", "PRIMARY HIGH-REACH GROUPS"));
      (plan.linkedin_groups_primary || []).forEach((g) => {
        const line = mkEl("div", "", `• ${g.name} (${g.members}) — ${g.goal}`);
        line.style.cssText = "font-size:12px;color:#334155;margin-top:4px;";
        pBox.appendChild(line);
      });

      const nBox = mkEl("div", "feed-item-card");
      nBox.style.background = "#ffffff";
      nBox.appendChild(mkEl("div", "eyebrow-label", "NICHE EXECUTIVE & ARCHITECT GROUPS"));
      (plan.linkedin_groups_niche_network || []).forEach((g) => {
        const line = mkEl("div", "", `• ${g.name} (${g.members}) — ${g.goal}`);
        line.style.cssText = "font-size:12px;color:#334155;margin-top:4px;";
        nBox.appendChild(line);
      });

      cols.append(pBox, nBox);
      planCard.appendChild(cols);
      liTab.appendChild(planCard);
    }

    const hdr = mkEl("div", "composer-section-hdr");
    hdr.style.marginBottom = "8px";
    hdr.appendChild(mkEl("strong", "", "Publication-Ready LinkedIn Draft & First Comment"));
    const copyBtn = mkEl("button", "btn-primary", "Copy Post Draft");
    copyBtn.type = "button";
    copyBtn.addEventListener("click", () =>
      copyTextSafe(detail.linkedin_post_draft || "", "Copied LinkedIn Post Draft!")
    );
    hdr.appendChild(copyBtn);

    const copyPre = mkEl("pre", "code-block-light", detail.linkedin_post_draft || "");
    copyPre.id = "linkedin-copy-pre";
    liTab.append(hdr, copyPre);
  }

  document.getElementById("creator-radar-drawer")?.classList.remove("open");
  document.getElementById("repo-inspector-drawer")?.classList.add("open");
  document.getElementById("drawer-backdrop")?.classList.add("open");
}

/* ==========================================================================
   View 2: 116 Certified Visual Blueprints Gallery
   ========================================================================== */
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
  grid.replaceChildren();

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
  const countBadge = document.getElementById("gallery-count-badge");
  if (countBadge && (STATE.templates || []).length) {
    countBadge.textContent = `${items.length} / ${STATE.templates.length} Certified Templates (${bestCount} Best + ${highCount} High)`;
  }

  items.forEach((t) => {
    const files = t.files || {};
    const svg = `/assets/template-gallery/${files.svg || t.id + ".svg"}?v=20261104`;
    const png = `/assets/template-gallery/${files.png || t.id + ".png"}?v=20261104`;
    const gif = `/assets/template-gallery/${files.gif || t.id + ".gif"}?v=20261104`;
    const drawio = files.drawio ? `/assets/template-gallery/${files.drawio}?v=20261104` : "";
    const pptx = files.pptx ? `/assets/template-gallery/${files.pptx}?v=20261104` : "";
    const gslidesUrl = t.google_slides_url || "";
    const qTier = t.quality_tier || "Best";

    const card = mkEl("article", "repo-card");
    card.setAttribute("data-testid", `template-card-${t.id}`);

    const topWrap = mkEl("div");
    const stage = mkEl("div", "card-artwork-stage");
    stage.style.marginBottom = "12px";
    const img = document.createElement("img");
    img.src = svg;
    img.alt = `${t.id} ${t.name} blueprint`;
    img.loading = "lazy";
    stage.appendChild(img);
    stage.appendChild(mkEl("span", "card-zoom-pill", "Click to Zoom @2x"));
    stage.addEventListener("click", () => {
      const acts = [];
      if (gslidesUrl) acts.push({ label: "Open Google Slides ↗", href: gslidesUrl, primary: true });
      if (pptx) acts.push({ label: "Download .pptx", href: pptx, download: `${t.id}.pptx` });
      if (drawio) acts.push({ label: "Download .drawio", href: drawio, download: `${t.id}.drawio` });
      acts.push({ label: "Open SVG ↗", href: svg });
      openLightbox({
        kicker: `${t.id} · ${qTier.toUpperCase()} TIER BLUEPRINT`,
        title: t.name,
        imgUrl: svg,
        actions: acts,
      });
    });
    topWrap.appendChild(stage);

    const hdr = mkEl("div", "repo-card-header");
    hdr.style.marginBottom = "6px";
    hdr.appendChild(mkEl("span", "brand-badge", t.id));
    hdr.appendChild(
      mkEl(
        "span",
        `pill-badge ${qTier === "Best" ? "pill-emerald" : "pill-sky"}`,
        qTier === "Best" ? "Best Tier" : "High Tier"
      )
    );
    topWrap.appendChild(hdr);

    const titleEl = mkEl("h3", "repo-card-title", t.name);
    titleEl.style.marginBottom = "5px";
    topWrap.appendChild(titleEl);

    const cleanWhen = String(t.when_to_use || "").replace(/`/g, "").replace(/\s*->\s*/g, " → ");
    topWrap.appendChild(mkEl("p", "repo-card-hook", cleanWhen));

    if (STATE.persona === "builder") {
      const cleanDyn = String(t.dynamic || "").replace(/`/g, "").replace(/\s*->\s*/g, " → ");
      const meta = mkEl("div", "", `Topology: ${cleanDyn}${t.rendering_tech ? " · " + t.rendering_tech : ""}`);
      meta.style.cssText = "margin-top:8px;font-size:11.5px;color:#475569;";
      topWrap.appendChild(meta);
    }

    if ((t.topic_posts || []).length > 0) {
      const showcase = mkEl("div", "feed-item-card");
      showcase.setAttribute("data-testid", "t79-topic-posts-showcase");
      showcase.style.marginTop = "10px";
      const shTitle = mkEl("div", "eyebrow-label", `${t.topic_posts.length} Canonical Spine Variants`);
      shTitle.style.marginBottom = "6px";
      showcase.appendChild(shTitle);
      const chips = mkEl("div", "deliverable-chips");
      t.topic_posts.forEach((tp) => {
        const a = mkEl("a", "deliverable-chip chip-blue", tp.id);
        a.style.textDecoration = "none";
        a.href = `/assets/template-gallery/${encodeURIComponent(tp.id)}.svg`;
        a.target = "_blank";
        a.title = tp.name || tp.id;
        chips.appendChild(a);
      });
      showcase.appendChild(chips);
      topWrap.appendChild(showcase);
    }
    card.appendChild(topWrap);

    const footer = mkEl("div", "repo-card-footer");
    const actGroup = mkEl("div", "studio-toolbar-actions");
    if (gslidesUrl) {
      const gs = mkEl("a", "btn-primary", "Google Slides ↗");
      gs.setAttribute("data-testid", `open-with-google-slides-btn-${t.id}`);
      gs.href = safeUrl(gslidesUrl);
      gs.target = "_blank";
      gs.rel = "noopener";
      actGroup.appendChild(gs);
    }
    if (pptx) {
      const pp = mkEl("a", "btn-secondary", ".pptx");
      pp.setAttribute("data-testid", `download-pptx-btn-${t.id}`);
      pp.href = pptx;
      pp.setAttribute("download", `${t.id}.pptx`);
      actGroup.appendChild(pp);
    }
    if (drawio) {
      const dr = mkEl("a", "btn-secondary", ".drawio");
      dr.setAttribute("data-testid", `download-drawio-btn-${t.id}`);
      dr.href = drawio;
      dr.setAttribute("download", `${t.id}.drawio`);
      actGroup.appendChild(dr);
    }
    const pngLink = mkEl("a", "btn-secondary", "PNG ↗");
    pngLink.href = png;
    pngLink.target = "_blank";
    actGroup.appendChild(pngLink);

    const svgLink = mkEl("a", "btn-secondary", "SVG ↗");
    svgLink.href = svg;
    svgLink.target = "_blank";
    actGroup.appendChild(svgLink);

    if (STATE.persona === "builder") {
      const gifLink = mkEl("a", "btn-secondary", "GIF");
      gifLink.href = gif;
      gifLink.setAttribute("download", "");
      actGroup.appendChild(gifLink);
    }

    footer.appendChild(actGroup);
    card.appendChild(footer);
    grid.appendChild(card);
  });

  const tbody = document.getElementById("pairings-tbody");
  if (tbody) {
    tbody.replaceChildren();
    (STATE.pairings || []).forEach((p) => {
      const tr = document.createElement("tr");
      [
        [p.capability, "font-weight:700;color:#0f172a;"],
        [p.google, "font-weight:600;color:#1e40af;"],
        [p.oss, "font-weight:600;color:#065f46;"],
        [p.note, "color:#334155;"],
      ].forEach(([txt, st]) => {
        const td = document.createElement("td");
        const cell = mkEl("div", "cell-card-equal");
        const sp = mkEl("span", "", txt);
        sp.style.cssText = `font-size:12px;${st}`;
        cell.appendChild(sp);
        td.appendChild(cell);
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  }
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

/* ==========================================================================
   View 3: Creator Radar & View 5: OpenHands Sandbox
   ========================================================================== */
function getInitials(name) {
  return String(name || "AI")
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0] || "")
    .join("")
    .toUpperCase();
}

function activatePlaybookPanel(panelId) {
  const next = PLAYBOOK_PANELS.includes(panelId) ? panelId : "playbook-panel-posts";
  STATE.activePlaybookPanel = next;
  PLAYBOOK_PANELS.forEach((pid) => {
    const el = document.getElementById(pid);
    if (el) el.style.display = pid === next ? "block" : "none";
  });
  document.querySelectorAll("[data-playbook-panel]").forEach((btn) => {
    const isAct = btn.getAttribute("data-playbook-panel") === next;
    btn.classList.toggle("active", isAct);
    btn.setAttribute("aria-selected", isAct ? "true" : "false");
  });
}

function populateReviewedAuthorSelect(posts) {
  const sel = document.getElementById("posts-audit-filter-author");
  if (!sel || sel.dataset.hydrated === "1") return;
  const authors = Array.from(
    new Set(posts.filter((p) => p.availability === "PUBLIC_VERIFIED").map((p) => p.author_name))
  ).sort((a, b) => a.localeCompare(b));
  authors.forEach((name) => {
    const opt = mkEl("option", "", name);
    opt.value = name;
    sel.appendChild(opt);
  });
  if (authors.length) sel.dataset.hydrated = "1";
}

async function remixPostInStudio(post) {
  activateView("view-miner");
  activateMinerPanel("miner-panel-composer");
  const qInput = document.getElementById("top5-query-input");
  if (qInput && post.hook_line_1) {
    qInput.value = `${post.author_name}: ${post.hook_line_1.slice(0, 90)}`;
  }
  if (post.matched_template_id) {
    STATE.selectedTemplateId = post.matched_template_id;
  }
  renderTop5EditorialDesk();
  await refreshPlatformPreviewPackages();
  showToast(`Loaded blueprint ${post.matched_template_id} from ${post.post_code} in Daily Studio`);
}

function polishArrows(s) {
  return String(s || "").replace(/\s*->\s*/g, " → ");
}

function closeAllSlideDrawers() {
  document.getElementById("repo-inspector-drawer")?.classList.remove("open");
  document.getElementById("creator-radar-drawer")?.classList.remove("open");
  document.getElementById("drawer-backdrop")?.classList.remove("open");
}

function openPostAnatomyDrawer(activityId) {
  const pb = STATE.playbook || {};
  const post = (pb.reviewed_posts || []).find((p) => p.activity_id === activityId);
  const drawer = document.getElementById("creator-radar-drawer");
  const badgeEl = document.getElementById("radar-drawer-badge");
  const titleEl = document.getElementById("radar-drawer-title");
  const bodyEl = document.getElementById("radar-drawer-body");
  if (!post || !drawer || !bodyEl) return;

  const matchedCreator = (pb.creator_profiles || []).find(
    (c) => c.name.toLowerCase() === String(post.author_name || "").toLowerCase()
  );

  document.getElementById("repo-inspector-drawer")?.classList.remove("open");
  if (badgeEl) badgeEl.textContent = `${post.post_code} · ${post.presentation_archetype_code} · ${post.published_utc || "DISCLOSED"}`;
  if (titleEl) titleEl.textContent = `${post.author_name} — Post & Presentation Anatomy`;
  bodyEl.replaceChildren();

  const actionsBar = mkEl("div", "studio-toolbar-actions");
  actionsBar.style.marginBottom = "12px";
  const liBtn = mkEl("a", "btn-secondary", "Open Original LinkedIn Post ↗");
  liBtn.href = safeUrl(post.post_url);
  liBtn.target = "_blank";
  liBtn.rel = "noopener";
  actionsBar.appendChild(liBtn);

  if (post.availability === "PUBLIC_VERIFIED") {
    const copyBtn = mkEl("button", "btn-secondary", "Copy Verbatim Text");
    copyBtn.type = "button";
    copyBtn.addEventListener("click", () => copyTextSafe(post.full_text, `Copied ${post.post_code} verbatim text!`));
    const creatorBtn = mkEl("button", "btn-secondary", `View ${post.author_name}'s Full Portfolio →`);
    creatorBtn.type = "button";
    creatorBtn.addEventListener("click", () => openCreatorPortfolioDrawer(post.author_name));
    const remixBtn = mkEl("button", "btn-primary", `Remix with ${post.matched_template_id} →`);
    remixBtn.type = "button";
    remixBtn.addEventListener("click", () => {
      closeAllSlideDrawers();
      remixPostInStudio(post);
    });
    actionsBar.append(copyBtn, creatorBtn, remixBtn);
  }
  bodyEl.appendChild(actionsBar);

  // Compact 2-Column Hero Grid: Left Visual + Right 3-Line Hook & Studio Blueprint Mapping
  const heroGrid = mkEl("div", "drawer-post-hero-grid");
  if (post.image_url) {
    const vbox = mkEl("div", "drawer-post-visual-card");
    const img = document.createElement("img");
    img.src = safeUrl(post.image_url);
    img.alt = `${post.author_name} post visual`;
    img.addEventListener("click", () =>
      openLightbox({
        kicker: `${post.post_code} · ${post.presentation_archetype_code}`,
        title: `${post.author_name} — ${post.hook_line_1}`,
        imgUrl: post.image_url,
        actions: [{ label: "Original LinkedIn Post ↗", href: post.post_url }],
      })
    );
    const zHint = mkEl("span", "eyebrow-muted", "Click artwork to zoom @2x");
    zHint.style.marginTop = "6px";
    vbox.append(img, zHint);
    heroGrid.appendChild(vbox);
  } else {
    const rBox = mkEl("div", "drawer-post-visual-card", "Public media unavailable (Restricted / Removed LinkedIn URN)");
    rBox.style.cssText = "color:#475569;font-size:12px;text-align:center;padding:24px;";
    heroGrid.appendChild(rBox);
  }

  const rightHero = mkEl("div");
  rightHero.style.cssText = "display:flex;flex-direction:column;gap:10px;min-width:0;";

  const hookBox = mkEl("div", "platform-spec-box");
  hookBox.append(
    mkEl("div", "platform-spec-label", `3-Line LinkedIn Opening Hook (${polishArrows(post.hook_formula)})`),
    mkEl("div", "platform-spec-text", post.hook_3_lines || post.hook_line_1)
  );
  hookBox.lastChild.style.whiteSpace = "pre-line";
  hookBox.lastChild.style.fontWeight = "600";
  rightHero.appendChild(hookBox);

  const tid = post.matched_template_id || "T79";
  const bpMap = mkEl("div", "drawer-blueprint-map-card");
  const bpImg = document.createElement("img");
  bpImg.src = `/assets/template-gallery/${tid}.svg?v=20261104`;
  bpImg.alt = `Studio Blueprint ${tid}`;
  const bpInfo = mkEl("div", "min-w-0");
  bpInfo.style.flex = "1";
  const bpTitle = mkEl("div", "", `Matched Studio Blueprint ${tid}`);
  bpTitle.style.cssText = "font-size:12.5px;font-weight:800;color:#1e40af;";
  const bpSub = mkEl("div", "", `${post.presentation_archetype_code} · ${post.presentation_archetype_label}`);
  bpSub.style.cssText = "font-size:11.5px;color:#334155;";
  bpInfo.append(bpTitle, bpSub);
  const openBpBtn = mkEl("button", "btn-secondary", `Inspect ${tid} →`);
  openBpBtn.type = "button";
  openBpBtn.addEventListener("click", () => {
    closeAllSlideDrawers();
    jumpToTemplateInGallery(tid);
  });
  bpMap.append(bpImg, bpInfo, openBpBtn);
  rightHero.appendChild(bpMap);

  const kpiRow = mkEl("div", "deliverable-chips");
  kpiRow.append(
    mkEl("span", "pill-badge pill-emerald tabular-nums", `${post.reactions.toLocaleString()} reactions`),
    mkEl("span", "deliverable-chip tabular-nums", `${post.comments.toLocaleString()} comments`),
    mkEl("span", "deliverable-chip chip-blue tabular-nums", `${post.discussion_ratio_pct}% discussion ratio`),
    mkEl("span", "deliverable-chip", polishArrows(`CTA: ${post.cta_mechanic}`))
  );
  rightHero.appendChild(kpiRow);
  heroGrid.appendChild(rightHero);
  bodyEl.appendChild(heroGrid);

  // Mentor + Critic Review Side-by-Side (Above the 1050px Fold!)
  const mcGrid = mkEl("div", "mentor-critic-grid");
  const mentorBox = mkEl("div", "mentor-card");
  const mLbl = mkEl("div", "platform-spec-label", "Mentor Review — Why This Works");
  mLbl.style.color = "#065f46";
  mentorBox.append(mLbl, mkEl("div", "platform-spec-text", polishArrows(post.mentor_review || post.content_structure)));

  const criticBox = mkEl("div", "critic-card");
  const cLbl = mkEl("div", "platform-spec-label", "Critic Review — Where to Sharpen & Repurpose");
  cLbl.style.color = "#92400e";
  criticBox.append(cLbl, mkEl("div", "platform-spec-text", polishArrows(post.critic_review || "")));
  mcGrid.append(mentorBox, criticBox);
  bodyEl.appendChild(mcGrid);

  // 3 Structural & Presentation Takeaways
  const takeBox = mkEl("div", "platform-spec-box");
  takeBox.style.marginBottom = "14px";
  takeBox.appendChild(mkEl("div", "platform-spec-label", "Structural & Presentation Takeaways"));
  const takeUl = document.createElement("ul");
  takeUl.style.cssText = "padding-left:18px;margin:4px 0 0;font-size:12px;color:#0f172a;line-height:1.52;";
  (post.structural_takeaways || [post.content_structure]).forEach((item) => {
    takeUl.appendChild(mkEl("li", "", polishArrows(item)));
  });
  takeBox.appendChild(takeUl);
  bodyEl.appendChild(takeBox);

  // Creator's Multi-Post & Cross-Platform Portfolio Inline
  if (matchedCreator && (matchedCreator.all_posts_portfolio || []).length) {
    const portHdr = mkEl(
      "h3",
      "subsection-heading",
      `${matchedCreator.name}'s Cross-Platform Portfolio (${matchedCreator.all_posts_portfolio.length} Artifacts)`
    );
    portHdr.style.marginBottom = "8px";
    bodyEl.appendChild(portHdr);
    const portWrap = mkEl("div", "platform-playbook-grid");
    portWrap.style.marginBottom = "14px";
    matchedCreator.all_posts_portfolio.forEach((entry) => {
      const pCard = mkEl("div", "feed-item-card");
      const pTop = mkEl("div", "composer-section-hdr");
      pTop.append(
        mkEl("strong", "", entry.title),
        mkEl("span", "pill-badge pill-sky", `${entry.platform} · ${entry.format}`)
      );
      pCard.appendChild(pTop);
      if (entry.url) {
        const a = mkEl("a", "eyebrow-link", "Open Artifact ↗");
        a.href = safeUrl(entry.url);
        a.target = "_blank";
        a.rel = "noopener";
        a.style.cssText = "display:inline-flex;width:fit-content;margin-top:6px;";
        pCard.appendChild(a);
      }
      portWrap.appendChild(pCard);
    });
    bodyEl.appendChild(portWrap);
  }

  const copyHdr = mkEl("h3", "subsection-heading", `Verbatim Post Copy (${post.char_count.toLocaleString()} chars · ${post.line_count} lines)`);
  copyHdr.style.marginBottom = "8px";
  const pre = mkEl("pre", "code-block-light", post.full_text);
  bodyEl.append(copyHdr, pre);

  drawer.classList.add("open");
  document.getElementById("drawer-backdrop")?.classList.add("open");
}

function openCreatorPortfolioDrawer(creatorName) {
  const pb = STATE.playbook || {};
  const cp = (pb.creator_profiles || []).find((c) => c.name.toLowerCase() === String(creatorName || "").toLowerCase());
  const drawer = document.getElementById("creator-radar-drawer");
  const badgeEl = document.getElementById("radar-drawer-badge");
  const titleEl = document.getElementById("radar-drawer-title");
  const bodyEl = document.getElementById("radar-drawer-body");
  if (!cp || !drawer || !bodyEl) return;

  document.getElementById("repo-inspector-drawer")?.classList.remove("open");
  if (badgeEl) badgeEl.textContent = `CREATOR PORTFOLIO · BLUEPRINT ${cp.template_id} · ${Number(cp.followers || 0).toLocaleString()} FOLLOWERS`;
  if (titleEl) titleEl.textContent = cp.name;
  bodyEl.replaceChildren();

  const roleP = mkEl("p", "section-description", cp.role);
  roleP.style.marginBottom = "10px";
  bodyEl.appendChild(roleP);

  const handlesWrap = mkEl("div", "social-handle-chips");
  handlesWrap.style.marginBottom = "14px";
  const handleLabels = {
    linkedin: "LinkedIn ↗",
    x: "X / Twitter ↗",
    substack: "Substack / Blog ↗",
    github: "GitHub ↗",
    youtube: "YouTube ↗",
    instagram: "Instagram ↗",
    tiktok: "TikTok ↗",
    website: "Website ↗",
  };
  Object.entries(cp.handles || { linkedin: cp.linkedin_url }).forEach(([k, url]) => {
    if (!url) return;
    const a = mkEl("a", "social-chip-link", handleLabels[k] || `${k} ↗`);
    a.href = safeUrl(url);
    a.target = "_blank";
    a.rel = "noopener";
    handlesWrap.appendChild(a);
  });
  const styleBtn = mkEl("button", "btn-primary", `Generate Batch in ${cp.name}'s Style →`);
  styleBtn.type = "button";
  styleBtn.style.marginLeft = "auto";
  styleBtn.addEventListener("click", () => {
    closeAllSlideDrawers();
    generateInCreatorStyle(cp.style_code || "AUTO", cp.name);
  });
  handlesWrap.appendChild(styleBtn);
  bodyEl.appendChild(handlesWrap);

  const sigBox = mkEl("div", "platform-spec-box");
  sigBox.style.marginBottom = "16px";
  sigBox.append(
    mkEl("div", "platform-spec-label", `Signature Content & Visual Presentation (${cp.archetype_label})`),
    mkEl("div", "platform-spec-text", cp.signature_style)
  );
  bodyEl.appendChild(sigBox);

  const auditedPosts = (pb.reviewed_posts || []).filter(
    (p) => p.availability === "PUBLIC_VERIFIED" && p.author_name.toLowerCase() === cp.name.toLowerCase()
  );
  if (auditedPosts.length) {
    const audHdr = mkEl("h3", "subsection-heading", `Audited Posts in 33-Post Cohort (${auditedPosts.length})`);
    audHdr.style.marginBottom = "10px";
    bodyEl.appendChild(audHdr);
    auditedPosts.forEach((ap) => {
      const item = mkEl("div", "feed-item-card");
      item.style.marginBottom = "10px";
      const row = mkEl("div", "composer-section-hdr");
      row.append(
        mkEl("strong", "", `${ap.post_code} · ${ap.hook_line_1}`),
        mkEl("span", "pill-badge pill-emerald tabular-nums", `${ap.reactions} 👍 · ${ap.comments} 💬`)
      );
      const sub = mkEl("p", "", ap.content_structure);
      sub.style.cssText = "font-size:12px;color:#334155;margin:6px 0 8px;";
      const openBtn = mkEl("button", "btn-secondary", "Inspect Full Post & Visual →");
      openBtn.type = "button";
      openBtn.addEventListener("click", () => openPostAnatomyDrawer(ap.activity_id));
      item.append(row, sub, openBtn);
      bodyEl.appendChild(item);
    });
  }

  const portList = cp.all_posts_portfolio || [];
  const portHdr = mkEl("h3", "subsection-heading", `Complete Researched Posts, Repos & Publications (${portList.length})`);
  portHdr.style.margin = "14px 0 10px";
  bodyEl.appendChild(portHdr);

  portList.forEach((entry) => {
    const card = mkEl("div", "feed-item-card");
    card.style.marginBottom = "8px";
    const hdr = mkEl("div", "composer-section-hdr");
    hdr.append(
      mkEl("strong", "", entry.title),
      mkEl("span", "pill-badge pill-sky", `${entry.platform} · ${entry.format}`)
    );
    card.appendChild(hdr);
    if (entry.url) {
      const link = mkEl("a", "eyebrow-link", "Open Source Artifact ↗");
      link.href = safeUrl(entry.url);
      link.target = "_blank";
      link.rel = "noopener";
      link.style.display = "inline-block";
      link.style.marginTop = "6px";
      card.appendChild(link);
    }
    bodyEl.appendChild(card);
  });

  drawer.classList.add("open");
  document.getElementById("drawer-backdrop")?.classList.add("open");
}

function renderReviewedPostsGrid() {
  const pb = STATE.playbook || {};
  const allPosts = pb.reviewed_posts || [];
  populateReviewedAuthorSelect(allPosts);

  const grid = document.getElementById("reviewed-posts-grid");
  if (!grid) return;
  grid.replaceChildren();

  const q = (document.getElementById("posts-audit-search-input")?.value || "").trim().toLowerCase();
  const presFilter = document.getElementById("posts-audit-filter-pres")?.value || "ALL";
  const authorFilter = document.getElementById("posts-audit-filter-author")?.value || "ALL";
  const sortMode = document.getElementById("posts-audit-sort-select")?.value || "INDEX";

  const filtered = allPosts.filter((p) => {
    if (presFilter !== "ALL" && p.presentation_archetype_code !== presFilter) return false;
    if (authorFilter !== "ALL" && p.author_name !== authorFilter) return false;
    if (q) {
      const hay = `${p.post_code} ${p.activity_id} ${p.author_name} ${p.hook_line_1} ${p.content_structure} ${p.full_text}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  filtered.sort((a, b) => {
    if (sortMode === "REACTIONS") return b.reactions - a.reactions || a.index - b.index;
    if (sortMode === "DISCUSSION") return b.discussion_ratio_pct - a.discussion_ratio_pct || b.comments - a.comments;
    if (sortMode === "COMMENTS") return b.comments - a.comments || b.reactions - a.reactions;
    return a.index - b.index;
  });

  const pillEl = document.getElementById("playbook-posts-count-pill");
  if (pillEl) pillEl.textContent = String(filtered.length);

  if (!filtered.length) {
    const empty = mkEl("div", "studio-surface", "No reviewed posts match the current search/filter.");
    empty.style.cssText = "grid-column: 1 / -1; text-align: center; padding: 32px; color: #475569;";
    grid.appendChild(empty);
    return;
  }

  filtered.forEach((post) => {
    const isRestricted = post.availability !== "PUBLIC_VERIFIED";
    const card = mkEl("article", `reviewed-post-card${isRestricted ? " restricted-card" : ""}`);
    card.setAttribute("data-testid", `reviewed-post-card-${post.index}`);

    const topCol = mkEl("div");
    topCol.style.cssText = "display:flex;flex-direction:column;gap:10px;min-width:0;";

    const metaRow = mkEl("div", "deliverable-chips");
    metaRow.appendChild(mkEl("span", "brand-badge tabular-nums", `${post.post_code} · #${String(post.index).padStart(2, "0")}`));
    metaRow.appendChild(
      mkEl(
        "span",
        isRestricted ? "pill-badge pill-amber" : "pill-badge pill-sky",
        isRestricted ? "RESTRICTED URN" : post.presentation_archetype_code
      )
    );
    metaRow.appendChild(mkEl("span", "deliverable-chip tabular-nums", `Blueprint ${post.matched_template_id}`));
    if (post.published_utc) {
      metaRow.appendChild(mkEl("span", "deliverable-chip tabular-nums", post.published_utc));
    }
    topCol.appendChild(metaRow);

    if (!isRestricted && post.image_url) {
      const frame = mkEl("div", "post-visual-frame");
      const img = document.createElement("img");
      img.src = safeUrl(post.image_url);
      img.alt = `${post.author_name} visual (${post.post_code})`;
      img.loading = post.index <= 6 ? "eager" : "lazy";
      const zoomPill = mkEl("span", "post-visual-zoom-pill", "Zoom Visual");
      frame.append(img, zoomPill);
      frame.addEventListener("click", () =>
        openLightbox({
          kicker: `${post.post_code} · ${post.presentation_archetype_code} · ${post.author_name}`,
          title: post.hook_line_1,
          imgUrl: post.image_url,
          actions: [{ label: "LinkedIn Post ↗", href: post.post_url }],
        })
      );
      topCol.appendChild(frame);
    }

    if (!isRestricted) {
      const authorBtn = mkEl("button", "post-author-btn");
      authorBtn.type = "button";
      authorBtn.appendChild(mkEl("span", "creator-monogram", getInitials(post.author_name)));
      const aMeta = mkEl("div", "min-w-0");
      aMeta.style.cssText = "display:flex;flex-direction:column;gap:2px;min-width:0;flex:1;";
      const aName = mkEl("h3", "truncate", post.author_name);
      aName.style.cssText = "font-size:13.5px;font-weight:800;color:#0f172a;line-height:1.25;";
      const aRole = mkEl("div", "truncate", post.author_headline || "Verified Creator");
      aRole.style.cssText = "font-size:11px;color:#475569;";
      aMeta.append(aName, aRole);
      authorBtn.appendChild(aMeta);
      authorBtn.addEventListener("click", () => openCreatorPortfolioDrawer(post.author_name));
      topCol.appendChild(authorBtn);

      const engRow = mkEl("div", "deliverable-chips");
      engRow.append(
        mkEl("span", "pill-badge pill-emerald tabular-nums", `${post.reactions.toLocaleString()} reactions`),
        mkEl("span", "deliverable-chip tabular-nums", `${post.comments.toLocaleString()} comments`),
        mkEl("span", "deliverable-chip chip-blue tabular-nums", `${post.discussion_ratio_pct}% discussion`)
      );
      topCol.appendChild(engRow);
    }

    topCol.appendChild(mkEl("div", "post-hook-headline", polishArrows(post.hook_line_1)));
    topCol.appendChild(mkEl("p", "post-structure-summary", polishArrows(post.content_structure)));
    if (!isRestricted && post.mentor_review) {
      topCol.appendChild(mkEl("div", "post-card-takeaway-strip", polishArrows(post.mentor_review)));
    }
    card.appendChild(topCol);

    const foot = mkEl("div", "repo-card-footer");
    const leftBtns = mkEl("div", "studio-toolbar-actions");
    const anatBtn = mkEl("button", "btn-secondary", isRestricted ? "Disclosure" : "Anatomy →");
    anatBtn.type = "button";
    anatBtn.setAttribute("data-testid", `inspect-post-anatomy-${post.index}`);
    anatBtn.addEventListener("click", () => openPostAnatomyDrawer(post.activity_id));
    const extLink = mkEl("a", "btn-secondary", "URN ↗");
    extLink.href = safeUrl(post.post_url);
    extLink.target = "_blank";
    extLink.rel = "noopener";
    leftBtns.append(anatBtn, extLink);
    foot.appendChild(leftBtns);

    if (!isRestricted) {
      const remixBtn = mkEl("button", "btn-primary", "Remix →");
      remixBtn.type = "button";
      remixBtn.addEventListener("click", () => remixPostInStudio(post));
      foot.appendChild(remixBtn);
    }
    card.appendChild(foot);
    grid.appendChild(card);
  });
}

function renderCreatorProfilesGrid() {
  const pb = STATE.playbook || {};
  const profiles = pb.creator_profiles || [];
  const cpGrid = document.getElementById("creator-profiles-grid");
  if (!cpGrid) return;
  cpGrid.replaceChildren();

  const q = (document.getElementById("creator-search-input")?.value || "").trim().toLowerCase();
  const pFilter = document.getElementById("creator-platform-filter")?.value || "ALL";

  const filtered = profiles.filter((cp) => {
    const h = cp.handles || {};
    if (pFilter === "AUDIT_33" && !cp.in_33_post_audit) return false;
    if (pFilter === "HAS_X" && !h.x) return false;
    if (pFilter === "HAS_SUBSTACK" && !h.substack) return false;
    if (pFilter === "HAS_GITHUB" && !h.github) return false;
    if (pFilter === "HAS_VIDEO" && !(h.youtube || h.instagram || h.tiktok)) return false;
    if (q) {
      const hay = `${cp.name} ${cp.role} ${cp.signature_style} ${JSON.stringify(h)} ${JSON.stringify(cp.all_posts_portfolio || [])}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  const cPill = document.getElementById("playbook-creators-count-pill");
  if (cPill) cPill.textContent = String(filtered.length);

  filtered.forEach((cp, idx) => {
    const card = mkEl("article", "creator-profile-card");
    card.setAttribute("data-testid", `creator-profile-${cp.template_id}-${idx}`);

    const top = mkEl("div");
    const avRow = mkEl("div", "creator-avatar-row");
    avRow.appendChild(mkEl("span", "creator-monogram", getInitials(cp.name)));
    const meta = mkEl("div", "min-w-0");
    meta.style.cssText = "display:flex;flex-direction:column;gap:2px;min-width:0;flex:1;";
    const nameEl = mkEl("h3", "truncate", cp.name);
    nameEl.style.cssText = "font-size:14.5px;font-weight:800;color:#0f172a;line-height:1.25;";
    const roleEl = mkEl("div", "truncate", cp.role);
    roleEl.style.cssText = "font-size:11.5px;color:#475569;";
    meta.append(nameEl, roleEl);
    avRow.appendChild(meta);
    top.appendChild(avRow);

    const badges = mkEl("div", "deliverable-chips");
    badges.style.marginBottom = "6px";
    const bpBadgeBtn = mkEl("button", "brand-badge", `Blueprint ${cp.template_id} ↗`);
    bpBadgeBtn.type = "button";
    bpBadgeBtn.style.cursor = "pointer";
    bpBadgeBtn.addEventListener("click", () => jumpToTemplateInGallery(cp.template_id));
    badges.appendChild(bpBadgeBtn);
    if (cp.in_33_post_audit) {
      badges.appendChild(mkEl("span", "pill-badge pill-emerald", "In 33-Post Audit"));
    }
    if (cp.followers) {
      badges.appendChild(mkEl("span", "pill-badge pill-sky tabular-nums", `${Number(cp.followers).toLocaleString()} reach`));
    }
    top.appendChild(badges);

    const chipRow = mkEl("div", "social-handle-chips");
    const shortLabels = { linkedin: "in", x: "X", substack: "Substack", github: "GitHub", youtube: "YT", instagram: "IG", tiktok: "TikTok", website: "Web" };
    Object.entries(cp.handles || { linkedin: cp.linkedin_url }).forEach(([k, url]) => {
      if (!url) return;
      const a = mkEl("a", "social-chip-link", `${shortLabels[k] || k} ↗`);
      a.href = safeUrl(url);
      a.target = "_blank";
      a.rel = "noopener";
      chipRow.appendChild(a);
    });
    top.appendChild(chipRow);

    top.appendChild(mkEl("p", "repo-card-hook", cp.signature_style));

    const portfolio = cp.all_posts_portfolio || [];
    if (portfolio.length) {
      const pList = mkEl("div", "portfolio-mini-list");
      portfolio.slice(0, 2).forEach((item) => {
        const row = mkEl("div", "portfolio-mini-item");
        const tSpan = mkEl("span", "truncate", `• ${item.title}`);
        const pSpan = mkEl("span", "eyebrow-muted", item.platform);
        pSpan.style.flexShrink = "0";
        row.append(tSpan, pSpan);
        pList.appendChild(row);
      });
      top.appendChild(pList);
    }
    card.appendChild(top);

    const foot = mkEl("div", "repo-card-footer");
    const leftBtns = mkEl("div", "studio-toolbar-actions");
    const portBtn = mkEl("button", "btn-secondary", `All Posts (${portfolio.length}) →`);
    portBtn.type = "button";
    portBtn.setAttribute("data-testid", `open-creator-portfolio-${idx}`);
    portBtn.addEventListener("click", () => openCreatorPortfolioDrawer(cp.name));
    leftBtns.appendChild(portBtn);

    const genBtn = mkEl("button", "btn-primary", "Use Style →");
    genBtn.type = "button";
    genBtn.setAttribute("data-testid", `generate-in-style-${cp.template_id}`);
    genBtn.addEventListener("click", () => generateInCreatorStyle(cp.style_code || "AUTO", cp.name));
    foot.append(leftBtns, genBtn);
    card.appendChild(foot);
    cpGrid.appendChild(card);
  });
}

function renderOmnichannelPlaybooks() {
  const pb = STATE.playbook || {};
  const platforms = pb.omnichannel_platforms || [];
  const pillsEl = document.getElementById("omnichannel-platform-pills");
  const stageEl = document.getElementById("omnichannel-active-platform-stage");
  if (pillsEl && stageEl && platforms.length) {
    pillsEl.replaceChildren();
    stageEl.replaceChildren();
    const activePlat =
      platforms.find((p) => p.id === STATE.activeOmnichannelPlatformId) || platforms[0];
    STATE.activeOmnichannelPlatformId = activePlat.id;

    platforms.forEach((plat) => {
      const btn = mkEl(
        "button",
        `top5-selector-pill${plat.id === activePlat.id ? " active" : ""}`,
        plat.short_label || plat.name
      );
      btn.type = "button";
      btn.setAttribute("role", "tab");
      btn.setAttribute("aria-selected", plat.id === activePlat.id ? "true" : "false");
      btn.setAttribute("data-testid", `omnichannel-pill-${plat.id}`);
      btn.addEventListener("click", () => {
        STATE.activeOmnichannelPlatformId = plat.id;
        renderOmnichannelPlaybooks();
      });
      pillsEl.appendChild(btn);
    });

    const hdrRow = mkEl("div", "composer-section-hdr");
    hdrRow.style.marginBottom = "12px";
    hdrRow.append(
      mkEl("h3", "subsection-heading", `${activePlat.name} — Distribution & Presentation Architecture`),
      mkEl("span", "pill-badge pill-emerald", activePlat.badge)
    );
    stageEl.appendChild(hdrRow);

    const specGrid = mkEl("div", "platform-playbook-grid");
    [
      ["Algorithmic Ranking Weights", activePlat.primary_signal_weights],
      ["Winning Visual & Copy Container", activePlat.ideal_specs],
      ["Outbound Link Guardrail", activePlat.link_strategy],
      ["Repeatable Structural Formula", activePlat.winning_formula],
      ["Fatal Anti-Patterns to Avoid", activePlat.anti_patterns],
      ["Sustainable Publishing Cadence", activePlat.cadence],
    ].forEach(([lbl, txt]) => {
      const box = mkEl("div", "platform-spec-box");
      box.append(mkEl("div", "platform-spec-label", lbl), mkEl("div", "platform-spec-text", polishArrows(txt)));
      specGrid.appendChild(box);
    });
    stageEl.appendChild(specGrid);
  }

  const xTbody = document.getElementById("x-leaders-tbody");
  if (xTbody) {
    xTbody.replaceChildren();
    (pb.x_ecosystem_leaders || []).forEach((xl) => {
      const tr = document.createElement("tr");
      const td1 = document.createElement("td");
      const c1 = mkEl("div", "cell-card-equal");
      const strong = mkEl("strong", "", xl.name);
      strong.style.cssText = "font-size:12.5px;color:#0f172a;";
      const hLink = mkEl("a", "eyebrow-link", `${xl.handle} ↗`);
      hLink.style.cssText = "width:fit-content;margin-top:4px;";
      hLink.href = safeUrl(xl.url);
      hLink.target = "_blank";
      hLink.rel = "noopener";
      c1.append(strong, hLink);
      td1.appendChild(c1);

      [xl.role, xl.focus, xl.winning_format].forEach((txt) => {
        const td = document.createElement("td");
        const c = mkEl("div", "cell-card-equal");
        const sp = mkEl("span", "", txt);
        sp.style.cssText = "font-size:12px;color:#334155;";
        c.appendChild(sp);
        td.appendChild(c);
        tr.appendChild(td);
      });
      tr.prepend(td1);
      xTbody.appendChild(tr);
    });
  }

  const repTbody = document.getElementById("repurposing-matrix-tbody");
  if (repTbody) {
    repTbody.replaceChildren();
    (pb.repurposing_matrix || []).forEach((row) => {
      const tr = document.createElement("tr");
      [
        [row.step, "font-weight:800;color:#1e40af;"],
        [row.asset, "font-weight:700;color:#0f172a;"],
        [row.platforms, "font-weight:600;color:#065f46;"],
        [row.spec, "color:#334155;"],
        [row.goal, "color:#334155;"],
      ].forEach(([txt, st]) => {
        const td = document.createElement("td");
        const c = mkEl("div", "cell-card-equal");
        const sp = mkEl("span", "", txt);
        sp.style.cssText = `font-size:12px;${st}`;
        c.appendChild(sp);
        td.appendChild(c);
        tr.appendChild(td);
      });
      repTbody.appendChild(tr);
    });
  }
}

function renderPlaybookView() {
  const pb = STATE.playbook || {};
  const sumEl = document.getElementById("playbook-summary-text");
  if (sumEl) sumEl.textContent = pb.executive_summary || "";

  const profiles = pb.creator_profiles || [];
  const posts = pb.reviewed_posts || [];
  const cpBadge = document.getElementById("creator-profiles-count-badge");
  if (cpBadge) cpBadge.textContent = `${profiles.length} Verified Creators · ${posts.length} Audited Posts`;
  const navCnt = document.getElementById("nav-playbook-count");
  if (navCnt) navCnt.textContent = String(profiles.length || 39);

  renderReviewedPostsGrid();
  renderCreatorProfilesGrid();
  renderOmnichannelPlaybooks();

  const pres12Grid = document.getElementById("presentation-archetypes-12-grid");
  if (pres12Grid) {
    pres12Grid.replaceChildren();
    (pb.presentation_archetypes_12 || []).forEach((pa) => {
      const card = mkEl("div", "repo-card");
      const inner = mkEl("div");
      const chips = mkEl("div", "deliverable-chips");
      chips.append(
        mkEl("span", "brand-badge", pa.code),
        mkEl("span", "pill-badge pill-sky", pa.aspect_ratio)
      );
      inner.appendChild(chips);
      const h = mkEl("h3", "repo-card-title", pa.name);
      h.style.margin = "8px 0 6px";
      inner.appendChild(h);
      const anat = mkEl("p", "", polishArrows(pa.visual_anatomy));
      anat.style.cssText = "font-size:12px;color:#334155;margin-bottom:6px;line-height:1.48;";
      inner.appendChild(anat);
      const exFormatted = (pa.exemplar_posts || []).map((s) =>
        String(s).replace(/#(\d+)\s*\(\d{10,}\)/g, "LI-$1 (#$1)")
      );
      const ex = mkEl("div", "", `Audited Exemplars: ${exFormatted.join(" · ")}`);
      ex.style.cssText = "font-size:11.5px;font-weight:700;color:#1e40af;margin-bottom:8px;";
      inner.appendChild(ex);
      card.appendChild(inner);

      const foot = mkEl("div", "repo-card-footer");
      const filterBtn = mkEl("button", "btn-secondary", "Filter Posts →");
      filterBtn.type = "button";
      filterBtn.addEventListener("click", () => {
        const sel = document.getElementById("posts-audit-filter-pres");
        if (sel) sel.value = pa.code;
        activatePlaybookPanel("playbook-panel-posts");
        renderReviewedPostsGrid();
      });
      const tplBtn = mkEl("button", "btn-primary", `Blueprint ${pa.matched_template_id}`);
      tplBtn.type = "button";
      tplBtn.addEventListener("click", () => jumpToTemplateInGallery(pa.matched_template_id));
      foot.append(filterBtn, tplBtn);
      card.appendChild(foot);
      pres12Grid.appendChild(card);
    });
  }

  const chGrid = document.getElementById("signal-channels-grid");
  if (chGrid) {
    chGrid.replaceChildren();
    (pb.signal_channels || []).forEach((ch) => {
      const card = mkEl("div", "repo-card");
      const inner = mkEl("div");
      inner.appendChild(mkEl("span", "brand-badge", ch.id));
      const h = mkEl("h3", "repo-card-title", ch.name);
      h.style.margin = "8px 0 6px";
      inner.appendChild(h);
      const p = mkEl("p", "", polishArrows(ch.mining_pattern));
      p.style.cssText = "font-size:12.5px;color:#475569;margin-bottom:8px;line-height:1.48;";
      inner.appendChild(p);
      const ul = document.createElement("ul");
      ul.style.cssText = "padding-left:18px;font-size:12px;color:#334155;line-height:1.5;";
      (ch.sources || []).forEach((s) => ul.appendChild(mkEl("li", "", polishArrows(s))));
      inner.appendChild(ul);
      card.appendChild(inner);
      chGrid.appendChild(card);
    });
  }

  const archGrid = document.getElementById("archetypes-grid");
  if (archGrid) {
    archGrid.replaceChildren();
    (pb.diagram_archetypes_2d || []).forEach((a) => {
      const card = mkEl("div", "repo-card");
      const inner = mkEl("div");
      inner.appendChild(mkEl("span", "brand-badge", a.code));
      const h = mkEl("h3", "repo-card-title", a.name);
      h.style.margin = "8px 0 6px";
      inner.appendChild(h);
      const flow = mkEl("p", "", polishArrows(a.visual_flow));
      flow.style.cssText = "font-size:12.5px;color:#475569;margin-bottom:8px;";
      inner.appendChild(flow);
      const used = mkEl("div", "", `Exemplars: ${(a.used_in_posts || []).join(" · ")}`);
      used.style.cssText = "font-size:11.5px;font-weight:700;color:#1e40af;";
      inner.appendChild(used);
      card.appendChild(inner);
      archGrid.appendChild(card);
    });
  }
}

async function generateInCreatorStyle(styleCode, creatorName) {
  activateView("view-miner");
  activateMinerPanel("miner-panel-radar");
  const styleSelect = document.getElementById("daily-style-select");
  if (styleSelect) styleSelect.value = styleCode || "AUTO";
  showToast(`Generating fresh batch in ${creatorName}'s style (${styleCode})...`);
  await triggerGenerateDailyPosts();
}

function renderOpenHandsView() {
  const pb = STATE.playbook || {};
  const cmpTbody = document.getElementById("openhands-comparison-tbody");
  if (cmpTbody) {
    cmpTbody.replaceChildren();
    ((pb.openhands_superiority || {}).comparison || []).forEach((row) => {
      const tr = document.createElement("tr");
      [
        [row.dimension, "font-weight:700;color:#0f172a;"],
        [row.bmad_meta_prompts, "color:#991b1b;"],
        [row.openhands_autonomous, "font-weight:600;color:#065f46;"],
      ].forEach(([txt, st]) => {
        const td = document.createElement("td");
        const c = mkEl("div", "cell-card-equal");
        const sp = mkEl("span", "", txt);
        sp.style.cssText = `font-size:12.5px;${st}`;
        c.appendChild(sp);
        td.appendChild(c);
        tr.appendChild(td);
      });
      cmpTbody.appendChild(tr);
    });
  }

  const trajList = document.getElementById("openhands-trajectories-list");
  if (trajList) {
    trajList.replaceChildren();
    (STATE.repos || []).forEach((r) => {
      const t = r.openhands_trajectory || {};
      const box = mkEl("div", "feed-item-card");
      const top = mkEl("div", "composer-section-hdr");
      top.style.marginBottom = "8px";
      top.appendChild(mkEl("strong", "", `${r.id} — ${r.repo_slug}`));
      top.appendChild(mkEl("span", "pill-badge pill-emerald tabular-nums", `SHA ${r.git_commit_sha}`));
      box.appendChild(top);

      const chips = mkEl("div", "deliverable-chips");
      (t.steps || []).forEach((s) => {
        chips.appendChild(
          mkEl("span", "deliverable-chip chip-emerald tabular-nums", `${s.stage}: ${s.status} (${s.duration_ms}ms)`)
        );
      });
      box.appendChild(chips);
      trajList.appendChild(box);
    });
  }
}

/* ==========================================================================
   View 6: Video & 24-Slide Enablement Studio (MINT-01 .. MINT-12)
   ========================================================================== */
function seekMint01Video(seconds) {
  const vid = document.getElementById("mint01-walkthrough-video");
  if (!vid) return;
  try {
    vid.currentTime = Number(seconds) || 0;
  } catch (_) {}
}

function toggleMint01WalkthroughPlay() {
  const vid = document.getElementById("mint01-walkthrough-video");
  if (!vid) return;
  if (vid.paused) vid.play().catch(() => {});
  else vid.pause();
}

function toggleMint01WalkthroughMute() {
  const vid = document.getElementById("mint01-walkthrough-video");
  if (!vid) return;
  vid.muted = !vid.muted;
}

function toggleMint01TwinPlay() {
  const vid = document.getElementById("mint01-twin-video");
  if (!vid) return;
  if (vid.paused) vid.play().catch(() => {});
  else vid.pause();
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
  grid.replaceChildren();

  const studio = STATE.mintingStudio || {};
  const topics = studio.topics || [];
  const badge = document.getElementById("minting-topics-count-badge");
  if (badge && topics.length) {
    const mintedCount = topics.filter((t) => t.siso_decision === "MINT_NEW").length;
    badge.textContent = `${topics.length} Career-Minting Topics • ${mintedCount} Newly Minted (T85–T89)`;
  }

  topics.forEach((t) => {
    const sisoScore = t.siso_audit?.siso_score ?? t.nearest_prior_siso ?? 62.0;
    const decision = t.siso_audit?.decision || t.siso_decision || "MINT_NEW";
    const tid = t.canonical_template_id || "T85";
    const gslidesUrl = t.template_google_slides_url || "";
    const flagshipUrl = t.flagship_24slide_url || "";
    const svgUrl = `/assets/template-gallery/${tid}.svg?v=20261104`;

    const card = mkEl("article", "repo-card");
    card.setAttribute("data-testid", `mint-topic-card-${t.id}`);

    const top = mkEl("div");
    const stage = mkEl("div", "card-artwork-stage");
    stage.style.marginBottom = "12px";
    const im = document.createElement("img");
    im.src = svgUrl;
    im.alt = `${t.title} Blueprint ${tid}`;
    im.loading = "lazy";
    stage.appendChild(im);
    stage.appendChild(mkEl("span", "card-zoom-pill", `Zoom ${tid}`));
    stage.addEventListener("click", () =>
      openLightbox({
        kicker: `${t.id} · BLUEPRINT ${tid}`,
        title: t.title,
        imgUrl: svgUrl,
        actions: gslidesUrl ? [{ label: "Open Slides ↗", href: gslidesUrl, primary: true }] : [],
      })
    );
    top.appendChild(stage);

    const hdr = mkEl("div", "repo-card-header");
    hdr.style.marginBottom = "6px";
    hdr.appendChild(mkEl("span", "brand-badge", `${t.id} · ${t.mnemonic}`));
    if (STATE.persona === "builder") {
      hdr.appendChild(mkEl("span", "pill-badge pill-sky tabular-nums", `S_iso ${sisoScore} (${decision})`));
    } else {
      hdr.appendChild(mkEl("span", "pill-badge pill-emerald", `Blueprint ${tid}`));
    }
    top.appendChild(hdr);

    const h = mkEl("h3", "repo-card-title", polishUiTypography(t.title));
    h.style.marginBottom = "6px";
    top.appendChild(h);

    const mn = mkEl("div", "", `${t.mnemonic}: ${t.mnemonic_expansion}`);
    mn.style.cssText = "font-size:12px;font-weight:700;color:#1e40af;margin-bottom:5px;";
    top.appendChild(mn);

    top.appendChild(mkEl("p", "repo-card-hook", `Analogy: ${t.analogy}`));

    if (STATE.persona !== "creator") {
      const promo = mkEl("div", "", `Impact: ${t.promo_impact}`);
      promo.style.cssText = "margin-top:8px;font-size:12px;font-weight:600;color:#065f46;";
      top.appendChild(promo);
    }
    card.appendChild(top);

    const foot = mkEl("div", "repo-card-footer");
    const acts = mkEl("div", "studio-toolbar-actions");
    if (flagshipUrl) {
      const fl = mkEl("a", "btn-primary", "24-Slide Deck ↗");
      fl.href = safeUrl(flagshipUrl);
      fl.target = "_blank";
      fl.rel = "noopener";
      acts.appendChild(fl);
    } else if (gslidesUrl) {
      const gs = mkEl("a", "btn-secondary", `${tid} Slides ↗`);
      gs.href = safeUrl(gslidesUrl);
      gs.target = "_blank";
      gs.rel = "noopener";
      acts.appendChild(gs);
    }
    const pp = mkEl("a", "btn-secondary", ".pptx");
    pp.href = `/assets/template-gallery/${encodeURIComponent(tid)}.pptx`;
    pp.setAttribute("download", `${tid}.pptx`);
    acts.appendChild(pp);

    const repoBtn = mkEl("button", "btn-primary", "Inspect Repo →");
    repoBtn.type = "button";
    repoBtn.addEventListener("click", () => openRepoInspector(t.repo_slug));
    acts.appendChild(repoBtn);

    foot.appendChild(acts);
    card.appendChild(foot);
    grid.appendChild(card);
  });
}

/* ==========================================================================
   View 4 Sub-Panel 3: 6-Style Batch Generator & Signal Radar
   ========================================================================== */
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
    btn.textContent = "Synthesizing...";
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
    showToast(`Generated ${STATE.dailyPosts.length} creator-style posts & custom SVGs!`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Generate Batch";
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
  await copyTextSafe(fullPayload, `Copied Post + Comment #1 (${p.canonical_template_id})!`);
}

function renderDailyGeneratedPosts() {
  const grid = document.getElementById("daily-generated-posts-grid");
  if (!grid) return;
  grid.replaceChildren();
  const posts = STATE.dailyPosts || [];
  if (!posts.length) {
    grid.appendChild(mkEl("div", "section-description", "No batch posts yet — click Generate Batch above."));
    return;
  }

  posts.forEach((p, idx) => {
    const score = p.scores?.composite_score ?? 90;
    const card = mkEl("article", "daily-post-card");
    card.setAttribute("data-testid", `daily-post-card-${idx + 1}`);

    const top = mkEl("div");
    const hdr = mkEl("div", "repo-card-header");
    hdr.style.marginBottom = "8px";
    hdr.appendChild(mkEl("span", "brand-badge", `${p.style_code} · ${p.creator_inspiration} (${p.canonical_template_id})`));
    hdr.appendChild(mkEl("span", "pill-badge pill-emerald tabular-nums", `Score ${score}`));
    top.appendChild(hdr);

    const h = mkEl("h3", "repo-card-title", polishUiTypography(p.topic_title));
    h.style.marginBottom = "8px";
    top.appendChild(h);

    const stage = mkEl("div", "daily-visual-stage");
    stage.style.marginBottom = "10px";
    const vTabs = mkEl("div", "daily-visual-tabs");
    const bSvg = mkEl("button", "daily-visual-tab-btn active", "Topic Flow (.svg)");
    bSvg.type = "button";
    bSvg.id = `daily-vbtn-svg-${p.id}`;
    bSvg.addEventListener("click", () => switchDailyVisualTab(p.id, "svg"));

    const bPng = mkEl("button", "daily-visual-tab-btn", `${p.canonical_template_id} Poster (.png)`);
    bPng.type = "button";
    bPng.id = `daily-vbtn-png-${p.id}`;
    bPng.addEventListener("click", () => switchDailyVisualTab(p.id, "png"));
    vTabs.append(bSvg, bPng);
    stage.appendChild(vTabs);

    const imSvg = document.createElement("img");
    imSvg.id = `daily-vis-svg-${p.id}`;
    imSvg.src = `${safeUrl(p.custom_dynamic_svg_url)}?v=20261104`;
    imSvg.alt = `Custom flow SVG for ${p.topic_title}`;
    imSvg.style.cssText = "width:100%;height:auto;display:block;border-radius:6px;background:#ffffff;";
    imSvg.loading = "lazy";

    const imPng = document.createElement("img");
    imPng.id = `daily-vis-png-${p.id}`;
    imPng.src = `${safeUrl(p.canonical_png_url)}?v=20261104`;
    imPng.alt = `Canonical ${p.canonical_template_id} poster`;
    imPng.style.cssText = "width:100%;height:auto;display:none;border-radius:6px;background:#ffffff;";
    imPng.loading = "lazy";

    stage.append(imSvg, imPng);
    top.appendChild(stage);

    const copyBox = mkEl("div", "daily-post-copy-box", `${polishUiTypography(p.linkedin_post_text)}\n\n${p.hashtags || ""}`);
    copyBox.id = `daily-copy-text-${p.id}`;
    top.appendChild(copyBox);
    card.appendChild(top);

    const foot = mkEl("div", "repo-card-footer");
    const copyBtn = mkEl("button", "btn-primary copy-daily-post-btn", "Copy Post + Source");
    copyBtn.type = "button";
    copyBtn.setAttribute("data-testid", `copy-daily-post-btn-${idx + 1}`);
    copyBtn.addEventListener("click", () => copyDailyPostText(p.id));

    const links = mkEl("div", "studio-toolbar-actions");
    const svgA = mkEl("a", "btn-secondary", "SVG ↗");
    svgA.href = safeUrl(p.custom_dynamic_svg_url);
    svgA.target = "_blank";
    links.appendChild(svgA);
    if (p.google_slides_url) {
      const gsA = mkEl("a", "btn-secondary", "Slides ↗");
      gsA.href = safeUrl(p.google_slides_url);
      gsA.target = "_blank";
      links.appendChild(gsA);
    }
    foot.append(copyBtn, links);
    card.appendChild(foot);
    grid.appendChild(card);
  });
}

async function refreshLiveFeeds() {
  const res = await fetch("/api/live-mining-feeds");
  const data = await res.json();

  const axList = document.getElementById("live-arxiv-list");
  if (axList) {
    axList.replaceChildren();
    (data.arxiv || []).forEach((item) => {
      const box = mkEl("div", "feed-item-card");
      const hdr = mkEl("div", "composer-section-hdr");
      hdr.style.marginBottom = "4px";
      hdr.appendChild(mkEl("span", "brand-badge", item.source_channel));
      const dt = mkEl("span", "tabular-nums", item.published_at);
      dt.style.cssText = "font-size:11.5px;color:#475569;";
      hdr.appendChild(dt);
      const t = mkEl("div", "", polishUiTypography(item.title));
      t.style.cssText = "font-size:13.5px;font-weight:700;color:#0f172a;margin-bottom:4px;";
      const s = mkEl("div", "", polishUiTypography(item.summary));
      s.style.cssText = "font-size:12px;color:#475569;margin-bottom:6px;";
      const a = mkEl("a", "", "Read on arXiv ↗");
      a.href = safeUrl(item.primary_url);
      a.target = "_blank";
      a.rel = "noopener";
      a.style.cssText = "font-size:12px;font-weight:700;color:#1d4ed8;text-decoration:none;";
      box.append(hdr, t, s, a);
      axList.appendChild(box);
    });
  }

  const ghList = document.getElementById("live-github-list");
  if (ghList) {
    ghList.replaceChildren();
    (data.github || []).forEach((repo) => {
      const box = mkEl("div", "feed-item-card");
      const hdr = mkEl("div", "composer-section-hdr");
      hdr.style.marginBottom = "4px";
      hdr.appendChild(mkEl("strong", "", repo.full_name));
      hdr.appendChild(mkEl("span", "pill-badge pill-amber tabular-nums", `★ ${repo.stars}`));
      const d = mkEl("div", "", repo.description);
      d.style.cssText = "font-size:12px;color:#475569;margin-bottom:6px;";
      const a = mkEl("a", "", "Open GitHub Repo ↗");
      a.href = safeUrl(repo.html_url);
      a.target = "_blank";
      a.rel = "noopener";
      a.style.cssText = "font-size:12px;font-weight:700;color:#1d4ed8;text-decoration:none;";
      box.append(hdr, d, a);
      ghList.appendChild(box);
    });
  }
}

/* ==========================================================================
   View 4 (Primary): Daily Top-5 Studio, Visual Blueprint Picker & Live Mockups
   ========================================================================== */
function getActiveTop5Idea() {
  const ideas = STATE.top5Briefing?.ideas || [];
  return ideas.find((i) => i.id === STATE.selectedIdeaId) || ideas[0] || null;
}

function getActiveTop5Template(idea) {
  if (!idea) return null;
  const list = idea.matching_templates || [];
  return list.find((t) => t.template_id === STATE.selectedTemplateId) || list[0] || null;
}

function formatModeDisplayName(modeKey) {
  const map = {
    Carousel: "Carousel",
    Image: "Image",
    Short_Video: "Short Video",
    Video: "16:9 Video",
    Slidedeck: "Slide Deck",
    Slide: "1-Slide BLUF",
    Doc: "Tech Doc",
    Text: "Text / Thread",
  };
  return map[modeKey] || String(modeKey || "").replace(/_/g, " ");
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
    if (!existing) {
      STATE.selectedMode = chosen.default_recommended_mode || "Carousel";
    }
  }
  const edBadge = document.getElementById("top5-edition-badge");
  if (edBadge && STATE.top5Briefing) {
    edBadge.textContent = `${STATE.top5Briefing.ideas_count || 5} Unique Signals · Edition ${STATE.top5Briefing.edition_date || ""}`;
  }
  const ledgerBadge = document.getElementById("top5-ledger-badge");
  if (ledgerBadge && STATE.top5Briefing) {
    ledgerBadge.textContent = `30-Day Dedupe (${STATE.top5Briefing.dedupe_ledger_entries || 5} tracked · ${STATE.top5Briefing.certified_pool_size || 116} blueprints)`;
  }
  STATE.activeCarouselIndex = 0;
  STATE.mockupCopyExpanded = false;
  renderTop5EditorialDesk();
  renderPublishingOutbox();
}

async function triggerGenerateTop5Briefing() {
  const btn = document.getElementById("generate-top5-briefing-btn");
  const qInput = document.getElementById("top5-query-input");
  const topic_query = (qInput?.value || "").trim();
  if (btn) {
    btn.disabled = true;
    btn.textContent = "Refreshing...";
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
    showToast("Refreshed Today's Top 5 Signals & Certified Blueprints!");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Refresh Top 5";
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
    STATE.activeCarouselIndex = 0;
    renderTop5ComposerCopySection();
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
    btn.textContent = "Rendering Media...";
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
      showToast(`Rendered 4:5 Carousel & 9:16 Safe-Zone Short MP4 for ${idea.id}!`);
    } else {
      showToast(out.error || "Media transcode did not complete");
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Rebuild 4:5 & 9:16 Media";
    }
  }
}

async function stageSelectedPlatformsToOutbox() {
  const idea = getActiveTop5Idea();
  const tpl = getActiveTop5Template(idea);
  if (!idea || !tpl) return;
  const platforms = Array.from(STATE.selectedStagePlatforms);
  if (!platforms.length) {
    showToast("Check at least one target channel first");
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
    showToast(`Staged ${platforms.length} channel packages to Publishing Queue!`);
  } else {
    showToast(data.error || "Unable to stage channel packages");
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
    showToast(`Validated & processed ${count} queue package(s)!`);
  }
}

function renderTop5EditorialDesk() {
  const ideasCol = document.getElementById("top5-ideas-column");
  const workbench = document.getElementById("top5-active-workbench");
  const channelMount = document.getElementById("top5-channel-selector-mount");
  if (!ideasCol || !workbench || !channelMount) return;

  ideasCol.replaceChildren();
  workbench.replaceChildren();
  channelMount.replaceChildren();

  const ideas = STATE.top5Briefing?.ideas || [];
  if (!ideas.length) {
    ideasCol.appendChild(mkEl("div", "section-description", "Loading today's Top 5 signals..."));
    return;
  }

  // Column 1: 5 Ranked Signal Cards
  ideas.forEach((idea, idx) => {
    const isAct = idea.id === STATE.selectedIdeaId;
    const card = mkEl("button", `top5-idea-card${isAct ? " active" : ""}`);
    card.type = "button";
    card.setAttribute("data-testid", `top5-idea-card-${idx + 1}`);

    const metaRow = mkEl("div", "idea-card-meta-row");
    metaRow.appendChild(mkEl("span", "idea-rank-cluster tabular-nums", `0${idea.rank} · ${idea.cluster_label}`));
    metaRow.appendChild(
      mkEl("span", "idea-demand-score tabular-nums", `${idea.scores?.demand_score ?? 94}`)
    );
    card.appendChild(metaRow);

    card.appendChild(mkEl("div", "idea-card-headline", polishUiTypography(idea.title)));
    card.appendChild(mkEl("div", "idea-card-summary", polishUiTypography(idea.summary)));

    const hintRow = mkEl("div", "idea-card-format-hint");
    hintRow.appendChild(mkEl("span", "", `★ ${formatModeDisplayName(idea.default_recommended_mode)}`));
    hintRow.appendChild(mkEl("span", "tabular-nums", idea.default_template_id || "T85"));
    card.appendChild(hintRow);

    card.addEventListener("click", async () => {
      STATE.selectedIdeaId = idea.id;
      STATE.selectedTemplateId = idea.default_template_id;
      STATE.selectedMode = idea.default_recommended_mode || "Carousel";
      STATE.activeCarouselIndex = 0;
      STATE.mockupCopyExpanded = false;
      renderTop5EditorialDesk();
      await refreshPlatformPreviewPackages();
    });
    ideasCol.appendChild(card);
  });

  const activeIdea = getActiveTop5Idea();
  const activeTpl = getActiveTop5Template(activeIdea);
  if (!activeIdea || !activeTpl) return;

  // Column 2: Center Editorial & Visual Blueprint Composer
  const ideaHdr = mkEl("div", "composer-idea-header");
  const kickerRow = mkEl("div", "composer-idea-kicker");
  kickerRow.appendChild(
    mkEl("span", "", polishUiTypography(`SIGNAL 0${activeIdea.rank} · ${activeIdea.source_channel}`))
  );
  const srcA = mkEl("a", "eyebrow-link", "Primary Source ↗");
  srcA.href = safeUrl(activeIdea.primary_url);
  srcA.target = "_blank";
  srcA.rel = "noopener";
  kickerRow.appendChild(srcA);
  ideaHdr.appendChild(kickerRow);
  ideaHdr.appendChild(mkEl("h2", "composer-idea-title", polishUiTypography(activeIdea.title)));
  ideaHdr.appendChild(
    mkEl("p", "composer-idea-impact", polishUiTypography(activeIdea.metrics_hint || activeIdea.summary))
  );
  workbench.appendChild(ideaHdr);

  // Step 1: Visual 5-Blueprint Thumbnail Strip
  const step1 = mkEl("div", "composer-section");
  const s1Hdr = mkEl("div", "composer-section-hdr");
  s1Hdr.appendChild(mkEl("span", "composer-step-title", "1. Visual Blueprint"));

  const s1Actions = mkEl("div", "studio-toolbar-actions");
  if (STATE.persona === "builder") {
    [
      [".drawio", `/assets/template-gallery/${activeTpl.template_id}.drawio`],
      [".pptx", `/assets/template-gallery/${activeTpl.template_id}.pptx`],
      ["SVG", `/assets/template-gallery/${activeTpl.template_id}.svg`],
    ].forEach(([lbl, href]) => {
      const a = mkEl("a", "deliverable-chip chip-blue", lbl);
      a.style.textDecoration = "none";
      a.href = safeUrl(href);
      a.target = "_blank";
      a.rel = "noopener";
      s1Actions.appendChild(a);
    });
  }
  const zoomBtn = mkEl("button", "btn-secondary", `Full Size (${activeTpl.template_id})`);
  zoomBtn.type = "button";
  zoomBtn.style.cssText = "min-height:28px;padding:3px 9px;font-size:11.5px;white-space:nowrap;";
  zoomBtn.addEventListener("click", () => {
    openLightbox({
      kicker: `${activeTpl.template_id} · ${activeTpl.angle_label || "CERTIFIED BLUEPRINT"}`,
      title: `${activeTpl.template_id} — ${activeTpl.name}`,
      imgUrl: `/assets/template-gallery/${activeTpl.template_id}.svg?v=20261104`,
      actions: [
        {
          label: "Download .pptx",
          href: `/assets/template-gallery/${activeTpl.template_id}.pptx`,
          download: `${activeTpl.template_id}.pptx`,
        },
        {
          label: "Open SVG ↗",
          href: `/assets/template-gallery/${activeTpl.template_id}.svg`,
        },
      ],
    });
  });
  s1Actions.appendChild(zoomBtn);
  s1Hdr.appendChild(s1Actions);
  step1.appendChild(s1Hdr);

  const builderSiso = document.getElementById("builder-kpi-siso");
  if (builderSiso) {
    builderSiso.textContent = `${activeTpl.template_id} · Score ${activeTpl.match_score || "99.2"}`;
  }

  const bpGrid = mkEl("div", "top5-blueprint-grid");
  bpGrid.setAttribute("data-testid", "top5-template-pills");
  (activeIdea.matching_templates || []).forEach((tpl, tIdx) => {
    const isSel = tpl.template_id === activeTpl.template_id;
    const btn = mkEl("button", `blueprint-thumb-btn${isSel ? " active" : ""}`);
    btn.type = "button";
    btn.setAttribute("data-testid", `top5-tpl-pill-${tIdx + 1}`);
    btn.title = `${tpl.template_id}: ${tpl.name} (Recommended: ${tpl.recommended_mode})`;

    const frame = mkEl("div", "blueprint-thumb-frame");
    const thImg = document.createElement("img");
    thImg.src = `/assets/template-gallery/${encodeURIComponent(tpl.template_id)}.png?v=20261104`;
    thImg.alt = `${tpl.template_id} ${tpl.name}`;
    thImg.loading = "lazy";
    frame.appendChild(thImg);
    if (tIdx === 0) {
      frame.appendChild(mkEl("span", "blueprint-rec-dot", "Best"));
    }
    btn.appendChild(frame);
    btn.appendChild(mkEl("div", "blueprint-thumb-id tabular-nums", tpl.template_id));
    btn.appendChild(
      mkEl("div", "blueprint-thumb-angle", tpl.angle_label || formatModeDisplayName(tpl.recommended_mode))
    );

    btn.addEventListener("click", async () => {
      STATE.selectedTemplateId = tpl.template_id;
      if (tpl.recommended_mode) STATE.selectedMode = tpl.recommended_mode;
      STATE.activeCarouselIndex = 0;
      renderTop5EditorialDesk();
      await refreshPlatformPreviewPackages();
    });
    bpGrid.appendChild(btn);
  });
  step1.appendChild(bpGrid);

  const bpCaption = mkEl(
    "div",
    "composer-step-sub",
    `${activeTpl.template_id}: ${activeTpl.name} · Recommended format: ${formatModeDisplayName(activeTpl.recommended_mode || activeIdea.default_recommended_mode)}`
  );
  step1.appendChild(bpCaption);
  workbench.appendChild(step1);

  // Step 2: 8 Presentation Modes + Calm 3-Metric Pacing Bar
  const step2 = mkEl("div", "composer-section");
  const s2Hdr = mkEl("div", "composer-section-hdr");
  s2Hdr.appendChild(mkEl("span", "composer-step-title", "2. Presentation Format & Content Pacing"));
  step2.appendChild(s2Hdr);

  const modeRow = mkEl("div", "top5-pill-row");
  modeRow.setAttribute("data-testid", "top5-mode-pills");
  const modeKeys = ["Carousel", "Image", "Short_Video", "Video", "Slidedeck", "Slide", "Doc", "Text"];
  const recMode = activeTpl.recommended_mode || activeIdea.default_recommended_mode;
  modeKeys.forEach((mKey) => {
    const isSel = STATE.selectedMode === mKey;
    const isRec = recMode === mKey;
    const pill = mkEl(
      "button",
      `top5-selector-pill${isSel ? " active" : ""}${isRec ? " recommended" : ""}`,
      `${isRec ? "★ " : ""}${formatModeDisplayName(mKey)}`
    );
    pill.type = "button";
    pill.setAttribute("data-testid", `top5-mode-pill-${mKey}`);
    pill.addEventListener("click", async () => {
      STATE.selectedMode = mKey;
      STATE.activeCarouselIndex = 0;
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
    ["Above-Fold Hook", budget.hook_above_fold || "Front-loaded metric hook"],
    ["Per-Unit Density", budget.per_unit_density || "Bounded visual density"],
    [
      `Deliverable (${budget.estimated_consumption_time || "Fast read"})`,
      budget.total_deliverable_size || "Platform-calibrated asset",
    ],
  ].forEach(([bTitle, bVal]) => {
    const bCard = mkEl("div", "top5-budget-card");
    bCard.appendChild(mkEl("div", "top5-budget-card-title", bTitle));
    bCard.appendChild(mkEl("div", "top5-budget-card-val", bVal));
    budgetGrid.appendChild(bCard);
  });
  step2.appendChild(budgetGrid);
  workbench.appendChild(step2);

  // Step 3: Channel Copy Mount inside Center Composer
  const copyMount = mkEl("div", "composer-copy-card");
  copyMount.id = "top5-composer-copy-mount";
  workbench.appendChild(copyMount);

  // Column 3 Top: 13-Channel Selector Card + Stage CTA
  const chCard = mkEl("div", "channel-selector-card");
  const chHdr = mkEl("div", "composer-section-hdr");
  chHdr.appendChild(
    mkEl("span", "composer-step-title tabular-nums", `3. Channels (${STATE.selectedStagePlatforms.size} checked)`)
  );
  const stageBtn = mkEl("button", "btn-primary", `Stage to Queue (${STATE.selectedStagePlatforms.size})`);
  stageBtn.type = "button";
  stageBtn.id = "stage-selected-platforms-btn";
  stageBtn.setAttribute("data-testid", "stage-selected-platforms-btn");
  stageBtn.addEventListener("click", stageSelectedPlatformsToOutbox);
  chHdr.appendChild(stageBtn);
  chCard.appendChild(chHdr);

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
    const shortName = pSpec.name.split("(")[0].trim();
    const isAct = STATE.selectedPreviewPlatform === pid;
    const tabBtn = mkEl("button", `top5-unified-channel-chip${isAct ? " active" : ""}`);
    tabBtn.type = "button";
    tabBtn.setAttribute("data-testid", `top5-plat-tab-${pid}`);

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = STATE.selectedStagePlatforms.has(pid);
    cb.setAttribute("aria-label", `Include ${shortName} when staging to Publishing Queue`);
    cb.title = `Include ${shortName} when staging to Publishing Queue`;
    cb.setAttribute("data-testid", `stage-check-${pid}`);
    cb.addEventListener("click", (ev) => ev.stopPropagation());
    cb.addEventListener("change", () => {
      if (cb.checked) STATE.selectedStagePlatforms.add(pid);
      else STATE.selectedStagePlatforms.delete(pid);
      stageBtn.textContent = `Stage to Queue (${STATE.selectedStagePlatforms.size})`;
    });
    tabBtn.appendChild(cb);
    tabBtn.appendChild(mkEl("span", "", shortName));

    tabBtn.addEventListener("click", () => {
      STATE.selectedPreviewPlatform = pid;
      STATE.activeCarouselIndex = 0;
      STATE.mockupCopyExpanded = false;
      previewTabs.querySelectorAll(".top5-unified-channel-chip").forEach((b) => {
        b.classList.toggle("active", b === tabBtn);
      });
      renderTop5ComposerCopySection();
      renderTop5PlatformPreviewStage();
    });
    previewTabs.appendChild(tabBtn);
  });
  chCard.appendChild(previewTabs);
  channelMount.appendChild(chCard);

  renderTop5ComposerCopySection();
  renderTop5PlatformPreviewStage();
}

function renderTop5ComposerCopySection() {
  const mount = document.getElementById("top5-composer-copy-mount");
  if (!mount) return;
  mount.replaceChildren();

  const pkg = STATE.previewPackagesByPlatform[STATE.selectedPreviewPlatform];
  if (!pkg) {
    mount.appendChild(mkEl("div", "section-description", "Preparing channel copy..."));
    return;
  }

  const checks = pkg.compliance_checks || {};
  const hdr = mkEl("div", "composer-section-hdr");
  hdr.style.marginBottom = "8px";
  const leftMeta = mkEl("div", "studio-toolbar-actions");
  leftMeta.appendChild(mkEl("span", "composer-step-title", `${pkg.platform_name.split("(")[0].trim()} Copy`));
  leftMeta.appendChild(
    mkEl(
      "span",
      `pill-badge tabular-nums ${checks.char_limit_ok ? "pill-emerald" : "pill-amber"}`,
      `${checks.char_used}/${checks.char_cap} chars ✓`
    )
  );
  hdr.appendChild(leftMeta);

  const copyBtn = mkEl("button", "btn-secondary", "Copy Channel Payload");
  copyBtn.type = "button";
  copyBtn.style.cssText = "min-height:30px;padding:4px 10px;font-size:12px;";
  copyBtn.addEventListener("click", () => {
    const combined = pkg.follow_up_comment
      ? `${pkg.body}\n\n---\n${pkg.follow_up_comment}`
      : pkg.body;
    copyTextSafe(combined, `Copied ${pkg.platform_name} payload!`);
  });
  hdr.appendChild(copyBtn);
  mount.appendChild(hdr);

  if (pkg.video_title) {
    const vt = mkEl("div", "", `Video Title (${pkg.video_title.length}/100): ${polishUiTypography(pkg.video_title)}`);
    vt.style.cssText = "font-size:12px;font-weight:700;color:#0f172a;margin-bottom:6px;";
    mount.appendChild(vt);
  }

  const bodyBox = mkEl("div", "top5-copy-full-box", polishUiTypography(pkg.body));
  bodyBox.setAttribute("data-testid", "top5-platform-copy-box");
  mount.appendChild(bodyBox);

  if (pkg.follow_up_comment) {
    mount.appendChild(
      mkEl("div", "composer-followup-note", `First Comment / Reply #2: ${pkg.follow_up_comment}`)
    );
  }

  const details = document.createElement("details");
  details.className = "composer-guardrail-details";
  if (STATE.persona === "builder") details.open = true;
  const sum = mkEl("summary", "", `Platform Compliance Guardrail (${pkg.link_strategy})`);
  const gBody = mkEl("div", "composer-guardrail-body", pkg.compliance_note);
  details.append(sum, gBody);

  if (STATE.persona === "builder") {
    const builderApi = document.getElementById("builder-kpi-api");
    if (builderApi) {
      builderApi.textContent = `${STATE.selectedPreviewPlatform.toUpperCase()} · ${pkg.tier || "TIER_1"}`;
    }
    if ((pkg.missing_env_vars || []).length > 0) {
      const envDiv = mkEl(
        "div",
        "",
        `Live API env vars: ${pkg.missing_env_vars.join(", ")} (currently Dry-Run Validated)`
      );
      envDiv.style.cssText = "margin-top:6px;font-family:var(--theme-font-mono,monospace);font-size:11px;color:#475569;";
      details.appendChild(envDiv);
    }
    const jsonPreview = mkEl(
      "pre",
      "code-block-light",
      JSON.stringify(
        {
          platform_id: pkg.platform_id,
          tier: pkg.tier,
          effective_mode: pkg.effective_mode,
          link_strategy: pkg.link_strategy,
          media_container: pkg.media?.container_format,
          primary_asset_url: pkg.media?.primary_asset_url,
          compliance_checks: pkg.compliance_checks,
        },
        null,
        2
      )
    );
    jsonPreview.style.cssText = "margin-top:8px;max-height:140px;font-size:11px;padding:8px 10px;";
    details.appendChild(jsonPreview);
  }
  mount.appendChild(details);
}

function renderTop5PlatformPreviewStage() {
  const stage = document.getElementById("top5-platform-preview-stage");
  if (!stage) return;
  stage.replaceChildren();

  const pkg = STATE.previewPackagesByPlatform[STATE.selectedPreviewPlatform];
  if (!pkg) {
    stage.appendChild(mkEl("div", "studio-surface", "Compiling live channel preview..."));
    return;
  }

  const media = pkg.media || {};
  const checks = pkg.compliance_checks || {};
  const pid = STATE.selectedPreviewPlatform;
  const isVertical9x16 = String(media.aspect_ratio || "").includes("9:16");
  const isMessaging = pid === "whatsapp" || pid === "telegram";

  const mockup = mkEl("div", "social-mockup-card");

  // Top Chrome Bar of Live Mockup
  const chrome = mkEl("div", "mockup-chrome-bar");
  chrome.appendChild(mkEl("span", "", `Live ${pkg.platform_name.split("(")[0].trim()} Preview`));
  if (isVertical9x16) {
    const szBtn = mkEl(
      "button",
      "btn-secondary",
      STATE.showSafeZoneOverlay ? "Safe-Zone Guides: ON" : "Safe-Zone Guides: OFF"
    );
    szBtn.type = "button";
    szBtn.style.cssText = "min-height:24px;padding:2px 8px;font-size:11px;";
    szBtn.addEventListener("click", () => {
      STATE.showSafeZoneOverlay = !STATE.showSafeZoneOverlay;
      renderTop5PlatformPreviewStage();
    });
    chrome.appendChild(szBtn);
  } else {
    chrome.appendChild(
      mkEl("span", "pill-badge pill-emerald tabular-nums", `Fold ${checks.fold_used}/${checks.fold_cap} ✓`)
    );
  }
  mockup.appendChild(chrome);

  // Author Header (for Feed & Microblog Channels)
  if (!isVertical9x16) {
    const authorRow = mkEl("div", "mockup-author-row");
    authorRow.appendChild(mkEl("span", "mockup-avatar", "NA"));
    const aMeta = mkEl("div", "min-w-0");
    aMeta.appendChild(mkEl("div", "mockup-author-name", "Nitin Aggarwal"));
    aMeta.appendChild(
      mkEl(
        "div",
        "mockup-author-sub",
        isMessaging ? "Broadcast Channel · 08:30 EST ✓✓" : "AI Systems & Cloud Architecture · Just now"
      )
    );
    authorRow.appendChild(aMeta);
    mockup.appendChild(authorRow);

    // Realistic Above-the-Fold Copy Preview with word-boundary "…more"
    const cleanBody = polishUiTypography(pkg.body || "");
    const foldCap = Math.max(90, checks.fold_cap || 180);
    const copyDiv = mkEl("div", "mockup-post-copy");
    if (!STATE.mockupCopyExpanded && cleanBody.length > foldCap) {
      let cut = cleanBody.slice(0, foldCap);
      const lastSpace = cut.lastIndexOf(" ");
      if (lastSpace > foldCap * 0.65) {
        cut = cut.slice(0, lastSpace);
      }
      cut = cut.replace(/[,:;.\-–—\s]+$/, "");
      copyDiv.appendChild(document.createTextNode(`${cut}… `));
      const moreBtn = mkEl("button", "mockup-more-btn", "more");
      moreBtn.type = "button";
      moreBtn.addEventListener("click", () => {
        STATE.mockupCopyExpanded = true;
        renderTop5PlatformPreviewStage();
      });
      copyDiv.appendChild(moreBtn);
    } else {
      copyDiv.appendChild(document.createTextNode(cleanBody));
      if (cleanBody.length > foldCap) {
        const lessBtn = mkEl("button", "mockup-more-btn", " show less");
        lessBtn.type = "button";
        lessBtn.addEventListener("click", () => {
          STATE.mockupCopyExpanded = false;
          renderTop5PlatformPreviewStage();
        });
        copyDiv.appendChild(lessBtn);
      }
    }
    mockup.appendChild(copyDiv);
  }

  // Media Stage: 9:16 Smartphone Bezel OR 16:9 Video OR Interactive Carousel/Slide Deck OR Retina Image
  const slides = media.slide_urls || [];
  const activeSlideIdx = Math.min(STATE.activeCarouselIndex, Math.max(0, slides.length - 1));

  if (isVertical9x16) {
    const phoneOuter = mkEl("div", "phone-stage-outer");
    const bezel = mkEl("div", "phone-bezel-frame");
    const screen = mkEl("div", "phone-screen-9x16");

    if (media.container_format === "MP4" && media.primary_asset_url) {
      const vid = document.createElement("video");
      vid.muted = true;
      vid.playsInline = true;
      vid.preload = "metadata";
      if (media.poster_url) vid.poster = safeUrl(media.poster_url);
      vid.src = safeUrl(media.primary_asset_url);
      screen.appendChild(vid);

      if (media.poster_url) {
        const posterCover = mkEl("button", "phone-poster-cover");
        posterCover.type = "button";
        posterCover.setAttribute("aria-label", "Play 9:16 vertical short video preview");
        const pImg = document.createElement("img");
        pImg.src = safeUrl(media.poster_url);
        pImg.alt = `${pkg.platform_name} 9:16 Safe-Zone video cover`;
        posterCover.appendChild(pImg);
        posterCover.appendChild(mkEl("span", "phone-play-pill", "▶ Play 9:16 Reel · 0:43"));
        posterCover.addEventListener("click", () => {
          posterCover.remove();
          vid.controls = true;
          vid.muted = false;
          vid.play().catch(() => {});
        });
        screen.appendChild(posterCover);
      } else {
        vid.controls = true;
      }
    } else if (slides.length > 0) {
      const im = document.createElement("img");
      im.src = safeUrl(slides[activeSlideIdx]);
      im.alt = `${pkg.platform_name} vertical slide ${activeSlideIdx + 1}`;
      screen.appendChild(im);
    } else if (media.preview_image_url) {
      const im = document.createElement("img");
      im.src = safeUrl(media.preview_image_url);
      im.alt = `${pkg.platform_name} vertical preview`;
      screen.appendChild(im);
    }

    const szOverlay = mkEl(
      "div",
      `safe-zone-overlay${STATE.showSafeZoneOverlay ? " visible" : ""}`
    );
    szOverlay.append(
      mkEl("div", "safe-zone-top"),
      mkEl("div", "safe-zone-right"),
      mkEl("div", "safe-zone-bottom")
    );
    screen.appendChild(szOverlay);
    bezel.appendChild(screen);
    phoneOuter.appendChild(bezel);
    mockup.appendChild(phoneOuter);

    if (slides.length > 1) {
      appendCarouselScrubber(mockup, slides, activeSlideIdx, pkg.platform_name);
    }
  } else if (media.container_format === "MP4" && media.primary_asset_url) {
    const vp = mkEl("div", "mockup-media-viewport");
    const vid = document.createElement("video");
    vid.controls = true;
    vid.muted = true;
    vid.playsInline = true;
    vid.preload = "metadata";
    if (media.poster_url) vid.poster = safeUrl(media.poster_url);
    vid.src = safeUrl(media.primary_asset_url);
    vp.appendChild(vid);
    mockup.appendChild(vp);
  } else if (slides.length > 0) {
    const vp = mkEl("div", "mockup-media-viewport");
    const heroImg = document.createElement("img");
    heroImg.src = safeUrl(slides[activeSlideIdx]);
    heroImg.alt = `${pkg.platform_name} Slide ${activeSlideIdx + 1} Preview`;
    heroImg.addEventListener("click", () =>
      openLightbox({
        kicker: `${pkg.platform_name.toUpperCase()} · SLIDE ${activeSlideIdx + 1} OF ${slides.length}`,
        title: pkg.idea_title || "Slide Preview",
        imgUrl: slides[activeSlideIdx],
        actions: media.primary_asset_url
          ? [{ label: `Download ${media.container_format}`, href: media.primary_asset_url, primary: true }]
          : [],
      })
    );
    vp.appendChild(heroImg);
    mockup.appendChild(vp);
    appendCarouselScrubber(mockup, slides, activeSlideIdx, pkg.platform_name);
  } else if (media.preview_image_url) {
    const vp = mkEl("div", "mockup-media-viewport");
    const im = document.createElement("img");
    im.src = safeUrl(media.preview_image_url);
    im.alt = `${pkg.platform_name} Visual Preview`;
    im.addEventListener("click", () =>
      openLightbox({
        kicker: `${pkg.platform_name.toUpperCase()} · VISUAL PREVIEW`,
        title: pkg.idea_title || "Blueprint Preview",
        imgUrl: media.blueprint_svg_url || media.preview_image_url,
        actions: media.primary_asset_url
          ? [{ label: `Open ${media.container_format} ↗`, href: media.primary_asset_url, primary: true }]
          : [],
      })
    );
    vp.appendChild(im);
    mockup.appendChild(vp);
  }

  // Platform-Authentic Engagement / Asset Action Footer
  const actFooter = mkEl("div", "mockup-actions-footer");
  let socialEngagementLabel = "👍 Like   ·   💬 Comment   ·   🔁 Repost";
  if (isMessaging) {
    socialEngagementLabel = "✓✓ Verified Broadcast Packet";
  } else if (pid === "youtube_shorts" || pid === "youtube") {
    socialEngagementLabel = "▶ Shorts Feed   ·   👍 Like   ·   ↗ Share";
  } else if (pid === "instagram" || pid === "tiktok") {
    socialEngagementLabel = "♡ Like   ·   💬 Comment   ·   🔖 Save";
  } else if (pid === "x" || pid === "bluesky") {
    socialEngagementLabel = "💬 Reply   ·   🔁 Repost   ·   ♡ Like";
  } else if (pid === "devto" || pid === "hashnode" || pid === "substack") {
    socialEngagementLabel = "📖 Engineering Article   ·   🔖 Bookmark";
  }
  actFooter.appendChild(mkEl("span", "", socialEngagementLabel));
  const dlWrap = mkEl("div", "studio-toolbar-actions");
  if (media.primary_asset_url) {
    const openAsset = mkEl("a", "btn-secondary", `${media.container_format} Asset ↗`);
    openAsset.style.cssText = "min-height:28px;padding:3px 9px;font-size:11.5px;";
    openAsset.href = safeUrl(media.primary_asset_url);
    openAsset.target = "_blank";
    openAsset.rel = "noopener";
    dlWrap.appendChild(openAsset);
  }
  if (pkg.share_intent_url) {
    const sh = mkEl("a", "btn-secondary", "1-Click Share ↗");
    sh.style.cssText = "min-height:28px;padding:3px 9px;font-size:11.5px;";
    sh.href = safeUrl(pkg.share_intent_url);
    sh.target = "_blank";
    sh.rel = "noopener";
    dlWrap.appendChild(sh);
  }
  actFooter.appendChild(dlWrap);
  mockup.appendChild(actFooter);

  // Clean Spec Strip (Preserves Exact E2E Container & Aspect Ratio Telemetry)
  const specStrip = mkEl("div", "mockup-spec-strip");
  specStrip.appendChild(
    mkEl("span", "pill-badge pill-emerald", `Container: ${media.container_format} • ${media.aspect_ratio}`)
  );
  specStrip.appendChild(mkEl("span", "pill-badge pill-sky", pkg.tier_badge || pkg.tier));
  if (pkg.mode_auto_adapted) {
    specStrip.appendChild(
      mkEl("span", "pill-badge pill-amber", `Adapted: ${pkg.requested_mode} → ${pkg.effective_mode}`)
    );
  }
  mockup.appendChild(specStrip);

  stage.appendChild(mockup);
}

function appendCarouselScrubber(mockup, slides, activeSlideIdx, platformName) {
  const nav = mkEl("div", "carousel-nav-strip");
  const prevBtn = mkEl("button", "btn-secondary", "‹ Prev");
  prevBtn.type = "button";
  prevBtn.style.cssText = "min-height:26px;padding:2px 8px;font-size:11px;";
  prevBtn.addEventListener("click", () => {
    STATE.activeCarouselIndex = (activeSlideIdx - 1 + slides.length) % slides.length;
    renderTop5PlatformPreviewStage();
  });

  const counter = mkEl("span", "tabular-nums", `Slide ${activeSlideIdx + 1} of ${slides.length}`);

  const nextBtn = mkEl("button", "btn-secondary", "Next ›");
  nextBtn.type = "button";
  nextBtn.style.cssText = "min-height:26px;padding:2px 8px;font-size:11px;";
  nextBtn.addEventListener("click", () => {
    STATE.activeCarouselIndex = (activeSlideIdx + 1) % slides.length;
    renderTop5PlatformPreviewStage();
  });

  nav.append(prevBtn, counter, nextBtn);
  mockup.appendChild(nav);

  const thumbs = mkEl("div", "top5-carousel-thumbs");
  slides.slice(0, 8).forEach((sUrl, sIdx) => {
    const th = document.createElement("img");
    th.src = safeUrl(sUrl);
    th.alt = `${platformName} Slide ${sIdx + 1}`;
    th.title = `Slide ${sIdx + 1} of ${slides.length}`;
    if (sIdx === activeSlideIdx) th.className = "active-thumb";
    th.loading = "lazy";
    th.addEventListener("click", () => {
      STATE.activeCarouselIndex = sIdx;
      renderTop5PlatformPreviewStage();
    });
    thumbs.appendChild(th);
  });
  mockup.appendChild(thumbs);
}

/* ==========================================================================
   View 4 Sub-Panel 2: Publishing Outbox Queue
   ========================================================================== */
function renderPublishingOutbox() {
  const tbody = document.getElementById("publishing-outbox-tbody");
  const badge = document.getElementById("outbox-summary-badge");
  const tabCountPill = document.getElementById("outbox-tab-count-pill");
  const execVal = document.getElementById("exec-kpi-outbox-value");
  if (!tbody) return;
  tbody.replaceChildren();

  const ledger = STATE.outboxLedger || { items: [] };
  const items = ledger.items || [];
  const pendingCount = ledger.pending_count ?? 0;

  if (badge) {
    badge.textContent = `${pendingCount} Pending · ${ledger.dispatched_count ?? 0} Validated (${items.length} Total)`;
  }
  if (tabCountPill) {
    tabCountPill.textContent = String(pendingCount > 0 ? pendingCount : items.length);
  }
  if (execVal) {
    execVal.textContent = pendingCount > 0 ? `${pendingCount} Pending Approval` : `${items.length} Validated`;
  }

  const approveAllBtn = document.getElementById("approve-all-outbox-btn");
  if (approveAllBtn) {
    approveAllBtn.textContent =
      pendingCount > 0
        ? `Approve & Dispatch Pending (${pendingCount})`
        : `Re-Verify Queue (${items.length})`;
  }

  if (!items.length) {
    const tr = document.createElement("tr");
    const td = mkEl("td", "", "No packages staged yet — check target channels in Today's Top 5 and click Stage to Queue.");
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

    const td1 = document.createElement("td");
    const c1 = mkEl("div", "cell-card-equal");
    const idStrong = mkEl("strong", "tabular-nums", item.outbox_id);
    idStrong.style.cssText = "font-size:11.5px;color:#1e40af;font-family:var(--theme-font-mono,monospace);";
    c1.append(idStrong, mkEl("span", "", item.platform_name || item.platform_id));
    td1.appendChild(c1);

    const td2 = document.createElement("td");
    const c2 = mkEl("div", "cell-card-equal");
    c2.appendChild(mkEl("strong", "", polishUiTypography(item.idea_title || item.idea_id)));
    const bp = mkEl("span", "", `Blueprint ${item.template_id} (${item.template_name || ""})`);
    bp.style.cssText = "font-size:11.5px;color:#475569;";
    c2.appendChild(bp);
    td2.appendChild(c2);

    const td3 = document.createElement("td");
    const c3 = mkEl("div", "cell-card-equal");
    c3.appendChild(mkEl("strong", "", formatModeDisplayName(item.mode)));
    const mSpan = mkEl("span", "", `${media.container_format || "TEXT"} · ${media.aspect_ratio || ""}`);
    mSpan.style.cssText = "font-size:11.5px;color:#1e40af;font-weight:600;";
    c3.appendChild(mSpan);
    td3.appendChild(c3);

    const td4 = document.createElement("td");
    const c4 = mkEl("div", "cell-card-equal");
    c4.appendChild(
      mkEl(
        "span",
        `pill-badge ${checks.all_passed ? "pill-emerald" : "pill-amber"}`,
        checks.all_passed ? "COMPLIANT ✓" : "CHECK LIMITS"
      )
    );
    const lenSpan = mkEl(
      "span",
      "tabular-nums",
      `${checks.char_used || 0}/${checks.char_cap || 0} chars · Fold ${checks.fold_used || 0}/${checks.fold_cap || 0}`
    );
    lenSpan.style.cssText = "font-size:11px;color:#475569;";
    c4.appendChild(lenSpan);
    td4.appendChild(c4);

    const td5 = document.createElement("td");
    const c5 = mkEl("div", "cell-card-equal");
    const okStatus =
      item.status === "PUBLISHED_LIVE" ||
      item.status === "DRY_RUN_VALIDATED" ||
      item.status === "SHARE_PACKET_READY";
    c5.appendChild(mkEl("span", `pill-badge ${okStatus ? "pill-emerald" : "pill-amber"}`, item.status));
    const tierNote = mkEl("span", "", item.tier_badge || "");
    tierNote.style.cssText = "font-size:11px;color:#475569;";
    c5.appendChild(tierNote);
    td5.appendChild(c5);

    const td6 = document.createElement("td");
    const c6 = mkEl("div", "cell-card-equal");
    const btnWrap = mkEl("div", "studio-toolbar-actions");
    const appBtn = mkEl(
      "button",
      item.status === "PENDING_APPROVAL" ? "btn-primary" : "btn-secondary",
      item.status === "PENDING_APPROVAL" ? "Approve" : "Re-Verify"
    );
    appBtn.type = "button";
    appBtn.style.cssText = "min-height:28px;padding:4px 8px;font-size:11px;";
    appBtn.setAttribute("data-testid", `approve-outbox-btn-${item.outbox_id}`);
    appBtn.addEventListener("click", () => approveOutboxItems([item.outbox_id]));

    const cpBtn = mkEl("button", "btn-secondary", "Copy");
    cpBtn.type = "button";
    cpBtn.style.cssText = "min-height:28px;padding:4px 8px;font-size:11px;";
    cpBtn.addEventListener("click", () =>
      copyTextSafe(pkg.body || "", `Copied ${item.platform_name} copy!`)
    );
    btnWrap.append(appBtn, cpBtn);
    c6.appendChild(btnWrap);
    td6.appendChild(c6);

    tr.append(td1, td2, td3, td4, td5, td6);
    tbody.appendChild(tr);
  });
}

/* ==========================================================================
   DOMContentLoaded Bootstrap & Event Listeners
   ========================================================================== */
document.addEventListener("DOMContentLoaded", () => {
  document.body.setAttribute("data-repo-layout", "cards");

  // Brand Home Click
  document.getElementById("brand-home-btn")?.addEventListener("click", () => {
    activateView("view-miner");
    activateMinerPanel("miner-panel-composer");
  });

  // Primary Workspace Navigation Tabs
  document.querySelectorAll(".global-header .nav-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => activateView(btn.getAttribute("data-view")));
  });
  wireRovingKeyboardGroup(".global-header .nav-tabs", ".nav-tab-btn");

  // Daily Studio Sub-Tabs
  document.querySelectorAll("[data-miner-panel]").forEach((btn) => {
    btn.addEventListener("click", () => activateMinerPanel(btn.getAttribute("data-miner-panel")));
  });
  wireRovingKeyboardGroup("[data-testid='miner-subtabs']", ".subview-tab-btn");

  // Creator Radar Sub-Tabs
  document.querySelectorAll("[data-playbook-panel]").forEach((btn) => {
    btn.addEventListener("click", () => activatePlaybookPanel(btn.getAttribute("data-playbook-panel")));
  });
  wireRovingKeyboardGroup("[data-testid='playbook-subtabs']", ".subview-tab-btn");

  document.getElementById("back-to-composer-btn")?.addEventListener("click", () => {
    activateMinerPanel("miner-panel-composer");
  });
  document.getElementById("exec-jump-outbox-btn")?.addEventListener("click", () => {
    activateMinerPanel("miner-panel-outbox");
  });
  document.getElementById("builder-jump-sandbox-btn")?.addEventListener("click", () => {
    activateView("view-openhands");
  });

  // Persona Mode Switcher
  document.querySelectorAll("[data-persona].persona-radio").forEach((btn) => {
    btn.addEventListener("click", () => setPersonaMode(btn.getAttribute("data-persona")));
  });
  wireRovingKeyboardGroup("[data-testid='persona-mode-switcher']", ".persona-radio");

  // Repository Layout Switcher
  document.querySelectorAll("[data-repo-layout]").forEach((btn) => {
    btn.addEventListener("click", () => setRepoLayoutMode(btn.getAttribute("data-repo-layout")));
  });
  wireRovingKeyboardGroup("#repos-layout-switcher", ".persona-radio");

  // Verified Telemetry Popover
  const popBtn = document.getElementById("status-popover-btn");
  const popPanel = document.getElementById("status-popover-panel");
  popBtn?.addEventListener("click", (ev) => {
    ev.stopPropagation();
    const open = popPanel?.classList.toggle("open");
    popBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.addEventListener("click", (ev) => {
    if (popPanel?.classList.contains("open") && !popPanel.contains(ev.target) && ev.target !== popBtn) {
      popPanel.classList.remove("open");
      popBtn?.setAttribute("aria-expanded", "false");
    }
  });

  // Command Palette (⌘K / Ctrl+K) & Lightbox
  document.getElementById("open-cmdk-btn")?.addEventListener("click", openCmdk);
  document.getElementById("close-cmdk-btn")?.addEventListener("click", closeCmdk);
  document.getElementById("cmdk-backdrop")?.addEventListener("click", (ev) => {
    if (ev.target.id === "cmdk-backdrop") closeCmdk();
  });
  document.getElementById("lightbox-backdrop")?.addEventListener("click", (ev) => {
    if (ev.target.id === "lightbox-backdrop") closeLightbox();
  });

  const cmdkInput = document.getElementById("cmdk-search-input");
  cmdkInput?.addEventListener("input", () => {
    STATE.cmdkActiveIdx = 0;
    renderCmdkResults();
  });
  cmdkInput?.addEventListener("keydown", (ev) => {
    const items = STATE.cmdkFilteredItems || [];
    if (ev.key === "ArrowDown" && items.length) {
      ev.preventDefault();
      STATE.cmdkActiveIdx = (STATE.cmdkActiveIdx + 1) % items.length;
      renderCmdkResults();
    } else if (ev.key === "ArrowUp" && items.length) {
      ev.preventDefault();
      STATE.cmdkActiveIdx = (STATE.cmdkActiveIdx - 1 + items.length) % items.length;
      renderCmdkResults();
    } else if (ev.key === "Enter" && items[STATE.cmdkActiveIdx]) {
      ev.preventDefault();
      const chosen = items[STATE.cmdkActiveIdx];
      closeCmdk();
      chosen.run();
    }
  });

  // Global Keyboard Shortcuts (⌘K & Layered Escape)
  document.addEventListener("keydown", (ev) => {
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "k") {
      ev.preventDefault();
      openCmdk();
      return;
    }
    if (ev.key === "Escape") {
      const lb = document.getElementById("lightbox-backdrop");
      if (lb && lb.style.display !== "none") {
        closeLightbox();
        return;
      }
      const ck = document.getElementById("cmdk-backdrop");
      if (ck && ck.style.display !== "none") {
        closeCmdk();
        return;
      }
      if (popPanel?.classList.contains("open")) {
        popPanel.classList.remove("open");
        popBtn?.setAttribute("aria-expanded", "false");
        return;
      }
      const radarDrawer = document.getElementById("creator-radar-drawer");
      if (radarDrawer?.classList.contains("open")) {
        closeAllSlideDrawers();
        return;
      }
      const drawer = document.getElementById("repo-inspector-drawer");
      if (drawer?.classList.contains("open")) {
        closeAllSlideDrawers();
      }
    }
  });

  // Inspector Drawer Tabs & Close
  document.querySelectorAll("#repo-inspector-drawer .drawer-tabs .nav-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#repo-inspector-drawer .drawer-tabs .nav-tab-btn").forEach((b) => {
        const isAct = b === btn;
        b.classList.toggle("active", isAct);
        b.setAttribute("aria-selected", isAct ? "true" : "false");
      });
      const target = btn.getAttribute("data-drawertab");
      ["dtab-visuals", "dtab-slides", "dtab-terraform", "dtab-linkedin"].forEach((tid) => {
        const p = document.getElementById(tid);
        if (p) p.style.display = tid === target ? "block" : "none";
      });
    });
  });
  wireRovingKeyboardGroup("#repo-inspector-drawer .drawer-tabs", ".nav-tab-btn");

  document.getElementById("close-drawer-btn")?.addEventListener("click", closeAllSlideDrawers);
  document.getElementById("close-radar-drawer-btn")?.addEventListener("click", closeAllSlideDrawers);
  document.getElementById("drawer-backdrop")?.addEventListener("click", closeAllSlideDrawers);

  // Creator Radar Filters & Sorts
  document.getElementById("posts-audit-search-input")?.addEventListener("input", renderReviewedPostsGrid);
  document.getElementById("posts-audit-filter-pres")?.addEventListener("change", renderReviewedPostsGrid);
  document.getElementById("posts-audit-filter-author")?.addEventListener("change", renderReviewedPostsGrid);
  document.getElementById("posts-audit-sort-select")?.addEventListener("change", renderReviewedPostsGrid);
  document.getElementById("creator-search-input")?.addEventListener("input", renderCreatorProfilesGrid);
  document.getElementById("creator-platform-filter")?.addEventListener("change", renderCreatorProfilesGrid);

  // Filters & Actions
  document.getElementById("gallery-search-input")?.addEventListener("input", renderGalleryView);
  document.getElementById("gallery-filter-tier")?.addEventListener("change", renderGalleryView);
  document.getElementById("gallery-filter-type")?.addEventListener("change", renderGalleryView);

  document.getElementById("search-input")?.addEventListener("input", renderReposView);
  document.getElementById("filter-archetype")?.addEventListener("change", renderReposView);
  document.getElementById("filter-author")?.addEventListener("change", renderReposView);

  document.getElementById("reset-filters-btn")?.addEventListener("click", () => {
    const s = document.getElementById("search-input");
    const a = document.getElementById("filter-archetype");
    const au = document.getElementById("filter-author");
    if (s) s.value = "";
    if (a) a.value = "ALL";
    if (au) au.value = "ALL";
    renderReposView();
  });

  document.getElementById("generate-daily-posts-btn")?.addEventListener("click", triggerGenerateDailyPosts);
  document.getElementById("generate-top5-briefing-btn")?.addEventListener("click", triggerGenerateTop5Briefing);
  document.getElementById("transcode-active-idea-btn")?.addEventListener("click", triggerTranscodeActiveIdea);
  document.getElementById("approve-all-outbox-btn")?.addEventListener("click", () => approveOutboxItems(null));
  document.getElementById("refresh-live-feeds-btn")?.addEventListener("click", () => {
    refreshLiveFeeds();
    showToast("Refreshed live arXiv & GitHub signals");
  });

  document.getElementById("trigger-ingest-btn")?.addEventListener("click", async () => {
    const url = (document.getElementById("inline-ingest-url-input")?.value || "").trim();
    const title = (document.getElementById("inline-ingest-title-input")?.value || "").trim();
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
    if (banner) {
      banner.style.display = "inline-flex";
      banner.className = "pill-badge pill-emerald";
      banner.textContent = `Verified & Mapped: ${out.status} → Repository: ${out.repo_slug}`;
    }
    showToast(`Grounded URL into repository ${out.repo_slug}`);
  });

  // Video Timecode Updater
  const walkVid = document.getElementById("mint01-walkthrough-video");
  const timeLbl = document.getElementById("mint01-walkthrough-time-label");
  walkVid?.addEventListener("timeupdate", () => {
    if (!timeLbl) return;
    const cur = Math.floor(walkVid.currentTime || 0);
    const dur = Math.floor(walkVid.duration || 44);
    const fmt = (n) => `${String(Math.floor(n / 60)).padStart(2, "0")}:${String(n % 60).padStart(2, "0")}`;
    timeLbl.textContent = `${fmt(cur)} / ${fmt(dur)} · 1080p30`;
  });

  // Hydrate Initial Data & Route
  const params = new URLSearchParams(window.location.search);
  const reqPersona = params.get("persona");
  if (reqPersona) setPersonaMode(reqPersona);

  loadWorkspaceData();
  loadMintingStudioData();

  const reqView = params.get("view");
  activateView(reqView && ALL_VIEWS.includes(reqView) ? reqView : "view-miner");
});
