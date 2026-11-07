# tiktok-short-edit

**Upstream:** https://www.marwieang.com/tiktok-short-edit.md  
**Licence:** published document (all rights reserved by default)  
**Pinned at commit:** `n/a`  
**Mode:** summarise  
**Doctrine files:** 0  
**Bytes:** 0

## Why nothing was copied

The licence (published document (all rights reserved by default)) does not permit redistribution, so no text, code or asset
from this source is included. What follows is a summary written for this project:
the ideas, in this project's words, which is what copyright does not cover.

If you want the source itself, use the upstream link above. If its terms suit you
better than these notes, that is a legitimate reason to go there — the point of this
repository is not to stop you reading the originals.

## Summary used by this project

# tiktok-short-edit — a complete 9:16 recipe in one document

**Licence:** published document (marwieang.com) · **Source:** https://www.marwieang.com/tiktok-short-edit.md ·
**Absorbed:** 2026-11-07

## What it is
Not a repo: one long skill document specifying a vertical short end to end, including
synthesized music and SFX generated in code so that no audio file is ever needed.

## Rules worth keeping
1. **Delivery shape is fixed:** 1080×1920, 30 fps, H.264/AAC.
2. **Loudness −14 LUFS integrated, true peak ≤ −1 dBTP** — measured, not aimed at.
3. **Safe zones:** keep text out of the top 150 px, the bottom 450 px (UI + caption rails)
   and the right 150 px (share/like rail).
4. **Something changes every 2–3 seconds.** Stillness longer than that reads as a freeze.
5. **The hook lands in the first 1–2 seconds** — and it must be visible, not promised.
6. **Synthesize the bed** (numpy → WAV) instead of shipping audio assets: no licences, no
   files, deterministic.
7. **Fades at every join**, including under the music.

## What it gets wrong
It stops at the render. There is no audit afterwards, so a file can ship at the wrong
loudness or with captions under the UI rail and nothing catches it.

## Where this landed
`safe zones` (3) and `2–3 s` (4) are enforced by gate G6 and G3 respectively ·
loudness (2) by G2 · the synthesized-bed technique is documented in
`motion-director/references/lanes.md` as a lane-A technique · the missing audit is this
project's reason to exist.
