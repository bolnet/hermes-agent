# nordyl — daily production

    workdir   /Users/aarjay/projects/hermes-platform/workspace
    python    .venv/bin/python
    profile   nordyl            (export HERMES_PROFILE=nordyl)
    brand     NÖRDYL Research — @nordylresearch on every platform
    boundary  tasks/PERMISSION-BOUNDARY.md

## 0. READ THE GUARDRAILS FIRST. Every run. No exceptions.

    profiles/nordyl/brand/CONTENT-GUARDRAILS.md

**Read the whole file before you write a single word of script or caption.**
Not a summary of it, not your memory of it — open it.

⚠️ **The downside here is NOT reach.** §1: Nördyl sells research-use-only
materials to laboratories, and regulators and payment underwriters infer
*intended use* from the whole artifact. Content that reads as consumer
marketing can cost the card processing this business runs on. Every other
profile risks a bad video. This one risks the merchant account.

**The test, applied to everything:** if a regulator read only this post, with
the disclaimer removed, would they conclude it was selling a human treatment?
If yes, it does not ship.

⚠️ There is a second copy of that file at
`~/Documents/social-media/data/nordyl/brand/CONTENT-GUARDRAILS.md` which you
**cannot read** — `~/Documents` is on the hard deny list. The workspace copy is
the operative one. If you find them out of sync you cannot fix it; report it.

## 1. Read before producing

    profiles/nordyl/editorial.md                 what this channel is
    profiles/nordyl/research/                    dossiers, strategy, craft
    profiles/nordyl/stages/1-dossier.md .. 5-queue.md   the five stage prompts
    profiles/nordyl/publish/POSTED-LOG.md        what already went out
    profiles/nordyl/out/                         what already exists

**The five-stage pipeline already exists** — dossier, script, render, QC,
queue. Use it. Do not invent a new flow; stage 2 is the compliance gate and it
is written to be one.

## 2. Produce ONE artifact

Quality over volume. This channel's own log records Facebook at 200-300 per reel
and every other platform trending to zero, so nothing here is solved by posting
more.

**Subject comes from §3 of the guardrails — the reliable territory:**

    analytical identity        purity ≠ identity ≠ sterility ≠ endotoxin
    COA forensics              what a COA does and does not establish
    structure/characterisation folding, confidence metrics, what a prediction is worth
    handling and stability     as LABORATORY practice, never user instruction
    research literature        what a study measured, in what model, and what it cannot support
    sourcing and regulation    facts about the industry, not claims about a product

**Framing rule, §3:** describe what is *known about a molecule*, never what it
*does for a person*. "Studied in non-human models for angiogenic signalling"
ships. "Helps you heal" does not.

⚠️ **Do not take hooks from competitors.** Measured 2026-08-19 in
`research/COMPETITOR-CRAFT-2026-08-19.md`: every high-performing hook in this
niche is built on something the guardrails forbid — outcome claims, sequencing
protocols, medical persona. The craft transfers; the hooks do not.

## 2b. Which reference — they are NOT equal

Two clone compositions exist and one of them rests on a bad number.

    NordylClone       Infographics Show   109 days old   2.27% engagement  ✅
    NordylPeptide101  PolyPeptide Group   5.9 YEARS old  0.01% engagement  ⚠️

**Default to `NordylClone`.** Its reference is current and has a real audience.

`NordylPeptide101` is still a legitimate build — a seller making claim-free
animated content is exactly our constraint set, and almost nobody else in the
niche is inside it. But **never cite its 5.45M views as a reason.** Both of that
video's engagement numbers are reported and both sit ~100x below every peer,
which is what promotion looks like rather than reach. `TEN-BEST-SHOTS.md` still
calls it "the single best bet we have" on 5,738 views/sub; that entry is wrong
and is being corrected.

⚠️ **Do not blend the two.** Their cut rates belong to different classes of
video: PolyPeptide is 15 cuts over 104s (6.9s average, a SLOW film) and the
Infographics build cuts at ~1.4s. Subdividing one to the other's rate produces a
video that matches neither reference and can be compared against neither.

## 3. Craft — what the measurement actually supports

