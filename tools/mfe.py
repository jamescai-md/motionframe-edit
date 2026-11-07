#!/usr/bin/env python3
"""
mfe — the motionframe-edit engine.

One executable that does the measurable half of the work so the agent can do the
judgement half: probe footage, drive an EDL, cut and compose with ffmpeg, build
captions, and *audit the result* against gates that fail loudly.

Design rules this file obeys:
  1. No network calls, no API keys, no accounts, no telemetry. Ever.
  2. Every dependency is free and open source (ffmpeg, Python stdlib, libass).
  3. A missing optional tool degrades to a clear message, never a silent wrong result.
  4. Nothing here decides taste. It measures, so the human and the model can decide.

Usage: mfe.py <command> [options]      (see `mfe.py doctor` and `mfe.py --help`)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

MFE_VERSION = "1.0.0"
SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Output profiles. These are delivery contracts, not preferences.
# safe zones are fractions of frame height/width where platform UI covers us.
# ---------------------------------------------------------------------------

PROFILES: dict[str, dict[str, Any]] = {
    "vertical-9x16": {
        "fit": "fill",
        "width": 1080, "height": 1920, "fps": 30,
        "loudness_lufs": -14.0, "true_peak_db": -1.0,
        # TikTok/Reels/Shorts UI: ~top 12%, ~bottom 23%, ~right 13%
        "safe": {"top": 0.12, "bottom": 0.23, "left": 0.04, "right": 0.13},
        "max_dead_stretch_s": 3.0,
    },
    "square-1x1": {
        "fit": "fill",
        "width": 1080, "height": 1080, "fps": 30,
        "loudness_lufs": -14.0, "true_peak_db": -1.0,
        "safe": {"top": 0.08, "bottom": 0.10, "left": 0.05, "right": 0.05},
        "max_dead_stretch_s": 4.0,
    },
    "landscape-16x9": {
        "fit": "pad",
        "width": 1920, "height": 1080, "fps": 30,
        "loudness_lufs": -16.0, "true_peak_db": -1.0,
        "safe": {"top": 0.05, "bottom": 0.08, "left": 0.05, "right": 0.05},
        "max_dead_stretch_s": 6.0,
    },
    "master-16x9": {
        "fit": "pad",
        "width": 3840, "height": 2160, "fps": 24,
        "loudness_lufs": -16.0, "true_peak_db": -1.0,
        "safe": {"top": 0.03, "bottom": 0.03, "left": 0.03, "right": 0.03},
        "max_dead_stretch_s": 8.0,
    },
}
DEFAULT_PROFILE = "vertical-9x16"


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------

_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def c(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOR else text


def ok(tag: str, msg: str) -> None:
    print(f"  {c('PASS', '32')}  {tag:<12} {msg}")


def bad(tag: str, msg: str) -> None:
    print(f"  {c('FAIL', '31')}  {tag:<12} {msg}")


def warn(tag: str, msg: str) -> None:
    print(f"  {c('WARN', '33')}  {tag:<12} {msg}")


def info(tag: str, msg: str) -> None:
    print(f"  {c('····', '90')}  {tag:<12} {msg}")


def die(msg: str, code: int = 2) -> "NoReturn":  # noqa: F821
    print(f"\n{c('error:', '31;1')} {msg}", file=sys.stderr)
    raise SystemExit(code)


# ---------------------------------------------------------------------------
# ffmpeg discovery. We accept a system ffmpeg, else the static build shipped by
# imageio-ffmpeg (pip installable, free), else nothing.
# ---------------------------------------------------------------------------

@dataclass
class Toolchain:
    ffmpeg: str | None = None
    ffprobe: str | None = None
    ffmpeg_version: str = ""
    filters: set[str] = field(default_factory=set)
    encoders: set[str] = field(default_factory=set)

    @property
    def has_ffmpeg(self) -> bool:
        return bool(self.ffmpeg)

    @property
    def can(self) -> set[str]:
        return self.filters & {"subtitles", "ass", "drawtext", "freezedetect",
                               "blackdetect", "ebur128", "loudnorm", "signalstats",
                               "overlay", "xfade", "zoompan"}


def find_toolchain() -> Toolchain:
    tc = Toolchain()
    tc.ffmpeg = shutil.which("ffmpeg")
    tc.ffprobe = shutil.which("ffprobe")
    if not tc.ffmpeg:
        try:  # free static build, pip install imageio-ffmpeg
            import imageio_ffmpeg  # type: ignore
            tc.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            tc.ffmpeg = None
    if not tc.ffmpeg:
        return tc
    try:
        out = subprocess.run([tc.ffmpeg, "-hide_banner", "-version"],
                             capture_output=True, text=True, timeout=20).stdout
        m = re.search(r"ffmpeg version (\S+)", out)
        tc.ffmpeg_version = m.group(1) if m else "unknown"
        fl = subprocess.run([tc.ffmpeg, "-hide_banner", "-filters"],
                            capture_output=True, text=True, timeout=20).stdout
        tc.filters = set(re.findall(r"^\s*[A-Z.|]+\s+(\w+)\s+", fl, re.M))
        en = subprocess.run([tc.ffmpeg, "-hide_banner", "-encoders"],
                            capture_output=True, text=True, timeout=20).stdout
        tc.encoders = set(re.findall(r"^\s*[VAS][A-Z.]{5}\s+(\w+)\s+", en, re.M))
    except Exception:
        pass
    return tc


TC = find_toolchain()


def require_ffmpeg() -> str:
    if not TC.ffmpeg:
        die("ffmpeg not found.\n"
            "  Free install, pick one:\n"
            "    pip install imageio-ffmpeg          (bundles a static ffmpeg)\n"
            "    brew install ffmpeg                 (macOS)\n"
            "    scoop install ffmpeg / winget install ffmpeg   (Windows)\n"
            "    sudo apt install ffmpeg             (Debian/Ubuntu)")
    return TC.ffmpeg


def run(cmd: list[str], *, capture: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, capture_output=capture, text=True)
    if check and p.returncode != 0:
        tail = (p.stderr or "")[-1800:]
        die(f"command failed ({p.returncode}):\n  {' '.join(shorten(cmd))}\n{tail}")
    return p


def shorten(cmd: Iterable[str], n: int = 160) -> list[str]:
    out = []
    for part in cmd:
        out.append(part if len(part) <= n else part[:n] + "…")
    return out


# ---------------------------------------------------------------------------
# Probing. Uses ffprobe when present; otherwise parses `ffmpeg -i`, and reads
# *display* dimensions (rotation side data), because phone footage lies about
# its shape.
# ---------------------------------------------------------------------------

def probe(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        die(f"no such media: {path}")
    if TC.ffprobe:
        p = run([TC.ffprobe, "-v", "error", "-show_streams", "-show_format",
                 "-of", "json", str(path)], check=False)
        if p.returncode == 0:
            data = json.loads(p.stdout)
            return _normalize_probe(data, path)
    # Fallback: parse `ffmpeg -i` stderr.
    p = run([require_ffmpeg(), "-hide_banner", "-i", str(path)], check=False)
    return _normalize_probe(_parse_ffmpeg_i(p.stderr or ""), path)


def _parse_ffmpeg_i(text: str) -> dict[str, Any]:
    dur = 0.0
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", text)
    if m:
        dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    streams: list[dict[str, Any]] = []
    for line in text.splitlines():
        if "Video:" in line:
            s: dict[str, Any] = {"codec_type": "video"}
            vm = re.search(r"Video:\s*(\w+)", line)
            s["codec_name"] = vm.group(1) if vm else "?"
            dm = re.search(r"(\d{2,5})x(\d{2,5})", line)
            if dm:
                s["width"], s["height"] = int(dm.group(1)), int(dm.group(2))
            fm = re.search(r"([\d.]+) fps", line)
            if fm:
                s["r_frame_rate"] = f"{fm.group(1)}/1"
            if "rotation" in line:
                rm = re.search(r"rotation of ([-0-9.]+) degrees", line)
                if rm:
                    s["tags"] = {"rotate": rm.group(1)}
            streams.append(s)
        elif "Audio:" in line:
            am = re.search(r"Audio:\s*(\w+)", line)
            streams.append({"codec_type": "audio", "codec_name": am.group(1) if am else "?"})
    return {"streams": streams, "format": {"duration": str(dur)}}


def _normalize_probe(data: dict[str, Any], path: Path) -> dict[str, Any]:
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    out: dict[str, Any] = {
        "file": str(path),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "duration_s": _f(data.get("format", {}).get("duration"), 0.0),
        "has_video": bool(v),
        "has_audio": bool(a),
    }
    if v:
        w, h = int(v.get("width") or 0), int(v.get("height") or 0)
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = int(float(sd["rotation"]))
        tags = v.get("tags") or {}
        if not rot and "rotate" in tags:
            rot = int(float(tags["rotate"]))
        disp_w, disp_h = (h, w) if abs(rot) % 180 == 90 else (w, h)
        out.update({
            "width": w, "height": h,
            "display_width": disp_w, "display_height": disp_h,
            "rotation": rot,
            "codec": v.get("codec_name"),
            "fps": _rate(v.get("r_frame_rate") or v.get("avg_frame_rate")),
            "pix_fmt": v.get("pix_fmt"),
            "sar": v.get("sample_aspect_ratio"),
        })
    if a:
        out.update({"audio_codec": a.get("codec_name"),
                    "audio_channels": a.get("channels"),
                    "audio_rate": int(a.get("sample_rate") or 0)})
    return out


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _rate(v: Any) -> float:
    if not v or v == "0/0":
        return 0.0
    if isinstance(v, str) and "/" in v:
        n, d = v.split("/")[:2]
        return round(_f(n) / (_f(d) or 1), 3)
    return round(_f(v), 3)


# ---------------------------------------------------------------------------
# EDL: the single source of truth for a cut.
# ---------------------------------------------------------------------------

def load_edl(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        die(f"EDL not found: {p}")
    try:
        edl = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"EDL is not valid JSON: {e}")
    return edl


def validate_edl(edl: dict[str, Any], base: Path | None = None) -> list[str]:
    """Return a list of hard errors. Empty list means the EDL is renderable."""
    errs: list[str] = []
    if not isinstance(edl, dict):
        return ["EDL root must be an object"]
    if edl.get("version") != SCHEMA_VERSION:
        errs.append(f"version must be {SCHEMA_VERSION} (got {edl.get('version')!r})")
    prof = edl.get("profile")
    if isinstance(prof, str):
        if prof not in PROFILES:
            errs.append(f"unknown profile {prof!r}; known: {', '.join(PROFILES)}")
    elif isinstance(prof, dict):
        for k in ("width", "height", "fps"):
            if k not in prof:
                errs.append(f"profile object missing {k}")
    else:
        errs.append("profile must be a name or an object")

    sources = edl.get("sources")
    if not isinstance(sources, dict) or not sources:
        errs.append("sources must be a non-empty object of {id: path}")
        sources = {}
    for sid, spath in sources.items():
        if base and not (base / spath).exists() and not Path(spath).exists():
            errs.append(f"source {sid!r} not found on disk: {spath}")

    segs = edl.get("segments")
    if not isinstance(segs, list) or not segs:
        errs.append("segments must be a non-empty array")
        return errs

    seen: set[str] = set()
    for i, s in enumerate(segs):
        tag = f"segments[{i}]"
        if not isinstance(s, dict):
            errs.append(f"{tag} must be an object")
            continue
        sid = s.get("id")
        if not sid:
            errs.append(f"{tag} missing id")
        elif sid in seen:
            errs.append(f"{tag} duplicate id {sid!r}")
        else:
            seen.add(str(sid))
        if s.get("source") not in sources:
            errs.append(f"{tag} source {s.get('source')!r} not in sources")
        start, end = _f(s.get("start"), -1), _f(s.get("end"), -1)
        if start < 0:
            errs.append(f"{tag} start must be >= 0")
        if end <= start:
            errs.append(f"{tag} end ({end}) must be > start ({start})")
        sp = _f(s.get("speed", 1.0), 1.0)
        if sp <= 0:
            errs.append(f"{tag} speed must be > 0")
        fi, fo = _f(s.get("fade_in", 0.03), 0.03), _f(s.get("fade_out", 0.03), 0.03)
        if fi > 0.25 or fo > 0.25:
            errs.append(f"{tag} fades above 0.25s will be audible as gaps; keep 0.02-0.05")
        if fi < 0 or fo < 0:
            errs.append(f"{tag} fades must be >= 0")
        # the classic silent failure: a cut edge inside a word
        for w in s.get("word_edges", []) or []:
            if isinstance(w, dict) and "start" in w and _f(w["start"]) < start - 0.001:
                errs.append(f"{tag} cut starts inside word {w.get('w')!r} — snap the edge")

    for i, o in enumerate(edl.get("overlays", []) or []):
        tag = f"overlays[{i}]"
        if not o.get("src"):
            errs.append(f"{tag} missing src")
        elif base and not (base / o["src"]).exists() and not Path(o["src"]).exists():
            errs.append(f"{tag} file not found: {o['src']}")
        if _f(o.get("dur"), 0) <= 0:
            errs.append(f"{tag} dur must be > 0")
    return errs


def resolve_profile(edl: dict[str, Any]) -> dict[str, Any]:
    prof = edl.get("profile", DEFAULT_PROFILE)
    if isinstance(prof, str):
        base = dict(PROFILES.get(prof, PROFILES[DEFAULT_PROFILE]))
        base["name"] = prof
    else:
        base = dict(PROFILES[DEFAULT_PROFILE])
        base.update(prof)
        base.setdefault("name", "custom")
    return base


def segment_duration(s: dict[str, Any]) -> float:
    """Duration on the OUTPUT timeline, after speed."""
    raw = max(0.0, _f(s.get("end")) - _f(s.get("start")))
    return raw / max(0.001, _f(s.get("speed", 1.0), 1.0))


def edl_timeline(edl: dict[str, Any]) -> list[dict[str, Any]]:
    """Segments annotated with their offset on the output timeline."""
    t = 0.0
    out = []
    for s in edl.get("segments", []):
        d = segment_duration(s)
        out.append({**s, "offset": round(t, 6), "duration": round(d, 6)})
        t += d
    return out


def edl_duration(edl: dict[str, Any]) -> float:
    return round(sum(segment_duration(s) for s in edl.get("segments", [])), 6)


def source_time(edl: dict[str, Any], output_time: float) -> tuple[str, float]:
    """Map an output-timeline instant back to (source id, source seconds).

    This is the one mapping every caption, overlay and note must go through.
    """
    for s in edl_timeline(edl):
        if s["offset"] <= output_time <= s["offset"] + s["duration"]:
            return s["source"], _f(s["start"]) + (output_time - s["offset"]) * _f(s.get("speed", 1.0), 1.0)
    last = edl_timeline(edl)[-1]
    return last["source"], _f(last["end"])


# ---------------------------------------------------------------------------
# Rendering: extract per segment, concat losslessly, then one composite pass.
# ---------------------------------------------------------------------------

def _vscale(prof: dict[str, Any], seg: dict[str, Any] | None = None) -> str:
    """Normalise every source to the delivery frame.

    fit="fill" crops to cover the frame and biases the crop toward the subject
    (framing [fx, fy], 0.5 = centre). Letterboxing a landscape take into a
    vertical frame is technically correct and editorially wrong: it wastes 60%
    of the screen and reads as a repost.
    """
    w, h, fps = int(prof["width"]), int(prof["height"]), prof.get("fps", 30)
    seg = seg or {}
    fit = seg.get("fit") or prof.get("fit", "pad")
    if fit == "fill":
        fx, fy = (seg.get("framing") or [0.5, 0.5])[:2]
        return (f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,"
                f"crop={w}:{h}:(iw-ow)*{_f(fx, 0.5):.4f}:(ih-oh)*{_f(fy, 0.5):.4f},"
                f"setsar=1,fps={fps}")
    return (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={fps}")


def _afade(dur: float, fi: float, fo: float) -> str:
    """30ms-style micro-fades at both edges. This is preventive, not stylistic."""
    parts = []
    if fi > 0:
        parts.append(f"afade=t=in:st=0:d={fi:.3f}")
    if fo > 0:
        parts.append(f"afade=t=out:st={max(0.0, dur - fo):.3f}:d={fo:.3f}")
    return ",".join(parts)


def _atempo_chain(speed: float) -> list[str]:
    """atempo accepts 0.5-2.0 per instance; chain for anything outside."""
    if abs(speed - 1.0) < 1e-6:
        return []
    parts, s = [], speed
    while s > 2.0:
        parts.append("atempo=2.0")
        s /= 2.0
    while s < 0.5:
        parts.append("atempo=0.5")
        s /= 0.5
    parts.append(f"atempo={s:.6f}")
    return parts


def cut_segments(edl: dict[str, Any], base: Path, workdir: Path,
                 preview: bool = False, crf: int = 18) -> list[Path]:
    ff = require_ffmpeg()
    prof = resolve_profile(edl)
    workdir.mkdir(parents=True, exist_ok=True)
    crf = 23 if preview else crf
    segfiles: list[Path] = []
    for i, s in enumerate(edl_timeline(edl)):
        sid = s["source"]
        src = str(base / edl["sources"][sid]) if (base / edl["sources"][sid]).exists() else edl["sources"][sid]
        start, dur, speed = _f(s["start"]), _f(s["end"]) - _f(s["start"]), _f(s.get("speed", 1.0), 1.0)
        out_dur = dur / speed
        vf = [_vscale(prof, s)]
        if abs(speed - 1.0) > 1e-6:
            vf.append(f"setpts=PTS/{speed:.6f}")
        af = _atempo_chain(speed)
        fades = _afade(out_dur, _f(s.get("fade_in", 0.03), 0.03), _f(s.get("fade_out", 0.03), 0.03))
        if fades:
            af.append(fades)
        out = workdir / f"seg_{i:03d}.mp4"
        cmd = [ff, "-hide_banner", "-loglevel", "error", "-y",
               "-ss", f"{start:.4f}", "-t", f"{dur + 0.15:.4f}", "-i", src]
        # optional music/audio replacement is a later pass; here audio comes from source
        cmd += ["-vf", ",".join(vf)]
        if af:
            cmd += ["-af", ",".join(af)]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
                "-t", f"{out_dur:.4f}", str(out)]
        run(cmd)
        segfiles.append(out)
        info("cut", f"{sid} {start:.2f}→{start + dur:.2f}s → seg {i:02d} ({out_dur:.2f}s)")
    return segfiles


def concat_lossless(segfiles: list[Path], out: Path) -> Path:
    ff = require_ffmpeg()
    listfile = out.parent / "concat.txt"
    listfile.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in segfiles), encoding="utf-8")
    run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(listfile), "-c", "copy", "-movflags", "+faststart", str(out)])
    return out


def composite(edl: dict[str, Any], base: Path, inp: Path, out: Path,
              captions: Path | None = None, prof: dict[str, Any] | None = None,
              loudness: bool = True, preview: bool = False, crf: int = 18) -> Path:
    """One encode pass: overlays (PTS-shifted) → captions LAST → loudness."""
    ff = require_ffmpeg()
    prof = prof or resolve_profile(edl)
    overlays = edl.get("overlays") or []
    args: list[str] = [ff, "-hide_banner", "-loglevel", "error", "-y", "-i", str(inp)]
    filters: list[str] = []
    last = "0:v"

    for i, o in enumerate(overlays):
        src = str(base / o["src"]) if (base / o["src"]).exists() else o["src"]
        is_img = Path(src).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
        if is_img:
            args += ["-loop", "1", "-t", f"{_f(o['dur']):.3f}", "-i", src]
        else:
            args += ["-i", src]
        idx = i + 1
        at = _f(o.get("at"), 0.0)
        dur = _f(o.get("dur"), 1.0)
        scale = _f(o.get("scale"), 1.0)
        # HARD RULE: shift the overlay's timeline so its frame 0 lands at `at`,
        # otherwise the window shows the middle of the animation.
        chain = [f"[{idx}:v]trim=duration={dur:.3f},setpts=PTS-STARTPTS+{at:.4f}/TB"]
        if abs(scale - 1.0) > 1e-6:
            chain.append(f"scale=iw*{scale:.4f}:ih*{scale:.4f}")
        chain.append("format=rgba")
        ol = f"ov{i}"
        filters.append(",".join(chain) + f"[{ol}]")
        x = o.get("x", "0")
        y = o.get("y", "0")
        filters.append(f"[{last}][{ol}]overlay=x={x}:y={y}:eof_action=pass:"
                       f"enable='between(t,{at:.4f},{at + dur:.4f})'[v{i}]")
        last = f"v{i}"

    if captions and Path(captions).exists():
        # HARD RULE: captions are the final video step, always.
        esc = Path(captions).resolve().as_posix().replace(":", r"\:").replace("'", r"\'")
        filters.append(f"[{last}]ass='{esc}'[vcap]")
        last = "vcap"

    afilter = None
    target_i = _f(prof.get("loudness_lufs"), -14.0)
    target_tp = _f(prof.get("true_peak_db"), -1.0)
    if loudness:
        afilter = (f"loudnorm=I={target_i}:TP={target_tp}:LRA=11:print_format=summary")

    cmd = list(args)
    if filters:
        cmd += ["-filter_complex", ";".join(filters), "-map", f"[{last}]"]
    else:
        cmd += ["-map", "0:v"]
    if inp_has_audio(inp):
        cmd += ["-map", "0:a"]
        if afilter:
            cmd += ["-af", afilter]
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", "medium" if not preview else "veryfast",
            "-crf", str(23 if preview else crf), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(out)]
    run(cmd)
    return out


def inp_has_audio(path: str | Path) -> bool:
    return bool(probe(path).get("has_audio"))


def build_cut(edl_path: str | Path, out: str | Path, *, preview: bool = False,
              base: Path | None = None) -> Path:
    edl_file = Path(edl_path).resolve()
    base = base or edl_file.parent
    edl = load_edl(edl_file)
    errs = validate_edl(edl, base)
    if errs:
        for e in errs:
            bad("edl", e)
        die(f"{len(errs)} EDL error(s) — nothing was rendered.")
    prof = resolve_profile(edl)
    out = Path(out)
    with tempfile.TemporaryDirectory(prefix="mfe-cut-") as tmp:
        segs = cut_segments(edl, base, Path(tmp), preview=preview)
        draft = concat_lossless(segs, Path(tmp) / "concat.mp4")
        caps = None
        capfile = (edl.get("captions") or {}).get("file")
        if capfile:
            cand = base / capfile
            if cand.exists():
                caps = cand
        composite(edl, base, draft, out, captions=caps, prof=prof, preview=preview)
    return out


# ---------------------------------------------------------------------------
# Loudness / stream measurement
# ---------------------------------------------------------------------------

def measure_loudness(path: str | Path) -> dict[str, float]:
    ff = require_ffmpeg()
    p = run([ff, "-hide_banner", "-nostats", "-i", str(path),
             "-af", "ebur128=peak=true", "-f", "null", "-"], check=False)
    text = (p.stderr or "")
    out: dict[str, float] = {}
    # ebur128 emits a per-frame line every 100ms AND a summary block at the end.
    # The per-frame lines start near -70 dBFS in silence, so the summary is the
    # only honest source for the integrated value.
    sm = re.search(r"Integrated loudness:(.*?)(?:Loudness range:|True peak:|\Z)", text, re.S)
    scope = sm.group(1) if sm else text
    vals = re.findall(r"I:\s*(-?[\d.]+)\s*LUFS", scope)
    if vals:
        out["integrated_lufs"] = float(vals[-1] if sm else vals[-1])
    lra = re.search(r"LRA:\s*(-?[\d.]+)\s*LU", text)
    if lra:
        out["lra"] = float(lra.group(1))
    tp = re.search(r"True peak:.*?Peak:\s*(-?[\d.]+)\s*dBFS", text, re.S)
    peaks = re.findall(r"Peak:\s*(-?[\d.]+)\s*dBFS", text)
    if tp:
        out["true_peak_db"] = float(tp.group(1))
    elif peaks:
        out["true_peak_db"] = float(peaks[-1])
    return out


def detect_events(path: str | Path) -> dict[str, Any]:
    """Freeze, black and dead-stretch detection in one decode pass."""
    ff = require_ffmpeg()
    vf = ("freezedetect=n=-58dB:d=0.35,blackdetect=d=0.15:pix_th=0.10,"
          "fps=4,signalstats,metadata=print:key=lavfi.signalstats.YDIF")
    p = run([ff, "-hide_banner", "-nostats", "-i", str(path), "-vf", vf, "-an", "-f", "null", "-"],
            check=False)
    text = p.stderr or ""
    freezes = [(float(a), float(b)) for a, b in
               re.findall(r"freeze_start:\s*([\d.]+).*?freeze_end:\s*([\d.]+)", text, re.S)]
    if not freezes:
        freezes = [(float(t), float(t)) for t in re.findall(r"freeze_start:\s*([\d.]+)", text)]
    blacks = [(float(a), float(b)) for a, b in
              re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", text)]
    ydif = [float(x) for x in re.findall(r"lavfi\.signalstats\.YDIF=([\d.]+)", text)]
    stretches = _dead_stretches(ydif, 4.0, 0.75)
    return {"freezes": freezes, "blacks": blacks, "ydif": ydif, "dead_stretches": stretches}


def _dead_stretches(ydif: list[float], rate: float = 4.0, threshold: float = 0.5) -> list[dict[str, float]]:
    """Runs of near-zero frame difference = the picture stopped while time passed."""
    out, run_start = [], None
    for i, v in enumerate(ydif):
        if v < threshold:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None and (i - run_start) / rate >= 1.0:
                out.append({"start": round(run_start / rate, 2), "end": round(i / rate, 2),
                            "seconds": round((i - run_start) / rate, 2)})
            run_start = None
    if run_start is not None and (len(ydif) - run_start) / rate >= 1.0:
        out.append({"start": round(run_start / rate, 2), "end": round(len(ydif) / rate, 2),
                    "seconds": round((len(ydif) - run_start) / rate, 2)})
    return out


def boundary_levels(path: str | Path, boundaries: list[float], window: float = 0.06) -> list[dict[str, float]]:
    """Peak level in a short window straddling each cut, vs the local body level.

    A discontinuity at a cut is inaudible if the window's peak is close to the
    surrounding speech level; it is a pop if the window is far louder than both
    sides. We measure, we do not assume.
    """
    ff = require_ffmpeg()
    out = []
    for b in boundaries:
        st = max(0.0, b - window)
        p = run([ff, "-hide_banner", "-nostats", "-ss", f"{st:.3f}", "-t", f"{window * 2:.3f}",
                 "-i", str(path), "-af", "astats=metadata=1:reset=0,ametadata=print:key=lavfi.astats.Overall.Peak_level",
                 "-f", "null", "-"], check=False)
        peaks = [float(x) for x in re.findall(r"Peak_level=(-?[\d.]+)", p.stderr or "")]
        p2 = run([ff, "-hide_banner", "-nostats", "-ss", f"{max(0.0, b - 1.0):.3f}", "-t", "2.0",
                  "-i", str(path), "-af", "astats=metadata=1:reset=0,ametadata=print:key=lavfi.astats.Overall.RMS_level",
                  "-f", "null", "-"], check=False)
        rms = [float(x) for x in re.findall(r"RMS_level=(-?[\d.]+)", p2.stderr or "")]
        peak = max(peaks) if peaks else -99.0
        body = sum(rms) / len(rms) if rms else -99.0
        out.append({"at": round(b, 3), "peak_db": round(peak, 2), "body_rms_db": round(body, 2),
                    "delta_db": round(peak - body, 2)})
    return out


# ---------------------------------------------------------------------------
# Captions → ASS. Word-level, safe-zone aware, karaoke highlight optional.
# ---------------------------------------------------------------------------

CAPTION_STYLES: dict[str, dict[str, Any]] = {
    "bold-pop":   {"font": "DejaVu Sans", "scale": 0.048, "weight": -1, "primary": "&H00FFFFFF",
                   "highlight": "&H0000E5FF", "outline": 3, "shadow": 0, "caps": True, "karaoke": "active"},
    "clean-line": {"font": "DejaVu Sans", "scale": 0.040, "weight": 0, "primary": "&H00FFFFFF",
                   "highlight": "&H00FFFFFF", "outline": 2, "shadow": 0, "caps": False, "karaoke": None},
    "quiet-box":  {"font": "DejaVu Sans", "scale": 0.038, "weight": 0, "primary": "&H00FFFFFF",
                   "highlight": "&H0050D0FF", "outline": 0, "shadow": 1, "caps": False, "karaoke": None,
                   "back": "&H99000000"},
}


def load_words(src: str | Path) -> list[dict[str, Any]]:
    """Word timings from our JSON, or phrase timings from an SRT."""
    p = Path(src)
    if not p.exists():
        die(f"no such transcript: {p}")
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        words = data.get("words") if isinstance(data, dict) else data
        if not words:
            die("transcript JSON has no `words` array")
        return [{"w": str(w.get("w") or w.get("word") or "").strip(),
                 "s": _f(w.get("s", w.get("start"))), "e": _f(w.get("e", w.get("end")))} for w in words
                if str(w.get("w") or w.get("word") or "").strip()]
    return _words_from_srt(p.read_text(encoding="utf-8", errors="ignore"))


def _words_from_srt(text: str) -> list[dict[str, Any]]:
    """Split each SRT cue into words by character share — good enough for
    phrase-level timing, never claimed to be word-accurate."""
    words: list[dict[str, Any]] = []
    for m in re.finditer(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)\s*\n(.*?)(?=\n\s*\n|\Z)",
                         text, re.S):
        h1, m1, s1, ms1, h2, m2, s2, ms2 = (int(x) for x in m.groups()[:8])
        st = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000
        en = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000
        line = re.sub(r"<[^>]+>", " ", m.group(9)).replace("\n", " ").strip()
        toks = [t for t in line.split() if t]
        if not toks:
            continue
        total = sum(len(t) + 1 for t in toks)
        t = st
        for tok in toks:
            share = (len(tok) + 1) / total
            words.append({"w": tok, "s": round(t, 3), "e": round(min(en, t + (en - st) * share), 3)})
            t += (en - st) * share
    return words


def _ass_color(ass_hex: str) -> str:
    return ass_hex


def _ass_time(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def max_chars_for(prof: dict[str, Any], fontsize: int) -> int:
    """How many characters actually fit between the margins. Guessing this is
    how captions end up running under the platform's right-hand UI."""
    safe = prof.get("safe", {})
    avail = int(prof["width"]) * (1 - _f(safe.get("left"), 0.04) - _f(safe.get("right"), 0.13))
    return max(10, min(42, int(avail * 0.95 / (fontsize * 0.60))))


