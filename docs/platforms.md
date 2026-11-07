# Platforms

One source of truth (`AGENTS.md` + `skills/`), many entry points. Nothing here is
duplicated per platform; the adapters are pointers, which is why they cannot drift.

| Agent | What it reads | Install |
|---|---|---|
| **Claude Code / Claude** | `skills/<name>/SKILL.md` with YAML frontmatter, discovered in `~/.claude/skills/` | `./install.sh --target claude` |
| **ChatGPT / Codex** | `AGENTS.md` at the repo root (hierarchy-walked); shared skills in `~/.codex/skills/` if your build supports them | `./install.sh --target codex` |
| **Gemini CLI** | `GEMINI.md` context file + `gemini-extension.json` | `gemini extensions link .` |
| **Antigravity** | `AGENTS.md`; skills convention `~/.gemini/antigravity/skills/` | `./install.sh --target antigravity` |
| **OpenCode** | `AGENTS.md`; skills in `${XDG_CONFIG_HOME:-~/.config}/opencode/skills/` | `./install.sh --target opencode` |
| **Hermes / Cursor / Windsurf / Zed / Aider / anything else** | `AGENTS.md` | `./install.sh --dir <your skills dir>`, or set `SV_SKILLS_DIR` |

## The three ways to mount it

**1. Skills directory (best).** The agent discovers each skill by its `description`
and loads a body only when it routes there. This is progressive disclosure, and it
is the whole reason the suite is seven skills rather than one enormous file.

```bash
./install.sh --target claude          # symlinks all seven into ~/.claude/skills
./install.sh --dir ~/my/agent/skills  # anywhere else
./install.sh --copy                   # for filesystems where symlinks fail
```

**2. Single context file (always works).** Every tool in the table can read a
markdown file. Paste or reference `AGENTS.md`, and point at the router:

```
Read AGENTS.md, then skills/supervision/SKILL.md before starting. Load other
skills from skills/<name>/SKILL.md only when the routing table says to.
```

**3. Project-local (per client, per repo).** Drop a project's `taste.md`,
`brief.md` and `edl.json` next to the footage and let the agent read those first.
This is how a one-off becomes a house style.

## Paths, honestly

Agent skill directories move as tooling matures. If your tool reads skills from a
path that is not listed above, do not edit `install.sh` — override it:

```bash
SV_SKILLS_DIR=~/.my-agent/skills ./install.sh
```

If a target prints a path that does not exist on your machine, that is expected:
the installer creates it, and the list above records the convention this repo
targets, not a guarantee about any particular build.

## What each platform gets

- **Claude Code**: the richest experience — real skills, subagents for parallel
  beats, hooks for a pre-delivery gate. `.claude-plugin/plugin.json` makes it
  installable as a plugin.
- **Codex / ChatGPT**: `AGENTS.md` plus skills where supported. Codex is strongest
  at the engine work (`sv.py`) because it can run commands in a loop and read the
  gate report.
- **Gemini CLI / Antigravity**: the extension manifest gives it `GEMINI.md` as
  context. Good at long-reference reading (`docs/lineage.md`, the lane docs).
- **OpenCode / Hermes / others**: `AGENTS.md` is the contract. Everything else is
  plain markdown, and the engine is a single stdlib file — it will work.

## The rule that keeps this portable

No skill depends on a platform feature. Subagents are an optimisation, not a
requirement: everything here can be done serially by one model with a shell. That
is deliberate, because the day a specific skill format changes, the doctrine is
still readable and the engine still runs.
