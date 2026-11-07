# freecut — the same discipline, local by default

**Licence:** MIT · **Source:** https://github.com/Moh4696/freecut · **Absorbed:** 2026-11-07

## What it is
Shares the rule set with `video-use` (the two `SKILL.md` files are near-identical in
structure) but defaults to local Whisper, which makes it the more honest reference for how
transcription should work in a free tool.

## Rules worth keeping
1. **Local ASR is the default**, not the fallback. A paid backend, if present, is an option
   and never the path a new user lands on.
2. **Everything else from the shared rule set applies** — see `video-use.md`; the rules are
   the same and are not duplicated here.
3. **Verify against the rendered file**, not the project state. A timeline is not a video.

## What it gets wrong
It is an editor, so it optimises for its own UI. There is no design doctrine, no motion
doctrine, and its optional paid backends undermine the local-first stance it opens with.

## Where this landed
The local-ASR default became law in `supervision/SKILL.md` and a `doctor` behaviour:
when no transcriber is installed, the message names the free one and nothing else.
