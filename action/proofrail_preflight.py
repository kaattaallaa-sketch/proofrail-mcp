import json
import os
import sys
import urllib.error
import urllib.request

endpoint = os.environ.get(
    "PROOFRAIL_PREFLIGHT_URL",
    "https://drkdm4jd-8767.uks1.devtunnels.ms/api/preflight",
)
target_url = os.environ["PROOFRAIL_TARGET_URL"]
declared = os.environ.get("PROOFRAIL_DECLARED_PROTOCOL_VERSION", "").strip()
fail_on_problem = os.environ.get("PROOFRAIL_FAIL_ON_PROBLEM", "false").lower() == "true"

payload = {"target_url": target_url, "check_profile": "basic"}
if declared:
    payload["declared_protocol_version"] = declared

request = urllib.request.Request(
    endpoint,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "github-actions-proofrail/1.0",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=25) as response:
        data = json.load(response)
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", errors="replace")
    print(f"ProofRail HTTP {exc.code}: {body}", file=sys.stderr)
    raise SystemExit(2)
except Exception as exc:
    print(f"ProofRail preflight request failed: {exc}", file=sys.stderr)
    raise SystemExit(2)

preflight = data.get("preflight", {})
connection = str(preflight.get("connection", "unknown"))
protocol_version = str(preflight.get("negotiated_protocol_version") or "")
tools_count = int(preflight.get("tools_count", 0) or 0)
schema_issues = int(preflight.get("schema_issues", 0) or 0)
compact = json.dumps(data, separators=(",", ":"))

outputs = {
    "connection": connection,
    "protocol_version": protocol_version,
    "tools_count": str(tools_count),
    "schema_issues": str(schema_issues),
    "response_json": compact,
}
output_path = os.environ.get("GITHUB_OUTPUT")
if output_path:
    with open(output_path, "a", encoding="utf-8") as handle:
        for key, value in outputs.items():
            handle.write(f"{key}={value}\n")

print(
    f"ProofRail preflight: connection={connection} "
    f"protocol={protocol_version or 'unknown'} tools={tools_count} "
    f"schema_issues={schema_issues}"
)

if fail_on_problem and (connection != "ok" or schema_issues > 0):
    print("Preflight problem detected; failing because fail_on_problem=true.", file=sys.stderr)
    raise SystemExit(1)
