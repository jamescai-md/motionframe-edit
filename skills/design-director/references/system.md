# The system

A design system is not a component library. It is the small set of decisions that
make every later decision cheaper and more consistent.

## Type

**One family.** Two only if one is a display cut of the other. Free, high quality,
open-licensed: Inter, Source Sans 3, IBM Plex, Instrument Sans, Fraunces,
Newsreader, JetBrains Mono.

```
scale (1.25 ratio, fluid between 390 and 1440)
  display   clamp(2.5rem, 6vw, 5rem)     leading 0.95–1.05, tracking −0.02em
  h1        clamp(2rem, 4vw, 3rem)       leading 1.05,      tracking −0.015em
  h2        clamp(1.5rem, 2.5vw, 2rem)   leading 1.15,      tracking −0.01em
  body      1rem–1.0625rem               leading 1.55,      tracking 0
  small     0.875rem                     leading 1.45
  mono      0.875rem                     for code, data, IDs
```

Five rules that do 80% of the work:

1. **Body text never below 16 px**, never above ~72 characters per line.
2. **Left-aligned.** Centred body copy and justified text are tells.
3. **Optical size relationships:** the display is 3–5× the body, not 1.6×. Weak
   contrast in scale is what "corporate" means.
4. **Never two weights in one line**, and never bold for more than ~8 words.
5. **Correct punctuation**: curly apostrophes, en dashes for ranges, no double
   spaces, no ALL CAPS for a long heading (tracked caps only for ≤ 3 words).

## Colour

```
ink-900  #0E0E10   text, primary
ink-600  #52525B   secondary text
ink-300  #D4D4D8   borders, dividers
paper    #FAFAF9   ground
surface  #FFFFFF   cards when a card is genuinely needed
accent   #     1  THE accent — one meaning, stated in DESIGN.md
semantic ok/warn/error — not accents, never decorative
```

- **One accent, one meaning.** "This is actionable", or "this is AI", or "this is
  on". Pick one. Not all three.
- **Contrast:** body ≥ 4.5:1, large text ≥ 3:1, UI borders ≥ 3:1 against their
  own background. Grey-on-grey is a defect, not a style.
- **Dark mode is a second design**, not an inversion. Surfaces are lighter than
  the ground, elevation comes from lightness not shadow, and the accent usually
  needs desaturating.
- **Gradients** are a ground, never a control. One per piece. Never on a place page.
- **Colour is never the only signal.** State must have a shape, an icon or a label
  too.

## Space

One step. 4 px, or 8 px. Everything is a multiple.

```
2 4 8 12 16 24 32 48 64 96 128 192
```

Section padding: 96–192 px desktop, 48–96 mobile. Component padding: 8–24.
Gap between related items: 8–12. Between groups: 32–48. Between sections: 96+.

**Whitespace is hierarchy.** If two elements are 20 px apart, they read as related.
If they are 96 px apart, they read as separate ideas. Nothing should be 37 px apart.

## Grid and measure

- 12-column grid, one max width (1080–1280 px for marketing, 1440 for apps),
  one gutter (24–32 px).
- Equal left and right content edges. Full-bleed elements break the grid on
  purpose and only once or twice.
- Stack to one column below 768 px, and check that the *order* still makes sense —
  mobile is not a squeezed desktop.

## Surfaces, radii, elevation

- Pick one containment method: a border, or a background change, or a shadow.
  Mixing all three is the "rounded card in a rounded panel" tell.
- One radius for controls, one for containers (or a single value for both).
  Pills for tags and avatars only.
- Two elevation levels maximum. Prefer a 1 px border over a shadow for anything
  that is not actually floating.
- Never nest more than one rounded container.

## Icons and imagery

- **One icon set**, one stroke width, one corner treatment. Real product logos only
  from official files — never redrawn, never generated.
- Photographs: real ones, cropped decisively, at least two per screen on a product
  page, and a different picture in every section.
- Every image has a `width`, `height` and a meaningful `alt`. Decorative images use
  `alt=""`.
- Aspect ratios from a small set (1:1, 4:5, 3:2, 16:9). Mixed ratios in one row is
  the fastest way to look unfinished.

## Tokens or nothing

```css
:root {
  --ink: #0E0E10; --ink-2: #52525B; --line: #D4D4D8;
  --paper: #FAFAF9; --surface: #FFFFFF;
  --accent: #1F6FEB;            /* one meaning: "actionable" */
  --step: 8px;
  --r-control: 8px; --r-container: 16px;
  --f-display: clamp(2.5rem, 6vw, 5rem);
  --t-fast: 130ms; --t-base: 200ms; --t-slow: 270ms;
  --ease-out: cubic-bezier(.16,1,.3,1);
}
```

If a raw hex, a raw px and a raw ms appear in a component, the system has failed
and the piece will drift. Grep for them before you ship.
