#!/usr/bin/env bash
# supervision — installer
# Links the seven skills into whichever agent(s) you have, and tells you exactly
# what it did. No network calls, no sudo, nothing written outside the paths below.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
MODE="link"
TARGETS=()
DRY=0

usage() {
  cat <<'USAGE'
supervision install

  ./install.sh [options]

  --target <name>   claude | codex | gemini | antigravity | opencode | hermes | all
                    (repeatable; default: auto-detect what is installed)
  --dir <path>      install into an explicit skills directory (repeatable)
  --copy            copy the skills instead of symlinking them
  --dry-run         print the plan, change nothing
  -h, --help        this text

  Override any destination with MFE_SKILLS_DIR for a single custom location.

  Symlinks are preferred: fixing a skill in the repo fixes it everywhere, and
  `git pull` updates every agent at once.
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target)  TARGETS+=("${2:-}"); shift 2 ;;
    --dir)     TARGETS+=("dir:${2:-}"); shift 2 ;;
    --copy)    MODE="copy"; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

skills() { find "$SKILLS_SRC" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort; }

known_dir() {
  case "$1" in
    claude)      echo "$HOME/.claude/skills" ;;
    codex)       echo "$HOME/.codex/skills" ;;
    opencode)    echo "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills" ;;
    antigravity) echo "$HOME/.gemini/antigravity/skills" ;;
    gemini)      echo "$HOME/.gemini/extensions" ;;
    hermes)      echo "$HOME/.hermes/skills" ;;
    *) return 1 ;;
  esac
}

# --- resolve destinations -----------------------------------------------------
DEST_DIRS=()
if [ ${#TARGETS[@]} -eq 0 ]; then
  for t in claude codex opencode antigravity hermes gemini; do
    d="$(known_dir "$t")" || continue
    parent="$(dirname "$d")"
    if [ -d "$parent" ] || [ -d "$d" ]; then
      DEST_DIRS+=("$t|$d")
    fi
  done
  [ ${#DEST_DIRS[@]} -eq 0 ] && DEST_DIRS+=("claude|$(known_dir claude)")
else
  for t in "${TARGETS[@]}"; do
    if [ "${t#dir:}" != "$t" ]; then
      DEST_DIRS+=("custom|${t#dir:}")
    elif [ "$t" = "all" ]; then
      for a in claude codex opencode antigravity hermes; do
        DEST_DIRS+=("$a|$(known_dir "$a")")
      done
    else
      d="$(known_dir "$t")" || { echo "unknown target: $t" >&2; exit 2; }
      DEST_DIRS+=("$t|$d")
    fi
  done
fi
if [ -n "${MFE_SKILLS_DIR:-}" ]; then
  DEST_DIRS+=("env|$MFE_SKILLS_DIR")
fi

# --- install -----------------------------------------------------------------
echo
echo "  supervision · $(skills | wc -l | tr -d ' ') skills · ${MODE}"
echo
for entry in "${DEST_DIRS[@]}"; do
  name="${entry%%|*}"; dest="${entry##*|}"
  echo "  → $name: $dest"
  if [ "$DRY" = "1" ]; then
    for s in $(skills); do echo "      would ${MODE} $s"; done
    continue
  fi
  mkdir -p "$dest"
  for s in $(skills); do
    if [ "$MODE" = "copy" ]; then
      rm -rf "${dest:?}/$s"
      cp -R "$SKILLS_SRC/$s" "$dest/$s"
    else
      ln -sfn "$SKILLS_SRC/$s" "$dest/$s"
    fi
  done
done

if [ "$DRY" = "0" ]; then
  echo
  echo "  done. Restart your agent so it re-scans its skills directory."
  echo
  echo "  verify the engine:"
  echo "    python3 \"$REPO_DIR/tools/sv.py\" doctor"
  echo "    python3 \"$REPO_DIR/tools/sv.py\" demo --selftest"
  echo
  case " ${TARGETS[*]:-} " in
    *" gemini "*|*" all "*)
      echo "  Gemini CLI extension:  (cd \"$REPO_DIR\" && gemini extensions link .)" ;;
  esac
  echo
fi
