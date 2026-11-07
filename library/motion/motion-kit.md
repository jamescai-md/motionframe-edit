# motion-kit — the motion designer's role, in one small skill

**Licence:** MIT · **Source:** https://github.com/hughminhphan/motion-kit · **Absorbed:** 2026-11-07

## What it is
Tiny compared to its neighbours (three files) and better for it: a role definition, a
work loop, and a library of curves, springs, timings and *devices*.

## Rules worth keeping
1. **Pick a register first** — editorial, product, broadcast, playful — before choosing any
   curve. Mixed registers are what "off" looks like.
2. **Devices are chosen, never stacked.** One move per beat: a wipe *or* a scale *or* a
   mask, not all three.
3. **Curves have provenance.** Use a named curve from a known system rather than an
   invented one; the library lists them by source.
4. **Springs where the object has mass, duration+easing where it has none.**
5. **Timing is content.** Its timing table is short and specific; copy the numbers, not the
   adjectives.
6. **The role is defined by refusals**: decide what does not move; build the hardest beat
   first; never ship unwatched.

## What it gets wrong
Thin: no verification, no gates, and it assumes a designer is driving. It also leaves
"register" undefined enough to be interpreted away.

## Where this landed
`motion-director/SKILL.md` §"Who you are on this job" (6 — written verbatim-ish in this
project's voice) · `references/timing.md` (1, 3, 4, 5) · `references/transitions.md` (2).
