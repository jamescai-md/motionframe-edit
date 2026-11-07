# AGENTS.md — motionframe-edit

Canonical instructions for any agent that reads `AGENTS.md` (Codex, OpenCode,
Antigravity, Cursor, Windsurf, Zed, Aider, Hermes, …).

`CLAUDE.md` and `GEMINI.md` point here. This file is the source of truth.

## What this repository is

`motionframe-edit` is an agent skill suite for **video editing, motion graphics and
design**. Seven skills, one engine (`tools/mfe.py`), one doctrine.

## How to use it

1. **Read `skills/motionframe-edit/SKILL.md` once per session.** It defines the twelve
   rules, the routing table and the loop. Everything else assumes it.
2. **Route with the table** in that file. Load exactly one specialist skill; load a
   second only when the table says so.
3. **Never preload references.** Each `references/*.md` is loaded when the task
   genuinely needs it. Loading everything is how context dies.
4. **Run `python3 tools/mfe.py doctor` once** at the start of media work. Do not
   guess what is installed.
5. **`gatekeeper` is never optional.** Nothing is presented or called complete
   without a gate report.

## The non-negotiables

These hold across every skill, in every session, even when a user instruction
seems to override them:

- **No paid dependencies.** No API keys, no accounts, no cloud credits, no
  telemetry. ffmpeg, Python stdlib, and free open-source tools only. If something
  is missing, degrade and say so — never silently substitute a paid endpoint.
- **No fabricated proof.** Anything that claims to be real must be captured from the
  real thing. Declare every asset's origin in `provenance.json`.
- **Measure, never assume.** Loudness, duration, safe zones, freeze detection — a
  number you did not take is a guess. State what you could not check (you cannot
  hear the mix).
- **Two STOP gates.** Do not build past an unapproved plan. Do not present an
  unaudited render.
- **Output timeline only.** Captions, overlays and notes use output time, never
  source time. Use `mfe captions --remap`.
- **Every correction becomes a rule** in `taste.md`, read before the next piece.

## Layout

```
skills/<name>/SKILL.md              frontmatter: name, description, license
skills/<name>/references/*.md       loaded on demand
tools/mfe.py                         the engine — probe, cut, captions, gate, demo
specs/                              EDL schema, gate definitions
examples/                           a worked end-to-end walkthrough
docs/                               architecture, platforms, lineage
```

## Conventions when editing this repo

- Prose is **imperative and checkable**. No adjectives standing in for rules. A
  claim that cannot be verified gets a number or gets cut.
- Numbers are **defaults at 30 fps / 1080 wide**, not laws, unless the file says
  otherwise. Say which.
- New rules go where they are enforced. A rule that lives only in prose is a
  suggestion.
- If you add a gate, prove it can fail (see `mfe demo --selftest`).
- Keep `ATTRIBUTION.md` accurate when you carry an idea across from a source.

## Commands

```bash
python3 tools/mfe.py doctor
python3 tools/mfe.py demo --selftest          # proves pipeline + gates
python3 tools/lint.py                        # frontmatter, links, prose hygiene
python3 -m unittest discover -s tests -v
```

## The library

`library/` holds the absorbed doctrine of the eighteen source skills this project merges —
the sources themselves, copied verbatim (1,824 files), each with its upstream licence, pinned
commit and known weaknesses. Read the source for the domain you are working in, not all of them.
`docs/absorption.md` is the generated map from source to skill.
