# Attribution

## What this repository is

**One install. Eighteen sources, combined.** The material of eighteen AI video-editing,
motion-graphics and design skills is in this repository, and it is in two forms:

- **`skills/`** — the merge. Seven skills that read as one voice, contradictions settled in
  writing, so you never invoke three skills per chat to get one edit done.
- **`library/`** — the evidence. The source material itself, so you can check the merge
  against what the upstreams actually said.

And it is in two modes, because licences differ and pretending otherwise would be theft:

| Mode | What it means | Count |
|---|---|---:|
| **copy** | The licence permits redistribution. Skill files, rules and references copied verbatim under `library/<area>/<source>/upstream/`, with the upstream licence travelling alongside as `LICENCE.upstream`. | 14 |
| **summarise** | The licence does **not** permit redistribution. Nothing copied. `SOURCE.md` carries a paraphrase written for this project. | 4 |

**1,066 files, 9.4 MB copied verbatim** — 41% of the 2,615 Markdown files the 18 sources
contain. Of the rest, 896 (34%) are in the three sources whose licences forbid copying, and
653 (25%) are release notes, byte-identical duplicates, test fixtures and changelogs. The
full accounting is in [`library/README.md`](library/README.md), generated from disk by
`tools/absorb.py` — not typed from memory.

### A note on the word "free"

An earlier attempt used GitHub's fork feature. That was wrong twice over: a fork is one
repository matched to one repository, so it cannot hold eighteen; and it put nine unwanted
public repositories on the account. They were deleted. A fork is not a merge. This
repository is the merge, in writing, and it is reviewable line by line.

---

## The eighteen sources

| # | Source | Licence | Mode | Files | Taken into `skills/` | Where |
|---|---|---|---:|---:|---|---|
| 1 | [ranahaani/i-hate-editing](https://github.com/ranahaani/i-hate-editing) | MIT | copy | 15 | cut on word boundaries, thinking pauses kept, hooks in 1–2 s, delivery package, hard rules over taste | [editing](library/editing/i-hate-editing/SOURCE.md) |
| 2 | [browser-use/video-use](https://github.com/browser-use/video-use) | MIT | copy | 19 | captions last, per-segment lossless concat, 30 ms fades, PTS-shifted overlays, output-timeline subtitles | [editing](library/editing/video-use/SOURCE.md) |
| 3 | [Moh4696/freecut](https://github.com/Moh4696/freecut) | MIT | copy | 19 | local ASR as the default, verify the rendered file not the timeline | [editing](library/editing/freecut/SOURCE.md) |
| 4 | [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | **MIT** | copy | 127 | silence candidates then a mandatory review gate; written handoffs; the GSAP trap list | [editing](library/editing/herk-edit-kit/SOURCE.md) |
| 5 | [petergyang/video-short](https://github.com/petergyang/video-short) | MIT | copy | 4 | the five layouts, receipts over claims, frame-by-frame review, QA stills | [editing](library/editing/video-short/SOURCE.md) |
| 6 | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | Apache-2.0 | copy | 10 | doctrine only — its CLI is a tool, not a rule | [editing](library/editing/open-edit/SOURCE.md) |
| 7 | [tiktok-short-edit](https://www.marwieang.com/tiktok-short-edit.md) | published document | **summarise** | — | −14 LUFS and safe zones, change every 2–3 s, synthesized bed | [editing](library/editing/tiktok-short-edit/SOURCE.md) |
| 8 | [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | modified Apache-2.0 | **summarise** | — | borrow structure never content; beat map before building | [editing](library/editing/hypit/SOURCE.md) |
| 9 | [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | Apache-2.0 | copy | 23 | the twelve reaches, never-ship list, judgement vs craft split | [motion](library/motion/motionmaxxing/SOURCE.md) |
| 10 | [hughminhphan/motion-kit](https://github.com/hughminhphan/motion-kit) | MIT | copy | 3 | register first, devices chosen not stacked, curves with provenance | [motion](library/motion/motion-kit/SOURCE.md) |
| 11 | [edenfunf/reelmimic](https://github.com/edenfunf/reelmimic) | MIT | copy | 389 | style as a named reproducible choice; one style per piece | [motion](library/motion/reelmimic/SOURCE.md) |
| 12 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | copy | 268 | mostly hard cuts, anti-monoculture, seek-safety, self-contained composition | [motion](library/motion/hyperframes/SOURCE.md) |
| 13 | [heygen-com/hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) | Apache-2.0 | copy | 54 | verify numerically not by eye; the trap list; scene continuity across cuts | [motion](library/motion/hyperframes-launches/SOURCE.md) |
| 14 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Remotion licence | **summarise** | — | frame determinism, parametrised variants, explicit sequences | [motion](library/motion/remotion/SOURCE.md) |
| 15 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT | copy | 25 | **the kind of business decides everything**, page plan by kind, reference-first art direction | [design](library/design/taste-skill/SOURCE.md) |
| 16 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | copy | 81 | tokens over values, type scale as a ratio, component states | [design](library/design/ui-ux-pro-max/SOURCE.md) |
| 17 | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | copy | 29 | should-it-animate, cheapest tool, transform/opacity, reduced motion | [design](library/design/emil-skills/SOURCE.md) |
| 18 | [dickwu/apple-design-skill](https://github.com/dickwu/apple-design-skill) | none stated | **summarise** | — | fixed audit lenses in a fixed order; platform convention is correctness | [design](library/design/apple-design/SOURCE.md) |

Two corrections worth stating, since both were wrong in an earlier draft of this file:

- **`herk-edit-kit` is MIT.** GitHub reports `NOASSERTION`, which is GitHub failing to parse
  the file, not the absence of a licence. Read it: MIT, so it is copied.
- **`hypit` is not plain Apache-2.0.** It is Apache-2.0 with added commercial conditions, so
  its text is not copied here.

## Why four sources are paraphrased and not copied

| Source | Licence | Why |
|---|---|---|
| hypit | modified Apache-2.0 | redistribution would carry commercial terms this project cannot accept for you |
| remotion | Remotion licence | free only below a company-size threshold; shipping its text would spread that trap to every user of this repo |
| apple-design-skill | no licence file | no grant to redistribute — copyright is retained by default |
| tiktok-short-edit | published document | published on the web is not licensed for republication |

A link and a paraphrase are honest. A copy would not be.

## The seven agent skills used to build this

These are tools, not sources, and nothing of them ships:

| Skill | What it did here |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | verification-before-completion; the rule that a claim needs a command behind it |
| [rea](https://github.com/jasonkuhrt/rea) | plan-then-execute discipline |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | TDD, source-driven development, code review |
| [anthropics/skills](https://github.com/anthropics/skills) | progressive disclosure and skill structure |
| [mattpocock/skills](https://github.com/mattpocock/skills) | small composable skills over one large prompt |
| [wayfinder](https://www.marwieang.com/wayfinder-skill.md) | plan-only boundaries, Settled/Questions/Unclear |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | smallest complete change; deletion beats addition |

## Verify it

```bash
python3 tools/absorb.py --check        # all 18 present, modes match licences, no text copied without a grant
python3 tools/verify-sources.py        # every upstream link resolves, every licence matches
python3 tools/vendor.py --check        # vendored files still match upstream at the pinned commit
```

If any of those three disagree with this page, believe the script and open an issue.
