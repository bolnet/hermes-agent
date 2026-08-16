# Running Hermes on the Claude subscription

`upstream` is `github.com/nousresearch/hermes-agent`. `origin` is our fork,
`github.com/bolnet/hermes-agent`. Diff against upstream with
`git diff upstream/main`.

The goal is the one the previous attempt got wrong: money-stories and nordyl as
**tasks inside an agent that owns them**, not as a fixed pipeline on a timer.

## Why this exists — what the previous attempt actually did

`agent-platform` was never a fork of Hermes. Its first commit (2026-08-08) is a
channel pipeline; it merely *lived in a directory* under the Hermes checkout at
`~/projects/hermes/money-stories` and was moved out on 2026-08-09 by commit
`fc87fc2`, which touched two files and deleted nothing.

What was lost was not code. It was **two cron jobs**, still sitting disabled in
`~/.hermes/cron/jobs.json`:

    money-stories-daily          0 8,18 * * *   enabled=False
    money-stories-weekly-review  0 9   * * 0    enabled=False

The daily one opens:

> *You own this channel end-to-end (full autonomy granted by the user Aug 2026
> — never ask permission, just produce and publish).*

That sentence is the entire difference. `agent-platform` replaced these with one
launchd slot running a fixed five-stage list, which cannot schedule itself,
cannot retry, and carries no autonomy grant — so a human re-enters the loop on
every decision and every failure.

Both jobs also point at paths that no longer exist (`render/out/`,
`~/projects/hermes/money-stories`). They cannot simply be re-enabled.

## Step 2 — the subscription. Already upstream; verified here.

**No API key is required and none was added.** Upstream already reads Claude
Code's refreshable OAuth credentials:

    agent/anthropic_adapter.py:1040   read_claude_code_credentials()
                                        1. macOS Keychain, "Claude Code-credentials"
                                        2. ~/.claude/.credentials.json
                                      prefers the fresher token; deliberately
                                      excludes ~/.claude.json primaryApiKey
    hermes_cli/model_setup_flows.py:3025   setup flow detects existing creds
    hermes_cli/providers.py:315            "claude-code" -> anthropic

Verified on this machine 2026-08-16 — keychain entry present, no credentials
file, Claude Code 2.1.233 (the version whose refresh quirk that function
documents):

    $ hermes -z "Reply with exactly: SUBSCRIPTION OK" \
             --provider anthropic -m claude-sonnet-4-6
    SUBSCRIPTION OK

So the port is not "build subscription auth". It is configuration, and it is done.

## Install — venv OUTSIDE the source tree

Upstream's own warning, and it is not theoretical: a venv inside the directory
the agent operates from can be wiped by a relative-path command the agent runs
against its own checkout, destroying the runtime mid-session.

    uv venv ~/.hermes/venvs/hermes-platform --python 3.12
    VIRTUAL_ENV=~/.hermes/venvs/hermes-platform uv pip install -e ".[all,dev]"

## HERMES_HOME is isolated, on purpose

    export HERMES_HOME=/Users/aarjay/projects/hermes-platform/.hermes-home

The machine already has a working Hermes at `~/.hermes`, configured for
`moonshotai/kimi-k3` via OpenRouter and holding the two disabled money-stories
jobs. Sharing that home would mean this project's config changes silently
rewrite a live install's provider, and a mistake here would cost the record of
how the old jobs were written. Isolation is cheap; that history is not.

Config in the isolated home:

    hermes config set model.provider anthropic
    hermes config set model.default  claude-sonnet-4-6

## Subscription ONLY — no OpenRouter, and why the home was rebuilt

The first build of this home came up reporting `Provider: OpenRouter`, and
`auth.json` had grown a `credential_pool.openrouter` entry. Nothing configured
it: Hermes imports credentials it finds in the environment, and
`~/.zshrc` sources `~/.zshrc.local`, which exports `OPENROUTER_API_KEY`. So an
inherited shell variable had quietly enrolled a paid per-token provider in a
project that is supposed to run on the subscription alone.

