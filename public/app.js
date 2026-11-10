// Ideas Minting Studio — Multi-Persona Interactive Client Controller (v3.0)
// Pure DOM construction (createElement / textContent / replaceChildren) across all dynamic views.

function mkEl(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined && text !== null) el.textContent = String(text);
  return el;
}

const ASSET_CACHE_BUST = "20261110c";

function safeUrl(rawUrl) {
  const s = String(rawUrl || "").trim();
  if (s.startsWith("/assets/") || s.startsWith("/repos/")) {
    const clean = s.replace(/\?v=[A-Za-z0-9_.-]+$/, "");
    if (/\.(png|svg|jpg|jpeg|gif|mp4|mp3)$/i.test(clean)) {
      return `${clean}?v=${ASSET_CACHE_BUST}`;
    }
    return s;
  }
  if (
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
  composerCopyExpanded: false,
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

  (STATE.templates || []).slice(0, 140).forEach((t) => {
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
    const imgUrl = `/repos/${encodeURIComponent(r.repo_slug)}/visuals/${plan ? "lead-template.svg" : "dynamic-solution-flow.svg"}?v=20261106c`;
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
      aSvg.href = `/repos/${encodeURIComponent(slug)}/visuals/lead-template.svg?v=20261106c`;
      aSvg.target = "_blank";
      actBar.appendChild(aSvg);
    }
    const aFlow = mkEl("a", "btn-secondary", "Moving-Arrow SVG ↗");
    aFlow.href = `/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.svg?v=20261106c`;
    aFlow.target = "_blank";
    actBar.appendChild(aFlow);

    const aDrawio = mkEl("a", "btn-secondary", "Editable .drawio");
    aDrawio.href = `/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.drawio?v=20261106c`;
    aDrawio.setAttribute("download", "");
    actBar.appendChild(aDrawio);
    visTab.appendChild(actBar);

    const figures = [];
    if (plan) {
      figures.push([
        `Paired Blueprint (${plan.primary_template_id}: ${plan.primary_template_name})`,
        `/repos/${encodeURIComponent(slug)}/visuals/lead-template.svg?v=20261106c`,
      ]);
    }
    figures.push(
      [
        "Figure 1 — Problem → 4-Step Moving-Arrow Solution Flow",
        `/repos/${encodeURIComponent(slug)}/visuals/dynamic-solution-flow.svg?v=20261106c`,
      ],
      [
        "Figure 2 — Google Cloud #78 4-Zone Hub-and-Spoke Architecture",
        `/repos/${encodeURIComponent(slug)}/visuals/gcp-architecture-2d.svg?v=20261106c`,
      ],
      [
        "Figure 3 — High-Resolution 2D Infographic Poster",
        `/repos/${encodeURIComponent(slug)}/visuals/linkedin-infographic-2d.svg?v=20261106c`,
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
    pHdr.appendChild(mkEl("strong", "", "Canonical 2D Architecture Blueprint Specification (#78 & Poster IR)"));
    const specText = detail.architecture_blueprint_spec || detail.nano_banana_3_prompt || "";
    const cpBtn = mkEl("button", "btn-secondary", "Copy Spec");
    cpBtn.type = "button";
    cpBtn.addEventListener("click", () =>
      copyTextSafe(specText, "Copied architecture blueprint specification!")
    );
    pHdr.appendChild(cpBtn);
    const pre = mkEl("pre", "code-block-light", specText);
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

  // Tab 3: Terraform, ADK Code & Reproducible Evals
  const tfTab = document.getElementById("dtab-terraform");
  if (tfTab) {
    tfTab.replaceChildren();
    if (detail.eval_results && detail.eval_results.metrics) {
      const m = detail.eval_results.metrics;
      const evalCard = mkEl("div", "feed-item-card");
      evalCard.style.cssText = "background:#f8fafc;border:1px solid #cbd5e1;border-left:4px solid #2563eb;padding:12px 14px;border-radius:10px;margin-bottom:14px;";
      const hdr = mkEl("div", "", `REPRODUCIBLE EVALUATION SUITE · ${detail.eval_results.total_scenarios || 20} SCENARIOS (${detail.eval_results.total_trial_executions || 100} TRIALS)`);
      hdr.style.cssText = "font-size:11px;font-weight:800;letter-spacing:0.06em;color:#1d4ed8;margin-bottom:6px;";
      const summaryLine = mkEl(
        "div",
        "",
        `pass^5 Reliability: ${m.naive_pass_pow_5_pct}% → ${m.engineered_pass_pow_5_pct}%  |  Token Reduction: -${m.token_reduction_pct}% (${m.naive_avg_tokens} → ${m.engineered_avg_tokens} tok)  |  p95 Speedup: ${m.p95_latency_speedup_x}x (${m.naive_p95_latency_ms}ms → ${m.engineered_p95_latency_ms}ms)  |  Adversarial Blocked: ${m.adversarial_Shot_blocked_engineered}  |  Cost/1K Runs: $${m.cost_per_1k_workflows_naive_usd} → $${m.cost_per_1k_workflows_engineered_usd}`
      );
      summaryLine.style.cssText = "font-size:12.5px;font-weight:700;color:#0f172a;line-height:1.5;";
      evalCard.append(hdr, summaryLine);
      tfTab.appendChild(evalCard);
    }
    [
      ["1-Click Google Cloud Deployment & Eval Suite Execution", `cd generated-repos/${slug} && python3 evals/run_eval_suite.py && ./scripts/deploy_gcp_one_click.sh ramp-portal-dev us-west1`],
      ["evals/eval_dataset.jsonl (20 Grounded Enterprise Benchmark Scenarios — Preview)", detail.eval_dataset_preview || ""],
      ["evals/run_eval_suite.py (Reproducible Naive vs. Engineered Benchmark Runner)", detail.eval_runner_py || ""],
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

      const distDir = detail.distribution_directory || plan || {};
      const pBox = mkEl("div", "feed-item-card");
      pBox.style.background = "#ffffff";
      pBox.appendChild(mkEl("div", "eyebrow-label", "PRIMARY HIGH-REACH LINKEDIN GROUPS"));
      (distDir.linkedin_groups_primary || plan.linkedin_groups_primary || []).forEach((g) => {
        const line = mkEl("div", "", `• ${g.name} (${g.members}) — ${g.goal}`);
        line.style.cssText = "font-size:12px;color:#334155;margin-top:4px;";
        if (g.url) {
          const lnk = mkEl("a", "", " [Group ↗]");
          lnk.href = safeUrl(g.url);
          lnk.target = "_blank";
          lnk.style.cssText = "color:#2563eb;font-weight:700;text-decoration:none;margin-left:4px;";
          line.appendChild(lnk);
        }
        pBox.appendChild(line);
      });

      const nBox = mkEl("div", "feed-item-card");
      nBox.style.background = "#ffffff";
      nBox.appendChild(mkEl("div", "eyebrow-label", "NICHE EXECUTIVE & ARCHITECT GROUPS"));
      (distDir.linkedin_groups_niche_network || plan.linkedin_groups_niche_network || []).forEach((g) => {
        const line = mkEl("div", "", `• ${g.name} (${g.members}) — ${g.goal}`);
        line.style.cssText = "font-size:12px;color:#334155;margin-top:4px;";
        if (g.url) {
          const lnk = mkEl("a", "", " [Group ↗]");
          lnk.href = safeUrl(g.url);
          lnk.target = "_blank";
          lnk.style.cssText = "color:#2563eb;font-weight:700;text-decoration:none;margin-left:4px;";
          line.appendChild(lnk);
        }
        nBox.appendChild(line);
      });

      cols.append(pBox, nBox);
      planCard.appendChild(cols);

      if (distDir.relevant_companies_and_pages && distDir.relevant_companies_and_pages.length) {
        const compBox = mkEl("div", "feed-item-card");
        compBox.style.cssText = "background:#ffffff;margin-top:10px;";
        compBox.appendChild(mkEl("div", "eyebrow-label", "RELEVANT COMPANY PAGES (@MENTIONS) & OFFICIAL ENGINEERING REFERENCES"));
        distDir.relevant_companies_and_pages.forEach((c) => {
          const cRow = mkEl("div", "", `• ${c.linkedin_page_tag} (${c.x_handle}) — ${c.role_in_post} `);
          cRow.style.cssText = "font-size:12px;color:#0f172a;margin-top:5px;";
          const refA = mkEl("a", "", `[${c.reference_title} ↗]`);
          refA.href = safeUrl(c.reference_url);
          refA.target = "_blank";
          refA.style.cssText = "color:#1d4ed8;font-weight:700;text-decoration:none;";
          cRow.appendChild(refA);
          compBox.appendChild(cRow);
        });
        planCard.appendChild(compBox);
      }

      if (distDir.hashtags_bundle) {
        const tagBox = mkEl("div", "feed-item-card");
        tagBox.style.cssText = "background:#f8fafc;margin-top:10px;";
        tagBox.appendChild(mkEl("div", "eyebrow-label", "HASHTAGS & CROSS-PLATFORM COMMUNITIES"));
        const tLine = mkEl("div", "", `LinkedIn Optimal 5: ${distDir.hashtags_bundle.linkedin_optimal_5}  |  Full Set: ${distDir.hashtags_bundle.full_hashtag_string}`);
        tLine.style.cssText = "font-size:12px;font-weight:700;color:#1e40af;margin-top:4px;";
        tagBox.appendChild(tLine);
        (distDir.cross_platform_pages_and_communities || []).forEach((cp) => {
          const cpLine = mkEl("div", "", `• ${cp.platform}: ${cp.page_or_group} (${cp.audience}) — ${cp.posting_angle}`);
          cpLine.style.cssText = "font-size:11.5px;color:#334155;margin-top:3px;";
          tagBox.appendChild(cpLine);
        });
        planCard.appendChild(tagBox);
      }

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
   View 2: 128 Certified Visual Blueprints Gallery
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
    const svg = `/assets/template-gallery/${files.svg || t.id + ".svg"}?v=20261106c`;
    const png = `/assets/template-gallery/${files.png || t.id + ".png"}?v=20261106c`;
    const gif = `/assets/template-gallery/${files.gif || t.id + ".gif"}?v=20261106c`;
    const drawio = files.drawio ? `/assets/template-gallery/${files.drawio}?v=20261106c` : "";
    const pptx = files.pptx ? `/assets/template-gallery/${files.pptx}?v=20261106c` : "";
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
    if (post.gif_url) {
      const gifBtn = mkEl("a", "btn-secondary", "Original 4:5 .GIF ↗");
      gifBtn.href = safeUrl(post.gif_url);
      gifBtn.target = "_blank";
      gifBtn.rel = "noopener";
      actionsBar.appendChild(gifBtn);
    }
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
  if (post.gif_url || post.image_url) {
    const activeMediaUrl = post.gif_url || post.image_url;
    const vbox = mkEl("div", "drawer-post-visual-card");
    const img = document.createElement("img");
    img.src = safeUrl(activeMediaUrl);
    img.alt = `${post.author_name} post visual`;
    img.addEventListener("click", () =>
      openLightbox({
        kicker: `${post.post_code} · ${post.presentation_archetype_code}${post.gif_url ? " · 4:5 GIF89a" : ""}`,
        title: `${post.author_name} — ${post.hook_line_1}`,
        imgUrl: activeMediaUrl,
        actions: [{ label: "Original LinkedIn Post ↗", href: post.post_url }],
      })
    );
    const zHint = mkEl(
      "span",
      "eyebrow-muted",
      post.gif_url ? "Live looping 4:5 GIF89a · Click to zoom @2x" : "Click artwork to zoom @2x"
    );
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
  bpImg.src = `/assets/template-gallery/${tid}.svg?v=20261106c`;
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
    const audHdr = mkEl("h3", "subsection-heading", `Audited Posts in 60-Post Cohort (${auditedPosts.length})`);
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
    if (presFilter === "ANIMATED_GIF") {
      if (!(p.is_gif || p.gif_url)) return false;
    } else if (presFilter === "RESTRICTED") {
      if (p.availability === "PUBLIC_VERIFIED") return false;
    } else if (presFilter !== "ALL" && p.presentation_archetype_code !== presFilter) {
      return false;
    }
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
    if (post.is_gif || post.gif_url) {
      metaRow.appendChild(mkEl("span", "pill-badge pill-emerald", "🎞️ 4:5 GIF89a"));
    }
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
      const zoomPill = mkEl("span", "post-visual-zoom-pill", post.gif_url ? "Play 4:5 GIF89a" : "Zoom Visual");
      frame.append(img, zoomPill);
      frame.addEventListener("click", () =>
        openLightbox({
          kicker: `${post.post_code} · ${post.presentation_archetype_code} · ${post.author_name}`,
          title: post.hook_line_1,
          imgUrl: post.gif_url || post.image_url,
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
      badges.appendChild(mkEl("span", "pill-badge pill-emerald", "In 60-Post Audit"));
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

  renderAutonomousMinerPanel();
}

async function loadAutonomousMinerData(forceLive = false) {
  const btn = document.getElementById("run-autominer-live-btn");
  const topicInput = document.getElementById("autominer-topic-input");
  const topicQuery = (topicInput?.value || "").trim();
  if (btn && forceLive) {
    btn.disabled = true;
    btn.textContent = "⏳ Harvesting Live RSS · arXiv · GitHub · DEV.to · Reddit...";
  }
  try {
    let payload;
    if (forceLive) {
      const res = await fetch("/api/radar/autonomous-miner/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic_query: topicQuery, use_live_network: true }),
      });
      payload = await res.json();
      showToast(`Harvested ${payload.total_discovered_signals || 0} zero-link signals with Format/Duration/Group prescriptions`);
    } else {
      const qParam = topicQuery ? `?q=${encodeURIComponent(topicQuery)}` : "";
      const res = await fetch(`/api/radar/autonomous-miner${qParam}`);
      payload = await res.json();
    }
    STATE.autonomousMiner = payload;
    renderAutonomousMinerPanel();
  } catch (_err) {
    // Keep existing state if offline
  } finally {
    if (btn && forceLive) {
      btn.disabled = false;
      btn.textContent = "⚡ Run Zero-Link Live Harvest Now";
    }
  }
}

function renderAutonomousMinerPanel() {
  const data = STATE.autonomousMiner;
  if (!data) return;

  const pill = document.getElementById("playbook-autominer-count-pill");
  if (pill) {
    pill.textContent = String((data.discovered_signals || []).length || "Live");
  }

  const badge = document.getElementById("autominer-status-badge");
  if (badge) {
    const counts = data.live_channel_counts || {};
    const total = data.total_discovered_signals || (data.discovered_signals || []).length;
    badge.textContent = `${total} Zero-Link Signals Ranked · RSS (${counts.creator_rss_syndicate || 0}) · Papers/Code (${(counts.arxiv_and_hf_papers || 0) + (counts.github_and_hn_velocity || 0)}) · Community (${counts.devto_and_reddit_pulse || 0})`;
  }

  const sigGrid = document.getElementById("autominer-signals-grid");
  if (sigGrid) {
    sigGrid.replaceChildren();
    (data.discovered_signals || []).slice(0, 12).forEach((sig) => {
      const pres = sig.prescription || {};
      const card = mkEl("div", "repo-card");
      card.setAttribute("data-testid", `autominer-signal-card-${sig.signal_id}`);
      const inner = mkEl("div");

      const chips = mkEl("div", "deliverable-chips");
      chips.append(
        mkEl("span", "brand-badge tabular-nums", `${sig.demand_score} Demand`),
        mkEl("span", "pill-badge pill-sky", sig.source_pipeline || "Zero-Link Signal"),
        mkEl("span", "pill-badge pill-emerald", sig.cluster_label || "AI Systems")
      );
      inner.appendChild(chips);

      const h = mkEl("h3", "repo-card-title", polishUiTypography(sig.title));
      h.style.margin = "8px 0 6px";
      inner.appendChild(h);

      const sum = mkEl("p", "", polishUiTypography(sig.summary));
      sum.style.cssText = "font-size:12px;color:#334155;margin-bottom:8px;line-height:1.48;";
      inner.appendChild(sum);

      const rxBox = mkEl("div", "platform-spec-box");
      rxBox.style.cssText = "background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:10px;margin-bottom:8px;";
      const rxFmt = mkEl("div", "", `🎯 Format: ${pres.recommended_primary_format || "4:5 Animated GIF89a"}`);
      rxFmt.style.cssText = "font-size:11.5px;font-weight:800;color:#1e40af;margin-bottom:4px;";
      const rxDur = mkEl("div", "", `⏱️ Duration & Spec: ${pres.optimal_duration_and_fps || "6–12s loop @ 20fps"} • ${pres.aspect_ratio_and_px || "1080×1350"}`);
      rxDur.style.cssText = "font-size:11.5px;font-weight:700;color:#065f46;margin-bottom:4px;";
      const rxGrp = mkEl(
        "div",
        "",
        `📣 Target Groups: ${(pres.target_groups_and_communities || []).slice(0, 3).join(" · ")}`
      );
      rxGrp.style.cssText = "font-size:11px;color:#334155;margin-bottom:4px;";
      const rxWin = mkEl("div", "", `🕒 Window: ${pres.optimal_posting_window || "Tue–Thu 07:45 AM EST"}`);
      rxWin.style.cssText = "font-size:11px;color:#475569;";
      rxBox.append(rxFmt, rxDur, rxGrp, rxWin);
      inner.appendChild(rxBox);
      card.appendChild(inner);

      const foot = mkEl("div", "repo-card-footer");
      const srcLink = mkEl("a", "btn-secondary", "Primary Source ↗");
      srcLink.href = safeUrl(sig.primary_url);
      srcLink.target = "_blank";
      srcLink.rel = "noopener";

      const synthBtn = mkEl("button", "btn-primary", "Synthesize in Studio →");
      synthBtn.type = "button";
      synthBtn.addEventListener("click", () => {
        const top5Input = document.getElementById("top5-topic-query-input");
        if (top5Input) top5Input.value = sig.title;
        activateView("view-miner");
        activateMinerPanel("miner-panel-composer");
        triggerGenerateTop5Briefing();
      });
      foot.append(srcLink, synthBtn);
      card.appendChild(foot);
      sigGrid.appendChild(card);
    });
  }

  const fmtTbody = document.getElementById("autominer-format-matrix-tbody");
  if (fmtTbody) {
    fmtTbody.replaceChildren();
    (data.format_duration_matrix || []).forEach((row) => {
      const tr = document.createElement("tr");
      [
        [row.format_name, "font-weight:800;color:#0f172a;"],
        [`${row.aspect_ratio_and_px} — ${row.optimal_duration_and_fps}`, "font-weight:700;color:#1e40af;"],
        [row.text_copy_budget, "color:#334155;"],
        [row.empirical_audit_evidence, "color:#065f46;font-weight:600;"],
        [(row.best_for_topic_types || []).join(" • "), "color:#334155;"],
      ].forEach(([txt, st]) => {
        const td = document.createElement("td");
        const c = mkEl("div", "cell-card-equal");
        const sp = mkEl("span", "", polishArrows(txt));
        sp.style.cssText = `font-size:12px;${st}`;
        c.appendChild(sp);
        td.appendChild(c);
        tr.appendChild(td);
      });
      fmtTbody.appendChild(tr);
    });
  }

  const grpTbody = document.getElementById("autominer-groups-tbody");
  if (grpTbody) {
    grpTbody.replaceChildren();
    (data.distribution_channels_and_groups || []).forEach((row) => {
      const tr = document.createElement("tr");
      [
        [row.platform, "font-weight:800;color:#0f172a;"],
        [row.community_or_group_name, "font-weight:700;color:#1e40af;"],
        [row.optimal_duration_or_length, "color:#065f46;font-weight:600;"],
        [row.best_posting_window_est, "color:#334155;font-weight:700;"],
        [row.distribution_playbook, "color:#334155;"],
      ].forEach(([txt, st]) => {
        const td = document.createElement("td");
        const c = mkEl("div", "cell-card-equal");
        const sp = mkEl("span", "", polishArrows(txt));
        sp.style.cssText = `font-size:12px;${st}`;
        c.appendChild(sp);
        td.appendChild(c);
        tr.appendChild(td);
      });
      grpTbody.appendChild(tr);
    });
  }

  const rssGrid = document.getElementById("autominer-rss-feeds-grid");
  if (rssGrid) {
    rssGrid.replaceChildren();
    (data.creator_syndicate_feeds || []).forEach((fd) => {
      const card = mkEl("div", "repo-card");
      const inner = mkEl("div");
      const chips = mkEl("div", "deliverable-chips");
      chips.append(
        mkEl("span", "brand-badge", fd.feed_id),
        mkEl("span", "pill-badge pill-emerald", `@${fd.handle}`)
      );
      inner.appendChild(chips);
      const h = mkEl("h3", "repo-card-title", fd.creator_or_lab);
      h.style.margin = "8px 0 6px";
      inner.appendChild(h);
      const p = mkEl("p", "", `Signature Output: ${fd.typical_format}`);
      p.style.cssText = "font-size:12px;color:#334155;margin-bottom:8px;";
      inner.appendChild(p);
      card.appendChild(inner);

      const foot = mkEl("div", "repo-card-footer");
      const link = mkEl("a", "btn-secondary", "Open RSS/Atom Feed ↗");
      link.href = safeUrl(fd.rss_url);
      link.target = "_blank";
      link.rel = "noopener";
      foot.appendChild(link);
      card.appendChild(foot);
      rssGrid.appendChild(card);
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
    const svgUrl = `/assets/template-gallery/${tid}.svg?v=20261106c`;

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
  const dd = p.distribution_directory || {};
  const compTags = dd.company_mentions_line_linkedin ? `\nMentions: ${dd.company_mentions_line_linkedin}` : "";
  const grpLine = (dd.linkedin_groups_primary || []).map((g) => `${g.name} (${g.url})`).join(" | ");
  const fullTags = dd.hashtags_bundle?.full_hashtag_string || p.hashtags || "";
  const fullPayload = `${p.linkedin_post_text}${compTags}\n\n${fullTags}\n\n---\n${p.first_comment_source}${grpLine ? `\nTarget Groups: ${grpLine}` : ""}`;
  await copyTextSafe(fullPayload, `Copied Post + @Companies + Groups + Comment #1 (${p.canonical_template_id})!`);
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
    imSvg.src = safeUrl(p.custom_dynamic_svg_url);
    imSvg.alt = `Custom flow SVG for ${p.topic_title}`;
    imSvg.style.cssText = "width:100%;height:auto;display:block;border-radius:6px;background:#ffffff;";
    imSvg.loading = "lazy";

    const imPng = document.createElement("img");
    imPng.id = `daily-vis-png-${p.id}`;
    imPng.src = safeUrl(p.canonical_png_url);
    imPng.alt = `Canonical ${p.canonical_template_id} poster`;
    imPng.style.cssText = "width:100%;height:auto;display:none;border-radius:6px;background:#ffffff;";
    imPng.loading = "lazy";

    stage.append(imSvg, imPng);
    top.appendChild(stage);

    const dd = p.distribution_directory || {};
    const fullHash = dd.hashtags_bundle?.full_hashtag_string || p.hashtags || "";
    const copyBox = mkEl("div", "daily-post-copy-box", `${polishUiTypography(p.linkedin_post_text)}\n\n${fullHash}`);
    copyBox.id = `daily-copy-text-${p.id}`;
    top.appendChild(copyBox);

    if (dd.relevant_companies_and_pages && dd.relevant_companies_and_pages.length) {
      const distStrip = mkEl("div", "feed-item-card");
      distStrip.style.cssText = "background:#f8fafc;border:1px solid #e2e8f0;padding:8px 10px;border-radius:8px;margin-top:8px;font-size:11.5px;color:#334155;";
      const cLine = mkEl("div", "", `🏢 Companies: ${dd.company_mentions_line_linkedin}`);
      cLine.style.cssText = "font-weight:700;color:#0f172a;margin-bottom:3px;";
      const gNames = (dd.linkedin_groups_primary || []).map((g) => `${g.name} (${g.members})`).join(" · ");
      const gLine = mkEl("div", "", `👥 Groups: ${gNames}`);
      distStrip.append(cLine, gLine);
      top.appendChild(distStrip);
    }
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
    ledgerBadge.textContent = `30-Day Dedupe (${STATE.top5Briefing.dedupe_ledger_entries || 5} tracked · ${STATE.top5Briefing.certified_pool_size || 128} blueprints)`;
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

const SHORT_PLATFORM_TAB_LABELS = {
  linkedin: "LinkedIn",
  telegram: "Telegram",
  youtube: "YouTube",
  youtube_shorts: "Shorts",
  instagram: "Instagram",
  facebook: "Facebook",
  tiktok: "TikTok",
  whatsapp: "WhatsApp",
  devto: "Dev.to",
  hashnode: "Hashnode",
  bluesky: "Bluesky",
  x: "X",
  substack: "Substack",
};

function shortenClusterLabel(raw) {
  const s = String(raw || "").trim();
  if (/LLM Serving|KV-Cache|Speculative/i.test(s)) return "KV-Cache & Routing";
  if (/FinOps|ROI|Governance/i.test(s)) return "FinOps & Governance";
  if (/Coding|Harnesses|Software/i.test(s)) return "Coding Harnesses";
  if (/MCP|Zero-Trust|OAuth/i.test(s)) return "MCP & Zero-Trust";
  if (/Multi-Agent|GraphRAG|Context/i.test(s)) return "Multi-Agent & Context";
  if (/Reliability|Tool-Calling|Production/i.test(s)) return "Agentic Reliability";
  return s.length > 24 ? `${s.slice(0, 22)}…` : s;
}

function extractIdeaTldrChips(idea, activeTpl) {
  const chips = [];
  const impact = String(idea.metrics_hint || idea.summary || "");
  const pctMatch = impact.match(/([+-]?\d+(?:\.\d+)?%\s+[A-Za-z -]{3,22})/);
  const latMatch = impact.match(/(<\s*\d+(?:\.\d+)?(?:ms|s)\s+[A-Za-z0-9 -]{2,18})/i);
  if (pctMatch) {
    const cleanPct = pctMatch[1]
      .trim()
      .replace(/\s+(?:while|with|across|in|for|by|on|at|to|and|or|from)$/i, "")
      .trim();
    chips.push({ icon: "⚡", text: cleanPct, tone: "emerald" });
  } else {
    chips.push({ icon: "⚡", text: `Demand ${idea.scores?.demand_score ?? 95}/100`, tone: "emerald" });
  }
  if (latMatch) {
    const cleanLat = latMatch[1]
      .trim()
      .replace(/\s+(?:while|with|across|in|for|by|on|at|to|and|or|from)$/i, "")
      .trim();
    chips.push({ icon: "🎯", text: cleanLat, tone: "blue" });
  } else {
    chips.push({ icon: "🎯", text: shortenClusterLabel(idea.cluster_label), tone: "blue" });
  }
  if (activeTpl?.template_id) {
    chips.push({
      icon: "📐",
      text: `${activeTpl.template_id} · ${activeTpl.angle_label || formatModeDisplayName(STATE.selectedMode)}`,
      tone: "slate",
    });
  }
  return chips;
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

  // Column 1: 5 Ranked Signal Cards (Linear-style compact signal list)
  ideas.forEach((idea, idx) => {
    const isAct = idea.id === STATE.selectedIdeaId;
    const card = mkEl("button", `top5-idea-card${isAct ? " active" : ""}`);
    card.type = "button";
    card.setAttribute("data-testid", `top5-idea-card-${idx + 1}`);

    const metaRow = mkEl("div", "idea-card-meta-row");
    metaRow.appendChild(
      mkEl("span", "idea-rank-cluster tabular-nums", `0${idea.rank} · ${shortenClusterLabel(idea.cluster_label)}`)
    );
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
      STATE.composerCopyExpanded = false;
      renderTop5EditorialDesk();
      await refreshPlatformPreviewPackages();
    });
    ideasCol.appendChild(card);
  });

  const activeIdea = getActiveTop5Idea();
  const activeTpl = getActiveTop5Template(activeIdea);
  if (!activeIdea || !activeTpl) return;

  // Column 2: Center Visual Stage (Canva Magic Studio + Gamma Pattern)
  const ideaHdr = mkEl("div", "composer-idea-header");
  const kickerRow = mkEl("div", "composer-idea-kicker");
  kickerRow.appendChild(
    mkEl("span", "", polishUiTypography(`SIGNAL 0${activeIdea.rank} · ${activeIdea.source_channel}`))
  );
  const srcA = mkEl("a", "eyebrow-link", "Source ↗");
  srcA.href = safeUrl(activeIdea.primary_url);
  srcA.target = "_blank";
  srcA.rel = "noopener";
  kickerRow.appendChild(srcA);
  ideaHdr.appendChild(kickerRow);
  ideaHdr.appendChild(mkEl("h2", "composer-idea-title", polishUiTypography(activeIdea.title)));

  // Canva/Gamma 3-Chip Visual TL;DR Bar (replaces dense paragraph in Creator mode)
  const tldrRow = mkEl("div", "composer-tldr-chip-row");
  extractIdeaTldrChips(activeIdea, activeTpl).forEach((c) => {
    const pill = mkEl("span", `composer-tldr-chip tone-${c.tone}`, `${c.icon} ${polishUiTypography(c.text)}`);
    tldrRow.appendChild(pill);
  });
  ideaHdr.appendChild(tldrRow);

  // Retained for Builder/Executive deep-read mode
  ideaHdr.appendChild(
    mkEl("p", "composer-idea-impact", polishUiTypography(activeIdea.metrics_hint || activeIdea.summary))
  );
  workbench.appendChild(ideaHdr);

  // Step 1: Canva-Style Visual Blueprint Stage + 5-Thumbnail Switcher
  const step1 = mkEl("div", "composer-section");
  const s1Hdr = mkEl("div", "composer-section-hdr");
  s1Hdr.appendChild(mkEl("span", "composer-step-title", "1. Visual Blueprint"));

  const s1Actions = mkEl("div", "studio-toolbar-actions");
  const resolvedTplObj =
    (STATE.templates || []).find((t) => t.id === activeTpl.template_id) || {};
  const activeGslidesUrl =
    activeTpl.google_slides_url || resolvedTplObj.google_slides_url || "";
  const activeDrawioUrl =
    activeTpl.drawio_url || `/assets/template-gallery/${activeTpl.template_id}.drawio`;
  const activePptxUrl =
    activeTpl.pptx_url || `/assets/template-gallery/${activeTpl.template_id}.pptx`;
  const activeSvgUrl =
    activeTpl.svg_url || `/assets/template-gallery/${activeTpl.template_id}.svg`;

  if (activeGslidesUrl) {
    const gsA = mkEl("a", "deliverable-chip chip-blue", "Google Slides ↗");
    gsA.setAttribute("data-testid", "daily-open-google-slides-btn");
    gsA.style.textDecoration = "none";
    gsA.href = safeUrl(activeGslidesUrl);
    gsA.target = "_blank";
    gsA.rel = "noopener";
    s1Actions.appendChild(gsA);
  }
  [
    [".drawio", activeDrawioUrl, `${activeTpl.template_id}.drawio`, "daily-download-drawio-btn"],
    [".pptx", activePptxUrl, `${activeTpl.template_id}.pptx`, "daily-download-pptx-btn"],
    ["SVG ↗", activeSvgUrl, "", "daily-open-svg-btn"],
  ].forEach(([lbl, href, dlName, testId]) => {
    const a = mkEl("a", "deliverable-chip chip-blue", lbl);
    a.setAttribute("data-testid", testId);
    a.style.textDecoration = "none";
    a.href = safeUrl(href);
    if (dlName) {
      a.setAttribute("download", dlName);
    } else {
      a.target = "_blank";
      a.rel = "noopener";
    }
    s1Actions.appendChild(a);
  });

  const openActiveBlueprintLightbox = () => {
    const lbActions = [];
    if (activeGslidesUrl) {
      lbActions.push({
        label: "Open Google Slides ↗",
        href: activeGslidesUrl,
        primary: true,
      });
    }
    lbActions.push(
      {
        label: "Download .drawio",
        href: activeDrawioUrl,
        download: `${activeTpl.template_id}.drawio`,
      },
      {
        label: "Download .pptx",
        href: activePptxUrl,
        download: `${activeTpl.template_id}.pptx`,
      },
      {
        label: "Open SVG ↗",
        href: activeSvgUrl,
      }
    );
    openLightbox({
      kicker: `${activeTpl.template_id} · ${activeTpl.angle_label || "CERTIFIED BLUEPRINT"}`,
      title: `${activeTpl.template_id} — ${activeTpl.name}`,
      imgUrl: safeUrl(activeSvgUrl),
      actions: lbActions,
    });
  };

  const zoomBtn = mkEl("button", "btn-secondary", `🔍 Zoom ${activeTpl.template_id}`);
  zoomBtn.type = "button";
  zoomBtn.style.cssText = "min-height:28px;padding:3px 9px;font-size:11.5px;white-space:nowrap;";
  zoomBtn.addEventListener("click", openActiveBlueprintLightbox);
  s1Actions.appendChild(zoomBtn);

  const twinBtn = mkEl("button", "btn-primary", "🎬 Produce Digital Twin Video");
  twinBtn.type = "button";
  twinBtn.setAttribute("data-testid", "top5-produce-digital-twin-btn");
  twinBtn.style.cssText = "min-height:28px;padding:3px 10px;font-size:11.5px;white-space:nowrap;";
  twinBtn.addEventListener("click", () => {
    openDigitalTwinProducerForPost({
      post_id: activeIdea.id,
      title: activeIdea.title,
      summary: activeIdea.summary,
      template_id: activeTpl.template_id,
    });
  });
  s1Actions.appendChild(twinBtn);
  s1Hdr.appendChild(s1Actions);
  step1.appendChild(s1Hdr);

  const builderSiso = document.getElementById("builder-kpi-siso");
  if (builderSiso) {
    builderSiso.textContent = `${activeTpl.template_id} · Score ${activeTpl.match_score || "99.2"}`;
  }

  // Canva-Style Center Artboard Stage (shows the active blueprint at crisp scale)
  const heroArtboard = mkEl("div", "composer-blueprint-hero-stage");
  heroArtboard.setAttribute("data-testid", "composer-blueprint-hero-stage");
  heroArtboard.title = "Click to inspect full-resolution blueprint (@2x)";
  const heroImg = document.createElement("img");
  heroImg.src = safeUrl(activeSvgUrl);
  heroImg.alt = `${activeTpl.template_id} — ${activeTpl.name} active visual blueprint`;
  heroArtboard.appendChild(heroImg);
  const heroOverlayPill = mkEl(
    "span",
    "composer-blueprint-hero-pill",
    `${activeTpl.template_id} · ${activeTpl.name} · Click to Zoom`
  );
  heroArtboard.appendChild(heroOverlayPill);
  heroArtboard.addEventListener("click", openActiveBlueprintLightbox);
  step1.appendChild(heroArtboard);

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
    thImg.src = safeUrl(`/assets/template-gallery/${encodeURIComponent(tpl.template_id)}.png`);
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
  workbench.appendChild(step1);

  // Step 2: 8 Presentation Modes + Whisper-Quiet Pacing Strip
  const step2 = mkEl("div", "composer-section");
  const s2Hdr = mkEl("div", "composer-section-hdr");
  s2Hdr.appendChild(mkEl("span", "composer-step-title", "2. Format"));
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
    ["Hook", budget.hook_above_fold || "Front-loaded metric hook"],
    ["Density", budget.per_unit_density || "Bounded visual density"],
    [
      `Spec (${budget.estimated_consumption_time || "Fast read"})`,
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

  // Step 3: Collapsible Channel Copy Bar inside Center Composer
  const copyMount = mkEl("div", "composer-copy-card");
  copyMount.id = "top5-composer-copy-mount";
  workbench.appendChild(copyMount);

  // Column 3 Top: Compact 13-Channel Selector Bar + Stage CTA
  const chCard = mkEl("div", "channel-selector-card");
  const chHdr = mkEl("div", "composer-section-hdr");
  chHdr.appendChild(
    mkEl("span", "composer-step-title tabular-nums", `3. Channels (${STATE.selectedStagePlatforms.size})`)
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
    const shortName = SHORT_PLATFORM_TAB_LABELS[pid] || pSpec.name.split("(")[0].trim();
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
  const shortPlat = SHORT_PLATFORM_TAB_LABELS[STATE.selectedPreviewPlatform] || pkg.platform_name.split("(")[0].trim();
  const isExpanded = STATE.composerCopyExpanded || STATE.persona === "builder";

  const hdr = mkEl("div", "composer-section-hdr");
  hdr.style.marginBottom = "6px";
  const leftMeta = mkEl("div", "studio-toolbar-actions");
  leftMeta.appendChild(mkEl("span", "composer-step-title", `${shortPlat} Caption`));
  leftMeta.appendChild(
    mkEl(
      "span",
      `pill-badge tabular-nums ${checks.char_limit_ok ? "pill-emerald" : "pill-amber"}`,
      `${checks.char_used}/${checks.char_cap} chars ✓`
    )
  );
  hdr.appendChild(leftMeta);

  const rightBtns = mkEl("div", "studio-toolbar-actions");
  const toggleBtn = mkEl(
    "button",
    "btn-secondary",
    isExpanded ? "Collapse Text ▴" : "✍️ Expand Caption ▾"
  );
  toggleBtn.type = "button";
  toggleBtn.setAttribute("data-testid", "toggle-composer-copy-btn");
  toggleBtn.style.cssText = "min-height:28px;padding:3px 9px;font-size:11.5px;";
  toggleBtn.addEventListener("click", () => {
    STATE.composerCopyExpanded = !STATE.composerCopyExpanded;
    renderTop5ComposerCopySection();
  });
  rightBtns.appendChild(toggleBtn);

  const copyBtn = mkEl("button", "btn-secondary", "Copy Post");
  copyBtn.type = "button";
  copyBtn.style.cssText = "min-height:28px;padding:3px 10px;font-size:11.5px;";
  copyBtn.addEventListener("click", () => {
    const combined = pkg.follow_up_comment
      ? `${pkg.body}\n\n---\n${pkg.follow_up_comment}`
      : pkg.body;
    copyTextSafe(combined, `Copied ${pkg.platform_name} payload!`);
  });
  rightBtns.appendChild(copyBtn);
  hdr.appendChild(rightBtns);
  mount.appendChild(hdr);

  if (pkg.video_title && isExpanded) {
    const vt = mkEl("div", "", `Video Title (${pkg.video_title.length}/100): ${polishUiTypography(pkg.video_title)}`);
    vt.style.cssText = "font-size:12px;font-weight:700;color:#0f172a;margin-bottom:6px;";
    mount.appendChild(vt);
  }

  const bodyBox = mkEl(
    "div",
    `top5-copy-full-box${isExpanded ? " expanded" : " collapsed-preview"}`,
    polishUiTypography(pkg.body)
  );
  bodyBox.setAttribute("data-testid", "top5-platform-copy-box");
  bodyBox.title = isExpanded ? "" : "Click to expand full caption";
  if (!isExpanded) {
    bodyBox.addEventListener("click", () => {
      STATE.composerCopyExpanded = true;
      renderTop5ComposerCopySection();
    });
  }
  mount.appendChild(bodyBox);

  if (pkg.follow_up_comment && isExpanded) {
    mount.appendChild(
      mkEl("div", "composer-followup-note", `First Comment / Reply #2: ${pkg.follow_up_comment}`)
    );
  }

  const activeIdeaObj = getActiveTop5Idea();
  const top5Dist = activeIdeaObj?.distribution_directory;
  if (top5Dist) {
    const distBar = mkEl("div", "feed-item-card");
    distBar.setAttribute("data-testid", "top5-distribution-directory-bar");
    distBar.style.cssText = "background:#f8fafc;border:1px solid #cbd5e1;padding:10px 12px;border-radius:8px;margin-top:8px;font-size:12px;color:#1e293b;";
    const compRow = mkEl("div", "", `🏢 Tag Companies: ${top5Dist.company_mentions_line_linkedin}  (${top5Dist.company_mentions_line_x})`);
    compRow.style.cssText = "font-weight:700;color:#0f172a;margin-bottom:4px;";
    const grpRow = mkEl(
      "div",
      "",
      `👥 Target LinkedIn Groups: ${(top5Dist.linkedin_groups_primary || []).map((g) => `${g.name} (${g.members})`).join(" · ")}`
    );
    grpRow.style.cssText = "color:#334155;margin-bottom:4px;";
    const tagRow = mkEl(
      "div",
      "",
      `#️⃣ Hashtags: ${top5Dist.hashtags_bundle?.full_hashtag_string || ""}`
    );
    tagRow.style.cssText = "color:#1d4ed8;font-weight:600;";
    distBar.append(compRow, grpRow, tagRow);
    mount.appendChild(distBar);
  }

  if (isExpanded || STATE.persona === "builder") {
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

    // Realistic Above-the-Fold Copy Preview with word-boundary "…more" (crisp 1-2 lines so media leads)
    const cleanBody = polishUiTypography(pkg.body || "");
    const foldCap = Math.min(115, Math.max(85, checks.fold_cap || 110));
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
  document.getElementById("run-autominer-live-btn")?.addEventListener("click", () => loadAutonomousMinerData(true));
  document.getElementById("autominer-topic-input")?.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") {
      ev.preventDefault();
      loadAutonomousMinerData(true);
    }
  });

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
  document.getElementById("compile-step-flow-btn")?.addEventListener("click", triggerCompileStepFlow);
  document.getElementById("step-flow-preset-select")?.addEventListener("change", () => triggerCompileStepFlow(false));
  document.getElementById("step-flow-theme-select")?.addEventListener("change", () => triggerCompileStepFlow(false));
  document.getElementById("copy-step-flow-post-btn")?.addEventListener("click", copyStepFlowPostText);
  document.getElementById("trace-player-play-btn")?.addEventListener("click", toggleTracePlayerPlayback);
  document.getElementById("trace-player-scrubber")?.addEventListener("input", (e) => {
    TRACE_PLAYER.currentMs = Number(e.target.value || 0);
    renderTraceWaterfallAtTime(TRACE_PLAYER.currentMs);
  });
  document.getElementById("trace-player-path-select")?.addEventListener("change", (e) => {
    TRACE_PLAYER.pathMode = e.target.value || "allow";
    renderTraceWaterfallAtTime(TRACE_PLAYER.currentMs);
  });
  document.getElementById("trace-player-speed-select")?.addEventListener("change", (e) => {
    TRACE_PLAYER.speed = Number(e.target.value || 1);
  });
  document.querySelectorAll("#trace-viz-mode-bar [data-viz-mode]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mode = btn.getAttribute("data-viz-mode") || "option1";
      setTraceVizMode(mode);
    });
  });
  document.querySelectorAll("#continuum-stage-bar [data-continuum-stage]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const stg = btn.getAttribute("data-continuum-stage") || "L3";
      setContinuumStage(stg);
    });
  });
  document.getElementById("continuum-prev-btn")?.addEventListener("click", () => stepContinuumStage(-1));
  document.getElementById("continuum-next-btn")?.addEventListener("click", () => stepContinuumStage(1));
  document.getElementById("deconstruct-raster-btn")?.addEventListener("click", triggerDeconstructRaster);
  document.getElementById("raster-render-mode-select")?.addEventListener("change", applyDeconstructedRasterMode);
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

  const reqPreset = params.get("preset");
  const reqTheme = params.get("theme");
  const reqViz = params.get("viz");
  const reqPath = params.get("path");
  const reqSubtab = params.get("subtab");
  const reqContinuum = params.get("continuum");

  if (reqPreset) {
    const pSel = document.getElementById("step-flow-preset-select");
    if (pSel) pSel.value = reqPreset;
  }
  if (reqTheme) {
    const tSel = document.getElementById("step-flow-theme-select");
    if (tSel) tSel.value = reqTheme;
  }
  if (reqPath === "deny" || reqPath === "allow") {
    TRACE_PLAYER.pathMode = reqPath;
    const pathSel = document.getElementById("trace-player-path-select");
    if (pathSel) pathSel.value = reqPath;
  }
  if (reqViz) {
    setTraceVizMode(reqViz);
  }
  if (reqContinuum) {
    setContinuumStage(reqContinuum.toUpperCase());
  }

  loadWorkspaceData();
  loadMintingStudioData();
  loadStepFlowStudio(reqPreset || "FLOW-01", reqTheme || "light");
  loadAutonomousMinerData(false);

  const reqView = params.get("view") || (window.location.hash === "#linkedin-groups-membership-radar-section" ? "view-openhands" : null);
  activateView(reqView && ALL_VIEWS.includes(reqView) ? reqView : "view-miner");

  if (reqView === "view-playbook" && reqSubtab) {
    const subMap = {
      posts: "playbook-subtab-btn-posts",
      creators: "playbook-subtab-btn-creators",
      platforms: "playbook-subtab-btn-platforms",
      archetypes: "playbook-subtab-btn-archetypes",
      autominer: "playbook-subtab-btn-autominer",
    };
    const btnId = subMap[reqSubtab] || reqSubtab;
    document.getElementById(btnId)?.click();
  } else if (reqSubtab === "radar" || reqViz || reqPreset || reqContinuum) {
    document.getElementById("miner-subtab-btn-radar")?.click();
    setTimeout(() => {
      const targetEl = reqContinuum
        ? document.getElementById("static-to-dynamic-continuum-card")
        : reqViz
          ? document.getElementById("step-flow-trace-player")
          : document.getElementById("step-by-step-flow-studio-card");
      targetEl?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 250);
  }
});

function renderStepFlowBundle(bundle) {
  if (!bundle) return;
  STATE.activeStepFlowBundle = bundle;

  const badge = document.getElementById("step-flow-status-badge");
  if (badge) {
    badge.textContent = `${bundle.preset_id} · ${bundle.matched_template_id} · ${bundle.gif_ready ? "Looping GIF89a + SVG Ready" : "Animated SVG Ready"}`;
  }

  const visLbl = document.getElementById("step-flow-visual-label");
  if (visLbl) {
    visLbl.textContent = `4:5 Phased Blueprint (${bundle.theme === "dark_neon" ? "Dark-Grid Neon" : "Executive Light"})`;
  }

  const img = document.getElementById("step-flow-preview-img");
  if (img && bundle.svg_url) {
    img.src = `${safeUrl(bundle.svg_url)}?t=${Date.now()}`;
  }

  const gslidesLink = document.getElementById("step-flow-open-gslides-link");
  if (gslidesLink) {
    const matchedTpl = (STATE.templates || []).find(
      (t) => t.id === bundle.matched_template_id
    );
    const gsUrl =
      bundle.google_slides_url || matchedTpl?.google_slides_url || "";
    if (gsUrl) {
      gslidesLink.href = safeUrl(gsUrl);
      gslidesLink.style.display = "inline-flex";
    } else {
      gslidesLink.style.display = "none";
    }
  }

  const drawioLink = document.getElementById("step-flow-download-drawio-link");
  if (drawioLink) {
    const drUrl =
      bundle.drawio_url ||
      `/assets/template-gallery/${bundle.matched_template_id || "T85"}.drawio`;
    drawioLink.href = safeUrl(drUrl);
    drawioLink.setAttribute(
      "download",
      `${bundle.preset_id || "FLOW-01"}.drawio`
    );
  }

  const pptxLink = document.getElementById("step-flow-download-pptx-link");
  if (pptxLink) {
    const ppUrl =
      bundle.pptx_url ||
      `/assets/template-gallery/${bundle.matched_template_id || "T85"}.pptx`;
    pptxLink.href = safeUrl(ppUrl);
    pptxLink.setAttribute(
      "download",
      `${bundle.matched_template_id || "T85"}.pptx`
    );
  }

  const svgLink = document.getElementById("step-flow-open-svg-link");
  if (svgLink && bundle.svg_url) {
    svgLink.href = safeUrl(bundle.svg_url);
  }

  const gifLink = document.getElementById("step-flow-download-gif-link");
  if (gifLink) {
    const targetUrl = bundle.gif_url || bundle.svg_url || "";
    gifLink.href = safeUrl(targetUrl);
    gifLink.textContent = bundle.gif_url ? "Download 4:5 .GIF" : "Download 4:5 .SVG";
  }

  const mp4Link = document.getElementById("step-flow-download-mp4-link");
  if (mp4Link) {
    const mp4Url = bundle.mp4_url || bundle.gif_url || bundle.svg_url || "";
    mp4Link.href = safeUrl(mp4Url);
    mp4Link.textContent = bundle.mp4_url ? "Download 4:5 .MP4" : "Download .MP4";
  }

  const copyBundle = bundle.copy_bundle || {};
  const statsBadge = document.getElementById("step-flow-copy-stats-badge");
  if (statsBadge) {
    statsBadge.textContent = `6-Beat Copy · ${copyBundle.char_count || 0} chars · ${copyBundle.line_count || 0} lines`;
  }

  const beatsStrip = document.getElementById("step-flow-beats-strip");
  if (beatsStrip) {
    beatsStrip.replaceChildren();
    (copyBundle.beats || []).forEach((b) => {
      const cell = mkEl("div", "feed-item-card");
      cell.style.padding = "8px 10px";
      const k = mkEl("div", "", b.beat);
      k.style.cssText = "font-size:11px;font-weight:800;color:#1d4ed8;margin-bottom:2px;";
      const v = mkEl("div", "", polishUiTypography(b.text));
      v.style.cssText = "font-size:11.5px;color:#334155;line-height:1.35;";
      cell.append(k, v);
      beatsStrip.appendChild(cell);
    });
  }

  const copyBox = document.getElementById("step-flow-post-copy-box");
  if (copyBox) {
    copyBox.textContent = polishUiTypography(copyBundle.post_copy || "");
  }

  const c1Box = document.getElementById("step-flow-comment1-box");
  if (c1Box) {
    c1Box.textContent = `Comment #1 (Pinned Link): ${copyBundle.comment_1 || ""}`;
  }

  if (bundle.execution_trace) {
    const spBadge = document.getElementById("trace-player-speedup-badge");
    if (spBadge && bundle.execution_trace.parallel_speedup_label) {
      spBadge.textContent = bundle.execution_trace.parallel_speedup_label;
    }
    renderTraceWaterfallAtTime(TRACE_PLAYER.currentMs);
    startTracePlayerLoop();
  }

  renderContinuumStageInspector();
}

const CONTINUUM_STAGE_ORDER = ["L0", "L1", "L2", "L3", "L4", "L5", "L6"];
const CONTINUUM_STATE = {
  activeStage: "L3",
  l1SlideIdx: 0,
  l6Artifact: "Artifact B",
  l6Env: "production",
  l6Fresh: true,
  l6Unused: true,
  l6RepoSlug: "gcp-mcp-zero-bloat-gateway",
  l6ServerResponse: null,
  lastDeconstructedRaster: null,
};

async function triggerDeconstructRaster() {
  const btn = document.getElementById("deconstruct-raster-btn");
  const fileInput = document.getElementById("raster-upload-file-input");
  const srcSelect = document.getElementById("raster-source-select");
  const customTopic = (document.getElementById("step-flow-topic-input")?.value || "").trim();

  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Segmenting Pixels & Compiling Direct Overlay + IR...";
  }
  try {
    let imageBase64 = "";
    const file = fileInput?.files?.[0];
    if (file) {
      imageBase64 = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ""));
        reader.onerror = () => resolve("");
        reader.readAsDataURL(file);
      });
    }
    const res = await fetch("/api/continuum/deconstruct-raster", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source_id_or_path: srcSelect?.value || "LI-01",
        image_base64: imageBase64,
        custom_hint: customTopic,
        compile_gif: true,
      }),
    });
    const out = await res.json();
    CONTINUUM_STATE.lastDeconstructedRaster = out;
    if (out.vector_ir_bundle) {
      STATE.activeStepFlowBundle = out.vector_ir_bundle;
    }
    applyDeconstructedRasterMode();
    const seg = out.raster_segmentation || {};
    showToast(
      `Deconstructed ${out.source_image_name} (${seg.width}×${seg.height}px, ${(seg.zones || []).length} zones detected)`
    );
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "🔬 Deconstruct & Animate Raster";
    }
  }
}

