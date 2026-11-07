# remotion — video as a React component

**Licence:** Remotion licence (NOASSERTION) — **summarised, not redistributed.**
Not free for companies; check before commercial use ·
**Source:** https://github.com/remotion-dev/remotion · **Absorbed:** 2026-11-07

## What it is
Programmatic video in React: compositions, `useCurrentFrame`, `<Sequence>`, parametric
renders. The most ergonomic option if the team already writes React.

## Rules worth keeping
1. **Determinism is the contract.** A frame must be a pure function of its index; no
   `Date.now()`, no `Math.random()` without a seed, no state that depends on play order.
2. **Parametrise variants** instead of duplicating: one composition, many data objects, is
   how a system survives its second client.
3. **Sequences are explicit** — every element has a start frame and a duration, declared.
4. **Preview is the same code path as render.** If preview and output differ, the preview
   is a lie.

## What it gets wrong
Framework lock-in and a licence that is *not* free for companies — the single biggest trap
in this collection, because it is invisible until procurement. Build weight is also real.

## Where this landed
`motion-director/references/lanes.md` lane C, including the licence warning in the lane
table and in the README · determinism (1) and parametrisation (2) are stated as the lane's
rules. No remotion code is shipped or required.
