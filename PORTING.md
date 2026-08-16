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

## Steps 4 and 5 — not started

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

**The collision is not today, it is at step 4.** The browser is machine-wide —
one persistent Chrome on one profile behind one lock, plus one residential IP.
A money-stories task here and `com.agent-platform.sequential.daily` would fight
over it. So retire that launchd job at the moment the Hermes task takes over
publishing, and not before: it is the only thing on this machine currently
producing anything, and a replacement that does not exist yet cannot cover it.

## Status

    [x] 1. fork + upstream remote
    [x] 2. Claude subscription, no API key            verified 2026-08-16
    [x] 3. multiple tasks on one tick                 verified 2026-08-16
    [ ] 4. money-stories as a task
    [ ] 5. nordyl as a task
    [ ] gateway install (nothing fires automatically until this runs)
