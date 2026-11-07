# Sound

You cannot hear the mix. That is the central fact of this file. You have
measurements and a waveform, and you have to be honest about the difference.

## Targets

| Destination | Integrated | True peak | Notes |
|---|---|---|---|
| TikTok / Reels / Shorts | −14 LUFS | ≤ −1 dBTP | platforms normalise down, never up |
| YouTube long form | −14 LUFS | ≤ −1 dBTP | |
| Podcast / interview | −16 LUFS | ≤ −1 dBTP | mono-ish is fine, dialogue-first |
| Broadcast | −23 LUFS | ≤ −2 dBTP | EBU R128 |
| Any | — | ≤ −1 dBTP | a true peak above 0 clips on encode |

`sv gate` measures both with `ebur128` and fails outside ±2 LU of target.
Normalise with `loudnorm` in the same pass that composites — not afterwards,
which re-encodes the picture for an audio change.

## The mix, in priority order

```
1  voice          intelligible, consistent, forward
2  music          present, ducked under speech, resolving with the picture
3  sfx            accents on visual events only
4  ambience       only if it establishes a place
```

If you can only get one right, it is the voice. A piece with no music and a clear
voice reads as intentional; a piece with music over a buried voice reads as broken.

## Ducking

Music must drop when the speaker speaks, not sit at one level and fight.

- Static bed under continuous speech: −18 to −22 dB relative to the voice.
- Music-led sections: −10 to −14 dB, with the voice still on top.
- Duck hard on the first syllable after a music-only section; recover over
  250–400 ms, not instantly.
- Sidechain-style ducking with a fast attack (10–30 ms) and slow release
  (300–500 ms) is the difference between "produced" and "two files played at once".

## Making a pop or a sting audible

A sting that is silent in the mix passes every level check, because the loudest
thing in that window is the voice. Measuring the master alone tells you about the
voice, not the effect.

**Measure by differencing.** Render the same window twice — master, and voice-only
cut — and compare. The delta is the sting. Correct for the few dB the render
attenuates the source audio by, measured on sting-free speech windows. A negative
lift is impossible from addition: if you see one, you have not applied that
correction.

Placement beats level:

- A sting lands **1–3 frames before** the visual event, not on it.
- One SFX per visible event. A whoosh on every transition is the single most
  common tell of a machine-made edit.
- Silence is an effect. A 200–400 ms hole before a drop does more than a riser.

## Voice treatment, in order

1. **Clean** — high-pass at 80–100 Hz (removes rumble, keeps body), a gentle
   de-esser if sibilance bites, a de-noise pass *only* if hiss is audible.
2. **Compress** — ratio 3:1, threshold around −18 dB, attack 6 ms, release 110 ms.
   This is for consistency, not loudness.
3. **Limit** — a true-peak limiter at −1 dBTP as the last step, always.
4. **Never** pitch-shift or time-stretch the voice to fit a runtime. Cut words.

Over-processing is worse than no processing: a fully "enhanced" voice sounds
synthetic and immediately reads as AI. If the source is usable, use it.

## What you must say at handoff

One line, every time:

> "Measured −14.2 LUFS, true peak −1.3 dBTP, music ducks 6 dB under speech. I can't
> hear it — check that the music sits under the voice on a phone speaker."

That sentence is the difference between supervision and wishful thinking.
