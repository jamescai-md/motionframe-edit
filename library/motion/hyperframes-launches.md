# hyperframes-launches — worked launch films, and the traps that bit

**Licence:** Apache-2.0 · **Source:** https://github.com/heygen-com/hyperframes-launches · **Absorbed:** 2026-11-07

## What it is
Real launch films built with HyperFrames, each with a `HANDOFF.md` recording the build, the
run commands, and the bugs that were actually hit. The handoffs are the value: a trap list
with receipts.

## Rules worth keeping
1. **Verify numerically, not by eye.** Every handoff says it, and the film is checked at
   specific timestamps rather than "looks right".
2. **The trap list** (each cost someone a day): a mask can defeat a cut-curve; never animate
   `left/top/width/height` — animate transforms; `transform-origin: 0 0` is load-bearing;
   CSS transform and GSAP fighting over one element; `immediateRender: false` on seek;
   assert every string replacement; count `<div>` after any splice.
3. **Build order is the beat sheet**: hardest beat first, then the rest against it.
4. **Sequence consistency across cuts** — a chat scene that resets between shots is the
   most common structural bug in explainer films.

## What it gets wrong
Examples, not transferable rules — the doctrine has to be extracted, which is what this
file is doing. Heavy on one runtime's specifics.

## Where this landed
`motion-director/references/transitions.md` and `lanes.md` (2 — the trap list) ·
`gatekeeper` (1) · beat-sheet format (3) · `motion-director` (4) as the scene-continuity check.
