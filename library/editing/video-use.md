# video-use — the sharpest production-correctness rules anywhere

**Licence:** MIT · **Source:** https://github.com/browser-use/video-use · **Absorbed:** 2026-11-07

## What it is
One 26k-character `SKILL.md` that reads like a post-mortem written by someone who has had
renders fail in every possible way. It is the single best source of correctness rules in
the collection, and the origin of most of the numeric rules in `edit-supervisor`.

## Rules worth keeping
1. **Captions are the last step**, built from the finished timeline. Doing them earlier
   guarantees they drift after the cut changes.
2. **Concatenate per segment, losslessly** (`-c copy` on identical encodes). One giant
   re-encode per revision is how quality and time both disappear.
3. **30 ms audio fades at every join.** Without them, cuts click — and the click is louder
   in headphones than any picture problem.
4. **Shift overlay timestamps (PTS) explicitly** when compositing onto a cut timeline.
5. **Subtitles are computed on the output timeline**, then remapped to source only when
   required.
6. **Read the packed transcript, not the raw one** — phrases with durations are what a
   cutting decision can actually use.
7. **Multi-take selection is a separate brief**, given to a sub-agent with the criterion
   written down, not the feeling.

## What it gets wrong
Its happy path needs ElevenLabs/Scribe keys for transcription — the one thing this project
refuses. The rules themselves are free; only the transcription vendor was not.

## Where this landed
`edit-supervisor/references/cutting.md` (2, 3, 6, 7) · `captions.md` (1, 5) ·
`specs/gates.json` G5 (3, measured) · `sv.py captions --remap` (5, executed) ·
gates G0/G1 were derived from its failure list. Transcription replaced with local
`whisper.cpp`; `doctor` says so.
