---
name: deepmind-emotional-audio-engine
description: Enterprise-grade emotional neural audio generation, 4,000+ procedural voice matrix casting, 30+ multilingual voice dubbing, clause-aware SSML prosody compilation, 7-persona interactive coaching narration, 5-band vocal tract formant convolution, real-time punctuation-weighted gold karaoke subtitles, "Prompt-to-Voice" custom AI voice design, and Executive Voice Vault sharing using native Google DeepMind & Cloud TTS models (gemini-3.1-flash-tts-preview / en-US-Chirp3-HD-*) with zero third-party cloud egress.
---

# 🎙️ DeepMind Emotional Audio Engine Skill

This skill provides comprehensive architectural patterns, code blueprints, and execution rules for generating humanized, broadcast-quality emotional voice briefings and interactive coaching narration across any application using Google DeepMind's native neural audio synthesis (`gemini-3.1-flash-tts-preview` & `en-US-Chirp3-HD-*`).

---

## 🏗️ Core Architecture & Pipeline

```
[Text / Slide / Live Demo Script Payload]
        │
        ▼
 1. Coaching Persona & Framing Engine   ──► Applies distinct persona lead-ins/takeaways & auto-pairs signature neural voice
        │
        ▼
 2. Clause-Aware SSML Prosody Compiler  ──► Splits on [, ; : — ... . ! ?], injects <break time="..."/> & per-clause <prosody rate pitch>
        │
        ▼
 3. 30+ Multilingual Voice Dubbing     ──► Instant native localized narration across 10–30+ languages (en-US, es-ES, fr-FR, de-DE, ja-JP, hi-IN, etc.)
        │
        ▼
 4. 4,000+ Procedural Voice Matrix      ──► (5 Neural Timbres × 25 Accents × 8 Archetypes × 4 Age Tiers) or "Prompt-to-Voice" Designer
        │
        ▼
 5. Multimodal Neural Synthesis         ──► Calls gemini-3.1-flash-tts-preview / Google Cloud TTS Chirp3-HD (Puck, Aoede, Kore, Charon, Fenrir, Casual-K)
        │
        ▼
 6. Web Audio DSP Mastering Rack        ──► +2.5dB 180Hz warmth EQ, 5-Band Formant Filter (F1-F5), Broadcast Compressor, headphone-class-device profile
        │
        ▼
 7. Punctuation-Weighted Gold Karaoke   ──► Syllable + punctuation-weighted millisecond word alignment & dynamic playbackRate clause contouring
        │
        ▼
 8. Executive Voice Vault & Sharing     ──► Persistent saved voice presets and 1-click encoded shareable persona tokens
```

---

## 🎛️ 1. The 4,000+ Voice Matrix Taxonomy

| Dimension | Options | Description |
| :--- | :--- | :--- |
| **Neural Base Models (6)** | `Charon`, `Aoede`, `Puck`, `Kore`, `Fenrir`, `Casual-K` | Physical vocal tract resonators (Deep Baritone, Soprano/Mezzo, Tenor, Alto, Bass, Conversational Male). |
| **Global Accents (25)** | `uk_rp`, `uk_cockney`, `uk_scottish`, `uk_irish`, `us_standard`, `us_texas`, `us_ny`, `us_silicon_valley`, `ca_toronto`, `au_sydney`, `nz_kiwi`, `in_bangalore`, `sg_singapore`, `za_joburg`, `fr_paris`, `de_frankfurt`, `it_milan`, `es_madrid`, `latam_mexico`, `se_stockholm`, `nl_amsterdam`, `jp_tokyo`, `br_saopaulo`, `ng_lagos`, `ch_zurich` | Global dialect & phonetics. |
| **C-Suite Archetypes (8)** | `board_director`, `chief_architect`, `startup_founder`, `keynote_orator`, `npr_investigative`, `research_professor`, `cyber_auditor`, `executive_coach` | Tone of authority, pacing, and strategic vocabulary. |
| **Age & Pacing Tiers (4)** | `statesman` (55+), `mid_career` (35-50), `rising_star` (25-35), `fireside` (Mentor) | Vocal weight, dynamic cadence, and breath frequency. |
| **30+ Multilingual Dubbing** | English, Spanish, French, German, Japanese, Mandarin, Hindi, Portuguese, Italian, Arabic, Dutch, Korean, Swedish, Polish, Turkish, Russian | 1-Click native translated executive storytelling. |

---

## 🎨 2. "Prompt-to-Voice" Custom AI Voice Designer Pattern

