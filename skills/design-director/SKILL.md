---
name: design-director
description: >-
  Art direction for pages, products, UIs, posters, decks, thumbnails and brand systems — and the
  critique of work that looks "AI-made", templated, generic or over-designed. Use when designing
  or reviewing anything visual that is not primarily footage or motion: landing pages, app
  screens, brand identity, type and colour systems, layout, imagery and asset policy. Enforces
  the anti-slop rules and resolves conflicting taste advice with one precedence ladder.
license: MIT
---

# Design director

The failure this skill exists to prevent is not ugliness. It is **genericity**: the
page, deck or poster that could belong to any company, made of the same rounded
cards, the same purple gradient, the same three-feature grid, and the same
confident sentence that says nothing.

The bar, in words: a good company would ship this, and a stranger could tell who it
is for.

Read `../motionframe-edit/SKILL.md` for the twelve rules. Rule 8 (the precedence ladder)
and law 9 (one system) do most of the work here.

## Step 0 — name the kind of thing it is

Most design failures are a mismatch between kind and treatment: a shader effect on
a bakery, photographs on a developer tool. Decide the kind first, in writing, and
let it drive every later choice.

| Brief | Kind | The page leads with |
|---|---|---|
| app, SaaS, AI, dev tool, fintech | **software** | its own real UI, at true size, doing the actual work |
| game, game studio | **gaming** | the game's world, full-bleed key art |
| hardware, device, gadget | **tech-product** | the object, whole, big, in a real setting |
| any other physical product | **product** | the product photographed or rendered, big |
| clinic, law firm, agency, studio | **service** | the people and the work |
| cafe, bar, bakery, guesthouse, shop | **place** | 12–20 real photographs and the address |

Then apply the consequences, which are strict:

- **Place** gets photographs, flat colour, type, real icons and a quiet hover layer.
  **No** shader effects, no gradient grounds, no "moments", no scenes.
- **Software/gaming/tech** may spend the one-effect budget — a shader ground, one
  WebGL object, one big scene — because the subject is technical and the audience
  expects it.
- **A physical product with no photographs** gets a render (or a diagram), never a
  stock mood shot and never a drawn SVG pretending to be the product.

## Step 1 — the one thing

Write, in four lines, before any layout:

```
Problem    what is broken or missing for this audience
Audience   who specifically, and what they already believe
Goal       the one action this page or piece exists to cause
Emotion    the one feeling that makes the action easy

Then: the ONE real thing this is about — a feature, a moment, a photo, a claim.
```

If the one thing is vague ("we help teams collaborate better"), the design will be
vague no matter how good the typography is. Fix the sentence, then design.

## Step 2 — material, honestly

Inventory what actually exists: logo (official file), screens, photographs,
prices, address, hours, real numbers, real quotes. Then place each on the asset
ladder and never skip down more than one rung:

```
real capture / real photograph
  → official asset from the brand
    → render or diagram of the real thing
      → typographic treatment
        → generated image (never implying reality)
```

Two rules with no exceptions:

- **Never invent facts.** No invented metrics, logos, testimonials, addresses or
  phone numbers. If a number is needed and missing, write less, not fiction.
- **Never fabricate proof.** A generated image may be a mood, a texture, an
  impossible object. It may never be a screenshot, a dashboard, a person's words,
  or a product that does not exist. Declare it in `provenance.json`.

## Step 3 — the system, before the page

```
grid        one column count, one gutter, one max width
type        one family (two at most), one scale, ≤ 4 sizes in use
colour      neutrals + exactly one accent with exactly one meaning
space       one spacing step (4 or 8 px) — no 13px, no 27px
radius      one value, or two (control, container)
elevation   at most two levels, and prefer a border to a shadow
icon        one icon set, real product icons where a real product is named
```

Write it as tokens and use only tokens. Details and the exact scales:
`references/system.md`.

The test: change one token, and the whole piece should update coherently. If a
value is hardcoded anywhere, the system is decorative.

## Step 4 — layout that behaves

- **One idea per screen.** A hero alone on the first screen; each section one or
  two screens tall at 1440×900; no second section heading peeking in.
- **Equal content edges** left and right. Asymmetry must be a decision with a
  reason, not a default that drifted.
- **One focal point per frame** — one hero, at most three elements competing.
- **Empty space must do a job.** If it is empty because nothing filled it, that is
  a hole, not whitespace.
- **Every visual renders.** No placeholder boxes, no empty image frames, at any of
  1440 / 1024 / 768 / 390 px.
- **The mobile view is the design**, not a squeezed desktop.

## Step 5 — copy is design

Half of "this looks AI-made" is the words. The rules:

- The headline names the category and the buyer, or the place. Not a feeling.
- One hard fact on the first screen — a number, a name, a price, a location.
- A noun in every heading. "Built for the way you work" is a mood; "Offline-first
  notes for field crews" is a page.
- Buttons are a verb and an object: "Book a room", "Start free trial",
  "Get directions". Never "Learn more" as the primary action.
- 60–80 words per screen for software; fewer for a place, where photographs speak.
- No sentence that could appear on a competitor's page unchanged. That test kills
  most copy, and it should.

## Step 6 — the polish layer

This is where work stops feeling generated. All of it is cheap, none of it is
optional:

- A linked card lifts 1–2 px on hover; a photograph zooms 1.02–1.03 inside its frame.
- Buttons step on hover, compress 1 px on press. Focus rings are visible and never
  removed.
- Underlines draw on hover, from the same direction as reading.
- Transitions are 130–270 ms and never animate layout properties.
- Every state exists: empty, loading, error, one item, a thousand items,
  unbroken text (a 40-character email), missing fields, offline.
- The tab title, favicon, social card and 404 exist and match.

Motion specifics for interfaces: `../ui-motion/SKILL.md`. It is the authority on
timing; this skill is the authority on everything around it.

## Step 7 — look, then fix

1. Screenshot at 1440, 1024, 768, 390. Look at all four.
2. Squint at the thumbnail. Can you tell what is being sold? If not, the hierarchy
   is wrong — not the type size.
3. Cover the headline. Does the picture still say something? If not, the image is
   decoration.
4. Swap the logo for a competitor's. If the page still works, the design is generic.
   That is the test, and it is brutal by design.
5. Fix in order: untrue or broken → the idea → hierarchy → spacing → type → colour
   → surface → motion.

The anti-slop checklist, with the exact tells and their fixes:
`references/anti-slop.md`. Read it before shipping, not before starting.

## Refuse

- Three identical feature cards, or a three-column grid with icons.
- A gradient as a button, a border, or text.
- Two accents, or an accent with no meaning.
- Stock photography of people pointing at laptops.
- An emoji as an icon; a drawn icon for a product that has a real one.
- Centred body text; justified text; grey-on-grey.
- A carousel, a timed tab switcher, a scroll-jacked section.
- Placeholder copy, lorem ipsum, or "Coming soon" where the real thing belongs.
- A dark hero and a gradient glow because the reference had one.

## Deliver

For a page: the files, plus a one-screen `DESIGN.md` recording the kind, the one
thing, the tokens, the asset provenance, and what you could not verify.

For a critique: verdict, ranked problems with evidence (a screenshot region or a
number), and the five fixes to do first. Never a compliment sandwich — say what
works once, then spend the rest on what does not, with fixes.
