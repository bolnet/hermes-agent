# money-stories — weekly review

Analyse and report. Full autonomy: change what the numbers tell you to change,
then say what you changed. Never ask.

**Autonomy is bounded.** Read `tasks/PERMISSION-BOUNDARY.md` and stay inside
it. The review's north star is monetization: judge the week's output by
whether research depth and content quality moved the channel toward #1 in its
space and toward earning.

    workdir  /Users/aarjay/projects/hermes-platform/workspace
    python   .venv/bin/python
    profile  money-stories
    boundary /Users/aarjay/projects/hermes-platform/tasks/PERMISSION-BOUNDARY.md

This is the counterweight to the daily task. The daily one produces; this one is
the only thing that decides whether producing that way is still right. A week of
output nobody measured is a week of guessing.

## 1. Pull the numbers

    .venv/bin/python pipeline/public_stats.py
    .venv/bin/python pipeline/retention_loop.py --days 28
    .venv/bin/python pipeline/audience_audit.py --profile money-stories

Three rules, each learned by getting it wrong:

- **Judge on views/day, not raw views.** Raw views mostly measure how long
  something has been up. Compute the rate in Python — never in your head.
- **A missing measurement is not a zero.** Retention rows returning `error`
  with an empty note, or `None` from a scrape, mean *unknown*. Report them as
  unknown. The Analytics API answers the wrong account with an empty 200, not
  an error, which is why `retention_loop.py` asserts the channel id first.
- **A number is not its meaning.** Say what you measured and what you think it
  means as two separate claims, so the second can be wrong without corrupting
  the first.

## 2. Answer the open question

The channel is running a format comparison and it is not yet settled:

    StoryCard 9s   v15, v16
    narrated ~45s  v04, v06, v14, v17
    UGC 30s        v16

v15 is the outlier — it accelerated in its second day rather than decaying,
which is the signature of algorithmic pickup rather than a launch spike. It
tells the SAME story as v14, so "the StoryCard format works" and "the Winklevoss
story works" are both still consistent with the data. **v17 is the control
test**: same narrated format, unrelated story. Read it against v14 and v04.

State which hypothesis this week's numbers support, or state plainly that they
still do not separate. "Not yet distinguishable" is a real answer; a confident
answer from indistinguishable data is not.

## 3. Act on it

Change something in the repo, not just in the report:

- Rebalance pillar shares in `profiles/money-stories/strategy.yaml` if a pillar
  is consistently under-performing. Shares must sum to 1.0 — assert it in
  Python, do not eyeball it.
- If a format has clearly won, say so and make it the default in the daily
  brief at `tasks/money-stories-daily.md`.
- If a defect cost time this week, fix it and commit. Conventional commits, no
  attribution footer.

You may also edit your own schedule with the cronjob tool — if daily production
is outrunning what the numbers can justify, slow it down and say why.

## 4. Known open defects — check whether they still bite

- Retention returns `status: "error"` with an **empty note** for several videos,
  including the ones the format comparison most needs. The empty note is the
  bug: it makes the failure undiagnosable. Fixing that diagnostic is worth more
  than any single video.
- `public_stats.py` sometimes disagrees with Studio by more than 3x. The public
  page is the one published by YouTube; trust it.

## The report

Lead with the single most decision-relevant number, not a table. Then: what
changed in the repo this week, what the format comparison now says, and what is
still unknown and why.

If there is genuinely nothing new — no new videos, no movement — reply exactly
`[SILENT]` and nothing else.

## RUN-OUTCOME — the last line of your report, always

End the report with exactly one of these, on its own line:

    RUN-OUTCOME: OK        everything this brief asked for actually happened
    RUN-OUTCOME: PARTIAL   some of it happened — say which, and which did not
    RUN-OUTCOME: BLOCKED   something stopped you — name it
    RUN-OUTCOME: FAILED    it went wrong

The scheduler reads this line and records the job as FAILED for anything other
than OK. Until 2026-08-18 it recorded the process outcome instead, so a run that
finished politely was `ok` — including one that published nothing behind a login
wall, one that produced four videos and published none, and one that uploaded to
another channel entirely. Three real failures, three green rows.

⚠️ **OK means the outcome, not the effort.** A careful run that was blocked is
BLOCKED. Nothing is lost by saying so — a blocked run that explains itself is
the most useful thing this system produces, and it is the only signal that
reaches the owner without them checking by hand.

