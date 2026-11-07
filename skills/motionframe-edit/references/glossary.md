# Glossary

So that a note means the same thing to the person giving it and the one making it.

**A-roll / B-roll** — the primary footage (the speaker, the subject) and the
supporting footage. B-roll illustrates; A-roll carries.

**Beat** — one unit of meaning in a piece. A beat *buys* something: attention,
comprehension, belief, desire. If it buys nothing, it is a slide.

**Beat sheet** — the motion equivalent of an EDL: which beat, what it buys, what
moves, in which frames, and what it hands off to.

**Caption** — on-screen text of the spoken words. Infrastructure, not decoration.

**Choreography** — how a group of elements moves together: what leads, what
follows, what stays still, how much they overlap.

**Cut on motion** — placing a cut at the peak of a movement so the eye reads
continuity across the join.

**Dead frame** — a frame where nothing is happening: no motion, no light change, no
grain, no sound. Rule 7 forbids it. Gate G3 catches stretches of it.

**Dead stretch** — three or more seconds with no visual change. A defect in short
form; a choice in a slow film, with a reason.

**Delivery shape** — exact width, height, fps, codec and container for a
destination. Gate G1.

**Ducking** — lowering music automatically while the voice is present.

**EDL (edit decision list)** — the cut, as data: sources, segments, in/out points,
speed, fades, beats. `edl.json` here. Every downstream artifact is derived from it.

**Handoff** — the way one beat connects to the next: a carried object, a shape
match, a cause and effect, a cut on motion. No handoff, no beat.

**Hook** — the first 1–3 seconds. A promise, not a volume setting.

**Karaoke highlight** — captions where the spoken word is accented. Here it is done
per-word with colour overrides, so only the active word is highlighted.

**LUFS** — loudness units relative to full scale. The integrated measure streaming
platforms normalise against. −14 for social, −16 for podcast.

**Output timeline** — time in the finished piece, after cuts. Captions, overlays and
notes live here. The opposite of source time.

**Packing** — compressing word-level transcripts into a phrase-level reading view:
the artifact you actually reason over.

**Padding** — 30–200 ms added at each side of a cut to absorb ASR drift and keep
the breath.

**Precedence ladder** — the seven-rung order that decides what happens when two
rules disagree. See `precedence.md`.

**Provenance** — the declared origin of every asset: captured, user, generated, or
stock-licensed. `provenance.json`. Gate G7.

**Receipt** — a real tweet, article or page shown as evidence while the speaker
discusses it.

**Retake** — a repeated attempt at the same line. Usually better than the first, and
usually clustered at a file boundary.

**Safe zone** — the area of the frame the platform's own UI does not cover. 9:16 is
roughly the middle: top 12%, bottom 23%, right 13% are all covered by app chrome.

**Spring** — a physically-modelled animation. Good for things a finger touched; a
toy on anything else.

**Stagger** — a small per-item delay in a group entrance. 2–4 frames; more than that
and the eye follows the stagger rather than the content.

**Sting** — a short sound effect placed on a visual event.

**Taste memory** — `taste.md`: the durable record of this person's corrections.

**True peak** — the inter-sample peak after reconstruction. Must stay ≤ −1 dBTP or
the encode clips even when the sample peaks look safe.

**Two-source rule** — anything that claims to be real must be captured from the
real thing; generated assets never imply reality.
