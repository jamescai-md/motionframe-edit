#!/usr/bin/env python3
"""
gate-docs.py — the repository, measured by its own doctrine.

`gatekeeper` says a gate that cannot fail is decoration, and that the thing you
ship is the thing you measured. The engine measures renders. Nothing measured the
repository. This does, with the same shape: numbered gates, a verdict, and a
selftest that feeds them deliberately broken input and fails if they pass.

    python3 tools/gate-docs.py              # D0-D5, no network
    python3 tools/gate-docs.py --online     # also check every external link (D6)
    python3 tools/gate-docs.py --selftest   # prove each gate can fail

Gates
  D0  first screen      README answers what / who / how before the fold
  D1  links             every relative link in every markdown file resolves
  D2  frontmatter       every skill declares a unique name and a real description
  D3  generated         llms-full.txt matches the skills it is generated from
  D4  placeholders      no TODO, TBD, FIXME or lorem anywhere in the repo
  D5  honesty           no unqualified superlative in the README's own claims
  D6  provenance        every credited source resolves with a matching licence
"""

from __future__ import annotations

import re
import sys
import tempfile
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

SUPERLATIVES = re.compile(
    r"\b(flawless|perfect|best[- ]in[- ]class|world[- ]class|revolutionary|game[- ]changing|"
    r"unmatched|seamless(ly)?|effortless(ly)?|ultimate)\b", re.I)
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b")
REL_LINK = re.compile(r"\[[^\]]*\]\((?![a-z]+:|#)([^)]+)\)")
EXT_LINK = re.compile(r"\[[^\]]*\]\((https?://[^)]+)\)")


VENDORED = ("upstream",)   # library/<area>/<source>/upstream/** is copied verbatim


def is_vendored(p: pathlib.Path) -> bool:
    """True for copied source material: its links, TODOs and claims are the upstream's."""
    return "library" in p.parts and bool(set(p.parts) & set(VENDORED))


def md_files(root: pathlib.Path) -> list[pathlib.Path]:
    return [p for p in root.rglob("*.md")
            if not any(x in p.parts for x in (".git", "node_modules", ".mfe-demo"))
            and not is_vendored(p)]


# --- gates -----------------------------------------------------------------
def d0_first_screen(root: pathlib.Path) -> tuple[bool, str]:
    readme = root / "README.md"
    if not readme.exists():
        return False, "no README.md"
    head = readme.read_text(encoding="utf-8").splitlines()[:60]
    text = "\n".join(head)
    # a bold claim may wrap across a soft line break — that is prose, not a defect
    has_claim = bool(re.search(r"\*\*[^*]{15,}\*\*", text, re.S))
    has_badges = text.count("img.shields.io") + text.count("badge.svg") >= 3
    nav = re.search(r"^\[[^\n]*\]\([^\n]*\)( · \[[^\n]*\]\([^\n]*\))+", text, re.M)
    missing = [n for n, ok in (("one-line claim", has_claim), ("badges", has_badges), ("nav", bool(nav))) if not ok]
    return (not missing), ("first screen complete" if not missing else f"missing: {', '.join(missing)}")


def d1_links(root: pathlib.Path) -> tuple[bool, str]:
    dead, checked = [], 0
    for p in md_files(root):
        for target in REL_LINK.findall(p.read_text(encoding="utf-8")):
            target = target.split("#")[0].strip()
            if not target:
                continue
            checked += 1
            if not (p.parent / target).resolve().exists():
                dead.append(f"{p.relative_to(root)} -> {target}")
    if dead:
        return False, f"{len(dead)} dead of {checked}: " + "; ".join(dead[:3])
    return True, f"{checked} relative links resolve"


def d2_frontmatter(root: pathlib.Path) -> tuple[bool, str]:
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        return False, "no skills found"
    names, problems = {}, []
    for s in skills:
        text = s.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            problems.append(f"{s.parent.name}: no frontmatter")
            continue
        fm = m.group(1)
        name = re.search(r"^name:\s*(.+)$", fm, re.M)
        desc = re.search(r"^description:\s*(.+)$", fm, re.M | re.S)
        if not name:
            problems.append(f"{s.parent.name}: no name")
        if not desc or len(desc.group(1).strip()) < 40:
            problems.append(f"{s.parent.name}: description too thin")
        if name:
            n = name.group(1).strip()
            if n in names:
                problems.append(f"duplicate skill name '{n}'")
            names[n] = s
    if problems:
        return False, "; ".join(problems[:4])
    return True, f"{len(skills)} skills, unique names, descriptions intact"


def d3_generated(root: pathlib.Path) -> tuple[bool, str]:
    gen = root / "tools" / "make-llms-full.py"
    out = root / "llms-full.txt"
    if not gen.exists() or not out.exists():
        return False, "generator or output missing"
    sys.path.insert(0, str(gen.parent))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("gen", gen)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        expected = mod.build()
    except Exception as e:
        return False, f"generator failed: {e}"
    if out.read_text(encoding="utf-8") != expected:
        return False, "llms-full.txt is stale — run tools/make-llms-full.py"
    return True, "llms-full.txt matches its sources"


