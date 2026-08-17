# money-stories — daily production

You own this channel end-to-end. Full autonomy: **never ask permission — produce,
check, and publish.** Report what you did and what you found. A question at the
end of a run is a failure of this task, not a courtesy: nothing else on this
machine schedules production any more, so a run that stops to ask produces
nothing that day.

**North star: monetization.** Views are the vehicle; the destination is a
channel that earns — improve the research and content quality every run until
this is the #1 channel in its space, then convert. Every production choice
should be defensible as a step toward that.

**Autonomy is bounded.** Read `tasks/PERMISSION-BOUNDARY.md` and stay inside
it: research + content tools + the platform browser toolset + this repo (git
commit / PR / merge included). No computer_use, no osascript, no other apps,
no personal folders. Denied commands are audited; do not retry them.

    workdir   /Users/aarjay/projects/hermes-platform/workspace
    python    .venv/bin/python           (always this, never system python3)
    profile   money-stories              (export HERMES_PROFILE=money-stories)
    boundary  /Users/aarjay/projects/hermes-platform/tasks/PERMISSION-BOUNDARY.md

The workspace is the former agent-platform tree, ported here 2026-08-17 with
its full git history intact. `render/node_modules` was stripped in the port —
run `npm install` in `render/` before the first render.

Every pipeline entry point refuses to guess a profile. Pass `--profile
money-stories` or export `HERMES_PROFILE`; a command that errors with "no profile
bound — refusing to default" is missing that, not broken.

## 1. Pick FOUR stories — one per format, never a repeat

**This run produces FOUR videos, not one.** Owner, 2026-08-17: "if no limit
than post each style one piece of content", "in diffrent time", and — asked
directly whether the four should share a story — **"four different stories"**.

    one video per FORMAT per day, FOUR DIFFERENT STORIES, staggered times

    story_card           typography-led, no b-roll
    ugc_number_overlay   for stories where NUMBERS are the content
    ranking_countdown    spec in profiles/money-stories/RANKING-FORMAT.md
    money_story          the narrated default with b-roll and voiceover

**Format selection is no longer a decision.** Every format ships every day, so
the format deficit is always zero by construction. Keep computing it — but as
a CHECK that a variant did not silently fail to render, never as an input to a
choice. The PILLAR deficit is what still drives which four stories get picked.

**Why four different stories and not four cuts of one.** The matched design
(same narration, four formats) was the better experiment and was abandoned on
purpose: YouTube's inauthentic-content policy names "templated storylines" and
"slideshows that all have the same narration" as ineligible, and TikTok
escalates from post to ACCOUNT for volumes of For-You-ineligible content
without any rule being broken. Four same-day variants sharing one script is a
verbatim description of both. The replacement is **randomisation instead of
matching**: at 7 samples per format per week the story-to-story variation
averages out rather than being held fixed. Do not "improve" this back.

**Write the format into the script JSON as a `format` field** and report
`format: <name>` next to each pillar line. That field exists because v19
(2026-08-17) shipped a numbers-driven story as a generic narrated video while
the purpose-built number-overlay format sat unused — the data had been measured
and then ignored, because there was nowhere to put the decision.

Default pairing (guidance, not a rule): `personal_finance` ->
`ugc_number_overlay`, `founder_drama` -> `money_story`, `genius_moves` ->
`story_card`, `investing`/`retirement`/`debt_and_credit` -> `ranking_countdown`.

**The niche is eight pillars wide as of 2026-08-17** — the five company-story
pillars plus `investing`, `retirement` and `debt_and_credit`. Those three carry
a house rule that binds absolutely: **record, never verdict.** Tell what
someone did and what the number was, with its source. Never tell the viewer
what to buy, sell, hold or allocate. "Kodak missed digital" is history; "put
15% in an index fund" is advice a stranger acts on with their own money.

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

## 6. Publish ONE now, queue the other three