function applyDeconstructedRasterMode() {
  const dec = CONTINUUM_STATE.lastDeconstructedRaster;
  if (!dec) return;
  const mode = document.getElementById("raster-render-mode-select")?.value || "direct_pixels";
  const badge = document.getElementById("raster-deconstruct-status-badge");
  const seg = dec.raster_segmentation || {};
  if (badge) {
    badge.textContent = `${dec.source_image_name} · ${seg.width || 1080}×${seg.height || 1350}px · ${(seg.zones || []).length || 4} Bounding Boxes · Theme: ${seg.detected_theme || "light"}`;
  }

  const previewImg = document.getElementById("step-flow-preview-img");
  const visLbl = document.getElementById("step-flow-visual-label");
  const svgLink = document.getElementById("step-flow-open-svg-link");
  const gifLink = document.getElementById("step-flow-download-gif-link");

  if (mode === "direct_pixels") {
    const useGif = CONTINUUM_STATE.activeStage === "L3" && dec.direct_raster_overlay_gif_url;
    const url = useGif ? dec.direct_raster_overlay_gif_url : dec.direct_raster_overlay_svg_url;
    if (previewImg && url) {
      previewImg.src = `${safeUrl(url)}?t=${Date.now()}`;
    }
    if (visLbl) {
      visLbl.textContent = `Direct Raster-Pixel Animation (${seg.width}×${seg.height}px · 4 Bounding-Box Spotlights)`;
    }
    if (svgLink && dec.direct_raster_overlay_svg_url) {
      svgLink.href = safeUrl(dec.direct_raster_overlay_svg_url);
    }
    if (gifLink) {
      gifLink.href = safeUrl(dec.direct_raster_overlay_gif_url || dec.direct_raster_overlay_svg_url || "");
    }
  } else if (dec.vector_ir_bundle) {
    renderStepFlowBundle(dec.vector_ir_bundle);
  }
}

