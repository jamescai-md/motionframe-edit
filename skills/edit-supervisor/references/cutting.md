# Cutting

Cutting is deciding what the viewer does not see. Everything here is judgement —
the only hard rules are the ones in `../SKILL.md` that prevent silent breakage.

## Audio is the timeline

You never cut by looking. Candidates come from two signals:

- **Word boundaries** from the transcript — the precise edge.
- **Silence gaps** from the audio — the safe place to put it.

| Gap | Meaning | Action |
|---|---|---|
| ≥ 600 ms | real air, a paragraph break | cut here, or keep as a beat |
| 400–600 ms | speaker handoff / new thought | the safest cut target |
| 150–400 ms | phrase boundary | usable, verify on a frame |
| < 150 ms | mid-phrase | never cut here |

Then **pad**: land 30–80 ms after the last kept word and 30–80 ms before the next,
staying inside 30–200 ms. ASR timestamps drift 50–100 ms; padding absorbs the
drift and leaves the breath intact. Tight for montage (30–50 ms), loose for
documentary (120–200 ms).

## Take selection

- **The last complete take of a repeated line usually wins.** The first is a
  warm-up; the performer finds it on the third.
- Retakes cluster at file boundaries. When one source ends and another begins,
  expect a repeated sentence — and expect the second to be better.
- Keep an unavoidable slip if there is no better take, and note it in the
  segment's `reason`. A clean read of a slightly wrong sentence beats a stumble in
  the right one.
- Assemble by **beat**, never by source-clip order. The viewer cannot tell which
  file a sentence came from, and never should.

## What to cut, precisely

The rules above decide *where the edges can go*. These decide *what must go*, and they
are where auto-editing gives itself away.

- **Dead air is not all dead.** Trim silences longer than ~600 ms *between* thoughts.
  Keep the 200–400 ms after a question, a reveal, or a punchline — that pause is rhythm,
  and removing it makes speech sound sped-up and hostile. Silence is a cut, not a gap.
- **Filler words go; filler rhythm stays.** Cut "um", "uh", "like I said", and abandoned
  false starts. Do **not** keep the cleaner take when it is the weaker one — take quality
  outranks sentence hygiene, always.
- **Rambles: cut to the point, not to the sentence.** If a 30-second aside serves a
  4-second point, keep the 4 seconds. Sentence-by-sentence trimming yields a fast,
  incoherent version of a ramble, which is worse than the ramble.
- **Repeated words across a join.** "so so", or a phrase delivered twice either side of
  a cut, reads as a stutter. Trim the second occurrence, not the first.
- **L-cuts and J-cuts, deliberately.** Let the next shot's audio start 6–12 frames before
  its picture (J-cut), or let the outgoing audio run 6–12 frames past the cut (L-cut).
  A hard audio-and-video cut on every single boundary is the signature of a machine.
- **Cut on motion, not on stillness, when you have the choice.** Mid-gesture cuts hide
  themselves; cuts in a static frame announce the edit — which is sometimes exactly what
  you want, but it must be a decision.

*Informed by the cutting rules in [i-hate-editing](https://github.com/ranahaani/i-hate-editing)
(MIT), rewritten here with numbers so they can be checked. See `ATTRIBUTION.md`.*

## Preserve the peaks

Laughs, punchlines, emphasis, a genuine reaction, applause, a sigh. Extend past
them — the reaction *is* the beat, and trimming it to the word makes a real
moment feel processed.

Non-verbal audio events mark beats. If the transcript shows `(laughs)` or the
waveform shows a burst, that is a place to land, not to cut through.

## Rhythm

Vary shot length on purpose. A useful shape for a 45–60 s piece:

```
2–4 s   hook shot (must change within 1 s)
1–3 s   establish; the claim
2–5 s   evidence, held long enough to read
1–2 s   reaction or punch
3–6 s   the turn — length is the emphasis
1–2 s   payoff
1–4 s   close (face, or a designed end card)
```

Two rules of thumb that survive contact with real work:

- **Nothing on screen for more than 3–4 s without a visual change** in short
  form. The gate enforces > 3 s as a defect, but treat 2.5 s as the real ceiling.
- **A held shot needs one living thing.** Drift, light, a caret, grain, a slow
  push. A dead frame is worse than a fast cut.

## The openings that work

The first 2 seconds decide everything, and most viewers are muted.

- **The claim first, the setup never.** Start at the conclusion, then earn it.
- **A question the piece answers** — planted, not stated as "in this video I will".
- **The strongest visual you have**, if there is one that explains without words.
- **Never** a logo, a title card, an intro animation, or "hey guys".

The hook is not volume. It is a promise specific enough that the viewer wants the
rest. On-screen text must carry it with the sound off.

## Endings

- End on the last word, or on a designed beat of stillness — 0.6–1.4 s, no more.
- Never fade to black by default. It reads as a truncated file.
- Do not let the music resolve before the picture does, and do not let it resolve
  after either. One ending.
- The close should answer the open question from the hook, or complete a loop with
  the opening image. A piece that just stops has failed the last 3 seconds.

## Structural archetypes

Pick one, adapt it, or invent a better one:

```
Launch / demo     HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA
Tutorial          INTRO → SETUP → STEPS → GOTCHA → RECAP
Interview         (QUESTION → ANSWER → FOLLOW-UP) repeat
Travel / event    ARRIVAL → HIGHLIGHTS → QUIET → DEPARTURE
Documentary       THESIS → EVIDENCE → COUNTERPOINT → CONCLUSION
Music / perf      INTRO → VERSE → CHORUS → BRIDGE → OUTRO
```

The archetype is a budget, not a cage: knowing where the turn goes is what lets
you spend 6 seconds on it.

## Multi-take selection brief

When the task is "pick the best take of each beat across many clips", a
sub-agent with a structured brief beats a heroic single pass. The shape matters:

```
You are editing a <type> piece. Pick the best take of each beat and assemble
them chronologically by beat, not by source order.

INPUTS
  takes_packed.md          phrase-level transcripts with time ranges
  context                  two sentences on the product / narrative
  speaker                  name, role, delivery note
  structure                the archetype, or invent one
  avoid                    verbal slips found in the pre-scan
  target                   45 s ± 5

RULES
  edges land on word boundaries; pad 30–200 ms
  prefer silences ≥ 400 ms; never cut inside a word
  keep an unavoidable slip only if no better take exists — note why
  over budget → drop a beat, do not speed up speech

OUTPUT  JSON only:
  [{"source":"C0103","start":2.42,"end":6.85,"beat":"HOOK",
    "quote":"…","reason":"…"}]
```

## Repairing someone else's cut

Given a finished file rather than footage, work in this order — the first two are
the only ones that are actually broken rather than merely wrong:

1. Measure it: `mfe gate --file cut.mp4 --out gate.json`.
2. Re-time captions first if they drift. Cheapest real fix.
3. Fix tone and loudness. Second cheapest.
4. Only then consider re-cutting — and say honestly when a re-cut is cheaper than
   a patch, because usually it is.
