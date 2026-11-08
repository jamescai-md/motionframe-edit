# Working from a reference

When the user hands you a video and says "this style", they are giving you a grammar, not a
subject. Two things must be separated before you animate anything:

- **Form** — palette, contrast, typography treatment, how things enter, how long they hold,
  what the composition is doing. This is what you copy.
- **Content** — the reference's numbers, its words, its specific story, its subject. This you
  never copy. Borrowing the form of a piece about *your* material, and filling it with *their*
  content, is the single most common way a reference-driven edit turns into impersonation.

## 1. Measure it, do not eyeball it

```bash
python3 tools/mfe.py style --ref reference/animation-1.mp4 --out work/reference.style.json
```

This writes what a file can tell you: aspect, the span that actually has picture (references
often end with a black tail), edit count and cadence, longest hold, mean luminance, and the
palette with the share each colour occupies.

## 2. Name the grammar by hand — the tool cannot

Watch the frames once and write three sentences:

- **Entry** — how does an element arrive? Draw-on, fade, scale, wipe, nothing at all?
- **Hold** — how long does a composition sit before it changes? The measured
  `longest_static_s` is the answer for the reference; match it within ~25%.
- **Exit and transition** — hard cut, morph, or does the previous element stay and the new one
  grow out of it?

Anything you cannot state in one sentence is not a rule yet, and you cannot follow it.

## 3. Write the three-column table before building

| Must match | May adapt | Must not copy |
|---|---|---|
| palette and its proportions | exact hex values, if the brand dictates otherwise | the reference's numbers |
| type treatment (weight, letterspacing, case) | the family, if licensing demands | its copy, captions or script |
| hold length and cadence | timing around your own audio | its subject or story |
| how graphics enter | whether an element is drawn or revealed | its logo, icons that belong to it |

## 4. The decoration test still applies

A reference's graphics carry *its* content. Copying the form and leaving the content empty
gives you a beautiful frame that says nothing — the failure mode is a stat card holding a
number the viewer just heard in the voiceover. Before building each element:

> "After this, the viewer knows ______ that they did not know from the audio."

If the blank repeats the voiceover, cut it. A reference cannot license decoration; it can only
license *style*.

## 4b. Copy the construction, not the furniture

There are two ways to take a style from a reference, and only one survives being looked at.

**Furniture** is what the frame is made of: a dark card, a neon accent, contour lines, a
tracked-caps label, a thin rule, a glow along one edge. It is easy to copy, and copying it
gives you a frame that is recognisably in the reference's family and says nothing — a panel
with a title, a subtitle and a diagram-shaped decoration. This is the specific way an agent
fails at style transfer: it works from stills, so it reproduces what the frames are made of
and not what they do.

**Construction** is how the reference makes its claim. In the reference this repo was tested
against, every frame does the same thing: it puts objects into a *relationship* and lets the
relationship carry the sentence. Money, effort and time are three icons; a curve joins them;
the total lands at the end of the curve. Nothing on the frame is a label *for* the frame.

Before you build a card, finish this sentence:

> This frame shows ______ related to ______, and the relation is the point.

If you cannot finish it, you are about to build furniture. Four things follow:

1. **The objects are the nouns of the sentence.** If the voiceover says "editing style", the
   card needs the things a style is made of — a cut, a grade, a sound — not a generic timeline.
2. **Something must join them.** A curve, a bracket, a sequence, a number that counts, a
   before-and-after. The join is the graphic. The panel it sits on is not.
3. **Nothing labels the card itself.** No `02 ·`, no section name, no brand in the corner. The
   caption already tells the viewer where they are, every second, for free.
4. **The join should move.** If the relationship is visible in a single frame with no motion,
   you have built a slide. A slide inside a film is the tell that the graphics were made
   separately from the edit.


## 5. When the reference has no subject and yours does

A pure graphics reference applied to footage with a person in it is a hybrid, and the mix is a
decision you have to state out loud:

- graphics as a **layer** over the subject (captions, annotations, punch-in emphasis), or
- graphics as **structure** around the subject (full-frame cards between beats), or
- both, with a rule for when each happens.

Say which you chose and why. An unstated mix is how a talking head ends up with a launch-film
overlay pasted on top of it.

## 6. Gate it against the reference, not against a generic rule

```bash
python3 tools/mfe.py gate --file work/master.mp4 --style work/reference.style.json
```

`G8 pace` takes its limit from the reference's own longest hold once a style spec is supplied —
imitating a slow piece is not a defect. `G9 reference match` reports how much of your picture
sits inside the reference's palette, and fails an aspect change outright: a style transfer that
changes the frame shape is a new piece, not a transfer.

Both gates measure form. Whether the graphics earn their place is the decoration test above,
and it is your call, not the tool's.
