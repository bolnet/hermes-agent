# board-order — daily production

You own this channel end-to-end. Full autonomy: **never ask permission —
produce, check, and publish.** A question at the end of a run is a failure of
this task, not a courtesy: nothing else schedules this channel, so a run that
stops to ask produces nothing that day.

    workdir   /Users/aarjay/projects/hermes-platform/workspace
    python    .venv/bin/python            (always this, never system python3)
    profile   board-order                 (export HERMES_PROFILE=board-order)
    channel   Board Order · @boardorder · UCFwQGCLYS-dZ4e3QAQp3I-Q
    account   aarjay4001@gmail.com        (Chrome sub-profile "Default")
    boundary  /Users/aarjay/projects/hermes-platform/tasks/PERMISSION-BOUNDARY.md

**Autonomy is bounded.** Read `PERMISSION-BOUNDARY.md` and stay inside it.
Denied commands are audited; do not retry them.

**North star: become the best ranking channel in its niche, then monetise.**
Views are the vehicle. Every production choice must be defensible as a step
toward that, and every run must leave the channel measurably better understood
than it found it.

## ⚠️ Two rules that override any improvement you think you have found

**1. ONE STYLE PER VIDEO. Never blend two.** Owner, 2026-08-18: *"clone one
video style completely, don't mix two."* Every video declares one `style:` from
`profiles/board-order/styles/` and takes ALL of its grammar from that style —
header, board, type, palette, cut rhythm, audio treatment, caption policy.

This is not taste, it is what keeps the work falsifiable. A single-style video
that under-performs can be compared frame-for-frame against its own reference
and the divergence found. A blend has no reference to diverge from, so there is
nothing to check and nothing to learn. If you catch yourself reasoning "the
captions from caption-rank would improve clean-board", you are proposing to
destroy the only measurement this channel has.

**2. NEVER ship a style at level `characterised` or `sketched`.** Promote it to
`measured` first — which means every number read off the reference's pixels AND
a clone built and compared frame-for-frame. v20 shipped from a frame grid that
was DESIGNED rather than measured and nothing in the repo said so; the `level`
field exists so that cannot happen quietly again.

**ENTERTAINMENT ONLY.** No finance, no business-collapse stories, no personal
finance. That is money-stories' territory. Two channels that drift into each
other's subject matter are one channel with two names.

