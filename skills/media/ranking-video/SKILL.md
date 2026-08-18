---
name: ranking-video
description: Produce a ranking/countdown short (Top 5 / worst-to-best / "Ranking X Moments") to the standard of the format's top performers. Carries the measured reference data, the edit grammar, the sourcing order, and the specific defects this format ships when unattended. Use when building or fixing any ranking-format video.
---

# Ranking / Countdown Video

The format-specific playbook. General video craft lives in
[`video-production`](../video-production/SKILL.md) — read that too; this file
does not repeat it.

Everything here was measured off real videos or paid for with a shipped defect.
Where something is inferred rather than measured, it says so.

---

## ⚠️ START HERE — the four things that went wrong repeatedly

Read these before writing any code. Every one shipped, passed every check that
existed at the time, and had to be caught by looking at pixels.

**1. It rendered as a SLIDESHOW, twice.** Measured: 85.4% of consecutive frame
pairs were pixel-identical, median frame-to-frame difference exactly 0.00,
against a reference at 0.0% static. The cause was banal — `shots[]` was an
empty array. The component had always supported three clips per item and cut
between them; nothing was ever passed, so it rendered black behind text.
**Check that footage actually reached the render before judging anything else.**

**2. The grade rendered near-black.** Stacking `contrast` + `saturate` + a
*darkening* brightness + `sepia` + a multiply overlay + a vignette on already-dark
footage. Contrast alone pulls the low end down; everything after it crushes.
**Brightness should RAISE.**

**3. The overlay whipped with the footage.** `TransitionSeries` transitions
whatever is inside it, so the rank numeral slid across frame during every
transition. The reference's board is pixel-stable through every whip.
**Three layers: footage inside the transition, type above it, rail above that.**

**4. `--props` JSON bypasses zod defaults.** An omitted `valuePrefix` arrived
`undefined` and template-literalled into **"undefined158 yrs"** on the payoff
board. It shipped in *both* renderers from one copy-paste. **Default optional
fields at the point of USE, not only in the schema.**

---

## 0. The editor's posture

You are the editor, not the assembler. The distinction is the whole skill:
an assembler places a clip in a beat and puts text over it; an editor decides
what the viewer feels at frame 142.

**The material is almost never the problem.** The best-performing reference in
this genre is a 97,700-subscriber channel with twenty videos, cutting other
people's phone footage of scooter crashes. Nothing about that raw material is
good. It went to 171 million views because every cut is a whip, the board
accumulates answers, the shot lengths breathe between 2.8 and 4.7 seconds, and
someone laid a cartoon *boing* under a takeoff.

So when a cut looks like junk, the reflex is wrong if it is "find better
clips". Ask in this order:

    1. Is footage actually reaching the render?     (it was empty twice)
    2. Is anything MOVING inside each shot?         (85% static, twice)
    3. Does every cut do something?                 (100% hard cuts)
    4. Can the type be READ over this footage?      (needed a scrim)
    5. Is there sound in the gaps?                  (-91 dB, digital silence)

Every one of those was a real defect here, and not one of them was a sourcing
problem. Four of the five were a single missing line of code.

**Three moves turn flat footage into a cut, in order of leverage:**

  * **Never let a camera move start or stop at rest.** Interpolate beyond the
    visible window and show only the middle. Motion continuity ACROSS the cut
    is most of what separates an edit from a slideshow, and it costs nothing.
  * **Give the cut itself a job.** A whip carries the eye through; a hard cut
    asks it to re-acquire. Zero hard cuts in the reference.
  * **Degrade everything identically.** Grain, vignette, aberration. Five clips
    from five shoots read as five clips until they are dirtied the same way.

And the discipline that matters more than any of them: **look at the frames.**
Not the metrics — the frames, consecutive, at 230px or larger. Three separate
passes here reported healthy numbers on a video that was a slideshow.

---

## 1. The reference data — measured, not sourced from anyone's blog

Pulled from YouTube's own metadata via `yt-dlp` on 2026-08-17. Ranked by
**views ÷ subscribers**, which is what isolates format from audience.

    v/sub   channel (subs)          video                        views    len
    1750x   Iconic Rankings 97.7K   Ranking Best Scooter Moments 171.0M    24s
     970x   BEN RANKS 199K          Best Wasps Nest Removal      193.1M    51s
     580x   Zero Ranks 179K         Ranking Best School Moments  103.7M    49s
     193x   Xiro Ranks 1.39M        Ranking Best Shark Moments   268.4M    21s
                                    ^ 6.7M views/DAY, densest specimen

