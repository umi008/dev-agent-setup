# AGENTS.md — rules for working on this repository

This repo distributes agent configuration. For general engineering conduct, follow the standard this
repo ships: `standards/en/Engineering_standards.md`. The points below are specific to editing the
repo itself.

## What this repo is

A personal, harness-agnostic agent setup shared publicly: one engineering standard (bilingual), one
MCP list, one pinned skill set. Minimal on purpose. No installer, no framework, no vendored skills.

## Ground rules

- **Never commit secrets.** No API keys, tokens, account ids, machine paths, or employer-internal
  names. MCP entries reference environment variables (`${TAVILY_API_KEY}`), never literals.
- **Nothing machine-specific.** If a file only makes sense on one laptop, it does not belong here.
- **Verify commands before documenting them.** Every CLI invocation in the READMEs or
  `skills/SKILLS.md` must have been run — flags are not guessed. The `skills` CLI in particular takes
  one `-s` per skill; comma lists fail silently.
- **Cite primary sources for harness paths and config shapes.** They come from each harness's official
  docs, not from memory.
- **English is the reference.** Code, identifiers and the English copy of every document are authored
  first; the Spanish copy follows.

## Keep these in sync

A change in one place usually needs edits in the others:

| If you change | Also update |
| --- | --- |
| the standard under `standards/en/` | its Spanish copy under `standards/es/`, keeping the same structure and file names per language |
| the skill set | the install commands **and** the inventory in `skills/SKILLS.md`, and the skill count in `README.md` and `README.es.md` |
| `mcps/MCPS.md` | the MCP row in both READMEs and their credentials tables |
| the directory layout | the layout tree in `README.md` and `README.es.md` |
| anything in the root READMEs | its counterpart in the other language |

## Non-goals

- An install script. Copying a few files is not worth a maintained installer.
- Vendoring skills. They stay upstream so `npx skills update -g` keeps working.
- Personal tooling: dashboards, hooks, status lines, employer-specific skills.
- CI. This repo is documents and a license — there is nothing to build or gate.
