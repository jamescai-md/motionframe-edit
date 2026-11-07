#!/usr/bin/env python3
"""
absorb.py — prove the combination, and generate the index from the material itself.

Every source in the brief must be present in `library/`, and its handling must match its
licence:

  copy      → `upstream/` exists, `LICENCE.upstream` travels with it, `SOURCE.md` records
              the upstream commit
  summarise → no copied text at all, only `SOURCE.md` with the paraphrase

This writes `library/README.md` and `docs/absorption.md` from the vendored tree, so the
tables cannot drift from what is actually on disk.

    python3 tools/absorb.py            # check + regenerate both indexes
    python3 tools/absorb.py --check    # verify only; exit 1 on any gap
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"

# name, area, mode, licence label, upstream
SOURCES = [
    ("i-hate-editing", "editing", "copy", "MIT", "https://github.com/ranahaani/i-hate-editing"),
    ("video-use", "editing", "copy", "MIT", "https://github.com/browser-use/video-use"),
    ("freecut", "editing", "copy", "MIT", "https://github.com/Moh4696/freecut"),
    ("herk-edit-kit", "editing", "copy", "MIT", "https://github.com/nateherkai/herk-edit-kit"),
    ("video-short", "editing", "copy", "MIT", "https://github.com/petergyang/video-short"),
    ("open-edit", "editing", "copy", "Apache-2.0", "https://github.com/veedstudio/open-edit"),
    ("tiktok-short-edit", "editing", "summarise", "published document",
     "https://www.marwieang.com/tiktok-short-edit.md"),
    ("hypit", "editing", "summarise", "modified Apache-2.0", "https://github.com/hypit-ai/hypit"),
    ("motionmaxxing", "motion", "copy", "Apache-2.0", "https://github.com/Tejashmakwana/motionmaxxing"),
    ("motion-kit", "motion", "copy", "MIT", "https://github.com/hughminhphan/motion-kit"),
    ("reelmimic", "motion", "copy", "MIT", "https://github.com/edenfunf/reelmimic"),
    ("hyperframes", "motion", "copy", "Apache-2.0", "https://github.com/heygen-com/hyperframes"),
    ("hyperframes-launches", "motion", "copy", "Apache-2.0",
     "https://github.com/heygen-com/hyperframes-launches"),
    ("remotion", "motion", "summarise", "Remotion licence", "https://github.com/remotion-dev/remotion"),
    ("taste-skill", "design", "copy", "MIT", "https://github.com/Leonxlnx/taste-skill"),
    ("ui-ux-pro-max", "design", "copy", "MIT", "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"),
    ("emil-skills", "design", "copy", "MIT", "https://github.com/emilkowalski/skills"),
    ("apple-design", "design", "summarise", "no licence file", "https://github.com/dickwu/apple-design-skill"),
]


def landed_where(source_md: pathlib.Path, notes: pathlib.Path) -> str:
    for f in (notes, source_md):
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        m = re.search(r"## Where this landed\n+(.*?)(?=\n## |\Z)", t, re.S)
        if m:
            return " ".join(m.group(1).split())[:150]
    return "—"


def main() -> int:
    check = "--check" in sys.argv
    rows, problems = [], []
    for name, area, mode, licence, upstream in SOURCES:
        d = LIB / area / name
        src = d / "SOURCE.md"
        if not src.exists():
            problems.append(f"missing library/{area}/{name}/SOURCE.md")
            continue
        files, size = 0, 0
        up = d / "upstream"
        if mode == "copy":
            if not up.exists():
                problems.append(f"library/{area}/{name}: mode is copy but there is no upstream/")
            if not (d / "LICENCE.upstream").exists():
                problems.append(f"library/{area}/{name}: no LICENCE.upstream (licence terms must travel)")
            files = len(list(up.rglob("*.md"))) if up.exists() else 0
            size = sum(p.stat().st_size for p in up.rglob("*") if p.is_file()) if up.exists() else 0
        else:
            if up.exists() and any(up.rglob("*.md")):
                problems.append(f"library/{area}/{name}: mode is summarise but text was copied")
        rows.append({"name": name, "area": area, "mode": mode, "licence": licence,
                     "upstream": upstream, "files": files, "size": size,
                     "landed": landed_where(src, d / "NOTES.md")})

    if problems:
        print("  absorption check FAILED")
        for p in problems:
            print(f"    - {p}")
        return 1
    if check:
        copied = sum(r["files"] for r in rows)
        print(f"  absorption check PASS — {len(rows)} sources · {copied} files vendored · "
              f"{len([r for r in rows if r['mode'] == 'copy'])} copied, "
              f"{len([r for r in rows if r['mode'] == 'summarise'])} summarised")
        return 0

    total_files = sum(r["files"] for r in rows)
    total_bytes = sum(r["size"] for r in rows)
    copied = [r for r in rows if r["mode"] == "copy"]
    summarised = [r for r in rows if r["mode"] == "summarise"]

    # ---- library/README.md -------------------------------------------------
    lines = [
        "# The library — eighteen sources, combined",
        "",
        "This folder is the combination. Every source in the brief is here, and how it is here",
        "depends on its licence — not on convenience:",
        "",
        "| Mode | Meaning |",
        "|---|---|",
        "| **copy** | The source's licence permits redistribution. Its skill files, rules and references are",
        "|  | copied verbatim under `upstream/`, and its LICENCE travels alongside as `LICENCE.upstream`. |",
        "| **summarise** | The licence does *not* permit redistribution. Nothing is copied; `SOURCE.md` carries a",
        "|  | paraphrase written for this project, and says so plainly. |",
        "",
        f"**{len(copied)} sources copied · {len(summarised)} summarised · "
        f"{total_files} files · {total_bytes:,} bytes.**",
        "",
        "| Source | Area | Mode | Licence | Files | Bytes |",
        "|---|---|---|---|---:|---:|",
    ]
    for r in rows:
        lines.append(f"| [{r['name']}]({r['area']}/{r['name']}/SOURCE.md) | {r['area']} | {r['mode']} "
                     f"| {r['licence']} | {r['files'] or '—'} | {r['size'] or '—'} |")
    lines += [
        "",
        "## How the skills use it",
        "",
        "`skills/` is the merge — one voice, contradictions settled. `library/` is the evidence:",
        "the source material to check that merge against, loaded only when a job needs the depth.",
        "That is progressive disclosure, and it is what lets eighteen sources fit into one install.",
        "",
        "## Editorial notes",
        "",
        "Each source folder also carries `NOTES.md` where one exists: what that source is good at,",
        "what it gets wrong, and where its rules landed in `skills/`. Notes are this project's",
        "writing, not the upstream's.",
        "",
        "## What is not here",
        "",
        "- **Assets** — themes, fonts, images, example films. Licences vary and a skill repo is not",
        "  an asset dump.",
        "- **Applications** — `open-edit`'s CLI code and `hypit`'s workflow are tools; only their",
        "  doctrine is useful here.",
        "- **Contradictions** — left as contradictions in the sources, resolved in",
        "  `../skills/supervision/references/precedence.md`, and nowhere else.",
        "",
    ]
    (LIB / "README.md").write_text("\n".join(lines), encoding="utf-8")

    # ---- docs/absorption.md ------------------------------------------------
    doc = [
        "# Absorption — where each source's material went",
        "",
        "*Generated by `tools/absorb.py` from the vendored tree. Do not edit by hand.*",
        "",
        f"**{len(rows)} sources · {len(copied)} copied verbatim · {len(summarised)} paraphrased "
        f"· {total_files} files · {total_bytes:,} bytes.**",
        "",
        "| Source | Mode | Licence | Where its doctrine is used |",
        "|---|---|---|---|",
    ]
    for r in rows:
        doc.append(f"| [{r['name']}]({r['upstream']}) | {r['mode']} | {r['licence']} | {r['landed']} |")
    doc += [
        "",
        "## Why four are paraphrased rather than copied",
        "",
        "| Source | Licence | Why nothing was copied |",
        "|---|---|---|",
        "| hypit | modified Apache-2.0 with commercial conditions | redistribution would carry terms this",
        "|  |  | project cannot accept on a user's behalf |",
        "| remotion | Remotion licence | not free for companies; shipping its text would spread a licence",
        "|  |  | trap to every user of this repo |",
        "| apple-design-skill | no licence file | no grant to redistribute |",
        "| tiktok-short-edit | published document | copyright by default; a link is honest |",
        "",
        "## What this table does not prove",
        "",
        "- **That the merge is good.** It proves the material is present and legal, not that the",
        "  curation is right. The measured argument lives in `specs/gates.json` and",
        "  `tools/gate-docs.py`.",
        "- **That nothing was lost.** Copied files are complete and diffable against upstream; the",
        "  paraphrase is a judgement, and judgements can be wrong.",
        "",
    ]
    (ROOT / "docs" / "absorption.md").write_text("\n".join(doc), encoding="utf-8")
    print(f"  wrote library/README.md and/docs/absorption.md — "
          f"{len(rows)} sources, {total_files} files, {total_bytes:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
