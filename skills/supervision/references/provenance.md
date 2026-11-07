# Lineage — what came from where, and what it was missing

`supervision` is a synthesis, not a wrapper. Nothing here is vendored, forked code:
each source contributed a craft idea or a discipline, and the gaps in one are
filled by another. This file is the honest map, so you can go upstream for depth
when you need it.

**Licensing:** the doctrine was rewritten — no text and no code were copied, and nothing
here is forked or vendored. Seventeen of the twenty-two repositories are MIT or
Apache-2.0. Five are not: `anthropics/skills` and `dickwu/apple-design-skill` carry no
licence file, and `nateherkai/herk-edit-kit`, `remotion-dev/remotion` and `hypit-ai/hypit`
report `NOASSERTION`. Only publicly observable ideas informed this work. Every link and
every licence is checked by `python3 tools/verify-sources.py`.
Full notices: `/ATTRIBUTION.md`.

## The agent-engineering sources

| Source | Its strength | Its gap (why you'd otherwise open another skill) | In supervision |
|---|---|---|---|
| [**obra/superpowers**](https://github.com/obra/superpowers) | process discipline: brainstorm → plan → execute → verify, parallel subagents, "verification before completion" | entirely software engineering; says nothing about how a cut or a page should *feel* | the loop and the two STOP gates; `gatekeeper` is its verification culture applied to media |
| [**morluto/rea**](https://github.com/morluto/rea) | investigating a real artifact down to the implementation before reimagining it | a heavyweight MCP server for binary/app analysis; no editorial craft | the investigative posture behind law 6: capture the real thing, never a mockup of it |
| [**addyosmani/agent-skills**](https://github.com/addyosmani/agent-skills) | constraint-driven development: write the quality bar as a contract so an agent cannot quietly lower it | 25 engineering skills, zero media craft | the quality bar became the gates — written down, checkable, enforced |
| [**anthropics/skills**](https://github.com/anthropics/skills) | the SKILL.md format itself, progressive disclosure, and `frontend-design` | format and examples, not a working doctrine; no video, no process enforcement | the file structure, the description-first routing, the reference split |
| [**mattpocock/skills**](https://github.com/mattpocock/skills) | writing *for agents*: terse, imperative, no hedging; deep-module vocabulary; the "grill me" interview | TypeScript-centric; no visual work | how every file here is written — imperative, checkable, no adjectives standing in for rules |
| [**wayfinder**](https://www.marwieang.com/wayfinder-skill.md) (marwieang) | guided requirement exploration → a phased plan without tickets | planning only, stops at the plan | STOP 1: the plan is written in plain English and approved before anything is built |
| **ponytail** *(unpinned — see ATTRIBUTION.md)* | the smallest change that fully solves it; a debt ledger; ruthless review | brevity can under-deliver on craft; "one line that works" is not always possible in a film | the "delete the move" instinct, the fix order, and cutting scope instead of quality |

## The video and motion sources

| Source | Its strength | Its gap | In supervision |
|---|---|---|---|
| [**i-hate-editing**](https://github.com/ranahaani/i-hate-editing) | the full studio: taste memory, hard rules won from rejected renders, a real delivery package | depends on a signed-in browser for voice enhancement and a local image proxy; talking-head only | law 12 (taste memory), the hard rules, the delivery package — all reimplemented with no accounts |
| [**video-use**](https://github.com/browser-use/video-use) | the sharpest correctness rules anywhere: captions last, per-segment concat, 30 ms fades, PTS-shifted overlays, output-timeline SRT | ElevenLabs/Scribe API keys | those rules became the engine's behaviour *and* gate G5/G6; local ASR replaces the API |
| [**freecut**](https://github.com/walterlow/freecut) | the same discipline with local Whisper by default | no design or motion doctrine; still ships optional paid backends | the free/local constraint became non-negotiable here |
| [**herk-edit-kit**](https://github.com/nateherkai/herk-edit-kit) | motion handoffs and arrival-from-oversize, inside a HyperFrames edit kit | bound to the HyperFrames runtime and an agency register | `motion-director`'s handoff and arrival laws; G3 measures the dead frame in our own terms |
| [**hyperframes**](https://github.com/heygen-com/hyperframes) | a real HTML/GSAP motion runtime, production-proven | install weight; a runtime assumption, not a craft guide | lane B in `motion-director/references/lanes.md`, with a portable capture loop |
| [**remotion**](https://github.com/remotion-dev/remotion) | React-native video: compositions, `useCurrentFrame`, parametric variants | framework lock-in, build weight, licence nuance for teams | lane C, and the honest note that lane B has no licence question |
| [**motion-kit**](https://github.com/hughminhphan/motion-kit) | a compact motion-designer role definition | thin; no verification, no timing tables | folded into `motion-director` |
| [**reelmimic**](https://github.com/edenfunf/reelmimic) | 36 named visual styles — paper cutout, anime cel, whiteboard, pixel art — with worked examples | scattered, uneven, no gates; style without standards | the style *catalogue* as a menu in `motion-director`, made subject to the one-system law |
| [**motionmaxxing**](https://github.com/Tejashmakwana/motionmaxxing) | motion doctrine plus computed gates (G0–G5) and a "look honestly" pass | complex toolchain, paid voice/music dependencies | the idea that a motion piece can be *gated at all*; reimplemented with free measurement |
| [**open-edit**](https://github.com/veedstudio/open-edit) / [**hypit**](https://github.com/hypit-ai/hypit) | real open-source editing applications | they are apps, not skills; nothing to learn about judgement | the reminder that the tool is not the deliverable — the package is |
| [**hyperframes-launches**](https://github.com/heygen-com/hyperframes-launches) | worked launch films, end to end | examples only, no transferable rules | the beat-sheet format and the "hardest beat first" build order |
| [**video-short**](https://github.com/petergyang/video-short) | the best short-form vertical workflow: layouts, receipts, frame-by-frame review, QA stills | an optional paid image/video/music key; no design system | the layout table (`a-roll`/`punch`/`split`/`receipt`/`page`), the review loop, the QA habit |
| [**tiktok-short-edit**](https://www.marwieang.com/tiktok-short-edit.md) | a tight, complete vertical edit recipe with synthesized audio | no audit layer; safe-zone advice only | the pacing rule ("something changes every 2–3 s") and the synthesized-audio stance, now enforced by G3 |

## The design sources

| Source | Its strength | Its gap | In supervision |
|---|---|---|---|
| [**ui-ux-pro-max**](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | breadth: brand, tokens, slides, banners, component styling | encourages gradients, glow and "premium" effects that read as slop elsewhere; no adjudication | the token/system discipline (`design-director/references/system.md`); its visual register is overruled by `precedence.md` |
| [**taste-skill**](https://github.com/Leonxlnx/taste-skill) | art direction from reference images plus a browser check, instead of accepting a generic generated page; an anti-slop stance | web only; extremely prescriptive; contradicts the source above with no tie-breaker | `design-director`'s reference-first authoring and `references/anti-slop.md`; the contradictions are resolved in `precedence.md` |
| [**emil-skills**](https://github.com/attentiondotnet/emilkowalski_skills) | interface motion craft: should-it-animate, springs, choreography, frame budget | React/web only; nothing about film or footage | `ui-motion`, almost whole; the "flag by default" review stance |
| [**apple-design**](https://github.com/dickwu/apple-design-skill) (dickwu) | HIG-grounded review of interface craft | review only, no build guidance; no licence file | the review rubric folded into `ui-motion`, ideas only |

## What the combination actually fixes

| Flaw in the sources | Who covers it |
|---|---|
| Paid APIs and accounts everywhere | `supervision` law: free and local; `sv` uses ffmpeg + stdlib only |
| Correctness rules in one place, craft in another | both live in the engine and the gates, not in prose |
| Contradictory taste advice (gradients, motion, restraint) | `references/precedence.md` — a ladder, plus twelve documented resolutions |
| No verification of the finished artifact | `gatekeeper` — eight measured gates, and `sv demo --selftest` proving they can fail |
| Framework lock-in (HyperFrames, Remotion, a specific NLE) | three lanes, one motion spec, chosen by need |
| Nothing remembers corrections | `taste-memory` |
| Twenty skills to install, twenty descriptions to route | one router with a table, seven specialists, progressive disclosure |
| Examples that do not transfer | rules that do, with worked numbers |
