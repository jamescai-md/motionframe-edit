#!/usr/bin/env python3
"""
vendor.py — copy the source doctrine into library/, legally and reproducibly.

The brief was to take eighteen editing, motion and design skill repositories and combine
them into one. "Fork" in GitHub's sense cannot do that: a fork is one repository, 1:1. So
the material is copied here instead — with the licence of each source respected:

  copy      the source's permissive licence allows redistribution. Everything doctrine-
            bearing is copied verbatim, its LICENCE travels with it, and SOURCE.md records
            the upstream commit so the copy is verifiable.
  summarise the licence does not allow redistribution (modified Apache, vendor licence, or
            no licence at all). Nothing is copied; a paraphrase written for this project is
            included instead, and SOURCE.md says exactly why.

    python3 tools/vendor.py                 # populate library/ from ../.cache/src
    python3 tools/vendor.py --check         # verify every vendored source is present + licensed
    python3 tools/vendor.py --source-dir X  # where the upstream clones live

Nothing proprietary is invented about a source: if it is not verifiable in the clone, it is
not written in SOURCE.md.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
DEFAULT_SRC = ROOT.parent / ".cache" / "src"

# Files that are never doctrine: assets, translations, tooling, tests, packaging.
EXCLUDE_PARTS = {
    "node_modules", ".git", "i18n", "translations", "assets", "themes", "public",
    "static", "dist", "build", "coverage", "test", "tests", "__tests__", "spec",
    "packages", "examples", "benchmarks", ".github", ".vscode", ".idea",
}
EXCLUDE_NAMES = {
    "CHANGELOG.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "tsconfig.json",
}
DOCTRINE_HINT = ("skill.md", "rules", "reference", "guide", "handoff", "frame.md", "blueprints")

# name, area, mode, upstream, licence label
SOURCES = [
    ("i-hate-editing", "editing", "copy", "https://github.com/ranahaani/i-hate-editing", "MIT"),
    ("video-use", "editing", "copy", "https://github.com/browser-use/video-use", "MIT"),
    ("freecut", "editing", "copy", "https://github.com/Moh4696/freecut", "MIT"),
    ("herk-edit-kit", "editing", "copy", "https://github.com/nateherkai/herk-edit-kit", "MIT"),
    ("video-short", "editing", "copy", "https://github.com/petergyang/video-short", "MIT"),
    ("open-edit", "editing", "copy", "https://github.com/veedstudio/open-edit", "Apache-2.0"),
    ("hypit", "editing", "summarise", "https://github.com/hypit-ai/hypit",
     "modified Apache-2.0 (commercial conditions)"),
    ("motionmaxxing", "motion", "copy", "https://github.com/Tejashmakwana/motionmaxxing", "Apache-2.0"),
    ("motion-kit", "motion", "copy", "https://github.com/hughminhphan/motion-kit", "MIT"),
    ("reelmimic", "motion", "copy", "https://github.com/edenfunf/reelmimic", "MIT"),
    ("hyperframes", "motion", "copy", "https://github.com/heygen-com/hyperframes", "Apache-2.0"),
    ("hyperframes-launches", "motion", "copy", "https://github.com/heygen-com/hyperframes-launches", "Apache-2.0"),
    ("remotion", "motion", "summarise", "https://github.com/remotion-dev/remotion",
     "Remotion licence (not free for companies)"),
    ("taste-skill", "design", "copy", "https://github.com/Leonxlnx/taste-skill", "MIT"),
    ("ui-ux-pro-max", "design", "copy", "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill", "MIT"),
    ("emil-skills", "design", "copy", "https://github.com/emilkowalski/skills", "MIT"),
    ("apple-design", "design", "summarise", "https://github.com/dickwu/apple-design-skill", "no licence file"),
    ("tiktok-short-edit", "editing", "summarise", "https://www.marwieang.com/tiktok-short-edit.md",
     "published document (all rights reserved by default)"),
]


def commit_of(d: pathlib.Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()[:12]
    except Exception:
        return "unknown"


def find_licence(d: pathlib.Path) -> pathlib.Path | None:
    for f in d.iterdir():
        if f.is_file() and f.name.lower().startswith(("license", "licence", "copying")):
            return f
    return None


def doctrine_files(d: pathlib.Path) -> list[pathlib.Path]:
    out = []
    for p in d.rglob("*.md"):
        if not p.is_file():
            continue
        parts = {x.lower() for x in p.parts}
        if parts & EXCLUDE_PARTS or p.name in EXCLUDE_NAMES:
            continue
        rel = str(p).lower()
        if any(h in rel for h in DOCTRINE_HINT):
            out.append(p)
    return sorted(out)


def write_source_md(dest: pathlib.Path, name: str, mode: str, upstream: str, licence: str,
                    sha: str, files: list[pathlib.Path], excluded_note: str) -> None:
    body = [f"# {name}", "",
            f"**Upstream:** {upstream}  ",
            f"**Licence:** {licence}  ",
            f"**Pinned at commit:** `{sha}`  ",
            f"**Mode:** {mode}  ",
            f"**Doctrine files:** {len(files)}  ",
            f"**Bytes:** {sum(f.stat().st_size for f in files):,}", ""]
    if mode == "copy":
        body += [
            "## What this is",
            "",
            "The source's doctrine, copied verbatim under its own licence. Its LICENCE file",
            "travels with it as `LICENCE.upstream`, so the terms are in the same folder as the",
            "text they cover.",
            "",
            "## What was taken",
            "",
            "Skill definitions, rule files, references and guides — the material that changes a",
            "decision. Each file keeps its original relative path so it can be diffed against",
            "upstream.",
            "",
            "## What was left out",
            "",
            excluded_note,
            "",
            "## How it is used here",
            "",
            "`skills/` routes to it. Nothing in this folder is edited by this project: it is",
            "reference material, loaded on demand, so the merged doctrine in `skills/` can always",
            "be checked against the sources it came from.",
            "",
        ]
    else:
        body += [
            "## Why nothing was copied",
            "",
            f"The licence ({licence}) does not permit redistribution, so no text, code or asset",
            "from this source is included. What follows is a summary written for this project:",
            "the ideas, in this project's words, which is what copyright does not cover.",
            "",
            "If you want the source itself, use the upstream link above. If its terms suit you",
            "better than these notes, that is a legitimate reason to go there — the point of this",
            "repository is not to stop you reading the originals.",
            "",
            "## Summary used by this project",
            "",
        ]
        notes = ROOT / "library" / "_summaries" / f"{name}.md"
        if notes.exists():
            body.append(notes.read_text(encoding="utf-8").strip())
        else:
            body.append("*No summary on file yet.*")
        body.append("")
    (dest / "SOURCE.md").write_text("\n".join(body), encoding="utf-8")


def main() -> int:
    src_root = DEFAULT_SRC
    if "--source-dir" in sys.argv:
        src_root = pathlib.Path(sys.argv[sys.argv.index("--source-dir") + 1])
    check = "--check" in sys.argv

    rows, problems = [], []
    for name, area, mode, upstream, licence in SOURCES:
        dest = LIB / area / name
        if check:
            if not (dest / "SOURCE.md").exists():
                problems.append(f"missing: library/{area}/{name}/SOURCE.md")
            elif mode == "copy" and not (dest / "LICENCE.upstream").exists():
                problems.append(f"missing licence: library/{area}/{name}/LICENCE.upstream")
            continue

        d = src_root / name
        if mode == "copy":
            if not d.exists():
                problems.append(f"source clone not found: {d}")
                continue
            files = doctrine_files(d)
            kept, total = [], 0
            for f in files:
                if total + f.stat().st_size > 3_500_000:      # per-source ceiling
                    continue
                kept.append(f); total += f.stat().st_size
            dest.mkdir(parents=True, exist_ok=True)
            for f in kept:
                rel = f.relative_to(d)
                target = dest / "upstream" / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
            lic = find_licence(d)
            if lic:
                shutil.copy2(lic, dest / "LICENCE.upstream")
            else:
                problems.append(f"no licence file found for {name} — refusing to copy")
                shutil.rmtree(dest); continue
            excluded = ("Assets, translations, examples, tests, packaging and tooling files. "
                        f"Skipped {len(files) - len(kept)} file(s) beyond the per-source ceiling.")
            write_source_md(dest, name, mode, upstream, licence, commit_of(d), kept, excluded)
            rows.append((name, area, mode, len(kept), total))
        else:
            dest.mkdir(parents=True, exist_ok=True)
            write_source_md(dest, name, mode, upstream, licence, commit_of(d) if d.exists() else "n/a", [], "")
            rows.append((name, area, mode, 0, 0))

    if check:
        if problems:
            print("  vendor check FAILED")
            for p in problems: print(f"    - {p}")
            return 1
        print(f"  vendor check PASS — {len(SOURCES)} sources, every copy carries its licence")
        return 0

    print(f"  {'source':<22} {'area':<8} {'mode':<10} {'files':>6} {'bytes':>10}")
    for name, area, mode, n, b in rows:
        print(f"  {name:<22} {area:<8} {mode:<10} {n:>6} {b:>10,}")
    if problems:
        print("\n  problems:")
        for p in problems: print(f"    - {p}")
    print(f"\n  {sum(r[3] for r in rows)} doctrine files copied · "
          f"{sum(r[4] for r in rows):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
