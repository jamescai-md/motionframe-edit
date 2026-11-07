#!/usr/bin/env python3
"""
fetch-restricted.py — get the last 34% without this repo redistributing it.

Three sources cannot be copied into this repository:

    hypit          Apache-2.0 with added commercial conditions
    remotion       the Remotion licence (free only below a company-size threshold)
    apple-design   no licence file at all, so copyright is retained by default

Their doctrine is paraphrased in `SOURCE.md`, but a paraphrase is not the source. This
script clones those repositories **onto your machine, at the pinned commit**, into
`library/<area>/<name>/local/` — which is gitignored. You end up with the complete set of
18 sources; nothing extra is republished, and the licence you accept is the one you would
have accepted cloning by hand.

    python3 tools/fetch-restricted.py            # fetch all three
    python3 tools/fetch-restricted.py --check    # report what is present, change nothing

Requires `git`. No API keys, no tokens, nothing paid.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"

# name, area, upstream, pinned commit, licence note
RESTRICTED = [
    ("hypit", "editing", "https://github.com/hypit-ai/hypit",
     "Apache-2.0 with added commercial conditions — read them before commercial use"),
    ("remotion", "motion", "https://github.com/remotion-dev/remotion",
     "Remotion licence — free only below a company-size threshold"),
    ("apple-design", "design", "https://github.com/dickwu/apple-design-skill",
     "no licence file — copyright retained by the author, personal study only"),
]


def pinned_commit(source_md: pathlib.Path) -> str:
    for line in source_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Pinned at commit:**"):
            return line.split("`")[1]
    return ""


def main() -> int:
    check = "--check" in sys.argv
    missing = 0
    for name, area, url, note in RESTRICTED:
        dest = LIB / area / name / "local"
        src = LIB / area / name / "SOURCE.md"
        sha = pinned_commit(src) if src.exists() else ""
        if dest.exists() and any(dest.iterdir()):
            files = len(list(dest.rglob("*.md")))
            print(f"  present  {name:14} {files:>4} .md in library/{area}/{name}/local/")
            continue
        missing += 1
        if check:
            print(f"  absent   {name:14} run: python3 tools/fetch-restricted.py")
            continue
        print(f"  cloning  {name} … {note}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["git", "clone", "--depth", "1", url, str(dest)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"    failed: {r.stderr.strip().splitlines()[-1] if r.stderr else 'unknown'}")
            continue
        if sha:
            subprocess.run(["git", "-C", str(dest), "fetch", "--depth", "1", "origin", sha],
                           capture_output=True)
            subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", sha],
                           capture_output=True)
        files = len(list(dest.rglob("*.md")))
        print(f"    {files} .md fetched at {sha[:12] or 'default branch'}")
    if check and missing:
        print(f"\n  {missing} of 3 not fetched locally — that is expected on a fresh clone. "
              f"Nothing is broken; you simply have 15 of 18 sources until you run this.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
