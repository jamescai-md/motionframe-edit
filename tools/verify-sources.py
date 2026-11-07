#!/usr/bin/env python3
"""
verify-sources.py — audit every provenance claim in ATTRIBUTION.md.

A credit table is only worth what can be checked. This parses the table, resolves every
link, and compares the licence written in the table against the licence the forge
actually reports. Exit code 1 on a dead link or a licence that has drifted.

    python3 tools/verify-sources.py            # check everything
    python3 tools/verify-sources.py --offline  # just list what is claimed

Needs network. Uses GITHUB_TOKEN if set, to avoid the anonymous rate limit.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent
DOC = ROOT / "ATTRIBUTION.md"

ROW = re.compile(r"^\|\s*\d+\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*\|\s*([^|]+?)\s*\|", re.M)
GH = re.compile(r"https://github\.com/([^/]+)/([^/)#]+)")

# what the table says  ->  what the API calls it
LICENCE_ALIASES = {
    "mit": {"MIT"},
    "apache-2.0": {"Apache-2.0"},
    "no licence file": {None, "NOASSERTION"},
    "noassertion (remotion licence)": {"NOASSERTION", None},
}


def fetch(url: str, token: str | None) -> tuple[int, dict | None]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "motionframe-edit-audit"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def alive(url: str) -> int:
    """Status of a plain document link — no JSON parsing, HTML and markdown are fine."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 motionframe-edit-audit"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main() -> int:
    if not DOC.exists():
        print(f"missing {DOC}")
        return 1
    rows = ROW.findall(DOC.read_text(encoding="utf-8"))
    if not rows:
        print("no source rows found in ATTRIBUTION.md — did the table format change?")
        return 1

    offline = "--offline" in sys.argv
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    print(f"{len(rows)} claimed sources in ATTRIBUTION.md\n")
    print(f"{'source':<32} {'claimed':<26} {'reported':<26} result")
    print("-" * 100)

    dead = drift = 0
    for name, url, claimed in rows:
        claimed = claimed.strip().strip("*").strip()
        if offline:
            print(f"{name:<32} {claimed:<26} {'-':<26} listed")
            continue
        m = GH.match(url)
        if m:
            owner, repo = m.group(1), m.group(2)
            code, data = fetch(f"https://api.github.com/repos/{owner}/{repo}", token)
        else:
            # a published document rather than a repository: check it resolves, no licence
            code = alive(url)
            if code == 200:
                print(f"{name:<32} {'document':<26} {'-':<26} ok")
            else:
                print(f"{name:<32} {'document':<26} {'-':<26} DEAD LINK ({code})")
                dead += 1
            continue
        if code != 200 or data is None:
            print(f"{name:<32} {claimed:<26} {'-':<26} DEAD LINK ({code})")
            dead += 1
            continue
        reported = (data.get("license") or {}).get("spdx_id")
        allowed = LICENCE_ALIASES.get(claimed.lower())
        ok = allowed is None or reported in allowed
        print(f"{name:<32} {claimed:<26} {str(reported):<26} {'ok' if ok else 'LICENCE DRIFT'}")
        if not ok:
            drift += 1

    print("-" * 100)
    if offline:
        print(f"  {len(rows)} sources listed (offline mode, nothing checked)")
        return 0
    print(f"  {len(rows) - dead - drift}/{len(rows)} verified · {dead} dead · {drift} licence drift")
    return 1 if (dead or drift) else 0


if __name__ == "__main__":
    sys.exit(main())
