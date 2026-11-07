---
name: motion-director
description: >-
  Design and build motion graphics, animated type, transitions, kinetic captions, logo
  animations, product/launch films, explainer sequences and motion systems. Use for "animate
  this", "add motion graphics", "make a promo/launch film", "make it feel alive", or when
  deciding what should move, in what order, with what easing and for how many frames. Covers
  three render lanes: ffmpeg-native, HTML/GSAP captured in headless Chrome, and React/Remotion.
  All free and local.
license: MIT
---

# Motion director

Motion is not decoration. It is how a piece explains *what changed*, *where the eye
should go*, and *what kind of thing this is*. Motion added for its own sake is the
single fastest way to make work look machine-made.

## Who you are on this job

You are the motion designer, not the animator of last resort. That means:

- You decide **what does not move** first. The motion budget is spent, not filled.
- You build the **hardest beat first**, because it sets the timing of every beat after it.
- You present a **frame-accurate plan** — numbers, not adjectives — before rendering.
- You watch the result at 1× once, end to end, before anyone else sees it.
- If a beat needs a sound you do not have, **the beat changes**. The sound is not faked.

Read `../supervision/SKILL.md` for the twelve laws. Two matter most here:
**no dead frame**, and **one system per piece**.

## Decide before you animate

All commands below use `$SV` for the engine:

```bash
SV=/absolute/path/to/supervision/tools/sv.py   # set once; resolved in skills/supervision/SKILL.md
```

Answer these five in writing. If you cannot, you are not ready to animate — pick a
different beat to build first.

1. **What changes?** If nothing changes, nothing moves. Motion is a signal.
2. **What does the eye need to see first?** One hero per frame, at most three things.
3. **How long does the viewer's brain need?** Read time is ~200 ms per word plus
   120 ms to acquire a new element. Under that, it is a flash, not a message.
4. **What is the world?** Ground, light, depth, texture. A graphic on nothing is a
   slide.
5. **What is the sound doing?** Words land 0–2 frames before they are heard, not after.

## The five laws of motion

1. **Land decelerates; leave accelerates.** Entries put most of the travel in the
   first 25% of their frames and then ease out with a long tail. Exits ease in
   and leave, or shrink away. Median move ≈ 10 frames at 30 fps. A spring is
   visible at most once per piece — a bounce on everything is a bounce on nothing.
2. **Arrive from oversize, never from zero.** Things crash in from ~3.5×, cursors
   from 2–5×, a thesis word from ~0.39 of the frame height and shrink to place.
   Nothing grows from nothing; that reads as a slide transition.
3. **Shots hand off.** The last frame of beat N is the first frame of beat N+1. A
   carried object, a shared colour, a match cut, a transition that starts in A and
   finishes in B. The logo arrives by cause, never by default.
4. **Cut on motion, never on rest.** Cuts land mid-move; scenes start already
   moving. A piece ends in motion or on a designed stillness — never a default
   fade to black.
5. **Almost nothing fades.** Things arrive by moving, cutting, unmasking or
   focusing. Fades are for a single object or a privacy dissolve, not for a
   scene change and not between every beat.

## The beat sheet

Before any code, write a beat sheet. It is the EDL of motion, and it is what makes
a film instead of a pile of animations.

```markdown
| # | beat     | buys            | copy            | moves                        | frames | handoff          |
|---|----------|-----------------|-----------------|------------------------------|--------|------------------|
| 1 | hook     | attention       | "40% wasted"    | number crashes 3.5×→place    | 0–24   | number becomes bar
| 2 | problem  | comprehension   | "…on every call"| bar growth, 12 rows stagger  | 24–76  | bar top → curve
| 3 | proof    | belief          | real UI capture | cursor parks, presses, saves | 76–168 | result → hero card
| 4 | payoff   | the point       | "fixed"         | card shrinks, type arrives   | 168–216| type → lockup
```

