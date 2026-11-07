# Lineage — why these twenty-five

The full per-source table (strength, gap, where the gap is filled) lives in
[`skills/supervision/references/provenance.md`](../skills/supervision/references/provenance.md),
where the agent can reach it. This page is the human-facing version: why these
sources, and what the combination actually fixed.

## The premise

Each of the 25 sources — twenty-two repositories, two published documents and one idea
that could not be pinned to a repository — is good at one thing and weak at another, and
the weaknesses
tend to be complementary. That is why people install ten of them and still get bad
output: the tools are complementary, but **nobody arbitrated between them**.

`supervision` is that arbitration, plus the missing layer none of them had — a
measured audit of the finished artifact.

## The five systematic flaws, and what covers each

| Flaw | Where it appears | Covered by |
|---|---|---|
| **Paid dependency** — a cloud ASR, voice, image or music API in the happy path | video-use, i-hate-editing, video-short, motionmaxxing | one local engine (`tools/sv.py`), ffmpeg-only, and a lint rule that fails the build on a paid key |
| **Correctness without craft** — impeccable hard rules, no opinion about whether the thing is any good | video-use, freecut | the craft references (cutting, timing, anti-slop) load alongside the rules |
| **Craft without correctness** — beautiful doctrine, silent breakage | herk-edit-kit, motionmaxxing, taste-skill | the hard rules became the engine's behaviour *and* gates G5/G6 |
| **Contradictory taste** — gradients banned in one, load-bearing in another; animate everything vs animate nothing | taste-skill ↔ ui-ux-pro-max, emil-skills ↔ motionmaxxing | `references/precedence.md`: a seven-rung ladder and twelve documented rulings |
| **No verification** — "verification before completion" as a slogan, never a measurement of a *video* | essentially all of them | `gatekeeper`: eight gates with numbers, plus `sv demo --selftest` proving they can fail |

Two more that matter in daily use:

| Flaw | Covered by |
|---|---|
| Nothing remembers your corrections | `taste-memory` + `taste.md` |
| Framework lock-in (HyperFrames *or* Remotion *or* this NLE) | three lanes, one motion spec, all optional |

## The three sources that changed the most

**video-use / freecut** contributed the sharpest correctness rules in the whole
collection — captions last, per-segment lossless concat, 30 ms fades, PTS-shifted
overlays, output-timeline subtitle maths. Their flaw was that those rules lived in
prose, behind an API key. Here they are the engine's behaviour, they run without an
account, and G5/G6 fail the build when they are violated.

[**taste-skill**](https://github.com/Leonxlnx/taste-skill) contributed an art-direction posture worth stealing: start from
reference images and check the result in a browser, rather than accepting whatever a
model produces by default — and name slop instead of hand-waving at it. Its flaw was
being web-only, extremely prescriptive, and in direct contradiction with another
installed skill. Here that reference-first stance opens `design-director`, and the
contradictions are decided in public.

*(An earlier version of this page credited taste-skill with a "kind of business" step
that the repository does not actually state. The step stayed — it earns its place —
but the credit was wrong and has been removed from the source table.)*

**superpowers** contributed process: brainstorm → plan → execute → verify, and the
idea that an agent should prove completion rather than claim it. Its flaw was that
it is entirely about software. This repo is that culture pointed at pictures and
sound, with the proof made numeric.

## What was left behind, deliberately

- **Vendored assets.** No fonts, shaders, style libraries or example films are
  redistributed. Licensing varies and a skill repo should not become an asset dump.
- **Applications.** `open-edit` and `hypit` are editors. Useful, but they are tools;
  the thing worth carrying was the workflow shape, not the code.
- **The API-key happy paths.** Every one removed. That is not a limitation to be
  improved on later; it is the constraint that makes the suite shareable.
