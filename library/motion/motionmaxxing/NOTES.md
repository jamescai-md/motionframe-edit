# motionmaxxing — motion graphics, with the slop named and gated

**Licence:** Apache-2.0 · **Source:** https://github.com/Tejashmakwana/motionmaxxing · **Absorbed:** 2026-11-07

## What it is
The most ambitious source here: a motion doctrine plus a computed gate set, built around
the claim that AI motion work fails in predictable, nameable ways. `references/slop.md`
alone is 60k characters of those failures, ranked.

## Rules worth keeping
1. **Judgement decides *what*; craft laws decide *how*.** Never let an easing curve make a
   decision about whether the piece should exist in that form.
2. **"Never ship" is a delete list, not a debate list.** The named slop patterns get
   deleted, not justified. Argue about the idea, not about the gradient.
3. **The twelve reaches** — the reflexive moves a model makes when it has no idea (glow,
   card float, gradient text, particle burst, three-card grid…). Name them out loud while
   reviewing; naming is what stops them.
4. **A motion piece can be gated at all.** Its G0–G5 showed that measuring a render is
   possible; this project took the idea further (G0–G7) and made the gates fail in a
   selftest.
5. **Build the hardest beat first**, because it sets the timing of everything after it.
6. **Know the brand/one true thing before designing the world** — the piece is about
   something, and that something is not the animation.
7. **"Look honestly" pass** before shipping: watch once as a stranger, not as its author.

## What it gets wrong
Enormous (500k+ characters), a heavy toolchain, and paid voice/music dependencies in the
happy path. Its gate idea is stronger than its delivery.

## Where this landed
`design-director/references/anti-slop.md` (1, 2, 3) · `gatekeeper` and `specs/gates.json`
(4 — extended to eight gates) · `motion-director` build order (5) · `design-director`
step 0 (6) · gatekeeper critic brief (7).
