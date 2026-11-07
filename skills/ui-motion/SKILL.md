---
name: ui-motion
description: >-
  Interface animation and interaction craft — deciding whether something should animate at all,
  then how: timing, springs, choreography, gestures, reduced motion and frame-budget performance.
  Use when building or reviewing app/website motion, popovers, sheets, drag interactions, page
  transitions, hover and press feedback, or when an interface feels "floaty", "cheap", "slow" or
  "janky". Apple-grade fluidity on a web frame budget.
license: MIT
---

# UI motion

An interface that moves well feels physical and inevitable. One that moves badly
feels like a slideshow with opinions. The difference is almost never the library.

## Should it animate at all?

Ask in this order. The first "no" means do not animate it.

1. **Did something change that the user did not do?** → animate it in (they need to
   know it appeared, and where from).
2. **Did the user just do it?** → animate only if the change is instant-but-continuous
   (a drag, a knob, a scroll). Continuity, not decoration.
3. **Is it on a high-frequency surface?** (a key repeat, a table sort, a keystroke,
   a hover trail) → **no.** Frequency and motion are inversely proportional: the
   more often it happens, the less it should move.
4. **Does it communicate a relationship?** (this panel came from that button; this
   row moved to that list) → yes, and the motion must show the relationship.
5. **Is it purely decorative?** → no, unless it is the one moment the piece is
   allowed and it costs no frames.

## The timing table

| Interaction | Duration | Notes |
|---|---|---|
| press / tap feedback | 100–170 ms | must feel instantaneous; transform only |
| hover | 130–270 ms | travel ≤ 2 px; never animate box-shadow |
| tooltip | 270–400 ms | origin-aware, no delay on show if it followed a click |
| popover / dropdown | 270–400 ms | scale from the trigger corner, 0.96 → 1 |
| sheet / modal | 470–800 ms | one spring; backdrop fades 1.4× slower than the panel |
| page / route | 200–400 ms | content in, chrome stays put |
| list reorder | 200–350 ms | items move along the shortest path |
| expand / collapse | 250–400 ms | animate `transform` + `scaleY`, never `height` |

Above 800 ms is a deliberate, watched moment. Below 100 ms nothing is perceived
as motion — either use no transition, or make it 130 ms and feel intentional.

## The four rules that prevent "floaty"

1. **One spring, at most, per view.** Springs are for physical things the user
   manipulated. A spring on a text label reads as a toy.
2. **Motion is proportional to distance.** A 4 px move is not 400 ms. Above 40 px of
   travel, add no more than 100 ms per additional 100 px.
3. **Everything that enters exits the same way.** Same curve, same duration,
   reversed. Consistency is what reads as craft.
4. **The end pose is exact.** No half-eased remainder, no 0.998 scale. Set the
   final state explicitly.

## Origin and relationship

The most legible motion in an interface is *where things came from*:

- A popover scales from the corner nearest its trigger, not from its centre.
- A detail view expands from the card that was tapped (a shared-element
  transition), not by sliding in from the right edge.
- A moved row animates along the path it actually took.
- A deleted item shrinks toward the trash, or toward where it went — not straight
  down and out.

If you cannot state the relationship, the animation is decoration. Delete it.

## What to animate (and what never to)

**Animate:** `transform` (translate, scale, rotate), `opacity`, `filter` (sparingly —
blur is expensive), `clip-path` (for reveals).

**Never animate:** `width`, `height`, `top`, `left`, `margin`, `padding`, `border-width`,
`box-shadow`, `background-position`, or anything that forces layout or paint on
every frame. These are the reason interfaces feel janky on real hardware.

Never `transition: all`. It is the same thing as "animate whatever happens", which
is what "cheap" means.

## Gestures

- **Track the finger 1:1** while dragging. Any easing during the drag feels broken.
- **On release, decide in one frame:** commit if past threshold or fast enough
  (velocity matters more than distance), else spring back.
- **Interruptible.** A second gesture during an animation takes over from the
  current visual position, never from the animation's start.
- **Rubber-band past the boundary** by ~12% of the travel, then resist.
- **Haptic/visual acknowledgement on the frame the gesture is recognised**, not
  when the animation completes.

## Reduced motion is not optional

Respect `prefers-reduced-motion: reduce`:

- Remove all decorative motion, parallax, and auto-playing movement.
- Keep state changes, but make them instant, or use a 100 ms opacity change.
- **No information may be conveyed by motion alone.** If the user cannot see the
  animation, they must still understand the outcome.
- Never hide content behind an intersection-observer reveal that also fails for
  reduced motion — the classic bug where the page looks empty.

## The frame budget

At 60 fps you have 16.7 ms per frame. Real hardware (a mid-range Android, a
thermal-throttled laptop) has less. So:

- Composite-only properties keep the work off the main thread.
- Blur, large shadows, and 3+ simultaneous transforms will drop frames.
- Animate at most 2–3 elements simultaneously; stagger the rest.
- Test with 6× CPU throttling. If it holds, it ships.

Details, spring maths and a performance audit procedure: `references/craft.md`.

## Reviewing motion (yours or someone else's)

Do not say "feels off". Say which of these it is:

| Symptom | Likely cause | Fix |
|---|---|---|
| floaty | duration too long, or easing too soft | ×0.7 duration, `expo.out` |
| cheap | spring on everything, or `transition: all` | one spring max, explicit properties |
| janky | animating layout/paint properties | transform/opacity only |
| confusing | origin or relationship unstated | animate from the trigger |
| slow | over 400 ms on a frequent interaction | halve it |
| distracting | high-frequency surface, or no state change | remove it |
| broken | end pose inexact, or not interruptible | set final state, take over on gesture |
| inaccessible | motion is the only signal | add a static state change |

Default to flagging. Approval must be earned, not inferred.
