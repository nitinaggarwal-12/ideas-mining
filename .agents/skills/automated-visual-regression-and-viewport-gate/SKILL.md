# automated-visual-regression-and-viewport-gate


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
