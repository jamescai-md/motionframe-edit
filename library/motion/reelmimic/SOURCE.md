# reelmimic

**Upstream:** https://github.com/edenfunf/reelmimic  
**Licence:** MIT  
**Pinned at commit:** `311d835b623e`  
**Mode:** copy  
**Doctrine files:** 389  
**Bytes:** 3,542,074

## What this is

The source's doctrine, copied verbatim under its own licence. Its LICENCE file
travels with it as `LICENCE.upstream`, so the terms are in the same folder as the
text they cover.

## What was taken

Skill definitions, rule files, references and guides — the material that changes a
decision. Each file keeps its original relative path so it can be diffed against
upstream.

## What was left out

Binary assets, translations, release notes, tests, packaging and tooling. 1 file(s) were byte-identical mirrors of files already copied (sources ship the same skill under `.claude/skills/` and `.agents/skills/`).

## How it is used here

`skills/` routes to it. Nothing in this folder is edited by this project: it is
reference material, loaded on demand, so the merged doctrine in `skills/` can always
be checked against the sources it came from.
