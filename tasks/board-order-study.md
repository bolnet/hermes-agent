# board-order — daily study session (~30 minutes)

You are studying the competition so that today's production run knows something
it did not know yesterday. **This is not a production run — you do not make a
video.** You watch, measure, and write down what you found.

    workdir   /Users/aarjay/projects/hermes-platform/workspace
    python    .venv/bin/python
    profile   board-order            (export HERMES_PROFILE=board-order)
    channel   Board Order · @boardorder · UCFwQGCLYS-dZ4e3QAQp3I-Q
    output    profiles/board-order/LEARNED.md   (append, dated)
              profiles/board-order/styles/*.yaml (update in place)
    boundary  tasks/PERMISSION-BOUNDARY.md

**Timebox: about 30 minutes.** Depth beats coverage. One video measured properly
is worth more than twelve skimmed — the entire style registry rests on ONE
video that was measured frame by frame.

## Why this session exists

The channel improves by measuring things, not by having opinions. Every number
in `styles/clean-board.yaml` came from a session like this one, and the format's
two most useful findings were both counter-intuitive and would never have been
guessed:

  * every cut is a WHIP, so ffmpeg's scene detector finds nothing at all
  * the reveal order is ARBITRARY (6, 5, 2, 4, 3, 1) — not a countdown

## 1. Catch the RISERS — the point the owner raised

*"That will capture the new popular video as well."* Yes — and that is the most
valuable thing this session does. A format that is working right now, on a small
channel, is worth more than a year-old megahit from a large one.

**Method — rank CHANNELS by views-to-SUBSCRIBERS, then take each channel's top
Short.** Do NOT keyword-search for ranking Shorts: it is a polluted term and
returns 1-view spam and unrelated videos. Discover channels, then their videos.

    discover   channel search with the channel filter (&sp=EgIQAg%3D%3D)
    score      top Short's views / channel subscribers
    keep       ratio high AND views large enough that the ratio means something

⚠️ **Discard tiny denominators.** 19K views off 95 subs scores 204x and is
noise. The two real signals found so far were 1750x on 171M views and 531x on
18.3M. Require at least ~500K views before a ratio is worth anything.

⚠️ Raw views would have picked a 16.3M-view video from a 610K-sub channel, where
the AUDIENCE carried it rather than the format. That is the trap this ranking
avoids.

**Track what is NEW.** Keep a dated list of every channel scored, so next
session can see which ones are climbing. A channel whose ratio is rising is a
format in ascent, and that is the earliest signal available.

## 2. Measure ONE thing properly

Pick the single most promising find and measure it, or advance an existing style
from `characterised` toward `measured`. `caption-rank` is the current candidate
and its yaml lists exactly what is missing.

**The measurement method, learned the hard way:**

    MEASURE AT NATIVE RESOLUTION. At 360x640 a 55px glyph is 14px and one
    threshold choice moves the answer 30% — the header read 8.75% instead of
    12.50%. Geometry survives downscaling; fine detail does not.

    CUTS: whips are gradual, so a scene detector sees nothing. Find them as
    peaks in frame-to-frame difference AND as troughs in per-frame sharpness,
    and check the two agree.

    TYPE: convert cap-height to font-size (~/0.72 for Montserrat).

    REVEAL ORDER: READ THE BOARD at several timestamps. A brightness test is
    fooled by white sky and white shirts, which register as "label present"
    exactly like a label does.

    CROSS-CHECK anything that could be faked by the footage. The header height
    was verified on a dark AND a bright frame, because dark footage fakes a
    taller black bar.

## 3. Check our own numbers

Pull views, retention and views-per-subscriber for everything published, and
compare each video against ITS OWN style's reference. Record the comparison even
when it is unflattering — especially then.

    first upload: https://www.youtube.com/shorts/Qh3XFyu2Vp0  (2026-08-18)

## 4. Write it down

Append to `LEARNED.md`, dated, with numbers:

    channels scored, with ratios, and which are new or rising
    what was measured, and what changed in which style file
    what our published videos did, against their references
    what did NOT work — a measured loss is worth more than an untried idea
    what to do next session

⚠️ **Never blend two styles.** If you find a technique in one reference that
would "improve" another, that is a NEW style, recorded separately with its own
reference. Owner: *"clone one video style completely, don't mix two."* A blended
video cannot be compared against anything, so nothing can be learned from it.

⚠️ **A session that exits 0 and prints numbers is not a session that measured
the thing.** State plainly what you actually opened, measured and compared, and
what you only skimmed.

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

