# Architecture

## The split that makes it work

```
        JUDGEMENT                          MEASUREMENT
   ┌──────────────────┐              ┌────────────────────┐
   │  the skills      │              │     tools/sv.py    │
   │  (markdown)      │  ──────────▶ │  (one file, ffmpeg)│
   │  what to do,     │   commands   │  probe, cut,       │
   │  why, and when   │  ◀────────── │  caption, gate     │
   └──────────────────┘   numbers    └────────────────────┘
```

Most skill repos are all judgement: strong opinions, no verification. The result
is confident work with defects nobody caught. This project puts every checkable
claim into an executable, and leaves prose responsible only for the things that
cannot be measured — taste, hierarchy, rhythm, whether an idea is worth making.

**Rule of thumb:** if a claim can be verified, it belongs in `sv.py` or a gate. If
it lives only in prose, it is a suggestion, and it will be skipped under pressure.

## Data flow

```
footage ──▶ probe ──▶ transcript (word-level, cached)
                          │
                          ├──▶ packed reading view  ──▶ EDL (the contract)
                          │                                │
                          │             ┌──────────────────┼──────────────────┐
                          │             ▼                  ▼                  ▼
                          │        segments           captions           overlays
                          │        (extract,          (remapped to        (PTS-shifted,
                          │         fade, scale,       output time)        frame 0 at `at`)
                          │         speed)                 │                  │
                          │             └──────────┬────────┴──────────────────┘
                          │                        ▼
                          │                 composite: overlays → captions LAST → loudnorm
                          │                        │
                          │                        ▼
                          │                  gate_report() ──▶ gate-report.json
                          │                        │
                          └────────────────────────┴──▶ contact sheet + report.md + provenance.json
```

## Four decisions worth defending

**1. The EDL is the single source of truth.**
Every artifact is derived: captions, overlays, sound, notes, variants, gates. It
is JSON so a machine can validate it, small enough to read, and human-editable
when a human wants to nudge something. A tool that renders without an EDL cannot
be re-timed, re-graded or audited cheaply, which is why the sources that do it
that way also cannot fix drift.

**2. Two encodes, not six.**
Per-segment extract (with grade, fades, speed, scale) → lossless concat → one
composite pass that does overlays, captions and loudness together. Adding an
overlay must never re-encode every segment, and captions must never be applied
before overlays. Both of those are silent failures in the wild; here they are
structural.

**3. Output time is the only time.**
`sources → segments → output` is a coordinate change, and captions/overlays/notes
must be authored in the output space. `remap_words_to_output()` is the only
sanctioned conversion. This one design choice eliminates the most common
class of defect in assembled cuts.

**4. Gates return data, not vibes.**
`gate_report()` returns JSON: per-gate status, the number judged, and the facts
behind it. That is what makes `sv demo --selftest` possible — you cannot feed a
vibe a broken render and assert it notices.

## Progressive disclosure

```
skills/supervision/SKILL.md      ~150 lines   always loaded
  └─ references/precedence.md          ~120 lines   loaded when rules conflict
  └─ references/lineage.md             ~130 lines   loaded when provenance matters
skills/edit-supervisor/SKILL.md        ~200 lines   loaded when editing footage
  └─ references/cutting.md             ~140 lines
  └─ references/captions.md            ~90 lines
  └─ references/sound.md               ~80 lines
  └─ references/delivery.md            ~90 lines
```

A 3,000-line monolith would be one skill that reliably evicts itself from context
halfway through the work. The split means a captioning task loads the router plus
one reference file — about 400 lines — instead of everything.

## Degradation, not substitution

Every optional capability has a defined fallback, and the engine reports which one
is active rather than failing silently:

| Missing | Behaviour |
|---|---|
| ffprobe | parse `ffmpeg -i` for duration, streams and rotation |
| ASR | refuse to guess; ask for a transcript or an SRT, and say why |
| libass | `sv captions` still writes a valid `.ass`; burning needs libass |
| Node / Chrome | the HTML/React lanes are unavailable; the ffmpeg lane still works |
| fonts | warn; captions render in a fallback face with a different metric |

The one substitution that never happens is a paid API. If a capability is absent,
the answer is "this is unavailable, here is the free path", never a silent upload.

## Extending

- **New destination** (a platform with a new aspect): add a profile to
  `PROFILES` in `tools/sv.py` and a row to the table in
  `skills/edit-supervisor/references/delivery.md`.
- **New gate**: add it to `gate_report()`, to `specs/gates.json`, to the table in
  `skills/gatekeeper/SKILL.md`, and to the selftest with a fixture it must catch.
- **New render lane**: document it in `skills/motion-director/references/lanes.md`
  and make it optional. Nothing may require it.
- **New style**: add a `CAPTION_STYLES` entry or a named grade preset; never a
  parallel code path.
