# Install ProofRail in Cline

ProofRail is a hosted remote MCP server. Do not clone or run the private service code locally.

## MCP configuration

Add this entry to Cline's MCP settings:

```json
{
  "mcpServers": {
    "proofrail": {
      "type": "streamableHttp",
      "url": "https://drkdm4jd-8767.uks1.devtunnels.ms/mcp",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Then reconnect/reload MCP servers and verify that Cline can see these tools:

- `health`
- `proofrail_info`
- `quote_certification`
- `mcp_release_certify`

## What to call

Use `quote_certification` to inspect the payment network and price.

Use `mcp_release_certify` before deploying, upgrading, or trusting an MCP server. Required input:

```json
{
  "target_url": "https://example.com/mcp"
}
```

Optional inputs are `declared_protocol_version`, `check_profile` (currently `basic`), and a server-configured safe `fixture_id`.

## Payment safety

Gate 1 currently uses x402 V2 on **Base Sepolia** (`eip155:84532`) at **$0.001 test-USDC**.

This is testnet validation, not production revenue. Base mainnet is disabled.

If the MCP client does not support x402 payment metadata, it can still connect, list the free tools, and inspect the quote; the paid certification call will return its payment requirement instead of running for free.

## Public documentation

- Landing page: https://kaattaallaa-sketch.github.io/proofrail-mcp/
- Official MCP Registry: `io.github.kaattaallaa-sketch/proofrail`
- OpenAPI: https://drkdm4jd-8767.uks1.devtunnels.ms/openapi.json
- x402 discovery: https://drkdm4jd-8767.uks1.devtunnels.ms/.well-known/x402
