# Attribution

## What this repository is — and is not

**It is not a fork.** There are no forks, no submodules, and no vendored code or prose. The
eighteen sources below were read, and their doctrine was rewritten at rule level into
`skills/` and summarised in `library/`.

That is a deliberate choice, not a shortcut. A literal fork of eighteen repositories would
have been legally impossible for five of them, technically unmaintainable, and would have
reproduced exactly the contradictions this project exists to settle.

**It is a merge with an audit trail.** Each source has a digest in `library/` with four
parts: what it is, the rules worth keeping, what it gets wrong, and where each kept rule
landed. Where two sources disagree, `skills/motionframe-edit/references/precedence.md` rules on
it in writing.

Check it yourself:

```bash
python3 tools/verify-sources.py     # every link resolves, every licence matches
python3 tools/absorb.py --check     # every source has a digest, every digest is complete
```

---

## The eighteen sources that were absorbed

| # | Source | Licence | What was taken | Digest |
|---|---|---|---|---|
| 1 | [ranahaani/i-hate-editing](https://github.com/ranahaani/i-hate-editing) | MIT | cut on word boundaries, thinking pauses kept, hooks in 1–2 s, delivery package, hard rules over taste | [editing](library/editing/i-hate-editing.md) |
| 2 | [browser-use/video-use](https://github.com/browser-use/video-use) | MIT | captions last, per-segment lossless concat, 30 ms fades, PTS-shifted overlays, output-timeline subtitles | [editing](library/editing/video-use.md) |
| 3 | [Moh4696/freecut](https://github.com/Moh4696/freecut) | MIT | local ASR as the default, verify the rendered file not the timeline | [editing](library/editing/freecut.md) |
| 4 | [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | NOASSERTION | silence candidates then a mandatory review gate; written handoffs; the GSAP trap list | [editing](library/editing/herk-edit-kit.md) |
| 5 | [petergyang/video-short](https://github.com/petergyang/video-short) | MIT | the five layouts, receipts over claims, frame-by-frame review, QA stills | [editing](library/editing/video-short.md) |
| 6 | [tiktok-short-edit](https://www.marwieang.com/tiktok-short-edit.md) | document | −14 LUFS and safe zones, change every 2–3 s, synthesized bed | [editing](library/editing/tiktok-short-edit.md) |
| 7 | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | Apache-2.0 | nothing carried — read for shape, credited | [editing](library/editing/open-edit.md) |
| 8 | [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | NOASSERTION | borrow structure, never content; beat map before building | [editing](library/editing/hypit.md) |
| 9 | [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | Apache-2.0 | the twelve reaches, never-ship list, judgement vs craft split, motion can be gated | [motion](library/motion/motionmaxxing.md) |
| 10 | [hughminhphan/motion-kit](https://github.com/hughminhphan/motion-kit) | MIT | register first, devices chosen not stacked, curves with provenance, springs vs duration | [motion](library/motion/motion-kit.md) |
| 11 | [edenfunf/reelmimic](https://github.com/edenfunf/reelmimic) | MIT | style as a named reproducible choice; one style per piece | [motion](library/motion/reelmimic.md) |
| 12 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | mostly hard cuts, anti-monoculture, seek-safety, self-contained composition | [motion](library/motion/hyperframes.md) |
| 13 | [heygen-com/hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) | Apache-2.0 | verify numerically not by eye; the trap list; scene continuity across cuts | [motion](library/motion/hyperframes-launches.md) |
| 14 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Remotion licence | frame determinism, parametrised variants, explicit sequences | [motion](library/motion/remotion.md) |
| 15 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT | **the kind of business decides everything**, page plan by kind, reference-first art direction | [design](library/design/taste-skill.md) |
| 16 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | tokens over values, type scale as a ratio, component states | [design](library/design/ui-ux-pro-max.md) |
| 17 | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | should-it-animate, cheapest tool, transform/opacity, interruption and exit, reduced motion | [design](library/design/emil-skills.md) |
| 18 | [dickwu/apple-design-skill](https://github.com/dickwu/apple-design-skill) | none stated | fixed audit lenses in a fixed order; platform convention is correctness | [design](library/design/apple-design.md) |

---

## The seven agent skills used to build this repository

These were the **tools** for the work, not sources of doctrine. They shaped how this was
planned, written, verified and shipped.

| Source | How it was used here |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | plan before building; verification before completion; the two STOP gates |
| [morluto/rea](https://github.com/morluto/rea) | read the real artifacts first — all 25 repositories were cloned and inspected before a line was written |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | the quality bar written as a contract: [specs/quality-bar.md](specs/quality-bar.md) |
| [anthropics/skills](https://github.com/anthropics/skills) | the `SKILL.md` format, progressive disclosure, description-first routing |
| [mattpocock/skills](https://github.com/mattpocock/skills) | how every file here is written: imperative, terse, no adjectives standing in for rules |
| [wayfinder](https://www.marwieang.com/wayfinder-skill.md) | the planning document at [docs/plan.md](docs/plan.md) — settled, open, excluded, phased |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | the smallest complete change: the engine was ported, not rewritten; what was skipped is named |

---

## Correction history

A provenance file that never admits an error is not a provenance file.

| Claim | Reality | Status |
|---|---|---|
| v1 of this project claimed `taste-skill` did not state the "kind of business" idea | **Wrong.** It is that source's section 1, and the original credit was right. The retraction was itself the error, caused by reading the README instead of `skills/taste-skill/SKILL.md`. | corrected here |
| `herk-edit-kit` credited with "cut on motion" and "no dead frame" | Neither phrase appears in its 210 markdown files. It is credited for what is there: silence candidates + review gate, handoffs, and the GSAP trap list. | corrected |
| `dickwu/apple-design` | The repository is `dickwu/apple-design-skill`. | corrected |
| `walterlow/freecut` | The brief's repository is `Moh4696/freecut`; this project uses the one from the brief. | corrected |
| `attentiondotnet/emilkowalski_skills` | The brief's repository is `emilkowalski/skills`. | corrected |
| "25 open-source repositories" | 18 sources were absorbed; 7 further repos were the agent skills used to build it. | corrected |
| ponytail "could not be pinned" | It is `DietrichGebert/ponytail`. | corrected |

## Reading order

- [`library/README.md`](library/README.md) — the eighteen, with licences and digests
- [`docs/plan.md`](docs/plan.md) — the plan this repository was built against
- [`specs/quality-bar.md`](specs/quality-bar.md) — what "done" means, as a contract
