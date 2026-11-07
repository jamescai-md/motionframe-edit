# Contributing

The bar for a change is the same as the bar for a finished piece: it must make the
work measurably better, and it must not break anyone else's.

## Ground rules

1. **No paid dependencies.** No API keys, no accounts, no cloud services, no
   telemetry. A PR that introduces one is closed with a note, however good it is.
2. **Numbers over adjectives.** "Faster" is not a change; "40 ms instead of 120 ms
   for press feedback, because…" is.
3. **A rule without enforcement is a suggestion.** If you add a rule that can be
   checked, add the check. If you add a gate, prove it can fail — see
   `sv demo --selftest`.
4. **Say what you measured.** A change to a gate threshold needs the data that
   motivated it.
5. **Keep the routing table honest.** Adding a skill means updating
   `skills/supervision/SKILL.md`, the README and `AGENTS.md`.

## Before you open a PR

```bash
python3 tools/lint.py                    # frontmatter, links, hygiene
python3 -m unittest discover -s tests -v
python3 tools/sv.py demo --selftest      # pipeline + gates (needs ffmpeg)
python3 tools/sv.py doctor --json        # what your machine can prove
```

## Writing a skill

- Follow the format: `skills/<name>/SKILL.md` with frontmatter `name`,
  `description`, `license`.
- The **description is the routing interface**. Say what it does *and* when to use
  it, in the user's words. A model reads it before it reads anything else.
- Body under ~400 lines. Depth goes in `references/<topic>.md`, loaded on demand.
- Imperative voice. Second person. No "you might consider".
- Every number needs a frame rate, a resolution, or a "this is a default" note.

## Writing a gate

1. It must be able to fail. Write the failing fixture first.
2. It must name the number it judged, in `detail`.
3. It must degrade honestly when a tool is missing (`skip`, never a silent `pass`).
4. Add it to `specs/gates.json` and the table in `skills/gatekeeper/SKILL.md`.

## Attribution

If your change carries an idea across from another project, add it to
`ATTRIBUTION.md`. Credit is cheap and its absence is expensive.

## Licence

Contributions are MIT. By opening a PR you agree to license your work that way.
