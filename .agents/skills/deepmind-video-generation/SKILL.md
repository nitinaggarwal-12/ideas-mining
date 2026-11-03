---
name: deepmind-video-generation
description: Enterprise-grade AI video generation, executive video briefing synthesis, cinematic architecture animations, AI talking avatar narration, multi-scene video storyboard compilation, and Remotion/Canvas video mastering powered by Google DeepMind's Veo 2 / Imagen 3 and multimodal Gemini models.
---

# 🎬 DeepMind Video Generation Engine Skill

This skill provides the architectural framework, API orchestration, and frontend rendering pipelines for generating broadcast-quality executive video briefings, cinematic architecture walkthroughs, animated slide videos, and AI avatar presentations using Google DeepMind's native video synthesis (Veo 2, Imagen 3 Video) and browser-based rendering engines.

---

## 🏗️ Video Synthesis Pipeline Architecture

```
[Assessment Report / Executive Script]
                  │
                  ▼
 1. Multimodal Storyboard Compiler   ──► Generates 5-act visual prompts, scene pacing, and keyframe descriptions
                  │
                  ▼
 2. DeepMind Veo 2 / Imagen 3 Video  ──► High-fidelity generative b-roll, 3D datacenter fly-throughs, architecture flows
                  │
                  ▼
 3. Slide-to-Video Motion Animator   ──► 60fps HTML5 Canvas / Remotion animations of radar charts, heatmaps, KPI counters
                  │
                  ▼
 4. Voiceover & Audio Sync Convolver ──► Aligns DeepMind Neural TTS voice tracks, background ambient music, and sound cues
                  │
                  ▼
 5. In-Browser Player & Video Export ──► HLS streaming preview, WebCodecs/FFmpeg MP4 stitcher, and 1-click YouTube/Drive upload
```

---

## 🎥 1. Google Veo 2 Video Generation Protocol

### Direct Vertex AI Veo 2 API Generation
```javascript
const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY || process.env.VERTEX_AI_KEY
});

/**
 * Generate cinematic architecture or executive B-roll scene using Veo 2
 */
async function generateVeoScene({ prompt, durationSeconds = 5, aspectRatio = '16:9', resolution = '1080p' }) {
  const response = await ai.models.generateVideos({
    model: 'veo-2.0-generate-001',
    prompt: `Cinematic 4K corporate technology visualization: ${prompt}. Ultra-realistic enterprise lighting, smooth camera track, photorealistic Google Cloud infrastructure.`,
    config: {
      durationSeconds,
      aspectRatio,
      personGeneration: 'dont_allow',
      fps: 24
    }
  });

  return {
    videoUri: response.videoUri,
    renderState: response.state
  };
}
```

---

## 🎞️ 2. Dynamic 5-Act Video Storyboard Architecture

For executive presentations, videos are decomposed into a structured **5-Act narrative**:

1. **Act 1: The Executive Hook (0:00 - 0:20)**
   - *Visual*: Dark luxury metallic cover, glowing ScoreX 3D emblem, organization title.
   - *Motion*: Kinetic typography showing Current Score vs. Target Horizon and **Projected 3-Yr ROI ($2.3M - $4.2M)**.
2. **Act 2: The Diagnostic Reality (0:20 - 0:50)**
   - *Visual*: Interactive radar chart sweep, dimensional risk heatmap highlighting critical technical debt.
   - *Motion*: Red pulsing nodes on legacy batch ETL, point-to-point cron pipelines, and idle VM compute waste.
3. **Act 3: Target State Architecture (0:50 - 1:30)**
   - *Visual*: 3D isometric animation of Google Cloud BigLake Medallion Architecture, Datastream CDC (<1s), Vertex AI Agent Mesh.
   - *Motion*: Smooth data particles streaming from ingestion to Iceberg open tables to AI agents.
4. **Act 4: 30-60-90 Day Transformation Horizon (1:30 - 2:00)**
   - *Visual*: 3-phase horizontal timeline cards dynamically filling with checkmarks and milestone badges.
5. **Act 5: Financial Realization & Board Sign-off (2:00 - 2:30)**
   - *Visual*: 35-50% TCO reduction metrics, financial payback curve, CTO governance sign-off card.

---

## 🎨 3. Browser-Side Canvas & Remotion Video Rendering

To render video slides in-browser with zero cloud rendering lag:

```javascript
/**
 * Real-time 60fps Canvas Animation Frame for Radar & KPI Counters
 */
export const renderSlideCanvasFrame = (ctx, { width, height, progress, scores, customerName }) => {
  ctx.clearRect(0, 0, width, height);

  // Background Gradient
  const bgGrad = ctx.createLinearGradient(0, 0, width, height);
  bgGrad.addColorStop(0, '#0b132b');
  bgGrad.addColorStop(1, '#1c2541');
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, width, height);

  // Interpolated Score Counter
  const currentScoreVal = (scores.overallScore * Math.min(1, progress * 1.5)).toFixed(1);
  ctx.font = 'bold 64px Arial';
  ctx.fillStyle = '#34d399';
  ctx.fillText(`${currentScoreVal} / 5.0`, 120, 240);

  // Progress Bar
  ctx.fillStyle = '#1d4ed8';
  ctx.fillRect(120, 280, (width - 240) * progress, 8);
};
```

