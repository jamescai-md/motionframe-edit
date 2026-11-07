#!/usr/bin/env python3
"""
forks.py — keep the fork network and this repository in step.

The 18 sources are real forks on the account (17 repositories; tiktok-short-edit is a
published document and cannot be forked). Each forked source is pinned into this
repository as a git submodule under `forks/`, so "combined" is literal: one repo that
references all of them at a known commit, plus the merged doctrine in `skills/` and the
rule-by-rule digests in `library/`.

    python3 tools/forks.py            # add/refresh submodule pins for every existing fork
    python3 tools/forks.py --check    # verify pins match the manifest; exit 1 on drift
    python3 tools/forks.py --pending  # list sources whose fork does not exist yet

Submodules are NOT fetched by a normal clone. That is deliberate: `git clone` stays small
and the install stays one command; `git clone --recurse-submodules` gives the full 2.6 GB
combined tree when you actually want it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "forks.json"
GITMODULES = ROOT / ".gitmodules"


def token() -> str:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""


def tip(repo: str, branch: str) -> str | None:
    url = f"https://api.github.com/repos/{repo}/commits/{branch}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "Authorization": f"Bearer {token()}"} if token()
                                 else {"Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)["sha"]
    except Exception:
        return None


def gitmodules_block(entries: list[dict]) -> str:
    out = []
    for e in entries:
        out.append(f'[submodule "forks/{e["name"]}"]\n\tpath = forks/{e["name"]}\n'
                   f'\turl = {e["fork_url"]}\n')
    return "".join(out)


def main() -> int:
    data = json.loads(MANIFEST.read_text())
    sources = data["sources"]
    forked = [s for s in sources if s["status"] == "forked"]
    pending = [s for s in sources if s["status"] == "pending-ratelimit"]

    if "--pending" in sys.argv:
        print(f"  {len(pending)} source(s) still without a fork:")
        for s in pending:
            print(f"    {s['name']:<22} {s['upstream']}")
        return 0

    for s in forked:
        s["fork_url"] = f"https://github.com/{s['fork']}.git"

    if "--check" in sys.argv:
        drift = 0
        for s in forked:
            path = ROOT / "forks" / s["name"]
            r = subprocess.run(["git", "ls-files", "-s", f"forks/{s['name']}"],
                               cwd=ROOT, capture_output=True, text=True)
            if not r.stdout.strip():
                print(f"  MISSING pin: forks/{s['name']}")
                drift += 1
        body = GITMODULES.read_text() if GITMODULES.exists() else ""
        for s in forked:
            if s["fork_url"] not in body:
                print(f"  MISSING .gitmodules entry: {s['name']}")
                drift += 1
        print(f"  {len(forked)} pins checked · {drift} problem(s) · {len(pending)} fork(s) pending")
        return 1 if drift else 0

    # write .gitmodules
    GITMODULES.write_text(gitmodules_block(forked))
    added = 0
    for s in forked:
        path = ROOT / "forks" / s["name"]
        sha = tip(s["fork"], s.get("pinned_sha") or "main") or tip(s["fork"], "master")
        if not sha:
            print(f"  SKIP {s['name']}: cannot resolve the fork's head")
            continue
        r = subprocess.run(["git", "ls-files", "-s", f"forks/{s['name']}"],
                           cwd=ROOT, capture_output=True, text=True)
        if r.stdout.strip():
            old = r.stdout.split()[1]
            if old != sha:
                subprocess.run(["git", "update-index", "--cacheinfo",
                                f"160000,{sha},forks/{s['name']}"], cwd=ROOT, check=True)
                print(f"  updated {s['name']:<20} {old[:7]} -> {sha[:7]}")
            continue
        subprocess.run(["git", "update-index", "--add", "--cacheinfo",
                        f"160000,{sha},forks/{s['name']}"], cwd=ROOT, check=True)
        print(f"  pinned  {s['name']:<20} {sha[:7]}")
        added += 1
    print(f"\n  {added} new pin(s), {len(forked)} total, {len(pending)} fork(s) still pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
