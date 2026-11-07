# The library — eighteen sources, one digest each

This is where "combined" is either true or marketing. Every source in the brief has a
digest here, and every digest has the same four parts:

1. **What it is** — in one paragraph, no sales copy.
2. **Rules worth keeping** — numbered, specific, the ones that change a decision.
3. **What it gets wrong** — the hole that made someone install a second skill.
4. **Where this landed** — the file in `skills/` (or `specs/`) that carries each rule.

## How the skills use it

The skills are deliberately small. When a job needs depth, the skill sends the agent here:
a captioning task loads `editing/captions`-related digests, not the design system. That is
progressive disclosure, and it is the only way eighteen sources fit in one install.

## How to read the licence column

| Marking | Meaning |
|---|---|
| **MIT** / **Apache-2.0** | ideas kept, rewritten. No text redistributed. |
| **none stated (NOASSERTION)** | read for ideas only. Nothing redistributable — these digests are original summaries. |
| **published document** | a single web document, not a repository; summarised with a link. |

No source's text, code or assets were copied into this repository. Where a source's licence
is unclear, only publicly observable ideas were used. Full notices: `../ATTRIBUTION.md`.

## The eighteen

| Source | Domain | Licence | Digest |
|---|---|---|---|
| i-hate-editing | editing | MIT | [editing/i-hate-editing.md](editing/i-hate-editing.md) |
| video-use | editing | MIT | [editing/video-use.md](editing/video-use.md) |
| freecut | editing | MIT | [editing/freecut.md](editing/freecut.md) |
| herk-edit-kit | editing · motion | NOASSERTION | [editing/herk-edit-kit.md](editing/herk-edit-kit.md) |
| video-short | editing | MIT | [editing/video-short.md](editing/video-short.md) |
| tiktok-short-edit | editing | document | [editing/tiktok-short-edit.md](editing/tiktok-short-edit.md) |
| open-edit | editing (application) | Apache-2.0 | [editing/open-edit.md](editing/open-edit.md) |
| hypit | editing (application) | NOASSERTION | [editing/hypit.md](editing/hypit.md) |
| motionmaxxing | motion | Apache-2.0 | [motion/motionmaxxing.md](motion/motionmaxxing.md) |
| motion-kit | motion | MIT | [motion/motion-kit.md](motion/motion-kit.md) |
| reelmimic | motion | MIT | [motion/reelmimic.md](motion/reelmimic.md) |
| hyperframes | motion (runtime) | Apache-2.0 | [motion/hyperframes.md](motion/hyperframes.md) |
| hyperframes-launches | motion | Apache-2.0 | [motion/hyperframes-launches.md](motion/hyperframes-launches.md) |
| remotion | motion (runtime) | Remotion licence | [motion/remotion.md](motion/remotion.md) |
| taste-skill | design | MIT | [design/taste-skill.md](design/taste-skill.md) |
| ui-ux-pro-max | design | MIT | [design/ui-ux-pro-max.md](design/ui-ux-pro-max.md) |
| emil-skills | design · ui motion | MIT | [design/emil-skills.md](design/emil-skills.md) |
| apple-design-skill | design | none stated | [design/apple-design.md](design/apple-design.md) |

## What is deliberately not here

- **`open-edit` and `hypit`** have digests but contributed no rules: they are applications.
  Reading them changed this project's shape (the tool is not the deliverable), not its rules.
- **Their assets.** No themes, fonts, examples or style libraries are redistributed.
- **Their conflicts.** Where two sources disagree, the digest names the disagreement and
  `../skills/motionframe-edit/references/precedence.md` decides it.
