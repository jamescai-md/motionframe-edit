# hyperframes — write HTML, render video

**Licence:** Apache-2.0 · **Source:** https://github.com/heygen-com/hyperframes · **Absorbed:** 2026-11-07 as a lane, not as doctrine

## What it is
A production HTML/GSAP motion runtime with an agent-facing guide, a composition contract,
a player/studio, and an importer. The guide (`claude-design-hyperframes.md`) is genuinely
well written for agents.

## Rules worth keeping
1. **Mostly hard cuts; at most one "shader moment"** in a first draft. Fancy transitions
   are the first refuge of a piece with no idea.
2. **Anti-monoculture:** do not ship the framework's default palette, default type, or the
   default three-card layout. Every composition fills identity explicitly.
3. **Seek-safety:** the composition must render identically when scrubbed to any frame,
   which forbids state that depends on playback history.
4. **Self-contained composition**: one HTML file, no external fetches at render time.
5. **The importer checks a contract** — dimensions, scene count, identity on `:root` — and
   returns 422 if it is wrong. Contracts over conventions.

## What it gets wrong
It is a runtime with a gravity well: adopt it and the piece is HyperFrames-shaped. Install
weight is real, and its guides assume its own studio.

## Where this landed
`motion-director/references/lanes.md` lane B (all five rules) · the "one system per piece"
law was sharpened by (2). The runtime is **optional** here; nothing depends on it.
