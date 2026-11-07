# A real render, and the report that measured it

Both files here were produced by `mfe.py` on 2026-11-07, not drawn by hand:

| File | What it is |
|---|---|
| `demo-540p.mp4` | 13.6 s vertical render from `python3 tools/mfe.py demo`, downscaled from 1080×1920 to 540×960 so the repository stays small |
| `gate-report.json` | the report from that 1080×1920 render, unmodified |

All eight gates passed on it: duration within 0.12 s of plan, 1080×1920 at 29.93 fps,
−14 dB LUFS loudness, no freeze, no black interval, no cut popping above the local body level,
captions inside the safe zone, and every asset declaring an origin.

## What this does and does not show

It shows the toolchain runs end to end and the report is a measurement rather than a claim.
You can check the numbers yourself:

```bash
python3 tools/mfe.py doctor
python3 tools/mfe.py demo --selftest    # renders, audits, and proves the gates can fail
```

It does not show the gates are hard to fool on real footage. The fixture is generated with
known properties; a real camera introduces rotation metadata, variable frame rate and noise
that the fixture never produces. That limitation is the first item in
[docs/plan.md](../../docs/plan.md).

## Why the clip is smaller than the report

The report describes the 1080×1920 render. The committed clip is that render scaled to 540
pixels wide at CRF 33, so the numbers in the report no longer describe the file byte for byte —
duration, frame count and audio loudness carry over, sharpness does not. The unmodified
1080×1920 file is 5.4 MB and was left out deliberately.
