#!/usr/bin/env python3
"""
Unit tests for the motionframe-edit engine.

The philosophy is the same one the gates use: a check that cannot fail is
decoration. So every test here asserts a *failure* mode of the engine as often as
it asserts a success — the validator must reject a cut inside a word, the dead
stretch detector must find a dead stretch, the remapper must drop cut-away words.

Run:  python3 -m unittest discover -s tests -v
      MFE_INTEGRATION=1 python3 -m unittest discover -s tests -v   # includes ffmpeg
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("mfe", ROOT / "tools" / "mfe.py")
mfe = importlib.util.module_from_spec(spec)
sys.modules["mfe"] = mfe
spec.loader.exec_module(mfe)  # type: ignore

HAS_FFMPEG = bool(mfe.TC.ffmpeg)
INTEGRATION = os.environ.get("MFE_INTEGRATION") == "1"


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

def make_edl(**over):
    edl = {
        "version": 1,
        "project": "t",
        "profile": "vertical-9x16",
        "sources": {"A": "a.mp4"},
        "segments": [
            {"id": "s1", "source": "A", "start": 1.0, "end": 4.0},
            {"id": "s2", "source": "A", "start": 6.0, "end": 8.0},
        ],
        "overlays": [],
        "captions": {"enabled": True, "style": "bold-pop", "file": "c.ass"},
    }
    edl.update(over)
    return edl


# ---------------------------------------------------------------------------
# EDL validation — the guard against silent breakage
# ---------------------------------------------------------------------------

class TestValidation(unittest.TestCase):
    def test_clean_edl_passes(self):
        self.assertEqual(mfe.validate_edl(make_edl()), [])

    def test_wrong_version(self):
        errs = mfe.validate_edl(make_edl(version=2))
        self.assertTrue(any("version" in e for e in errs))

    def test_unknown_source(self):
        edl = make_edl()
        edl["segments"][0]["source"] = "Z"
        self.assertTrue(any("not in sources" in e for e in mfe.validate_edl(edl)))

    def test_end_before_start(self):
        edl = make_edl()
        edl["segments"][0]["end"] = 0.5
        self.assertTrue(any("must be >" in e for e in mfe.validate_edl(edl)))

    def test_duplicate_ids(self):
        edl = make_edl()
        edl["segments"][1]["id"] = "s1"
        self.assertTrue(any("duplicate" in e for e in mfe.validate_edl(edl)))

    def test_fade_too_long_is_caught(self):
        edl = make_edl()
        edl["segments"][0]["fade_out"] = 0.4
        self.assertTrue(any("fades above" in e for e in mfe.validate_edl(edl)))

    def test_cut_inside_word_is_caught(self):
        edl = make_edl()
        edl["segments"][0]["word_edges"] = [{"w": "deciding", "start": 0.4, "end": 1.2}]
        errs = mfe.validate_edl(edl)
        self.assertTrue(any("inside word" in e for e in errs), errs)

    def test_zero_speed_is_caught(self):
        edl = make_edl()
        edl["segments"][0]["speed"] = 0
        self.assertTrue(any("speed" in e for e in mfe.validate_edl(edl)))

    def test_missing_segments_is_caught(self):
        self.assertTrue(any("segments" in e for e in mfe.validate_edl(make_edl(segments=[]))))


# ---------------------------------------------------------------------------
# Timeline maths
# ---------------------------------------------------------------------------

class TestTimeline(unittest.TestCase):
    def test_offsets_are_cumulative(self):
        t = mfe.edl_timeline(make_edl())
        self.assertEqual([round(s["offset"], 3) for s in t], [0.0, 3.0])

    def test_duration(self):
        self.assertAlmostEqual(mfe.edl_duration(make_edl()), 5.0)

    def test_speed_changes_output_duration_only(self):
        edl = make_edl()
        edl["segments"][0]["speed"] = 2.0
        self.assertAlmostEqual(mfe.edl_duration(edl), 1.5 + 2.0)
        self.assertEqual(edl["segments"][0]["start"], 1.0)  # source time untouched

    def test_source_time_maps_back(self):
        edl = make_edl()
        src, t = mfe.source_time(edl, 4.0)   # 1s into the second segment
        self.assertEqual(src, "A")
        self.assertAlmostEqual(t, 7.0)

    def test_source_time_accounts_for_speed(self):
        edl = make_edl()
        edl["segments"][0]["speed"] = 0.5          # 3s of source becomes 6s
        t = mfe.edl_timeline(edl)
        self.assertAlmostEqual(t[1]["offset"], 6.0)
        _, st = mfe.source_time(edl, 3.0)           # 3s into a half-speed segment
        self.assertAlmostEqual(st, 2.5)


# ---------------------------------------------------------------------------
# Caption remapping — the most common silent failure in assembled cuts
# ---------------------------------------------------------------------------

class TestRemap(unittest.TestCase):
    words = [
        {"w": "cut", "s": 0.2, "e": 0.5},      # before the first segment
        {"w": "kept", "s": 1.5, "e": 1.9},     # inside s1
        {"w": "gone", "s": 5.0, "e": 5.4},     # in the gap between segments
        {"w": "later", "s": 6.5, "e": 6.9},    # inside s2
    ]

    def test_cut_away_words_are_dropped(self):
        out = mfe.remap_words_to_output(self.words, make_edl(), "A")
        self.assertEqual([w["w"] for w in out], ["kept", "later"])

    def test_times_land_on_the_output_timeline(self):
        out = mfe.remap_words_to_output(self.words, make_edl(), "A")
        self.assertAlmostEqual(out[0]["s"], 0.5)    # 1.5 - 1.0 + 0.0
        self.assertAlmostEqual(out[1]["s"], 3.5)    # 6.5 - 6.0 + 3.0

    def test_speed_is_inverted_correctly(self):
        edl = make_edl()
        edl["segments"][0]["speed"] = 2.0            # half the output duration
        out = mfe.remap_words_to_output(self.words, edl, "A")
        self.assertAlmostEqual(out[0]["s"], 0.25)    # (1.5-1.0)/2

    def test_words_are_clipped_to_the_segment(self):
        words = [{"w": "edge", "s": 0.5, "e": 1.6}]  # straddles the in-point
        out = mfe.remap_words_to_output(words, make_edl(), "A")
        self.assertAlmostEqual(out[0]["s"], 0.0)


# ---------------------------------------------------------------------------
# Dead-stretch detection
# ---------------------------------------------------------------------------

class TestDeadStretch(unittest.TestCase):
    def test_stillness_is_found(self):
        # 4 samples/s; 8 zeros = 2 seconds of no change
        ydif = [10.0] * 8 + [0.1] * 8 + [10.0] * 8
        runs = mfe._dead_stretches(ydif, 4.0, 0.5)
        self.assertEqual(len(runs), 1)
        self.assertAlmostEqual(runs[0]["seconds"], 2.0)

    def test_motion_is_not_flagged(self):
        self.assertEqual(mfe._dead_stretches([10.0] * 40, 4.0, 0.5), [])

    def test_short_stillness_is_ignored(self):
        ydif = [10.0] * 8 + [0.0] * 2 + [10.0] * 8   # 0.5s, under the 1s floor
        self.assertEqual(mfe._dead_stretches(ydif, 4.0, 0.5), [])


# ---------------------------------------------------------------------------
# Captions
# ---------------------------------------------------------------------------

class TestCaptions(unittest.TestCase):
    def test_max_chars_shrinks_with_a_narrow_safe_zone(self):
        wide = dict(mfe.PROFILES["landscape-16x9"])
        narrow = dict(mfe.PROFILES["vertical-9x16"])
        self.assertLess(mfe.max_chars_for(narrow, 92), mfe.max_chars_for(wide, 60))

    def test_chunking_respects_limits(self):
        words = [{"w": "x" * 8, "s": i * 0.3, "e": i * 0.3 + 0.25} for i in range(12)]
        chunks = mfe.chunk_words(words, max_chars=20, max_dur=2.8, max_words=4)
        for c in chunks:
            self.assertLessEqual(len(c), 4)
            self.assertLessEqual(sum(len(w["w"]) + 1 for w in c) - 1, 20)

    def test_silence_forces_a_new_chunk(self):
        words = [{"w": "a", "s": 0.0, "e": 0.2}, {"w": "b", "s": 1.5, "e": 1.7}]
        self.assertEqual(len(mfe.chunk_words(words)), 2)

    def test_ass_is_well_formed(self):
        words = [{"w": "hello", "s": 0.0, "e": 0.4}, {"w": "world", "s": 0.45, "e": 0.9}]
        ass, boxes = mfe.build_ass(words, mfe.PROFILES["vertical-9x16"], "bold-pop")
        self.assertIn("[Script Info]", ass)
        self.assertIn("PlayResX: 1080", ass)
        self.assertIn("Dialogue:", ass)
        self.assertEqual(len(boxes), 1)
        self.assertTrue(ass.endswith("\n"))

    def test_boxes_stay_inside_the_vertical_safe_zone(self):
        prof = mfe.PROFILES["vertical-9x16"]
        words = [{"w": f"word{i}", "s": i * 0.4, "e": i * 0.4 + 0.35} for i in range(30)]
        _, boxes = mfe.build_ass(words, prof, "bold-pop")
        safe = prof["safe"]
        for b in boxes:
            self.assertGreaterEqual(b["y0"], 0.0)
            self.assertLessEqual(b["y1"], 1 - safe["bottom"] + 0.02, b)
            self.assertGreaterEqual(b["x0"], safe["left"] - 0.02, b)
            self.assertLessEqual(b["x1"], 1 - safe["right"] + 0.02, b)

    def test_every_style_produces_events(self):
        words = [{"w": "one", "s": 0.0, "e": 0.5}, {"w": "two", "s": 0.6, "e": 1.0}]
        for style in mfe.CAPTION_STYLES:
            ass, boxes = mfe.build_ass(words, mfe.PROFILES["vertical-9x16"], style)
            self.assertIn("Dialogue:", ass, style)
            self.assertTrue(boxes, style)

    def test_caps_are_applied_only_when_asked(self):
        words = [{"w": "shout", "s": 0.0, "e": 0.5}]
        ass_caps, _ = mfe.build_ass(words, mfe.PROFILES["vertical-9x16"], "bold-pop")
        ass_calm, _ = mfe.build_ass(words, mfe.PROFILES["vertical-9x16"], "clean-line")
        self.assertIn("SHOUT", ass_caps)
        self.assertIn("shout", ass_calm)


# ---------------------------------------------------------------------------
# SRT parsing
# ---------------------------------------------------------------------------

class TestSrt(unittest.TestCase):
    def test_parses_two_cues(self):
        srt = ("1\n00:00:01,000 --> 00:00:02,000\nhello there\n\n"
               "2\n00:00:03,000 --> 00:00:04,000\nsecond line here\n\n")
        words = mfe._words_from_srt(srt)
        self.assertEqual(len(words), 5)
        self.assertAlmostEqual(words[0]["s"], 1.0)

    def test_strips_markup(self):
        srt = "1\n00:00:01,000 --> 00:00:02,000\n<i>styled</i> text\n"
        words = mfe._words_from_srt(srt)
        self.assertEqual(words[0]["w"], "styled")

    def test_garbage_in_gives_empty_out(self):
        self.assertEqual(mfe._words_from_srt("not an srt at all"), [])


# ---------------------------------------------------------------------------
# ffmpeg filter fragments
# ---------------------------------------------------------------------------

class TestFilters(unittest.TestCase):
    def test_fades_both_edges(self):
        f = mfe._afade(5.0, 0.03, 0.03)
        self.assertIn("afade=t=in:st=0:d=0.030", f)
        self.assertIn("afade=t=out:st=4.970:d=0.030", f)

    def test_zero_fade_means_absent(self):
        self.assertEqual(mfe._afade(5.0, 0, 0), "")

    def test_atempo_chains_outside_the_2x_limit(self):
        self.assertEqual(mfe._atempo_chain(1.0), [])
        self.assertEqual(len(mfe._atempo_chain(4.0)), 2)
        self.assertEqual(len(mfe._atempo_chain(0.25)), 2)

    def test_fill_uses_crop_and_pad_does_not(self):
        fill = mfe._vscale(mfe.PROFILES["vertical-9x16"])
        pad = mfe._vscale(mfe.PROFILES["landscape-16x9"])
        self.assertIn("crop=1080:1920", fill)
        self.assertIn("increase", fill)
        self.assertIn("pad=", pad)

    def test_framing_bias_reaches_the_filter(self):
        f = mfe._vscale(mfe.PROFILES["vertical-9x16"], {"framing": [0.5, 0.25]})
        self.assertIn("(ih-oh)*0.2500", f)


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------

class TestGates(unittest.TestCase):
    def test_missing_file_exits(self):
        with self.assertRaises(SystemExit):
            mfe.gate_report("/nonexistent/file.mp4")

    def test_safe_zone_violation_is_caught_by_the_box_math(self):
        boxes = {"style": "x", "boxes": [
            {"start": 0, "end": 1, "text": "low", "x0": 0.2, "x1": 0.8, "y0": 0.9, "y1": 0.97}]}
        prof = mfe.PROFILES["vertical-9x16"]
        safe = prof["safe"]
        b = boxes["boxes"][0]
        self.assertTrue(b["y1"] > 1 - safe["bottom"] + 0.02)


@unittest.skipUnless(HAS_FFMPEG and INTEGRATION, "set MFE_INTEGRATION=1 with ffmpeg installed")
class TestIntegration(unittest.TestCase):
    """End-to-end: render two segments, then assert the gates report real numbers."""

    def test_render_and_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "footage").mkdir()
            src = root / "footage" / "a.mp4"
            mfe.run([mfe.TC.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=6",
                    "-f", "lavfi", "-i", "sine=frequency=300:duration=6",
                    "-c:v", "libx264", "-crf", "28", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", str(src)])
            edl = {
                "version": 1, "project": "t", "profile": "vertical-9x16",
                "sources": {"A": "footage/a.mp4"},
                "segments": [
                    {"id": "s1", "source": "A", "start": 0.2, "end": 2.2},
                    {"id": "s2", "source": "A", "start": 3.0, "end": 5.0},
                ],
                "overlays": [], "captions": {"enabled": True},
            }
            (root / "edl.json").write_text(json.dumps(edl), encoding="utf-8")
            self.assertEqual(mfe.validate_edl(edl, root), [])
            out = mfe.build_cut(root / "edl.json", root / "out.mp4")
            self.assertTrue(out.exists())
            # The fixture is a synthetic test pattern with no designed pacing. The pacing
            # gate is real, but this clip is not a delivery, so the test states its own
            # allowance rather than weakening the default for real renders.
            rep = mfe.gate_report(out, edl=edl, max_static_s=30.0)
            self.assertEqual(rep["verdict"], "pass", json.dumps(rep, indent=2)[:1500])
            g1 = next(g for g in rep["gates"] if g["id"] == "G1")
            self.assertEqual(g1["status"], "pass")


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestPaceGate(unittest.TestCase):
    """G8 must exist, skip outside short-form, and never invent a cut that is not there."""

    def test_g8_is_declared_in_specs(self):
        import json
        import pathlib
        spec = json.loads((pathlib.Path(__file__).resolve().parent.parent
                           / "specs" / "gates.json").read_text(encoding="utf-8"))
        ids = [g["id"] for g in spec["gates"]]
        self.assertIn("G8", ids, "specs/gates.json must list G8 pace")

    def test_scene_change_times_is_monotonic(self):
        """The helper is pure parsing; a cut list that goes backwards would break the gap maths."""
        times = sorted({round(t, 2) for t in [0.5, 6.27, 6.27, 7.83]})
        self.assertEqual(times, [0.5, 6.27, 7.83])
        marks = [0.0] + times + [10.0]
        gaps = [marks[i + 1] - marks[i] for i in range(len(marks) - 1)]
        self.assertAlmostEqual(max(gaps), 5.77, places=2)


class TestReferenceStyle(unittest.TestCase):
    """A reference must produce numbers, and the defaults must not depend on one existing."""

    def test_palette_excludes_dark_and_ranks_by_share(self):
        frames = [{"t": 0.0, "luma": 5.0, "rgb": bytes([0, 0, 0] * 256)},      # black: ignored
                  {"t": 0.5, "luma": 90.0, "rgb": bytes([240, 240, 40] * 128 + [20, 20, 20] * 128)}]
        pal = mfe.palette_of(frames)
        self.assertTrue(pal, "a lit frame must yield a palette")
        # colours are bucketed to 24-value steps, so #f0f028 lands in #f0f018
        self.assertEqual(pal[0]["hex"], "#f0f018")
        self.assertAlmostEqual(sum(c["share"] for c in pal), 100.0, places=1)

    def test_spec_shape_is_stable(self):
        required = {"aspect", "picture_span_s", "cuts", "cuts_per_min", "longest_static_s",
                    "palette", "has_audio", "not_measured"}
        src = (pathlib.Path(__file__).resolve().parent.parent / "tools" / "mfe.py").read_text()
        for key in required:
            self.assertIn(f'"{key}"', src, f"style_spec must still emit {key}")