You produced four videos. **Publish the first and hand the rest to the
queue** — the owner requires them staggered across the day (2026-08-17, "in
diffrent time") so four of our own videos do not compete for one distribution
window. Three separate cron jobs — `money-stories-slot2/3/4` at 17:05, 19:35
and 22:05 — each publish one, following `tasks/money-stories-publish-slot.md`.

**Write the queue BEFORE you publish anything.** If the run dies during the
first upload, a queue already on disk means three finished videos still go out
tonight; a queue written afterwards means all four are stranded.

    .venv/bin/python pipeline/publish_queue.py \
        --path profiles/money-stories/state/publish-queue.json \
        --init <YYYY-MM-DD> \
        --item <slug1>:<format1> --item <slug2>:<format2> \
        --item <slug3>:<format3> --item <slug4>:<format4>

**Rotate which format lands in which slot, every day**, and say in the report
what today's mapping was. Time of day affects reach, so pinning a format to a
slot would make the slot a second variable and confound the format comparison
this whole design exists to make.

Then publish the first slug now, and **mark it** so the 17:05 fire moves on:

    .venv/bin/python pipeline/publish_queue.py \
        --path profiles/money-stories/state/publish-queue.json --mark <slug1>

Mark only AFTER verification (step 7) confirms it is live. Marking early
retires a video that never published, and nothing downstream would notice.

If a render failed and you have fewer than four videos, queue only the ones
that exist. `--init` refuses more items than slots, so never pad the list.

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

Then **check Account Status on all three platforms** — this is new as of
2026-08-17 and it is the only DOCUMENTED signal of suppression any of them
publish. Everything else is reading tea leaves in an analytics chart:

    Instagram   Settings -> Account -> Account Status   (recommendation eligibility)
    TikTok      Studio -> More tools -> Account check   (For You feed eligibility)
    YouTube     YouTube Studio                          (monetisation / strikes)

This matters more at four videos a day than it did at one. TikTok's Community
Guidelines state that accounts posting a lot of For-You-ineligible content "may
be made ineligible for the FYF and harder to find" WITHOUT breaking any rule —
a quality trigger reached through volume. Account Status is where that becomes
visible, and it becomes visible before the views number explains why.

Report the three states explicitly. "Not checked" is an acceptable answer;
inferring "we're fine" from a views number is not.

Then **append the ledger line**. This step is not optional and has now been
missed twice — by a human on v17 and by the first autonomous run on v18, both
times because the instruction said "record" without giving the command:

    .venv/bin/python - <<'PY'
    import json
    from pathlib import Path
    p = Path("automation/logs/production.jsonl")
    p.open("a").write(json.dumps({
      "ts": "<UTC ISO8601>", "video": "<slug>", "pillar": "<pillar>",
      "title": "<title>",
      "url": {"youtube": "...", "tiktok": "...", "instagram": "..."},
      "platforms": {"youtube": True, "tiktok": True, "instagram": True},
      "cost_usd": 0.0,
      "notes": "what you changed, what you found, what you could not verify",
    }) + "\n")
    PY

`production.jsonl` is the memory across runs: step 1 reads it to avoid repeating
a story, and the weekly review reads it to know what exists. An unrecorded video
is invisible to both — v17 was published and the weekly review still reported it
as missing, so the control test it was waiting for could not be used.

Verify the line landed before you finish:

    grep -c "<slug>" automation/logs/production.jsonl    # must be 1

Record exactly what was verified, never what you believe succeeded. `platforms`
values must be the results you checked, not the ones you attempted.

**Titles containing `$`:** set the title INSIDE the state file, never through a
shell `--set title=...` — `run_state.py` has the same `$`-expansion exposure
`upload.py` was fixed for. v18 silently lost "$139" from its headline this way.
Do not weaken a title to dodge the bug; write it via Python and keep the number.

## 8. Measure, and change something

    .venv/bin/python pipeline/public_stats.py
    .venv/bin/python pipeline/retention_loop.py --days 28

Judge on **views/day**, not raw views — raw views mostly measure how long
something has been up. Retention rows that come back `error` with an empty note
are a known open defect; say so rather than reporting a zero.

**Compare formats on ENGAGED VIEWS, never on Views.** Since 2025-03-31 a
YouTube Shorts "view" counts every play or replay with no minimum watch time,
which makes it close to an impression count and unable to discriminate between
formats. The stricter old metric survives in Analytics as **Engaged Views**,
and monetisation still runs on it. A format comparison reported on Views is
invalid — say so and re-pull rather than reporting it.

Compare formats **on the same platform**. The three feeds rank on different
signals, so a cross-platform format comparison is confounded; use TikTok and
Instagram to check the direction, and YouTube Engaged Views to decide.

## The report

End with: the published URLs, per-platform verified true/false, cost from the
ledger, and **one thing you changed or learned**. If a defect cost you time,
fix it in the repo and commit it — you own this pipeline, not just its output.
Conventional commits, no attribution footer.

If a step fails twice, stop, write the failure plainly in the report, and do not
loop.
