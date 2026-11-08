# Delivery

A cut file is not a deliverable. The package is.

```
out/
├── <name>-9x16.mp4       the piece, platform-correct
├── <name>-1x1.mp4        variant (optional)
├── <name>-16x9.mp4       variant (optional)
├── captions.srt          uploadable, output-timeline times, proofread
├── thumbnail.jpg         chosen from 3 candidates, checked at small size
├── report.md             every judgement call + every measurement
├── watch.md              one sentence per sampled frame, the design read, the verdict
├── graphics.json         every overlay declared: what it is, and what it proves
├── gate-report.json      the audit as data
└── provenance.json       origin of every asset that claims to be real
```

`watch.md` and `graphics.json` are deliverables, not working files. They are the two pieces of
evidence that the craft half happened — that someone described the frames and that the overlays
can justify themselves — and `mfe gate` fails the package when they are missing. A render with
a gate report and no watch notes is a render whose audit stops at "it decoded".

## Encoding

| Field | Vertical social | Landscape |
|---|---|---|
| Codec | H.264 High, yuv420p | H.264 High |
| Bitrate | 10–16 Mbps for 1080×1920 | 16–24 Mbps for 1080p |
| Frame rate | the source's, 30 or 60, constant | constant |
| Audio | AAC 192 kbps, 48 kHz, stereo | same |
| Container | MP4, `+faststart` | MP4, `+faststart` |
| Colour | tagged bt709, no stray HDR | tagged |

Two things that break uploads and never warn you: **variable frame rate** (screen
recordings and phone footage) — force constant; and **odd dimensions** — always
even, yuv420p requires it.

## Variants

Never re-cut for another aspect. Reframe:

- **Same content, different frame.** Re-crop with a subject bias (`fit: "fill"`,
  `framing` per segment) so faces stay centred. Do not letterbox a vertical into
  a landscape — it screams "repost".
- **Re-check safe zones.** The 1:1 and 16:9 safe zones differ; captions that pass
  on 9:16 can sit in the UI on 16:9.
- **Re-audit each variant.** Each is a separate delivery with its own gates.
- **One export per platform, not one export for all.** Bitrate, length and caption
  behaviour differ meaningfully.

## Thumbnails and covers

- Three candidates, generated from real frames at the strongest beats.
- Check at **120 px wide**. If the text is unreadable, it is unreadable.
- One idea per thumbnail: a face, or a claim, or the product. Never all three.
- The hook line is the obvious cover title — reuse it rather than inventing a
  second headline for the same piece.

## report.md

Short, factual, and written for the person publishing, not for you.

```markdown
# <piece> — 52 s, 1080×1920

**Shape**    hook → claim → proof → turn → CTA
**Take choices**  s3 (2nd take of the opening), s7 (last, cleanest read)
**Cut**      11 segments, 40–120 ms padding, cut on silences ≥ 400 ms
**Grade**    neutral_punch, +6 saturation, no hue shift
**Captions** bold-pop, 34 cues, active-word accent, proofread against 9 names
**Sound**    −14.2 LUFS, TP −1.3 dBTP, music −19 dB under voice, 4 SFX
**Audit**    gates G0–G7 pass; 1 warning (end card 9 dB under dialogue, intentional)
**Not checked**  the mix on a phone speaker — needs a human ear
**Open questions**  the third stat needs a real source before publishing
```

## provenance.json

Required whenever any asset could be mistaken for reality.

```json
{ "assets": [
  { "id": "hero-shot",  "origin": "captured",  "source": "real app at 2:14:05",
    "claims_reality": true },
  { "id": "sky-plate",  "origin": "generated", "model": "local", "claims_reality": false },
  { "id": "logo",       "origin": "user",      "claims_reality": true }
]}
```

`origin` ∈ `captured` | `user` | `generated` | `stock-licensed`. A `generated`
asset with `claims_reality: true` fails gate G7 — that is the point.