def chunk_words(words: list[dict[str, Any]], max_chars: int = 26,
                max_dur: float = 2.8, max_words: int = 4) -> list[list[dict[str, Any]]]:
    """Short-form caption chunking: short lines, one idea at a time."""
    chunks: list[list[dict[str, Any]]] = []
    cur: list[dict[str, Any]] = []
    for w in words:
        cand = cur + [w]
        too_long = sum(len(x["w"]) + 1 for x in cand) - 1 > max_chars
        too_many = len(cand) > max_words
        too_slow = cand and (cand[-1]["e"] - cand[0]["s"]) > max_dur
        gap = cur and (w["s"] - cur[-1]["e"]) > 0.65
        if cur and (too_long or too_many or too_slow or gap):
            chunks.append(cur)
            cur = [w]
        else:
            cur = cand
    if cur:
        chunks.append(cur)
    return chunks


def build_ass(words: list[dict[str, Any]], prof: dict[str, Any], style_name: str = "bold-pop",
              base: Path | None = None) -> tuple[str, list[dict[str, Any]]]:
    """Return (ass_text, caption_boxes) — boxes feed the safe-zone gate."""
    st = dict(CAPTION_STYLES.get(style_name, CAPTION_STYLES["bold-pop"]))
    W, H = int(prof["width"]), int(prof["height"])
    safe = prof.get("safe", {"top": 0.12, "bottom": 0.23, "left": 0.04, "right": 0.13})
    fontsize = max(18, round(H * _f(st["scale"])))
    margin_v = round(H * (_f(safe.get("bottom")) + 0.06))
    margin_l = round(W * _f(safe.get("left")))
    margin_r = round(W * _f(safe.get("right")))
    bold = -1 if _f(st.get("weight"), 0) < 0 else 0

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SV,{st['font']},{fontsize},{st['primary']},{st['highlight']},{st.get('back', '&H00000000')},{st.get('back', '&H80000000')},{bold},0,0,0,100,100,0,0,{1 if st.get('back') else 1},{_f(st.get('outline'), 2):.0f},{_f(st.get('shadow'), 0):.0f},2,{margin_l},{margin_r},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    maxc = max_chars_for(prof, fontsize)
    avail_px = W - margin_l - margin_r
    center_x = margin_l + avail_px / 2
    events, boxes = [], []
    for chunk in chunk_words(words, max_chars=maxc):
        if not chunk:
            continue
        s, e = chunk[0]["s"], chunk[-1]["e"]
        if e <= s:
            continue
        words_txt = [_ass_escape(w["w"], st.get("caps", False)) for w in chunk]
        if st.get("karaoke") == "active" and len(chunk) > 1:
            # One event per active word: the spoken word takes the accent, the
            # rest stay in the primary ink. This is the look every short-form
            # editor means by "highlight the key word", and karaoke \k cannot
            # produce it (\k sweeps colour, it does not isolate a word).
            for i, w in enumerate(chunk):
                body = []
                for j, t in enumerate(words_txt):
                    if j == i:
                        body.append(f"{{\\c{st['highlight']}&}}{t}{{\\c{st['primary']}&}}")
                    else:
                        body.append(t)
                wend = w["e"] if i == len(chunk) - 1 else min(chunk[i + 1]["s"], w["e"])
                if wend <= w["s"]:
                    wend = min(w["e"], e)
                events.append(f"Dialogue: 0,{_ass_time(w['s'])},{_ass_time(wend)},SV,,0,0,0,,"
                              + " ".join(body))
        else:
            events.append(f"Dialogue: 0,{_ass_time(s)},{_ass_time(e)},SV,,0,0,0,,"
                          + " ".join(words_txt))
        plain = " ".join(w["w"] for w in chunk)
        est_w = len(plain) * fontsize * 0.60
        lines = max(1, math.ceil(est_w / avail_px))
        box_w = min(avail_px, est_w)
        box_h = lines * fontsize * 1.18
        boxes.append({
            "start": round(s, 3), "end": round(e, 3), "text": plain, "lines": lines,
            # bounding box in fractions of the frame, for the safe-zone gate
            "x0": round((center_x - box_w / 2) / W, 4), "x1": round((center_x + box_w / 2) / W, 4),
            "y0": round(max(0.0, 1 - (margin_v + box_h) / H), 4), "y1": round(1 - margin_v / H, 4),
        })
    return header + "\n".join(events) + "\n", boxes