---

## 🔒 4. Enterprise Video Governance & Compliance
- **Zero Third-Party Egress**: 100% Google Cloud Vertex AI & native WebCodecs in-browser mastering.
- **Watermarking & Classification**: Automatic "STRICTLY CONFIDENTIAL - BOARD USE ONLY" digital watermark on all generated MP4 frames.
- **Fast Preview Streaming**: HLS / MP4 fast-start (`moov` atom at front) for instant playback on mobile and desktop monitors.

---

## 🧑‍💼 5. Cohesive Omni 1.1 Audio-Video Per-Slide MP4 Protocol (`models/gemini-omni-1.1-flash`)
- **Zero 2D Cartoon Avatars, Zero Canvas Jaw-Slicing & Multi-Deck Cohesive Digital Twin Clips (`OMNI_DECK_MANIFESTS` + `OMNI_SLIDE_SCRIPTS_BY_DEMO`)**: Every slide in Omni-enabled playbook decks (`merck-skills-workflow-playbook`, `merck-adk-a2a-a2ui-playbook`, and future playbooks registered in `OMNI_DECK_MANIFESTS`) is backed by a cohesive 720p 24fps H.264 `.mp4` video with native 48kHz stereo speech audio, real human lip-sync, natural hand gestures, and eye blinks generated by `models/gemini-omni-1.1-flash` (`https://generativelanguage.googleapis.com/v1beta/interactions`) from `/screenshots/avatars/twin_*.jpg`. Pre-rendered clips are stored per deck under `screenshots/omni-video/<demoKey>/slide_<01..18>_<personaId>.mp4` (`144` clips across `8 Digital Twins × 18 slides` for `merck-skills-workflow-playbook`, plus `36+` pre-rendered clips across `sundar-puck` & `indra-diya × 18 slides` for `merck-adk-a2a-a2ui-playbook`) via `DEMO_KEY=<demoKey> ONLY_PERSONAS=<personas> node scripts/generate_omni_cohesive_slide_videos.mjs` so every persona plays unmuted (`muted === false`, `loop === false`) with real lip-sync on every slide.
- **Immediate Slide 1 Playback + Background Lookahead Queue (`POST /api/omni-video/prefetch` & `ensureCohesiveOmniSlideVideo`)**: Selecting any Digital Twin or custom script plays Slide 1 as soon as ready while `POST /api/omni-video/prefetch` (`triggerOmniBackgroundPrefetch`) passes `demoKey: currentDemoKey` and queues/synthesizes any uncached slides in playback order (`concurrency = 3`, deduplicated via `IN_FLIGHT_OMNI_SLIDE_PROMISES` with deck-scoped SHA-256 key `omni11::${safeDemoKey}::${videoTwin}::${conciseScript}`) ready for their turn.
- **15–18 Word Immediate Vocal Attack (`0.0s`), Brisk 165-WPM Keynote Pace, Non-Blocking Startup & WebAudio Speech-End Auto-Advance (`window.__omniClipSpeechEndSec`)**: Each slide's cohesive spoken script is 15–18 words with immediate vocal attack (`0.0s`) and brisk 165-wpm keynote delivery so the complete sentence finishes by `6.0s` inside the `8.0s` MP4 clip with zero cut-off words. `startSlideNarration` never blocks active playback waiting for a 2MB Blob download: it plays from `window.__omniBlobUrlCache` if ready or streams `canonicalUrl` immediately while `resolvePlayableOmniVideoSrc` warms the RAM blob and decodes the audio track into `window.__omniClipSpeechEndSec`, advancing to the next slide at `speechEndSec + 0.25s` with a `100ms` zero-freeze transition (`onNarrationFinished(true)`).
- **Zero-Overlap PiP Gutter & Multi-Deck Cohesive Video Law (`verify_all_12_forensic_fixes.mjs` & `verify_audio_video_completeness_and_zero_freeze.mjs`)**: `#aiPresenterVideoPip` docks in a dedicated `264px` right/left gutter (`0 px²` overlap with `#slide-img` across Normal, Edit, and Fullscreen Theater modes) with wrapped `.pip-footer-controls` (`0px` button clipping), and `resolveLocalOmniCohesiveVideo` / `lookupPreRenderedOmniSlideVideo` / `buildCompleteOfflinePackageZipBuffer` resolve per-deck manifests (`OMNI_DECK_MANIFESTS[currentDemoKey]` / `resolveDeckOmniScripts(safeDemoKey)` / `resolveDeckCohesiveScripts(slug)`) so each playbook deck plays and exports its own lip-synced MP4 videos while non-Omni decks never inherit wrong-deck audio or video.

