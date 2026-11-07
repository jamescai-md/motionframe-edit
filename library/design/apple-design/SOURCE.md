# apple-design

**Upstream:** https://github.com/dickwu/apple-design-skill  
**Licence:** no licence file  
**Pinned at commit:** `ff4ebddf0488`  
**Mode:** summarise  
**Doctrine files:** 0  
**Bytes:** 0

## Why nothing was copied

The licence (no licence file) does not permit redistribution, so no text, code or asset
from this source is included. What follows is a summary written for this project:
the ideas, in this project's words, which is what copyright does not cover.

If you want the source itself, use the upstream link above. If its terms suit you
better than these notes, that is a legitimate reason to go there — the point of this
repository is not to stop you reading the originals.

## Summary used by this project

# apple-design-skill — a HIG-grounded review rubric

**Licence:** none stated — **summarised, not redistributed** ·
**Source:** https://github.com/dickwu/apple-design-skill · **Absorbed:** 2026-11-07

## What it is
A review skill that audits interfaces through Apple's Human Interface Guidelines, with
references loaded by what is on screen, plus a code-audit pass for platform marks and
payment buttons.

## Rules worth keeping
1. **Audit through fixed lenses, in a fixed order** — platform conventions, hierarchy,
   typography, colour/contrast, motion — so two reviewers reach comparable verdicts.
2. **Load the reference by what is on screen**, not the whole guideline set: a review that
   cites everything cites nothing.
3. **Platform convention is a correctness issue, not a taste issue.** A wrong back-button,
   a misused payment mark, or a broken safe area is a defect.
4. **Write a report with severities**, not a list of opinions.

## What it gets wrong
Review only — it will tell you what is wrong and never how to build it right. And with no
licence file, only the ideas were taken.

## Where this landed
`gatekeeper/references/critic.md` (1, 4 — the fixed-lens order and severity report) ·
`design-director/references/anti-slop.md` (2, 3) · the design gates D0–D8 in
`specs/gates.json`.
