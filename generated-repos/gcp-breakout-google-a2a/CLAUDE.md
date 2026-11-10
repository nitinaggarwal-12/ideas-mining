# gcp-mcp-zero-bloat-gateway — Agent Constitution (AGENTS.md / GEMINI.md / CLAUDE.md)

- **Topic ID**: `MINT-01` (`urn:ietf:rfc:8693:mcp-zero-bloat-gateway-2026`)
- **Primary Source**: IETF RFC 8693 OAuth 2.0 Token Exchange + MCP Dynamic Tool Discovery Specification
- **Model Routing (Rule 55)**: Vertex AI `locations/global` (`ramp-portal-dev`), `gemini-4-argon` / `gemini-3.8-flash`, discrete `thinkingLevel='HIGH'`, `maxOutputTokens <= 32768`
- **Theme Invariant (Rule 54)**: Executive Light Theme (`#F8FAFC` / `#FFFFFF`) on `/demo`
- **Verification Commands**:
  - `python3 -m unittest discover -s tests -p 'test_*.py'`
  - `python3 demo_runner.py --compare`