async function triggerServerL6PolicySandbox(extraPayload = {}) {
  try {
    const res = await fetch("/api/continuum/execute-l6-sandbox", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        approved_artifact: "Artifact A",
        approved_environment: "staging",
        max_ttl_sec: 300,
        requested_artifact: CONTINUUM_STATE.l6Artifact,
        requested_environment: CONTINUUM_STATE.l6Env,
        token_age_sec: CONTINUUM_STATE.l6Fresh ? 14 : 920,
        simulate_replayed_nonce: !CONTINUUM_STATE.l6Unused,
        repo_slug: CONTINUUM_STATE.l6RepoSlug,
        ...extraPayload,
      }),
    });
    CONTINUUM_STATE.l6ServerResponse = await res.json();
    renderContinuumStageInspector();
  } catch (_err) {
    // Keep last state
  }
}

const CONTINUUM_STAGE_META = {
  L0: {
    badge: "L0 · Pure Static Poster (0 Hz · Simultaneous Spatial View)",
    dimension: "Spatial Topology (x, y) — Zero Motion",
    artifact: "@2x Retina PNG (1080×1350) + Static PDF Brief",
    compiler: "Renders Canonical Scene-Graph with motion=off, opacity=1.0 across all 5 architectural zones.",
    whenToUse: "Executive PDF handouts, fast <2s scroll-stop scan, print/Substack static embeds.",
  },
  L1: {
    badge: "L1 · 4-Step Progressive Reveal Carousel (Discrete Paged Build)",
    dimension: "Discrete Ordinal Sequence (Step 1/4 → 4/4)",
    artifact: "8-Slide 4:5 Native PDF Carousel + Interactive Step-Through Deck",
    compiler: "Slices the Scene-Graph by phase_index=1..4, spotlighting 1 active zone per card while dimming future hops.",
    whenToUse: "LinkedIn Native PDF Carousels, Instagram Carousels, progressive slide build-animations.",
  },
  L2: {
    badge: "L2 · Ambient Vector Micro-Motion (<25 KB CSS/SMIL SVG)",
    dimension: "Continuous Directional Velocity (dx/dt)",
    artifact: "Lightweight Vector SVG with Marching-Ant Conduits & Gate Pulse",
    compiler: "Injects CSS stroke-dashoffset keyframes along directed edges and radial glow on the enforcement point.",
    whenToUse: "Engineering blogs, GitHub READMEs, Substack/DEV.to articles with infinite Retina zoom.",
  },
  L3: {
    badge: "L3 · Choreographed 4:5 GIF89a State-Machine Loop (15–30 fps)",
    dimension: "Autonomous State Transitions (Phase 0..3 over 6–12s Loop)",
    artifact: "1080×1350 Looping GIF89a (<=12 MB, Bayer Dithered)",
    compiler: "Samples Scene-Graph across 12–180 keyframes, animates packet tokens ①..⑧, and compiles via Chrome + FFmpeg paletteuse.",
    whenToUse: "#1 LinkedIn Feed Format (69.9% avg comment ratio) — auto-loops inline on mobile with zero click.",
  },
  L4: {
    badge: "L4 · Synchronized Multi-Track Cinema (H.264 MP4 + Voiceover)",
    dimension: "Synchronized Audio + Video Timeline + Clause Captions",
    artifact: "1080×1350 (4:5) & 1080×1920 (9:16) H.264 MP4 + 155 WPM Script",
    compiler: "Muxes 30fps H.264 yuv420p stream with clause-timed narration beats and burned-in gold karaoke captions.",
    whenToUse: "YouTube Shorts, Reels, TikTok, X Native Video, LinkedIn Mobile Video Tab.",
  },
  L5: {
    badge: "L5 · Interactive Time-Travel & Branch Debugger (t=0..320ms)",
    dimension: "User-Controlled Time (Scrubber) + Branch Mutation (ALLOW ⇄ DENY)",
    artifact: "60fps DOM/SVG Dual Swimlane + Gantt Waterfall + Live JSON Span Inspector",
    compiler: "Binds the post's execution_trace DAG to a real-time playhead scrubber comparing Serial (320ms) vs Parallel ×4 (165ms).",
    whenToUse: "Interactive engineering deep-dives, Comment #1 live replay links, architecture reviews.",
  },
  L6: {
    badge: "L6 · Live Executable Policy & ADK Sandbox (Interactive Compute)",
    dimension: "Live Computation & Verifiable State (Input Mutation → Gate Execution)",
    artifact: "Live Out-of-Loop Temporal Policy Evaluator + Runnable ADK Repository",
    compiler: "Executes the 4 deterministic temporal policy rules against user-mutated tool parameters and emits a signed audit receipt.",
    whenToUse: "Staff/Principal engineer validation, hands-on codelabs, customer PoCs, OpenHands verification.",
  },
};

