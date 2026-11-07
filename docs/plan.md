# Plan — motionframe-edit, one skill built from eighteen

Written before implementation, in the shape **wayfinder** asks for: settled facts,
open questions, exclusions, then a phased plan. Kept in the repo because a plan that
disappears cannot be checked against what was actually built.

## Settled

| | |
|---|---|
| **Goal** | One installable skill that replaces the eighteen editing / motion / design skill repos a person otherwise copies into every chat. |
| **Why** | Each of those repos is strong in one direction and weak in another, and the weaknesses are complementary — so people install many and get contradictions instead of coverage. |
| **Product** | A repository, `motionframe-edit`: seven skills, a library of absorbed rules, and a free local engine that measures the result. |
| **Hard constraints** | No paid API, no keys, no accounts. Local only. MIT. |
| **Platforms** | Claude Code, ChatGPT/Codex, Gemini CLI/Antigravity, OpenCode, Hermes, and anything that reads `AGENTS.md` or `SKILL.md`. |
| **Success** | A stranger clones it, installs in one command, and never needs another editing skill for a normal job — and a wrong render is caught by a gate, not by taste. |
| **Build tools** | The seven agent skills supplied with the brief (superpowers, rea, addyosmani/agent-skills, anthropics/skills, mattpocock/skills, wayfinder, ponytail) were used to make this repository, and are credited as tools, not as sources. |

## Questions that were open, and how they were settled

| Question | Decision | Why |
|---|---|---|
| Fork each repo's files, or rewrite the doctrine? | **Rewrite, at rule level, with a named home for every rule.** | Five of the eighteen cannot be legally redistributed (no licence file or `NOASSERTION`), and verbatim merging reproduces the contradictions the project exists to remove. |
| One giant SKILL.md, or several skills? | **A router plus six specialists, plus a library loaded on demand.** | Progressive disclosure: a captioning job must not load the design system. |
| Where do 18 sources' rules live? | **`library/`** — one digest per source: what it is, the rules kept, what it gets wrong, and where each rule landed. | Keeps the loaded context small while making "combined" auditable. |
| What happens when sources contradict? | **`skills/motionframe-edit/references/precedence.md`** — a published ladder with numbered rulings. | The contradiction is the reason to combine; hiding it would waste the exercise. |
| Do we need an engine? | **Yes** — the one differentiator every source lacks is measuring the finished artifact. | No source can tell you its own render is correct. |

## Still unclear (deliberately deferred)

- **Real footage.** Every render so far is validated against a synthetic `testsrc2` fixture.
  This is the largest honest gap and it is stated as such in the README.
- **Depth of absorption per source.** 18 digests exist; the rule-by-rule audit is complete
  for the editing sources and partial for the design sources. `docs/absorption.md` tracks it.

## Excluded

- Paid services, keys, accounts, telemetry — excluded permanently.
- Redistributing any source's text or assets where the licence does not allow it.
- Reimplementing `open-edit` and `hypit`: they are applications, not doctrine. Read, credited,
  not merged.

## Phased plan

1. **Port and rename** the proven engine and gates to `motionframe-edit` / `sv`. Nothing is
   rewritten that already works (*ponytail*: the smallest complete change).
2. **Absorb** — one digest per source in `library/`, every rule either kept (with a home) or
   rejected (with a reason).
3. **Curate** — seven skills in one voice, routed by the router, contradictions resolved in
   `precedence.md`.
4. **Enforce** — eight gates on renders, seven gates on the repository itself, and a selftest
   proving both can fail.
5. **Publish** — MIT, CI green, one-command install per platform.
