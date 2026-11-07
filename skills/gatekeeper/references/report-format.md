# Report format

The handoff is the product. Two artifacts, both short, both factual.

## 1. `report.md` — for the human publishing it

```markdown
# <piece> — 52 s, 1080×1920

**Shape**         hook → claim → proof → turn → CTA
**Take choices**  s3 (2nd take of the opening), s7 (last, cleanest)
**Cut**           11 segments · 40–120 ms padding · cuts on silences ≥ 400 ms
**Grade**         neutral_punch, +6 sat, no hue shift
**Captions**      bold-pop · 34 cues · active-word accent · 9 names proofread
**Sound**         −14.2 LUFS · TP −1.3 dBTP · music −19 dB under voice · 4 SFX
**Gates**         G0–G2, G4–G8 pass · G3 warn (intentional 1.2 s hold before payoff)
**Not checked**   the mix on a phone speaker
**Open**          the third stat needs a real source before publishing
```

Nothing else. No process notes, no self-congratulation, no restating the brief.

## 2. `gate-report.json` — for the machine and the next session

Produced by `mfe gate`. Keep it in the output folder. It is how a future session
knows what was already verified, and it is the only proof that anything was
audited at all.

```json
{
  "tool": "motionframe-edit 1.0.0",
  "file": "out/final.mp4",
  "profile": "vertical-9x16",
  "media": { "duration_s": 52.1, "display_width": 1080, "display_height": 1920, "fps": 30 },
  "gates": [ { "id": "G2", "name": "loudness", "status": "pass",
               "detail": "-14.2 LUFS (target -14±2), true peak -1.3 dBTP" } ],
  "verdict": "pass",
  "warnings": 1
}
```

## The sentence that must never be missing

Every handoff ends with the thing you could not verify:

> "I can't hear the mix — check that the music sits under the voice on a phone
> speaker. Everything else is measured."

You are not allowed to imply you checked something you did not. That single
sentence is what separates motionframe-edit from a confident guess.