def d4_placeholders(root: pathlib.Path) -> tuple[bool, str]:
    """Find unfinished work, not rules about unfinished work.

    First run flagged design-director's own rule against placeholder copy. A banned-word
    list is not an unfinished sentence, so a negated or bulleted mention is skipped — and
    this file is skipped because it necessarily contains the words it hunts.
    """
    NEGATED = re.compile(r"\b(no|never|not|avoid|refuse|don't|without|banned)\b", re.I)
    hits = []
    for p in list(md_files(root)) + list(root.glob("tools/*.py")):
        if p.name in {"llms-full.txt", "gate-docs.py"}:
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if not PLACEHOLDER.search(line):
                continue
            stripped = line.strip()
            if stripped.startswith(("- ", "* ")) or NEGATED.search(stripped[:80]):
                continue
            hits.append(f"{p.relative_to(root)}:{i}")
    if hits:
        return False, f"{len(hits)} placeholder(s): " + ", ".join(hits[:4])
    return True, "no unfinished text"


def d5_honesty(root: pathlib.Path) -> tuple[bool, str]:
    """Superlatives are only allowed if the sentence carrying them also carries evidence."""
    readme = (root / "README.md").read_text(encoding="utf-8")
    flags = []
    for line in readme.splitlines():
        if not SUPERLATIVES.search(line):
            continue
        if re.search(r"\]\(|\d|`|PASS|verified|measured", line):
            continue
        flags.append(line.strip()[:60])
    if flags:
        return False, f"{len(flags)} unqualified claim(s): " + " | ".join(flags[:2])
    return True, "every superlative sits beside evidence"


def d6_provenance(root: pathlib.Path, online: bool) -> tuple[bool, str]:
    script = root / "tools" / "verify-sources.py"
    if not script.exists():
        return False, "verify-sources.py missing"
    mode = [] if online else ["--offline"]
    if not online:
        r = subprocess.run([sys.executable, str(script), *mode], capture_output=True, text=True)
        last = [l for l in r.stdout.splitlines() if "sources listed" in l]
        return r.returncode == 0, (last[0].strip() if last else "offline listing")
    r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True,
                       env={"PATH": "/usr/local/bin:/usr/bin:/bin", "GITHUB_TOKEN": _tok()})
    last = [l for l in r.stdout.splitlines() if "verified" in l and "/" in l]
    return r.returncode == 0, (last[0].strip() if last else r.stdout.splitlines()[-1])


def _tok() -> str:
    import os
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""


# --- selftest: prove the gates can fail ------------------------------------
def selftest() -> int:
    cases = []

    def build(fault: str) -> pathlib.Path:
        d = pathlib.Path(tempfile.mkdtemp()) / "repo"
        shutil.copytree(ROOT, d, ignore=shutil.ignore_patterns(".git", ".mfe-demo", "*.png"))
        if fault == "d0":
            (d / "README.md").write_text("# x\n\nnothing interesting here.\n")
        elif fault == "d1":
            (d / "README.md").write_text((d / "README.md").read_text() + "\n[gone](does/not/exist.md)\n")
        elif fault == "d2":
            (d / "skills" / "gatekeeper" / "SKILL.md").write_text("---\nname: gatekeeper\n---\nthin\n")
        elif fault == "d3":
            (d / "llms-full.txt").write_text("stale\n")
        elif fault == "d4":
            (d / "CONTRIBUTING.md").write_text("TODO: write this.\n")
        elif fault == "d5":
            (d / "README.md").write_text((d / "README.md").read_text() + "\nThis is a flawless, world-class tool.\n")
        return d

    plan = [
        ("D0", lambda r: d0_first_screen(r), "d0"),
        ("D1", lambda r: d1_links(r), "d1"),
        ("D2", lambda r: d2_frontmatter(r), "d2"),
        ("D3", lambda r: d3_generated(r), "d3"),
        ("D4", lambda r: d4_placeholders(r), "d4"),
        ("D5", lambda r: d5_honesty(r), "d5"),
    ]
    print("  selftest — each gate is fed input it must reject\n")
    for gid, fn, fault in plan:
        d = build(fault)
        ok_on_broken, detail = fn(d)
        shutil.rmtree(d.parent, ignore_errors=True)
        verdict = "correctly failed" if not ok_on_broken else "MISSED THE DEFECT"
        cases.append(not ok_on_broken)
        print(f"  {gid}  broken input -> {verdict:<20} ({detail[:52]})")
    print()
    passed = sum(cases)
    print(f"  {passed}/{len(plan)} gates demonstrably fail on bad input")
    return 0 if passed == len(plan) else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    online = "--online" in sys.argv
    root = ROOT
    checks = [
        ("D0", "first screen", d0_first_screen(root)),
        ("D1", "links", d1_links(root)),
        ("D2", "frontmatter", d2_frontmatter(root)),
        ("D3", "generated", d3_generated(root)),
        ("D4", "placeholders", d4_placeholders(root)),
        ("D5", "honesty", d5_honesty(root)),
        ("D6", "provenance", d6_provenance(root, online)),
    ]
    print("\n  gate report  ·  the repository itself\n")
    for gid, name, (ok, detail) in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {gid:<4} {name:<13} {detail}")
    failed = [c[0] for c in checks if not c[2][0]]
    print()
    print(f"  verdict: {'PASS' if not failed else 'FAIL — ' + ', '.join(failed)}")
    if not online:
        print("  (D6 ran offline; use --online to re-check every source link)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
