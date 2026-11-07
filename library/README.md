# The library — eighteen sources, combined

This folder is the combination. Every source in the brief is here, and how it is here
depends on its licence — not on convenience:

| Mode | Meaning |
|---|---|
| **copy** | The source's licence permits redistribution. Its skill files, rules and references are
|  | copied verbatim under `upstream/`, and its LICENCE travels alongside as `LICENCE.upstream`. |
| **summarise** | The licence does *not* permit redistribution. Nothing is copied; `SOURCE.md` carries a
|  | paraphrase written for this project, and says so plainly. |

**14 sources copied · 4 summarised · 1066 files · 9,379,496 bytes.**

| Source | Area | Mode | Licence | Files | Bytes |
|---|---|---|---|---:|---:|
| [i-hate-editing](editing/i-hate-editing/SOURCE.md) | editing | copy | MIT | 15 | 123869 |
| [video-use](editing/video-use/SOURCE.md) | editing | copy | MIT | 19 | 138914 |
| [freecut](editing/freecut/SOURCE.md) | editing | copy | MIT | 19 | 139247 |
| [herk-edit-kit](editing/herk-edit-kit/SOURCE.md) | editing | copy | MIT | 127 | 740624 |
| [video-short](editing/video-short/SOURCE.md) | editing | copy | MIT | 4 | 31332 |
| [open-edit](editing/open-edit/SOURCE.md) | editing | copy | Apache-2.0 | 10 | 99176 |
| [tiktok-short-edit](editing/tiktok-short-edit/SOURCE.md) | editing | summarise | published document | — | — |
| [hypit](editing/hypit/SOURCE.md) | editing | summarise | modified Apache-2.0 | — | — |
| [motionmaxxing](motion/motionmaxxing/SOURCE.md) | motion | copy | Apache-2.0 | 23 | 564937 |
| [motion-kit](motion/motion-kit/SOURCE.md) | motion | copy | MIT | 3 | 24605 |
| [reelmimic](motion/reelmimic/SOURCE.md) | motion | copy | MIT | 389 | 3542074 |
| [hyperframes](motion/hyperframes/SOURCE.md) | motion | copy | Apache-2.0 | 268 | 1888153 |
| [hyperframes-launches](motion/hyperframes-launches/SOURCE.md) | motion | copy | Apache-2.0 | 54 | 545342 |
| [remotion](motion/remotion/SOURCE.md) | motion | summarise | Remotion licence | — | — |
| [taste-skill](design/taste-skill/SOURCE.md) | design | copy | MIT | 25 | 429554 |
| [ui-ux-pro-max](design/ui-ux-pro-max/SOURCE.md) | design | copy | MIT | 81 | 773026 |
| [emil-skills](design/emil-skills/SOURCE.md) | design | copy | MIT | 29 | 338643 |
| [apple-design](design/apple-design/SOURCE.md) | design | summarise | no licence file | — | — |

## How the skills use it

`skills/` is the merge — one voice, contradictions settled. `library/` is the evidence:
the source material to check that merge against, loaded only when a job needs the depth.
That is progressive disclosure, and it is what lets eighteen sources fit into one install.

## Editorial notes

Each source folder also carries `NOTES.md` where one exists: what that source is good at,
what it gets wrong, and where its rules landed in `skills/`. Notes are this project's
writing, not the upstream's.

## How complete this is — measured

Across the 18 sources there are **2,615 Markdown files** in total (Release notes and the
four non-redistributable repos included). Here is what happened to every one of them:

| Files | Share | What happened | Why |
|---:|---:|---|---|
| **1,066** | 41% | **copied verbatim under `upstream/`** | they are the doctrine, and the licence permits it |
| 896 | 34% | not copied — paraphrased in `SOURCE.md` | the licence forbids redistribution (hypit, remotion, apple-design) |
| 410 | 16% | left out | upstream release notes (`releases/v0.9.2.md`), not rules |
| 171 | 6.5% | left out | byte-identical mirror of a file already copied (`.claude/skills/` vs `.agents/skills/`) |
| 54 | 2% | left out | test fixtures |
| 18 | 0.7% | left out | changelog, contributing, security policy, CI templates |

Nothing above is a judgement call disguised as a technical one: the third column is
reproducible with `python3 tools/vendor.py --check` plus a directory diff. The only category
that involves taste is the 896 — and there the constraint was legal, not editorial.

## What is not here

- **Binary assets** — themes, fonts, images, example films, ~1.5 GB across the sources.
  Licences vary, and a skill repo is not an asset dump. Their *instructions* are here.
- **Applications** — `open-edit`'s CLI code and `hypit`'s workflow are tools; only their
  doctrine is useful here.
- **Contradictions** — left as contradictions in the sources, resolved in
  `../skills/supervision/references/precedence.md`, and nowhere else.
