# Changelog

All notable changes. Format loosely follows [Keep a Changelog](https://keepachangelog.com);
this project uses [Semantic Versioning](https://semver.org).

## [1.0.0] — 2026-11-07

First release. Eighteen editing, motion and design skill repositories merged into one agent
skill, with the bookkeeping that makes "merged" checkable.

### Added

- **Seven skills** — `motionframe-edit` (router: twelve laws, precedence ladder, two STOP gates),
  `edit-supervisor`, `motion-director`, `design-director`, `ui-motion`, `gatekeeper`,
  `taste-memory`. Progressive disclosure: each loads only when its job matches.
- **`library/`** — one digest per source, eighteen in total, each with what the source is,
  the rules worth keeping, what it gets wrong, and where every kept rule landed.
  **89 rules kept and given a home**; the rest rejected as redundant, tool-specific, or a
  contradiction already settled in `precedence.md`.
- **`tools/absorb.py`** — verifies every digest has its four sections, and generates
  `docs/absorption.md` from the digests so the coverage table cannot drift.
- **`specs/quality-bar.md`** — what "done" means written as a contract: eight measured
  conditions plus six judgement conditions.
- **`docs/plan.md`** — the plan this repository was built against: settled, open, excluded,
  phased.
- **`tools/mfe.py`** — the engine: `doctor`, `probe`, `scaffold`, `validate`, `render`,
  `captions`, `gate`, `sheet`, `demo`. Standard library plus an `ffmpeg` binary.
- **Eight gates** G0–G7 on every render, and `demo --selftest` feeds them deliberately
  broken renders and fails if they pass.
- **`tools/gate-docs.py`** — the same discipline applied to the repository: D0 first screen,
  D1 links, D2 frontmatter, D3 generated drift, D4 unfinished text, D5 unqualified
  superlatives, D6 provenance. `--selftest` proves each can fail. Wired into CI.
- **Platform adapters** — Claude Code, ChatGPT/Codex, Gemini CLI, Antigravity, OpenCode,
  Hermes, plus anything that reads `AGENTS.md`.

### Fixed (relative to the first build of this idea)

- **Provenance is verified, not asserted.** `tools/verify-sources.py` resolves every source
  link and compares the stated licence with the forge: 18/18 today.
- **`taste-skill` credit restored.** Its "kind of business decides everything" *is* its
  section 1; an earlier retraction was the error, caused by reading its README instead of
  its skill file.
- **Five sources are not MIT/Apache**, not two: `remotion`, `hypit`, `herk-edit-kit` report
  `NOASSERTION`; `anthropics/skills` and `apple-design-skill` carry no licence file. None of
  their text is redistributed — the digests are original summaries.
- **Correct repositories:** `Moh4696/freecut`, `emilkowalski/skills`,
  `DietrichGebert/ponytail` — all per the brief.

### Known limits

- Renders are validated against a synthetic `testsrc2` fixture, not real footage. Stated in
  the README, not buried.
- Design digests are summaries; the editing and motion digests were built from rule-level
  reading. `docs/absorption.md` says which is which.