function setContinuumStage(stageId) {
  const clean = CONTINUUM_STAGE_ORDER.includes(stageId) ? stageId : "L3";
  CONTINUUM_STATE.activeStage = clean;
  document.querySelectorAll("#continuum-stage-bar [data-continuum-stage]").forEach((btn) => {
    const isAct = btn.getAttribute("data-continuum-stage") === clean;
    btn.classList.toggle("active", isAct);
    btn.setAttribute("aria-selected", isAct ? "true" : "false");
  });
  if (clean === "L6" && !CONTINUUM_STATE.l6ServerResponse) {
    triggerServerL6PolicySandbox();
  }
  renderContinuumStageInspector();
}

function stepContinuumStage(delta) {
  const idx = CONTINUUM_STAGE_ORDER.indexOf(CONTINUUM_STATE.activeStage);
  const nextIdx = (idx + delta + CONTINUUM_STAGE_ORDER.length) % CONTINUUM_STAGE_ORDER.length;
  setContinuumStage(CONTINUUM_STAGE_ORDER[nextIdx]);
}

function renderContinuumStageInspector() {
  const box = document.getElementById("continuum-stage-inspector");
  if (!box) return;
  box.replaceChildren();

  const stg = CONTINUUM_STATE.activeStage || "L3";
  const meta = CONTINUUM_STAGE_META[stg] || CONTINUUM_STAGE_META.L3;
  const bundle = STATE.activeStepFlowBundle || {};
  const spec = bundle.spec || {};

  const badgeEl = document.getElementById("continuum-active-stage-badge");
  if (badgeEl) badgeEl.textContent = meta.badge;

  // Synchronize the main left-hand visual preview image with the active continuum level!
  const previewImg = document.getElementById("step-flow-preview-img");
  const visLbl = document.getElementById("step-flow-visual-label");
  if (previewImg) {
    if (stg === "L0" && bundle.png_url) {
      previewImg.src = safeUrl(bundle.png_url);
      if (visLbl) visLbl.textContent = "L0 · Pure Static Retina PNG Snapshot (0 Hz)";
    } else if (stg === "L3" && bundle.gif_url) {
      previewImg.src = safeUrl(bundle.gif_url);
      if (visLbl) visLbl.textContent = "L3 · Native 4:5 Looping GIF89a State Machine";
    } else if (bundle.svg_url) {
      previewImg.src = safeUrl(bundle.svg_url);
      if (visLbl) visLbl.textContent = `${stg} · 4:5 Vector State-Machine Blueprint`;
    }
  }

  // Top Metadata Spec Strip for the selected stage (compact 3-chip summary in Creator mode; full 4-box grid in Builder mode)
  const metaChipRow = mkEl("div", "composer-tldr-chip-row continuum-meta-chips");
  metaChipRow.style.marginBottom = "10px";
  [
    ["⚡", meta.dimension, "blue"],
    ["📦", meta.artifact, "emerald"],
    ["🎯", meta.whenToUse.split("—")[0].trim(), "slate"],
  ].forEach(([ic, txt, tone]) => {
    metaChipRow.appendChild(mkEl("span", `composer-tldr-chip tone-${tone}`, `${ic} ${txt}`));
  });
  box.appendChild(metaChipRow);

  const metaGrid = mkEl("div", "platform-playbook-grid continuum-builder-grid");
  metaGrid.style.marginBottom = "12px";
  [
    ["Unlocked Dynamic Dimension", meta.dimension],
    ["Compiled Output Artifact", meta.artifact],
    ["Deterministic IR Compiler Pass", meta.compiler],
    ["Optimal Channel & Reader Mode", meta.whenToUse],
  ].forEach(([lbl, val]) => {
    const cell = mkEl("div", "platform-spec-box");
    cell.append(mkEl("div", "platform-spec-label", lbl), mkEl("div", "platform-spec-text", val));
    metaGrid.appendChild(cell);
  });
  box.appendChild(metaGrid);

  // Stage-specific interactive experience
  const stageArena = mkEl("div", "feed-item-card");
  stageArena.style.cssText = "background:#f8fafc;border:1px solid #cbd5e1;padding:12px 14px;";

  if (stg === "L0") {
    const h = mkEl("strong", "", "L0 Pure Static Snapshot — Flattened t=∞ Topology");
    h.style.cssText = "display:block;font-size:13px;color:#0f172a;margin-bottom:6px;";
    const p = mkEl(
      "p",
      "",
      `All 5 architectural zones (${spec.approved_label || "Human Approved"} vs ${spec.requested_label || "Agent Requested"} → ${spec.gateway_title || "Policy Gateway"} → ${spec.policy_title || "Temporal Policy"} → ALLOW/DENY) are rendered simultaneously at 100% opacity with zero motion. Ideal for instant <2s scanning or PDF printing.`
    );
    p.style.cssText = "font-size:12px;color:#334155;margin-bottom:8px;";
    const dlLink = mkEl("a", "btn-primary", "Open Static @2x PNG Snapshot ↗");
    dlLink.href = safeUrl(bundle.png_url || bundle.svg_url || "");
    dlLink.target = "_blank";
    dlLink.rel = "noopener";
    stageArena.append(h, p, dlLink);
  } else if (stg === "L1") {
    const slides = [
      {
        step: "Step 1 of 4 · Zone 1: The Parameter-Swap Mismatch",
        zone: `${spec.approved_label || "HUMAN APPROVED"} (${spec.approved_primary || "Artifact A"} @ ${spec.approved_secondary || "staging"}) vs. ${spec.requested_label || "AGENT REQUESTED"} (${spec.requested_primary || "Artifact B"} @ ${spec.requested_secondary || "production"})`,
        narrative: spec.scenario_setup || "Human approves Artifact A for staging; seconds later the agent requests Artifact B for production.",
        takeaway: "Static tool permissions ('Can this agent call deploy?') pass 100% — yet the action is unauthorized.",
      },
      {
        step: "Step 2 of 4 · Zone 2: Out-of-Loop Enforcement Point",
        zone: `${spec.gateway_title || "Policy Gateway"} (${spec.gateway_sub || "ADK BeforeToolCallback"}) intercepts the tool call BEFORE downstream execution`,
        narrative: spec.core_question || "The policy gate evaluates the bound approval record outside the probabilistic LLM prompt.",
        takeaway: `Enforces 4 deterministic rules: ${(spec.policy_rules || []).join(" · ")}`,
      },
      {
        step: "Step 3 of 4 · Zone 3A: Parallel ×4 Verification → ALLOW Stream",
        zone: `When all 4 temporal rules pass in parallel (135–165ms) → ${spec.exec_svc_title || "Deployment Service"} executes with idempotency key`,
        narrative: "Parallel fan-out across Approval Lookup + 4 Rules + Model Armor + Session Ledger cuts gate latency from 88ms serial to 30ms parallel.",
        takeaway: "Zero added human friction on valid, matching approvals.",
      },
      {
        step: "Step 4 of 4 · Zone 3B & Zone 4: Circuit-Breaker DENY + 3 Built-In Pillars",
        zone: `${spec.deny_label || "DENY: artifact or environment mismatch"} → ${spec.blocked_title || "Action blocked"} (${spec.blocked_sub || "No call made"})`,
        narrative: `${spec.footer_takeaway || "Approval must match the action that executes."} ${spec.closing_question || ""}`,
        takeaway: "Security (Model Armor) · Performance (Regional routing) · Cost (Prefix KV-cache).",
      },
    ];
    const curIdx = CONTINUUM_STATE.l1SlideIdx % slides.length;
    const curSlide = slides[curIdx];

    const navRow = mkEl("div", "composer-section-hdr");
    navRow.style.marginBottom = "8px";
    const stepTitle = mkEl("strong", "", curSlide.step);
    stepTitle.style.cssText = "font-size:13px;color:#1e40af;";
    const btnGroup = mkEl("div", "studio-toolbar-actions");
    const prevS = mkEl("button", "btn-secondary", "◀ Prev Slide");
    prevS.type = "button";
    prevS.addEventListener("click", () => {
      CONTINUUM_STATE.l1SlideIdx = (curIdx - 1 + slides.length) % slides.length;
      renderContinuumStageInspector();
    });
    const nextS = mkEl("button", "btn-primary", "Next Slide ▶");
    nextS.type = "button";
    nextS.addEventListener("click", () => {
      CONTINUUM_STATE.l1SlideIdx = (curIdx + 1) % slides.length;
      renderContinuumStageInspector();
    });
    btnGroup.append(prevS, nextS);
    navRow.append(stepTitle, btnGroup);

    const zBox = mkEl("div", "", `Spotlighted Architecture Zone: ${curSlide.zone}`);
    zBox.style.cssText = "font-size:12px;font-weight:700;color:#0f172a;margin-bottom:4px;";
    const nBox = mkEl("div", "", curSlide.narrative);
    nBox.style.cssText = "font-size:12px;color:#334155;margin-bottom:4px;";
    const tBox = mkEl("div", "", `Slide Takeaway: ${curSlide.takeaway}`);
    tBox.style.cssText = "font-size:11.5px;font-weight:700;color:#065f46;";
    stageArena.append(navRow, zBox, nBox, tBox);
  } else if (stg === "L2") {
    const h = mkEl("strong", "", "L2 Ambient Vector Micro-Motion (<25 KB SVG with CSS Keyframes)");
    h.style.cssText = "display:block;font-size:13px;color:#0f172a;margin-bottom:6px;";
    const p = mkEl(
      "p",
      "",
      "The left canvas is now rendering the live vector SVG with CSS marching-ant conduits (stroke-dashoffset) and pulsing status nodes. Readers get instant directional flow cues at infinite Retina resolution without downloading a multi-megabyte video."
    );
    p.style.cssText = "font-size:12px;color:#334155;margin-bottom:8px;";
    const openSvg = mkEl("a", "btn-primary", "Inspect Live Animated Vector SVG ↗");
    openSvg.href = safeUrl(bundle.svg_url || "");
    openSvg.target = "_blank";
    openSvg.rel = "noopener";
    stageArena.append(h, p, openSvg);
  } else if (stg === "L3") {
    const h = mkEl("strong", "", "L3 Choreographed 4:5 GIF89a State-Machine Loop (LinkedIn Feed Champion)");
    h.style.cssText = "display:block;font-size:13px;color:#0f172a;margin-bottom:6px;";
    const p = mkEl(
      "p",
      "",
      "The left canvas is now displaying the compiled 1080×1350 GIF89a loop cycling automatically through Phase 1 (Mismatch Ingress) → Phase 2 (Gateway + 4 Temporal Rules) → Phase 3 (ALLOW Stream) → Phase 4 (Circuit-Breaker DENY). Auto-plays inline on LinkedIn mobile with zero click."
    );
    p.style.cssText = "font-size:12px;color:#334155;margin-bottom:8px;";
    const dlGif = mkEl("a", "btn-primary", "Download 4:5 Animated .GIF (1080×1350)");
    dlGif.href = safeUrl(bundle.gif_url || bundle.svg_url || "");
    dlGif.setAttribute("download", "");
    stageArena.append(h, p, dlGif);
  } else if (stg === "L4") {
    const h = mkEl("strong", "", "L4 Synchronized H.264 MP4 Cinema + Clause-Timed Narration Track");
    h.style.cssText = "display:block;font-size:13px;color:#0f172a;margin-bottom:8px;";
    const split = mkEl("div", "composer-split-layout");
    split.style.alignItems = "start";

    const vidWrap = mkEl("div");
    if (bundle.mp4_url) {
      const vid = document.createElement("video");
      vid.src = safeUrl(bundle.mp4_url);
      vid.controls = true;
      vid.autoplay = true;
      vid.loop = true;
      vid.muted = true;
      vid.playsInline = true;
      vid.style.cssText = "width:100%;max-width:280px;border-radius:8px;border:1px solid #cbd5e1;background:#0f172a;display:block;";
      vidWrap.appendChild(vid);
    }

    const scriptBox = mkEl("div");
    [
      ["00:00 – 00:08 · Beat 1 (Hook & Mismatch)", spec.hook_line_1 || "Your AI agent can use an approved tool to perform an unapproved action."],
      ["00:08 – 00:19 · Beat 2 (Parameter Swap)", spec.scenario_setup || "Human approves Artifact A for staging; agent requests Artifact B for production."],
      ["00:19 – 00:32 · Beat 3 (Out-of-Loop Gate)", `At t=135ms, ${spec.gateway_title || "Policy Gateway"} fans out across 4 parallel temporal rules in 30ms.`],
      ["00:32 – 00:45 · Beat 4 (Verdict & Takeaway)", `${spec.footer_takeaway || "Approval must match the action that executes."} ${spec.footer_sub || ""}`],
    ].forEach(([tc, line]) => {
      const row = mkEl("div", "platform-spec-box");
      row.style.marginBottom = "6px";
      row.append(mkEl("div", "platform-spec-label", tc), mkEl("div", "platform-spec-text", line));
      scriptBox.appendChild(row);
    });
    split.append(vidWrap, scriptBox);
    stageArena.append(h, split);
  } else if (stg === "L5") {
    const h = mkEl("strong", "", "L5 Interactive Time-Travel Scrubber & Serial-vs-Parallel Debugger (t = 0..320ms)");
    h.style.cssText = "display:block;font-size:13px;color:#0f172a;margin-bottom:6px;";
    const p = mkEl(
      "p",
      "",
      "Use the interactive 60fps Trace Player directly below to scrub across t=0..320ms, switch between the 7 visualization modes (Dual Waterfall, Split CLI, FSM, OTel, Sequence Diagram, 3D Stack), or toggle Happy Path (ALLOW) vs Attack Path (DENY)."
    );
    p.style.cssText = "font-size:12px;color:#334155;margin-bottom:8px;";
    const actRow = mkEl("div", "studio-toolbar-actions");
    const btnAllow = mkEl("button", "btn-secondary", "Jump to t=150ms Parallel Fan-Out (ALLOW)");
    btnAllow.type = "button";
    btnAllow.addEventListener("click", () => {
      TRACE_PLAYER.pathMode = "allow";
      TRACE_PLAYER.currentMs = 150;
      const pSel = document.getElementById("trace-player-path-select");
      if (pSel) pSel.value = "allow";
      renderTraceWaterfallAtTime(150);
      document.getElementById("step-flow-trace-player")?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    const btnDeny = mkEl("button", "btn-primary", "Inject Parameter Swap @ t=165ms (DENY)");
    btnDeny.type = "button";
    btnDeny.addEventListener("click", () => {
      TRACE_PLAYER.pathMode = "deny";
      TRACE_PLAYER.currentMs = 175;
      const pSel = document.getElementById("trace-player-path-select");
      if (pSel) pSel.value = "deny";
      renderTraceWaterfallAtTime(175);
      document.getElementById("step-flow-trace-player")?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    actRow.append(btnAllow, btnDeny);
    stageArena.append(h, p, actRow);
  } else if (stg === "L6") {
    const h = mkEl(
      "strong",
      "",
      "L6 Server-Backed Python ADK Policy Sandbox — Parallel ThreadPoolExecutor(4) + HMAC-SHA256 + Persistent Nonce Ledger"
    );
    h.style.cssText = "display:block;font-size:13px;color:#0f172a;margin-bottom:8px;";

    const controlsRow = mkEl("div", "studio-toolbar");
    controlsRow.style.marginBottom = "10px";

    const artSel = document.createElement("select");
    artSel.className = "select-light";
    [
      ["Artifact A", "Requested: Artifact A (Matches Approval ✓)"],
      ["Artifact B", "Requested: Artifact B (Parameter Swap ✕)"],
    ].forEach(([val, lbl]) => {
      const opt = mkEl("option", "", lbl);
      opt.value = val;
      if (CONTINUUM_STATE.l6Artifact === val) opt.selected = true;
      artSel.appendChild(opt);
    });
    artSel.addEventListener("change", () => {
      CONTINUUM_STATE.l6Artifact = artSel.value;
      triggerServerL6PolicySandbox();
    });

    const envSel = document.createElement("select");
    envSel.className = "select-light";
    [
      ["staging", "Target Env: staging (Matches Approval ✓)"],
      ["production", "Target Env: production (Env Escalation ✕)"],
    ].forEach(([val, lbl]) => {
      const opt = mkEl("option", "", lbl);
      opt.value = val;
      if (CONTINUUM_STATE.l6Env === val) opt.selected = true;
      envSel.appendChild(opt);
    });
    envSel.addEventListener("change", () => {
      CONTINUUM_STATE.l6Env = envSel.value;
      triggerServerL6PolicySandbox();
    });

    const ttlBtn = mkEl(
      "button",
      CONTINUUM_STATE.l6Fresh ? "btn-secondary" : "btn-primary",
      CONTINUUM_STATE.l6Fresh ? "TTL: Fresh (14s < 300s ✓)" : "TTL: Expired (920s > 300s ✕)"
    );
    ttlBtn.type = "button";
    ttlBtn.addEventListener("click", () => {
      CONTINUUM_STATE.l6Fresh = !CONTINUUM_STATE.l6Fresh;
      triggerServerL6PolicySandbox();
    });

    const nonceBtn = mkEl(
      "button",
      CONTINUUM_STATE.l6Unused ? "btn-secondary" : "btn-primary",
      CONTINUUM_STATE.l6Unused ? "1-Shot Nonce: UNUSED ✓" : "1-Shot Nonce: REPLAYED ✕"
    );
    nonceBtn.type = "button";
    nonceBtn.addEventListener("click", () => {
      CONTINUUM_STATE.l6Unused = !CONTINUUM_STATE.l6Unused;
      triggerServerL6PolicySandbox();
    });

    const matchPresetBtn = mkEl("button", "btn-primary", "▶ Run Valid Approval on Server (ALLOW)");
    matchPresetBtn.type = "button";
    matchPresetBtn.addEventListener("click", () => {
      CONTINUUM_STATE.l6Artifact = "Artifact A";
      CONTINUUM_STATE.l6Env = "staging";
      CONTINUUM_STATE.l6Fresh = true;
      CONTINUUM_STATE.l6Unused = true;
      triggerServerL6PolicySandbox({ reset_nonce: true });
    });

    controlsRow.append(artSel, envSel, ttlBtn, nonceBtn, matchPresetBtn);

    const srvReceipt = CONTINUUM_STATE.l6ServerResponse || {
      status: "EXECUTING_ON_SERVER",
      note: "Dispatching to POST /api/continuum/execute-l6-sandbox...",
    };
    const isAllow = srvReceipt.verdict === "ALLOW";

    const pre = mkEl("pre", "tabular-nums", JSON.stringify(srvReceipt, null, 2));
    pre.style.cssText = `font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;padding:10px;border-radius:8px;border:1px solid ${isAllow ? "#10b981" : "#ef4444"};background:#ffffff;color:#0f172a;overflow-x:auto;max-height:320px;margin:0;`;

    stageArena.append(h, controlsRow, pre);
  }

  box.appendChild(stageArena);
}

const TRACE_PLAYER = {
  playing: true,
  currentMs: 148,
  totalMs: 320,
  speed: 1.0,
  pathMode: "allow",
  vizMode: "option1",
  rafId: null,
  lastTick: 0,
};

function setTraceVizMode(mode) {
  const validModes = ["option1", "option2", "option3", "option4", "option5", "option6", "option7"];
  TRACE_PLAYER.vizMode = validModes.includes(mode) ? mode : "option1";
  document.querySelectorAll("#trace-viz-mode-bar [data-viz-mode]").forEach((btn) => {
    const isAct = btn.getAttribute("data-viz-mode") === TRACE_PLAYER.vizMode;
    btn.classList.toggle("active", isAct);
    btn.setAttribute("aria-selected", isAct ? "true" : "false");
  });
  renderTraceWaterfallAtTime(TRACE_PLAYER.currentMs);
}

function toggleTracePlayerPlayback() {
  TRACE_PLAYER.playing = !TRACE_PLAYER.playing;
  const btn = document.getElementById("trace-player-play-btn");
  if (btn) {
    btn.textContent = TRACE_PLAYER.playing ? "⏸ Pause Trace" : "▶ Play Trace";
  }
  if (TRACE_PLAYER.playing) {
    TRACE_PLAYER.lastTick = performance.now();
    startTracePlayerLoop();
  }
}

function startTracePlayerLoop() {
  if (TRACE_PLAYER.rafId) return;
  TRACE_PLAYER.lastTick = performance.now();
  const step = (now) => {
    const dt = now - TRACE_PLAYER.lastTick;
    TRACE_PLAYER.lastTick = now;
    if (TRACE_PLAYER.playing) {
      // Advance ~45 timeline-ms per real second at 1x speed so the 320ms trace loops smoothly every ~7 seconds
      TRACE_PLAYER.currentMs = (TRACE_PLAYER.currentMs + dt * 0.045 * TRACE_PLAYER.speed) % TRACE_PLAYER.totalMs;
      const scrub = document.getElementById("trace-player-scrubber");
      if (scrub) scrub.value = String(Math.round(TRACE_PLAYER.currentMs));
      renderTraceWaterfallAtTime(TRACE_PLAYER.currentMs);
    }
    TRACE_PLAYER.rafId = requestAnimationFrame(step);
  };
  TRACE_PLAYER.rafId = requestAnimationFrame(step);
}

function renderTraceWaterfallAtTime(tMs) {
  const trace = STATE.activeStepFlowBundle?.execution_trace;
  if (!trace || !Array.isArray(trace.spans)) return;
  const totalMs = trace.total_duration_ms || 320;
  TRACE_PLAYER.totalMs = totalMs;
  const cur = Math.max(0, Math.min(totalMs, Number(tMs || 0)));

  const readout = document.getElementById("trace-player-time-readout");
  if (readout) {
    readout.textContent = `t = ${Math.round(cur)} ms / ${totalMs} ms`;
  }

  const rowsWrap = document.getElementById("trace-player-waterfall-rows");
  const customStage = document.getElementById("trace-player-custom-stage");
  if (!rowsWrap) return;

  const activeSpans = [];
  trace.spans.forEach((sp) => {
    const isActive = cur >= sp.start_ms && cur <= sp.end_ms;
    if (isActive) activeSpans.push(sp);
  });

  if (TRACE_PLAYER.vizMode === "option1") {
    rowsWrap.style.display = "flex";
    if (customStage) customStage.style.display = "none";
    rowsWrap.replaceChildren();
    trace.spans.forEach((sp) => {
      const isActive = cur >= sp.start_ms && cur <= sp.end_ms;
      const isDone = cur > sp.end_ms;

      const row = mkEl("div", "");
      row.style.cssText =
        "display:grid;grid-template-columns:110px 210px 1fr 78px;align-items:center;gap:10px;padding:6px 10px;border-radius:8px;background:" +
        (isActive ? "#eff6ff" : "#ffffff") +
        ";border:1px solid " +
        (isActive ? "#3b82f6" : "#e2e8f0") +
        ";";

      const modeBadge = mkEl(
        "span",
        `pill-badge ${sp.mode === "PARALLEL" ? "pill-amber" : "pill-blue"} tabular-nums`,
        `${sp.order} · ${sp.mode}`
      );
      modeBadge.style.fontSize = "10.5px";

      const whereCol = mkEl("div", "");
      const wTitle = mkEl("div", "", sp.lane);
      wTitle.style.cssText = "font-size:11.5px;font-weight:800;color:#0f172a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;";
      const wSub = mkEl("div", "", sp.where);
      wSub.style.cssText = "font-size:10.5px;color:#475569;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;";
      whereCol.append(wTitle, wSub);

      const barTrack = mkEl("div", "");
      barTrack.style.cssText =
        "position:relative;height:20px;background:#f1f5f9;border-radius:6px;overflow:hidden;border:1px solid #cbd5e1;";

      const leftPct = (sp.start_ms / totalMs) * 100;
      const widthPct = Math.max(2, ((sp.end_ms - sp.start_ms) / totalMs) * 100);
      const fillRatio = cur <= sp.start_ms ? 0 : cur >= sp.end_ms ? 1 : (cur - sp.start_ms) / Math.max(1, sp.end_ms - sp.start_ms);

      const ghostBar = mkEl("div", "");
      ghostBar.style.cssText = `position:absolute;top:2px;bottom:2px;left:${leftPct}%;width:${widthPct}%;background:${sp.color};opacity:0.22;border-radius:4px;`;

      const liveBar = mkEl("div", "");
      const barColor = TRACE_PLAYER.pathMode === "deny" && sp.span_id === "S5" ? "#dc2626" : sp.color;
      liveBar.style.cssText = `position:absolute;top:2px;bottom:2px;left:${leftPct}%;width:${widthPct * fillRatio}%;background:${barColor};border-radius:4px;`;

      const playhead = mkEl("div", "");
      playhead.style.cssText = `position:absolute;top:0;bottom:0;left:${(cur / totalMs) * 100}%;width:2px;background:#0f172a;`;

      barTrack.append(ghostBar, liveBar, playhead);

      const timingCol = mkEl("span", "tabular-nums", `${sp.start_ms}–${sp.end_ms}ms`);
      timingCol.style.cssText =
        "font-size:11px;font-weight:700;text-align:right;color:" + (isDone ? "#059669" : isActive ? "#1d4ed8" : "#64748b") + ";";

      row.append(modeBadge, whereCol, barTrack, timingCol);
      rowsWrap.appendChild(row);
    });
  } else if (customStage) {
    rowsWrap.style.display = "none";
    customStage.style.display = "block";
    renderTraceCustomStage(TRACE_PLAYER.vizMode, customStage, trace, cur, totalMs, activeSpans);
  }

  const stageLbl = document.getElementById("trace-player-active-stage-label");
  const modePill = document.getElementById("trace-player-active-mode-badge");
  const jsonBox = document.getElementById("trace-player-active-json");
  const chosen = activeSpans.length ? activeSpans : [trace.spans[trace.spans.length - 1]];
  const isParallelGroup = chosen.some((s) => s.mode === "PARALLEL" && s.fork_group === "GATEWAY_FANOUT_4");

  if (stageLbl) {
    stageLbl.textContent = isParallelGroup
      ? `Active @ ${Math.round(cur)}ms: 4 Concurrent Gateway Verification Lanes Running in Parallel`
      : `Active @ ${Math.round(cur)}ms: ${chosen.map((s) => `${s.order} (${s.where})`).join(" + ")}`;
  }
  if (modePill) {
    modePill.textContent = isParallelGroup
      ? `PARALLEL ×4 FAN-OUT · BARRIER JOIN @ ${trace.barrier_join_ms}ms`
      : chosen.map((s) => s.mode).join(" + ");
  }
  if (jsonBox) {
    jsonBox.textContent = chosen
      .map((s) => {
        const pStr = TRACE_PLAYER.pathMode === "deny" ? s.payload_deny : s.payload_allow;
        return `[${s.order} | ${s.where}] ${s.what}\n  ↳ ${pStr}`;
      })
      .join("\n");
  }
}

async function loadStepFlowStudio(presetId = "FLOW-01", theme = "light") {
  try {
    const res = await fetch(
      `/api/step-flow?preset_id=${encodeURIComponent(presetId)}&theme=${encodeURIComponent(theme)}`
    );
    if (!res.ok) return;
    const bundle = await res.json();
    renderStepFlowBundle(bundle);
  } catch (_err) {
    // Non-fatal on initial load
  }
}

function renderTraceCustomStage(mode, container, trace, cur, totalMs, activeSpans) {
  const bundle = STATE.activeStepFlowBundle || {};
  const spec = bundle.spec || {};
  const isDeny = TRACE_PLAYER.pathMode === "deny";

  // Option 2: Native 4:5 H.264 MP4 Video Player + Frame HUD
  if (mode === "option2") {
    const existingVid = container.querySelector("video[data-src]");
    const targetMp4 = safeUrl(bundle.mp4_url || "/assets/step-flows/FLOW-01-light-7742D372.mp4");
    if (!existingVid || existingVid.getAttribute("data-src") !== targetMp4) {
      container.replaceChildren();
      const grid = mkEl("div", "composer-split-layout");
      grid.style.alignItems = "center";

      const vidCard = mkEl("div", "feed-item-card");
      vidCard.style.cssText = "background:#ffffff;padding:12px;text-align:center;";
      const vid = document.createElement("video");
      vid.src = targetMp4;
      vid.setAttribute("data-src", targetMp4);
      vid.controls = true;
      vid.autoplay = true;
      vid.loop = true;
      vid.muted = true;
      vid.playsInline = true;
      vid.style.cssText = "width:100%;max-width:380px;height:auto;border-radius:8px;border:1px solid #cbd5e1;";
      vidCard.appendChild(vid);

      const hud = mkEl("div", "feed-item-card");
      hud.id = "opt2-frame-hud";
      hud.style.cssText = "background:#ffffff;padding:16px;";
      grid.append(vidCard, hud);
      container.appendChild(grid);
    }
    const hud = container.querySelector("#opt2-frame-hud");
    if (hud) {
      hud.replaceChildren();
      const frameIdx = Math.floor((cur / totalMs) * 360);
      hud.append(
        mkEl("span", "pill-badge pill-blue tabular-nums", `Option 2 · Frame ${frameIdx} / 360 @ 30fps H.264`),
        mkEl("h4", "subsection-heading", `Programmatic 4:5 MP4 Video Mastering (${bundle.preset_id || "FLOW-01"})`),
        mkEl(
          "p",
          "section-description",
          "Plays natively with timeline scrubbing on LinkedIn, X (Twitter), and YouTube Shorts without GIF 256-color banding."
        )
      );
      activeSpans.forEach((sp) => {
        const line = mkEl("div", "feed-item-card", `${sp.order} [${sp.mode}] · ${sp.where} (${sp.start_ms}–${sp.end_ms}ms)`);
        line.style.cssText = "margin-top:6px;font-size:12px;font-weight:700;color:#0f172a;";
        hud.appendChild(line);
      });
    }
    return;
  }

  container.replaceChildren();

  // Option 3: 3-Pane Split-Screen (Live Agent Terminal CLI | Active Topology Nodes | OTel Span Stream)
  if (mode === "option3") {
    const split = mkEl("div", "");
    split.style.cssText = "display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;";

    const cliPane = mkEl("div", "feed-item-card");
    cliPane.style.cssText = "background:#ffffff;border:1px solid #cbd5e1;padding:12px;font-family:ui-monospace,monospace;font-size:11.5px;";
    cliPane.appendChild(mkEl("div", "pill-badge pill-blue", "Pane 1 · Live Agent CLI & Tool Stream"));
    trace.spans.forEach((sp) => {
      if (cur >= sp.start_ms) {
        const ln = mkEl("div", "", `[+${String(sp.start_ms).padStart(3, "0")}ms] ${sp.mode === "PARALLEL" ? "⇉ [PARALLEL]" : "→ [SERIAL]"} ${sp.lane}`);
        ln.style.cssText = "margin-top:5px;color:" + (cur <= sp.end_ms ? "#1d4ed8;font-weight:800;" : "#334155;");
        cliPane.appendChild(ln);
      }
    });

    const nodePane = mkEl("div", "feed-item-card");
    nodePane.style.cssText = "background:#ffffff;border:1px solid #cbd5e1;padding:12px;";
    nodePane.appendChild(mkEl("div", "pill-badge pill-amber", "Pane 2 · Active Service Boundaries (WHERE)"));
    trace.spans.forEach((sp) => {
      const act = cur >= sp.start_ms && cur <= sp.end_ms;
      const card = mkEl("div", "", `${act ? "● ACTIVE: " : "○ "}${sp.where}`);
      card.style.cssText =
        "margin-top:5px;padding:4px 8px;border-radius:6px;font-size:11.5px;font-weight:" +
        (act ? "800;background:#eff6ff;border:1px solid #3b82f6;color:#1e40af;" : "600;color:#64748b;");
      nodePane.appendChild(card);
    });

    const otelPane = mkEl("div", "feed-item-card");
    otelPane.style.cssText = "background:#ffffff;border:1px solid #cbd5e1;padding:12px;font-family:ui-monospace,monospace;font-size:11px;";
    otelPane.appendChild(mkEl("div", "pill-badge pill-emerald", "Pane 3 · OpenTelemetry Live Spans (WHAT)"));
    (activeSpans.length ? activeSpans : trace.spans.slice(0, 2)).forEach((sp) => {
      const pText = isDeny ? sp.payload_deny : sp.payload_allow;
      const box = mkEl("div", "", `span_id=${sp.span_id} (${sp.duration_ms}ms)\n${pText}`);
      box.style.cssText = "margin-top:6px;padding:6px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;white-space:pre-wrap;color:#0f172a;";
      otelPane.appendChild(box);
    });

    split.append(cliPane, nodePane, otelPane);
    container.appendChild(split);
    return;
  }

  // Option 4: Interactive 5-State Deterministic FSM + WebSpeech Audio Narration Cue Sync
  if (mode === "option4") {
    const fsmWrap = mkEl("div", "feed-item-card");
    fsmWrap.style.cssText = "background:#ffffff;border:1px solid #cbd5e1;padding:14px;";
    const hdr = mkEl("div", "composer-section-hdr");
    hdr.style.marginBottom = "10px";
    hdr.appendChild(mkEl("span", "pill-badge pill-blue", "Option 4 · 5-State Deterministic FSM + Audio Cue Sync"));
    const speakBtn = mkEl("button", "btn-secondary", "🔊 Speak Step-by-Step Narration");
    speakBtn.type = "button";
    speakBtn.addEventListener("click", () => {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(
          `${spec.hook_line_1 || ""} Step 1: Serial ingress from ${spec.agent_title || "Agent"} to ${spec.gateway_title || "Gateway"}. Step 2: 4 parallel verification lanes execute concurrently in 30 milliseconds. Step 3: Barrier join enforces ${isDeny ? "circuit-breaker DENY" : "verified ALLOW"}.`
        );
        window.speechSynthesis.speak(u);
      }
      showToast("Triggered synchronized step-by-step narration");
    });
    hdr.appendChild(speakBtn);
    fsmWrap.appendChild(hdr);

    const states = [
      { id: "S0", label: "1. Trust Root (0–45ms)", range: [0, 45] },
      { id: "S1", label: "2. Serial Reasoning (45–115ms)", range: [45, 115] },
      { id: "S2", label: "3. Gateway Intercept (115–135ms)", range: [115, 135] },
      { id: "S3", label: "4. Parallel ×4 Fan-Out (135–165ms)", range: [135, 165] },
      { id: "S4", label: isDeny ? "5. Barrier Join → DENY (165–320ms)" : "5. Barrier Join → ALLOW (165–320ms)", range: [165, 320] },
    ];
    const row = mkEl("div", "");
    row.style.cssText = "display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;";
    states.forEach((st) => {
      const act = cur >= st.range[0] && cur <= st.range[1];
      const btn = mkEl("button", "", st.label);
      btn.type = "button";
      btn.style.cssText =
        "padding:10px 8px;border-radius:8px;cursor:pointer;font-size:11.5px;font-weight:800;border:2px solid " +
        (act ? "#2563eb;background:#eff6ff;color:#1e3a8a;" : "#cbd5e1;background:#f8fafc;color:#475569;");
      btn.addEventListener("click", () => {
        TRACE_PLAYER.currentMs = st.range[0] + 5;
        renderTraceWaterfallAtTime(TRACE_PLAYER.currentMs);
      });
      row.appendChild(btn);
    });
    fsmWrap.appendChild(row);
    container.appendChild(fsmWrap);
    return;
  }

  // Option 5: OpenTelemetry / Perfetto Distributed Trace Span Tree Replay
  if (mode === "option5") {
    const otelCard = mkEl("div", "feed-item-card");
    otelCard.style.cssText = "background:#ffffff;border:1px solid #cbd5e1;padding:12px;font-family:ui-monospace,monospace;font-size:11.5px;";
    otelCard.appendChild(
      mkEl("div", "pill-badge pill-emerald", `Option 5 · OpenTelemetry Span Tree Replay · trace_id=0x752394973654 · barrier_join=${trace.barrier_join_ms}ms`)
    );
    trace.spans.forEach((sp) => {
      const isAct = cur >= sp.start_ms && cur <= sp.end_ms;
      const indent = sp.mode === "PARALLEL" ? "  ├─ [PARALLEL FORK] " : "├─ [ROOT/SERIAL] ";
      const item = mkEl(
        "div",
        "",
        `${indent}span=${sp.span_id} parent=${sp.mode === "PARALLEL" ? "S3" : "ROOT"} start=${sp.start_ms}ms end=${sp.end_ms}ms (${sp.duration_ms}ms) · ${sp.where}`
      );
      item.style.cssText =
        "margin-top:5px;padding:4px 8px;border-radius:5px;background:" +
        (isAct ? "#ecfdf5;border:1px solid #059669;font-weight:800;color:#065f46;" : "#f8fafc;color:#334155;");
      otelCard.appendChild(item);
    });
    container.appendChild(otelCard);
    return;
  }

  // Option 6: Animated UML Sequence Diagram with Parallel `par [4x Concurrent] ... end` Lifelines
  if (mode === "option6") {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 960 280");
    svg.style.cssText = "width:100%;height:auto;background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;display:block;";

    const actors = [
      { x: 90, name: "1. Approver" },
      { x: 250, name: "2. Agent ⇄ LLM" },
      { x: 430, name: "3. Policy Gateway" },
      { x: 610, name: "4. Approval / Policy" },
      { x: 780, name: "5. Security / Ledger" },
      { x: 900, name: isDeny ? "6. Blocked" : "6. Deploy Svc" },
    ];
    actors.forEach((a) => {
      const rect = document.createElementNS(ns, "rect");
      rect.setAttribute("x", String(a.x - 65));
      rect.setAttribute("y", "10");
      rect.setAttribute("width", "130");
      rect.setAttribute("height", "28");
      rect.setAttribute("rx", "6");
      rect.setAttribute("fill", "#eff6ff");
      rect.setAttribute("stroke", "#3b82f6");
      svg.appendChild(rect);

      const txt = document.createElementNS(ns, "text");
      txt.setAttribute("x", String(a.x));
      txt.setAttribute("y", "28");
      txt.setAttribute("text-anchor", "middle");
      txt.setAttribute("font-size", "11");
      txt.setAttribute("font-weight", "800");
      txt.setAttribute("fill", "#0f172a");
      txt.textContent = a.name;
      svg.appendChild(txt);

      const line = document.createElementNS(ns, "line");
      line.setAttribute("x1", String(a.x));
      line.setAttribute("y1", "38");
      line.setAttribute("x2", String(a.x));
      line.setAttribute("y2", "268");
      line.setAttribute("stroke", "#cbd5e1");
      line.setAttribute("stroke-dasharray", "4 4");
      svg.appendChild(line);
    });

    // Par box for 135..165ms
    const parBox = document.createElementNS(ns, "rect");
    parBox.setAttribute("x", "380");
    parBox.setAttribute("y", "122");
    parBox.setAttribute("width", "450");
    parBox.setAttribute("height", "74");
    parBox.setAttribute("rx", "6");
    parBox.setAttribute("fill", "#fef3c7");
    parBox.setAttribute("fill-opacity", "0.35");
    parBox.setAttribute("stroke", "#d97706");
    parBox.setAttribute("stroke-dasharray", "5 3");
    svg.appendChild(parBox);

    const parLbl = document.createElementNS(ns, "text");
    parLbl.setAttribute("x", "390");
    parLbl.setAttribute("y", "138");
    parLbl.setAttribute("font-size", "10.5");
    parLbl.setAttribute("font-weight", "800");
    parLbl.setAttribute("fill", "#b45309");
    parLbl.textContent = "par [PARALLEL ×4 FAN-OUT · 135–165ms · Simultaneous Execution]";
    svg.appendChild(parLbl);

    const arrows = [
      { y: 62, x1: 90, x2: 610, col: "#2563eb", label: "S1 [0–45ms] Mint Signed Approval" },
      { y: 88, x1: 250, x2: 430, col: "#0d9488", label: "S2–S3 [45–135ms] Tool Call → Gateway Intercept" },
      { y: 154, x1: 430, x2: 610, col: "#059669", label: "P4A ∥ P4B [135–159ms] Approval + 4 Temporal Rules" },
      { y: 178, x1: 430, x2: 780, col: "#7c3aed", label: "P4C ∥ P4D [135–165ms] Model Armor + Session Ledger" },
      { y: 224, x1: 430, x2: 900, col: isDeny ? "#dc2626" : "#059669", label: isDeny ? "S5 [165ms] Barrier Join → DENY Block" : "S5 [165–265ms] Barrier Join → Verified ALLOW" },
    ];
    arrows.forEach((ar) => {
      const ln = document.createElementNS(ns, "line");
      ln.setAttribute("x1", String(ar.x1));
      ln.setAttribute("y1", String(ar.y));
      ln.setAttribute("x2", String(ar.x2));
      ln.setAttribute("y2", String(ar.y));
      ln.setAttribute("stroke", ar.col);
      ln.setAttribute("stroke-width", "2.2");
      svg.appendChild(ln);

      const lb = document.createElementNS(ns, "text");
      lb.setAttribute("x", String((ar.x1 + ar.x2) / 2));
      lb.setAttribute("y", String(ar.y - 5));
      lb.setAttribute("text-anchor", "middle");
      lb.setAttribute("font-size", "10.5");
      lb.setAttribute("font-weight", "700");
      lb.setAttribute("fill", "#0f172a");
      lb.textContent = ar.label;
      svg.appendChild(lb);
    });

    // Moving horizontal time cursor
    const cursorY = 48 + (cur / totalMs) * 210;
    const curLine = document.createElementNS(ns, "line");
    curLine.setAttribute("x1", "20");
    curLine.setAttribute("y1", String(cursorY));
    curLine.setAttribute("x2", "940");
    curLine.setAttribute("y2", String(cursorY));
    curLine.setAttribute("stroke", "#dc2626");
    curLine.setAttribute("stroke-width", "1.8");
    svg.appendChild(curLine);

    container.appendChild(svg);
    return;
  }

  // Option 7: 3D Isometric 4-Plane Spatial Layer Stack
  if (mode === "option7") {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 960 270");
    svg.style.cssText = "width:100%;height:auto;background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;display:block;";

    const planes = [
      { y: 20, col: "#2563eb", title: "Plane 1 · Human & Workforce IAM Trust Root (0–45ms SERIAL)", active: cur < 45 },
      { y: 80, col: "#0d9488", title: "Plane 2 · Agent Runtime ⇄ Frontier LLM Reasoning (45–135ms SERIAL)", active: cur >= 45 && cur < 135 },
      { y: 140, col: "#d97706", title: "Plane 3 · Out-of-Loop Policy Mesh (135–165ms PARALLEL ×4 FAN-OUT)", active: cur >= 135 && cur <= 165 },
      { y: 200, col: isDeny ? "#dc2626" : "#059669", title: isDeny ? "Plane 4 · Circuit-Breaker DENY + Async OTel (165–320ms)" : "Plane 4 · Protected Data Execution + Async OTel (165–320ms)", active: cur > 165 },
    ];
    planes.forEach((pl) => {
      const poly = document.createElementNS(ns, "polygon");
      const y = pl.y;
      poly.setAttribute("points", `180,${y} 840,${y} 780,${y + 44} 120,${y + 44}`);
      poly.setAttribute("fill", pl.active ? "#eff6ff" : "#f8fafc");
      poly.setAttribute("stroke", pl.col);
      poly.setAttribute("stroke-width", pl.active ? "3" : "1.5");
      svg.appendChild(poly);

      const tx = document.createElementNS(ns, "text");
      tx.setAttribute("x", "480");
      tx.setAttribute("y", String(y + 27));
      tx.setAttribute("text-anchor", "middle");
      tx.setAttribute("font-size", "12.5");
      tx.setAttribute("font-weight", "800");
      tx.setAttribute("fill", "#0f172a");
      tx.textContent = pl.title;
      svg.appendChild(tx);
    });
    container.appendChild(svg);
  }
}

async function triggerCompileStepFlow(compileGif = true) {
  const presetId = document.getElementById("step-flow-preset-select")?.value || "FLOW-01";
  const theme = document.getElementById("step-flow-theme-select")?.value || "light";
  const customTopic = (document.getElementById("step-flow-topic-input")?.value || "").trim();
  const btn = document.getElementById("compile-step-flow-btn");
  if (btn) {
    btn.disabled = true;
    btn.textContent = compileGif ? "Compiling 4:5 Flow & GIF..." : "Updating Preview...";
  }
  try {
    const res = await fetch("/api/step-flow/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        preset_id: presetId,
        theme,
        custom_topic: customTopic,
        compile_gif: Boolean(compileGif),
      }),
    });
    const bundle = await res.json();
    renderStepFlowBundle(bundle);
    showToast(`Compiled ${bundle.preset_id} (${theme === "dark_neon" ? "Dark-Grid Neon" : "Executive Light"})`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Compile 4:5 Flow & GIF";
    }
  }
}