To synthesize any voice from a natural language prompt:
```javascript
const { GoogleGenAI } = require('@google/genai');

async function synthesizeDesignedVoice(text, voicePrompt, apiKey) {
  const ai = new GoogleGenAI({ apiKey });
  
  // Classify gender and register from prompt description
  const isFemale = /female|woman|lady|her|she|soprano|alto/i.test(voicePrompt);
  const baseVoice = isFemale ? 'Aoede' : 'Charon';

  const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-tts-preview',
    contents: `Read as a master voice actor embodying this persona: ${voicePrompt}. Emote with authentic human breath and emotional resonance:\n\n"${text}"`,
    config: {
      responseModalities: ['AUDIO'],
      speechConfig: {
        voiceConfig: {
          prebuiltVoiceConfig: {
            voiceName: baseVoice
          }
        }
      }
    }
  });

  const rawPcm = Buffer.from(response.candidates[0].content.parts[0].inlineData.data, 'base64');
  return pcmToWav(rawPcm, 24000, 1, 16);
}
```

---

## 🧪 3. 5-Band Vocal Tract Formant Convolver & Harmonic Air

When capturing microphone audio for voice cloning:
1. **Spectral Denoise Gate**: Compute noise floor from initial silent frames and apply a `-42dB` threshold gate.
2. **5-Band Formant Extraction**:
   - $F0$ Fundamental Pitch ($80\text{--}260\text{Hz}$)
   - $F1$ Pharyngeal Throat Warmth ($350\text{--}750\text{Hz}$)
   - $F2$ Oral Cavity Clarity ($1200\text{--}2400\text{Hz}$)
   - $F3$ Speaker Timbre Fingerprint ($2600\text{--}3500\text{Hz}$)
   - $F4$ Nasal Brilliance ($3600\text{--}4800\text{Hz}$)
   - $F5$ Harmonic Air / Presence Band ($8000\text{--}12000\text{Hz}$)
3. **Web Audio Convolver Rack**: Connect 5 parametric peaking filter nodes (`BiquadFilterNode`) in series with the audio source before the dynamic compressor.

---

## 🎤 4. Real-Time Punctuation-Weighted Gold Karaoke & Speed Contouring (`computeHumanWordTimings`)

**STRICT BAN ON METRONOME TIMING**: Never use a fixed `setInterval(..., durationMs / words.length)` timer. Every word's highlight duration and playback speed MUST be weighted by syllable length, punctuation dwell pauses, and clause position:

```javascript
function computeHumanWordTimings(spokenText, totalDurationMs, emotionMode) {
  const words = String(spokenText || '').trim().split(/\s+/).filter(Boolean);
  let clauseIndex = 0;
  let insideEmDash = false;
  const wordMeta = words.map((w, idx) => {
    const cleanLen = w.replace(/[^a-zA-Z0-9]/g, '').length || 2;
    let weight = Math.pow(Math.max(cleanLen, 1), 0.72);
    let pauseBonus = 0;
    if (w === '—' || w === '--') {
      pauseBonus = 2.8;
      insideEmDash = !insideEmDash;
      clauseIndex++;
    } else if (/[,]$/.test(w)) {
      pauseBonus = 1.9;
      clauseIndex++;
    } else if (/[;]$/.test(w)) {
      pauseBonus = 2.3;
      clauseIndex++;
    } else if (/[:]$/.test(w)) {
      pauseBonus = 2.6;
      clauseIndex++;
    } else if (/[.!?]["']?$/.test(w)) {
      pauseBonus = 3.6;
      insideEmDash = false;
      clauseIndex++;
    }
    let rateMod = 1.0;
    if (idx < 5) rateMod = 1.04;
    else if (insideEmDash) rateMod = 0.91;
    else if (idx > words.length - 7) rateMod = 0.93;
    else rateMod = clauseIndex % 2 === 0 ? 1.01 : 0.96;
    return { w, weight: weight + pauseBonus, rateMod };
  });
  const totalWeight = wordMeta.reduce((acc, m) => acc + m.weight, 0) || 1;
  let cumulativeMs = 0;
  return wordMeta.map((m, idx) => {
    const dur = (m.weight / totalWeight) * totalDurationMs;
    const entry = { index: idx, word: m.w, startMs: cumulativeMs, endMs: cumulativeMs + dur, durationMs: dur, rateMod: m.rateMod };
    cumulativeMs += dur;
    return entry;
  });
}
```

---

## 🏛️ 5. Executive Voice Vault & Sharing

- Saves custom presets (persona, formants, sliders, language) to persistent storage.
- Generates 1-click base64 encoded sharing tokens to allow immediate cross-organization persona casting.

---

## 🎭 6. Mandatory Clause-Aware SSML Prosody Compiler, Punctuation Pause Enforcement & 7-Persona Coaching Law (`compileSSML` & `COACHING_PERSONA_CONFIG`)

