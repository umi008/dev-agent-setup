<div align="center">

# Dev Agent Setup

**A portable, harness-agnostic configuration for AI coding agents.**

House rules · MCP servers · global skills — reproducible on any machine, in any agent.

Works with Claude Code, OpenCode, Codex CLI, Kilo Code, Cursor, Gemini CLI, Oh My Pi, and anything
else that reads an `AGENTS.md`-style rules file and speaks MCP.

[![CI](https://github.com/umi008/dev-agent-setup/actions/workflows/ci.yml/badge.svg)](https://github.com/umi008/dev-agent-setup/actions/workflows/ci.yml)

</div>

---

## What this is

This is not a product or a framework. It is **my personal working setup**, cleaned up and shared
because it may save you an afternoon. Nothing here is load-bearing for anyone but me — fork it,
delete half of it, keep the parts that fit.

The goal is one all-in-one baseline that stays sane across the whole range of real work: a
throwaway script and a million-line monorepo, a fresh repo with no context and a legacy codebase
with too much of it. That means deliberately **minimal but professional**:

- **Minimal** — one ruleset, three MCP servers, no installer, no vendored skills, no framework to
  learn. Every file has a single job and you can read all of them in ten minutes.
- **Professional** — the rules encode non-negotiables (verify before delivering, tests first, spec
  first on anything sizeable, real quality gates per language) instead of vibes.
- **Context-aware** — cheap models and small skills handle small jobs; the reasoning roles,
  spec-driven flow, and research/grilling skills only kick in when the work actually warrants them.

---

## What you get

| Piece | Purpose |
| --- | --- |
| **House rules** | One ruleset (`rules/AGENTS.md`) — communication, code, validation, per-language quality gates, TDD and spec-first workflow. Written in English; it tells the agent to reply in the user's language. |
| **MCP servers** | Context7 (live library docs), Playwright (headless browser), and Tavily (web search) in one canonical `mcpServers` block — translate it to whatever shape your harness expects. |
| **Skills** | 38 agent skills installed **globally** from upstream repos via the `skills` CLI, shared by every harness that reads `~/.agents/skills`. |
| **Model profiles** | Optional, harness-specific. `harnesses/omp/` maps agent roles (`plan`, `task`, `review`, `smol`, …) to models and thinking levels. |

## Layout

```
.
├── AGENTS.md                rules for working on this repo (not the ruleset you install)
├── LICENSE                  MIT
├── skills-lock.json         all 38 skills pinned to source + content hash
├── rules/
│   └── AGENTS.md            the ruleset — drop it wherever your harness reads rules
├── mcp/
│   └── mcp-servers.json     canonical `mcpServers` block (stdio; Tavily reads `TAVILY_API_KEY`)
├── skills/
│   └── SKILLS.md            install commands + inventory + lockfile usage
├── harnesses/
│   └── omp/                 Oh My Pi model-role profiles (baseline + two overlays)
├── scripts/
│   └── check_sync.py         consistency checks: JSON, skill-set sync, secret scan
└── .github/
    └── workflows/
        └── ci.yml            runs check_sync.py on every push and PR
```

## Prerequisites

| Tool | Why |
| --- | --- |
| Node ≥ 20 + `npx` | Runs the `skills` CLI and all three stdio MCP servers. |
| Per-language gates | `uv`, `ruff`, `mypy`, `pytest` (Python) · `pnpm`/`bun`, `biome`, `tsc`, `vitest` (JS/TS) · `cargo fmt`/`clippy` (Rust) · `gofmt`/`go vet` (Go). Install what you actually use. |

No agent harness is required by this repo — bring whichever one(s) you already use.

---

## Quick start (let an agent do it)

Clone this repo, open any coding agent inside it, and paste:

```text
Set up this machine from this repository. Do exactly the following, nothing else:

1. Detect which agent harnesses are installed on this machine (look for the `claude`, `opencode`,
   `codex`, `omp`, `gemini`, and `cursor-agent` binaries, and for ~/.claude, ~/.config/opencode,
   ~/.codex, ~/.omp, ~/.config/kilo, ~/.cursor). List what you found before changing anything.
2. For each harness found, install rules/AGENTS.md and the MCP servers following the
   "Per-harness installation" table in README.md. Skip the `tavily` MCP entry on any harness with
   native web search (e.g. Oh My Pi). Back up any file you would overwrite to <file>.bak first.
3. Install the global skills by running every command in skills/SKILLS.md verbatim, then run
   `npx skills ls -g` and show me the result.
4. Read the "Credentials" section of README.md and tell me which credentials are missing on this
   machine. Inspect the environment only: never print secret values, never write them to a file.
5. Report a summary: harnesses detected, files written, files backed up, skills installed,
   credentials missing.

Constraints: do not edit this repository, do not invent extra files, do not install language
toolchains I did not ask for, and stop to ask if a step is ambiguous for a harness you detected.
```

## Per-harness installation

Pick your harness, copy the rules file, then declare the two servers from `mcp/mcp-servers.json`
wherever that harness keeps MCP config. Everything below is user-global scope; swap in the
project-level path if you want it per repository.

| Harness | Rules file | MCP config |
| --- | --- | --- |
| **Claude Code** | `rules/AGENTS.md` → `~/.claude/CLAUDE.md` | `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp` (same for playwright), or merge `mcp/mcp-servers.json` into `~/.claude.json` |
| **OpenCode** | `rules/AGENTS.md` → `~/.config/opencode/AGENTS.md` | `mcp` key in `~/.config/opencode/opencode.json` (entries use `"type": "local"` + `"command": [...]`) |
| **Codex CLI** | `rules/AGENTS.md` → `~/.codex/AGENTS.md` | `[mcp_servers.<name>]` tables in `~/.codex/config.toml` (`command` + `args`) |
| **Kilo Code** | `rules/AGENTS.md` → `~/.config/kilo/rules/AGENTS.md`, then list it in `instructions` | `mcp` key in `~/.config/kilo/kilo.jsonc` (entries use `"type": "local"` + `"command": [...]`) |
| **Oh My Pi** | `rules/AGENTS.md` → `~/.omp/agent/RULES.md` | copy `mcp/mcp-servers.json` → `~/.omp/agent/mcp.json`, **minus the `tavily` entry** (OMP has native Tavily search — see below) |
| **Cursor** | Project scope only: `rules/AGENTS.md` → `<repo>/AGENTS.md` (Cursor reads it natively). Global rules are UI-only: Settings → Rules → User Rules — paste the file's contents there. | copy `mcp/mcp-servers.json` → `~/.cursor/mcp.json` |
| **Gemini CLI** | `rules/AGENTS.md` → `~/.gemini/GEMINI.md` | merge `mcp/mcp-servers.json` into `~/.gemini/settings.json` |
| **Anything else** | Drop `rules/AGENTS.md` in the repo root — most agents read it automatically. | Start from `mcp/mcp-servers.json`: the `mcpServers` shape is what most clients expect; check your harness's docs for its key and transport field names. |

Every server is a plain stdio process launched with `npx`, so any harness can run them — only the
surrounding JSON/TOML keys differ. If you're unsure, hand `mcp/mcp-servers.json` to your agent and
ask it to write the equivalent block for your harness.

### Tavily: drop the MCP server if your harness has native search

Some harnesses have a built-in web-search provider chain and speak to Tavily directly. Oh My Pi is
one: it reads `TAVILY_API_KEY` from the environment and ranks Tavily through
`providers.webSearchOrder` in `harnesses/omp/config.yml`, exposing it as the native `web_search`
tool. In that case **remove the `tavily` entry from your MCP config** — running both wastes context
on duplicate tools and burns two API calls for one question. Configure the harness's own provider
instead. Keep the MCP server only where search is not built in (Claude Code, Cursor, Kilo Code, …).

Note on the key: the entry uses `"TAVILY_API_KEY": "${TAVILY_API_KEY}"`. Claude Code expands
`${VAR}` in MCP config; harnesses that don't will pass the literal string, so inline the key in your
own config file (never here) or launch the harness with the variable already exported.

Example, Claude Code end to end:

```bash
cp rules/AGENTS.md ~/.claude/CLAUDE.md
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
claude mcp add --scope user playwright -- npx -y @playwright/mcp@0.0.79 --browser chromium --headless
claude mcp list
```

Example, OpenCode + Codex (rules only; add the MCP block in each harness's own config file):

```bash
cp rules/AGENTS.md ~/.config/opencode/AGENTS.md
cp rules/AGENTS.md ~/.codex/AGENTS.md
```

## Skills

Skills are **not vendored** here. They are installed globally from their upstream repos with the
[`skills`](https://skills.sh) CLI, which writes to `~/.agents/skills/` — the directory OMP, Claude
Code, and most other harnesses read:

```bash
# run the four commands in skills/SKILLS.md, then:
npx skills ls -g
npx skills update -g -y
```

For a reproducible, pinned set instead of upstream `main`, copy `skills-lock.json` into a project
and run `npx skills experimental_install`; it restores all 38 skills by source path and content
hash into that project's `.agents/skills/`.

See [`skills/SKILLS.md`](skills/SKILLS.md) for the full command set, the inventory, and how to
regenerate the lockfile.

## Model profiles (optional)

Role-to-model mapping is harness-specific, so it lives under `harnesses/`. Only Oh My Pi is shipped
today — three profiles, same roles:

| Role | `config.yml` (baseline) | `sonnet-direct.yml` | `openrouter-free.yml` |
| --- | --- | --- | --- |
| `default` | deepseek-v4.1-flash `:high` | claude-opus-5 `:medium` | deepseek-v4-flash:free `:high` |
| `plan` | deepseek-v4.1-flash `:high` | claude-opus-5 `:high` | kimi-k2.6:free `:high` |
| `task` | deepseek-v4.1-flash `:high` | claude-sonnet-5 `:medium` | qwen3-coder:free |
| `review` | deepseek-v4.1-flash `:max` | claude-opus-5 `:high` | kimi-k2.6:free `:high` |
| `designer` | deepseek-v4.1-flash `:high` | claude-opus-5 `:high` | glm-5.2:free `:high` |
| `slow` | deepseek-v4.1-flash `:max` | claude-opus-5 `:high` | kimi-k2.6:free `:high` |
| `smol` / `tiny` | deepseek-v4.1-flash `:low` | claude-sonnet-5 `:low` | glm-4.5-air:free / qwen3-4b:free |
| `vision` | deepseek-v4.1-flash `:low` | claude-sonnet-5 `:low` | nemotron-nano-12b-vl:free |
| `advisor` | deepseek-v4.1-flash `:high` | claude-sonnet-5 `:medium` | glm-4.5-air:free `:low` |

```bash
cp harnesses/omp/config.yml ~/.omp/agent/config.yml
cp harnesses/omp/sonnet-direct.yml harnesses/omp/openrouter-free.yml ~/.omp/

omp                                       # baseline
omp --config ~/.omp/sonnet-direct.yml     # Anthropic direct (OAuth)
omp --config ~/.omp/openrouter-free.yml   # free tier
```

Overlays are read once at process start — restart to switch. For hard isolation (separate auth,
sessions, caches) use `omp --profile <name> --alias <cmd>`.

The idea ports cleanly: cheap-and-fast model as the default, a reasoning model for `plan`/`review`,
a tiny model for mechanical work. Add your own harness directory and open a PR.

## Credentials

Nothing secret lives in this repo. Provide these yourself:

| Credential | How |
| --- | --- |
| **Your model provider** | Whatever your harness expects — OAuth login (`/login` in OMP, `claude` login, `codex login`) or an API key such as `ANTHROPIC_API_KEY` / `OPENROUTER_API_KEY` exported from your shell rc. |
| **Tavily** (web search) | `export TAVILY_API_KEY=...` in your shell rc. The MCP entry reads it from the environment — no key is stored in this repo. Drop the entry entirely if your harness already talks to Tavily natively (see above). |

Context7 and Playwright need no credentials.

## Notes

- **One ruleset, any language.** `rules/AGENTS.md` is written in English and instructs the agent to
  reply in the user's language, so there is nothing to localize.
- **Agent-state dashboard.** I run **herdr** to watch live agent state across sessions; its harness
  extensions and hooks are intentionally **not** in this repo (they are machine-specific).
  Recommended if you juggle several parallel agents.
- **Skills stay upstream.** `npx skills update -g` keeps them current instead of freezing a copy here.
- **CI.** `.github/workflows/ci.yml` runs `scripts/check_sync.py` on every push and PR — it validates
  every JSON file, keeps the skill set in sync across `skills-lock.json`, `skills/SKILLS.md` and the
  counts in this README, and fails if anything secret-looking or machine-specific gets committed.
  Run it locally with `python3 scripts/check_sync.py`.
- **Editing this repo?** `AGENTS.md` at the root holds the conventions (what must stay in sync, what
  never gets committed). It is not the ruleset you install — that one is `rules/AGENTS.md`.

## License

MIT — see [`LICENSE`](LICENSE). Take it, fork it, strip it down.
