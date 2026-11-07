# Gates for design and stills

The video gates are measured by a script. These are judged by eye, but they are
**binary** — no sliding scale, no "mostly fine". Either the check passes or the
piece is not done. Nine of them, and a piece that fails three is a rebuild, not a
patch.

| Gate | Check | How to test |
|---|---|---|
| **D0** | Every visual renders | screenshots at 1440, 1024, 768, 390 — no empty frames, no placeholder boxes |
| **D1** | Legibility | body ≥ 16 px; contrast ≥ 4.5:1 body, ≥ 3:1 large and UI borders; nothing under 12 px |
| **D2** | Hierarchy | squint at 120 px: can you tell what is being sold, and what to do? |
| **D3** | One system | one type scale, one accent with one meaning, one spacing step, one radius family; no raw values in components |
| **D4** | Specificity | swap the logo for a competitor's — does the page still work? If yes, fail |
| **D5** | Content reality | no invented number, quote, logo, address, testimonial, screenshot; every asset declares an origin |
| **D6** | States | empty, loading, error, one item, 1000 items, 40-char unbroken text, missing fields, offline |
| **D7** | Accessibility | focus visible on every interactive element; `prefers-reduced-motion` respected; no information in colour or motion alone |
| **D8** | The one deviation | exactly one unexpected move against a quiet system. Zero is plain; two is noise |

## Why these and not "does it look nice"

"Nice" is not checkable, so it is not a gate. Each of the nine above can be
answered yes or no by someone who did not make the piece, which is the only
definition of a gate that matters.

## Fast procedure

```
1  Screenshot all four widths. Look at all four, at 100%, not zoomed out.
2  Squint / shrink to 120 px. One sentence: what is this selling?
3  Grep for raw values:  #[0-9a-f]{3,6}   [0-9]+px   [0-9]+ms
   Every hit outside the token file is a D3 failure.
4  Tab through the page. Is focus visible on every stop?
5  Force the states: rename the data, empty the list, break the image URL.
6  Turn on reduced motion. Does anything become invisible or unusable?
7  Read the copy aloud. Any sentence a competitor could also say?
```

## Report format

```
D0 pass  — 1440/1024/768/390, all visuals render
D1 pass  — body 17px, contrast 7.1:1
D2 fail  — at 120px it reads as "software"; the product is not visible above the fold
D3 pass  — 0 raw values outside tokens.css
D4 fail  — competitor-swap test passes: copy is category-level, not specific
D5 pass  — 1 image, origin declared
D6 warn  — empty and error states exist; 1000-item state untested
D7 pass  — focus visible, reduced motion honoured
D8 warn  — no deviation; the page is correct and forgettable
```

Two failures and one warning is a real verdict. It is also a plan.