From `research/COMPETITOR-CRAFT-2026-08-19.md`, measured not guessed:

  * **Music is an EDIT, not a bed.** The two best performers re-cue music every
    6-7 seconds, scored to sections. Nothing in the reference set performs well
    on a static bed. `pipeline/gen_audio.py` produces the material and writes a
    provenance sidecar per asset.
  * **Chapter every long-form upload.** 9 and 13 chapters on the top two; zero
    on the rest. Costs nothing.
  * **Speech rate does NOT discriminate** — 160-188 wpm across all six
    regardless of performance. Do not tune it hoping to buy retention.
  * **Frame 0 carries information** — guardrails §4, and all six references
    independently obey it. Never open on a fade or a logo sting.
  * **One story, one cut per platform** — §4. A 16:9 re-exported to 9:16 is a
    crop, not a cut. Re-lay the typography for the frame it will be viewed in.

⚠️ **Cut rate exists for the two references we cloned, and NOWHERE else.**
`NordylPeptide101/index.tsx` carries a measured spec for PolyPeptide — 104s, 15
cuts, 6.9s average — recorded when that video was still downloadable. Those are
real numbers and may be used.

For every OTHER competitor, cut rate, shot length and LUFS are **not measured**:
YouTube now 403s on video and audio download, so nothing new can be measured
this way. Do not cite numbers that do not exist, and do not generalise
PolyPeptide's 6.9s to the niche — the Infographics build cuts at ~1.4s, five
times faster, and both are references we hold.

## 4. Verify before it goes anywhere

Run the guardrails' own §6 checklist, item by item, and say so in the report:

    [ ] no dosing, administration or reconstitution instruction anywhere
    [ ] no therapeutic, outcome or performance claim — caption and hook included
    [ ] no before/after, no testimonial, no implied personal result
    [ ] every factual claim traced to a primary source, checked TODAY, not recalled
    [ ] regulatory status re-verified at source if the post touches it
    [ ] AI disclosure set at platform level; wordmark correct; nothing else burned in
    [ ] the post survives being read with the disclaimer deleted
    [ ] nothing contradicts the RUO position the merchant account depends on

⚠️ **"Checked today, not recalled" is not decoration.** On 2026-08-19 the
strategy doc's claim that a folded peptide "scored 61.9" did not match the
folding output, where the lowest real score is MOTS-C at **0.586**. 61.9 is an
EXAMPLE VALUE in `stages/2-script.md`, and it had been absorbed as a fact. Read
the number out of the data every time.

**LOOK at the render.** A run that exits 0 and prints numbers is not a run that
produced a good artifact — this repo has three separate incidents on record.

## 5. Publishing

⚠️ **DO NOT PUBLISH ON AN AUTONOMOUS RUN.** Produce, verify, and QUEUE.

nordyl was un-paused on 2026-08-19 after being dormant, and its queue held eight
posts that had gone stale — they were held, not fired. Nothing here has
published unattended before, and the first thing that does so must be watched by
the owner. Write the artifact and the caption, run §4, put it in
`profiles/nordyl/publish/queue.json` with `status: held`, and say in the report
that it is waiting for a human.

Platforms: nordyl declares NONE, which means no ceiling — Instagram, TikTok,
YouTube, Facebook, Threads are all permitted. That is deliberate and unlike the
video channels; do not "fix" it. Its own log says Facebook is the only surface
currently producing reach.

## 6. Report

State: the subject and why it is inside §3 territory, what you actually read or
measured, every number with its provenance, the §4 checklist result item by
item, what you could NOT verify, and where the artifact is queued.

If you abandoned a subject on a guardrail, **say which rule**. That is the most
valuable line in the report — it is the only evidence the compliance gate works.

## RUN-OUTCOME — the last line of your report, always

End the report with exactly one of these, on its own line:

    RUN-OUTCOME: OK        everything this brief asked for actually happened
    RUN-OUTCOME: PARTIAL   some of it happened — say which, and which did not
    RUN-OUTCOME: BLOCKED   something stopped you — name it
    RUN-OUTCOME: FAILED    it went wrong

The scheduler reads this line and records the job as FAILED for anything other
than OK. **OK means the outcome, not the effort.** A careful run that was
blocked is BLOCKED, and a blocked run that explains itself is the most useful
thing this system produces.
