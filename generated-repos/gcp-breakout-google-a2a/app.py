"""Cloud Run v2 HTTP Service Entrypoint & Executive Light-Theme Sandbox for gcp-mcp-zero-bloat-gateway."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from src.engine import ZeroBloatMcpOboGateway


ENGINE = ZeroBloatMcpOboGateway()

DEMO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Zero-Bloat MCP Gateway: Dynamic Top-K Tool Search + RFC 8693 OAuth 2.1 On-Behalf-Of Security — Live Comparison Sandbox</title>
  <style>
    body { margin: 0; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; background: #f8fafc; color: #0f172a; }
    .wrap { width: 100%; box-sizing: border-box; padding: 24px clamp(16px, 2vw, 32px); }
    .hdr { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; gap: 16px; }
    .badge { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 999px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; }
    .card.bad { border-top: 4px solid #e11d48; }
    .card.good { border-top: 4px solid #059669; }
    .kpi { font-size: 28px; font-weight: 800; margin: 8px 0; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
    .bar { display: flex; gap: 10px; margin-bottom: 20px; }
    input { flex: 1; padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; background: #ffffff; color: #0f172a; }
    button { background: #2563eb; color: #ffffff; border: none; border-radius: 8px; padding: 10px 18px; font-weight: 700; cursor: pointer; }
    pre { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; font-size: 12px; overflow-x: auto; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hdr">
      <div>
        <span class="badge">MINT-01 · Vertex AI locations/global · Gemini 4 Argon + 3.8 Flash</span>
        <h1 style="margin:8px 0 4px;font-size:22px;">Zero-Bloat MCP Gateway: Dynamic Top-K Tool Search + RFC 8693 OAuth 2.1 On-Behalf-Of Security</h1>
        <div style="color:#475569;font-size:14px;">Interactive Naive Baseline vs. Engineered Google Cloud ADK Harness</div>
      </div>
    </div>
    <div class="bar">
      <input id="q" value="Correlate Q3 P1 latency incidents with regional BigQuery spend spikes" />
      <button onclick="runCompare()">Run Live Benchmark</button>
    </div>
    <div class="grid" id="cards"></div>
    <div class="card" style="margin-top:20px;">
      <h3 style="margin-top:0;">Cryptographic Receipt & Telemetry Payload</h3>
      <pre id="raw">Loading...</pre>
    </div>
  </div>
  <script>
    async function runCompare() {
      const q = document.getElementById('q').value;
      const res = await fetch('/api/compare?q=' + encodeURIComponent(q));
      const d = await res.json();
      const n = d.naive_baseline, e = d.engineered_harness;
      document.getElementById('cards').innerHTML = `
        <div class="card bad">
          <div style="color:#be123c;font-weight:800;font-size:12px;">NAIVE BASELINE (ANTI-PATTERN)</div>
          <div class="kpi" style="color:#e11d48;">${n.schema_tokens_per_turn.toLocaleString()} tok / turn</div>
          <div class="row"><span>Architecture</span><strong>${n.architecture}</strong></div>
          <div class="row"><span>Injected Schemas</span><strong>${n.selected_tools_injected} static tools</strong></div>
          <div class="row"><span>L1 Prefix Cache Hit</span><strong>${n.prefix_cache_hit_pct}%</strong></div>
          <div class="row"><span>Auth Posture</span><strong>${n.auth_posture}</strong></div>
          <div class="row"><span>p95 Latency</span><strong>${n.p95_latency_ms} ms</strong></div>
        </div>
        <div class="card good">
          <div style="color:#047857;font-weight:800;font-size:12px;">ENGINEERED HARNESS (VERIFIED PASS)</div>
          <div class="kpi" style="color:#059669;">${e.schema_tokens_per_turn.toLocaleString()} tok / turn (-${d.deltas.token_bloat_reduction_pct}%)</div>
          <div class="row"><span>Architecture</span><strong>${e.architecture}</strong></div>
          <div class="row"><span>Injected Schemas</span><strong>${e.selected_tools_injected} Top-K slim tools</strong></div>
          <div class="row"><span>L1 Prefix Cache Hit</span><strong>${e.prefix_cache_hit_pct}%</strong></div>
          <div class="row"><span>Auth Posture</span><strong>${e.auth_posture}</strong></div>
          <div class="row"><span>p95 Latency</span><strong>${e.p95_latency_ms} ms (${d.deltas.latency_speedup_x}x faster)</strong></div>
        </div>`;
      document.getElementById('raw').textContent = JSON.stringify(d, null, 2);
    }
    runCompare();
  </script>
</body>
</html>"""


class AgentServiceHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status_code: int, html_body: str) -> None:
        body = html_body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/healthz"):
            self._send_json(
                200,
                {
                    "status": "HEALTHY",
                    "post_id": ENGINE.POST_ID,
                    "repo_slug": ENGINE.REPO_SLUG,
                    "source_urn": ENGINE.SOURCE_URN,
                    "demo_url": "/demo",
                    "vertex_config": ENGINE.config.validate(),
                    "metrics": ENGINE.METRICS,
                },
            )
            return
        if parsed.path == "/demo":
            self._send_html(200, DEMO_HTML)
            return
        if parsed.path == "/api/compare":
            qs = parse_qs(parsed.query)
            q = (qs.get("q") or ["Correlate Q3 P1 latency incidents with regional BigQuery spend spikes"])[0]
            self._send_json(200, ENGINE.compare_naive_vs_engineered(q))
            return
        if parsed.path == "/api/run-demo":
            result = ENGINE.execute_scoped_mcp_turn("Execute verified Google Cloud ADK + OpenHands workflow")
            self._send_json(200, result)
            return
        self._send_json(404, {"error": "Not Found"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), AgentServiceHandler)
    print(f"[gcp-mcp-zero-bloat-gateway] Listening on http://0.0.0.0:{port} (Sandbox UI: /demo)...")
    server.serve_forever()