A config value would not have removed it — the credential was in the pool, and a
pool entry is what a fallback reaches for. The home was deleted and rebuilt with
the variable unset for the command that creates it:

    rm -rf "$HERMES_HOME" && mkdir -p "$HERMES_HOME"
    env -u OPENROUTER_API_KEY -u OPENAI_API_KEY HERMES_HOME=... hermes config set model.provider anthropic
    env -u OPENROUTER_API_KEY -u OPENAI_API_KEY HERMES_HOME=... hermes config set model.default  claude-sonnet-4-6

Verified after:

    credential_pool providers : ['anthropic']
    config.yaml               : no openrouter, no kimi, no moonshot
    hermes -z "..."           : SUBSCRIPTION ONLY OK

**Run every command for this project with those variables unset**, or the pool
re-populates on the next write. `~/.zshrc.local` is deliberately left alone —
the money-stories pipeline still needs ELEVENLABS_API_KEY from the same file.

## Step 3 — multiple tasks. Verified.

Two jobs, different schedules, one tick, both delivered locally:

    hermes cron create "every 1h" "Reply with exactly: TASK-A OK" --name smoke-a --deliver local
    hermes cron create "every 2h" "Reply with exactly: TASK-B OK" --name smoke-b --deliver local
    hermes cron run <id>            # marks due
    hermes cron runs <id>           # completed

Outputs landed in `$HERMES_HOME/cron/output/<job>/<timestamp>.md`, each carrying
`TASK-A OK` / `TASK-B OK`. Both smoke jobs were then removed — they are
reproducible from the commands above and would otherwise fire hourly once a
gateway runs.

Note the delivery contract Hermes injects into every scheduled run: produce the
report as the final response, and answer exactly `[SILENT]` when there is
genuinely nothing to report. A task that has nothing to say should say nothing.

## The task model, from a real job spec

`hermes cron create` accepts far more than a prompt, and steps 4-5 depend on it:

| field | why it matters here |
|---|---|
| `--workdir` | each channel is a different checkout |
| `--skill` (repeatable) | `broll-matching` is already a skill; attach it |
| `--script` | deterministic work behind an allowlisted entry point |
| `--no-agent` | watchdogs with no LLM at all |
| `--monitor-script` / `--monitor-url` | unchanged output suppresses the run entirely |
| `--model` / `--provider` | per-task tier |
| `--deliver` | origin, local, telegram, … |
| notepad | durable KV across runs (`hermes cron notepad`) |

`--monitor-script` is the one worth planning around: a cheap script runs each
tick BEFORE the agent, and an unchanged hash suppresses the agent run entirely.
That is how a daily channel check costs nothing on a quiet day.

## Step 4 — money-stories. Task created, wiring verified.

    job       7ff39695b6fb  money-stories-daily
    schedule  0 8 * * *     (the slot the retired launchd job held)
    workdir   /Users/aarjay/projects/agent-platform
    script    money-stories-brief.sh
    deliver   local

**The task definition lives in git, not in `jobs.json`.** `--script` injects the
script's stdout into the prompt on every run, so
`$HERMES_HOME/scripts/money-stories-brief.sh` simply cats
`tasks/money-stories-daily.md` from this repo. An edit to that file takes effect
on the next run — no `cron edit`, and the definition stays reviewable,
diffable and revertible. If the brief is missing the script says so and tells the
agent to stop rather than improvise a production run.

The brief carries the autonomy grant from the original 2026 job — produce, check
and publish without asking — plus one section the old pipeline never had:

**§4 LOOK at the render.** Build a 6x4 frame grid, open it with the vision tool,
and ask of every panel whether the footage shows what the headline claims. Prove
the audio is audible. Every silent failure this channel shipped passed every
numeric check that existed: a modern iPhone under "NOKIA OWNED 40% OF PHONES",
confetti reading "Hooray!" over a $7.6bn write-off, a card at -91 dB, a
made-for-kids flag nobody set on purpose. `vision` is an enabled toolset, so this
is finally checkable by the thing doing the work.

