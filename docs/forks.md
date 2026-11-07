# The fork network

This project began as a request to **literally fork** eighteen editing, motion and design
skill repositories and combine them. Seventeen of the eighteen are forkable; the eighteenth
(`tiktok-short-edit`) is a published document, so there is nothing to fork.

## What exists right now

Every fork below is a real GitHub fork on `jamescai-md` — same commit history, upstream
linked, licence untouched. Each forked source is then **pinned into this repository as a git
submodule** under `forks/`, so the combination is literal and reproducible rather than
implied:

```bash
git clone --recurse-submodules https://github.com/jamescai-md/motionframe-edit.git
# full combined tree (~2.6 GB). A normal clone omits forks/ and stays small.
```

| Source | Area | Licence | Upstream | Your fork | Pinned |
|---|---|---|---|---|---|
| i-hate-editing | editing | MIT | [upstream](https://github.com/ranahaani/i-hate-editing) | [jamescai-md/i-hate-editing](https://github.com/jamescai-md/i-hate-editing) | yes |
| video-use | editing | MIT | [upstream](https://github.com/browser-use/video-use) | [jamescai-md/video-use](https://github.com/jamescai-md/video-use) | yes |
| freecut | editing | MIT | [upstream](https://github.com/Moh4696/freecut) | [jamescai-md/freecut](https://github.com/jamescai-md/freecut) | yes |
| herk-edit-kit | editing/motion | NOASSERTION | [upstream](https://github.com/nateherkai/herk-edit-kit) | [jamescai-md/herk-edit-kit](https://github.com/jamescai-md/herk-edit-kit) | yes |
| video-short | editing | MIT | [upstream](https://github.com/petergyang/video-short) | [jamescai-md/video-short](https://github.com/jamescai-md/video-short) | yes |
| tiktok-short-edit | editing | document | [upstream](https://www.marwieang.com/tiktok-short-edit.md) | *not a repository* | n/a |
| open-edit | editing | Apache-2.0 | [upstream](https://github.com/veedstudio/open-edit) | [jamescai-md/open-edit](https://github.com/jamescai-md/open-edit) | yes |
| hypit | editing | NOASSERTION | [upstream](https://github.com/hypit-ai/hypit) | [jamescai-md/hypit](https://github.com/jamescai-md/hypit) | yes |
| motionmaxxing | motion | Apache-2.0 | [upstream](https://github.com/Tejashmakwana/motionmaxxing) | [jamescai-md/motionmaxxing](https://github.com/jamescai-md/motionmaxxing) | yes |
| motion-kit | motion | MIT | [upstream](https://github.com/hughminhphan/motion-kit) | [jamescai-md/motion-kit](https://github.com/jamescai-md/motion-kit) | yes |
| reelmimic | motion | MIT | [upstream](https://github.com/edenfunf/reelmimic) | — *(pending)* | no |
| hyperframes | motion | Apache-2.0 | [upstream](https://github.com/heygen-com/hyperframes) | — *(pending)* | no |
| hyperframes-launches | motion | Apache-2.0 | [upstream](https://github.com/heygen-com/hyperframes-launches) | — *(pending)* | no |
| remotion | motion | Remotion licence | [upstream](https://github.com/remotion-dev/remotion) | — *(pending)* | no |
| taste-skill | design | MIT | [upstream](https://github.com/Leonxlnx/taste-skill) | — *(pending)* | no |
| ui-ux-pro-max | design | MIT | [upstream](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | — *(pending)* | no |
| emil-skills | design | MIT | [upstream](https://github.com/emilkowalski/skills) | — *(pending)* | no |
| apple-design | design | none stated | [upstream](https://github.com/dickwu/apple-design-skill) | — *(pending)* | no |

## Why eight are pending

GitHub throttles fork creation per account: after nine in quick succession the API returns
`403 was submitted too quickly`, and a 90-second cooldown does not clear it. The remaining
eight are not blocked by permissions — the same token forked the first nine.

Two ways to finish them:

1. **Click Fork eight times** (works immediately, no throttle on the web UI):
   [reelmimic](https://github.com/edenfunf/reelmimic) ·
   [hyperframes](https://github.com/heygen-com/hyperframes) ·
   [hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) ·
   [remotion](https://github.com/remotion-dev/remotion) ·
   [taste-skill](https://github.com/Leonxlnx/taste-skill) ·
   [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) ·
   [skills (emilkowalski)](https://github.com/emilkowalski/skills) ·
   [apple-design-skill](https://github.com/dickwu/apple-design-skill)
2. **Wait for the throttle to lift** and run `python3 tools/forks.py` again — it adds any
   fork that now exists and pins it, without touching the ones already done.

Either way, `python3 tools/forks.py --pending` prints exactly what is missing.

## Status is machine-readable

`forks.json` is the manifest: upstream, fork, licence, area, and status for all eighteen.
`tools/forks.py --check` fails if a fork exists but is not pinned, so this table cannot
drift from reality by hand-editing.
