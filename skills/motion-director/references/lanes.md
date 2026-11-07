# The three lanes

One motion spec, three ways to execute it. Choosing well is most of the schedule.

## Lane A — ffmpeg native

**Best for:** cuts, crops, punch-ins, drifts, speed ramps, grades, captions,
text cards, logo overlays, simple overlays, anything under ~30 s of motion.

```bash
# punch-in on an emphasis word, easing baked into keyframes is not available —
# so use a short, small move; a 106% push over 8 frames reads as intentional
ffmpeg -i in.mp4 -vf "scale=1088:1936,crop=1080:1920:x='(iw-ow)/2':y='(ih-oh)/2'" out.mp4

# slow drift over a held shot (the "no dead frame" fix)
ffmpeg -i in.mp4 -vf "zoompan=z='min(1.00+0.0008*on,1.10)':d=1:s=1080x1920:fps=30" out.mp4

# overlay a rendered animation, frame 0 at t=2.0  ← the classic silent failure
ffmpeg -i base.mp4 -i anim.mov -filter_complex \
 "[1:v]trim=duration=3,setpts=PTS-STARTPTS+2.0/TB,format=rgba[ov];[0:v][ov]overlay=enable='between(t,2.0,5.0)'" out.mp4
```

Grudging but correct. Easing is limited to what filters express; `zoompan`,
`xfade`, `curves` and `sendcmd` cover more than people expect. If you need real
easing curves, stop and use lane B.

## Lane B — HTML + GSAP + headless Chrome

**Best for:** type-led motion, layouts, UI demos, charts, kinetic captions,
anything that would be a webpage if it stood still.

The loop is: a deterministic HTML page where **time is an input**, a headless
browser that can render frame N on demand, and ffmpeg to assemble.

```html
<!-- film.html — every frame is a pure function of t -->
<script src="gsap.min.js"></script>
<script>
const M = { beat: 2.0, title: 3.4, out: 6.0 };      // the motion spec, one place
function seek(t) {
  const tl = gsap.timeline({ paused: true });
  tl.from(".num",   { scale: 3.5, opacity: 0, duration: 0.4, ease: "expo.out" }, 0)
    .from(".claim", { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.35)
    .to(".card",    { scale: 0.94, duration: 0.3, ease: "power2.in" }, M.out - 0.3);
  tl.seek(t);                                       // exact, seekable, repeatable
  return tl;
}
window.__render = (t) => { seek(t); return true; };
</script>
```

Capture frames with a headless browser you already have, then encode:

```bash
# determinism first: the same t must produce the same pixels, twice in a row
node -e "/* puppeteer/playwright: page.evaluate(t => window.__render(t), 1.2) → screenshot */"
ffmpeg -framerate 30 -i frames/%05d.png -c:v libx264 -crf 16 -pix_fmt yuv420p out.mp4
```

Rules that make lane B reliable:

- **Never** use CSS transitions or `requestAnimationFrame` for scene motion. They
  are wall-clock; you need virtual time.
- **Disable font loading races** — embed fonts as base64, or wait for
  `document.fonts.ready` before the first frame.
- **Fixed viewport, fixed device scale factor**, `--force-device-scale-factor=1`.
  A 2× capture that gets resampled later looks soft at exactly the moment it
  matters.
- **Deterministic textures**: no `Math.random()` without a seed, no video elements,
  no live data.
- Two frames of overlap on every seek is cheap insurance against a rounding error.

## Lane C — React / Remotion

**Best for:** parametric systems, data-driven scenes, many variants from one
source, a component library of moves.

```tsx
// one composition, N variants — this is what lane C is actually for
export const Scene: React.FC<{ variant: Variant }> = ({ variant }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = interpolate(frame, [0, 0.5 * fps], [3.5, 1],
                            { easing: Easing.out(Easing.expo), extrapolateRight: "clamp" });
  return <div style={{ transform: `scale(${enter})` }}>{variant.copy}</div>;
};
```

Remotion is MIT-licensed and free for individuals and small teams; check its
current licence terms before commercial use, and note that other tools in this
space are not free — prefer lane B when in doubt, it has no licence question at
all.

Rules: `useCurrentFrame()` only, no `useState` for visual values, no timers, no
network. Every parameter that changes between variants belongs in props, not in
the component.

## Choosing, in one table

| Need | Lane |
|---|---|
| cut, crop, caption, grade | A |
| 2–10 s of type motion | B |
| a UI demo where real DOM helps | B |
| 20 variants of one animated card | C |
| data-driven scene at scale | C |
| no Node available | A |
| a client who needs the source project | B |

## The frame handoff between lanes

Lane B and C render to video, then lane A composites them. Two rules:

1. **Match the delivery fps and frame size exactly** at render time. Resampling a
   motion graphic is how it gets soft edges at the worst moment.
2. **Render motion with an alpha channel** if it composites over footage —
   `-c:v qtrle` (lossless RGBA) or ProRes 4444, never a codec that drops alpha.
    For long graphics, render `png` sequences instead; disk is cheaper than a
    re-render.
