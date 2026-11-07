---
name: taste-memory
description: >-
  Turn corrections into durable rules so the next piece starts where the last one finished. Use
  when the user gives feedback on a result, says "I hate X" or "always do Y", when a project has
  a taste.md, or when starting new work in a project that has been worked on before. Stops the
  same note being given twice.
license: MIT
---

# Taste memory

The reason people keep twenty skills open in a chat is not that no single skill has
the knowledge. It is that **none of them remember anything**. Every session starts
from the median and gets corrected back to the same place.

This is the smallest skill in the suite and the one that changes the most.

## The file

`taste.md` lives at the project root, created by `mfe scaffold`. It is read **before**
any decision and appended to **after** every correction.

```markdown
# Taste — this person's corrections, in their own words

## Global
- No music beds on talking-head pieces. Silence is fine. (replaced: a −22 dB bed)
- End holds ≤ 1.2 s. (replaced: 2.0 s default)

## Pacing
- Cuts land 60 ms after the last word, not 100. (replaced: 30–200 ms guidance, tighter)
- Keep one 1.5 s still before the payoff. (replaced: cutting every gap)

## Captions
- Never ALL CAPS. (replaced: bold-pop default)
- No accent colour on captions, at all. (replaced: active-word accent)

## Sound
- Music ducked to inaudibility under speech, then up 4 dB between sentences.
- No whooshes on cuts. Ever.

## Look
- Grade is neutral; no teal shadows. (replaced: warm_cinematic)

## Never
- Generated images of people.
- Emoji anywhere in a video.
```

## How to write a rule

A rule has three parts, and all three matter:

1. **The instruction, in the user's terms.** "No music beds" — not
   "music_gain_db: none".
2. **What it replaced**, so a future reader knows which default lost.
3. **The scope** — the heading. A caption rule is not a pacing rule.

Bad: `- music: false` (unreadable in three weeks)
Good: `- No music on talking heads. Silence is fine. (replaced: a −22 dB bed)`

## The loop

```
read taste.md          at the start, before the brief, before the footage
  ↓
make the piece
  ↓
take the note          "the end is too long" — as a note, not a setting
  ↓
write the rule         instruction + what it replaced, under the right heading
  ↓
say it back            one line: "End holds now cap at 1.2 s. Noted for next time."
```

The say-back matters: it tells the user the note is durable, which is why they stop
repeating themselves.

## What is a rule and what is not

| Note | Rule? | Why |
|---|---|---|
| "this thumbnail is great" | **no** | a one-off |
| "always pick the more graphic thumbnail" | yes — Look | a preference with direction |
| "cut the second stat" | no | a content decision for this piece |
| "I never want stats in the first 5 s" | yes — Pacing | generalisable |
| "this client's brand is green" | yes — but in `brief.md` | project fact, not taste |
| "use a different font for this" | **ask once**: this piece, or always? | ambiguity is the only time to ask |

The test: **would saying it again next session be annoying?** If yes, it is a rule.

## Rewriting versus appending

Append. Never rewrite history, because a reversal is information:

```markdown
- Captions in caps. (replaced: sentence case, 2026-03)
- Back to sentence case — caps felt shouty at 45 s. (replaced: caps)
```

Two lines that contradict each other, in date order, tell the truth. One line that
silently changed tells a lie about what the person wanted.

## When taste contradicts the laws

Taste outranks style, never correctness or legibility. If a rule would break a law
(captions under the UI, a pop at every cut, a fabricated screenshot), say so once:

> "You asked for captions at the bottom edge. On Reels that is exactly where the
> caption bar sits, so the words will be covered. I've put them 40 px higher and
> noted the reason. Say the word and I'll move them back."

Then follow the instruction, and note the exception in the file.

## Portability

`taste.md` is plain markdown with no schema beyond headings. Copy it between
projects, keep a `global/` version for a person and a per-project one for a client,
and read the specific before the general. It should still be readable in five
years, by a human, without this skill installed.
