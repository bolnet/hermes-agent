# Permission boundary — binds every scheduled run

Adopted 2026-08-17 after a cron run escalated to `computer_use` and
osascript-driven Safari control, spraying macOS permission dialogs. The owner's
rule: **the mission needs research, content tools, a browser, and its own
repo — nothing wider.** Full autonomy stands *inside* this fence; the fence
itself is enforced in config and code (`.hermes-home/config.yaml`
`agent.disabled_toolsets` + `approvals.deny`), so a run cannot talk itself
past it. Do not try: denied commands log to `logs/cron_activity.jsonl` and
retrying a denial is treated as an incident.

## Allowed — everything the mission needs

- **Research**: web/search toolsets, `curl` to public APIs, reading anything
  under the project workdir.
- **Content creation**: the platform's content tools (image/video/tts/vision),
  `ffmpeg`, python scripts under the project, writing to the project
  workspace.
- **Publishing**: exactly two routes, one per surface.
  - **LinkedIn — the platform browser toolset** (`browser_navigate` and
    friends, the managed browser). There is no LinkedIn API here.
  - **X — the official X API via `xurl`** (OAuth 1.0a, credentials in
    `workspace/.env`). Amended 2026-08-18 with the owner's approval. This is
    not a widening: the API can do strictly less than a browser signed into
    the same account — it posts as `@surendra_ai` and nothing else, with no
    browsing, no other sites, and no session to leak. The fence's target is
    OS control, not the official API of a declared surface.

  Either way: post only to the declared surfaces, download
  results/analytics **into the project workspace** (never `~/Downloads`) and
  review them with the vision tools.
- **Self-improvement**: edit code under this repo, `git` commit/branch/push,
  `gh` PR create and merge, adjust its own cron schedule (cronjob toolset).

## Forbidden — never needed, permanently denied

- `computer_use` / `desktop_ui` — driving the screen or other apps. Removed
  from the toolset registry; do not look for substitutes.
- `osascript` / AppleScript / `open -a` — controlling Safari or any app.
- macOS privacy & persistence: `tccutil`, TCC.db, `launchctl`, `crontab`,
  `defaults write`, LaunchAgents/LaunchDaemons.
- Other processes & privilege: `sudo`, `killall`, `pkill`.
- Personal data outside the project: `~/Documents`, `~/Desktop`,
  `~/Downloads`, `~/Pictures`, `~/.ssh`, `~/.aws`, `~/.gnupg`, Keychain.
- System configuration: `networksetup`, `systemsetup`, `csrutil`, `spctl`.

## When a step seems to need a forbidden capability

It doesn't. Find the in-boundary route — between the browser toolset and the X
API, everything posting requires is covered — or record the blocker in the run
report as output. A blocked run that explains itself is a success; an escalation
is the only real failure.

⚠️ The two publishing routes above are the complete list. "The X API is allowed,
so presumably the LinkedIn one is too" is exactly the reasoning this fence
exists to stop: each route was named individually, after being checked
individually. A new route is the owner's decision, never a run's.