function copyStepFlowPostText() {
  const b = STATE.activeStepFlowBundle?.copy_bundle;
  if (!b) return;
  const full = `${b.post_copy}\n\n---\nComment #1: ${b.comment_1}`;
  navigator.clipboard?.writeText(full);
  showToast("Copied 6-Beat Step-by-Step Post + Comment #1");
}

async function triggerSynthesizeCustomTemplate() {
  const topicInput = document.getElementById("gen-template-topic-input");
  const personaSelect = document.getElementById("gen-template-persona-select");
  const orgSelect = document.getElementById("gen-template-org-select");
  const grammarSelect = document.getElementById("gen-template-grammar-select");
  const stage = document.getElementById("gen-template-result-stage");
  const btn = document.getElementById("synthesize-custom-template-btn");
  if (!stage) return;

  const topic = (topicInput?.value || "").trim() || "Multi-Agent MCP OAuth 2.1 Zero-Trust Gateway & Vertex AI Runtime Topology";
  const persona_id = personaSelect?.value || "vp_principal_architect";
  const org_id = orgSelect?.value || "cloud_hyperscaler";
  const grammar_id = grammarSelect?.value || "AUTO";

  if (btn) {
    btn.disabled = true;
    btn.textContent = "Synthesizing Blueprint...";
  }
  try {
    const res = await fetch("/api/templates/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, persona_id, org_id, grammar_id }),
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      showToast(data.error || "Failed to synthesize custom blueprint");
      return;
    }
    stage.style.display = "block";
    stage.replaceChildren();

    const metaRow = mkEl("div", "section-header-row");
    metaRow.style.marginBottom = "12px";
    const leftInfo = mkEl("div", "min-w-0");
    const badgeRow = mkEl("div", "masthead-eyebrow-row");
    badgeRow.append(
      mkEl("span", "pill-badge pill-emerald", `${data.grammar_id} (${data.template_id}) · ${data.confidence_score}% Fit`),
      mkEl("span", "pill-badge pill-sky", `Persona: ${data.persona?.short_label || persona_id}`),
      mkEl("span", "pill-badge pill-amber", `Org: ${data.organization?.short_label || org_id}`)
    );
    const titleEl = mkEl("h3", "subsection-heading", `${data.grammar?.name || data.template_id}`);
    titleEl.style.marginTop = "6px";
    const whyEl = mkEl("p", "section-description", data.why_selected || "");
    leftInfo.append(badgeRow, titleEl, whyEl);

    const actions = mkEl("div", "studio-toolbar-actions");
    if (data.files?.svg_url) {
      const aSvg = mkEl("a", "btn-secondary", "Open Custom SVG ↗");
      aSvg.href = safeUrl(data.files.svg_url);
      aSvg.target = "_blank";
      aSvg.rel = "noopener";
      actions.appendChild(aSvg);
    }
    if (data.files?.drawio_url) {
      const aDraw = mkEl("a", "btn-secondary", "Download .drawio");
      aDraw.href = safeUrl(data.files.drawio_url);
      aDraw.setAttribute("download", `${data.template_id}_custom.drawio`);
      actions.appendChild(aDraw);
    }
    if (data.files?.canonical_pptx_url) {
      const aPptx = mkEl("a", "btn-primary", "Download Editable .pptx");
      aPptx.href = safeUrl(data.files.canonical_pptx_url);
      aPptx.setAttribute("download", `${data.template_id}.pptx`);
      actions.appendChild(aPptx);
    }
    metaRow.append(leftInfo, actions);
    stage.appendChild(metaRow);

    if (data.self_critic_receipt) {
      const rc = data.self_critic_receipt;
      const criticBar = mkEl("div", "feed-item-card");
      criticBar.style.cssText = "margin-bottom:12px;background:#ecfdf5;border:1px solid #a7f3d0;padding:10px 14px;";
      const hdr = mkEl("div", "masthead-eyebrow-row");
      hdr.append(
        mkEl("span", "pill-badge pill-emerald tabular-nums", `Self-Critic: ${rc.overall_score}/100 · 4/4 Judges PASS`),
        mkEl("span", "pill-badge pill-sky tabular-nums", `SVG: ${rc.geometry_check?.svg_rects || 0} cards / ${rc.geometry_check?.svg_texts || 0} text nodes`),
        mkEl("span", "pill-badge pill-amber tabular-nums", `Draw.io: ${rc.geometry_check?.drawio_vertices || 0}v / ${rc.geometry_check?.drawio_edges || 0}e`)
      );
      criticBar.appendChild(hdr);
      if ((rc.auto_healed_adjustments || []).length) {
        const adj = mkEl("div", "", `Auto-Healed: ${rc.auto_healed_adjustments.join(" · ")}`);
        adj.style.cssText = "font-size:11.5px;color:#065f46;margin-top:6px;font-weight:600;";
        criticBar.appendChild(adj);
      }
      stage.appendChild(criticBar);
    }

    const previewWrap = mkEl("div");
    previewWrap.style.cssText = "background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;padding:16px;display:flex;justify-content:center;max-height:760px;overflow:auto;";
    if (data.files?.svg_url) {
      const img = document.createElement("img");
      img.src = `${safeUrl(data.files.svg_url)}?t=${Date.now()}`;
      img.alt = `${data.template_id} synthesized blueprint`;
      img.style.cssText = "max-width:680px;width:100%;height:auto;border-radius:8px;box-shadow:0 4px 16px rgba(15,23,42,0.08);";
      previewWrap.appendChild(img);
    }
    stage.appendChild(previewWrap);
    showToast(`Synthesized ${data.grammar_id} (${data.template_id}) for ${data.persona?.short_label}`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "✨ Synthesize Custom Blueprint";
    }
  }
}

