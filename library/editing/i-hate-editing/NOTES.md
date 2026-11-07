# i-hate-editing — talking-head footage in, publishable package out

**Licence:** MIT · **Source:** https://github.com/ranahaani/i-hate-editing · **Absorbed:** 2026-11-07

## What it is
The most complete single-purpose editing skill in the collection, and the origin of the
"taste memory" idea. Drop in raw takes; get back a cut, captions, a grade, and a delivery
package. Its `HARD-RULES.md` and `rules/{cutting,captions,framing,hooks,assets}.md` are the
most useful rule files here.

## Rules worth keeping
1. **Cut on word boundaries read from the transcript**, not on what sounds like an edge —
   and place the cut in the silence *after* the word, never inside the consonant.
2. **Not every pause is dead air.** Keep thinking pauses (200–400 ms after a question or
   reveal); trim the long gaps between thoughts. Cutting all of them sounds sped-up.
3. **Filler goes, rhythm stays.** Removing every "um" produces a hostile, mechanical read.
4. **Hooks live in the first 1–2 seconds** and must be visual, not verbal.
5. **Captions are burned at the output timeline**, never the source timeline.
6. **Ship a delivery package**, not a file: cut, captions, thumbnail, QA stills, notes.
7. **Hard rules beat taste.** When a rule and a preference conflict, the rule wins and the
   preference gets written down instead.

## What it gets wrong
Enhanced voice requires a signed-in browser, and image handling goes through a local proxy —
two accounts-shaped dependencies in an otherwise local tool. It is also talking-head only:
nothing about design, nothing about graphics.

## Where this landed
`edit-supervisor/references/cutting.md` (rules 1–4, plus the six "what to cut precisely"
rules added after a rule-level audit) · `captions.md` (5) · `delivery.md` (6) ·
`taste-memory` (7) · the accounts dependency is removed: `doctor` offers the local path only.
