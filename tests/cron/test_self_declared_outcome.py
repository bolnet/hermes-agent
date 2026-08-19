"""A run that FINISHED is not a run that SUCCEEDED.

`last_status` recorded the agent's process outcome, so any run that returned
without raising was `ok`. On 2026-08-18 that covered three real failures in one
day:

    surendra       published nothing — LinkedIn phone checkpoint      -> ok
    money-stories  produced four videos, published zero               -> ok
    board-order    uploaded its video to ANOTHER TENANT'S CHANNEL     -> ok

The owner found the third by eye. An agent cannot signal failure through an exit
code — it is a conversation, not a command, and it ends politely whatever
happened — so it declares the outcome and the scheduler believes the declaration
over the fact that the process ended.
"""

import re
import unittest
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
SCHEDULER = ROOT / "cron" / "scheduler.py"


def _load_detector():
    """Exec just the detector, so the test does not import the whole gateway."""
    src = SCHEDULER.read_text()
    start = src.index("_RUN_OUTCOME_RE = re.compile(")
    end = src.index("def run_one_job(")
    namespace = {"re": re, "Optional": Optional}
    exec(src[start:end], namespace)          # noqa: S102 - reading our own source
    return namespace["_self_declared_failure"]


declared = _load_detector()


class TestSelfDeclaredOutcome(unittest.TestCase):
    def test_blocked_is_a_failure(self):
        self.assertIn("BLOCKED", declared(
            "RUN-OUTCOME: BLOCKED LinkedIn phone checkpoint"))

    def test_failed_and_partial_are_failures(self):
        self.assertIn("FAILED", declared("RUN-OUTCOME: FAILED published nothing"))
        self.assertIn("PARTIAL", declared("RUN-OUTCOME: PARTIAL 2 of 4 published"))

    def test_clean_run_is_left_alone(self):
        self.assertIsNone(declared("All four videos published successfully."))
        self.assertIsNone(declared(""))
        self.assertIsNone(declared(None))

    def test_a_run_cannot_upgrade_itself(self):
        """One-directional by design.

        A run may mark itself worse, never better. An agent asserting success is
        precisely the claim that was never trustworthy — `ok` has to be earned
        by the absence of a declared failure, not by declaring victory.
        """
        self.assertIsNone(declared("RUN-OUTCOME: OK everything fine"))
        self.assertIsNone(declared("RUN-OUTCOME: SUCCESS all good"))

    def test_a_mid_line_mention_does_not_count(self):
        """The briefs DESCRIBE this marker, so prose about it must not match.

        The marker is anchored to the start of a line for exactly this reason:
        every brief now contains the words RUN-OUTCOME: BLOCKED as instructions,
        and a run that quotes its own brief would otherwise mark itself failed.
        """
        self.assertIsNone(declared(
            "The brief says to emit RUN-OUTCOME: BLOCKED when blocked."))
        self.assertIsNone(declared(
            "I considered whether this was RUN-OUTCOME: FAILED but it was not."))

    def test_markdown_around_the_marker_still_matches(self):
        """Agents write reports in markdown; bold and bullets are normal."""
        self.assertIn("BLOCKED", declared("**RUN-OUTCOME: BLOCKED** xurl unregistered"))
        self.assertIn("PARTIAL", declared("  - RUN-OUTCOME: PARTIAL 2 of 4"))

    def test_markdown_does_not_bleed_into_the_reason(self):
        self.assertNotIn("*", declared("**RUN-OUTCOME: BLOCKED** xurl unregistered"))

    def test_case_insensitive(self):
        self.assertIsNotNone(declared("run-outcome: blocked lowercase"))

    def test_first_marker_wins_over_later_prose(self):
        self.assertIn("BLOCKED", declared(
            "RUN-OUTCOME: BLOCKED no session\n\nnotes about RUN-OUTCOME: OK"))


class TestEveryBriefAsksForIt(unittest.TestCase):
    def test_all_task_briefs_require_the_marker(self):
        """A detector nothing emits is dead code.

        Every scheduled job's brief has to ask for the line, or that job keeps
        reporting ok whatever happens.
        """
        briefs = sorted((ROOT / "tasks").glob("*.md"))
        self.assertTrue(briefs, "no task briefs found")
        missing = [b.name for b in briefs
                   if "RUN-OUTCOME" not in b.read_text()
                   and b.name != "PERMISSION-BOUNDARY.md"]
        self.assertEqual(missing, [], f"briefs with no RUN-OUTCOME section: {missing}")


if __name__ == "__main__":
    unittest.main()
