# money-stories — weekly review

Analyse and report. Full autonomy: change what the numbers tell you to change,
then say what you changed. Never ask.

    workdir  /Users/aarjay/projects/agent-platform
    python   .venv/bin/python
    profile  money-stories

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