**The canonical reference is `t8O0f874wI4`** — 171M views from a 97,700-sub
channel with only 20 videos total. The format is doing 100% of the work.

**⚠️ Rank candidates by views-to-SUBSCRIBERS, never by views.** The most viral
ranked list found by raw views (squewe, 23.5M) came from a 2.33M-sub channel —
10x, so the audience carried it — and was 1920x1080 LANDSCAPE from 2022, not
even a vertical Short.

### Search failures worth not repeating

  * **"countdown" is a polluted keyword on YouTube** — it returns TIMER videos.
    Top hit: "10 Second Countdown Timer With Voice", 8.2M views. Use "ranked",
    "top 10", "tier list", "worst to best", and filter the timer genre out.
  * **Relevance-sorted search returns the spam tail.** The genuine ranking
    videos it surfaced topped out at 28,944 views.
  * `yt-dlp --flat-playlist` does **not** return `channel_follower_count`, so a
    views-to-subs filter silently matches nothing. Fetch full metadata per video.
  * **Channel enumeration beats search.** `yt-dlp --flat-playlist --dump-json`
    on `youtube.com/channel/<ID>/shorts` surfaces real outliers. Channel-type
    search (`&sp=EgIQAg%3D%3D`) on the query `ranks` returns the whole ecosystem.

---

## 2. The format's actual structure

    items        5-8, NEVER 10
    length       20-60s; the best views/day specimens are all 20-27s
    pacing       3.4-4.6s per item on sub-30s videos
    shot lengths VARY 2.83-4.70s, average 3.41 — not a grid
    order        descending N->1 ... only about half the time
    narration    NONE in the references — clip audio + music + added SFX

### ⚠️ The real invariant is the BOARD, not the countdown direction

Frame-by-frame verification of 14 TikTok ranking videos: **6 descending, 1
ascending, 7 arbitrary.** "#1 revealed last" holds roughly half the time.

What is universal is **a persistent numbered board, on screen from frame 1**,
filling in with the ANSWERS as they resolve — "2 Lego Scooter", "3 Impossible",
"4 Waiter". Not a progress bar. A running list of what has been revealed.

**Protect the board above everything else.** It is the format.

Two consequences:

  * A viewer landing mid-video gets content, not just position.
  * **The board must never spoil.** An item joins it only once its beat has
    FINISHED. Counting an item revealed when its Sequence *starts* put every
    answer except #1 on screen during item #2 — four beats early.

### The reference has NO boards and NO large numeral

Measured: the reference spends **0% of its runtime** on full-screen cards. Scene
1 starts at 0:00 with content. An early build spent 23% on hook and payoff
boards — that is a quarter of the video showing nothing.

It also shows **no large rank numeral at all**. The rank lives only in the
board. A centre-screen `#5` is double-encoding and eats the frame where footage
should be.

### Scene-by-scene, from the canonical reference

    scene  span        len  shot     audio
    1      0:00-0:04   4s   Medium   rail impact, splash, a woman screaming
    2      0:04-0:07   3s   Wide     wind, thud, bystander shouting "Whoa!"
    3      0:07-0:10   3s   Wide     wheels, plastic bricks clattering
    4      0:10-0:15   5s   Medium   upbeat electronic pop + skates
    5      0:15-0:20   5s   Wide     cartoon "boing" SFX + crowd roar
    6      0:20-0:24   4s   Wide     "I got this!" + pistol-shot SFX + thud

Note scenes 5 and 6: **they add sound effects to found clips.** That is
deliberate sound design, not passthrough.

---

## 3. Every cut is a WHIP. There are zero hard cuts.

Detected by measuring horizontal-gradient energy per frame — a whip shows a
sharp dip as the image smears.

    cut     time     blurred frames   detail floor (baseline 7.91)
    f142    4.73s          8               2.98   = 38%
    f249    8.30s          4               3.11
    f334   11.13s          4               3.31
    f474   15.80s          3               3.54
    f615   20.50s          3               3.38

Three encodable facts:

  * **Transitions SHORTEN as the video runs** — 8, 4, 4, 3, 3 frames. The edit
    accelerates. This is a pacing curve, not noise.
  * **Blur bottoms out on the frame BEFORE the cut.** The whip peaks going OUT;
    the new shot arrives already resolving. Symmetric blur feels like a dissolve.
  * **Motion vectors match across the cut** — exit left, enter from the right.
    Opposing directions read as a glitch.

