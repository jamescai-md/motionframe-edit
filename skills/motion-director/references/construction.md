# Construction — from decisions to frames

The rest of this skill decides *what* moves and *why*. This file is the part that gets a frame
out of a browser or out of ffmpeg without it looking wrong, and it exists because the sources
that taught the hard parts had their rules scattered across launch handoffs and none of them
survived the first merge.

## Pick the lane by what has to move

| What moves | Lane | Why |
|---|---|---|
| A cut, a punch-in, a reframe, a slow push | **ffmpeg only** | no browser, no dependencies, renders in seconds |
| Type, layout, charts, SVG line-work, UI | **HTML + GSAP + headless Chrome** | real DOM, real typography, real easing |
| Anything frame-exact, parameterised, re-rendered | **Remotion** (own licence, optional) | React components as frames |

Do not reach for the browser lane to do a punch-in. It is 40× slower and adds a dependency
chain to something ffmpeg already does.

## The four traps that ruin otherwise-good animation

Every one of these comes from launch handoffs in `library/motion/hyperframes-launches/` and
`library/motion/hyperframes/`, where each was learned by shipping a broken frame.

**1. `transform-origin: 0 0` is load-bearing.**
SVG and transformed boxes scale from their centre by default, so a scale animation drifts away
from the point the designer aligned. Set the origin explicitly on every element you animate:
`transform-origin: 0 0` for anything anchored top-left in a layout, `50% 100%` for something
that must squash into the floor or sit on a baseline. A rule in a handoff word for word:
*squash uses `transform-origin: 50% 100%` so shapes compress into the floor contact.*

**2. `immediateRender: false` on entry tweens that share a timeline.**
A paused timeline still applies the *starting* value of every tween it contains the moment the
timeline is built. Positioned elements therefore jump to their start state before the playhead
reaches them — in one launch that put a card 1250 px off-screen. Add
`immediateRender: false` to entry tweens (`from`, `fromTo`) on a timeline you will seek.

**3. Never animate `left`, `top`, `width`, `height`.**
They force layout on every frame, and they break when the composition is resized or re-seeked.
Animate `transform` (`x`, `y`, `scale`, `rotate`) and `opacity`. The one exception is a
deliberate layout change, not motion.

**4. A mask defeats "cut the curve".**
If you mask an element and animate its path, the easing you set becomes invisible — the mask
edge is what the viewer reads. Either animate the mask deliberately or do not mask.

## Draw-on, for line-work and graphs

The technique the reference pieces use for glowing charts and underlines:

```html
<path d="..." stroke-dasharray="440" stroke-dashoffset="440" />
```

```js
gsap.to(".line", { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" });
```

Set `stroke-dasharray` and `stroke-dashoffset` to the path length (measure with
`getTotalLength()`; 440 is a placeholder, not a number to copy). Animate the offset to zero.
For a left-to-right reveal, also set `transform-origin: 0 0`.

## Deterministic capture, then assemble

A browser renders at whatever rate it likes. A video needs frame N on demand:

```javascript
// the page exposes a seek hook; the harness calls it per frame
window.renderAt = (t) => { tl.pause(); tl.time(t); };
```

- Drive the timeline by `tl.time(t)` with the timeline paused, never by real time.
- Capture at the delivery fps (30 or 60), one screenshot per frame.
- Assemble with ffmpeg, and keep the audio out of the browser entirely:

```bash
ffmpeg -framerate 30 -i work/frames/%05d.png -i work/audio.wav \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest work/layer.mp4
```

- Composite that layer over footage with the PTS-shifted overlay pattern in `lanes.md`.

## What to check before you call it built

- [ ] Every animated element has an explicit `transform-origin`.
- [ ] Every entry tween on a seekable timeline has `immediateRender: false`.
- [ ] No tween animates a layout property.
- [ ] The draw-on uses the real path length.
- [ ] Frame N is identical across two renders (determinism) — capture frame 0 and frame 0 again
      and diff them; a difference means something is animating off the timeline.
- [ ] The last frame is a designed still, not whatever the animation happened to end on.
- [ ] `mfe.py gate` passes on the assembled layer before it is composited.

## What this file does not cover

Colour, type and layout decisions are `../../design-director/references/system.md`; whether the
motion is worth making at all is the decoration test in `../SKILL.md`; and pacing against a
reference is `reference-work.md`.
