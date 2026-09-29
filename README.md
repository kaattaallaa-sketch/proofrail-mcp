# ProofRail

ProofRail is a public MCP release preflight service for AI agents.

Use it **before deploying, upgrading, or trusting an MCP server**. It checks protocol negotiation, `tools/list`, tool schemas, Streamable HTTP transport, authentication classification, and optional server-configured safe fixtures.

## Connect

- MCP Streamable HTTP: `https://drkdm4jd-8767.uks1.devtunnels.ms/mcp`
- HTTP API: `https://drkdm4jd-8767.uks1.devtunnels.ms/api/certify`
- OpenAPI: `https://drkdm4jd-8767.uks1.devtunnels.ms/openapi.json`
- x402 discovery: `https://drkdm4jd-8767.uks1.devtunnels.ms/.well-known/x402`
- MCP Server Card: `https://drkdm4jd-8767.uks1.devtunnels.ms/mcp/server-card`
- AI Catalog: `https://drkdm4jd-8767.uks1.devtunnels.ms/.well-known/ai-catalog.json`

## MCP tools

- `health` — free service health.
- `proofrail_info` — free service description.
- `quote_certification` — free price quote.
- `mcp_release_certify` — x402-paid compatibility certification.

## Current validation stage

ProofRail is currently in Gate 1 on **Base Sepolia** using **test-USDC**. Payments are testnet validation and are not revenue.

The production service code is not published in this repository. This repository contains only public discovery metadata and the automated MCP Registry publication workflow.

## Discovery

ProofRail publishes machine-readable metadata for:

- Official MCP Registry (`server.json`)
- MCP Streamable HTTP
- OpenAPI 3.1
- x402 / Bazaar
- x402scan-compatible discovery
- experimental MCP Server Card + AI Catalog
- `llms.txt`

The service returns PASS, FAIL, or PARTIAL with a deterministic evidence receipt.