---

## 🚫 6. Strict Zero-Hardcoding & Dynamic Per-Deck Manifest Law (`resolveDeckOmniScripts` + `OMNI_DECK_MANIFESTS` + `manifest.json`)
- **Forbidden Hardcoded Deck-Slug Checks**: Never write `(currentDemoKey|demoKey|safeDemoKey|slug) === 'merck-skills-workflow-playbook'` or `=== 'merck-adk-a2a-a2ui-playbook'` inside `resolveLocalOmniCohesiveVideo`, `startSlideNarration`, `lookupPreRenderedOmniSlideVideo`, `ensureCohesiveOmniSlideVideo`, `buildCompleteOfflinePackageZipBuffer`, or `resolveLiveOmniVideoUrl`.
- **Mandatory Registry & Filesystem-Driven Resolution**:
  1. **Frontend (`src/portal-views/slides-fullscreen.html` & `live-demo-narrator.html`)**: Always resolve deck scripts and pre-baked persona sets via declarative maps (`OMNI_DECK_MANIFESTS[currentDemoKey]`, `OMNI_PREBAKED_PERSONAS_BY_DECK[currentDemoKey]`, `OMNI_SLIDE1_PERSONAS_BY_DECK[currentDemoKey]`, and `DEMO_META[currentDemoKey].cleanViewDefault`).
  2. **Backend (`src/mcp-server/server.mjs` & `src/mcp-server/merckMicrosoftValidatorAndPptx.mjs`)**: Always resolve per-deck scripts via `resolveDeckOmniScripts(safeDemoKey)` and `resolveDeckCohesiveScripts(slug, rootDir)`, which automatically parse `screenshots/omni-video/<demoKey>/manifest.json` from disk whenever a new deck is generated.
  3. **Batch Pre-Bake CLI (`scripts/generate_omni_cohesive_slide_videos.mjs`)**: Always resolve slide scripts via `resolveSlideScriptsForDemo(DEMO_KEY)`, which automatically extracts `DEMO_DECKS[DEMO_KEY]` from `slides-fullscreen.html` if `DEMO_KEY` is not yet in `SLIDE_SCRIPTS_BY_DEMO`.


## Humanized Multi-Shot Narration (Rule 51 Addendum, 2026-10-08)
For presenter clips, write 2–3 conversational shots per slide (<=18 words each), render each with a natural consultative pace directive, trim at speech end +0.3s, and stitch per slide with ffmpeg (`-nostdin` when driven via `bash -s`). Never narrate deck structure (`Slide N`), gloss jargon once, and disclose real gaps.

## Transcription QA Gate for Omni 1.1 Shots (2026-10-08)

- Omni 1.1 renders a fixed 8.0 s window. When the script ends early the model may **echo the last phrase** or stutter; an echo is speech, so silence-based trimming cannot remove it.
- Every shot must pass `generateVerifiedOmniShot()` in `scripts/generate_omni_cohesive_slide_videos.mjs`: verbatim transcript by an orthogonal judge (`gemini-2.5-flash`, temp 0, numbers written as words) → `judgeShotTranscript()` (no script 2/3-gram heard more often than written, no adjacent-word stutter, ≥85 % spelling-tolerant word coverage, no long extra tail) → regenerate up to `OMNI_QA_MAX_REGEN` (3) times; verdict stored in `<shot>.mp4.qa.json`.
- Prompt tail directive must say "Say the text EXACTLY ONCE — never repeat, echo, re-say or paraphrase… stay completely silent" after the last word.
- Re-verify/re-stitch existing decks with `DEMO_KEY=<deck> OMNI_RESTITCH=1 node scripts/generate_omni_cohesive_slide_videos.mjs` (shots live in `screenshots/omni-video/<deck>/shots/`, git-ignored).

## 👤 7. My Presenter — Custom Photo + Voice Digital Twin (Rule 68, 2026-10-09)
- Store: `src/mcp-server/customPersonaStore.mjs` (`createCustomPersona`, `loadCustomPersona`, `customPersonaToTwinMeta`, `customPersonaRenderStatus`). Endpoints `/api/persona/custom` (GET list, POST {displayName, photoBase64, voiceBase64?, consent:true, demoKey}, DELETE /:id, GET /:id/status?demoKey=).
- Pipeline: photo → Omni 1.1 reference image (same path as the 8 studio twins); voice sample → `gemini-2.5-flash` audio+image JSON profile (`isFemale`, `appearance`, `voiceDesc`) → Omni speaks in that described voice. True clone only via Chirp 3 Instant Custom Voice when allowlisted (`voiceMode: 'cloned'`).
- Invariants: custom id maps to its own `videoTwin`; no cross-twin face fallback (poster = uploaded photo while rendering); UI lives inside accordion 2 (6-accordion harness invariant); consent required; uploads git-ignored.


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
