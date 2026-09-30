# ProofRail MCP

**MCP server verification, testing, evaluation, and compatibility preflight before deployment.**

Use ProofRail before deploying, upgrading, or trusting an MCP server. It checks protocol negotiation, `tools/list`, tool schemas, Streamable HTTP transport, authentication classification, and optional server-configured safe fixtures. It returns **PASS**, **FAIL**, or **PARTIAL** with deterministic evidence.

## Public landing page

https://kaattaallaa-sketch.github.io/proofrail-mcp/

## Connect

- Free HTTP preflight: `POST https://drkdm4jd-8767.uks1.devtunnels.ms/api/preflight`
- MCP Streamable HTTP: `https://drkdm4jd-8767.uks1.devtunnels.ms/mcp`
- A2A Agent Card: `https://drkdm4jd-8767.uks1.devtunnels.ms/.well-known/agent-card.json`
- A2A JSON-RPC: `https://drkdm4jd-8767.uks1.devtunnels.ms/a2a`
- A2A HTTP+JSON: `https://drkdm4jd-8767.uks1.devtunnels.ms/a2a-rest`
- HTTP API: `https://drkdm4jd-8767.uks1.devtunnels.ms/api/certify`
- OpenAPI: `https://drkdm4jd-8767.uks1.devtunnels.ms/openapi.json`
- x402 discovery: `https://drkdm4jd-8767.uks1.devtunnels.ms/.well-known/x402`
- ARD catalog: `https://drkdm4jd-8767.uks1.devtunnels.ms/.well-known/ard.json`

## MCP Radar

ProofRail maintains an autonomous read-only index of public MCP endpoints discovered independently from multiple public sources, currently including the official MCP Registry and public GitHub `server.json` manifests.

- HTTP snapshot: `GET https://drkdm4jd-8767.uks1.devtunnels.ms/api/radar`
- HTTP changes: `GET https://drkdm4jd-8767.uks1.devtunnels.ms/api/radar/changes`
- MCP tools: `mcp_radar_snapshot` and `mcp_radar_changes`
- Snapshot filters include `outcome`, `connection`, `source`, `tool_contains`, `min_tools`, and `limit`.
- Radar sweeps refresh automatically; reading the snapshot or changes never triggers a live scan.
- Change tracking covers new/not-seen endpoints plus outcome, connection, protocol, tool-count, tool-name, and schema changes.
- Results are point-in-time compatibility observations, not a security audit or uptime guarantee.

## MCP tools

- `health` — free service health
- `mcp_radar_snapshot` — free cached autonomous MCP Radar snapshot with capability filters
- `mcp_radar_changes` — free changes observed between the latest Radar sweeps
- `proofrail_info` — free capability description
- `mcp_release_preflight` — free endpoint preflight; no payment
- `quote_certification` — free network/price quote
- `mcp_release_certify` — x402-paid compatibility certification

## GitHub Actions: preflight before deploy

Coding agents and CI jobs can run the free preflight when they already have a concrete MCP URL:

```yaml
- name: ProofRail MCP preflight
  id: proofrail
  uses: kaattaallaa-sketch/proofrail-mcp@v1
  with:
    target_url: ${{ vars.MCP_URL }}
    fail_on_problem: "true"
```

Outputs: `connection`, `protocol_version`, `tools_count`, `schema_issues`, and `response_json`.

With `fail_on_problem: "true"`, the Action blocks on connection problems, schema issues, incomplete evidence, non-PASS verdicts, or a mismatch with `declared_protocol_version`. The protocol comparison also works against earlier preflight responses. Without enforcement, it is advisory.

The endpoint must already be reachable (for example, a staging deployment) before this check runs. A manifest URL alone does not test code that has not been deployed.

Scope: this is a basic external endpoint check using a client that supports negotiated MCP revisions through 2025-11-25. It is not full MCP conformance, a security audit, or a guarantee that every MCP client will accept the server. The official [MCP conformance framework](https://github.com/modelcontextprotocol/conformance) is available for broader protocol testing.

This action uses the free no-payment preflight. The x402-paid `mcp_release_certify` operation remains a separate optional step for a deterministic PASS/FAIL/PARTIAL evidence receipt.

## Discovery

ProofRail is distributed through:

- Official MCP Registry: `io.github.kaattaallaa-sketch/proofrail`
- PayAI Bazaar
- Ultravioleta DAO Bazaar aggregation
- Wellknown verified MCP record: https://wellknown.network/agents/proofrail
- Wellknown verified A2A record: https://wellknown.network/agents/proofrail-access-agent
- OpenAPI 3.1, RFC 9727 API Catalog, ARD 0.9, Server Card, `llms.txt`, JSON-LD and crawler metadata

## Current validation stage

The free preflight requires no payment. Full certification currently advertises **$0.10 USDC on Base mainnet** through x402. The payment path has been technically preflighted without sending a transaction; no completed external sale or settlement has been confirmed yet.

The production ProofRail service code is **not** published in this repository. This repository contains public discovery metadata, the reusable preflight GitHub Action, the static discovery landing page, and the automated MCP Registry publication workflow.
