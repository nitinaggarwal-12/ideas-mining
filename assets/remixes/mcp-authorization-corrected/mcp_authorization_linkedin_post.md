# Your AI Agent Has Access to Your Tools. Who Governs Every Call? (Corrected Enterprise MCP Authorization Blueprint)

Connecting an AI Agent to GitHub, Gmail, or Jira without OAuth 2.1 authorization turns a productivity demo into an enterprise security incident.

The updated **MCP Authorization specification (`2025-11-25`)** cleanly separates the **MCP Server (OAuth Resource Server)** from the **Authorization Server** — and adds critical protections that many early tutorials miss.

Here is the complete **7-Phase, 16-Step Enterprise MCP Authorization Flow**:

1. **Challenge (`POST /mcp`)** -> Server responds `401` + `WWW-Authenticate: resource_metadata, scope`.
2. **Discover (`RFC 9728` + `RFC 8414`)** -> Client fetches `GET /.well-known/oauth-protected-resource` (notice the trailing `n`!) and Authorization Server metadata verifying mandatory `S256` PKCE support.
3. **Register** -> Resolve `client_id` in priority order: **Pre-registered > CIMD (Client ID Metadata Document) > DCR (legacy fallback)**.
4. **Authorize (`PKCE S256` + `state` + `iss`)** -> Browser sign-in with `resource` (RFC 8707), `state` (CSRF), `redirect_uri`, and `iss` (RFC 9207 mix-up protection).
5. **Token** -> Exchange authorization code + `code_verifier` + `redirect_uri` + `resource` for a short-lived, audience-bound `access_token` (`aud == this MCP server`).
6. **Call & Verify** -> Send `Authorization: Bearer <token>` + `MCP-Protocol-Version` + `Mcp-Session-Id`; server strictly validates signature, `exp`, `aud`, and `scope` (returning `403 insufficient_scope` for step-up consent).
7. **Upstream On-Behalf-Of (`RFC 8693 OBO`)** -> Never forward the client's raw MCP token upstream AND never share a single static server key across tenants (Confused-Deputy bypass). Exchange caller identity via **RFC 8693 OBO** (or a per-user Token Vault) before calling GitHub, Gmail, or Jira.

For headless/autonomous enterprise agents, pair this pattern with **Enterprise-Managed Authorization (`ID-JAG`: RFC 7523 + RFC 8693)** or scoped `client_credentials`.

Runnable Google Cloud ADK + FastMCP + IAM STS Reference Repo (`100`-trial evaluation harness & 24-slide architecture deck):
https://github.com/nitinaggarwal-12/ideas-mining/tree/main/generated-repos/gcp-mcp-zero-bloat-gateway

#MCP #ModelContextProtocol #AgenticAI #OAuth21 #ZeroTrust #GoogleCloud #VertexAI #CyberSecurity #AISecurity #EnterpriseAI
