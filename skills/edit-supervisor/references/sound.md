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

`mfe gate` measures both with `ebur128` and fails outside ±2 LU of target.
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

## SFX — the visual-event map

Sound effects are not decoration sprinkled on cuts; they are the audible half of a physical
action. Build them from a list, not from mood.

**Write the event map first.** For each shot, name the events that deserve a sound:

| Visual event | Sound | Where it lands |
|---|---|---|
| an object makes contact (logo lands, card hits, stamp) | impact — low body + click | peak on the contact frame, not the file's start |
| a spatial move (camera whips, element flies in) | whoosh — filtered noise | tail of the whoosh into the cut, 1–3 frames early |
| a small UI action (toggle, tap, tick) | dry click or soft tap | on the frame, quiet |
| text or a number appears with weight | short sub-thump or single tick | on the frame |
| a section ends, or a turn is coming | riser, or **silence** | riser ends on the cut; silence needs nothing |
| a place is established | room tone / ambience | under everything, constant, very low |

**Alignment beats choice.** The rule that matters most, from a launch handoff:
*"Give each sound cue a visible event; align its audible impact, not its file start."* A file
whose peak is 200 ms in has to be trimmed so its peak hits the frame.

**The ban list.** Laser zaps, pitch-drop plops, sci-fi chirps, camera-shutter clicks, and a
whoosh on every transition. Each one is a recognisable stock-file tell. Also: no SFX under a
cut with no visible action — that is the definition of decoration.

**Levels.** SFX sit under the voice and above the music bed: roughly −12 to −6 dB relative to
dialogue for an accent that should be felt, −20 dB for texture. If an effect is the loudest
thing in a window containing speech, it is too loud, regardless of how good it sounds.

### Where effects come from, and the licence line

No paid dependency, ever. Three routes, and say which you used:

1. **Retrieval, free and keyless.** Openverse's audio index (most results are Freesound) takes
   `license=cc0,by` and needs no account. This is what the HyperFrames launch pipeline in
   `library/motion/hyperframes/upstream/skills/media-use/audio/references/sfx.md` does, and its
   licence discipline is the part worth keeping:
   - **CC0 or CC BY only.** Never NonCommercial, ShareAlike or NoDerivatives — those cannot
     travel in work you hand to someone else.
   - **Credit every CC BY sound** in `CREDITS.md`, with the artist and the licence, and keep
     that file with the project. CC0 needs no credit but still gets recorded in
     `provenance.json` as `stock-licensed`.
   - **One asset per effect name**, reused across cues. A whoosh is a whoosh.
   - **No match means skip, not fail.** A missing effect is recorded and the render continues;
     sound design of the whole piece is never blocked by one cue.
2. **A small local library**, curated and licence-checked once, so a project works offline.
3. **Synthesis**, below — offline, frame-exact, and often the better answer for transitions.
2. **Synthesise it.** For transitions and impacts a generated sound is often better than stock,
   because it can be timed to the frame. These run with the ffmpeg you already have:

```bash
# impact: 55 Hz body + a 30 ms click, exponential decay, peak ≈ -5 dBFS
ffmpeg -y -f lavfi -i "sine=frequency=55:duration=0.35,volume=0.9" \
       -f lavfi -i "anoisesrc=duration=0.03:color=white:amplitude=0.5" \
  -filter_complex "[0:a]afade=t=out:st=0.02:d=0.33:curve=exp[body];\
                   [1:a]afade=t=out:st=0:d=0.03:curve=exp[click];\
                   [body][click]amix=inputs=2:normalize=0[a]" -map "[a]" impact.wav

# whoosh: shaped pink noise, 0.55 s, peak ≈ -7 dBFS
ffmpeg -y -f lavfi -i "anoisesrc=duration=0.55:color=pink:amplitude=0.6" \
  -af "highpass=f=350,lowpass=f=5200,afade=t=in:st=0:d=0.22,\
       afade=t=out:st=0.33:d=0.22,volume=6dB" whoosh.wav

# riser: noise swelling over 1 s, cut on the drop
ffmpeg -y -f lavfi -i "anoisesrc=duration=1.2:color=pink:amplitude=0.5" \
  -af "highpass=f=600,afade=t=in:st=0:d=1.0:curve=exp,volume=10dB" riser.wav
```

Each is a starting point: render it, look at the waveform, move the decay and the peak, and
check the peak lands where the picture does.

**What you must say about SFX at handoff:** how many, on which events, and that you cannot hear
them. "Six effects, each on a contact or a transition, peaks trimmed to the frame; I have not
heard the mix — check the whooshes are not stepped on by the dialogue."

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

That sentence is the difference between motionframe-edit and wishful thinking.