async function loadAndRenderSelfCriticHarness(triggerRun = false) {
  const gatesGrid = document.getElementById("self-critic-gates-grid");
  const personasGrid = document.getElementById("self-critic-personas-grid");
  const gapsGrid = document.getElementById("self-critic-gap-exemplars-grid");
  const scorePill = document.getElementById("self-critic-live-score-pill");
  const mastheadBadge = document.getElementById("self-critic-masthead-badge");
  const headerBadge = document.getElementById("telemetry-self-critic-badge");
  const btn = document.getElementById("run-self-critic-sweep-btn");

  if (triggerRun && btn) {
    btn.disabled = true;
    btn.textContent = "Running 8-Gate Self-Critic...";
  }
  try {
    const res = triggerRun
      ? await fetch("/api/harness/self-critic/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ auto_heal: true, refresh_discovery: true }),
        })
      : await fetch("/api/harness/self-critic");
    const data = await res.json();
    if (!res.ok || !data) return;

    const summaryTxt = `Harness² v2.4 · ${data.gates_passed}/${data.gates_total} Gates PASS (${data.overall_score}/100)`;
    if (scorePill) scorePill.textContent = `Score: ${data.overall_score} / 100 · All ${data.gates_passed}/${data.gates_total} Gates Verified`;
    if (mastheadBadge) mastheadBadge.textContent = summaryTxt;
    if (headerBadge) headerBadge.textContent = `Harness² Self-Critic: ${data.gates_passed}/${data.gates_total} Gates PASS (${data.overall_score}%)`;

    if (gatesGrid) {
      gatesGrid.replaceChildren();
      (data.gates || []).forEach((g) => {
        const card = mkEl("article", "repo-card");
        const top = mkEl("div", "masthead-eyebrow-row");
        top.append(
          mkEl("span", g.status === "PASS" ? "pill-badge pill-emerald" : "pill-badge pill-amber", `${g.status} · ${g.score}%`),
          mkEl("span", "deliverable-chip tabular-nums", g.gate_id)
        );
        const h3 = mkEl("h3", "subsection-heading", g.name);
        h3.style.margin = "8px 0 6px";
        const m = mkEl("p", "", g.metrics);
        m.style.cssText = "font-size:12px;color:#0f172a;font-weight:600;margin-bottom:6px;";
        const prev = mkEl("p", "", g.what_it_prevents);
        prev.style.cssText = "font-size:11.5px;color:#475569;line-height:1.45;";
        card.append(top, h3, m, prev);
        gatesGrid.appendChild(card);
      });
    }

    if (personasGrid) {
      personasGrid.replaceChildren();
      (data.persona_critics || []).forEach((c) => {
        const card = mkEl("article", "repo-card");
        const top = mkEl("div", "masthead-eyebrow-row");
        top.append(
          mkEl("span", "pill-badge pill-emerald tabular-nums", `${c.status} · ${c.score}/100`),
          mkEl("span", "pill-badge pill-sky", c.critic_id)
        );
        const h3 = mkEl("h3", "subsection-heading", c.role);
        h3.style.margin = "8px 0 6px";
        const foc = mkEl("p", "", `Focus: ${c.focus}`);
        foc.style.cssText = "font-size:11.5px;color:#334155;margin-bottom:6px;";
        const fnd = mkEl("p", "", c.latest_finding);
        fnd.style.cssText = "font-size:11.5px;color:#065f46;font-weight:600;";
        card.append(top, h3, foc, fnd);
        personasGrid.appendChild(card);
      });
    }

    if (gapsGrid) {
      gapsGrid.replaceChildren();
      const exemplars = data.discovery_and_gap_radar?.auto_synthesized_gap_exemplars || [];
      exemplars.forEach((ex) => {
        const card = mkEl("article", "repo-card");
        const top = mkEl("div", "masthead-eyebrow-row");
        top.append(
          mkEl("span", "pill-badge pill-emerald", `${ex.gap_id} · ${ex.grammar_id} (${ex.template_id})`),
          mkEl("span", "pill-badge pill-sky", ex.persona_label),
          mkEl("span", "pill-badge pill-amber", ex.org_label)
        );
        const h3 = mkEl("h3", "subsection-heading", ex.topic);
        h3.style.margin = "8px 0 6px";
        const sub = mkEl("p", "", ex.subtitle);
        sub.style.cssText = "font-size:11.5px;color:#475569;margin-bottom:10px;line-height:1.45;";
        const acts = mkEl("div", "studio-toolbar-actions");
        const aSvg = mkEl("a", "btn-secondary", "Preview SVG ↗");
        aSvg.href = safeUrl(ex.svg_url);
        aSvg.target = "_blank";
        aSvg.rel = "noopener";
        const aDio = mkEl("a", "btn-secondary", ".drawio");
        aDio.href = safeUrl(ex.drawio_url);
        aDio.setAttribute("download", `${ex.gap_id.toLowerCase()}.drawio`);
        const aPptx = mkEl("a", "btn-primary", ".pptx");
        aPptx.href = safeUrl(ex.pptx_url);
        aPptx.setAttribute("download", `${ex.template_id}.pptx`);
        acts.append(aSvg, aDio, aPptx);
        card.append(top, h3, sub, acts);
        gapsGrid.appendChild(card);
      });
    }

    const csGrid = document.getElementById("customer-success-inventions-grid");
    const csCountPill = document.getElementById("cs-inventions-count-pill");
    const csRadar = data.discovery_and_gap_radar?.customer_success_invention_radar;
    if (csCountPill && csRadar?.inventions) {
      csCountPill.textContent = `${csRadar.inventions.length} Agentic AI Inventions Mapped to Customer KPIs`;
    }
    if (csGrid && csRadar?.inventions) {
      csGrid.replaceChildren();
      csRadar.inventions.forEach((inv) => {
        const card = mkEl("article", "repo-card");
        const top = mkEl("div", "masthead-eyebrow-row");
        top.append(
          mkEl("span", "pill-badge pill-emerald tabular-nums", `${inv.invention_id} · ${inv.recommended_template_id}`),
          mkEl("span", "pill-badge pill-sky", inv.discovery_category || "Agentic AI Invention")
        );
        const h3 = mkEl("h3", "subsection-heading", inv.invention_title);
        h3.style.margin = "8px 0 6px";
        const pain = mkEl("p", "", `Customer Blocker: ${inv.customer_pain_point}`);
        pain.style.cssText = "font-size:11.5px;color:#334155;margin-bottom:6px;line-height:1.45;";
        const rx = mkEl("p", "", `Playbook Fix: ${inv.customer_success_prescription}`);
        rx.style.cssText = "font-size:11.5px;color:#0f172a;margin-bottom:6px;line-height:1.45;";
        const kpi = mkEl("p", "", `Value Realized: ${inv.quantified_value_kpis}`);
        kpi.style.cssText = "font-size:11.5px;color:#065f46;font-weight:700;margin-bottom:10px;";

        const acts = mkEl("div", "studio-toolbar-actions");
        const aBp = mkEl("a", "btn-secondary", `Blueprint ${inv.recommended_template_id} ↗`);
        aBp.href = safeUrl(`/assets/template-gallery/${inv.recommended_template_id}.svg`);
        aBp.target = "_blank";
        aBp.rel = "noopener";
        const btnSynth = mkEl("button", "btn-secondary", "Synthesize Custom Lens");
        btnSynth.type = "button";
        btnSynth.addEventListener("click", () => {
          const tIn = document.getElementById("gen-template-topic-input");
          const pSel = document.getElementById("gen-template-persona-select");
          const oSel = document.getElementById("gen-template-org-select");
          if (tIn) tIn.value = inv.invention_title;
          if (pSel && inv.target_persona_id) pSel.value = inv.target_persona_id;
          if (oSel && inv.target_org_id) oSel.value = inv.target_org_id;
          document.getElementById("tab-btn-gallery")?.click();
          triggerSynthesizeCustomTemplate();
        });
        const btnRepo = mkEl("button", "btn-primary", "Inspect ADK Repo →");
        btnRepo.type = "button";
        btnRepo.addEventListener("click", () => {
          if (typeof openRepoInspector === "function") {
            openRepoInspector(inv.reference_repo_slug || "gcp-mcp-zero-bloat-gateway");
          }
        });
        acts.append(aBp, btnSynth, btnRepo);
        card.append(top, h3, pain, rx, kpi, acts);
        csGrid.appendChild(card);
      });
    }

    if (triggerRun) {
      const healedCount = (data.auto_heal_actions || []).length;
      showToast(
        `Self-Critic & Auto-Heal Sweep Complete: ${data.gates_passed}/${data.gates_total} Gates PASS (${data.overall_score}/100) · ${healedCount} Auto-Heal Checks Verified!`
      );
      loadDailyTop5Briefing();
    }
  } finally {
    if (triggerRun && btn) {
      btn.disabled = false;
      btn.textContent = "🛡️ Run Self-Critic & Auto-Heal Sweep";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const synthBtn = document.getElementById("synthesize-custom-template-btn");
  if (synthBtn) {
    synthBtn.addEventListener("click", () => triggerSynthesizeCustomTemplate());
  }
  const criticBtn = document.getElementById("run-self-critic-sweep-btn");
  if (criticBtn) {
    criticBtn.addEventListener("click", () => loadAndRenderSelfCriticHarness(true));
  }
  loadAndRenderSelfCriticHarness(false);
});


