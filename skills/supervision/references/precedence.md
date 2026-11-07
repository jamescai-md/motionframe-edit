# Precedence — how to decide when two rules disagree

Every skill suite accumulates contradictions because it accumulates authors.
This file exists so the contradictions are decided **once**, in public, instead
of being re-litigated per project or resolved by whichever rule the model read last.

## The ladder

When two instructions conflict, the higher rung wins. Always. Without exception.
If the higher rung cannot be satisfied, the lower rung is not a workaround — the
piece is broken and you say so.

```
1  SAFETY & TRUST     nothing fabricated, nothing harmful, no secret leaked
2  CORRECTNESS        plays, syncs, decodes, lands in the right frame
3  LEGIBILITY         readable at phone size, at a glance, muted
4  INTENT             it does the job the user actually asked for
5  SYSTEM             one type scale, one accent, one motion grammar
6  STYLE              the look, the vibe, the references
7  TREND              what is popular this quarter
```

Consequences that surprise people:

- **A beautiful frame that hides the caption is wrong**, not "bold". (3 > 6)
- **A trend-perfect transition that pops is wrong.** (2 > 7)
- **A brand guideline that makes the phone view unreadable loses.** (3 > 6) Say
  that out loud to the user; do not silently obey either side.
- **"Make it look like this reference" never overrides 1–3.** Borrow the *move*
  (pacing, layout, rhythm), never the words, assets or proof.
- **User instruction sits at 4, not at 1.** A user asking to break correctness is
  asking for a broken file. Do it only after saying what will break, and prefer a
  version that keeps 2 intact.

## The one-effect budget

Most over-designed work is not ugly; it is *plural*. The fix is a budget, not a
taste argument.

| Piece | Effects budget | What counts as one effect |
|---|---|---|
| 15–60 s short | 1 signature + 2 supporting | a caption system is *not* an effect; it is infrastructure |
| Launch / promo film | 1 effect, 1–2 moments | a shader ground, one 3D object, one big scene |
| Landing page | 1 effect, 1–2 moments, ≤4 live WebGL contexts | |
| App UI | 0–3 moments total, ever | a moment = anything the user waits for |
| Poster / deck | 1 idea | the idea may be loud; nothing else may be |

Spend the budget where the payoff is, and make everything else quiet. A piece with
five effects has no effect; a piece with one, in the right place, is memorable.

## Documented conflicts, resolved

These are real disagreements between sources. The resolution is binding.

| # | Conflict | Resolution | Why |
|---|---|---|---|
| 1 | One school bans gradients and glow outright; another builds whole brand systems on them | **Gradients are allowed as a ground, never as a button, a border, or a text effect.** One gradient per piece. On a "place" (cafe, shop, guesthouse) page: none. | Gradients as atmosphere are fine; as affordance they destroy state legibility. |
| 2 | "Big type, bold, maximum contrast" vs "restrained type, generous space" | **Match the medium's reading distance.** Video watched on a phone: big, high contrast, ≤4 words per caption line. Document or desktop reading: restrained. | Both schools are right about their own medium and wrong about the other. |
| 3 | "Animate everything that can move" vs "most things should not move" | **Motion is a signal of state change.** If nothing changed, nothing moves. Entry, exit, and the user's own action animate; static data and keyboard-driven surfaces do not. | Motion that isn't signalling is noise, and noise is what makes work feel AI-made. |
| 4 | "Every scene needs a transition" vs "cut on motion, never fade" | **Default is the hard cut.** Transitions are for a change of world, not a change of shot. Never a fade to black as an ending unless the brand earns it. | Cuts are invisible; transitions announce themselves and cost time. |
| 5 | "Use AI-generated imagery to fill gaps" vs "never mock up reality" | **Generated imagery is allowed for concept, texture, mood and impossibility. Never for anything that claims to be a screenshot, a metric, a person's words, or a product feature.** Declared in `provenance.json`. | The rule is not about pixels; it is about the viewer's trust. |
| 6 | "Follow the brand guide exactly" vs "the guide is unreadable at 1080×1920" | **Brand rules bend on scale and contrast, never on logo lockup or colour identity.** Say which rule bent and why. | Small deviations, explicitly disclosed, are professional. Silent ones are not. |
| 7 | "More real photographs" vs "we have no photographs" | **Real > rendered > diagram > typographic > generated.** Move down the ladder by one rung, never four, and name the rung you are on. | A missing asset degrades gracefully; it does not require a fabricated one. |
| 8 | "Caption every word" vs "captions over a clean face" | **Captions are infrastructure, not decoration.** They exist, they are legible, they never cover the mouth or chin, and they never carry the meaning alone. | Muted autoplay is the default viewing condition. |
| 9 | "Hooks must be loud in the first second" vs "earn the viewer's attention" | **First visual change within 1 s; first spoken claim within 2 s; the hook question answered before the end.** Loudness is not the mechanism — a promise is. | Loud without a promise is worse than quiet with one. |
| 10 | "One accent colour" vs "a full brand palette" | **One accent carries one meaning.** A palette of neutrals plus one accent; semantic colours (error, success) are not accents. | Two accents mean neither means anything. |
| 11 | "Automate everything" vs "the human owns the call" | **Automate measurement, never judgement.** The tool takes the numbers; the model makes the call; the human vetoes. | Measurement is objective and cheap; taste is neither. |
| 12 | "Ship it, iterate later" vs "never present what hasn't passed" | **Internal drafts iterate fast; anything a human sees has passed its gates.** The audit is not a formality, it is the handoff. | The first look a user gets is the one they judge you by. |

## Adjudicating a rule you have not seen

Ask in this order; stop at the first yes.

1. Does breaking it produce a **defect someone will notice**? → it's correctness. Don't.
2. Does breaking it make the piece **unreadable at phone size, muted**? → legibility. Don't.
3. Does breaking it **contradict an explicit instruction from the user**? → do it their
   way, and say what you'd have done differently in one line.
4. Is there a **cheaper version that keeps the idea**? → take it.
5. Is it **decoration**? → cut it. Then see if the piece misses it. Usually it doesn't.

## When the user is wrong

Say it once, plainly, with the consequence and the cheapest alternative:

> "That transition will hide the caption for 0.4 s on the two beats where the
> claim lands. I can put the wipe on the beat *before* instead — same energy, no
> lost words. Want that?"

Then do what they choose. Never argue twice. Never silently "fix" it either —
a silent override is the worst of both.

## Calibration

If you cannot tell which rung applies, the piece is under-specified, not
over-constrained. Go back to the brief and ask one question that resolves the
rung, not five questions about settings.
