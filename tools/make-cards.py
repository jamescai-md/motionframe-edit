#!/usr/bin/env python3
"""
make-cards.py — generate the repository's brand assets.

Two images, one design system: a README banner and a 1280x640 social preview
(GitHub's Open Graph card). Generated, not hand-drawn, so they can be regenerated
when the copy changes rather than drifting out of date.

    pip install pillow          # the only dev dependency in this repo
    python3 tools/make-cards.py

Writes:
    .github/banner.png          1280x340   top of the README
    .github/social-preview.png  1280x640   Settings -> Social preview (upload by hand)

Design rules it follows (the same ones the skills enforce):
  * one accent, one meaning — the accent marks "measured / active", nothing else
  * type: one family, four sizes, no fourth weight
  * the timeline strip is the logo: segments, cut marks, a playhead
  * nothing decorative that is not carrying information
"""

from __future__ import annotations

import pathlib
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("needs Pillow:  pip install pillow")

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / ".github"

# --- tokens -----------------------------------------------------------------
BG = (11, 11, 16)
PANEL = (20, 20, 28)
INK = (242, 242, 239)
MUTED = (138, 138, 150)
FAINT = (38, 38, 48)
ACCENT = (255, 92, 56)

FONT_DIR = pathlib.Path("/usr/share/fonts/truetype/dejavu")
SANS_B = FONT_DIR / "DejaVuSans-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
MONO = FONT_DIR / "DejaVuSansMono.ttf"

NAME = "supervision"
KICKER = "ONE SKILL  ·  EIGHTEEN SOURCES  ·  MIT  ·  v1.0.0"
TAGLINE = "Eighteen editing, motion and design skills — merged into one."
SUB = "Every rule given a home. Every contradiction ruled on. Eight gates that measure the render."
ACCENT_WORD = "measure"


def font(path: pathlib.Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        sys.exit(f"missing font: {path} — install fonts-dejavu-core")
    return ImageFont.truetype(str(path), size)


def fit(draw: ImageDraw.ImageDraw, text: str, path: pathlib.Path, start: int, max_w: float) -> ImageFont.FreeTypeFont:
    """Largest size at or below `start` that keeps `text` inside `max_w`."""
    size = start
    while size > 12:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 12)


def runs(draw: ImageDraw.ImageDraw, x: int, y: int, parts: list[tuple[str, ImageFont.FreeTypeFont, tuple[int, int, int]]]) -> int:
    """Draw a sequence of styled runs on one baseline; return the end x."""
    for text, f, colour in parts:
        draw.text((x, y), text, font=f, fill=colour)
        x += draw.textlength(text, font=f)
    return int(x)


def frame_ticks(draw: ImageDraw.ImageDraw, w: int, h: int, step: int = 64) -> None:
    """Faint vertical frame marks — the only texture, and it is a ruler."""
    for x in range(step, w, step):
        draw.line([(x, 0), (x, h)], fill=FAINT, width=1)


def timeline(draw: ImageDraw.ImageDraw, x0: int, y: int, w: int, h: int) -> None:
    """The mark: segments, cut marks, a playhead. Editing, in one glyph."""
    segs = [0.16, 0.09, 0.22, 0.07, 0.13, 0.05, 0.18]
    total = sum(segs)
    gap = 3
    x = x0
    usable = w - gap * (len(segs) - 1)
    for i, s in enumerate(segs):
        sw = int(usable * s / total)
        shade = PANEL if i % 2 == 0 else (28, 28, 38)
        draw.rectangle([x, y, x + sw, y + h], fill=shade)
        # a cut mark on the leading edge of every segment after the first
        if i:
            draw.line([(x - 1, y - 6), (x - 1, y + h + 6)], fill=MUTED, width=1)
        x += sw + gap
    # playhead, accent: the one thing that is "current"
    px = x0 + int((w) * 0.38)
    draw.line([(px, y - 10), (px, y + h + 10)], fill=ACCENT, width=2)
    draw.polygon([(px - 5, y - 16), (px + 5, y - 16), (px, y - 9)], fill=ACCENT)


