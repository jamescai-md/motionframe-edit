---
name: edit-supervisor
description: >-
  Edit footage into a finished, publishable piece — talking heads, interviews, tutorials,
  travel, montages, demos, podcasts, vertical shorts. Use when someone hands over raw takes or
  a rough cut and wants a real edit: cut, captions, grade, sound, B-roll, platform variants and
  a thumbnail. Audio-first cutting, word-boundary precision, output-timeline captions, and an
  audit before anything is shown. Replaces an editor, not a render.
license: MIT
---

# Edit supervisor

Input: raw footage. Output: a package someone can publish without opening an editor.

**The bar:** if a professional editor returned this, would the client accept it?

Read `../motionframe-edit/SKILL.md` first if you have not — the twelve laws apply here
and are not repeated.

## 0. Taste, then inventory

All commands below use `$SV` for the engine:

```bash
SV=/absolute/path/to/motionframe-edit/tools/mfe.py   # set once; resolved in skills/motionframe-edit/SKILL.md
```

```bash
python3 "$SV" scaffold <project>          # brief.md, taste.md, edl.json, provenance.json
```

Read `taste.md` and `brief.md` **before** looking at footage. A correction from a
previous session outranks every default in this file. Then:

```bash
python3 "$SV" probe footage/*            # display dimensions, fps, rotation, audio
```

Probe **display** dimensions, not stream dimensions: phone footage carries a
rotation matrix, so the stream says 1920×1080 while the decoder outputs 1080×1920.
Reading it the naive way letterboxes an entire vertical edit, silently.

Flag, in writing, anything that will bite later: variable frame rate, mismatched
fps between takes, mono vs stereo, a silent audio track, a source shorter than the
plan needs, missing audio entirely.

## 1. Transcribe, then pack

Word-level, verbatim, cached per source, **language pinned** — never auto-detected.
Auto-detect silently *translates* some languages instead of transcribing them,
which corrupts every downstream timestamp.

```bash
# Free and local. Either backend; both are open source.
whisper-cli -m models/ggml-large-v3.bin -ml 1 -l en -oj footage/take-01.wav
# or: python -m faster_whisper --word_timestamps True footage/take-01.mp4
```

Then pack the transcripts into one phrase-level reading view — the artifact you
actually reason over. This is the single derived file that earns its keep:

```
## C0103  (43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

Rules that make the packed view trustworthy:

- Phrase breaks on silence ≥ 0.5 s **or** speaker change.
- Keep fillers, stutters and restarts. They are the editorial signal — a restart
  marks a retake, and retakes cluster at file boundaries.
- Cache per source. Never re-transcribe unless the file itself changed.
- If your ASR cannot give word timings in a script (some CJK paths corrupt on
  subword splitting), use segment-level output plus silence detection, and say so.

You read the packed view to decide the cut. You look at frames only at decision
points — never scan video continuously.

## 2. Read, then converse

One pass over the packed transcript, noting in plain text: verbal slips, repeated
lines, the strongest claim, the weakest section, anything that must be preserved
(a laugh, a result, a specific number).

Then ask questions shaped by *this* material — not a fixed checklist. The ones
that almost always matter:

- What is this for, and where does it publish? (aspect, length, platform)
- Who is it for, and what should they do after watching?
- What must survive untouched?
- Is there real material for the claims — sources, screenshots, demos, data?
- What should it *feel* like? One or two adjectives, not a style name.

Then write the plan in 4–8 sentences: shape, take choices, cut direction, motion
plan, grade direction, caption approach, runtime estimate.

> **STOP.** Wait for a plain "go". Never build on an unapproved plan.

## 3. Build the cut

Write `edl.json`, never a filtergraph by hand. The EDL is the contract that makes
captions, overlays, sound and notes line up:

```json
{
  "version": 1,
  "profile": "vertical-9x16",
  "sources": { "A": "footage/take-01.mp4" },
  "segments": [
    { "id": "s1", "source": "A", "start": 2.42, "end": 6.85,
      "beat": "HOOK", "fit": "fill", "framing": [0.5, 0.38],
      "fade_in": 0.03, "fade_out": 0.03, "quote": "Ninety percent of this is wasted." }
  ],
  "overlays": [], "captions": { "enabled": true, "style": "bold-pop" }
}
```

```bash
python3 "$SV" validate --edl edl.json
python3 "$SV" render --edl edl.json --out work/draft.mp4 --preview
```

Cut craft lives in `references/cutting.md`. The five things that go wrong most:

1. **Cutting inside a word.** Snap to a word boundary, then pad 30–200 ms.
2. **Defaulting to the first take.** Later takes are usually better; the last
   complete take of a repeated line is almost always the keeper.
3. **Cutting the reaction.** The laugh *is* the beat. Extend past the punchline.
4. **Even rhythm.** Vary shot length on purpose; metronomic cutting reads as a
   slideshow, and random cutting reads as a mistake.
5. **Deleting the breath.** Leave 150–300 ms of air after commas and list items.
   A cut on every possible millisecond sounds machine-made.

## 4. Layout, for vertical

Full-screen talking head for at least half the runtime — viewers connect with a
face; a piece that never shows one is a slideshow.

| Layout | Use for | Rule |
|---|---|---|
| `a-roll` | the speaker carrying a point | default |
| `punch` | emphasis — tighter crop | never two punches in a row |
| `split` | visual above, speaker below | visual must be *about* what they said |
| `b-roll` | full-screen supporting shot | ≤ 3.5 s each, and never a still image |
| `receipt` | the tweet / article / page being discussed | crop to the lines that matter, mark the key line |
| `page` | a real web page | capture at phone width so it reflows; drift down one section |
| `number` | a stat the speaker says | count up to it, land on the spoken value |
| `list` | a spoken list | add one row per item, on the word |
| `graphic` | a flow, before/after, diagram | must end on the next shot's first frame |

Full-screen visuals show **what the words cannot**: the product doing the thing,
the result, the proof. Captions already carry the words.

Visuals hierarchy, and it is strict: the user's own footage and sources →
official material about the subject → a designed graphic → a generated image.
Never upload a still image as B-roll: an image is only the first frame of a
generated clip, a scrolling page capture, or a receipt.

## 5. Captions

```bash
python3 "$SV" captions --edl edl.json --words work/words.json --remap A \
                       --style bold-pop --out captions.ass
