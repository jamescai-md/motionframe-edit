# open-edit — an agent-driven editing pipeline (an application)

**Licence:** Apache-2.0 · **Source:** https://github.com/veedstudio/open-edit · **Absorbed:** none, by design

## What it is
A CLI pipeline for agents: `login`, `token`, `transcribe`, `whisper`, `words`, `generate`,
`background-removal`, `lipsync`, `veed-project`, `fal`. Substantial, and it works — but it
is a tool, not a doctrine.

## Rules worth keeping
*None of its doctrine. Two observations, which are not rules:*

1. **Subtitles first-class**: a word-level transcript as the primary data structure, which
   is the same conclusion `video-use` reached independently.
2. **The tool is not the deliverable.** Everything here is machinery; none of it decides
   what the piece should be.

## What it gets wrong (for this project's purposes)
`login`/`token` and `fal` mean accounts and paid jobs in the happy path, and the pipeline
is bound to one vendor's project format.

## Where this landed
Nothing was copied. It is credited because it was read, and because its existence is the
argument for this project's shape: an open editor with accounts is a better tool and worse
doctrine.
