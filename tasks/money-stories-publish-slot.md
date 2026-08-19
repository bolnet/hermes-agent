# money-stories — publish one queued video

You publish **exactly one** already-rendered video and stop. You do not
research, script, render, or pick anything. The daily run at 14:35 did all of
that and left a queue behind; your entire job is to take the next one from it.

**Full autonomy inside that scope — never ask permission.** A question at the
end of this run is a failure: nothing else fires this slot, so a run that stops
to ask leaves a finished video unpublished.

    workdir   /Users/aarjay/projects/hermes-platform/workspace
    python    .venv/bin/python           (always this, never system python3)
    profile   money-stories              (export HERMES_PROFILE=money-stories)
    queue     profiles/money-stories/state/publish-queue.json
    boundary  /Users/aarjay/projects/hermes-platform/tasks/PERMISSION-BOUNDARY.md

**Why this task exists separately from the daily run.** `upload.py` publishes
the instant it is invoked and has no scheduling flag, so four videos at four
different times needs four separate fires. The owner requires the stagger
(2026-08-17, "in diffrent time") so that four of our own videos do not compete
for one distribution window on the same day — which is the one way the format
test could lose to itself. It is **not** a platform limit; the research on
2026-08-17 found no documented per-day cap on any of the three platforms.

## 1. Ask the queue what is due

    .venv/bin/python pipeline/publish_queue.py \
        --path profiles/money-stories/state/publish-queue.json --next

    exit 0   the slug is on stdout — that is your video
    exit 1   nothing due. STOP, report "nothing due", do not improvise
    exit 3   the queue is unusable. STOP and say so plainly

**Exit 1 is a normal outcome, not a failure.** It means the daily run produced
fewer than four videos, or an earlier slot already took this one. Do not go
looking for something else to publish, and do not re-render anything.

The queue **catches up rather than skipping**: if the 17:05 fire never
happened, the 19:35 fire gets 17:05's video. That is deliberate — publishing
late beats silently dropping a video that already cost a render. So the slug
you get may not be the one nominally assigned to this hour. Publish what you
are given.

## 2. Confirm the render exists before touching a browser

    ls -la profiles/money-stories/out/<slug>.mp4
    ffmpeg -i profiles/money-stories/out/<slug>.mp4 -af volumedetect -f null - 2>&1 | grep volume

Expect `mean_volume` near -20 dB. **Below -60 dB is digital silence** — a card
once shipped at -91 dB with every check green, because a file existing and
having an audio stream are both true of silence. If it is silent, do NOT
publish: mark nothing, report the defect, and leave the entry due so it can be
fixed and picked up later.

## 3. Publish — all three platforms

    .venv/bin/python pipeline/run_state.py \
        --path profiles/money-stories/state/run-<UTC stamp>.json \
        --init <UTC stamp> --profile money-stories --task shorts \
        --set video=<slug>

    HERMES_PROFILE=money-stories .venv/bin/python pipeline/upload.py \
        profiles/money-stories/out/<slug>.mp4 IGNORED \
        scripts/desc/<slug>.txt --state <state file>

**Set the title INSIDE the state file with Python, never via `--set
title=...`.** `$` in a title dies in the shell — it once published a video as
*"Quibi Raised .75B"* and later silently lost "$139" from v18's headline.

**If a platform session is logged out, STOP for that platform only** — record
it and move on; the other two still land. Never handle credentials and never
attempt to log in.

Close every open browser tab first, publish everywhere else, then switch Google
account and do **YouTube last**. House order for every profile.

## 4. Verify, then mark the queue

    .venv/bin/python pipeline/publish_verify.py <youtube_video_id>

Exit 0 = publicly resolvable. **A draft gets a URL too**, and one was once
recorded as published behind a link no viewer could open. Shorts can take ~2
minutes to resolve; if it says not_public, wait and check once more.

Then append the ledger line (`automation/logs/production.jsonl`) exactly as
`money-stories-daily.md` step 7 specifies, including the `format` field, and
verify it landed:

    grep -c "<slug>" automation/logs/production.jsonl    # must be 1

**Only then mark the queue** — and only if something actually published:

    .venv/bin/python pipeline/publish_queue.py \
        --path profiles/money-stories/state/publish-queue.json --mark <slug>

Order matters. Marking before verifying would retire a video that never went
live, and nothing downstream would ever notice: the next slot would move on to
the following video and this one would be lost silently. If all three platforms
failed, leave it unmarked so a later slot retries it.

Marking is idempotent, so a retry after a timeout is safe.

## Report

One short paragraph: which slug, why it was due (assigned slot vs caught up),
per-platform verified true/false with URLs, whether the ledger line landed, and
whether you marked the queue. If you did not mark it, say why in one sentence.

Record what you VERIFIED, never what you believe succeeded.

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