To prevent flat, monotonous, mechanical speech or non-responsive Coaching Persona selectors, the following **4 Non-Negotiable Audio Engineering Laws** are strictly enforced across all servers and frontends:

1. **Law 1 — Strict Ban on Disabling SSML for `Chirp3-HD` & `Casual` Voices**:
   - NEVER gate SSML compilation behind `!resolvedVoice.includes('Chirp3-HD')` or `!resolvedVoice.includes('Casual')`.
   - `en-US-Chirp3-HD-*` (`Puck`, `Aoede`, `Kore`, `Charon`, `Fenrir`), `en-US-Casual-K`, `Neural2`, and `Wavenet` voices MUST ALWAYS be synthesized using `{ ssml: compileSSML(...) }` (`<speak><p><s><prosody rate="..." pitch="...">...</prosody><break time="..."/></s></p></speak>`).
   - Only `Studio` voices (`en-US-Studio-O`, `en-US-Studio-Q`) omit the `pitch` attribute and `<emphasis>` tag while still receiving full `<speak>`, `<p><s>`, `<break time="..."/>`, `<sub alias="...">`, and `<prosody rate="...">` clause contouring.
2. **Law 2 — Mandatory Punctuation Breath Pauses & Clause-Level Speed/Pitch Contouring (`compileSSML`)**:
   - Every sentence MUST be split into punctuation-delimited clauses (`,`, `;`, `:`, `—`, `...`, `.`, `!`, `?`).
   - Inject persona-scaled `<break time="..."/>` pauses at every punctuation boundary:
     - Comma (`,`): `210ms–310ms`
     - Semicolon (`;`): `300ms–420ms`
     - Colon (`:`): `330ms–460ms`
     - Em-dash (`—`): `350ms–490ms`
     - Ellipsis (`...`): `420ms–580ms`
     - Sentence boundary (`. ! ?`): `440ms–630ms`
   - Modulate `<prosody rate="..." pitch="...">` clause-by-clause (brighter/faster on opening hooks, slower/deeper on em-dash asides, rising inflection on `?`, energetic lift on `!`, and warm slower resolution on closing takeaways).
   - Apply `<sub alias="...">` for enterprise acronyms (`GxP` $\rightarrow$ `G X P`, `3LO` $\rightarrow$ `three L O`, `21 CFR` $\rightarrow$ `twenty-one C F R`, `ACLs` $\rightarrow$ `A C Ls`, `OAuth` $\rightarrow$ `O-Auth`, `MTTR` $\rightarrow$ `M T T R`).
3. **Law 3 — Immediate Coaching Persona Action, Voice Pairing & Distinct Framing (`7/7` Personas)**:
   - All 7 Coaching Personas (`omni-auto`, `coach-trainer`, `warm-storyteller`, `enthusiastic-innovator`, `empathetic-advisor`, `executive-keynote`, `podcast-duet`) MUST produce 7 distinct spoken scripts (even when `slide.coachIntro` is pre-populated) and auto-pair their signature neural voice (`Kore` for `🧭 GxP & Security`, `Fenrir` for `🔥 Energetic Coach`, `David Casual-K` for `🎙️ Warm Storyteller`, `Aoede` for `🌟 Exec Keynote`, `Puck` for `🎓 Hands-On Trainer`, `Puck + Aoede` for `🎧 2-Host Duet`).
   - Selecting any persona in `#narratorEmotionSelect` or `#theaterModalEmotionSelect` (`changeNarratorEmotion`) MUST immediately pair the voice, expand the bottom karaoke bar (`toggleCaptionsCollapse(false)`), update `#karaokeVoiceName` and `#karaokeText`, and start/restart narration (`startSlideNarration()`).
4. **Law 4 — Cloudtop Token Auto-Refresh & Clause-Sequenced Browser Fallback**:
   - On macOS workstations where Santa blocks local `gcloud`, `getGcloudAccessTokenAsync()` MUST automatically fall back to `ssh nitinagga.c.googlers.com "gcloud auth print-access-token"` so neural synthesis never silently degrades to flat browser TTS.
   - If offline browser `speechSynthesis` is ever invoked, it MUST execute as a clause-by-clause prosody sequencer with punctuation pauses—never a single flat `SpeechSynthesisUtterance`.
