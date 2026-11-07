# Timing

Numbers here are starting points at **30 fps**, not laws. They are what "feels
right" distilled into something you can type. Deviate with intent, not by accident.

## The three curves you actually need

```
ease-out  (expo/power3.out)   enters, decelerates   ← most arrivals
ease-in   (power2.in)         exits, accelerates   ← leaving shots
ease-in-out (power2.inOut)    A→B repositioning    ← moves that stay on screen
```

Everything else is a variant. Rules:

- **Arrivals** never bounce more than 4% past their target. A UI card that
  overshoots 20% looks broken; a logo that overshoots 4% looks alive.
- **Exits** are ~60% the duration of the matching entrance. Leaving is cheaper
  than arriving, and it keeps the piece moving.
- **Springs** are for physical things the user touched (a drag, a tap, a sheet).
  One spring per piece, at most. A spring on a text line reads as a toy.
- **Linear** is only correct for continuous loops (a marquee, a turntable, a
  progress fill during a real wait).

## Duration by role

| Role | Frames | ms | Notes |
|---|---|---|---|
| press feedback | 3–5 | 100–170 | must feel instantaneous |
| hover / focus | 4–8 | 130–270 | travel ≤ 2 px |
| tooltip / popover | 8–12 | 270–400 | origin-aware, scale from the trigger |
| modal / sheet | 14–24 | 470–800 | one spring, backdrop fades slower |
| text line in | 6–12 | 200–400 | stagger lines 2–4 f |
| word-level type | 2–12 between words | — | 2–4 fast, 8–12 voice-led |
| image / card entrance | 10–18 | 330–600 | arrive from oversize, never 0 |
| number count-up | 12–30 | 400–1000 | step per frame, land on the spoken value |
| scene change (cut) | 0 | 0 | free, invisible, always available |
| scene change (dissolve/mask) | 12–24 | 400–800 | only on a change of world |
| hold before payoff | 18–45 | 600–1500 | needs a stated reason |
| end hold | 18–42 | 600–1400 | under 0.6 s ends mid-motion |

## Stagger and choreography

Stagger is how a group reads as one thing instead of a list:

- **Rows/lines:** 2–4 frames apart, total under 12 frames. More than that and the
  eye follows the stagger instead of the content.
- **Grids/cards:** 1–2 frames per item, diagonal order, total under 20 frames.
- **Subordination:** the hero moves 100%, its supports 40%, the ground 0%. If
  everything moves, nothing leads.
- **Overlap:** start the next element at 70–80% of the previous one's duration.
  Simultaneous is mechanical; strictly sequential is slow.
- **What stays still** is a choreography decision. Choose at least one thing that
  does not move, so the movement has a reference.

## Easing tables by feel

Because "make it snappier" is a direction, not a number:

| Direction | Change |
|---|---|
| snappier / punchier | duration ×0.7, keep the curve, add 0–2 f of anticipation |
| slower / more premium | duration ×1.4, switch to expo.out, reduce travel |
| more playful | one small overshoot (≤4%), stagger ×1.5 |
| more expensive | less travel, longer tails, fewer simultaneous moves |
| less busy | delete a move entirely before shortening it |

**Deleting a move is almost always the right answer to "too busy".**

## The read-time budget

The viewer needs time to *acquire* and time to *read*:

```
acquire  ≈ 120 ms   (a new element appearing somewhere new)
read     ≈ 200 ms/word  (short words are cheaper, numbers are slower)
```

So a 4-word claim needs ~0.9 s on screen after it has settled, and a number needs
~0.5 s. Anything under budget is a flash; anything over 3× budget is a pause that
reads as an error. This is why "no more than 3–4 s without a change" works in
short form: the budget runs out before the patience does.

## Frame-exactness checks

Three checks catch nearly all motion bugs:

1. **First frame of a move** is the intended start pose — not 20% in.
   For ffmpeg overlays that means `setpts=PTS-STARTPTS+T/TB` shifting the overlay
   so its frame 0 lands on the window start.
2. **Last frame** is the settled pose, fully resolved, no half-eased remainder.
3. **Determinism**: render the same frame twice; it must be identical. If it is
   not, some state leaked into the animation.
