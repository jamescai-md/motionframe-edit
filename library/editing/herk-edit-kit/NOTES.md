# herk-edit-kit — HyperFrames edit kit: silence rules, review gates, handoffs

**Licence:** none stated (NOASSERTION) — **summarised, not redistributed** ·
**Source:** https://github.com/nateherkai/herk-edit-kit · **Absorbed:** 2026-11-07

## What it is
A 210-file Codex/Claude kit built on HyperFrames: `cut-silences`, `cut-mistakes`,
`hyperframes-video-beats`, a full GSAP reference set, and a habit of writing `HANDOFF.md`
files between agents. Strongest on the mechanics of silence cutting and on the idea that a
cut proposal must be *reviewed before it is applied*.

## Rules worth keeping
1. **Silence cutting is mechanical, then reviewed.** Find candidates by measurement, then a
   gate step that a human or agent must pass before any cut is applied. Never auto-apply.
2. **Silence decisions are tunable, and the tuning is written down** (minimum gap, padding
   either side, what counts as speech). Defaults are a starting position, not the truth.
3. **Handoffs are written, not implied.** When one agent finishes a stage, the next needs a
   file with what was built, how to run it, and what is still broken.
4. **Verify numerically, not by eye** — the `HANDOFF.md` files repeatedly assert this, and
   list the specific traps (mask defeating a curve, `immediateRender: false`, animating
   layout properties instead of transforms).

## What it gets wrong
Bound to the HyperFrames runtime, and its register is agency-promo throughout. Much of its
content is project handoffs for specific films, which is context, not doctrine.

## Where this landed
`motion-director/references/transitions.md` (the trap list) · `edit-supervisor` cut-review
step (1, 2) · `docs/` handoff convention (3) · gatekeeper's "numbers, not eyeballs" (4).
