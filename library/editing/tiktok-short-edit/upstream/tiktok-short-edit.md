---
name: "tiktok-short-edit"
description: Edit a raw talking-head video into a finished, captivating 9:16 TikTok/Reel/Short entirely in code, with synthesized music and SFX. Use when the user asks to edit a video for TikTok, Reels or Shorts.
---

# TikTok Short Edit

Turn the user's raw talking-head recording into a finished, ready-to-post 9:16 short for TikTok (also usable as a Reel / YouTube Short). Do it entirely in code: ffmpeg, Python, Node and HyperFrames (`npx --yes hyperframes`). No video editor app.

You may install what you need locally inside the project (npm packages in the project folder, pip into a local venv) without asking. Never install system-wide software.

## Step 0: Gather inputs

Collect these before doing any work. Anything the user already gave in their message (or in the skill arguments) counts as answered; don't ask it again. So does anything in the `## My style` section at the end of this file, if there is one: follow its style profile for captions, pacing, graphics and sound.

### 0a. The video file
- Look for a video file the user named or attached, then in the current project (e.g. Glob for *.mp4, *.mov, *.m4v, *.webm).
- If there is exactly one, use it and say which file in one line.
- If there are several, ask which one.
- If there is none, ask the user for the path to the video, and stop until they give it.

Assume the audio is already cleaned and the takes are already spliced unless the user says otherwise.

### 0b. Edit preferences
Ask everything still missing in ONE AskUserQuestion call (max 4 questions). Use these, skipping any already answered:

1. **Review mode** (header: "Mode")
   - "Approve plan first (Recommended)": transcribe, draft the edit plan, wait for approval before rendering
   - "Fully autonomous": make every call yourself, log it in the report
2. **Visual style** (header: "Style")
   - "Bold & high-energy": big captions, fast zooms, punchy graphics
   - "Clean & minimal": restrained motion, elegant type
   - "Playful": bouncy animations, emoji-style accents, more SFX
3. **Music vibe** (header: "Music")
   - "Upbeat electronic"
   - "Lo-fi / chill"
   - "Cinematic / tension"
   - "No music"
4. **Branding** (header: "Brand")
   - "Match the video": pick an accent color and bold sans font that suit the footage, no handle
   - "Use my brand": user types colors (hex), font and @handle in the Other field or in a follow-up
   - "No branding"

If the user picks "Use my brand" without giving details, ask once in plain text for colors, font and handle. If AskUserQuestion is unavailable or the user isn't there to answer, use the Recommended/first option for each, state the choices at the top of your work, and carry on.

The topic and main point are NOT asked up front: infer them from the transcript and confirm them in the edit plan.

## Output spec

- `final.mp4`: 1080x1920, 30fps, H.264 + AAC, loudness about -14 LUFS integrated, true peak no higher than -1 dBTP.
- No fixed length. Keep everything that carries the message; trim dead air, filler and repeated points. Don't otherwise re-cut the content or re-process the voice beyond loudness normalization.
- `report.md`: every judgement call made, plus anything that couldn't be done and what was done instead.
- Save both next to the input video (or in an `output/` folder in the project) and tell the user where they are.

## Audio (all synthesized in code)

No audio files, no downloads.
- **Music:** a short original loop generated in code (Python, e.g. numpy/scipy) in the chosen vibe, matching the video's energy. Sit it well under the voice and duck it further whenever the speaker talks. Skip if the user chose "No music".
- **SFX:** whooshes, pops, clicks, risers and hits, all synthesized. Use them to accent visual events, not on every one. Scale density to the chosen style (more for Playful, fewer for Clean & minimal).

## Pacing: something changes every 2–3 seconds

Rotate between these so it never feels repetitive:
- Punch-in / punch-out zooms on emphasis words
- Word-by-word animated captions with key words highlighted in the accent color
- Motion graphics that explain the point: icons, diagrams, numbers counting up, lists building on screen, simple UI mockups (if a real product UI isn't capturable, rebuild it from public screenshots/docs and note it in the report)
- Text callouts for key phrases
- Subtle transitions between sections

After rendering, check the timeline: no stretch longer than 3 seconds without a visual change.

## Hook

- The first 1–2 seconds must stop the scroll: a bold on-screen hook line drawn from what the speaker says, with movement and a sound accent from frame one.
- The hook text also serves as the cover title.

## Layout

- Keep captions and graphics inside TikTok's safe zone: nothing important in roughly the top 150px, the bottom 450px, or the right 150px (the app UI covers those).
- Graphics must never cover the speaker's face for more than a moment.

## Process

1. **Transcribe** with word-level timestamps (e.g. local Whisper / faster-whisper in a venv).
2. **Plan.** Write `edit_plan.md`: inferred topic and main point, the hook line, then a timestamped list of every zoom, caption style, graphic, SFX and music change, and what each graphic shows.
3. **Checkpoint** (only in "Approve plan first" mode): share the plan, ask any questions it raised (one AskUserQuestion call), and wait for approval before rendering. In "Fully autonomous" mode, skip this and log the calls in the report.
4. **Build and render.**
5. **Self-review.** Extract frames every ~2 seconds and inspect them for safe-zone violations, text overflow, caption/speech timing drift, faces covered, and anything that looks off. Measure loudness with ffmpeg's loudnorm/ebur128. Fix and re-render.
6. **Deliver** `final.mp4` and `report.md`, with one line on what came out and one natural next step if there is one.

## Failure handling

If something fails, try another tool or method rather than stopping. A missing tool is not a reason to stop: install it locally or use an alternative. Only stop early if the input video is missing or unreadable.