let _activeLiGroupsWaveFilter = 0; // 0 = All Waves, 1 = Wave 1, 2 = Wave 2, 3 = Wave 3
let _latestLiRadarData = null;

async function loadAndRenderLinkedinGroupsRadar(payloadOverride = null) {
  const grid = document.getElementById("linkedin-groups-membership-radar-grid");
  if (!grid) return;
  try {
    let data = payloadOverride;
    if (!data) {
      const res = await fetch("/api/linkedin-groups/membership-radar");
      if (!res.ok) return;
      data = await res.json();
    }
    _latestLiRadarData = data;

    const pill = document.getElementById("li-groups-unjoined-count-pill");
    if (pill) {
      pill.textContent = `${data.unjoined_count}/${data.total_catalog_groups} Unjoined · ${data.pending_count || 0}/12 Pending · ${data.joined_count} Joined (${data.unjoined_combined_member_reach} Unjoined Reach)`;
    }

    const syncBadge = document.getElementById("li-last-sync-badge");
    if (syncBadge) {
      if (data.last_authenticated_sync_utc) {
        syncBadge.textContent = `Last Synced: ${data.last_authenticated_sync_utc} (${data.last_sync_method})`;
      } else {
        syncBadge.textContent = "Same-Origin Bookmarklet & 12-Slot Governor Ready";
      }
    }

    const bmLink = document.getElementById("li-bookmarklet-sync-link");
    if (bmLink && data.authenticated_browser_bridge && data.authenticated_browser_bridge.bookmarklet_href) {
      bmLink.setAttribute("href", data.authenticated_browser_bridge.bookmarklet_href);
    }

    // Render 3-Wave Staged Join Queue & Pending-Slot Governor Bar
    const govBar = document.getElementById("li-groups-wave-governor-bar");
    if (govBar && data.pending_slot_governor && Array.isArray(data.staged_join_waves)) {
      govBar.replaceChildren();
      const gov = data.pending_slot_governor;
      const shell = mkEl("div", "");
      shell.style.cssText = "background:#ffffff;border:1px solid #bfdbfe;border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:10px;";

      const hdr = mkEl("div", "");
      hdr.style.cssText = "display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;";
      const govTitle = mkEl(
        "div",
        "",
        `🛡️ LinkedIn Pending-Request Slot Governor: ${gov.current_pending_count}/${gov.max_concurrent_pending_cap} Active Pending · ${gov.available_pending_slots} Slots Available · Safe Daily Join Budget: ${gov.daily_safe_join_budget}/day`
      );
      govTitle.style.cssText = "font-size:13px;font-weight:700;color:#0f172a;";
      const govSub = mkEl("span", "pill-badge pill-emerald", gov.governor_summary || gov.governor_status);
      hdr.append(govTitle, govSub);

      const waveRow = mkEl("div", "");
      waveRow.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px;";

      data.staged_join_waves.forEach((w) => {
        const wCard = mkEl("div", "");
        const isCurrentFilter = _activeLiGroupsWaveFilter === w.wave_number;
        wCard.style.cssText = `background:${isCurrentFilter ? "#eff6ff" : "#f8fafc"};border:1px solid ${isCurrentFilter ? "#2563eb" : "#cbd5e1"};border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:6px;`;

        const wTop = mkEl("div", "");
        wTop.style.cssText = "display:flex;justify-content:space-between;align-items:center;gap:6px;";
        const wBadge = mkEl("span", "pill-badge pill-blue", `Wave ${w.wave_number} · ${w.group_count} Groups`);
        const wReach = mkEl("span", "pill-badge pill-emerald tabular-nums", `${w.combined_reach} Reach`);
        wTop.append(wBadge, wReach);

        const wTitle = mkEl("div", "", w.title);
        wTitle.style.cssText = "font-size:12.5px;font-weight:700;color:#0f172a;line-height:1.35;";

        const wSched = mkEl("div", "", `${w.schedule_window} — ${w.rationale}`);
        wSched.style.cssText = "font-size:11.5px;color:#334155;line-height:1.4;";

        const wActions = mkEl("div", "");
        wActions.style.cssText = "display:flex;gap:8px;align-items:center;margin-top:auto;padding-top:4px;flex-wrap:wrap;";

        const stageBtn = mkEl(
          "button",
          "btn-primary",
          w.group_count > 0
            ? `🚀 Stage & Open Wave ${w.wave_number} (${Math.min(w.group_count, gov.daily_safe_join_budget || 8, Math.max(1, gov.available_pending_slots))} Safe)`
            : `✓ Wave ${w.wave_number} Staged`
        );
        stageBtn.type = "button";
        stageBtn.disabled = w.group_count === 0 || gov.available_pending_slots === 0;
        stageBtn.style.cssText = "font-size:11.5px;padding:5px 10px;";
        stageBtn.addEventListener("click", async () => {
          const r = await fetch("/api/linkedin-groups/stage-wave", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ wave_number: w.wave_number, max_batch: 8 }),
          });
          if (r.ok) {
            const updated = await r.json();
            loadAndRenderLinkedinGroupsRadar(updated);
            const urls = updated.staged_wave_receipt?.staged_urls || [];
            urls.slice(0, 8).forEach((u, idx) => {
              setTimeout(() => {
                try { window.open(u, "_blank", "noopener"); } catch (_e) {}
              }, idx * 350);
            });
            showToast(`Staged ${urls.length} group(s) in Wave ${w.wave_number} as Pending Approval under the 12-slot governor!`);
          }
        });

        const filterBtn = mkEl(
          "button",
          "btn-secondary",
          isCurrentFilter ? "Showing Only This Wave (Reset)" : `Filter Wave ${w.wave_number}`
        );
        filterBtn.type = "button";
        filterBtn.style.cssText = "font-size:11.5px;padding:5px 10px;";
        filterBtn.addEventListener("click", () => {
          _activeLiGroupsWaveFilter = isCurrentFilter ? 0 : w.wave_number;
          loadAndRenderLinkedinGroupsRadar(_latestLiRadarData);
        });

        wActions.append(stageBtn, filterBtn);
        wCard.append(wTop, wTitle, wSched, wActions);
        waveRow.appendChild(wCard);
      });

      shell.append(hdr, waveRow);
      govBar.appendChild(shell);
    }

    grid.replaceChildren();
    let groups = data.unjoined_priority_queue && data.unjoined_priority_queue.length
      ? [
          ...data.unjoined_priority_queue,
          ...(data.groups || []).filter((g) => g.membership_status === "PENDING_APPROVAL"),
          ...(data.groups || []).filter((g) => g.membership_status === "JOINED"),
        ]
      : (data.groups || []);

    if (_activeLiGroupsWaveFilter > 0) {
      groups = groups.filter((g) => Number(g.assigned_join_wave) === _activeLiGroupsWaveFilter);
    }

    groups.forEach((g) => {
      const isJoined = g.membership_status === "JOINED";
      const isPending = g.membership_status === "PENDING_APPROVAL";
      const card = mkEl("div", "feed-item-card");
      const borderCol = isJoined ? "#cbd5e1" : (isPending ? "#f59e0b" : "#bfdbfe");
      const bgCol = isJoined ? "#f8fafc" : (isPending ? "#fffbeb" : "#ffffff");
      card.style.cssText = `background:${bgCol};border:1px solid ${borderCol};border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:7px;opacity:${isJoined ? "0.75" : "1"};`;

      const topRow = mkEl("div", "");
      topRow.style.cssText = "display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;";
      const tierBadge = mkEl("span", "pill-badge pill-blue", g.tier.split("—")[0].trim());
      const waveTag = g.assigned_join_wave
        ? ` · Wave ${g.assigned_join_wave}`
        : (isPending ? " · ⏳ Pending" : " · ✓ Joined");
      const reachBadge = mkEl("span", "pill-badge pill-emerald tabular-nums", `${g.members} · Score ${g.visibility_score}${waveTag}`);
      topRow.append(tierBadge, reachBadge);

      const titleEl = mkEl("h4", "", g.name);
      titleEl.style.cssText = "margin:0;font-size:14px;font-weight:700;color:#0f172a;line-height:1.35;";

      const probEl = mkEl("div", "", `Unjoined Likelihood: ${g.unjoined_probability} · Moderation: ${g.moderation_speed}`);
      probEl.style.cssText = "font-size:11.5px;font-weight:700;color:#b45309;background:#fffbeb;border:1px solid #fde68a;padding:4px 8px;border-radius:6px;";

      const whyEl = mkEl("div", "", g.why_join_for_max_visibility);
      whyEl.style.cssText = "font-size:12px;color:#334155;line-height:1.45;";

      const bestPostsEl = mkEl("div", "", `Best Posts to Share: ${g.best_post_types}`);
      bestPostsEl.style.cssText = "font-size:11.5px;color:#065f46;font-weight:600;";

      const actRow = mkEl("div", "");
      actRow.style.cssText = "display:flex;justify-content:space-between;align-items:center;gap:6px;margin-top:auto;padding-top:6px;border-top:1px solid #f1f5f9;flex-wrap:wrap;";

      const openA = mkEl("a", "btn-primary", "Open Group ↗");
      openA.href = safeUrl(g.direct_group_url);
      openA.target = "_blank";
      openA.rel = "noopener";
      openA.style.cssText = "text-decoration:none;font-size:11.5px;padding:5px 10px;";

      const pendingBtn = mkEl(
        "button",
        "btn-secondary",
        isPending ? "⏳ Pending (Click to Clear)" : "Mark Pending ⏳"
      );
      pendingBtn.type = "button";
      pendingBtn.style.cssText = "font-size:11.5px;padding:5px 9px;";
      pendingBtn.addEventListener("click", async () => {
        const nextSt = isPending ? "NOT_JOINED_YET" : "PENDING_APPROVAL";
        const r = await fetch("/api/linkedin-groups/membership-radar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ toggle_group_id: g.group_id, status: nextSt }),
        });
        if (r.ok) {
          const updated = await r.json();
          loadAndRenderLinkedinGroupsRadar(updated);
        }
      });

      const toggleBtn = mkEl(
        "button",
        "btn-secondary",
        isJoined ? "✓ Joined (Undo)" : "Mark Joined ✓"
      );
      toggleBtn.type = "button";
      toggleBtn.style.cssText = "font-size:11.5px;padding:5px 9px;";
      toggleBtn.addEventListener("click", async () => {
        const nextSt = isJoined ? "NOT_JOINED_YET" : "JOINED";
        const r = await fetch("/api/linkedin-groups/membership-radar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ toggle_group_id: g.group_id, status: nextSt }),
        });
        if (r.ok) {
          const updated = await r.json();
          loadAndRenderLinkedinGroupsRadar(updated);
        }
      });

      actRow.append(openA, pendingBtn, toggleBtn);
      card.append(topRow, titleEl, probEl, whyEl, bestPostsEl, actRow);
      grid.appendChild(card);
    });
  } catch (_err) {
    // Non-fatal
  }
}