def banner() -> pathlib.Path:
    w, h = 1280, 340
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    frame_ticks(d, w, h)

    f_kick, f_name = font(MONO, 15), font(SANS_B, 68)
    f_tag = fit(d, TAGLINE, SANS, 27, w - 2 * 64)
    f_sub = fit(d, SUB, SANS, 24, w - 2 * 64)
    x = 64

    d.text((x, 40), KICKER, font=f_kick, fill=MUTED)
    runs(d, x - 3, 66, [(NAME, f_name, INK)])

    # tagline, with one word carrying the accent — the caption system, dogfooded
    y = 158
    runs(d, x, y, [(TAGLINE, f_tag, MUTED)])
    pre, post = SUB.split(ACCENT_WORD)
    runs(d, x, y + 38, [(pre, f_sub, MUTED), (ACCENT_WORD, f_sub, ACCENT), (post, f_sub, MUTED)])

    timeline(d, x, 268, w - 2 * x, 34)

    # accent rule on the left edge: the frame's edge, i.e. where cuts happen
    d.rectangle([0, 0, 5, h], fill=ACCENT)

    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "banner.png"
    img.save(p, optimize=True)
    return p


def gate_panel(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    """A gate report, rendered. This is the product, so it belongs on the card."""
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=FAINT)
    d.rectangle([x, y, x + w, y + 38], fill=(16, 16, 23))
    f_head, f_row = font(MONO, 14), font(MONO, 17)
    d.text((x + 16, y + 12), "gate-report.json", font=f_head, fill=MUTED)
    for i, (gid, label, value) in enumerate([
        ("G0", "render exists", "52.10s"),
        ("G1", "delivery shape", "1080x1920"),
        ("G2", "loudness", "-14.2 LUFS"),
        ("G3", "picture alive", "0 freezes"),
        ("G5", "cuts don't pop", "10 / 10"),
        ("G7", "honest proof", "6 declared"),
    ]):
        ry = y + 56 + i * 26
        d.text((x + 16, ry), gid, font=f_row, fill=MUTED)
        d.text((x + 52, ry), "PASS", font=f_row, fill=INK)
        d.text((x + 108, ry), label, font=f_row, fill=MUTED)
        tw = d.textlength(value, font=f_row)
        d.text((x + w - 16 - tw, ry), value, font=f_row, fill=INK)


def social() -> pathlib.Path:
    w, h = 1280, 640
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    frame_ticks(d, w, h)

    f_kick, f_name = font(MONO, 16), font(SANS_B, 78)
    f_tag = fit(d, TAGLINE, SANS, 29, 1280 - 2 * 76)
    f_sub = fit(d, SUB, SANS, 24, 1280 - 2 * 76)
    f_chip = font(MONO, 16)
    x = 76

    d.text((x, 68), KICKER, font=f_kick, fill=MUTED)
    runs(d, x - 3, 96, [(NAME, f_name, INK)])
    runs(d, x, 206, [(TAGLINE, f_tag, MUTED)])
    pre, post = SUB.split(ACCENT_WORD)
    runs(d, x, 248, [(pre, f_sub, MUTED), (ACCENT_WORD, f_sub, ACCENT), (post, f_sub, MUTED)])

    # chips, one per row, left column
    for i, c in enumerate(["FREE · LOCAL · NO API KEYS",
                           "7 SKILLS · 12 LAWS · 8 GATES",
                           "CLAUDE · CODEX · GEMINI · OPENCODE"]):
        cy = 316 + i * 54
        tw = d.textlength(c, font=f_chip)
        d.rectangle([x, cy, x + tw + 32, cy + 42], fill=PANEL, outline=FAINT)
        d.text((x + 16, cy + 13), c, font=f_chip, fill=INK)

    gate_panel(d, 660, 316, 544, 218)
    timeline(d, x, 556, w - 2 * x, 40)
    d.rectangle([0, 0, 6, h], fill=ACCENT)

    p = OUT / "social-preview.png"
    img.save(p, optimize=True)
    return p


if __name__ == "__main__":
    for p in (banner(), social()):
        img = Image.open(p)
        print(f"  wrote {p.relative_to(ROOT)}  {img.width}x{img.height}  {p.stat().st_size // 1024} KB")
