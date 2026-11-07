# Status, and what is not finished

This project is a first release, not a finished product. This page lists what is known to be
unfinished or weak, in the order it matters, so nobody has to discover it by accident.

## Known gaps

**1. Renders are validated against a synthetic fixture, not real footage.**
`mfe.py demo --selftest` builds a test clip with known defects — a freeze, a silent stretch, a
wrong aspect — and proves the gates catch them. That tests the gates, not your camera. On real
footage, expect to correct frame-rate and rotation mismatches the fixture never produces.

**2. Rule-level tracing is partial.**
`docs/absorption.md` maps each source to the files in `skills/` that carry its capability. That
is a topic-level map. Only one source has been traced at the level of individual rules
(`i-hate-editing`, in `skills/edit-supervisor/references/cutting.md`), where five rules the
earlier draft missed were added. Until the rest are done, "combined" is a claim about ideas,
not a line-by-line audit.

**3. Loudness and safe zones are measured; whether the edit is any good is not.**
The gates check duration, aspect, loudness, freeze, black, cut boundaries, caption placement
and asset provenance. None of them can tell you the pacing is wrong.

**4. Four sources are here on the maintainer's stated permission.**
`hypit`, `remotion`, `apple-design` and the TikTok short-edit document do not grant
redistribution. Their folders record the basis in `PERMISSION.md`. If you are redistributing
this repository further, read `NOTICE` first — the MIT licence does not cover them.

**5. One motion lane has its own licence.**
Remotion is free only below a company-size threshold. It is optional: the other two lanes
(HTML + GSAP + headless Chrome, and ffmpeg alone) carry no such condition.

**6. No Windows-native testing.**
CI runs Python 3.10, 3.12 and 3.13 on Linux. `install.sh` is POSIX shell; on Windows it
assumes WSL or Git Bash. Nobody has tested PowerShell.

## What would move this forward

1. **Finish the rule-level audit** for the other seventeen sources, in the format used for
   `i-hate-editing`: every rule in the source, marked covered or missing, missing ones written.
2. **Run the gates on real footage** from three cameras with different rotation metadata, and
   record where they disagree with a human reviewer.
3. **Windows check** on a fresh machine, then either support it or say plainly that it is
   unsupported.

## How to see the current state for yourself

```bash
python3 tools/gate-docs.py          # the repository's own documentation checks
python3 tools/absorb.py --check      # all 18 sources present, each with its licence basis
python3 -m unittest discover -s tests
```

CI runs all three on every push, plus a clean-machine install.