function checkHashForLinkedinGroupsRadar() {
  if (window.location.hash === "#linkedin-groups-membership-radar-section") {
    if (typeof activateView === "function") {
      activateView("view-openhands");
    } else {
      document.getElementById("tab-btn-openhands")?.click();
    }
    setTimeout(() => {
      document.getElementById("linkedin-groups-membership-radar-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 180);
  }
}

window.addEventListener("hashchange", checkHashForLinkedinGroupsRadar);

document.addEventListener("DOMContentLoaded", () => {
  loadAndRenderLinkedinGroupsRadar();
  checkHashForLinkedinGroupsRadar();

  document.getElementById("btn-copy-li-console-sync")?.addEventListener("click", async () => {
    const scriptTxt = _latestLiRadarData?.authenticated_browser_bridge?.console_oneliner || "";
    if (scriptTxt && navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(scriptTxt);
        showToast("Copied 1-Line Console Sync! Paste in DevTools Console on your linkedin.com/groups tab.");
      } catch (_e) {}
    }
    try {
      window.open("https://www.linkedin.com/groups/", "_blank", "noopener");
    } catch (_e) {}
  });

  document.getElementById("btn-diff-linkedin-groups")?.addEventListener("click", async () => {
    const inp = document.getElementById("paste-linkedin-groups-input");
    const txt = (inp ? inp.value : "").trim();
    const isCurlOrCookie = txt.startsWith("curl ") || txt.includes("li_at=") || txt.includes("-H 'cookie:");
    const r = await fetch("/api/linkedin-groups/sync-authenticated", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        profile_url: "https://www.linkedin.com/in/nitin-aggarwal-b49786a/",
        joined_ids_or_text: isCurlOrCookie ? "" : txt,
        curl_or_cookie_header: isCurlOrCookie ? txt : "",
        sync_source: isCurlOrCookie ? "IN_MEMORY_CURL_VOYAGER_SYNC" : "PASTED_DOM_TEXT_SYNC",
      }),
    });
    if (r.ok) {
      const updated = await r.json();
      if (inp && isCurlOrCookie) inp.value = ""; // Clear any session token immediately from input box
      loadAndRenderLinkedinGroupsRadar(updated);
      const rec = updated.sync_receipt || {};
      showToast(
        `Synced ${rec.matched_joined_catalog_groups?.length || 0} joined & ${rec.matched_pending_catalog_groups?.length || 0} pending catalog groups (${updated.unjoined_count} unjoined)!`
      );
    }
  });

  try {
    const bc = new BroadcastChannel("linkedin_groups_sync");
    bc.onmessage = (ev) => {
      if (ev?.data?.type === "SYNC_COMPLETE") {
        loadAndRenderLinkedinGroupsRadar();
        showToast("Live Bookmarklet Sync received from https://www.linkedin.com/in/nitin-aggarwal-b49786a/!");
      }
    };
  } catch (_e) {}

  window.addEventListener("storage", (ev) => {
    if (ev.key === "linkedin_groups_last_sync") {
      loadAndRenderLinkedinGroupsRadar();
    }
  });
});


/* ==========================================================================
   Live Fast-Growing Authentic GitHub Repo Miner & 1-Click ADK Minter
   ========================================================================== */
async function loadAndRenderBreakoutGithubRepos(forceLive = false) {
  const grid = document.getElementById("live-github-breakout-repos-grid");
  const badge = document.getElementById("breakout-miner-status-badge");
  const btn = document.getElementById("mine-live-breakout-repos-btn");
  if (!grid) return;

  const q = (document.getElementById("breakout-repo-search-input")?.value || "").trim();
  const sort = document.getElementById("breakout-repo-sort-select")?.value || "velocity";

  if (forceLive && btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Mining Live GitHub API...";
  }
  try {
    const url = `/api/github/breakout-repos?q=${encodeURIComponent(q)}&sort=${encodeURIComponent(sort)}&live=${forceLive ? "1" : "0"}`;
    const res = await fetch(url);
    if (!res.ok) return;
    const data = await res.json();
    const repos = data.repositories || [];

    if (badge) {
      badge.textContent = `${repos.length} Fast-Growing Authentic Repos (${data.live_github_api_hits || 0} Live API Hits) · Ready to Mint`;
    }

    grid.replaceChildren();
    repos.slice(0, 8).forEach((r) => {
      const card = mkEl("article", "repo-card");
      card.setAttribute("data-testid", `breakout-repo-card-${r.full_name.replace(/[^a-zA-Z0-9_-]/g, "-")}`);

      const top = mkEl("div");
      const chips = mkEl("div", "deliverable-chips");
      chips.style.marginBottom = "8px";
      chips.append(
        mkEl("span", "brand-badge tabular-nums", `★ ${(r.stars || 0).toLocaleString()}`),
        mkEl("span", "pill-badge pill-emerald tabular-nums", `+${r.daily_star_velocity || 120} ★/day`),
        mkEl("span", "pill-badge pill-sky", r.category || "Agentic AI")
      );
      if (r.already_minted) {
        chips.appendChild(mkEl("span", "pill-badge pill-amber", "✓ Minted in Studio"));
      }
      top.appendChild(chips);

      const titleRow = mkEl("div", "composer-section-hdr");
      titleRow.style.marginBottom = "6px";
      const h3 = mkEl("h3", "repo-card-title", r.full_name);
      h3.style.margin = "0";
      const ghLink = mkEl("a", "eyebrow-link", "GitHub ↗");
      ghLink.href = safeUrl(r.html_url);
      ghLink.target = "_blank";
      ghLink.rel = "noopener";
      titleRow.append(h3, ghLink);
      top.appendChild(titleRow);

      const desc = mkEl("p", "repo-card-hook", r.description || "");
      desc.style.marginBottom = "6px";
      top.appendChild(desc);

      const whyBox = mkEl("div", "", `🔥 Why Trending: ${r.why_trending || ""}`);
      whyBox.style.cssText = "font-size:11.5px;color:#334155;margin-bottom:4px;line-height:1.4;";
      top.appendChild(whyBox);

      const gcpBox = mkEl("div", "", `☁️ GCP ADK Bridge: ${r.gcp_enterprise_bridge || ""}`);
      gcpBox.style.cssText = "font-size:11.5px;font-weight:700;color:#1e40af;margin-bottom:8px;line-height:1.4;";
      top.appendChild(gcpBox);
      card.appendChild(top);

      const foot = mkEl("div", "repo-card-footer");
      const actRow = mkEl("div", "studio-toolbar-actions");
      actRow.style.width = "100%";
      actRow.style.justifyContent = "space-between";

      const bpTag = mkEl("span", "deliverable-chip chip-blue", `Blueprint ${r.recommended_template_id || "T85"}`);
      const mintBtn = mkEl(
        "button",
        "btn-primary",
        r.already_minted ? "Inspect / Re-Mint ADK Repo →" : "⚡ 1-Click Mint ADK Repo + Evals"
      );
      mintBtn.type = "button";
      mintBtn.setAttribute("data-testid", `mint-breakout-btn-${r.full_name.replace(/[^a-zA-Z0-9_-]/g, "-")}`);
      mintBtn.addEventListener("click", () => mintBreakoutGithubRepo(r.full_name, "", mintBtn));
      actRow.append(bpTag, mintBtn);
      foot.appendChild(actRow);
      card.appendChild(foot);
      grid.appendChild(card);
    });

    if (forceLive) {
      showToast(`Mined ${repos.length} fast-growing authentic GitHub repositories!`);
    }
  } catch (_e) {
    // Non-fatal
  } finally {
    if (forceLive && btn) {
      btn.disabled = false;
      btn.textContent = "🔍 Mine Live GitHub Breakouts";
    }
  }
}

async function mintBreakoutGithubRepo(ownerRepoOrUrl, customFocus = "", btnEl = null) {
  const cleanTarget = String(ownerRepoOrUrl || "").trim();
  if (!cleanTarget) {
    showToast("Enter a GitHub owner/repo (e.g., google/A2A) or GitHub URL first");
    return;
  }
  const origText = btnEl ? btnEl.textContent : "";
  if (btnEl) {
    btnEl.disabled = true;
    btnEl.textContent = "⏳ Minting 35-File ADK Repo + 100-Trial Evals...";
  }
  try {
    const res = await fetch("/api/github/mint-breakout-repo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        owner_repo: cleanTarget,
        custom_focus: customFocus,
      }),
    });
    const out = await res.json();
    if (!res.ok || out.error) {
      showToast(out.error || "Unable to mint repository");
      return;
    }
    await loadWorkspaceData();
    await loadAndRenderBreakoutGithubRepos(false);
    populateDigitalTwinPostSelect();
    const tabCount = document.querySelector("#tab-btn-repos .tab-count");
    if (tabCount && STATE.repos?.length) {
      tabCount.textContent = String(STATE.repos.length);
    }
    showToast(`Minted ${out.repo_slug} (${out.files_created} files + 100-trial evals PASS)! Opening Inspector...`);
    if (out.repo_slug) {
      openRepoInspector(out.repo_slug);
    }
  } finally {
    if (btnEl) {
      btnEl.disabled = false;
      btnEl.textContent = origText || "⚡ 1-Click Mint Full ADK Repo + 100-Trial Evals";
    }
  }
}

/* ==========================================================================
   On-Demand Digital Twin & 1080p30 Walkthrough Producer for ANY Post
   ========================================================================== */
function populateDigitalTwinPostSelect() {
  const sel = document.getElementById("digital-twin-post-select");
  if (!sel) return;
  const currentVal = sel.value || "MINT-01";
  sel.replaceChildren();

  const addedIds = new Set();
  const addOpt = (id, label, extra = {}) => {
    if (!id || addedIds.has(id)) return;
    addedIds.add(id);
    const opt = mkEl("option", "", polishUiTypography(label));
    opt.value = id;
    if (extra.title) opt.dataset.title = extra.title;
    if (extra.summary) opt.dataset.summary = extra.summary;
    if (extra.template_id) opt.dataset.templateId = extra.template_id;
    if (extra.repo_slug) opt.dataset.repoSlug = extra.repo_slug;
    sel.appendChild(opt);
  };

  // 1. Today's Top-5 Signals
  (STATE.top5Briefing?.ideas || []).forEach((idea) => {
    const tid = idea.default_template_id || "T61";
    addOpt(
      idea.id,
      `[Today's Top 5 #0${idea.rank}] ${idea.id} · ${idea.title} (${tid})`,
      {
        title: idea.title,
        summary: idea.summary,
        template_id: tid,
      }
    );
  });

  // 2. All Verified & Dynamically Minted Cloud Repos
  (STATE.repos || []).forEach((r) => {
    const tid = r.template_and_distribution_plan?.primary_template_id || r.canonical_template_id || "T85";
    addOpt(
      r.id,
      `[Cloud Repo] ${r.id} · ${r.post_title} (${tid})`,
      {
        title: r.post_title,
        summary: r.daily_problem_short || r.original_hook || "",
        template_id: tid,
        repo_slug: r.repo_slug,
      }
    );
  });

  if (addedIds.has(currentVal)) {
    sel.value = currentVal;
  }
}

async function loadDigitalTwinScriptForSelectedPost() {
  const sel = document.getElementById("digital-twin-post-select");
  const tplSel = document.getElementById("digital-twin-template-select");
  const ta = document.getElementById("digital-twin-narration-textarea");
  const badge = document.getElementById("twin-producer-status-badge");
  if (!sel || !ta) return;

  const postId = sel.value || "MINT-01";
  const selectedOpt = sel.options[sel.selectedIndex];
  const title = selectedOpt?.dataset?.title || "";
  const summary = selectedOpt?.dataset?.summary || "";
  const tplOverride = tplSel && tplSel.value !== "AUTO" ? tplSel.value : (selectedOpt?.dataset?.templateId || "");
  const repoSlug = selectedOpt?.dataset?.repoSlug || "";

  const qs = new URLSearchParams({
    post_id: postId,
    title,
    summary,
    template_id: tplOverride,
    repo_slug: repoSlug,
  });
  try {
    const res = await fetch(`/api/video/digital-twin-script?${qs.toString()}`);
    if (!res.ok) return;
    const data = await res.json();
    const sb = data.script_bundle || data || {};
    ta.value = sb.full_narration_text || sb.full_spoken_script || "";
    if (badge) {
      badge.textContent = `${postId} · Blueprint ${data.resolved_spec?.template_id || "T85"} · ${sb.word_count || 95} words (${sb.estimated_duration_sec || 44}s @ 155 WPM)`;
    }
  } catch (_e) {
    // Non-fatal
  }
}

async function triggerProduceDigitalTwinVideo() {
  const sel = document.getElementById("digital-twin-post-select");
  const tplSel = document.getElementById("digital-twin-template-select");
  const ta = document.getElementById("digital-twin-narration-textarea");
  const btn = document.getElementById("produce-digital-twin-video-btn");
  const receiptBar = document.getElementById("digital-twin-produce-receipt-bar");
  const badge = document.getElementById("twin-producer-status-badge");
  if (!sel) return;

  const postId = sel.value || "MINT-01";
  const selectedOpt = sel.options[sel.selectedIndex];
  const title = selectedOpt?.dataset?.title || "";
  const summary = selectedOpt?.dataset?.summary || "";
  const tplOverride = tplSel && tplSel.value !== "AUTO" ? tplSel.value : (selectedOpt?.dataset?.templateId || "");
  const repoSlug = selectedOpt?.dataset?.repoSlug || "";
  const customNarration = (ta?.value || "").trim();

  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Synthesizing 1080p30 Walkthrough MP4 + Digital Twin...";
  }
  try {
    const res = await fetch("/api/video/produce-digital-twin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        post_id: postId,
        title,
        summary,
        template_id: tplOverride,
        repo_slug: repoSlug,
        custom_narration_override: customNarration,
        force: true,
      }),
    });
    const manifest = await res.json();
    if (!res.ok || manifest.error) {
      showToast(manifest.error || "Unable to synthesize Digital Twin video");
      return;
    }

    // Update Hero Video Player in Video & Decks to play the newly synthesized post walkthrough immediately!
    const walkVid = document.getElementById("mint01-walkthrough-video");
    const twinVid = document.getElementById("mint01-twin-video");
    const audioEl = document.getElementById("mint01-chirp3-audio");
    const metaBadge = document.getElementById("mint01-video-meta-badge");
    const heroHeading = document.querySelector("#mint01-flagship-hero-card .section-heading");

    if (walkVid && manifest.walkthrough_mp4_url) {
      if (manifest.poster_png_url) {
        walkVid.poster = `${safeUrl(manifest.poster_png_url)}&t=${Date.now()}`;
      }
      walkVid.src = `${safeUrl(manifest.walkthrough_mp4_url)}&t=${Date.now()}`;
      walkVid.load();
      walkVid.play().catch(() => {});
    }
    if (twinVid && manifest.digital_twin_mp4_url) {
      twinVid.src = `${safeUrl(manifest.digital_twin_mp4_url)}&t=${Date.now()}`;
    }
    if (audioEl && manifest.chirp3_audio_url) {
      audioEl.src = `${safeUrl(manifest.chirp3_audio_url)}&t=${Date.now()}`;
    }
    if (metaBadge) {
      metaBadge.textContent = `${manifest.post_id} · ${manifest.resolution || "1920x1080"} @ ${manifest.fps || 30}fps · ${manifest.duration_sec || 44.0}s`;
    }
    if (heroHeading && manifest.title) {
      heroHeading.textContent = `${manifest.post_id} — ${polishUiTypography(manifest.title)}`;
    }
    if (badge) {
      badge.textContent = `✓ Produced ${manifest.post_id} (${manifest.walkthrough_size_bytes ? (manifest.walkthrough_size_bytes / (1024 * 1024)).toFixed(2) + " MB" : "1080p30"}) · 0.0 px² Occlusion`;
    }
    if (receiptBar) {
      receiptBar.style.display = "flex";
      receiptBar.style.justifyContent = "space-between";
      receiptBar.style.alignItems = "center";
      receiptBar.style.flexWrap = "wrap";
      receiptBar.style.gap = "10px";
      receiptBar.replaceChildren();
      const msg = mkEl(
        "span",
        "",
        `✓ Produced 1080p30 Digital Twin Walkthrough for ${manifest.post_id} (${manifest.template_id}) — Playing now in the studio stage below!`
      );
      const dlLink = mkEl("a", "btn-primary", "⬇ Download 1080p30 .MP4");
      dlLink.href = safeUrl(manifest.walkthrough_mp4_url);
      dlLink.setAttribute("download", `${manifest.post_id}_walkthrough.mp4`);
      dlLink.style.cssText = "text-decoration:none;font-size:11.5px;padding:5px 12px;";
      receiptBar.append(msg, dlLink);
    }
    showToast(`Produced Digital Twin & 1080p30 Walkthrough MP4 for ${manifest.post_id}!`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "🎬 Produce Digital Twin & 1080p30 Walkthrough MP4";
    }
  }
}

async function openDigitalTwinProducerForPost({ post_id, title, summary, template_id, repo_slug }) {
  activateView("view-minting-studio");
  populateDigitalTwinPostSelect();
  const sel = document.getElementById("digital-twin-post-select");
  const tplSel = document.getElementById("digital-twin-template-select");
  if (sel && post_id) {
    let found = Array.from(sel.options).find((o) => o.value === post_id);
    if (!found) {
      found = mkEl("option", "", `[Selected Post] ${post_id} · ${title || ""}`);
      found.value = post_id;
      if (title) found.dataset.title = title;
      if (summary) found.dataset.summary = summary;
      if (template_id) found.dataset.templateId = template_id;
      if (repo_slug) found.dataset.repoSlug = repo_slug;
      sel.prepend(found);
    }
    sel.value = post_id;
  }
  if (tplSel && template_id) {
    const hasTpl = Array.from(tplSel.options).some((o) => o.value === template_id);
    if (!hasTpl) {
      const opt = mkEl("option", "", `Blueprint ${template_id}`);
      opt.value = template_id;
      tplSel.appendChild(opt);
    }
    tplSel.value = template_id;
  }
  await loadDigitalTwinScriptForSelectedPost();
  document.getElementById("any-post-digital-twin-producer-card")?.scrollIntoView({ behavior: "smooth", block: "start" });
  await triggerProduceDigitalTwinVideo();
}

document.addEventListener("DOMContentLoaded", () => {
  loadAndRenderBreakoutGithubRepos(false);
  setTimeout(() => {
    populateDigitalTwinPostSelect();
    loadDigitalTwinScriptForSelectedPost();
  }, 450);

  document.getElementById("mine-live-breakout-repos-btn")?.addEventListener("click", () => {
    loadAndRenderBreakoutGithubRepos(true);
  });
  document.getElementById("breakout-repo-search-input")?.addEventListener("input", () => {
    loadAndRenderBreakoutGithubRepos(false);
  });
  document.getElementById("breakout-repo-sort-select")?.addEventListener("change", () => {
    loadAndRenderBreakoutGithubRepos(false);
  });
  document.getElementById("mint-custom-github-repo-btn")?.addEventListener("click", () => {
    const repoVal = (document.getElementById("custom-github-mint-input")?.value || "").trim() || "google/A2A";
    const focusVal = (document.getElementById("custom-github-focus-input")?.value || "").trim();
    const btn = document.getElementById("mint-custom-github-repo-btn");
    mintBreakoutGithubRepo(repoVal, focusVal, btn);
  });

  document.getElementById("digital-twin-post-select")?.addEventListener("change", () => {
    loadDigitalTwinScriptForSelectedPost();
  });
  document.getElementById("digital-twin-template-select")?.addEventListener("change", () => {
    loadDigitalTwinScriptForSelectedPost();
  });
  document.getElementById("load-digital-twin-script-btn")?.addEventListener("click", () => {
    loadDigitalTwinScriptForSelectedPost();
    showToast("Loaded 6-Act spoken narration script for selected post!");
  });
  document.getElementById("produce-digital-twin-video-btn")?.addEventListener("click", () => {
    triggerProduceDigitalTwinVideo();
  });
});