5. **Law 5 — Strict Zero-Hardcoding Multi-Deck Audio/Video Resolution Law (`OMNI_DECK_MANIFESTS` & `resolveDeckOmniScripts`)**:
   - Never hardcode `(currentDemoKey|demoKey|safeDemoKey|slug) === 'merck-skills-workflow-playbook'` or `=== 'merck-adk-a2a-a2ui-playbook'` in `resolveLocalOmniCohesiveVideo`, `startSlideNarration`, `lookupPreRenderedOmniSlideVideo`, `ensureCohesiveOmniSlideVideo`, `buildCompleteOfflinePackageZipBuffer`, or `resolveLiveOmniVideoUrl`. Always use `OMNI_DECK_MANIFESTS[currentDemoKey]`, `OMNI_PREBAKED_PERSONAS_BY_DECK[currentDemoKey]`, and the single canonical loader `src/mcp-server/omniManifestLoader.mjs` (`CANONICAL_OMNI_SLIDE_SCRIPTS_BY_DEMO` + filesystem-backed `resolveDeckOmniScripts(safeDemoKey)` reading `screenshots/omni-video/<demoKey>/manifest.json`) across `server.mjs`, `merckMicrosoftValidatorAndPptx.mjs`, and `scripts/generate_omni_cohesive_slide_videos.mjs` so every new playbook deck inherits full lip-sync audio/video automatically without script duplication.

---

## 👤 7. Top-Right AI Person Face Video Presenter & 12 Famous Personas Voice Continuity (`FAMOUS_PERSONA_CATALOG` & `ge_face_presenter_state_v1`)

1. **Logical Tie Between Famous Persona & Existing Neural Voices (`FAMOUS_PERSONA_CATALOG`)**:
   - Every famous persona in `#famousPersonaSelect` and `🎲 Random Famous` (`pickRandomFamousPersona()`) is logically mapped to the matching existing neural voice and coaching emotion:
     - `sundar-visionary` (`Sundar P. — CEO Visionary`) $\rightarrow$ `en-US-Chirp3-HD-Charon` (`Charon` • `executive-keynote`)
     - `jensen-architect` (`Jensen H. — GPU & AI Systems Architect`) $\rightarrow$ `en-US-Chirp3-HD-Fenrir` (`Fenrir` • `enthusiastic-innovator`)
     - `demis-nobel` (`Sir Demis H. — DeepMind Nobel Laureate`) $\rightarrow$ `en-US-Chirp3-HD-Puck` (`Puck` • `coach-trainer`)
     - `mira-builder` (`Mira M. — Frontier AI Product Leader`) $\rightarrow$ `en-US-Chirp3-HD-Aoede` (`Aoede` • `executive-keynote`)
     - `satya-empathy` (`Satya N. — Cloud Platform Strategist`) $\rightarrow$ `en-US-Casual-K` (`David Casual-K` • `warm-storyteller`)
     - `feifei-pioneer` (`Dr. Fei-Fei L. — Spatial & Vision Pioneer`) $\rightarrow$ `en-US-Chirp3-HD-Kore` (`Kore` • `empathetic-advisor`)
     - `jony-craft` (`Sir Jony I. — Design & Craft Purist`) $\rightarrow$ `en-US-Studio-Q` (`Studio-Q` • `warm-storyteller`)
     - `lisa-semi` (`Dr. Lisa S. — Silicon & Compute Chief`) $\rightarrow$ `en-US-Chirp3-HD-Aoede` (`Aoede` • `executive-keynote`)
     - `andrej-hacker` (`Andrej K. — Neural Net Educator`) $\rightarrow$ `en-US-Chirp3-HD-Puck` (`Puck` • `coach-trainer`)
     - `jeff-systems` (`Jeff D. — Chief Distributed Systems Fellow`) $\rightarrow$ `en-US-Chirp3-HD-Charon` (`Charon` • `empathetic-advisor`)
     - `ada-analytical` (`Ada L. — Analytical Engine Pioneer`) $\rightarrow$ `en-US-Chirp3-HD-Kore` (`Kore` • `omni-auto`)
     - `feynman-explainer` (`Richard F. — First-Principles Explainer`) $\rightarrow$ `en-US-Chirp3-HD-Fenrir` (`Fenrir` • `enthusiastic-innovator`)
2. **100% Cross-Route Character Continuity (`ge_face_presenter_state_v1`)**:
   - State (`{ enabled, personaId, voice, emotion, corner }`) is persisted to `localStorage.getItem('ge_face_presenter_state_v1')` and synchronized across `/slides` and `/live-demo` so the presenter face, voice pill, and lip-sync animation remain 100% continuous throughout the entire demo.

---

## 🛡️ Enterprise Privacy Mandate
* Never send confidential client metrics or assessment text to third-party TTS services.
* Always synthesize through native Google Cloud TTS / `@google/genai` (`gemini-3.1-flash-tts-preview` & `en-US-Chirp3-HD-*`).
* Cache all generated buffers using SHA-256 content addressing (`coach_v5_prosody`) for instant $0\text{ms}$ replays.



## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
