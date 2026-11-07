# Craft notes: springs, choreography, performance

## Springs in practice

A spring has three useful parameters and no more: **stiffness**, **damping**, **mass**.
Think in behaviour, not numbers:

| Feel | stiffness / damping / mass | Use |
|---|---|---|
| precise, near-instant | 400 / 30 / 1 | controls, toggles |
| natural, slight settle | 260 / 24 / 1 | sheets, modals, cards |
| lazy, heavy | 170 / 20 / 1 | large surfaces, drawers |
| playful (use once, never twice) | 300 / 16 / 1 | one hero moment |

Rules:

- **Overshoot ≤ 4%** for anything with text in it. Text that bounces past its
  resting position is unreadable for 100 ms, and 100 ms is a long time.
- **Settling time matters more than curve shape.** If it takes more than ~600 ms to
  be visually at rest, it is too slow, whatever it looks like frame by frame.
- **Springs do not take a duration.** If your API wants both a spring and a
  duration, you are holding two contradictory models; pick one.
- Never run a spring on a value a user is currently dragging.

## Choreography

A group of elements moving together needs a lead, a follow, and something still.

```
lead      the hero: 100% of the travel, longest tail
follow    the supports: 40% travel, stagger 2–4 f
still     the ground: 0
```

- **Overlap, do not queue.** Start element 2 at 70–80% of element 1's duration.
  Fully sequential feels like a loading sequence; fully simultaneous has no lead.
- **Stagger is a rhythm, not a constant.** 2–4 frames per item, capping the total
  under ~12 frames; beyond that the eye follows the stagger instead of the content.
- **Direction follows reading order** (left→right, top→bottom) unless the content
  has its own flow — then follow the content.
- **Interrupt gracefully.** If the user acts mid-choreography, snap everything to
  its end state instantly rather than finishing the show.

## Gesture physics

```
commit if:  distance > 35% of the travel  OR  velocity > 0.5 px/ms in that direction
otherwise:  spring back with the sheet's own spring

drag:       1:1, no easing, no smoothing
boundary:   rubber-band at ~12% of travel, then asymptote
release:    decide in one frame, animate from current position
cancel:     reverse from current position (never from 0)
```

The single most common gesture bug: releasing and animating back to the *start*
instead of continuing from where the finger left it. That one bug makes an
interface feel broken even when the rest is perfect.

## Performance audit

1. **Record a performance profile** while doing the interaction, on 6× CPU
   throttling. Not on your machine at 1×.
2. Look for **long frames** (> 16.7 ms) and read what caused them: layout, paint,
   or composite. Composite-only means the animation itself is fine.
3. Check for **layout thrash**: reading `getBoundingClientRect()` inside a scroll or
   drag handler, then writing styles. Batch reads, then writes, or use
   `ResizeObserver`.
4. Check for **layer explosion**: too many `will-change` declarations, or
   `transform: translateZ(0)` sprinkled everywhere. Each layer costs memory; on a
   low-end device this is where the jank lives.
5. Check **image decoding** — a large image first rendered during an animation is an
   instant dropped frame. Decode before you animate (`img.decode()`).
6. Re-test with **reduced motion on** and with the network throttled.

## Accessibility, concretely

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

That rule handles the crude case. It is not enough on its own, because:

- Content revealed by scroll must be visible without the observer firing
  (a `no-js`/reduced-motion fallback that sets `opacity: 1`).
- A state change signalled only by motion (a shake for "wrong") must also have a
  text or colour change.
- Focus movement must never depend on an animation completing. Move focus
  immediately; animate the visuals around it.
- Auto-playing motion over 5 s needs a pause control.

## The invisible details that read as quality

Cheap to add, immediately felt:

- The press state starts on `pointerdown`, not on `click`.
- Hover out is faster than hover in (by ~30%).
- A sheet's backdrop and its content do not move together; the backdrop lags.
- Focus rings never disappear, and they are drawn inside the layout so they do not
  shift the page.
- Scrolling is not hijacked; anchors scroll smoothly only if the user asked for it.
- A list that changes while off-screen does not animate when it comes back.
- The cursor changes on the whole hit target, not just the label.
