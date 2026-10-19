---
name: ideas-mining-openhands-microagent
type: repo
version: 2.0.0
agent: CodeActAgent
triggers:
  - ui
  - repo
  - diagram
  - terraform
  - verify
---

# OpenHands Autonomous Repository & UI Engineering Microagent

You are an autonomous OpenHands software engineer operating inside `/Users/nitinagga/Documents/ideas-mining`.
Unlike static markdown meta-prompt frameworks (BMAD), you execute real code inside a sandboxed environment:

1. **Workspace Inspection**: Always inspect `src/catalog/posts_catalog.py` and existing tests before modifying code.
2. **Executive Light Theme UI Development (`Rule 54` & `Rule 25`)**:
   - Build and maintain `public/index.html`, `public/styles.css`, and `public/app.js` using `#f8fafc` (`bg-slate-50`) root background, `#ffffff` cards and drawers, `#0f172a` typography, `100%` fluid width, rigid table cell containment (`overflow: hidden; max-width: 0; height: 1px;`), and non-blocking right-side drawers.
3. **Sandbox Verification Before Commit**:
   - Run `python3 scripts/verify_all_repos.py` to execute unit tests across all 8 generated repositories, verify zero SVG/Draw.io node collisions, validate 12-slide `.pptx` decks, and verify Terraform HCL files before proposing any Git commit.
