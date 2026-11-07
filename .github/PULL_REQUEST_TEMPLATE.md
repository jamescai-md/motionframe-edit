## What this changes

<!-- One paragraph. What was wrong or missing, and what you did about it. -->

## Why it is better

<!-- Numbers beat adjectives. "40ms instead of 120ms because ..." -->

## Checks

- [ ] `python3 tools/lint.py` passes
- [ ] `python3 -m unittest discover -s tests -v` passes
- [ ] `python3 tools/sv.py demo --selftest` passes (needs ffmpeg)
- [ ] If I added or changed a **rule**, it is enforced somewhere (a gate, a lint check, a test) — not just prose
- [ ] If I added or changed a **gate**, I added a fixture that proves it can fail
- [ ] If I carried an idea across from another project, `ATTRIBUTION.md` is updated
- [ ] No paid dependency, API key, or network call was introduced

## Notes for the reviewer

<!-- Anything you are unsure about, or deliberately left out of scope. -->
