# Anti-slop

Slop is not one mistake. It is a set of tells that individually look fine and
together say "nobody was here". This is the checklist, with the fix for each.

## The tells, in order of how often they appear

| # | Tell | Why it reads as machine-made | Fix |
|---|---|---|---|
| 1 | Three identical feature cards with icons | the layout is the default of every template ever made | make one thing the hero; give the other two asymmetric weight, or use a real screenshot instead of an icon |
| 2 | Purple/violet gradient on a dark hero | the house style of 2023–24 AI startups | a real product image, or flat ink on paper colour |
| 3 | A rounded card in a rounded panel on a grey ground | three levels of containment saying nothing | flatten: one container, one border, no nesting |
| 4 | Emoji as an icon (🚀 ⚡ ✨) | renders inconsistently, reads as a template | a real icon set, or nothing |
| 5 | "Built for the way you work" / "The future of X" | a headline with no noun | name the category and the buyer |
| 6 | Centred everything, equal spacing everywhere | no hierarchy, so the eye has nowhere to land | one left-aligned column, deliberate asymmetry in scale |
| 7 | Glassmorphism / blur panels | costs performance, signals "demo" | solid surface, real contrast |
| 8 | Icons drawn for products that have real ones | looks like the wrong company | official asset from the brand, or write the name |
| 9 | Two accents, or an accent used for links and buttons and highlights | nothing means anything | one accent, one meaning |
| 10 | Stock photos of people at laptops, handshakes, city skylines | the reader knows they are not your product | real photographs, or no photographs |
| 11 | Constant motion on scroll (parallax on everything) | motion without state change | decorative motion only where there is an effect budget |
| 12 | Placeholder text anywhere in a shipped artifact | obviously unfinished | write the real sentence, or remove the element |
| 13 | A "moment" on a local business page (a shader, a WebGL object) | the wrong register: a cafe is not a product launch | photographs, flat colour, type |
| 14 | Borders of 1px on everything, shadows on everything | no surface hierarchy | pick one method for elevation and stick to it |
| 15 | Text over a busy photo with no scrim | unreadable, immediately | a gradient scrim, a solid panel, or a different crop |
| 16 | The same section structure twice | reads as an unfinished template | deal each section a different composition |
| 17 | Numbers with no source ("10x faster") | an invented metric is the worst kind of slop | a real number, with a real source, or none |
| 18 | Letter-by-letter typing effect on a headline | a 2010s tell | whole words, or nothing |

## The three tests

Run all three. They are fast and they do not lie.

**1. The competitor swap.** Replace the logo and the product name with a
competitor's. If the page still works, it was never *for* anyone. Fix: specificity
in copy, imagery and the one thing.

**2. The cover test.** Cover the headline with your hand. Does the picture alone
say what this is? If not, the image is decoration and the page is a template with a
paragraph.

**3. The thumbnail test.** Shrink to 120 px wide. Can you still tell what is being
sold? If not, the hierarchy is broken — often because the hero is a decorative
gradient and the actual product is a small card below the fold.

## Register: the most common real mistake

The same "expensive" treatment reads as *good* on one kind of business and
*absurd* on another. Getting the register wrong is worse than being plain.

| Kind | What works | What is wrong |
|---|---|---|
| Software / AI / dev tool | its own UI at true size, dense real detail, one shader ground | a stock photo of a "team" |
| Hardware | the object, whole, in a real place, with real scale | a floating render on a gradient |
| Product (food, clothes, furniture) | real photographs, honest colour, the thing in use | a drawn SVG of the product |
| Service (clinic, law, agency) | the people, the work, the address, credentials | a glowing dashboard mockup |
| Place (cafe, bakery, guesthouse) | 12–20 real photographs, the address set large, hours, one action | any effect; any WebGL; any "moment" |

## What "expensive" actually means

Not effects. Rather:

- **Less, done precisely.** One font. Four sizes. One accent. Every value from a token.
- **Real material.** A real product, a real place, a real person, a real number.
- **Tight craft at small sizes.** Optical alignment, consistent optical margin,
  no orphan words, no 1px misalignments, correct apostrophes.
