# Security policy

## What this project is, security-wise

`motionframe-edit` runs **entirely on your machine**. The engine
(`tools/mfe.py`) has no network code at all: no `urllib`, no HTTP client, no
telemetry, no update check. It shells out to `ffmpeg` and reads/writes local files.

The only network access in this repository is in the optional tooling the docs
mention (e.g. `yt-dlp` for fetching clips), which you install and run yourself.

## The security model you should actually care about

- **Never put an API key in a project.** This repo does not need one, and a lint rule
  fails the build if a paid-API pattern appears in a skill.
- **Treat generated commands as code.** The skills tell an agent to run `ffmpeg`,
  `whisper-cli` and similar. Review what an agent is doing in your project, especially
  anything writing outside the project folder.
- **`sv`/`sv` write only inside the paths you pass.** Temp work goes to a system
  temp directory and is removed.
- **`install.sh` only creates symlinks** (or copies, with `--copy`) into agent skill
  directories. It needs no root and touches nothing else. Read it — it is ~120 lines.

## Supported versions

The latest release on `main` only. This is a single-track project.

## Reporting a vulnerability

Open a [private security advisory](https://github.com/jamescai-md/motionframe-edit/security/advisories/new)
rather than a public issue.

Please include: what you ran, what you expected, what happened, and the output of
`python3 tools/mfe.py doctor --json` (it contains no secrets — the paid-key check
reports only variable *names* that are set, never their values).

Expect an acknowledgement within a week. This is a small project maintained in the
open; there is no bug bounty.
