#!/usr/bin/env python3
"""
lint.py — repository hygiene for motionframe-edit.

Checks the things that silently rot in a skill repo:
  * frontmatter present, valid YAML-ish, and the name matches the directory
  * every description says WHEN to use it (that is how a model routes)
  * descriptions are within the practical budget
  * every relative link inside a skill resolves
  * no absolute local paths, no secrets, no paid-API instructions
  * required prose sections exist in the router
  * reference files are long enough to be useful and short enough to load

Exit code 1 on any error. Warnings do not fail the build.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MAX_DESC = 1024
MIN_REF_LINES = 20
MAX_SKILL_LINES = 400

# Phrases that mean we are about to depend on something paid.
PAID_PATTERNS = [
    (r"ELEVENLABS_API_KEY", "paid API key"),
    (r"OPENAI_API_KEY", "paid API key"),
    (r"ANTHROPIC_API_KEY", "paid API key"),
    (r"GEMINI_API_KEY", "paid API key"),
    (r"REPLICATE_API_TOKEN", "paid API key"),
    (r"HEYGEN_API_KEY", "paid API key"),
    (r"RUNWAY_API_SECRET", "paid API key"),
    (r"\bsk-[A-Za-z0-9]{16,}", "hardcoded key"),
    (r"aws_secret_access_key", "credential"),
]

errors: list[str] = []
warnings: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"{where}: {msg}")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    data: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            data[key] = val
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def check_skill(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    fm = parse_frontmatter(text)
    if fm is None:
        err(rel, "missing YAML frontmatter")
        return
    for key in ("name", "description"):
        if key not in fm or not fm[key]:
            err(rel, f"frontmatter missing `{key}`")
    name = fm.get("name", "").strip().strip('"').strip("'")
    if name:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            err(rel, f"name `{name}` must be lowercase-hyphenated")
        if name != path.parent.name:
            warn(rel, f"name `{name}` does not match directory `{path.parent.name}`")
    desc = fm.get("description", "")
    if len(desc) > MAX_DESC:
        err(rel, f"description is {len(desc)} chars (max {MAX_DESC})")
    low = desc.lower()
    if not any(k in low for k in ("use when", "use for", "use whenever", "use on")):
        warn(rel, "description does not say WHEN to use the skill — routing will suffer")
    if len(desc) < 80:
        warn(rel, "description is very short; a model cannot route on it")
    if len(lines) > MAX_SKILL_LINES:
        warn(rel, f"{len(lines)} lines — consider splitting into references/")
    if "license:" not in text[:600]:
        warn(rel, "no `license` in frontmatter")

    # links resolve
    for m in re.finditer(r"\]\(([^)#][^)]*)\)", text):
        target = m.group(1).split("#")[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).resolve().exists():
            err(rel, f"broken relative link: {target}")

    # references are loadable
    refdir = path.parent / "references"
    if refdir.is_dir():
        for r in sorted(refdir.glob("*.md")):
            n = len(r.read_text(encoding="utf-8").splitlines())
            if n < MIN_REF_LINES:
                warn(f"{rel} → {r.name}", f"{n} lines; is it worth a file?")
    # every referenced file is mentioned from the SKILL.md
    for r in sorted(path.parent.glob("references/*.md")):
        if r.name not in text:
            warn(rel, f"reference `{r.name}` is never mentioned from SKILL.md")

    # hygiene
    for pat, why in PAID_PATTERNS:
        if re.search(pat, text):
            if re.search(rf"(never|no|not|without|ignore|refuse)[^.\n]{{0,60}}{pat}", text):
                continue
            err(rel, f"contains {why} pattern `{pat}`")


def check_all_markdown() -> None:
    for p in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "node_modules", ".mfe-demo"} for part in p.parts):
            continue
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        if re.search(r"/(home|Users)/[a-z0-9_.-]+/", text):
            warn(rel, "contains an absolute local path")
        if "\t" in text:
            warn(rel, "contains a literal tab (breaks some renderers)")
        for m in re.finditer(r"\]\(([^)#][^)]*)\)", text):
            t = m.group(1).split("#")[0].strip()
            if not t or t.startswith(("http://", "https://", "mailto:")):
                continue
            if not (p.parent / t).resolve().exists():
                err(rel, f"broken link: {t}")


def check_required(rel: str, needles: list[str]) -> None:
    p = ROOT / rel
    if not p.exists():
        err(rel, "missing")
        return
    text = p.read_text(encoding="utf-8")
    for n in needles:
        if n.lower() not in text.lower():
            err(rel, f"missing required content: `{n}`")


def main() -> int:
    if not SKILLS.is_dir():
        print("no skills/ directory", file=sys.stderr)
        return 2

    skill_dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir())
    for d in skill_dirs:
        skill = d / "SKILL.md"
        if not skill.exists():
            err(d.name, "no SKILL.md")
            continue
        check_skill(skill)

    check_all_markdown()

    check_required("skills/motionframe-edit/SKILL.md",
                   ["twelve laws", "route", "gatekeeper", "no api key"])
    check_required("skills/gatekeeper/SKILL.md", ["G0", "G7", "fix order"])
    check_required("skills/edit-supervisor/SKILL.md", ["output", "captions", "LUFS"])
    check_required("skills/motion-director/SKILL.md", ["beat", "easing", "lane"])
    check_required("skills/design-director/SKILL.md", ["kind", "token", "anti-slop"])
    check_required("skills/ui-motion/SKILL.md", ["should it animate", "reduced motion"])
    check_required("skills/taste-memory/SKILL.md", ["taste.md", "append"])
    check_required("AGENTS.md", ["non-negotiable", "doctor"])
    check_required("README.md", ["gates", "install", "licence"])

    for f in ("LICENSE", "ATTRIBUTION.md", "CHANGELOG.md", "CONTRIBUTING.md",
              "specs/edl.schema.json", "tools/mfe.py", "install.sh"):
        if not (ROOT / f).exists():
            err(f, "missing")

    print(f"\n  motionframe-edit lint — {len(skill_dirs)} skills, {len(list(ROOT.rglob('*.md')))} markdown files\n")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")
    if not errors:
        print(f"  PASS  clean{' (%d warnings)' % len(warnings) if warnings else ''}\n")
        return 0
    print(f"\n  {len(errors)} error(s)\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
