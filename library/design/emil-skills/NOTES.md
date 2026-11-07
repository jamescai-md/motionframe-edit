# emil-skills — interface motion craft

**Licence:** MIT · **Source:** https://github.com/emilkowalski/skills · **Absorbed:** 2026-11-07

## What it is
The best interface-motion material available: a build sequence that starts by questioning
whether anything should animate, then picks the cheapest tool and the right property.

## Rules worth keeping
1. **Step 1 is "should this animate at all?"** Most interface motion is added to cover a
   missing state, not to explain a change.
2. **Purpose before easing**: explain a change, direct attention, or acknowledge input. If
   it does none of the three, delete it.
3. **Cheapest tool that works** — CSS transition before a library, transform before
   layout, one property before five.
4. **Animate `transform` and `opacity`**; never animate layout properties.
5. **Duration vs spring by nature of the object**: springs for things with mass and for
   interruption; durations for fades and state changes.
6. **Design the interruption and the exit**, not just the entrance. Most "janky" motion is
   an entrance with no plan for being interrupted.
7. **`prefers-reduced-motion` and pointer gating are not optional**, and on touch it is
   press, not hover.

## What it gets wrong
React/web only; nothing about film, footage, or motion graphics with a timeline. It is
about *interface* motion and says so.

## Where this landed
`ui-motion/SKILL.md`, almost whole (1–7) · `motion-director/references/timing.md` (5) for
the spring/duration distinction · gatekeeper's "should it move" check (1, 2).
