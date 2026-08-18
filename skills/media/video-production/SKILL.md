---
name: video-production
description: Source, generate and edit short-form video to a professional standard — stock and archival sourcing, AI b-roll generation via fal.ai, the measured edit grammar, and when to use Remotion vs DaVinci Resolve. Use when producing or improving any video for money-stories or nordyl.
---

# Video Production

Everything needed to take a short-form video from "assembled clips" to "edited".
Ported into this repo 2026-08-18 from `~/Documents/social-media`, which had
already solved most of it — and which was NOT found until after several days of
rediscovering the same answers badly.

**Read `references/` before starting.** The material there is the evaluation,
not a summary of it.

    references/fal-toolkit.md              83 i2v endpoints swept, per-model verdicts
    references/production-capabilities.md  the full asset->assembly->delivery stack
    references/davinci-resolve-mcp.md      what Resolve can and cannot do via MCP
    references/fal_video.py.txt            working i2v generation code
    references/fal_image.py.txt            working keyframe generation code

---

## 1. Which editor — decided, not open

**REMOTION when the cut is deterministic and typography-led.** Clip order and
durations come from a spec, text is driven by data, captions are timed from
word timestamps in code, and you expect to re-render after a script tweak.

**RESOLVE when the work is footage-led and needs real post.** Colour grading
with CDL, conform/AAF/XML, Fairlight mixing, multicam — anything where you must
*look at the footage to decide the cut*.

**The line that settles it for automated daily production:** Resolve's MCP
**cannot do keyframe animation** (`references/davinci-resolve-mcp.md`). It sets
static transforms; animating one needs the UI. Any format built on per-frame
motion — whip transitions, running camera moves, handheld drift, text springs —
is therefore Remotion or nothing, because nobody is at the keyboard at 14:35.

Where Resolve genuinely wins if a human is available: real CDL grading rather
than CSS `contrast()`/`saturate()`, and Fusion for true directional blur rather
than an isotropic-blur approximation.

⚠️ Resolve constraint that bites this repo: **still images cannot have their
duration set via the API** (locked at 150 frames). Bake stills to mp4 first.

---

## 2. Sourcing footage — in priority order

**The rule that matters most: stock footage does not look like evidence.**
Generic stock cannot BE the subject. A stranger walking down an office corridor
is not Enron. This was learned twice the hard way and is written into
`pipeline/broll_source.py`'s own docstring.

### a. ARCHIVAL — the real subject. Always try this first.

    .venv/bin/python pipeline/broll_source.py --search "Lehman Brothers Times Square"
    .venv/bin/python pipeline/broll_source.py --get "<term>" --slug <slug> --id a1

Wikimedia Commons, with a licence sidecar written next to every download.
Prefer **public domain** > **CC BY** (needs credit) > **CC BY-SA** (share-alike
is a real licence decision for a monetised channel, not a formality — say so in
the report if you take one).

Verified wins on v20: the actual Lehman HQ with the sign legible, a Pan Am 747
in flight (public domain, NARA), the genuine Enron Code of Ethics from July 2000.

### b. STOCK — for motion and texture, never for subject

`pipeline/stock_clips.py` → Pexels, Pixabay, archive.org.

**⚠️ OR is the default operator on both Pexels and Pixabay. Extra words BROADEN
the result set, they do not narrow it.** Measured: Pexels `flower` = 25,399
results, `red flower` = 57,879. This single fact invalidates most query advice.

  * **One concrete noun per query.** Fan out, merge locally.
  * **Pexels is semantic, Pixabay is lexical.** `a company going bankrupt` on
    Pexels returns "woman packing her things into a box in the office"; the same
    query on Pixabay returns rafting vans. Two different query generators.
  * **Never send negation to Pexels** — it strips the `-` and treats the word as
    positive. `flower -red` renders as "Flower Red Videos".
  * **After one good hit, stop querying and enumerate that contributor.** Both
    APIs expose `user.id`. This is where shot-to-shot consistency comes from.
  * Pexels ships `video_pictures[]` — a ready-made contact sheet. **Vision-check
    it BEFORE downloading.**

Failures this catches: a magnetic-tape reel standing in for photographic film, a
military warbird standing in for a Pan Am airliner, a basilica dome returned for
"bank vault". All three were thematically adjacent and all three were wrong.

### c. GENERATED — when neither archival nor stock has the shot

`references/fal-toolkit.md` carries a live sweep of 83 image-to-video endpoints
with a verdict on each. `FAL_KEY` is already in the money-stories `.env`.