Verified without producing anything — a throwaway job on the same script, told to
report readiness and stop:

    workdir       /Users/aarjay/projects/agent-platform     correct
    entry points  produce, upload, publish_verify, audience_audit, clip_sheet   all present
    public_stats  12 videos live, v15 leading at 2153
    ffmpeg        8.1 at /opt/homebrew/bin/ffmpeg
    verdict       GO

It also found something unprompted, which is the §1 "check BOTH lists" rule
earning its place on the first run: **v15 and v16 are live with no script in
`scripts/json/`**, so a slug-collision check against that directory alone would
have been wrong about them. Next slug is v18.

The throwaway job was then removed. Approval model checked first: pipeline
commands run without prompting, `rm -rf /` is hardline-blocked even under
`--yolo`, so a scheduled run cannot hang on a confirmation and cannot be talked
into something catastrophic.

## money-stories is otherwise complete

    7ff39695b6fb  money-stories-daily    0 8 * * *   skill: broll-matching
    4160f8125c33  money-stories-weekly   0 9 * * 0

Both briefs live in `tasks/` in this repo and reach the agent through
`--script`, so editing a brief changes the next run.

`broll-matching` is registered as a **local** skill by symlinking
`$HERMES_HOME/skills/broll-matching` at
`agent-platform/.claude/skills/broll-matching`. A copy would drift; the symlink
keeps agent-platform the single source of truth for a skill that documents that
pipeline's tools.

### The weekly task was run for real, and it worked

Read-only, so it was safe to prove with actual work rather than a dry run. It
pulled stats and retention, judged the format comparison, and **committed
`ab3533d`** — three changes in one commit (its report said "three commits",
which was wrong; verify claims against `git log`, not the report):

- **`retention_loop` read `.error` on a dataclass that carries `.detail`.** The
  attribute did not exist, so `getattr(res, "error", "")` always returned `""`
  and every failed retention call wrote `status: "error", note: ""`. That empty
  note was the top open defect on the channel — it made the format comparison
  unreadable. Confirmed fixed by re-running it: the note now reads *"no rows —
  this is NOT proof of zero retention"*, which says the Analytics API returned
  zero rows rather than that anything failed. YouTube lags about 48h, which fits
  v15, v16 and v17 exactly.
- Pillar shares rebalanced on 12 videos by age-normalised views/day —
  `corporate_disasters` was the largest target (0.29) and the weakest performer
  (median 2.1 v/day), cut to 0.21; `founder_drama` 0.17 -> 0.25. Sum asserts to
  1.0 in Python, verified independently.
- `automation/daily.md` still quoted the pre-measurement priors; corrected.

It also refused to call the format comparison, correctly: v15 and v14 tell the
same story, so a 5x gap on views/day still cannot separate "StoryCard works"
from "the Winklevoss story works". "Not yet distinguishable" was the right
answer and it gave it.

### One real gap it exposed

It reported v17 as unpublished. v17 had in fact gone live on all three platforms
that morning — but the **record stage never ran**, so nothing wrote
`automation/logs/production.jsonl`. The control test the review was waiting for
was invisible to the reviewer. Recorded retroactively in agent-platform
`8ee5de3`.

`production.jsonl` is the memory across runs, so an unrecorded run is not a
bookkeeping gap: the next pick stage would have been free to repeat the story.

### Browser integration — tested through a task, not assumed

Everything above this point was read-only, which proved nothing about the half
of the pipeline that matters most: the publisher drives a real Chrome. A task
that can read files and call APIs may still be unable to launch a browser from a
scheduled context.

Tested with `automation/check-sessions.py`, which uses the same
`browser.get_context()` the publisher does, visits each platform and reads only
public page state — it never touches credentials and posts nothing:

    YouTube    LOGGED IN
    TikTok     LOGGED IN
    Instagram  LOGGED IN
    Facebook   unclear        (nothing publishes there — money-stories is 3 platforms)

24 seconds, exit 0, no retries. So Chrome launches from a Hermes task, the shared
`browser-profile/` and its lock work, and the sessions the publisher needs are
live. The throwaway job was removed after.