- **Confidence through restraint.** A large headline with nothing competing
  beside it, and a lot of honest space.
- **One deviation.** A single unexpected move — a huge number, an oddly cropped
  photograph, one bold colour — against an otherwise quiet system. That is what
  people remember, and it only works if it is the only one.

## Two that come back from source material, because they are what video slop looks like

Motion work fails differently from page work, and the sources said so before we did. Both of
these were in the material and neither survived the first merge — which is why a render can
now pass every mechanical gate and still read as machine-made.

| # | Pattern | Why it reads as slop | Instead |
|---|---|---|---|
| 18 | **Production metadata as decoration** — `SAMPLE 01`, `TAKE 3`, `FILM 01`, `01 / 04`, version numbers, timecode, HUD corners | It is the look of a design tool, not of a finished piece. The viewer learns nothing and the frame gets busier | Nothing. The frame does not need to cite itself |
| 19 | **A stat card that restates what was just said** — big number over a small label ("Pause 1.57 s") | A number on screen only earns its place if it compares, ranks, or proves something the audio does not already carry. Otherwise it is a wall of self-important decoration | Show the comparison, or cut the card. One number that lands beats five that decorate |
| 20 | **Page chrome** — a name in the corner, `02 / THE STYLE` counters, tracked-caps micro labels, a timecode, a progress bar under a card, a kicker over a headline | The frame is labelling itself instead of saying something. Of everything in the source material this was the most strictly policed — one of the sources shipped a linter that fails a build for a corner label alone | Delete it. An empty corner is empty, and that is fine |
| 21 | **A dashboard for a sentence** — a fake NLE timeline, a graph with a dashed diagonal and a dot, a row of progress bars filling for no reason | Instruments imply data. With no data behind them they are set dressing that invites the viewer to read a chart that means nothing, which is worse than a blank space | Draw the relationship the sentence is actually about, or use the frame for something else |
| 22 | **One idea labelled three times** — corner label, card title and caption all naming the same thing in the same frame | Repetition without addition makes the frame busy and makes the writer look unsure of the first two attempts | One label. The caption already exists and does not need a headline above it |
| 23 | **A sub-label under a headline that restates it** — "Stylize your content with a signature look" under "EDITING STYLE" | The second line exists because the first was too vague | Make the headline do the whole job, or give the second line information the headline does not carry |

20–23 all share a cause: the graphics were designed as *furniture* rather than as *argument*.
The reference that taught the palette was making a claim in every frame; copying its panels
without copying what the panels were doing produces exactly these four.

20, 21 and 23 are now checked rather than remembered. Declare every overlay and the gate
reads it:

```bash
python3 tools/mfe.py gate --file work/master.mp4 --graphics work/graphics.json
```

```json
{"elements": [
  {"id": "value-curve", "kind": "graphic", "t": 6.2,
   "text": "TOTAL VALUE", "smallest_text_pct": 6.0,
   "proves": "money and effort compound, so the total outruns both"},
  {"id": "brand-corner", "kind": "corner-label", "t": 11.5,
   "text": "THE BRAND", "smallest_text_pct": 1.1, "proves": ""}
]}
```

The first element passes. The second fails three times over: it is page chrome, it is under the
type floor, and it does not say what the viewer knows afterwards.


## Pre-ship checklist

- [ ] Could this be a competitor's page with the logo swapped? → fix specificity
- [ ] Renders at 1440 / 1024 / 768 / 390 with no empty frames
- [ ] One accent, one meaning; one type scale; one spacing step
- [ ] Every heading has a noun; every button is verb + object
- [ ] No invented number, quote, logo, address, or screenshot
- [ ] Every external asset has a declared origin
- [ ] All states exist: empty, loading, error, one item, 1000 items, long text
- [ ] Focus rings visible; contrast ≥ 4.5:1 for body text
- [ ] Reduced-motion honoured: no essential information in motion only
- [ ] The one deviation is genuinely only one