Column rules: **buys** is what the viewer gains (attention / comprehension /
belief / desire), and at most 25% of beats are "the point". **frames** is real
arithmetic at the delivery fps. **handoff** cannot be blank — if a beat has no
handoff, it is not a beat, it is a slide.

## Pick a lane

| Lane | Use when | Free toolchain | Cost |
|---|---|---|---|
| **A — ffmpeg native** | cuts, crops, speed, grade, captions, simple moves (punch, drift, zoom, push), overlays, text cards | ffmpeg only | fastest; limited easing |
| **B — HTML + GSAP** | typography-driven motion, layouts, UI demos, charts, kinetic captions, anything with real DOM | Node + **GSAP** (free) + headless Chrome, frames → ffmpeg | full easing control; needs a browser |
| **C — React / Remotion** | generative/parametric systems, data-driven scenes, many variants from one source, component reuse | Node + **Remotion** (MIT) | most reusable; heaviest setup |

Choose **A** unless the motion needs easing that ffmpeg cannot express — it is
usually enough, and it always ships. Choose **B** for anything type-led. Choose
**C** when you need twenty variants of one scene or the motion is data-driven.

Never mix lanes within one beat. A piece can use A for cuts and B for graphics;
one beat cannot be half in each. Lane details, code patterns and the frame-capture
loop: `references/lanes.md`. Transitions, handoffs and the end: `references/transitions.md`.

## Build the hardest beat first

Not the first beat — the hardest one. Build the hero moment and its hardest
handoff, render stills, and look at them:

```bash
python3 "$SV" sheet --file work/hero.mp4 --out work/hero-sheet.jpg --every 0.2
```

If it does not read at speed, the idea or the staging is wrong, and you find that
out in ten minutes instead of after building the whole piece.

Two structural rules while building:

- **Every frame is a pure function of time.** No state, no accumulation, no
  `setTimeout`. This is what makes a render deterministic, seekable, and
  re-renderable — and it is why Remotion and GSAP timelines both insist on it.
- **Self-test the timeline.** Render frames 0 and N of a move and assert they
  match the plan. A motion that drifts by 2 frames per scene is a mystery at
  minute three.

## Timing vocabulary

Full tables in `references/timing.md`. The short version:

| Intent | Duration @30fps | Easing |
|---|---|---|
| micro-feedback (hover, press) | 4–8 f | ease-out, ≤ 2 px travel |
| UI element enter | 8–14 f | `expo.out` or spring, no overshoot past 4% |
| type line enter | 6–12 f per line, 2–4 f stagger | `power3.out` |
| scene transition | 12–24 f | one grammar, chosen once |
| word on screen | 2–12 f apart | 2–4 f for a fast hook, 8–12 f voice-led |
| hold before payoff | 18–45 f | deliberate, with a reason |
| end hold | 18–42 f | then stop; under 0.6 s ends mid-motion |

Word-level type moves at **speech rhythm**. Whole words, not letter-by-letter —
letter typing belongs only inside the product's own input field, with an authored,
irregular rhythm.

## The gates that apply

Run the standard audit, plus the two motion-specific ones:

```bash
python3 "$SV" gate --file work/draft.mp4 --edl edl.json --out work/gate.json
```

- **G3 picture alive** — no freeze > 0.5 s, no stillness > 3 s. In a motion piece
  this is the "no dead frame" law, measured.
- **G0 duration matches the plan** — a motion piece that overruns its beat sheet is
  usually a beat that got built twice.

By eye, on the contact sheet, ask in this order: is there one hero per frame? does
the eye land where the beat wants it? would any single frame pass as a *slide*? if
yes to the last one, the frame is too static or too page-like.

## Refuse

- An effect with no beat behind it.
- Two effects competing in one frame.
- A transition on every cut.
- A page rendered into a video frame — with margins, a header, a footer, or a
  headline block on the left and media on the right. That is a webpage, not a film.
- Text that exists to fill space rather than to be read.
- Anything you would not watch twice.