Facebook has never been part of money-stories: `upload.py` has exactly three
publish functions. `post_facebook` exists only in nordyl's separate
`pipeline/publishing/poster.py`, which has published nothing yet.

### NOT DONE — the gateway

`hermes gateway install --start-now --start-on-login` was **refused by this
environment's approval classifier**, twice-flagged and not worked around.
Installing it starts a persistent background service that publishes to live
social accounts on a schedule, which is a standing commitment the operator
should make deliberately.

**Until it runs, neither job fires**, and the launchd job they replace is
already retired — so this machine currently produces nothing. Run:

    export HERMES_HOME=/Users/aarjay/projects/hermes-platform/.hermes-home
    ~/.hermes/venvs/hermes-platform/bin/hermes gateway install --start-now --start-on-login
    ~/.hermes/venvs/hermes-platform/bin/hermes cron status

Meanwhile both jobs run on demand with `hermes cron run <id>`, which is how the
weekly one was proven.

## Step 5 — nordyl. Not started.

4. **money-stories** as the first task.
5. **nordyl** as the second.

Both are ports of working pipelines, so the risk is not whether they run — it is
what they do when they fail. Carry these forward from `agent-platform`, where
each was learned the expensive way:

- **Publishing must not ask.** It is the one thing the old cron job did every
  day without a human. Any port that re-introduces a confirmation has lost the
  feature.
- **Nothing is a guard unless a test fails when it is removed.** Twelve tests in
  `agent-platform` passed while verifying nothing.
- **Measurement is not interpretation.** A cut count is not a shot list; a 200
  response with an empty body is not a zero; an existing audio stream is not
  audible sound.
- **A silent success is the failure mode of this whole system** — a swallowed
  `except`, a made-for-kids flag nobody set on purpose, a −91 dB track, a denied
  command retried until the turn budget died.

## What this project can currently interrupt: nothing

Separate repo, separate venv, separate `HERMES_HOME`, and **no gateway
installed** — `hermes cron` says so on every write: *"Gateway is not running —
jobs won't fire automatically."* Nothing here fires until `hermes gateway
install` runs, which is deliberate.

Scheduled jobs on this machine as of 2026-08-16:

    LOADED  exit=1   com.agent-platform.sequential.daily   08:00  money-stories production
    LOADED  exit=1   com.hermes-for-claude.loop            03:00  skill-evolution loop (already subscription)
    not loaded       com.self-improvement-agent.daily / .weekly / .telegram   stale plists

Both loaded jobs are currently FAILING (exit 1). The agent-platform one died at
its `describe` stage this morning; nothing retried it.

**`com.agent-platform.sequential.daily` was retired on 2026-08-16**, on the
owner's instruction, ahead of its replacement rather than at handover:

    launchctl bootout gui/$(id -u)/com.agent-platform.sequential.daily
    mv ~/Library/LaunchAgents/com.agent-platform.sequential.daily.plist \
       ~/Library/LaunchAgents/disabled/

Booted out and moved rather than deleted, so it cannot reload at login and can
still be read or restored.

**So nothing on this machine now produces content automatically.** That was the
reason to keep it — the browser is machine-wide (one persistent Chrome on one
profile behind one lock, plus one residential IP), so it and a money-stories
task here would have fought over it at step 4. Retiring it early removes the
collision and the producer at the same time. Step 4 is now the only path back
to daily output, which makes it the priority rather than one item of five.

Producing by hand meanwhile still works and is unaffected — the launchd job was
only a timer around `automation/run-profiles-sequential.sh`.

## Status

    [x] 1. fork + upstream remote
    [x] 2. Claude subscription, no API key            verified 2026-08-16
    [x] 3. multiple tasks on one tick                 verified 2026-08-16
    [x] 4. money-stories as a task    job 7ff39695b6fb, 0 8 * * *, wiring verified
    [ ] 5. nordyl as a task
    [ ] gateway install — REQUIRED. Until it runs, job 7ff39695b6fb never fires
        and this machine produces nothing, because the launchd job it replaces
        is already retired. `hermes gateway install`, then `hermes cron status`.