**Style comes from the STILL, motion from i2v — never from text-to-video.** Feed
a text prompt and the model goes photoreal and ignores the brief; feed a styled
plate and it holds the look exactly. This is why the whole pipeline is i2v.

    keyframe   FLUX Ultra ~$0.06        objects, scenery
               FLUX LoRA  ~$0.03        character shots, needs a trigger word
    motion     Kling 2.6 Pro  $0.07/s   the cost candidate
               Kling v3 Pro   $0.22/s   verified working, best object detail
               Hailuo         $0.017/s  budget

**Skip every speed tier** (`fast`/`turbo`/`lite`/`mini`) — they trade exactly
the detail this look depends on. **Re-sweep the registry before any new
pipeline**; the catalog moves monthly and a stale model choice is the most
common silent quality loss.

---

## 3. The edit grammar — measured, in `render/src/edit/grammar.ts`

Extracted frame by frame from a reference that did 171M views from a
97,700-subscriber channel. Not taste.

  * **Every cut is a whip.** Zero hard cuts in the entire reference. 3-8 frames
    of lateral blur, bottoming out at ~38% of baseline detail on the frame
    BEFORE the cut. Transitions SHORTEN as the video runs (8,6,5,4,3) — the edit
    accelerates.
  * **The overlay does NOT whip.** The numbered board stays pixel-stable through
    every transition; the blur applies to the footage layer only. Getting this
    wrong makes the whip read as a glitch.
  * **Shot lengths vary** 2.83-4.70s, average 3.41. A locked grid is more rigid
    than the thing being cloned.
  * **Cut 1-2 frames BEFORE the beat**, never on it — the ear registers a
    transient before the eye registers a cut. But **accents land exactly on the
    beat**: an impact effect IS the sound's visual.
  * **Offset picture cuts from sentence boundaries by 6-15 frames** (J/L-cut).
    The amateur pattern is sentence-ends-cut-new-sentence; every boundary lines
    up and it reads as a slideshow with narration.
  * **Never let a camera move start or stop at rest.** Interpolate beyond the
    visible window and show the middle, so motion is continuous ACROSS cuts.
    Amateur Ken Burns settles on every cut, and that settling is most of what
    reads as slideshow.
  * **Degrade everything identically** — grain with a PER-FRAME seed (a frozen
    seed reads as a dirty lens), vignette, slight aberration. Stock's defining
    quality is being too clean; five clips from five shoots read as five clips
    until they are degraded the same way.
  * **Text**: Remotion's own production template uses spring `damping: 200`
    (non-overshooting), scale 0.8→1.0, translateY 50→0, over 5 frames. Overshoot
    belongs on headlines, never on captions. Exits are faster than entrances.

---

## 4. Verify by LOOKING, at adequate size

Three separate passes missed that a video was a slideshow. The method error,
recorded so it is not repeated:

  * **Sampling too sparsely** — every 2.6s. A 0.2s whip transition is invisible
    at that rate. Step CONSECUTIVE frames at 30fps.
  * **Rendering too small** — 150px wide. A whip reads as "slightly soft" at
    150px and as obvious smear at 230px+. The same error hid magnetic tape
    standing in for film.
  * **Measuring proxies instead of looking.** Frame-difference statistics say
    WHEN a cut lands and never WHAT technique made it.

`ffmpeg -vf "select='eq(n,N)'"` at 230px+ is the instrument. No extra tooling
was ever needed — the tools were pointed wrong.

**Numbers worth checking against:** near-static frame share (reference 0.0%),
mean frame-to-frame motion (reference 22.32), and integrated loudness. Platforms
normalise playback DOWN but never up, so **-14 LUFS** via
`pipeline/normalize_audio.py` — a quiet upload just stays quiet in the feed.

---

## 5. Sourcing and editing — how the top channels actually do it (2026-08-18)

### ⚠️ The ranking channels SCRAPE. They do not license.

Verified from the artifacts and from operators' own tutorials, not commentary.
Five sampled channels with 8.9M-123M view videos credit **no** licensor, no
marketplace, no creator. The genre's standard description boilerplate is
"educational and entertainment purposes… All credit to the creators."

An operator selling tutorials for this niche teaches, verbatim: source raw
clips from "TikTok, Instagram, Reddit, and YouTube", then **"improve weak
clips, remove text, use blur and scaling techniques"** — that is watermark and
caption removal — then "add ranking elements like numbers, titles, and optional
commentary to make your videos more engaging **and monetization-friendly**."

**The ranking overlay is the minimum viable transformation.** That is the whole
design of the format. We are not doing this, which costs us their footage
quality and buys us a channel that cannot be taken down for it.

**No UGC clip licensor has an API** — Jukin, ViralHog, Newsflare, Storyful are
all human sales loops. ViralHog does advertise bulk/partnership models, which
is the only realistic path to legitimate found footage at volume.

### ⚠️⚠️ TEMPLATED SAMENESS IS ITSELF THE COMPLIANCE RISK