## 1. Read the state before producing anything

    profiles/board-order/styles/STYLES.md       the registry and the rules
    profiles/board-order/styles/*.yaml          one spec per style
    profiles/board-order/LEARNED.md             what previous runs established
    profiles/board-order/out/                   what has already shipped

A run that produces before reading these repeats work that is already done.

## 2. Produce ONE video

One video per day, in ONE style. Quality over volume while the channel has no
data: four-a-day was money-stories' answer to a different problem and its own
notes flag templated sameness as the real compliance risk.

    a. choose the style     default clean-board; only a `measured` style
    b. choose the subject   §2b — from what PERFORMS, not from what stock has
    c. source every asset   nothing from any reference video, ever
    d. build               the style's `implementation` component
    e. verify              §4
    f. publish             unlisted first ONLY if a check is inconclusive;
                            otherwise public

## 2b. Pick the subject from PROVEN DEMAND — anything entertainment

Owner, 2026-08-18: *"make sure channel is for entertainment and it can have
ranking for anything related to entertainment — pick top video in any
entertainment or huge views and make new video based on that."*

**The method, in order:**

  1. Find an entertainment video or topic that is genuinely PERFORMING — huge
     views, or a strong views-to-subscribers ratio. `board-order-study` at 12:47
     already ranks channels this way and writes them to LEARNED.md; start there,
     and look beyond ranking channels — any entertainment video with outsized
     views names a topic people are currently watching.
  2. Build OUR OWN ranking on that topic. Our items, our footage, our board.
     Never the reference's clips, never its list — the topic is the signal, the
     video is ours.
  3. Say in the report which video or topic you took the signal from, and what
     its numbers were. "It seemed popular" is not a reason.

**Entertainment is the WHOLE field**, not one corner of it: film and TV moments,
music, games, celebrities, internet culture and memes, food, animals, travel,
stunts, sport. The only hard rule remains no finance and no business-collapse
stories — that is money-stories' territory.

⚠️ **DO NOT let sourcing pick the subject. That is what went wrong.** The first
three videos were "Best Action Moments", "Best Extreme Moments" and "Best Skate
Moments" — three near-identical action-clip rankings, titles differing by one
word. No one chose that. §3 said to pick subjects whose peak moments are
sourceable on free stock, and the honest answer to that is always sports. The
constraint selected the subject three times running while the strategy sat
unread.

Sourcing is a problem to SOLVE for the chosen subject, not the thing that
chooses it. If the footage is not there, say so in the report and propose the
licensing spend — do not silently retreat to skateboards.

⚠️ **Do not repeat the same subject AREA twice in a row.** Check
`profiles/board-order/out/` before choosing; three consecutive action-sports
videos is exactly the templated sameness this brief opens by warning about.

## 3. Sourcing — the wall this channel keeps hitting

**Verify every clip at 230px+ before building.** Of 12 action clips pulled for
v01, six were rejects — a man carrying a bag, parked rental scooters, an empty
ramp, a snowboarder taking a selfie. None was distinguishable from real action
at 150px.

**Cut each clip at its highest-motion window, not its head.** Stock clips open
and close on a hold, so the first N seconds is reliably the dullest part.

⚠️ **`clean-board` needs PEAK footage and free stock is thin on it.** Licensed
UGC (Jukin / ViralHog / Newsflare) has it and none of them has an API — all
human sales loops.

**This is a sourcing problem to solve, NOT a licence to re-pick the subject.**
Read as the latter it produced three action-sports videos in a row (see §2b).
For a subject chosen from proven demand, the options in order are:

    1. archive and public-domain film, not just modern stock — many
       entertainment topics are far better served by archival than by Pexels
    2. stills animated with i2v, which this project has already used for
       exactly this gap
    3. a different ITEM within the same subject that is sourceable
    4. propose the licensing spend in the report

Only if all four fail does the subject change — and then the report says which
subject was abandoned and why. Do not quietly substitute ambient B-roll and call
it the style.

⚠️ **OR is the default operator on Pexels and Pixabay** — extra words BROADEN
results. Search single concrete nouns.

**Every generated asset gets a ledger entry and a `.source.json` sidecar.**
Non-negotiable. v20 and v21 were produced with zero ledger entries, so when the
owner asked where the music came from there was no answer on disk: no record, no
metadata, no source file, no generating code. An unattributable asset on a
monetised channel is a Content ID claim with no receipt.

## 4. Verify the RENDER, not the inputs

Duration, loudness and file-existence checks cannot see content, and a content
check pointed at an input cannot see what assembly did to it.

    motion + static %     0.0% static is the bar; the reference hits it
    loudness              -14 LUFS  (pipeline/normalize_audio.py)
    frame comparison      side by side against the style's reference, at 230px+
    every asset present   a black beat means shots[] was empty — that shipped
                          twice at 85.4% static

## 5. Improve — this is the part that makes the run worth doing

Every run must add to `profiles/board-order/LEARNED.md`, with dates and numbers:

**a. Measure what shipped.** Pull views, retention and views-per-subscriber for
every published video. Compare each against ITS OWN style's reference.

**b. Act on the measurement, and say so.** If a style under-performs its
reference on a dimension you measured, change that dimension in the style's
yaml and record what changed and why. A measurement nobody acted on is the
failure this repo keeps recording — a pillar loop that measured and then ignored
the result shipped v19 in the wrong format.

**c. Promote or add styles.** Move one style from `characterised` to `measured`
per run where possible. `caption-rank` is the current candidate and its yaml
lists exactly what is missing.

**d. Find new references** when the registry stops improving. Rank CHANNELS by
views-to-SUBSCRIBERS, then take each channel's top Short — keyword search for
ranking Shorts is polluted and returns 1-view spam. Discard tiny denominators:
19K views off 95 subs scores 204x and is noise.

**e. Record what did NOT work.** A style that was measured and lost is more
valuable than one that was never tried, and it must not be re-attempted blind.

## 6. Report

    style used, and why that one
    subject, and why it was sourceable
    every asset with its origin and ledger line
    the verification numbers next to the reference's
    what LEARNED.md gained this run
    what you could not do, and what it would take

⚠️ **A run that exits 0 and prints numbers is not a run that measured the
thing.** Verified three separate ways on 2026-08-17: a licence check that
skipped four repos while reporting success, a benchmark arm that flatlined
against a token ceiling for 89 turns, and a cost comparison inflated by 96
skipped calls. State plainly what you actually checked.