```

Two rules carry the whole thing:

- **Remap to output time.** `--remap A` converts source-time words onto the cut
  timeline and drops words you cut away. Caption times in source time are the
  classic silent failure.
- **Stay out of the platform UI.** The profile's safe zone is enforced and audited:
  ~top 12%, bottom 23%, right 13% on 9:16. Captions never cover the mouth or chin.

Style: 2–4 words a line, high contrast, one accent used for the *active* word and
nothing else. Sentence case for calm pieces, caps for high-energy, never both in
one piece. Details in `references/captions.md`.

## 6. Sound

The voice is the mix. Everything else is support.

```bash
python3 "$SV" gate --file work/draft.mp4 --edl edl.json    # G2 measures LUFS + true peak
```

- Normalise to the profile target (−14 LUFS integrated for social, true peak ≤ −1 dBTP).
- Music sits **under** the voice and ducks further whenever speech is present.
- SFX only where a visual event deserves attention — "on every cut" is a tell.
- Never speed up or pitch-shift the voice to fit. Cut the words instead.
- Music must not resolve the piece before the piece does; end on the last word or
  on a designed beat of silence.

Mixing numbers, ducking curves and the differencing trick that proves a sting is
actually audible: `references/sound.md`.

## 7. Audit, then present

```bash
python3 "$SV" gate  --file work/draft.mp4 --edl edl.json \
                    --boxes captions.boxes.json --out work/gate.json
python3 "$SV" sheet --file work/draft.mp4 --out work/sheet.jpg
```

Look at the sheet. Describe each frame in one sentence — what is on screen, what
is the hero, would it pass as a slide — *before* judging it. Then fix in this
order, because the order is the cost order:

**broken or untrue → the idea → connections between beats → hierarchy and scale
→ timing → surface and finish → sound polish.**

For anything published (launch, ad, promo), run one **critic pass**: a fresh-context
review briefed to roast, not to praise. Verdict, ranked problems with timecodes
and evidence, and the five fixes to do first. Fresh eyes catch what the author
stopped seeing. Brief in `../gatekeeper/references/critic.md`.

Max three audit passes. Past that, present with the failures stated.

## 8. Deliver a package

A cut file is not the deliverable. Ship:

```
out/
├── <name>-9x16.mp4        the piece, platform-correct
├── <name>-1x1.mp4         variant, if asked
├── captions.srt           uploadable, output-timeline times
├── thumbnail.jpg          3 candidates, chosen for the muted first frame
├── report.md              every judgement call + every measurement
├── gate-report.json       the audit, as data
└── provenance.json        origin of every asset that claims to be real
```

Variant rules and the report format: `references/delivery.md`.

## 9. Learn

Every correction the user makes is a rule, not an edit:

> "the end card was too long" → **End holds ≤ 1.2 s. Cut on the beat, not after it.**

Append to `taste.md` under the right heading, with the correction and what it
replaced. Read it at the top of the next piece. A suite that does not remember is
a suite you have to re-teach every time — which is the exact problem this project
exists to solve.

## Failure modes, with the fix

| Symptom | Cause | Fix |
|---|---|---|
| Captions drift later and later | source-time captions on an assembled cut | remap with `--remap` |
| Pop at every cut | no micro-fade at segment edges | `fade_in/fade_out: 0.03` |
| Text hidden behind a lower third | overlay applied after captions | captions composite last, always |
| Edit feels slow | cuts on breath, not on words | tighten to 80–150 ms padding |
| Edit feels frantic | padding below 30 ms, no air after commas | 150–300 ms after punctuation |
| Audio "looks fine" but is quiet | nobody measured | `mfe gate` → G2 |
| Aimless middle third | the plan had no shape | re-plan the beats, don't patch B-roll |
| Generated image reads as a fake screenshot | trust rule violated | capture the real thing |
