# Captions

Captions are infrastructure. They are not a style choice, and they are not
decoration. Roughly four in five social views start muted; if the piece does not
work with the sound off, the piece does not work.

## What they must do

1. **Be readable in one glance** at phone size, in motion.
2. **Stay out of the platform UI.** 9:16 safe zone: ~top 12%, **bottom 23%**,
   right 13%. The bottom band is where the caption bar, handle and CTA live.
3. **Never cover the mouth or chin.** A caption over a moving mouth is unwatchable.
4. **Carry rhythm.** A caption that appears on the word feels synced; one that
   appears 200 ms late feels broken even to a viewer who cannot say why.

## The mechanics that fail silently

- **Output-timeline times.** `output = word_start − segment_start + segment_offset`.
  In this suite that is `mfe captions --remap <source_id>`; never hand-compute it.
- **Language pinned.** Auto-detected language can *translate* instead of
  transcribe. Every downstream timestamp is then wrong.
- **Word-level ASR only** where the script supports it. Phrase-level loses the
  sub-second gap data cutting depends on; normalised text loses the restarts.
- **Captions composite last.** One overlay after the caption layer hides it.
- **Burn for social, sidecar for platform.** Deliver `captions.srt` alongside the
  burned file whenever the platform accepts uploads — access beats styling.

## Style, decided once per piece

| Choice | Calm / editorial | High energy / social |
|---|---|---|
| Case | sentence case | CAPS |
| Words per line | 3–5 | 2–3 |
| Weight | regular or medium | bold to black |
| Accent | none, or one word | the active word, every time |
| Background | none | optional 60% box for busy footage |
| Motion | fade 120 ms | 60–90 ms pop on entry, no bounce |

Four rules that hold in both columns:

- **One accent, one use.** If the accent marks the active word, it marks nothing
  else — not keywords, not names, not numbers.
- **Emphasis is rare.** Two or three emphasised words per 30 s. Everything
  emphasised is nothing emphasised.
- **Contrast is non-negotiable.** White on a bright sky fails. Either a shadow, a
  box, or a different position — never "it's probably fine".
- **No emoji unless the brand already uses emoji.** They render as tofu on some
  devices and read as a template on all of them.

## Layout

```
1080×1920
┌──────────────────┐  ← top 12%: platform header, never content
│                  │
│      picture     │
│                  │
│   CAPTION LINE   │  ← lower third: y ≈ 0.68–0.78
│   CAPTION LINE   │     max 2 lines, 3–5 words each
│                  │
├──────────────────┤  ← bottom 23%: caption bar, handle, CTA
└──────────────────┘
```

Keep the caption block inside the middle of the frame horizontally too — the right
13% is the share/like rail. `mfe captions` derives the character budget from the
frame and the margins so lines do not run under it; the gate rejects any cue whose
box leaves the zone.

## Proofreading

Captions are the most-read text you will ever ship, so they get read twice.

- Build a name list **before** rendering: product names, people, tools, jargon.
  Fix them in one pass, not by catching them in review.
- Numbers: prefer digits for data (`40%`, `2.4×`) and words for small counts
  ("three things"). Never mix in one sentence.
- Strip fillers from captions even when they stay in the audio — `um`, false
  starts, and repeated words read as sloppy. The word *timing* stays; only the
  displayed text changes.
- Do not caption `[music]`, `[applause]` or `[laughter]` unless the platform
  requires it for accessibility.

## Accessibility, honestly

- Burned captions are not accessible captions. Ship the `.srt`.
- If a piece is important, say plainly that a human should verify the transcript
  against the audio for names and numbers, because ASR gets exactly those wrong.
- Contrast and size rules are accessibility rules that happen to also look better.