def _ass_escape(word: str, upper: bool) -> str:
    w = word.upper() if upper else word
    return w.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def build_captions(words_path: str | Path, out_ass: str | Path, prof: dict[str, Any],
                   style: str = "bold-pop", boxes_out: str | Path | None = None) -> Path:
    words = load_words(words_path)
    if not words:
        die("no words found in transcript")
    ass, boxes = build_ass(words, prof, style)
    out = Path(out_ass)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ass, encoding="utf-8")
    if boxes_out:
        Path(boxes_out).write_text(json.dumps({"style": style, "boxes": boxes}, indent=2), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Gates: the reason this project exists. Every check is measurable and named.
# ---------------------------------------------------------------------------

@dataclass
class Gate:
    id: str
    name: str
    status: str = "pass"   # pass | fail | warn | skip
    detail: str = ""
    facts: dict[str, Any] = field(default_factory=dict)

    @property
    def failed(self) -> bool:
        return self.status == "fail"



def scene_change_times(path: str | Path, threshold: float = 0.25) -> list[float]:
    """Timestamps where the picture changes enough to read as an edit.

    Uses ffmpeg's scene score rather than frame differencing, so a moving subject does not
    register as a cut and a hard cut does. Cheap enough to run on every render.
    """
    ff = require_ffmpeg()
    p = subprocess.run(
        [ff, "-hide_banner", "-i", str(path),
         "-vf", f"select='gt(scene,{threshold})',metadata=print:file=-",
         "-f", "null", "-"],
        capture_output=True, text=True)
    times = [float(t) for t in re.findall(r"pts_time:([0-9.]+)", p.stdout + p.stderr)]
    return sorted({round(t, 2) for t in times})


def gate_report(path: str | Path, edl: dict[str, Any] | None = None,
                profile: str | dict[str, Any] | None = None,
                caption_boxes: dict[str, Any] | None = None,
                expected_duration: float | None = None,
                max_static_s: float | None = None) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        die(f"nothing to gate: {path}")
    if edl and profile is None:
        prof = resolve_profile(edl)
    elif isinstance(profile, str):
        prof = dict(PROFILES.get(profile, PROFILES[DEFAULT_PROFILE]))
        prof["name"] = profile
    elif isinstance(profile, dict):
        base = dict(PROFILES[DEFAULT_PROFILE]); base.update(profile); prof = base
    else:
        # No destination declared: infer it from the file instead of assuming vertical,
        # which made every landscape render fail G1 for a rule nobody had stated.
        prof = dict(PROFILES[DEFAULT_PROFILE]); prof["name"] = DEFAULT_PROFILE
        prof["_inferred"] = True

    md = probe(path)
    if prof.pop("_inferred", False):
        w, h = md.get("display_width") or 0, md.get("display_height") or 0
        if w and h:
            ratio = w / h
            guess = min(PROFILES, key=lambda k: abs((PROFILES[k]["width"] / PROFILES[k]["height"]) - ratio))
            prof = dict(PROFILES[guess]); prof["name"] = guess
            prof["_note"] = (f"profile inferred from the file ({w}x{h}); "
                             f"pass --profile to enforce a destination")
    gates: list[Gate] = []

    # G0 — exists and matches the plan
    if not md.get("has_video"):
        gates.append(Gate("G0", "render exists", "fail", "no video stream"))
    else:
        exp = expected_duration if expected_duration is not None else (edl_duration(edl) if edl else None)
        dur = _f(md.get("duration_s"))
        if exp:
            delta = abs(dur - exp)
            gates.append(Gate("G0", "render exists", "pass" if delta <= max(0.35, exp * 0.01) else "fail",
                              f"duration {dur:.2f}s vs planned {exp:.2f}s (Δ{delta:.2f}s)",
                              {"duration": dur, "expected": exp}))
        else:
            gates.append(Gate("G0", "render exists", "pass" if dur > 0.2 else "fail",
                              f"duration {dur:.2f}s", {"duration": dur}))

    # G1 — delivery shape
    want_w, want_h = int(prof["width"]), int(prof["height"])
    got_w, got_h = int(md.get("display_width") or md.get("width") or 0), int(md.get("display_height") or md.get("height") or 0)
    shape_ok = (got_w, got_h) == (want_w, want_h)
    gates.append(Gate("G1", "delivery shape", "pass" if shape_ok else "fail",
                      f"{got_w}x{got_h} @{md.get('fps')}fps (want {want_w}x{want_h} @{prof.get('fps')}fps)",
                      {"width": got_w, "height": got_h, "fps": md.get("fps")}))

    # G2 — loudness and true peak
    if md.get("has_audio"):
        L = measure_loudness(path)
        li = L.get("integrated_lufs", -99.0)
        tp = L.get("true_peak_db", 0.0)
        target = _f(prof.get("loudness_lufs"), -14.0)
        ceil = _f(prof.get("true_peak_db"), -1.0) + 0.1
        st = "pass" if abs(li - target) <= 2.0 and tp <= ceil else "fail"
        gates.append(Gate("G2", "loudness", st,
                          f"{li:+.1f} LUFS (target {target:+.0f}±2), true peak {tp:+.1f} dBTP (max {ceil:+.1f})",
                          {"lufs": li, "true_peak": tp, "target": target}))
    else:
        gates.append(Gate("G2", "loudness", "fail", "no audio stream — a silent render is not a deliverable"))

    # G3 — dead picture: freezes and stretches
    ev = detect_events(path)
    bad_freezes = [f for f in ev["freezes"] if (f[1] - f[0]) > 0.5]
    long_stretch = [s for s in ev["dead_stretches"] if s["seconds"] > _f(prof.get("max_dead_stretch_s"), 3.0)]
    if bad_freezes:
        gates.append(Gate("G3", "picture alive", "fail",
                          f"{len(bad_freezes)} freeze(s) over 0.5s: {bad_freezes[:4]}",
                          {"freezes": bad_freezes}))
    elif long_stretch:
        gates.append(Gate("G3", "picture alive", "fail",
                          f"{len(long_stretch)} stretch(es) with no visual change: "
                          f"{[s['start'] for s in long_stretch][:5]}",
                          {"stretches": long_stretch}))
    else:
        gates.append(Gate("G3", "picture alive", "pass",
                          f"no freeze >0.5s, no stillness >{prof.get('max_dead_stretch_s', 3.0)}s",
                          {"freezes": ev["freezes"], "stretches": ev["dead_stretches"]}))

    # G4 — black frames
    if ev["blacks"]:
        gates.append(Gate("G4", "no black holes", "warn",
                          f"{len(ev['blacks'])} black stretch(es): {ev['blacks'][:3]}",
                          {"blacks": ev["blacks"]}))
    else:
        gates.append(Gate("G4", "no black holes", "pass", "none detected"))

    # G5 — cut boundaries: no pops
    if edl and md.get("has_audio"):
        bounds = [s["offset"] for s in edl_timeline(edl)][1:]
        if bounds:
            lv = boundary_levels(path, bounds)
            jumpy = [x for x in lv if x["delta_db"] > 6.0 and x["peak_db"] > -6.0]
            gates.append(Gate("G5", "cuts don't pop",
                              "fail" if jumpy else "pass",
                              f"{len(bounds)} boundaries checked, {len(jumpy)} spike(s)"
                              + (f": {[(x['at'], x['delta_db']) for x in jumpy][:4]}" if jumpy else ""),
                              {"boundaries": lv}))
        else:
            gates.append(Gate("G5", "cuts don't pop", "skip", "single segment, no interior boundary"))

    # G6 — captions readable and clear of platform UI
    if caption_boxes and caption_boxes.get("boxes"):
        safe = prof.get("safe", {})
        top, bottom = _f(safe.get("top")), _f(safe.get("bottom"))
        right = _f(safe.get("right")); left = _f(safe.get("left"))
        viol = []
        for b in caption_boxes["boxes"]:
            if b["y1"] > 1 - bottom + 0.02 or b["y0"] < top - 0.02 \
               or b["x0"] < left - 0.02 or b["x1"] > 1 - right + 0.02:
                viol.append(b)
        min_h = 0.035
        gates.append(Gate("G6", "captions safe", "fail" if viol else "pass",
                          f"{len(caption_boxes['boxes'])} cues, {len(viol)} outside the safe zone"
                          + (f": {[v['text'] for v in viol][:3]}" if viol else ""),
                          {"violations": viol[:10]}))
    else:
        gates.append(Gate("G6", "captions safe", "skip", "no caption boxes supplied"))

    # G7 — honest provenance
    prov = next((c for c in (path.parent / "provenance.json",
                             path.parent.parent / "provenance.json") if c.exists()),
                path.parent / "provenance.json")
    if prov.exists():
        try:
            data = json.loads(prov.read_text(encoding="utf-8"))
            entries = data.get("assets", [])
            unknown = [e for e in entries if e.get("origin") not in {"captured", "user", "generated", "stock-licensed"}]
            fabricated = [e for e in entries if e.get("claims_reality") and e.get("origin") == "generated"]
            if fabricated:
                gates.append(Gate("G7", "honest proof", "fail",
                                  f"{len(fabricated)} generated asset(s) implying reality: "
                                  f"{[e.get('id') for e in fabricated]}", {"fabricated": fabricated}))
            elif unknown:
                gates.append(Gate("G7", "honest proof", "warn",
                                  f"{len(unknown)} asset(s) with undeclared origin", {"unknown": unknown}))
            else:
                gates.append(Gate("G7", "honest proof", "pass",
                                  f"{len(entries)} asset(s), all origins declared", {"count": len(entries)}))
        except json.JSONDecodeError:
            gates.append(Gate("G7", "honest proof", "warn", "provenance.json is not valid JSON"))
    else:
        gates.append(Gate("G7", "honest proof", "warn",
                          "no provenance.json — declare origins if any asset claims reality"))

    # G8 — pace: something has to change, and the sum of the parts must not stall.
    # Applies by duration, not aspect: a 19-second landscape cut is still short-form.
    dur_s = float(md.get("duration_s") or 0.0)
    if dur_s <= 90 or prof.get("name", "").endswith(("9x16", "1x1")):
        cuts = scene_change_times(path)
        marks = [0.0] + [c for c in cuts if c > 0.05] + [float(md.get("duration_s") or 0.0)]
        gaps = [(round(marks[i + 1] - marks[i], 2), round(marks[i], 2))
                for i in range(len(marks) - 1)]
        worst, worst_at = max(gaps) if gaps else (0.0, 0.0)
        cap = float(max_static_s
                    or (edl or {}).get("pacing", {}).get("max_static_s")
                    or 3.5)
        if worst > cap:
            gates.append(Gate("G8", "pace", "fail",
                              f"{worst:.2f}s with no visible change from {worst_at:.2f}s "
                              f"(max {cap:.1f}s) — {len(cuts)} edit point(s) in "
                              f"{md.get('duration_s', 0):.1f}s",
                              {"longest_static_s": worst, "at_s": worst_at,
                               "cuts": cuts, "max_static_s": cap}))
        elif worst > cap * 0.85:
            gates.append(Gate("G8", "pace", "warn",
                              f"{worst:.2f}s without a change from {worst_at:.2f}s, close to the "
                              f"{cap:.1f}s limit", {"longest_static_s": worst, "at_s": worst_at,
                                                   "cuts": cuts}))
        else:
            gates.append(Gate("G8", "pace", "pass",
                              f"longest stretch without a change {worst:.2f}s over {len(cuts)} "
                              f"edit point(s)", {"longest_static_s": worst, "cuts": cuts}))
    else:
        gates.append(Gate("G8", "pace", "skip",
                          f"{dur_s:.0f}s is long-form — pacing is the piece's own, not a rule"))

    report = {
        "tool": f"motionframe-edit {MFE_VERSION}",
        "file": str(path),
        "profile": prof.get("name", "custom"),
        "profile_note": prof.get("_note"),
        "measured_at": _now(),
        "media": {k: md.get(k) for k in ("duration_s", "display_width", "display_height",
                                         "fps", "codec", "audio_codec", "rotation")},
        "gates": [{"id": g.id, "name": g.name, "status": g.status,
                   "detail": g.detail, "facts": g.facts} for g in gates],
        "verdict": "fail" if any(g.failed for g in gates) else "pass",
        "warnings": sum(1 for g in gates if g.status == "warn"),
    }
    return report


def remap_words_to_output(words: list[dict[str, Any]], edl: dict[str, Any],
                          source: str | None = None) -> list[dict[str, Any]]:
    """Move source-time words onto the OUTPUT timeline, dropping cut-away words.

    Caption timing is the most common silent failure in assembled cuts: the
    words are right, the times belong to a different timeline. This function is
    the only sanctioned way to produce caption times from a source transcript.
    """
    segs = [s for s in edl_timeline(edl) if source is None or s["source"] == source]
    out: list[dict[str, Any]] = []
    for w in words:
        s, e = _f(w.get("s")), _f(w.get("e"))
        mid = (s + e) / 2
        for seg in segs:
            a, b = _f(seg["start"]), _f(seg["end"])
            if a <= mid <= b:
                sp = _f(seg.get("speed", 1.0), 1.0)
                out.append({
                    "w": w["w"],
                    "s": round(seg["offset"] + (max(s, a) - a) / sp, 3),
                    "e": round(seg["offset"] + (min(e, b) - a) / sp, 3),
                })
                break
    return out


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def print_report(rep: dict[str, Any]) -> None:
    print(f"\n  {c('gate report', '1')}  {Path(rep['file']).name}  ·  profile {rep['profile']}")
    m = rep["media"]
    info("measured", f"{m.get('duration_s')}s  {m.get('display_width')}x{m.get('display_height')}  "
                     f"@{m.get('fps')}fps  {m.get('codec')}/{m.get('audio_codec')}")
    for g in rep["gates"]:
        if g["status"] == "pass":
            ok(g["id"], f"{g['name']}: {g['detail']}")
        elif g["status"] == "fail":
            bad(g["id"], f"{g['name']}: {g['detail']}")
        elif g["status"] == "warn":
            warn(g["id"], f"{g['name']}: {g['detail']}")
        else:
            info(g["id"], f"{g['name']}: {g['detail']}")
    verdict = rep["verdict"]
    line = f"  verdict: {verdict.upper()}"
    if rep["warnings"]:
        line += f"  ({rep['warnings']} warning(s))"
    print("\n" + (c(line, "32;1") if verdict == "pass" else c(line, "31;1")) + "\n")


# ---------------------------------------------------------------------------
# Contact sheet: look at your own output before anyone else does.
# ---------------------------------------------------------------------------

def contact_sheet(path: str | Path, out: str | Path, every: float = 1.0,
                  cols: int = 4, thumb_w: int = 320) -> Path:
    ff = require_ffmpeg()
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    md = probe(path)
    dur = _f(md.get("duration_s"), 0)
    rows = max(1, math.ceil((dur / max(0.05, every)) / cols))
    vf = (f"fps=1/{every},scale={thumb_w}:-1,"
          f"drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.6,"
          f"tile={cols}x{rows}:padding=4:color=0x101010")
    run([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", str(path),
         "-vf", vf, "-frames:v", "1", "-q:v", "3", str(out)], check=False)
    return out


# ---------------------------------------------------------------------------
# Scaffold: a project an agent can safely work inside.
# ---------------------------------------------------------------------------

PROJECT_TEMPLATE = {
    "motionframe-edit.json": {
        "version": SCHEMA_VERSION,
        "profile": DEFAULT_PROFILE,
        "created_with": f"motionframe-edit {MFE_VERSION}",
    },
    "edl.json": {
        "version": SCHEMA_VERSION,
        "project": "untitled",
        "profile": DEFAULT_PROFILE,
        "sources": {"A": "footage/take-01.mp4"},
        "segments": [],
        "overlays": [],
        "captions": {"enabled": True, "style": "bold-pop", "file": "captions.ass"},
    },
    "taste.md": """# Taste — this person's corrections, in their own words

> Read this before every edit. Append. Never rewrite history.
> One rule per line: the correction, then what it replaced.

## Global
- (empty — every line here was paid for by a real correction)

## Pacing
## Captions
## Sound
## Look
## Never
""",
    "brief.md": """# Brief

**What this is:**
**Who it's for:**
**The one thing they should remember:**
**Where it publishes:**
**Length target:**
**Must keep:**
**Must cut:**
""",
    "notes.md": "# Session notes\n\nAppend decisions and why. Newest last.\n",
    "provenance.json": {"assets": []},
}


def scaffold(target: str | Path, profile: str = DEFAULT_PROFILE) -> Path:
    root = Path(target)
    (root / "footage").mkdir(parents=True, exist_ok=True)
    (root / "assets").mkdir(exist_ok=True)
    (root / "out").mkdir(exist_ok=True)
    (root / "work").mkdir(exist_ok=True)
    for name, content in PROJECT_TEMPLATE.items():
        p = root / name
        if p.exists():
            info("exists", name)
            continue
        if isinstance(content, dict):
            c2 = json.loads(json.dumps(content))
            if name == "edl.json":
                c2["profile"] = profile
            p.write_text(json.dumps(c2, indent=2) + "\n", encoding="utf-8")
        else:
            p.write_text(content, encoding="utf-8")
        ok("created", name)
    return root


# ---------------------------------------------------------------------------
# Doctor: capability scan, so the agent never guesses what is installed.
# ---------------------------------------------------------------------------

def doctor(as_json: bool = False) -> dict[str, Any]:
    def ver(cmd: list[str]) -> str | None:
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            return (p.stdout or p.stderr).strip().splitlines()[0]
        except Exception:
            return None

    tys = shutil.which("yt-dlp")
    whisper = shutil.which("whisper-cli") or shutil.which("whisper-cpp") or shutil.which("main")
    fw = None
    try:
        import faster_whisper  # noqa: F401
        fw = "faster-whisper"
    except Exception:
        pass
    node = ver(["node", "--version"])
    chrome = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome") or shutil.which("chrome")
    result = {
        "motionframe-edit": MFE_VERSION,
        "ffmpeg": {"path": TC.ffmpeg, "version": TC.ffmpeg_version,
                   "filters_ok": sorted(TC.can)},
        "ffprobe": TC.ffprobe,
        "node": node,
        "chrome": chrome,
        "yt_dlp": tys,
        "asr": whisper or fw,
        "asr_kind": "whisper.cpp" if whisper else (fw or None),
        "fonts": _font_count(),
        "paid_keys_detected": _paid_env_vars(),
        "lanes": {
            "ffmpeg": bool(TC.ffmpeg),
            "html-capture": bool(node and chrome),
            "react-motion": bool(node),
        },
    }
    if as_json:
        print(json.dumps(result, indent=2))
        return result

    print(f"\n  {c('motionframe-edit', '1')} {MFE_VERSION}  ·  capability scan\n")
    if TC.ffmpeg:
        ok("ffmpeg", f"{TC.ffmpeg_version} — {len(TC.can)}/11 core filters available")
    else:
        bad("ffmpeg", "missing — pip install imageio-ffmpeg (free)")
    info("ffprobe", TC.ffprobe or "not found (falling back to `ffmpeg -i` parsing)")
    (ok if node else warn)("node", node or "not found — the html/react motion lanes need it, ffmpeg lane does not")
    (ok if chrome else warn)("chrome", chrome or "not found — needed only for HTML-capture motion")
    (ok if result["asr"] else warn)("asr", result["asr"] or
                                    "not found — install whisper.cpp or faster-whisper for transcription (both free)")
    (ok if tys else info)("yt-dlp", tys or "not found — only needed to fetch source clips")
    info("fonts", f"{result['fonts']} available" + ("" if result["fonts"] > 2 else " — install a font package for captions"))
    keys = result["paid_keys_detected"]
    if keys:
        warn("paid keys", f"present in env but IGNORED by motionframe-edit: {', '.join(keys)}")
    else:
        ok("paid keys", "none in use — this toolchain is fully local")
    print()
    for lane, has in result["lanes"].items():
        (ok if has else info)(lane, "ready" if has else "unavailable (documented fallback applies)")
    print()
    return result


def _font_count() -> int:
    try:
        p = subprocess.run(["fc-list"], capture_output=True, text=True, timeout=20)
        return len([ln for ln in p.stdout.splitlines() if ln.strip()])
    except Exception:
        return 0


PAID_ENV = ["ELEVENLABS_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY",
            "GOOGLE_API_KEY", "REPLICATE_API_TOKEN", "HEYGEN_API_KEY", "RUNWAY_API_SECRET",
            "SHOTSTACK_API_KEY", "CLOUDINARY_URL", "AWS_SECRET_ACCESS_KEY"]


def _paid_env_vars() -> list[str]:
    return [k for k in PAID_ENV if os.environ.get(k)]


# ---------------------------------------------------------------------------
# Demo: a self-contained proof that the pipeline and the gates both work.
# `mfe demo` must pass. `mfe demo --selftest` must fail in the ways it claims to.
# ---------------------------------------------------------------------------

def _make_demo_fixture(dirpath: Path) -> tuple[Path, Path]:
    """Synthetic footage: moving pattern + tone with real speech-shaped gaps."""
    ff = require_ffmpeg()
    src = dirpath / "footage" / "take-01.mp4"
    src.parent.mkdir(parents=True, exist_ok=True)
    run([ff, "-hide_banner", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30:duration=14",
         "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000:duration=14",
         "-filter_complex", "[1:a]volume=0.22,tremolo=f=3:d=0.8[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src)])
    srt = dirpath / "footage" / "take-01.srt"
    srt.write_text(
        "1\n00:00:00,200 --> 00:00:02,400\nNinety percent of editing is deciding\n\n"
        "2\n00:00:02,600 --> 00:00:05,200\nnot rendering. The renderer is the easy part.\n\n"
        "3\n00:00:05,400 --> 00:00:08,100\nWhat nobody tells you is that a cut\n\n"
        "4\n00:00:08,300 --> 00:00:11,000\nhas to be audited, frame by frame.\n\n"
        "5\n00:00:11,200 --> 00:00:13,600\nThat is what motionframe-edit is for.\n",
        encoding="utf-8")
    return src, srt


def _demo_edl(srt_words: list[dict[str, Any]]) -> dict[str, Any]:
    segs = []
    spans = [(0.10, 5.30, "HOOK"), (5.40, 11.10, "BODY"), (11.15, 13.70, "PAYOFF")]
    for i, (a, b, beat) in enumerate(spans):
        segs.append({
            "id": f"s{i+1}", "source": "A", "start": round(a, 2), "end": round(b, 2),
            "beat": beat, "grade": "none", "fade_in": 0.03, "fade_out": 0.03,
        })
    return {
        "version": SCHEMA_VERSION, "project": "demo", "profile": "vertical-9x16",
        "sources": {"A": "footage/take-01.mp4"},
        "segments": segs, "overlays": [],
        "captions": {"enabled": True, "style": "bold-pop", "file": "captions.ass"},
        # the demo is a fixture, not a delivery: one locked-off shot by construction, so the
        # pacing gate would be measuring the fixture rather than the engine
        "pacing": {"max_static_s": 15.0},
    }


def demo(workdir: str | Path, selftest: bool = False, keep: bool = False) -> int:
    root = Path(workdir)
    root.mkdir(parents=True, exist_ok=True)
    print(f"\n  {c('demo', '1')}  building a synthetic project in {root}\n")
    scaffold(root)
    src, srt = _make_demo_fixture(root)
    ok("fixture", f"{src.name} + phrase timings (no assets, no downloads)")

    # Remap the SRT into output-timeline caption data, the way the skill tells you to.
    words = _words_from_srt(srt.read_text(encoding="utf-8"))
    edl = _demo_edl(words)
    (root / "edl.json").write_text(json.dumps(edl, indent=2) + "\n", encoding="utf-8")
    ok("edl", f"{len(edl['segments'])} segments")

    errs = validate_edl(edl, root)
    if errs:
        for e in errs:
            bad("edl", e)
        return 1
    ok("edl", "validates clean")

    prof = resolve_profile(edl)
    mapped = remap_words_to_output(words, edl, source="A")
    wjson = root / "work" / "words.json"
    wjson.parent.mkdir(parents=True, exist_ok=True)
    wjson.write_text(json.dumps({"source": "transcript-on-output-timeline",
                                 "words": mapped}, indent=2), encoding="utf-8")
    info("captions", f"{len(words)} source words → {len(mapped)} on the output timeline "
                     f"({len(words) - len(mapped)} cut away, correctly dropped)")
    ass = build_captions(wjson, root / "captions.ass", prof, "bold-pop",
                         root / "work" / "caption-boxes.json")
    ok("captions", f"{len(json.loads((root / 'work' / 'caption-boxes.json').read_text())['boxes'])} cues → captions.ass")

    out = root / "out" / "demo.mp4"
    with tempfile.TemporaryDirectory(prefix="mfe-demo-") as tmp:
        segs = cut_segments(edl, root, Path(tmp) / "segs")
        draft = concat_lossless(segs, Path(tmp) / "concat.mp4")
        composite(edl, root, draft, out, captions=root / "captions.ass", prof=prof)
    ok("render", str(out.relative_to(root)))

    (root / "out" / "provenance.json").write_text(json.dumps({"assets": [
        {"id": "take-01", "origin": "generated", "claims_reality": False,
         "note": "synthetic ffmpeg fixture; it depicts nothing real, and says so"}
    ]}, indent=2) + "\n", encoding="utf-8")
    boxes = json.loads((root / "work" / "caption-boxes.json").read_text())
    rep = gate_report(out, edl=edl, caption_boxes=boxes)
    print_report(rep)
    (root / "gate-report.json").write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
    sheet = contact_sheet(out, root / "work" / "sheet.jpg", every=1.5)
    if sheet.exists():
        ok("sheet", str(sheet.relative_to(root)) + " — look at it before you trust the numbers")

    if not selftest:
        return 0 if rep["verdict"] == "pass" else 1

    # ---- selftest: prove the gates can fail ----
    print(f"  {c('selftest', '1')}  feeding the gates known-bad renders\n")
    failures = 0

    # (a) a frozen picture must trip G3
    frozen = root / "out" / "bad-freeze.mp4"
    ff = require_ffmpeg()
    prof_w, prof_h = int(prof["width"]), int(prof["height"])
    run([ff, "-hide_banner", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", f"color=c=0x2b2b2b:s={prof_w}x{prof_h}:d=6:r=30",
         "-f", "lavfi", "-i", "sine=frequency=300:duration=6",
         "-c:v", "libx264", "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-shortest", str(frozen)], check=False)
    r1 = gate_report(frozen, profile="vertical-9x16")
    g3 = next(g for g in r1["gates"] if g["id"] == "G3")
    if g3["status"] == "fail":
        ok("selftest", "G3 catches a frozen picture")
    else:
        bad("selftest", f"G3 did NOT catch a frozen picture ({g3['detail']})")
        failures += 1

    # (b) a silent render must trip G2
    silent = root / "out" / "bad-silent.mp4"
    run([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), "-an",
         "-c:v", "libx264", "-crf", "24", str(silent)], check=False)
    r2 = gate_report(silent, profile="vertical-9x16")
    g2 = next(g for g in r2["gates"] if g["id"] == "G2")
    if g2["status"] == "fail":
        ok("selftest", "G2 catches a silent render")
    else:
        bad("selftest", f"G2 did not catch a missing audio stream ({g2['detail']})")
        failures += 1

    # (c) wrong aspect must trip G1
    r3 = gate_report(out, profile="landscape-16x9")
    g1 = next(g for g in r3["gates"] if g["id"] == "G1")
    if g1["status"] == "fail":
        ok("selftest", "G1 catches a delivery-shape mismatch")
    else:
        bad("selftest", f"G1 missed an aspect mismatch ({g1['detail']})")
        failures += 1

    # (d) captions outside the safe zone must trip G6
    bad_boxes = {"style": "x", "boxes": [{"start": 0, "end": 1, "text": "too low",
                                          "x0": 0.2, "x1": 0.8, "y0": 0.90, "y1": 0.97}]}
    r4 = gate_report(out, edl=edl, caption_boxes=bad_boxes)
    g6 = next(g for g in r4["gates"] if g["id"] == "G6")
    if g6["status"] == "fail":
        ok("selftest", "G6 catches captions in the platform UI zone")
    else:
        bad("selftest", f"G6 missed unsafe captions ({g6['detail']})")
        failures += 1

    # (e) a fabricated screenshot must trip G7
    prov = root / "out" / "provenance.json"
    prov.write_text(json.dumps({"assets": [
        {"id": "shot-1", "origin": "generated", "claims_reality": True}]}), encoding="utf-8")
    r5 = gate_report(out, edl=edl, caption_boxes=boxes)
    g7 = next(g for g in r5["gates"] if g["id"] == "G7")
    if g7["status"] == "fail":
        ok("selftest", "G7 catches a generated asset implying reality")
    else:
        bad("selftest", f"G7 missed fabricated proof ({g7['detail']})")
        failures += 1
    prov.unlink(missing_ok=True)

    print()
    if failures:
        bad("selftest", f"{failures} gate(s) are asleep — fix before trusting any report")
        return 1
    ok("selftest", "all gates demonstrably fail on bad input, and pass on good input")
    print()
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_probe(a: argparse.Namespace) -> int:
    out = [probe(p) for p in a.files]
    if a.json or True:
        print(json.dumps(out if len(out) > 1 else out[0], indent=2))
    return 0


def cmd_doctor(a: argparse.Namespace) -> int:
    doctor(as_json=a.json)
    return 0 if TC.has_ffmpeg else 1


def cmd_scaffold(a: argparse.Namespace) -> int:
    scaffold(a.target, a.profile)
    print(f"\n  next: put footage in {a.target}/footage, then write {a.target}/brief.md\n")
    return 0


def cmd_validate(a: argparse.Namespace) -> int:
    edl = load_edl(a.edl)
    errs = validate_edl(edl, Path(a.edl).resolve().parent)
    print(f"\n  duration on the output timeline: {edl_duration(edl):.2f}s "
          f"across {len(edl.get('segments', []))} segment(s)")
    if errs:
        for e in errs:
            bad("edl", e)
        return 1
    ok("edl", "valid")
    print()
    return 0


def cmd_render(a: argparse.Namespace) -> int:
    out = build_cut(a.edl, a.out, preview=a.preview)
    md = probe(out)
    print(f"\n  wrote {out}  ({md.get('duration_s')}s, {md.get('display_width')}x{md.get('display_height')})\n")
    return 0


def cmd_captions(a: argparse.Namespace) -> int:
    edl = load_edl(a.edl) if a.edl else None
    prof = resolve_profile(edl) if edl else dict(PROFILES[a.profile])
    if edl and a.remap:
        words = remap_words_to_output(load_words(a.words), edl, source=a.remap)
        tmp = Path(a.out).with_suffix(".words.json")
        tmp.write_text(json.dumps({"words": words}, indent=2), encoding="utf-8")
        a.words = str(tmp)
        info("remap", f"{len(words)} words placed on the output timeline from source {a.remap!r}")
    boxes = Path(a.out).with_suffix(".boxes.json")
    p = build_captions(a.words, a.out, prof, a.style, boxes)
    n = len(json.loads(boxes.read_text())["boxes"])
    print(f"\n  wrote {p} ({n} cues) and {boxes}\n")
    return 0


def cmd_gate(a: argparse.Namespace) -> int:
    edl = load_edl(a.edl) if a.edl else None
    boxes = json.loads(Path(a.boxes).read_text()) if a.boxes else None
    rep = gate_report(a.file, edl=edl, profile=a.profile, caption_boxes=boxes,
                      expected_duration=a.expect, max_static_s=a.max_static)
    print_report(rep)
    if a.out:
        Path(a.out).write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
        print(f"  report: {a.out}\n")
    return 0 if rep["verdict"] == "pass" else 1


def cmd_sheet(a: argparse.Namespace) -> int:
    p = contact_sheet(a.file, a.out, every=a.every)
    print(f"\n  wrote {p} — describe every frame before you judge it\n")
    return 0


def cmd_demo(a: argparse.Namespace) -> int:
    return demo(a.workdir, selftest=a.selftest)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mfe", description="motionframe-edit — the measurable half of editing.")
    p.add_argument("--version", action="version", version=f"motionframe-edit {MFE_VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor", help="capability scan (what is installed, what is not)")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_doctor)

    pr = sub.add_parser("probe", help="probe media (display dimensions, fps, rotation)")
    pr.add_argument("files", nargs="+")
    pr.add_argument("--json", action="store_true")
    pr.set_defaults(func=cmd_probe)

    sc = sub.add_parser("scaffold", help="create a project an agent can work inside")
    sc.add_argument("target")
    sc.add_argument("--profile", default=DEFAULT_PROFILE, choices=list(PROFILES))
    sc.set_defaults(func=cmd_scaffold)

    va = sub.add_parser("validate", help="validate an EDL and print its timeline")
    va.add_argument("edl")
    va.set_defaults(func=cmd_validate)

    rd = sub.add_parser("render", help="render an EDL to a file")
    rd.add_argument("--edl", required=True)
    rd.add_argument("--out", required=True)
    rd.add_argument("--preview", action="store_true", help="fast, smaller, for review not delivery")
    rd.set_defaults(func=cmd_render)

    ca = sub.add_parser("captions", help="build ASS captions + safe-zone boxes")
    ca.add_argument("--edl", help="take the profile from this EDL")
    ca.add_argument("--profile", default=DEFAULT_PROFILE, choices=list(PROFILES))
    ca.add_argument("--words", required=True, help="word timings JSON or phrase-level SRT")
    ca.add_argument("--style", default="bold-pop", choices=list(CAPTION_STYLES))
    ca.add_argument("--out", required=True)
    ca.add_argument("--remap", metavar="SOURCE_ID",
                    help="remap source-time words onto the output timeline using --edl")
    ca.set_defaults(func=cmd_captions)

    ga = sub.add_parser("gate", help="audit a render against the gates")
    ga.add_argument("--file", required=True)
    ga.add_argument("--edl")
    ga.add_argument("--profile", default=None)
    ga.add_argument("--boxes", help="caption boxes JSON from `mfe captions`")
    ga.add_argument("--expect", type=float, help="expected duration in seconds")
    ga.add_argument("--max-static", type=float, default=None, dest="max_static",
                    help="longest allowed stretch with no visible change (default 3.5 s)")
    ga.add_argument("--out")
    ga.set_defaults(func=cmd_gate)

    sh = sub.add_parser("sheet", help="contact sheet of a render")
    sh.add_argument("--file", required=True)
    sh.add_argument("--out", required=True)
    sh.add_argument("--every", type=float, default=1.0)
    sh.set_defaults(func=cmd_sheet)

    de = sub.add_parser("demo", help="build a synthetic project end-to-end and audit it")
    de.add_argument("--workdir", default=".mfe-demo")
    de.add_argument("--selftest", action="store_true", help="also prove the gates fail on bad input")
    de.set_defaults(func=cmd_demo)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