Implementation is in `render/src/edit/whip.tsx`. CSS blur is isotropic, so a
lateral smear is faked; at 3-8 frames the eye reads it as directional and it
needs no WebGL2, which the render environment does not guarantee.

---

## 4. Sourcing — archival first, always

**Generic stock cannot BE the subject.** A stranger walking down an office
corridor is not Enron. This was learned twice.

    1. ARCHIVAL   pipeline/broll_source.py — the real company, the real object
    2. STOCK      pipeline/stock_clips.py — motion and texture only
    3. GENERATED  fal.ai FLUX -> Kling i2v, when neither has the shot

Verified wins on v20: the actual Lehman HQ with the sign legible, a Pan Am 747
in flight (public domain, NARA), a real Kodak Stereo Camera, a genuine video-
rental interior, and **the actual Enron Code of Ethics, July 2000** — the
company behind one of history's great frauds, and here is its printed ethics
policy. That last one is what "evidence, not adjacency" means.

**Verify every clip at 230px+ before it reaches a render.** Failures caught this
way, all of which would have passed a 150px contact sheet:

    query                              returned                    verdict
    "vintage film camera reel"         magnetic tape, not film     WRONG
    "vintage airplane propeller"       US military warbird         WRONG
    "bank vault"                       a basilica dome             WRONG
    "2008 events" (for Lehman)         rockets, Kosovo, riots      WRONG

All four traced to the same root cause: **OR is the default operator on Pexels
and Pixabay.** `"vintage film camera reel"` matched *vintage* OR *film* OR
*camera* OR *reel*. Single concrete nouns — `film negative`, `airliner` —
returned the right subject immediately.

⚠️ **Licence is a decision, not a formality.** CC BY-SA asks that adaptations
carry the same licence, which is a real question for a monetised channel. Prefer
public domain > CC BY (needs a credit line) > CC BY-SA (raise it explicitly).

---

## 5. Per-platform — the format does NOT behave the same everywhere

**TikTok reproduces the YouTube ecosystem almost exactly.** 68 ranking accounts
in a 768-video sample, same naming grammar (@aidensranks, @rankora00 mirroring
RankZilla, BEN RANKS), same 5-item found-clip structure. Biggest hits from
1,500-44,000 follower accounts.

⚠️ **A retracted claim, kept because the mistake is instructive.** This skill
briefly held that the format does not transfer to TikTok, from sampling four
accounts whose TikTok bests were 35-818,800 against YouTube bests in the
hundreds of millions. Those were **neglected mirror accounts**. Measuring a
platform through accounts famous somewhere else measures their neglect, not the
platform. Sample natively or do not conclude.

**Instagram is a MEDIUM MISMATCH, not a quality problem.** Ranking there lives
in **carousels**, not Reels:

    @rankingroyals (204K)        carousel    80,000 likes
    @dailyrankdepartment (80K)   carousel    18,000 likes
    --- against ranking REELS from comparable accounts ---
    @thetierzoo (67K)            reel         3,637 likes
    @watchmojo (721K)            reel           877 likes

The `(SLIDE 1/4)` framing is the persistent board in another medium. **Instagram
gets a carousel** (`RankedCarousel.tsx`, 1080x1350).

⚠️ **Instagram view counts are unobtainable and the one API field that exists is
corrupt** — 3 of 10 sampled reels reported views BELOW likes. Take views from
the TikTok cross-post.

**Never average this format's performance across platforms**, or a video that
wins on YouTube and TikTok is reported as a channel-wide loser on Instagram's
numbers.

---

## 6. Enforce the promise in the SCHEMA

The format's core claim is that the order is objective — a record, not a
verdict. A promise enforced by a writer remembering to check is not enforced.

Four refinements **fail the build** rather than warn, because each renders
looking entirely correct:

    1. item count matches the grid exactly
    2. ranks are exactly 1..N, no gaps, no duplicates
    3. VALUES STRICTLY MONOTONIC in the stated direction
    4. every item carries a source with a URL and a date

Refinement 3 is the one that matters. A ranking whose numbers do not actually
sort is indistinguishable from a real one at a glance, and it destroys the only
thing separating this format from an opinion. Equal values fail too —
monotonicity must be *strict*.

**Pick a metric that is a subtraction, not a judgement.** v20 ranks by years
survived (founding year minus collapse year), so the ordering carries almost no
figure risk. Dollars lost, percentage collapse, years survived — never "best".

---

## 7. There is NO research supporting this format

Worth knowing before citing anything.

