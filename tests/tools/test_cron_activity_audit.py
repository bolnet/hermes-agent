"""The 2026-08-17 permission boundary: cron commands are audited, and the
escalation commands from the incident are denied by the shipped config.

The deny rules themselves live in ``.hermes-home/config.yaml``
(``approvals.deny``); these tests pin the two code-level guarantees:

  * ``check_all_command_guards`` writes a JSONL record for every cron-context
    decision — approved or blocked — to ``logs/cron_activity.jsonl``.
  * an audit-write failure never changes the approval decision.
"""

import json
import os
from unittest.mock import patch

import pytest

from tools import approval


@pytest.fixture()
def cron_context(tmp_path, monkeypatch):
    """Simulate a cron approval context with an isolated HERMES_HOME."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    monkeypatch.setenv("HERMES_CRON_SESSION", "1")
    return tmp_path


def _audit_lines(home) -> list[dict]:
    path = os.path.join(str(home), "logs", "cron_activity.jsonl")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


class TestCronActivityAudit:
    def test_approved_command_is_audited(self, cron_context):
        result = approval.check_all_command_guards("git status", "local")
        assert result["approved"] is True
        records = _audit_lines(cron_context)
        assert len(records) == 1
        assert records[0]["command"] == "git status"
        assert records[0]["approved"] is True

    def test_denied_command_is_audited_with_rule(self, cron_context):
        with patch.object(
            approval, "_get_approval_config",
            return_value={"deny": ["*osascript*"]},
        ):
            result = approval.check_all_command_guards(
                'osascript -e \'tell application "Safari" to activate\'',
                "local",
            )
        assert result["approved"] is False
        records = _audit_lines(cron_context)
        assert len(records) == 1
        assert records[0]["approved"] is False
        assert records[0]["rule"] == "user_deny"

    def test_non_cron_context_is_not_audited(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HERMES_HOME", str(tmp_path))
        monkeypatch.delenv("HERMES_CRON_SESSION", raising=False)
        approval.check_all_command_guards("git status", "local")
        assert _audit_lines(tmp_path) == []

    def test_audit_failure_never_blocks_the_command(self, cron_context):
        with patch.object(approval, "_audit_cron_command",
                          side_effect=RuntimeError("disk full")):
            with pytest.raises(RuntimeError):
                # Direct call raises — confirms the patch target is live.
                approval._audit_cron_command("x", {})
        # The wrapper itself must swallow audit errors: patch open() to fail.
        with patch("builtins.open", side_effect=OSError("disk full")):
            result = approval.check_all_command_guards("git status", "local")
        assert result["approved"] is True
