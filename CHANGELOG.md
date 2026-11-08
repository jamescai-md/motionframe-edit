# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com); versioning follows
[Semantic Versioning](https://semver.org).

## [1.0.0] — 2026-11-07

First release. Eighteen video-editing, motion-graphics and design skill repositories read
together, their disagreements decided in writing, and their source text kept next to the
decisions so the merge can be checked.

### Added

- **Seven skills** — `motionframe-edit` (routes between the others and settles conflicts),
  `edit-supervisor`, `motion-director`, `design-director`, `ui-motion`, `gatekeeper`,
  `taste-memory`. Each loads only when its job matches; nothing is preloaded.
- **`library/`** — all eighteen sources under their own terms: 1,824 files, 13.4 MB, each
  folder carrying its upstream URL, licence, pinned commit and its known weaknesses.
  Fourteen are copied under an explicit licence grant; four are copied on the maintainer's
  stated permission, recorded in `PERMISSION.md`.
- **`tools/mfe.py`** — one file, standard library plus `ffmpeg`: probe, cut, caption, mix,
  measure. No network code, no keys.
- **Eight gates** (G0–G7) on every render, with `mfe.py demo --selftest` feeding them
  deliberately broken input and failing the build if they do not catch it.
- **`tools/gate-docs.py`** — the same discipline applied to this repository's own
  documentation: links, frontmatter, generated files, honesty of claims.
- Installation for Claude Code, ChatGPT/Codex, Gemini CLI, Antigravity, OpenCode, and any
  tool that reads `AGENTS.md`.

### Notes

- The root MIT licence covers this project's writing only. Copied sources keep their own
  terms — see `NOTICE`, including Remotion's company-size threshold and hypit's commercial
  conditions.
- Renders are validated against a synthetic fixture, not real camera footage. That is the
  first item in `docs/plan.md`.