**Zero credible studies segment short-video performance by list/countdown/
ranking format.** Eleven named analytics publishers were checked — Wistia,
Socialinsider, Metricool, Buffer, Vidyard, Rival IQ, Emplifi, Dash Social,
Later, Hootsuite, Tubular. Every one segments by platform, length, post type or
account size. **Nobody classifies "is this a ranked list?"**

Structural reason: **YouTube does not permit A/B testing on Shorts**, so nobody
outside the platforms can run the experiment.

⚠️ **"Lists and countdowns perform 41% better" is fabricated.** It traces to
exactly one page — a "93+ stats" listicle where none of the 93 claims carries a
citation, source, period or sample size. An exact-phrase search returns **zero
other hits**, so it was caught before repetition laundered it into authority.
Never cite it except as a documented example of fabrication.

Also weak: the curiosity-gap foundation. *Scientific Reports* 2024, on the
Upworthy archive of **27,000+ randomised headline A/B tests**, found
curiosity-gap headlines can get clicked **less**. Do not build on Zeigarnik.

**The consequence:** any defensible claim about this format has to come from
data we generate. That is a gap and an opportunity — publish what was measured
with the config attached, because nobody else in this space does.

---

## 8. ⚠️ The compliance risk is TEMPLATED SAMENESS

The most important strategic finding, and it cuts against running this format
on a locked template.

YouTube's inauthentic-content policy targets "generic, repetitive, or
template-based" content with no narrative arc, and is explicitly
**tool-agnostic** — AI use is not the trigger. The classifier already
false-positives: it flagged **Kurzgesagt**, entirely hand-made, because a flat
house style is over-represented in AI output.

**Visual sameness across a catalogue is a detectable risk in its own right.**
Four videos a day from one locked template is exactly the shape the policy
describes. **Vary structure deliberately across the catalogue** — treat template
diversity as a compliance requirement.

Related: the top ranking channels **scrape rather than license**. Operator
tutorials for this niche teach "remove text, use blur and scaling techniques" —
watermark removal — and frame the ranking overlay as what makes it
"monetization-friendly". The overlay is their minimum viable transformation. We
do not do this, which costs their footage quality and buys a channel that
cannot be taken down for it.

---

## 9. How to verify — the method, because three passes missed a slideshow

  * **Step CONSECUTIVE frames at 30fps.** Sampling every 2.6s cannot see a 0.2s
    whip transition.
  * **Render at 230px or larger.** A whip reads as "slightly soft" at 150px and
    as obvious smear at 230px. The same error hid magnetic tape standing in for
    photographic film.
  * **Frame-difference statistics say WHEN a cut lands and never WHAT technique
    made it.** Aggregate motion numbers cannot see craft.

`ffmpeg -vf "select='eq(n,N)'"` at 230px+ is the instrument. No extra tooling
was ever needed — the tools were pointed wrong.

### Numbers to check against

    near-static frames   reference 0.0%   (a slideshow reads 85%+)
    mean frame motion    reference 22.32
    integrated loudness  -14 LUFS via pipeline/normalize_audio.py
    every narration take verified against its script via pipeline/verify_takes.py

**`verify_takes.py` is the one that catches what nothing else can.** Duration,
loudness and file-existence checks cannot see CONTENT — a take of the wrong
line, right length, right loudness, is invisible to all of them and audible to
every viewer.

⚠️ **Film grain does not survive compression.** The grade applies per-frame
grain; export a high-bitrate master. Someone who tested it found **CBR 100 Mbps
h.264 beat ProRes** after YouTube's re-encode.

⚠️ **Over-loud SFX is the most commonly named amateur tell in this exact
format.** Two practitioners, unprompted, on an otherwise well-received ranking
edit: "the sfx need to be more subtle — they need to add to the content not
distract from it."

---

## 10. Build order

    1. pick a metric that is a subtraction, not a judgement
    2. verify it sorts strictly — the schema will refuse it otherwise
    3. source archival for every item, verify each at 230px+
    4. add a second angle per item so beats can cut internally
    5. narration per beat, never one track (drift reaches 2s)
    6. verify every take against its script
    7. music at 120 BPM if the grid is bar-aligned
    8. render, then normalise to -14 LUFS
    9. step consecutive frames across one cut and one beat, at 230px+
    10. check the board never spoils and never whips

Components: `RankedEdit.tsx` (the edited format), `RankedList.tsx` (the earlier
assembly version), `RankedCarousel.tsx` (Instagram), `edit/grammar.ts`,
`edit/whip.tsx`, `edit/Shot.tsx`. Spec and full provenance:
`profiles/money-stories/RANKING-FORMAT.md`.