The single most important finding for this channel's strategy, and it cuts
against a locked format:

YouTube's inauthentic-content policy (renamed 2025-07-15, clarified 2026-07-16)
targets "generic, repetitive, or template-based" content with no narrative arc,
and is explicitly **tool-agnostic** — AI use is not the trigger. The classifier
already false-positives: it flagged **Kurzgesagt**, entirely hand-made, as AI
slop, because its flat house style is over-represented in AI output.

**Visual sameness across a catalogue is a detectable risk in its own right.**
Four videos a day from one locked template is precisely the shape the policy
describes. **Treat template diversity as a compliance requirement, not a
creative nicety** — vary structure deliberately across the catalogue.

### Economics — the numbers that decide the stack

    Remotion          FREE for individuals and companies <=3 people,
                      commercial use, unlimited renders. Beyond that
                      $0.01/render, $100/mo minimum.
    Resolve free      scripting is INTERNAL CONSOLE ONLY. Headless/external
                      Python needs Studio (~$295 one-time). Since 19.1 the
                      UIManager GUI layer is Studio-only.
    Artlist Max       $50.66/mo annual — footage (Artgrid folded in), LUTs,
                      music, SFX, AND unlimited credit-free generation on 13
                      models incl. Veo 3.1 Lite, Kling 2.6, Wan 2.7, LTX 2.3.
                      Dramatically cheaper than per-second API for volume.
    Storyblocks       $30/mo, and a real API with a partner agreement — the
                      genuinely programmatic search-and-download option.
    Shutterstock      the most developer-friendly: official Python CLI, MIT,
                      sandbox, license+download endpoints.
    Envato            ToS EXPLICITLY BANS scripted/mass downloading. Do not
                      build against it.

Veo 3.1 $0.40/s · Kling 2.6 Pro $0.07/s · Runway Gen-4.5 ~$0.10-0.23/s.

### Archival — the uncomfortable shape of it

**The sources with the footage have no API; the sources with great APIs do not
have the footage.**

    Internet Archive / Prelinger   PD confirmed, free, `internetarchive` python
                                   package. Has Pan Am (86 hits incl. a 1955
                                   corporate film). ⚠️ SD ONLY — 640x480.
    NARA / LoC / NASA / DVIDS      real APIs, free, PD-ish, per-item rights
    Getty / AP / Pathé / Reuters   have the 2000s broadcast footage, all
                                   require a human licensing step

**Two traps that will bite an automated pipeline:**

  * **archive.org TV News is NOT usable.** "Enron AND collection:tvnews"
    returns 2,027 tempting hits, all `access-restricted-item: true` —
    copyrighted network news under library research access. Fine for
    fact-checking, not clearable for a monetised video.
  * **C-SPAN is not public domain.** Verbatim: "C-SPAN does NOT permit
    unlicensed commercial use of any of its audio or video programming
    (including coverage of federal government events)." The event is public;
    their recording is not.

**Budget a Content ID dispute step regardless.** Content ID matches
fingerprints, not rights, and outlets fingerprint their own rebroadcasts of PD
material. Cite the archive.org item id and its `licenseurl` in the dispute.

### The look — two practitioner findings that beat any LUT

**⚠️ FILM GRAIN DOES NOT SURVIVE COMPRESSION.** "It can look fantastic on the
full-quality footage but video compression often does a number and it looks
like shit." Concrete countermeasure from someone who tested it: export a very
high-bitrate master — **CBR 100 Mbps h.264 came out slightly better than
ProRes after YouTube's re-encode.** This directly affects `edit/Shot.tsx`,
which applies per-frame grain.

**Over-loud SFX is the most commonly named amateur tell in this exact format.**
Two commenters, unprompted, on an otherwise well-received ranking edit: "the
sfx need to be more subtle (they need to add to the content not distract from
it) — I feel like your sfx are loud."

And the deflating consensus worth internalising before buying any plugin:
**"85% is production value and lighting, 10% lens/sensor, 5% grade."**

### Captions

The genre-defining style is literally named in Submagic's API docs as
**"Hormozi 2"** — bold condensed sans, word-by-word pop-on, keyword colour and
scale emphasis. Fonts: Bebas Neue, Archivo Black, Bangers, Unbounded.
**ZapCap at $0.10/min outputs transparent-alpha caption layers**, which keeps
captions compositable rather than baked pixels.

Note the supply chain: Submagic's "AI picks your b-roll" is a **Storyblocks
partner API call** underneath.

### Unverified — do not treat as established

Why premium stock looks better (LOG/RAW/ProRes headroom) · which AI model
passes as real footage for which shot type — **no independent source exists;
run your own bake-off** · the AI-tell countermeasure list · any named creator
succeeding at scale with AI b-roll (none found).
