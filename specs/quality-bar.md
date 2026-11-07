# The quality bar, as a contract

The bar is written down so that it cannot be quietly lowered — by a model, by a tired
author, or by a reviewer who wants to ship. **addyosmani/agent-skills** calls this
constraint-driven development; here it is executable wherever possible.

## What "done" means

A piece is done when **all** of the following are true. Not "mostly". Not "except the audio".

| # | Condition | Checked by |
|---|---|---|
| 1 | It exists as a file and decodes | gate G0 |
| 2 | It has the exact shape the destination requires | gate G1 |
| 3 | Its loudness is within ±2 LU of target, true peak ≤ −1 dBTP | gate G2 |
| 4 | Nothing freezes for >0.5 s, nothing is still for >3 s unless intended | gate G3 |
| 5 | No unintended black interval | gate G4 |
| 6 | No boundary spike >6 dB over the local body level | gate G5 |
| 7 | Every caption cue is inside the platform safe zone | gate G6 |
| 8 | Every asset declares an origin; nothing generated claims to be real | gate G7 |

Run `sv gate --file <render> --edl <edl.json>` and the report says PASS or FAIL with
numbers. A human "looks fine" is not one of the conditions.

## What "good" means

Correctness is gateable; judgement is not. These are the judgement conditions, and they are
checked by a critic with fresh eyes (`gatekeeper/references/critic.md`):

1. **It has one point** and says it in the first two seconds.
2. **One system**: one type scale, one palette, one motion register.
3. **Nothing is on screen that is not carrying information.**
4. **The cut serves the audio**, not the other way round.
5. **The first version of the idea that works** — not the third, not the safest.
6. **A stranger can say what it was about** after one watch.

## What is never acceptable, at any speed

- A paid dependency, an API key, or an account in the happy path.
- A generated image presented as a real capture.
- A render presented as finished that has not passed its gates.
- A claim in the repository that cannot be checked.
- Copying another project's text or assets where its licence does not allow it.

## How the bar is enforced on this repository

`tools/gate-docs.py` applies the same discipline to the repository itself — links,
frontmatter, generated drift, unfinished text, superlatives without evidence, provenance —
and `--selftest` feeds each gate broken input to prove it can fail. CI runs it on every
push, along with the engine tests, the installer check, and the end-to-end self-audit.

A gate that cannot fail is decoration.
