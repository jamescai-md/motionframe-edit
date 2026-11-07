# Coverage — what actually landed from each source

`ATTRIBUTION.md` records credit. This page records **coverage**: for each source, the one
capability that was worth taking, and where in the doctrine it now lives. A credit that
never reaches a skill is a name-drop, so the two files answer different questions.

**Method.** Each capability was searched for, case-insensitively, across the files an agent
actually loads — `skills/**/*.md` and `AGENTS.md` — on 2026-11-07. A hit means the
capability is *present*, not that it is *good*: presence is necessary, not sufficient. The
quality argument is `tools/gate-docs.py`, which measures the repository, and
`tools/sv.py demo --selftest`, which measures whether the gates can fail.

Result: **22 of 23 capabilities present. 2 sources deliberately not carried. 1 idea unpinned.**

## Present in the doctrine

| Source | The capability taken | Lives in |
|---|---|---|
| [browser-use/video-use](https://github.com/browser-use/video-use) | correctness rules: 30 ms fades, per-segment lossless concat, PTS-shifted overlays, output-timeline captions | `skills/edit-supervisor/SKILL.md`, `references/cutting.md` |
| [ranahaani/i-hate-editing](https://github.com/ranahaani/i-hate-editing) | hard rules won from rejected renders; `taste.md` as durable memory | `skills/edit-supervisor/`, `skills/taste-memory/SKILL.md` |
| [walterlow/freecut](https://github.com/walterlow/freecut) | local Whisper by default — no account in the path | `skills/edit-supervisor/SKILL.md` |
| [obra/superpowers](https://github.com/obra/superpowers) | verification before completion; the two STOP gates | `skills/supervision/SKILL.md` §"STOP 1 / STOP 2" |
| [anthropics/skills](https://github.com/anthropics/skills) | progressive disclosure; `SKILL.md` frontmatter as routing | every `skills/*/SKILL.md` |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | the quality bar written as a contract | `skills/gatekeeper/`, `specs/gates.json` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | imperative, unhyped writing for agents | all doctrine files |
| [morluto/rea](https://github.com/morluto/rea) | examine the real artifact before reimagining it | `skills/design-director/SKILL.md` |
| [wayfinder](https://www.marwieang.com/wayfinder-skill.md) | plan in plain English, approved before building | `skills/supervision/SKILL.md` §"STOP 1" |
| [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | motion handoffs; arrival from oversize | `skills/edit-supervisor/references/cutting.md` |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | lane B: HTML/GSAP captured in headless Chrome | `skills/motion-director/references/lanes.md` |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | lane C: React compositions with `useCurrentFrame` | `skills/motion-director/references/lanes.md` |
| [hughminhphan/motion-kit](https://github.com/hughminhphan/motion-kit) | a motion-designer **role definition** — what the job refuses | `skills/motion-director/SKILL.md` §"Who you are on this job" *(added in this pass — it was absent)* |
| [edenfunf/reelmimic](https://github.com/edenfunf/reelmimic) | named visual styles as a menu, subject to the one-system law | `skills/motion-director/` |
| [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | a motion piece can be *gated* at all | `skills/gatekeeper/`, `specs/gates.json` |
| [heygen-com/hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) | beat sheet; build the hardest beat first | `skills/motion-director/SKILL.md` |
| [petergyang/video-short](https://github.com/petergyang/video-short) | the layout table — a-roll / punch / split / receipt / page | `skills/edit-supervisor/SKILL.md` |
| [tiktok-short-edit](https://www.marwieang.com/tiktok-short-edit.md) | platform safe zones; "something changes every 2–3 s" | `skills/edit-supervisor/SKILL.md`, gate G6 |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | token and system discipline: brand, type scale, components | `skills/design-director/references/system.md` |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | reference-first art direction; name slop instead of hand-waving | `skills/design-director/references/anti-slop.md` |
| [attentiondotnet/emilkowalski_skills](https://github.com/attentiondotnet/emilkowalski_skills) | should-it-animate, springs, choreography, frame budget | `skills/ui-motion/`, `skills/motion-director/` |
| [dickwu/apple-design-skill](https://github.com/dickwu/apple-design-skill) | HIG-grounded review rubric | `skills/design-director/references/anti-slop.md` |

## Deliberately not carried — 2

| Source | Why nothing was taken |
|---|---|
| [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | It is an **application**, not a skill. The lesson taken was negative: the tool is not the deliverable, the package is. That lesson lives in the router, not as code. |
| [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | Same — a workflow engine, not editorial judgement. Referenced, not absorbed. |

Both are cited in `ATTRIBUTION.md` as sources read. Neither is a dependency, and neither
appears in the engine.

## Unpinned — 1

| Source | Status |
|---|---|
| **ponytail** — "the smallest change that fully solves it", a debt ledger, ruthless review | The idea is present in the doctrine (scope discipline). Its origin could not be resolved to a canonical repository, so it is credited as a borrowed idea, not as a source. See `ATTRIBUTION.md`. |

## Rule-level audit — started, 1 of 23 sources done

Phrase presence is a weak test, so the stronger one is being run source by source: take a
source's rule file, extract every discrete instruction, and check whether this repo
contains it. Not the topic — the rule.

**`ranahaani/i-hate-editing` · `rules/cutting.md`** (the first one audited):

| | |
|---|---|
| Discrete rules in the source | 8 |
| Already covered by `edit-supervisor/references/cutting.md` | 3 |
| **Missing** | **5** — dead-air nuance, filler words, false starts, rambles, repeated words across a join, L/J-cuts |
| Action taken | all five written into the reference in this repo's voice, with numbers, credited in-file |

That is the real shape of the problem, and it is why the phrase test was not enough: the
topic "cutting" was covered, while five specific rules inside it were not.

**Not yet audited at rule level: 22 of 23 sources.** Until that is done, "combined" is a
claim about ideas, not about rules.

## What this page does not prove

- **That the doctrine is good.** Only that it is there. Judgement is not measurable by grep.
- **That the sources are unchanged.** They are other people's repos; they move.
- **That nothing was lost in the rewrite.** Prose was rewritten, not copied, so a rule can
  survive in spirit and drift in the retelling. The strongest evidence against that is the
  executed behaviour: `specs/gates.json` + `sv demo --selftest`.
