# Corrected MCP Authorization Package — Exact Fixes vs. Original Post & Pass-1 Critique

Source audited: Jean Lee (`jeanklee`), *"How MCP Authorization Works"*, LinkedIn `activity-7526630995425644545-x4Sk` (`1080×1350` `GIF89a`, `180` frames, `6.00s`, `2026-11-12T13:04:27Z`).

## 1. Visual Copy, Typo & Spacing Fixes (6/6 Resolved)
| Zone | Original Bug in GIF | Fixed in Production Version |
|---|---|---|
| Zone 1 (`Auth Server`) | `Separate role (can be-hosted)` | `Co-hosted or self-hosted` (`Separate IdP Role`) |
| Zone 2 (Step 2 / Hop 2) | `401 + www-Authenticate` | `401 + WWW-Authenticate` |
| Zone 2 (Step 3 / Hop 3) | `GET /.well-know/oauth-protected-resource` | `GET /.well-known/oauth-protected-resource` |
| Zone 2 (Step 5 / Hop 5) | `Fetch auth server Metadata IRFC 8414 / OIDC)` | `Fetch auth server metadata` `<->` `RFC 8414 / OIDC (issuer, endpoints)` |
| Zone 2 (Step 9 / Hop 9) | `scopped` | `scoped consent` |
| Zone 2 (Step 10 / Hop 10) | `resourse (RFC 8707)` | `resource (RFC 8707)` |
| Monospace Pills | Cramped punctuation (`scopes_supported.authorization_servers`, `PKCES256`) | Chrome-measured symmetric `8px` padded rounded monospace pills |

## 2. Adversarial Design & Protocol Fixes (Pass-2 Polish)
1. **Band Spotlight Containment (`5/6` fixed -> `0` border collisions)**: Shifted all Phase bands (`y0..y1`) so every hop halo (`y - 25 .. y - 4`) sits `>= 7px` inside its band top and `>= 12px` above its band bottom.
2. **Lifeline Alignment (`Hop 7` & `Hop 13`)**: Clamped `Hop 7` inside `[122..]` (zero bleed past User lifeline `x=120`) and tightened `Hop 13` (`13 · RFC 8693 OBO` `<->` `urn:...:token-exchange · sub+act ≤5m`), ending well before `Downstream APIs`.
3. **Strict Terminology & Protocol Precision**: Unified `Downstream APIs` (`External Services`); stripped meta-word `CORRECTED` from eyebrow pill; fixed subtitle comma (`OAuth 2.1, RFC 9728/8414 discovery, PKCE + audience binding`); replaced `grant_type=token-exchange` invalid literal with `urn:...:token-exchange · sub+act ≤5m` (full URN in post); added `state` to `Hop 7`; made `Hop 5` `<->` returning issuer metadata; clarified headless WIF skips Steps 7–9 directly to Step 5.
4. **WCAG 2.2 AA Contrast (`>= 4.5:1`)**: Darkened Amber (`#D97706 -> #B45309`), Emerald (`#059669 -> #047857`), and Teal (`#0D9488 -> #0F766E`) across all badges, subtitles, and step boxes.
