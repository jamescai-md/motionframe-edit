# Worked example — three takes to a 45-second Reel

A real session, abbreviated. The interesting part is not the commands; it is the
decisions and the audit.

## What the user said

> "I filmed three takes about our new offline mode. Make me a Reel. Keep it tight,
> I hate waffle. No music."

That is a brief. Not a spec. Everything below is supervision filling it in.

## 0 · Taste and inventory

```bash
sv.py scaffold ./offline-reel
# → brief.md, taste.md, edl.json, provenance.json, footage/

sv.py probe footage/*.mp4
```

```
take-01.mp4   62.4s  1920x1080 rot=90 → display 1080x1920  @29.97fps  h264/aac
take-02.mp4   48.1s  1920x1080 rot=90 → display 1080x1920  @29.97fps  h264/aac
take-03.mp4   51.7s  1920x1080 rot=90 → display 1080x1920  @29.97fps  h264/aac
```

Three things noted, in writing, before touching anything:

- Rotation metadata: the streams say 1920×1080, the *display* is 1080×1920. Reading
  the stream size would letterbox the entire edit.
- 29.97, not 30. The profile demands 30, so every segment gets normalised on extract.
- Take 3 is 51.7 s for the same content as take 1's 62.4 s — it is the tightest read.

## 1 · Transcribe and pack

```bash
whisper-cli -m ggml-large-v3.bin -ml 1 -l en -oj footage/take-01.wav   # ×3, cached
# pack → takes.md, phrase-level, time-ranged
```

The packed view is what gets read, not the video:

```
## take-03  (51.7s, 14 phrases)
  [000.42-004.10] S0 Offline mode started as a bug report. One line: "I lost two hours of work."
  [004.80-006.20] S0 That was enough.
  [007.10-011.40] S0 So every edit now lands in a local log before it touches the network.
  [018.20-022.80] S0 Which means the forty minutes you spent on a plane are not gone.
```

Retake pattern spotted: all three files open with a variant of the same line, and
take 3's version is the shortest and most specific. Keep take 3 for the hook.

## 2 · Plan (written, then approved)

> The hook is the bug report itself — take 3's version, 3.7 s, cut straight after
> "That was enough." Then the mechanism in two sentences, then the payoff: the
> plane line, held for 5 s with the real changelog captured on screen. No music, so
> the silence has to be designed: one 0.6 s hole before the payoff.
>
> 9:16, 42–46 s, captions bold with the active word accented, neutral grade. Two
> full-screen visuals only: the real changelog, and the local log file. No B-roll —
> there is nothing real to show that is better than the speaker's face.
>
> **I will not add a call to action** — the brief did not ask, and "link in bio"
> would be invented speech.

User: *"go, but make the changelog bit longer"* → one revision to the plan, one
segment duration, then build.

## 3 · The EDL

```json
{
  "version": 1, "project": "offline-reel", "profile": "vertical-9x16",
  "sources": { "A": "footage/take-03.mp4", "B": "footage/take-02.mp4" },
  "segments": [
    { "id": "s1", "source": "A", "start": 0.42, "end": 4.10, "beat": "HOOK",
      "fit": "fill", "framing": [0.5, 0.38],
      "quote": "Offline mode started as a bug report. I lost two hours of work." },
    { "id": "s2", "source": "A", "start": 7.10, "end": 11.40, "beat": "MECHANISM",
      "quote": "Every edit lands in a local log before it touches the network." },
    { "id": "s3", "source": "B", "start": 22.40, "end": 28.10, "beat": "PROOF",
      "quote": "Here is the log file itself." },
    { "id": "s4", "source": "A", "start": 18.20, "end": 22.80, "beat": "PAYOFF",
      "quote": "The forty minutes you spent on a plane are not gone." }
  ],
  "captions": { "enabled": true, "style": "bold-pop", "file": "captions.ass" }
}
```

Every edge is a word boundary, padded 60 ms. `framing: [0.5, 0.38]` lifts the crop so
the face is not centred on his chin. The grade is `neutral` — an offline-mode story
does not need a look.

## 4 · Draft, then the audit nobody skips

```bash
sv.py captions --edl edl.json --words work/take-03.words.json --remap A --out captions.ass
sv.py render   --edl edl.json --out work/draft.mp4 --preview
sv.py gate     --file work/draft.mp4 --edl edl.json --boxes captions.boxes.json
```

First pass — **failed**, as first passes do:

```
  PASS  G0  render exists: duration 21.55s vs planned 21.50s (Δ0.05s)
  PASS  G1  delivery shape: 1080x1920 @30fps
  PASS  G2  loudness: -15.8 LUFS (target -14±2), true peak -2.1 dBTP
  FAIL  G3  picture alive: 1 stretch > 3.0s with no visual change: [12.4]
  PASS  G4  no black holes: none detected
  FAIL  G5  cuts don't pop: 3 boundaries checked, 1 spike: [(9.18, 11.4)]
  PASS  G7  honest proof: 4 assets, all origins declared
  verdict: FAIL
```

What that meant, and what got fixed:

- **G3 at 12.4 s** — the changelog capture was a still. That is a dead frame, and it
  was the beat the whole piece exists for. Fixed by making the page slowly scroll
  (`page:` treatment), which also made the payoff land better.
- **G5 at 9.18 s** — the join between the two source files had `fade_out: 0` because
  it was the end of a file, not a cut inside one. One missing 30 ms fade, one audible
  click. Fixed in the EDL, not by re-recording.
- **G2 at −15.8** — `loudnorm` with a single-pass estimate. Corrected to target in the
  composite pass; second run lands at −14.1.

Second pass: all gates pass, one warning kept (a 0.6 s hold before the payoff, which
G3 allows and the plan intended).

## 5 · Look

```bash
sv.py sheet --file work/draft.mp4 --out work/sheet.jpg --every 2
```

Six frames described in one sentence each — the discipline that catches what numbers
cannot:

1. Face, close, mid-sentence. Caption: "ONE LINE". Good.
2. Face, same crop, 4 s later. *Same frame as 1 — the cut did not change the image.*
3. Changelog, scrolled, real UI. Caption readable over the white panel. Good.
4. Changelog, further down. Fine.
5. Face, payoff line. **Caption sits exactly on his mouth** — legal by the box math,
   wrong by eye. Fixed by raising the caption margin for this beat.
6. Face, end. 1.1 s hold. Good.

Frame 2 and frame 5 are why a contact sheet exists. Neither is a gate failure; both
are things a viewer notices.

## 6 · Deliver

```
out/
├── offline-reel-9x16.mp4     43.2s · 1080x1920 · -14.1 LUFS
├── captions.srt              28 cues, proofread
├── thumbnail.jpg             frame 6 (the payoff face), text-free
├── report.md
├── gate-report.json          all pass, 1 intentional warning
└── provenance.json           changelog = captured, log file = captured
```

The handoff line:

> "All eight gates pass. −14.1 LUFS, true peak −1.9 dBTP. Two visuals, both captured
> from the real app. I can't hear it — with no music, check the 0.6 s hole before the
> payoff doesn't read as a stall on a phone speaker."

## 7 · What the next session inherits

```markdown
## Pacing
- 0.6 s hole before a payoff works. Keep doing it. (replaced: filling every gap)
## Captions
- Raise the caption margin on close-crop shots; the box math passes but it covers the mouth.
## Look
- Neutral grade on product stories. (replaced: warm_cinematic)
```

That is the difference between a skill and a skill with memory. The second Reel
starts here.
