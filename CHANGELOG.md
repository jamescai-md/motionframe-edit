# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com); versioning follows
[Semantic Versioning](https://semver.org).

## [1.3.0] — 2026-11-08

A render built with this repo shipped with a corner label, a section counter, four play
buttons and a fake timeline in it, and passed every gate. That is the finding: the ten gates
measured delivery, and nothing measured whether anyone had looked at the frame or whether the
graphics were furniture. Two gates and one command close that hole.

### Added

- **`mfe watch`** — samples frames on a budget that scales with the duration (one a second up
  to 30 s, sparser after) and writes `work/watch.md`: one sentence per frame, the five
  design-read questions, a verdict. The notes are a deliverable, not a note to self.
- **G10 `you looked at it`** — fails when the notes are missing, when any sampled frame was
  described in under six words, when a design-read question is unanswered, or when there is no
  verdict. Declared-gate discipline: the table is read back, not trusted.
- **G11 `no page chrome`** — fails a declared overlay that is frame furniture (corner or edge
  label, tracked caps, counter, timecode, kicker, progress bar, bracket, watermark, HUD), that
  puts text under 3.5% of frame height, that cannot say what the viewer knows after it, or that
  restates its own label.
- `mfe gate --notes / --tiles / --graphics / --no-notes`; `specs/gates.json` v1.3.0 at thirteen
  entries.

### Merged from the sources, because the first merge dropped them

- The page-chrome ban, with its full list — one source shipped a linter for this and the
  curated version had reduced it to a single line about self-citing frames.
- The type floor as a measurement of frame height, not of points (`design-director/system.md`).
- **Construction vs furniture** in `motion-director/reference-work.md`: copy how the reference
  makes its claim, not what its panels are made of. Four tests that follow from it.
- **Endings must land** in `cutting.md`: the last six words have to finish the thought.

### Changed

- `gatekeeper/SKILL.md` documents twelve gates and the `watch` step between LOOK and READ.

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
