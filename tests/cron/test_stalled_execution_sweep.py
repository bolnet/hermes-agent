"""An execution that never reports must not sit 'running' forever.

`recover_interrupted_executions()` only reclaims an execution whose OWNER
PROCESS has exited. That covers a scheduler restart and misses the case that
actually happened on 2026-08-19: the gateway stayed alive and the agent
subprocess died under it. board-order-study ran for eleven minutes, examined
five videos, wrote nothing, and its row stayed 'running' with the job reporting
no status at all.

Invisible is worse than red. A failed job prompts someone to look; a job with no
status looks like a job that has not run yet.
"""

import sqlite3
import sys
import unittest
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from cron import executions                                 # noqa: E402


class TestStalledSweep(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        executions._initialize_schema(self.conn)
        self.now = executions._hermes_now()

    def tearDown(self):
        self.conn.close()

    def _insert(self, execution_id: str, *, hours_ago: float, status: str = "running"):
        claimed = (self.now - timedelta(hours=hours_ago)).isoformat()
        self.conn.execute(
            "INSERT INTO executions (id, job_id, source, status, claimed_at, "
            "process_id, pid) VALUES (?,?,?,?,?,?,?)",
            (execution_id, "job-1", "builtin", status, claimed, "proc-x", 999999),
        )

    def _status(self, execution_id: str) -> str:
        return self.conn.execute(
            "SELECT status FROM executions WHERE id=?", (execution_id,)
        ).fetchone()["status"]

    def test_a_run_stuck_past_the_bound_is_closed_out(self):
        self._insert("stale", hours_ago=executions.MAX_EXECUTION_HOURS + 1)
        swept = executions._sweep_stalled_executions(self.conn, self.now.isoformat())
        self.assertEqual(len(swept), 1)
        self.assertEqual(self._status("stale"), "unknown")

    def test_a_healthy_long_run_is_left_alone(self):
        """money-stories produces four videos and legitimately runs ~an hour.

        The bound is a backstop for runs that are never coming back, not a
        runtime budget — killing a working publish mid-upload would be worse
        than the bug being fixed.
        """
        self._insert("healthy", hours_ago=1)
        swept = executions._sweep_stalled_executions(self.conn, self.now.isoformat())
        self.assertEqual(swept, [])
        self.assertEqual(self._status("healthy"), "running")

    def test_claimed_but_never_started_is_also_swept(self):
        """A run that died between claiming and starting leaves 'claimed'."""
        self._insert("never-started",
                     hours_ago=executions.MAX_EXECUTION_HOURS + 1, status="claimed")
        executions._sweep_stalled_executions(self.conn, self.now.isoformat())
        self.assertEqual(self._status("never-started"), "unknown")

    def test_already_finished_rows_are_untouched(self):
        for status in ("completed", "failed", "unknown"):
            with self.subTest(status=status):
                self._insert(f"done-{status}",
                             hours_ago=executions.MAX_EXECUTION_HOURS + 5,
                             status=status)
                executions._sweep_stalled_executions(self.conn, self.now.isoformat())
                self.assertEqual(self._status(f"done-{status}"), status)

    def test_marked_unknown_rather_than_failed(self):
        """'failed' would assert nothing happened. We cannot know that.

        A study run that dies writes nothing, but a PUBLISH run that dies may
        already have posted. 'unknown' is the honest status and matches what the
        owner-exited path already records.
        """
        self._insert("stale", hours_ago=executions.MAX_EXECUTION_HOURS + 1)
        executions._sweep_stalled_executions(self.conn, self.now.isoformat())
        row = self.conn.execute(
            "SELECT status, error FROM executions WHERE id=?", ("stale",)).fetchone()
        self.assertEqual(row["status"], "unknown")
        self.assertIn("side effects", row["error"])
        self.assertNotEqual(row["status"], "failed")

    def test_the_bound_is_generous_enough_for_real_work(self):
        self.assertGreaterEqual(
            executions.MAX_EXECUTION_HOURS, 2,
            "too tight — this would reap healthy multi-video production runs")


if __name__ == "__main__":
    unittest.main()
