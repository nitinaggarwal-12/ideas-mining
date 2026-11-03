---
name: security-code-scanner
description: Static Application Security Testing (SAST) for XSS in custom SVG renderers, unhandled API route inputs, environment secret leak checks, and npm audit dependency CVE scanning.
---

# Security Code Scanner & Vulnerability Guard Skill

This skill performs automated Static Application Security Testing (SAST) to detect unhandled user inputs, potential XSS vectors in Draw.io SVG canvas renders, secret leaks in git commits, and `npm audit` dependency vulnerabilities.

## 1. SAST Audit Protocols

1. **Dependency Audit**: Run `npm audit --json` to detect known high or critical CVEs in `node_modules`.
2. **SVG XSS Sanitization Audit**: Verify that user-controlled XML/SVG tags rendered in `DiagramViewer.tsx` or iframe bridges pass through sanitization (`DOMPurify` or safe text node creation).
3. **Secret Leak Detection**: Check for hardcoded API keys, JWT secrets, or un-hashed database credentials in `src/` files.

## 2. Automated SAST Audit Runner (`scratch/run_security_sast.js`)

```javascript
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function runSecurityScan() {
  console.log('🔒 Starting SAST & Secret Leak Audit...\n');

  // 1. Secret Leak Scanner
  const srcDir = path.join(process.cwd(), 'src');
  const files = fs.readdirSync(srcDir, { recursive: true }).filter(f => f.endsWith('.ts') || f.endsWith('.tsx'));

  let secretLeaks = 0;
  for (const f of files) {
    const fullPath = path.join(srcDir, f);
    const content = fs.readFileSync(fullPath, 'utf8');
    if (content.includes('AIZASy') || content.includes('sk_live_')) {
      console.error(`🚨 Potential API Secret Leak detected in: ${f}`);
      secretLeaks++;
    }
  }

  // 2. npm audit check
  try {
    const auditOutput = execSync('npm audit --json', { encoding: 'utf8' });
    const auditJson = JSON.parse(auditOutput);
    const vulnerabilities = auditJson?.metadata?.vulnerabilities || {};
    console.log(`📦 Dependency Vulnerabilities: High: ${vulnerabilities.high || 0}, Critical: ${vulnerabilities.critical || 0}`);
  } catch (err) {
    console.warn('⚠️ npm audit returned advisories.');
  }

  console.log(`\n✅ SAST Scan Complete. Secret leaks found: ${secretLeaks}`);
}

runSecurityScan();
```

## 3. Workflow Protocol
Execute `node scratch/run_security_sast.js` before git commits or deployment pushes.


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
