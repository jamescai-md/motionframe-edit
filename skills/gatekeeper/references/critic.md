# The critic brief

A fresh-context review is the cheapest quality gain available, and it only works if
you brief it to attack. A critic asked "how does this look?" will say something
nice. A critic asked "find what is wrong, with evidence" will find it.

## Spawn it in a clean context

Give the critic: the rendered file, the EDL or design spec, the brief, and any
reference the user supplied. **Do not** give it your reasoning, your notes, or the
problems you already suspect — a fresh eye that inherits your blind spots is not a
fresh eye.

## The brief

```
You are reviewing a <type> piece for publication. Assume it is not good enough
yet and your job is to find out why. Do not praise. Do not be polite. Be specific.

INPUTS
  file            <path>
  spec            <edl.json | storyboard.md | design tokens>
  brief           <what it is for, who it is for, where it publishes>
  reference       <what the user asked it to feel like, if anything>

METHOD
  1  Look at the contact sheet and describe every frame in one sentence.
  2  Watch the first 3 seconds and the last 3 seconds at full speed.
  3  Then judge in this order: is it broken or untrue → is there a reason to
     watch → do the beats connect → does the eye land right → is the timing
     right → is the surface right → is the sound right.

OUTPUT  (exactly this shape, no preamble)
  VERDICT     one line — ship / fix first / rebuild
  PROBLEMS    ranked, each as: <severity> <timecode or element> <what is wrong>
              <the evidence you saw or measured> <the fix, in one line>
  FIRST FIVE  the five fixes that would move it furthest, in the order to do them
  DO NOT TOUCH  what is genuinely working, so the author does not break it
```

Require **evidence**: a timecode, a frame number, a measured level, an element
name. "The pacing feels off" is not a finding; "cuts at 0:04, 0:06 and 0:08 are
all 1.9 s with identical framing — the middle third has no rhythm change" is.

## What critics reliably catch that authors do not

- A payoff line cut half a word early.
- Captions that are legible on a laptop and not at phone size.
- The first 0.5 s doing nothing (no change, no claim, no sound).
- Audio that is 6 dB quieter than everything else the user publishes.
- Two elements with equal visual weight where one should lead.
- A section that restates the section before it.
- Text under a platform UI element.
- An ending that stops rather than closes.

## What to do with the output

- Take the top five, in the order given. Do not cherry-pick the easy one.
- If the critic and your own judgement disagree, the one with evidence wins.
- If the critic is wrong, write down why in `notes.md` — a critic that is
  systematically wrong about your project needs different input next time.
- Never present the critic's raw output to the user as your verdict. Synthesise:
  you are the supervisor, not the messenger.
