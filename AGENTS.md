# AGENTS.md — rules for working on this repository

This repo distributes agent configuration. Follow `rules/AGENTS.md` (the ruleset this repo ships)
for general engineering conduct; the points below are specific to editing the repo itself.

## What this repo is

A personal, harness-agnostic agent setup shared publicly: one ruleset, one MCP block, a pinned skill
set, and optional model profiles. Minimal on purpose. No installer, no framework, no vendored
skills.

## Ground rules

- **Never commit secrets.** No API keys, tokens, account ids, machine paths, or employer-internal
  names. MCP entries reference environment variables (`${TAVILY_API_KEY}`), never literals.
- **Nothing machine-specific.** If a file only makes sense on one laptop, it does not belong here.
- **Verify commands before documenting them.** Every CLI invocation in the README or
  `skills/SKILLS.md` must have been run — flags are not guessed. The `skills` CLI in particular
  needs one `-s` per skill; comma lists fail silently.
- **Cite primary sources for harness paths.** Rules-file locations and MCP config shapes come from
  each harness's official docs, not from memory.

## Keep these in sync

A change in one place usually needs edits in the others:

| If you change | Also update |
| --- | --- |
| the skill set | install commands **and** the inventory table in `skills/SKILLS.md`, the skill count in `README.md`, and `skills-lock.json` |
| `rules/AGENTS.md` | any skill it names must still be in the installed set |
| `mcp/mcp-servers.json` | the per-harness table and the credentials table in `README.md` |
| the directory layout | the layout tree in `README.md` |

The skill-set rows above are enforced by CI: `python3 scripts/check_sync.py` (run by
`.github/workflows/ci.yml` on every push and PR) validates the JSON files and the skill-set sync,
and fails on anything secret-looking or machine-specific. Run it locally before pushing.

## Regenerating the lockfile

```bash
cd $(mktemp -d)
# re-run the four commands from skills/SKILLS.md with --project instead of -g
npx skills add <repo> --project -a universal -y -s <skill> -s <skill> …
cp skills-lock.json /path/to/this-repo/skills-lock.json
```

## Non-goals

- An install script. Copying four files is not worth a maintained installer.
- Vendoring skills. They stay upstream so `npx skills update -g` keeps working.
- Personal tooling: dashboards, hooks, status lines, employer-specific skills.
