# Attribution

## What this repository is

**One install. Eighteen sources, combined.** The material of eighteen AI video-editing,
motion-graphics and design skills is in this repository, in two layers:

- **`skills/`** — the merge. Seven skills that read as one voice, contradictions settled in
  writing, so you never invoke three skills per chat to get one edit done.
- **`library/`** — the evidence. **Every source's own text**, so the merge can be checked
  against what the upstreams actually said.

**1,824 files, 13.4 MB copied verbatim — 70% of the 2,616 Markdown files the eighteen sources
contain.** The other 30% is release notes (410), byte-identical duplicates (300), test
fixtures (54), and project admin files such as changelogs and CI templates (28). Nothing is
paraphrased: each source's doctrine is here in its own words.

### How each source is here

| Mode | Count | What it means |
|---|---:|---|
| **copy** | 14 | The licence grants redistribution. Files copied under `library/<area>/<source>/upstream/`, the upstream LICENCE travelling alongside as `LICENCE.upstream`, and Apache-2.0 `NOTICE` files as `NOTICE.upstream`. |
| **copy-permission** | 4 | The licence does **not** grant redistribution. Copied at the maintainer's instruction on the stated permission of the rights holder; each folder's `PERMISSION.md` records the basis and what this repository did and did not verify. |

An earlier draft paraphrased those four. That was the safe default, not what you asked for;
they are now copied in full, with their terms stated rather than implied.

**Licence scope matters here.** The root MIT `LICENSE` covers this project's own work only.
It does not cover `library/**/upstream/` — the upstream terms govern that text, and for the
four `copy-permission` sources those terms still bind you (the Remotion company-size
threshold, hypit's commercial conditions). The exact scope is in [`NOTICE`](NOTICE).

### A note on the word "fork"

An earlier attempt used GitHub's fork feature. That was wrong twice over: a fork is one
repository matched to one repository, so it cannot hold eighteen; and it put nine unwanted
public repositories on the account. They were deleted. A fork is not a merge. This
repository is the merge, in writing, and it is reviewable line by line.

---

## The eighteen sources

| # | Source | Licence | Mode | Files | Taken into `skills/` |
|---|---|---|---:|---:|---|
| 1 | [ranahaani/i-hate-editing](https://github.com/ranahaani/i-hate-editing) | MIT | copy | 15 | cut on word boundaries, thinking pauses kept, hooks in 1–2 s, delivery package, hard rules over taste |
| 2 | [browser-use/video-use](https://github.com/browser-use/video-use) | MIT | copy | 19 | captions last, per-segment lossless concat, 30 ms fades, PTS-shifted overlays, output-timeline subtitles |
| 3 | [Moh4696/freecut](https://github.com/Moh4696/freecut) | MIT | copy | 19 | local ASR as the default, verify the rendered file not the timeline |
| 4 | [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | **MIT** | copy | 127 | silence candidates then a mandatory review gate; written handoffs; the GSAP trap list |
| 5 | [petergyang/video-short](https://github.com/petergyang/video-short) | MIT | copy | 4 | the five layouts, receipts over claims, frame-by-frame review, QA stills |
| 6 | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | Apache-2.0 | copy | 10 | cut and review doctrine from its `CUT.md`; its CLI is a tool, not a rule |
| 7 | [tiktok-short-edit](https://www.marwieang.com/tiktok-short-edit.md) | published document | **permission** | 1 | −14 LUFS and safe zones, change every 2–3 s, synthesized bed |
| 8 | [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | modified Apache-2.0 | **permission** | 247 | borrow structure never content; beat map before building |
| 9 | [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | Apache-2.0 | copy | 23 | the twelve reaches, never-ship list, judgement vs craft split |
| 10 | [hughminhphan/motion-kit](https://github.com/hughminhphan/motion-kit) | MIT | copy | 3 | register first, devices chosen not stacked, curves with provenance |
| 11 | [edenfunf/reelmimic](https://github.com/edenfunf/reelmimic) | MIT | copy | 389 | style as a named reproducible choice; one style per piece |
| 12 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | copy | 268 | mostly hard cuts, anti-monoculture, seek-safety, self-contained composition |
| 13 | [heygen-com/hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) | Apache-2.0 | copy | 54 | verify numerically not by eye; the trap list; scene continuity across cuts |
| 14 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Remotion licence | **permission** | 379 | frame determinism, parametrised variants, explicit sequences |
| 15 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT | copy | 25 | **the kind of business decides everything**, page plan by kind, reference-first art direction |
| 16 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | copy | 81 | tokens over values, type scale as a ratio, component states |
| 17 | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | copy | 29 | should-it-animate, cheapest tool, transform/opacity, reduced motion |
| 18 | [dickwu/apple-design-skill](https://github.com/dickwu/apple-design-skill) | none stated | **permission** | 131 | fixed audit lenses in a fixed order; platform convention is correctness |

Two corrections worth stating, since both were wrong in an earlier draft of this file:

- **`herk-edit-kit` is MIT.** GitHub reports `NOASSERTION`, which is GitHub failing to parse
  the file, not the absence of a licence. Read it: MIT.
- **`hypit` is not plain Apache-2.0.** It is Apache-2.0 with added commercial conditions.

## The four sources copied on asserted permission

| Source | Licence | Status |
|---|---|---|
| hypit | Apache-2.0 with added commercial conditions | copied at the maintainer's instruction on 2026-11-07; **its commercial conditions still bind the copied text** |
| remotion | Remotion licence | as above; **its company-size threshold still binds users of the copied text** |
| apple-design-skill | no licence file | as above; no grant exists upstream, so the copy rests entirely on the assertion |
| tiktok-short-edit | published document | as above |

Each of those four folders carries `PERMISSION.md` recording the basis, the date, and the fact
that this repository verified **no** licence grant for them. The root MIT licence does not
extend to them — see [`NOTICE`](NOTICE) for the exact scope. If you are a rights holder and
object, open an issue and the folder is removed.

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
python3 tools/absorb.py --check        # 18 sources present, every mode has its basis on file
python3 tools/verify-sources.py        # every upstream link resolves, every licence matches
python3 tools/vendor.py --check        # every copy carries its licence or its permission record
```

If any of those three disagree with this page, believe the script and open an issue.
