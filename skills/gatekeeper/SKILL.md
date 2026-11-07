---
name: gatekeeper
description: >-
  The audit layer: measure a finished render, page or asset against named gates, then look at it
  with fresh eyes before anyone else does. Use whenever work is about to be called done,
  presented, published or handed over — and whenever reviewing someone else's cut, design or
  animation. Turns "looks good to me" into named checks with numbers, and produces the ranked
  fix list when they fail.
license: MIT
---

# Gatekeeper

Every other skill in this suite makes judgements. This one checks them.

Two things never happen without passing through here: a render being presented, and
a piece being called complete. Not because the checks are profound, but because
**a completed render is not a correct render**, and the gap between those two is
where every embarrassing result lives.

## The eight gates

All commands below use `$SV` for the engine:

```bash
SV=/absolute/path/to/motionframe-edit/tools/mfe.py   # set once; resolved in skills/motionframe-edit/SKILL.md
```

```bash
python3 "$SV" gate --file out/final.mp4 --edl edl.json \
                   --boxes captions.boxes.json --out gate-report.json
```

| Gate | Name | Passes when | Measured by |
|---|---|---|---|
| **G0** | render exists | decodes, non-blank, duration within 1% (or 0.35 s) of the plan, audio present | `mfe gate` |
| **G1** | delivery shape | exact width×height and fps for the profile; correct codec, container, pixel format | `mfe gate` |
| **G2** | loudness | integrated within ±2 LU of target, true peak ≤ −1 dBTP | `mfe gate` (ebur128) |
| **G3** | picture alive | no freeze > 0.5 s, no stretch > 3 s with no visual change | `mfe gate` (freezedetect + frame deltas) |
| **G4** | no black holes | no unintended black interval > 0.15 s | `mfe gate` |
| **G5** | cuts don't pop | no boundary spike > 6 dB over the local body level in the 120 ms around a cut | `mfe gate` (astats) |
| **G6** | captions safe | every cue box inside the platform safe zone; text height ≥ 3.5% of frame | `mfe gate` + boxes |
| **G7** | honest proof | every asset declares an origin; nothing generated claims to be real | `mfe gate` + `provenance.json` |

For pages, UIs and stills, the analogue is named and binary — see
`references/gates-for-design.md`. Same principle: no gate, no verdict.

## The audit, in order

The order is the cost order. Fixing a broken render after redesigning a section
wastes the redesign.

```
1  MEASURE     run the gates. Write the report to disk, not to the chat.
2  LOOK        contact sheet, then full-speed playback of the first 3 s and the last 3 s.
3  READ        describe every sheet frame in one sentence before judging it.
4  ROAST       a critic pass in fresh context, briefed to find problems. (references/critic.md)
5  FIX         in the fix order below. Re-run the gates. Cap at three passes.
6  REPORT      pass/fail per gate, plus what you could not check.
```

```bash
python3 "$SV" sheet --file out/final.mp4 --out work/sheet.jpg --every 1.5
```

**Describe before you judge.** One sentence per frame: what is on screen, what is
the hero, would this frame pass as a slide? Skipping this step is why people
"look" at a render for ten minutes and miss that the caption is behind the logo.

## The fix order

Never fix in the order you noticed things. Fix in this order:

```
1  broken or untrue      (won't play, wrong claim, fabricated asset)
2  the idea              (there is no reason to watch)
3  connections           (beats don't hand off; sections don't follow)
4  hierarchy and scale   (the eye lands wrong; text unreadable at size)
5  timing                (too fast, too slow, dead stretch)
6  surface and finish    (grade, grain, borders, alignment)
7  sound polish          (last, because it is the cheapest to change and the
                          first thing people redo instead of the real problem)
```

## What you must report

A verdict is not a report. Every handoff includes:

- **Per-gate status**, with the number it was judged on.
- **The one warning you decided to keep**, and why it is acceptable.
- **What you could not check** — you cannot hear the mix, you cannot feel the
  timing on a phone, you cannot see it on a device you do not have. Say it.
- **The five fixes to do first**, if it failed. Ranked, with evidence.

Never: "audio looks good", "the design is clean", "should be fine now". If you did
not measure it, say you did not measure it.

## Three failure modes of the auditor

1. **The vacuous gate.** A check that cannot fail is decoration. Prove your gates
   can fail: `mfe demo --selftest` deliberately feeds broken renders to G2, G3, G1,
   G6 and G7 and asserts they trip. Do the same for any check you add.
2. **The infinite audit.** Three passes, then report. Past three, you are no longer
   improving the piece; you are avoiding the handoff.
3. **The polite critic.** A critic briefed to find good things will find them. Brief
   for the roast, and require timecodes and numbers as evidence.

## When a gate cannot pass

Some gates are legitimately unsatisfiable — a source with no audio, a platform
that demands 4:3, a brand that forbids the caption position that is readable.

Do not fake the number, and do not silently skip the gate. Instead:

> "G2 cannot pass: the source has no audio track and there is no music budget. I
> have delivered it silent with a note on the thumbnail. G0, G1, G3–G7 pass."

A stated, justified exception is professional. A silent one is the thing this
entire repository exists to prevent.

## Files

- `references/critic.md` — the fresh-context review brief
- `references/gates-for-design.md` — the binary checks for pages, UIs and stills
- `references/report-format.md` — the exact handoff format
