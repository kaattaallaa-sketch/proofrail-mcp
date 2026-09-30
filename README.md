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

## MCP tools

- `health` — free service health
- `proofrail_info` — free capability description
- `mcp_release_preflight` — free endpoint preflight; no payment
- `quote_certification` — free network/price quote
- `mcp_release_certify` — x402-paid compatibility certification

## GitHub Actions: preflight before deploy

Coding agents and CI jobs can run the free preflight when they already have a concrete MCP URL:

```yaml
- name: ProofRail MCP preflight
  id: proofrail
  uses: kaattaallaa-sketch/proofrail-mcp@main
  with:
    target_url: ${{ vars.MCP_URL }}
    fail_on_problem: "true"
```

Outputs: `connection`, `protocol_version`, `tools_count`, `schema_issues`, and `response_json`.

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

Gate 1 runs on **Base Sepolia** at **$0.001 test-USDC**. Testnet payments are validation, not revenue. Base mainnet remains disabled.

The production ProofRail service code is **not** published in this repository. This repository contains only public discovery metadata, the static discovery landing page, and the automated MCP Registry publication workflow.
