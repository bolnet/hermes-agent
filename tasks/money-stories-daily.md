# money-stories — daily production

You own this channel end-to-end. Full autonomy: **never ask permission — produce,
check, and publish.** Report what you did and what you found. A question at the
end of a run is a failure of this task, not a courtesy: nothing else on this
machine schedules production any more, so a run that stops to ask produces
nothing that day.

    workdir   /Users/aarjay/projects/agent-platform
    python    .venv/bin/python           (always this, never system python3)
    profile   money-stories              (export HERMES_PROFILE=money-stories)

Every pipeline entry point refuses to guess a profile. Pass `--profile
money-stories` or export `HERMES_PROFILE`; a command that errors with "no profile
bound — refusing to default" is missing that, not broken.

## 1. Pick — never repeat a story

Read `profiles/money-stories/strategy.yaml` for pillar shares. Then check BOTH:

    ls scripts/json/                             # every script ever written
    .venv/bin/python pipeline/public_stats.py    # what is actually live

Three of last week's seven planned slugs collided with stories that already had
a script. Checking one list is not enough — a script can exist unpublished, and a
video can be published from a script since renamed.

Fact-check dates and figures with web search before writing. Never invent a
number.

## 2. Write the script JSON

Match an existing file's shape exactly — `scripts/json/v17-nokia-burning-platform.json`
is the current reference. ~140 words of narration (about 55s at 140wpm), 5 scenes,
beats hook/context/twist/payoff/cta, each with `headline`, `headline_accent`,
`image_prompt`, `clip_query`.

**No scene may hold longer than ~9 seconds.** v17 shipped a 15s motionless hold —
a third of the video on one frame. Split any beat that long into two.

`clip_query` is what actually reaches stock search; `image_prompt` never does.
Write the query for the *subject*, not the mood. "hands holding mobile phone
sunlight" returned a modern iPhone for a headline about Nokia's 2007 dominance.

## 3. Produce

    HERMES_PROFILE=money-stories .venv/bin/python pipeline/produce.py \
        scripts/json/<slug>.json --profile money-stories

Output lands in `profiles/money-stories/out/<slug>.mp4`. Not `render/out/` —
that path has been empty since renders moved into the profile workspace.

## 4. LOOK at the render. This is not optional.

Every silent failure this channel has shipped passed every numeric check.
A render that "succeeded" has proven nothing.

**a. Build a frame grid and actually view it:**

    for i in $(seq 0 23); do T=$(.venv/bin/python -c "print(round($i*1.85,2))"); \
      ffmpeg -v error -ss $T -i profiles/money-stories/out/<slug>.mp4 -frames:v 1 \
      -vf scale=250:-1 /tmp/fr/f$(printf %02d $i).png; done
    ffmpeg -v error -i /tmp/fr/f%02d.png -vf "tile=6x4:padding=4:color=white" \
      -frames:v 1 /tmp/fr/grid.png

Then open `/tmp/fr/grid.png` with your vision tool and read it. For each panel
ask: **does the footage show what the headline claims?** Not "is it thematically
adjacent" — does it show the subject. v17 opened on a modern iPhone under
"NOKIA OWNED 40% OF PHONES" and closed on confetti reading "Hooray!" over a
$7.6 billion write-off. Both passed every check that existed.

If a scene is wrong, fix it and re-render:

    .venv/bin/python pipeline/clip_sheet.py --query "<better query>" --limit 12 --out /tmp/sheet.jpg
    # view the sheet, then pin the winner as "clip_url" on that scene

Pin by URL so a re-run cannot silently swap it back. For a beat where a real
photograph of the real subject beats any stock clip, source it and set
`"still_only": true`:

    .venv/bin/python pipeline/broll_source.py --search "<subject>"
    .venv/bin/python pipeline/broll_source.py --get "<file>" --slug <slug> --id s1

Prefer `free` (public domain / CC0). `share-alike` is a licence decision, not a
formality — say so in the report if you take one.

**b. Prove the audio is audible:**

    ffmpeg -i profiles/money-stories/out/<slug>.mp4 -af volumedetect -f null - 2>&1 | grep volume

A card once shipped at -91 dB with every check green: the file existed and had
an audio stream, and both are true of digital silence. Expect roughly
`mean_volume` near -20 dB. Anything below -60 dB is silent — stop and fix it.

**c. Check the cadence:**

    .venv/bin/python pipeline/shot_cadence.py profiles/money-stories/out/<slug>.mp4

## 5. Description

Write `scripts/desc/<slug>.txt`. **The first paragraph must stand alone** —
`upload.py` truncates it to 150 characters for the TikTok and Instagram caption,
so a first paragraph that only makes sense with the second becomes a broken
caption on two platforms. End with a follow line and hashtags.

## 6. Publish — all three

    .venv/bin/python pipeline/run_state.py --path profiles/money-stories/state/run-<UTC stamp>.json \
        --init <UTC stamp> --profile money-stories --task shorts --set video=<slug> --set title="<title>"

    HERMES_PROFILE=money-stories .venv/bin/python pipeline/upload.py \
        profiles/money-stories/out/<slug>.mp4 IGNORED scripts/desc/<slug>.txt --state <state file>

Pass the title through `--state`, never on the command line: `$` in a title dies
in the shell and once published a video as *"Quibi Raised .75B"*.

**If a platform session is logged out, STOP for that platform only** — record it
and move on. The other two still land. Never handle credentials, and never
attempt to log in.

## 7. Verify, then record

    .venv/bin/python pipeline/publish_verify.py <youtube_video_id>

Exit 0 = publicly resolvable. **A draft gets a URL too**, and one was once
recorded as published with a link no viewer could open. Shorts can take about 2
minutes to resolve; if it says not_public, wait and check once more.

Then confirm the video is not flagged made-for-kids, which silently removes it
from the Shorts feed, suggested videos and notifications:

    .venv/bin/python pipeline/audience_audit.py --profile money-stories

Two of nordyl's four videos sat in that state for a week with 20 impressions
between them and 0% Shorts-feed traffic.

Record exactly what was verified, never what you believe succeeded.

## 8. Measure, and change something

    .venv/bin/python pipeline/public_stats.py
    .venv/bin/python pipeline/retention_loop.py --days 28

Judge on **views/day**, not raw views — raw views mostly measure how long
something has been up. Retention rows that come back `error` with an empty note
are a known open defect; say so rather than reporting a zero.

## The report

End with: the published URLs, per-platform verified true/false, cost from the
ledger, and **one thing you changed or learned**. If a defect cost you time,
fix it in the repo and commit it — you own this pipeline, not just its output.
Conventional commits, no attribution footer.

If a step fails twice, stop, write the failure plainly in the report, and do not
loop.
