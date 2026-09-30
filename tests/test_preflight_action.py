import contextlib
import io
import json
import os
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "action" / "proofrail_preflight.py"

def run_action(preflight, declared="", enforce=True):
    env = {"PROOFRAIL_TARGET_URL": "https://example.com/mcp", "PROOFRAIL_DECLARED_PROTOCOL_VERSION": declared,
           "PROOFRAIL_FAIL_ON_PROBLEM": str(enforce).lower()}
    with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps({"preflight": preflight}).encode())), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            runpy.run_path(str(SCRIPT), run_name="__main__")
            return 0
        except SystemExit as exc:
            return exc.code

class ReleaseGateTests(unittest.TestCase):
    def test_blocks_declared_protocol_mismatch_on_legacy_backend(self):
        self.assertEqual(run_action({"connection":"ok","negotiated_protocol_version":"2025-11-25","tools_count":1,"schema_issues":0}, "2024-11-05"),1)
    def test_blocks_incomplete_schema_evidence(self):
        self.assertEqual(run_action({"connection":"ok","tools_count":None,"schema_issues":None}),1)
    def test_blocks_partial_outcome(self):
        self.assertEqual(run_action({"outcome":"PARTIAL","connection":"ok","tools_count":1,"schema_issues":0}),1)
    def test_accepts_healthy_result(self):
        self.assertEqual(run_action({"outcome":"PASS","connection":"ok","tools_count":1,"schema_issues":0}),0)
    def test_advisory_mode_reports_without_blocking(self):
        self.assertEqual(run_action({"outcome":"FAIL","connection":"ok","tools_count":1,"schema_issues":2},enforce=False),0)

    def test_real_github_action_identifies_repository_and_run(self):
        captured = {}
        def fake_urlopen(request, timeout=0):
            captured["user_agent"] = request.get_header("User-agent")
            return io.BytesIO(json.dumps({"preflight": {"outcome":"PASS","connection":"ok","tools_count":1,"schema_issues":0}}).encode())
        env = {
            "PROOFRAIL_TARGET_URL": "https://example.com/mcp",
            "PROOFRAIL_DECLARED_PROTOCOL_VERSION": "",
            "PROOFRAIL_FAIL_ON_PROBLEM": "true",
            "GITHUB_ACTIONS": "true",
            "GITHUB_REPOSITORY": "owner/repo",
            "GITHUB_RUN_ID": "12345",
        }
        with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", side_effect=fake_urlopen), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(captured["user_agent"], "github-actions-proofrail/1.1 repo=owner/repo run=12345")

    def test_non_github_execution_is_marked_internal(self):
        captured = {}
        def fake_urlopen(request, timeout=0):
            captured["user_agent"] = request.get_header("User-agent")
            return io.BytesIO(json.dumps({"preflight": {"outcome":"PASS","connection":"ok","tools_count":1,"schema_issues":0}}).encode())
        env = {
            "PROOFRAIL_TARGET_URL": "https://example.com/mcp",
            "PROOFRAIL_DECLARED_PROTOCOL_VERSION": "",
            "PROOFRAIL_FAIL_ON_PROBLEM": "true",
        }
        with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", side_effect=fake_urlopen), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(captured["user_agent"], "proofrail-internal-action-test/1.1")

if __name__ == "__main__":
    unittest.main()
