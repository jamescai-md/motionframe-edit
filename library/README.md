# The library — eighteen sources, combined

This folder is the combination. Every source in the brief is here, and how it is here
depends on its licence — not on convenience:

| Mode | Meaning |
|---|---|
| **copy** | The source's licence permits redistribution. Its skill files, rules and references are
|  | copied verbatim under `upstream/`, and its LICENCE travels alongside as `LICENCE.upstream`. |
| **summarise** | The licence does *not* permit redistribution. Nothing is copied; `SOURCE.md` carries a
|  | paraphrase written for this project, and says so plainly. |

**14 sources copied · 4 summarised · 713 files · 6,844,906 bytes.**

| Source | Area | Mode | Licence | Files | Bytes |
|---|---|---|---|---:|---:|
| [i-hate-editing](editing/i-hate-editing/SOURCE.md) | editing | copy | MIT | 11 | 103042 |
| [video-use](editing/video-use/SOURCE.md) | editing | copy | MIT | 16 | 124657 |
| [freecut](editing/freecut/SOURCE.md) | editing | copy | MIT | 16 | 122285 |
| [herk-edit-kit](editing/herk-edit-kit/SOURCE.md) | editing | copy | MIT | 136 | 787743 |
| [video-short](editing/video-short/SOURCE.md) | editing | copy | MIT | 2 | 23512 |
| [open-edit](editing/open-edit/SOURCE.md) | editing | copy | Apache-2.0 | 1 | 21121 |
| [tiktok-short-edit](editing/tiktok-short-edit/SOURCE.md) | editing | summarise | published document | — | — |
| [hypit](editing/hypit/SOURCE.md) | editing | summarise | modified Apache-2.0 | — | — |
| [motionmaxxing](motion/motionmaxxing/SOURCE.md) | motion | copy | Apache-2.0 | 15 | 472975 |
| [motion-kit](motion/motion-kit/SOURCE.md) | motion | copy | MIT | 1 | 5449 |
| [reelmimic](motion/reelmimic/SOURCE.md) | motion | copy | MIT | 276 | 2890864 |
| [hyperframes](motion/hyperframes/SOURCE.md) | motion | copy | Apache-2.0 | 129 | 1078437 |
| [hyperframes-launches](motion/hyperframes-launches/SOURCE.md) | motion | copy | Apache-2.0 | 15 | 243542 |
| [remotion](motion/remotion/SOURCE.md) | motion | summarise | Remotion licence | — | — |
| [taste-skill](design/taste-skill/SOURCE.md) | design | copy | MIT | 18 | 347340 |
| [ui-ux-pro-max](design/ui-ux-pro-max/SOURCE.md) | design | copy | MIT | 60 | 368573 |
| [emil-skills](design/emil-skills/SOURCE.md) | design | copy | MIT | 17 | 255366 |
| [apple-design](design/apple-design/SOURCE.md) | design | summarise | no licence file | — | — |

## How the skills use it

`skills/` is the merge — one voice, contradictions settled. `library/` is the evidence:
the source material to check that merge against, loaded only when a job needs the depth.
That is progressive disclosure, and it is what lets eighteen sources fit into one install.

## Editorial notes

Each source folder also carries `NOTES.md` where one exists: what that source is good at,
what it gets wrong, and where its rules landed in `skills/`. Notes are this project's
writing, not the upstream's.

## What is not here

- **Assets** — themes, fonts, images, example films. Licences vary and a skill repo is not
  an asset dump.
- **Applications** — `open-edit`'s CLI code and `hypit`'s workflow are tools; only their
  doctrine is useful here.
- **Contradictions** — left as contradictions in the sources, resolved in
  `../skills/supervision/references/precedence.md`, and nowhere else.
