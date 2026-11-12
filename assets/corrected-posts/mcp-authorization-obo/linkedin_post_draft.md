Your AI agent can call GitHub, Gmail, and Jira. Without OAuth 2.1 audience binding and On-Behalf-Of delegation, one leaked tool call compromises every downstream API.

Here is the production MCP authorization flow, cleanly updated for real-world enterprise deployments:

1. Challenge (401 + WWW-Authenticate)
Calling POST /mcp without a bearer token triggers a standard HTTP 401 challenge pointing to resource metadata.

2. Discover (RFC 9728 + RFC 8414)
The client fetches GET /.well-known/oauth-protected-resource (RFC 9728) to discover authorization_servers and scopes_supported, then resolves the IdP via RFC 8414 / OIDC discovery (issuer, endpoints, JWKS).

3. Client Registration (Pre-reg > CIMD > DCR)
Use pre-registered client_id or HTTPS Client ID Metadata Documents (CIMD) first; reserve Dynamic Client Registration (DCR) for legacy fallback.

4. Authorize (PKCE S256 + state + RFC 9207 iss)
Interactive desktop/IDE hosts run OAuth 2.1 with mandatory PKCE S256 and state; headless Cloud Run / backend agents use Workload Identity Federation (WIF) directly at Step 5 (/token). Callback validation checks both state and iss (RFC 9207) against RFC 8414 metadata to stop IdP mix-up attacks.

5. Audience-Bound Token (RFC 8707)
The client passes explicit resource= on /authorize and /token. The MCP server enforces aud matches its own server URI so sibling servers cannot replay tokens.

6. Execute, Step-Up (403) & RFC 8693 On-Behalf-Of (OBO)
Two rules keep downstream APIs safe from Confused-Deputy leaks:
→ Never forward the client MCP token downstream, AND never store a single shared static PAT / service key.
→ Exchange the MCP JWT via RFC 8693 Token Exchange (grant_type=urn:ietf:params:oauth:grant-type:token-exchange) for a short-lived (<=5m), narrow-scope API token carrying both sub (user) and act (MCP server), while gating mutating tool writes behind Human-in-the-Loop (HITL) approval.

Reference Google Cloud ADK + Zero-Bloat MCP Gateway implementation (Dynamic Tool Search + RFC 8693 OBO + Read=Auto / Write=HITL):
https://github.com/nitinaggarwal-12/ideas-mining/tree/main/generated-repos/gcp-mcp-zero-bloat-gateway

Which enterprise constraint breaks first in your MCP rollouts: Dynamic Client Registration (DCR) governance or RFC 8693 OBO delegation to legacy APIs?

@Google Cloud @Anthropic @Model Context Protocol
#MCP #ModelContextProtocol #OAuth2 #ZeroTrust #AgenticAI #AISecurity #CloudArchitecture #GoogleCloud #ADK
