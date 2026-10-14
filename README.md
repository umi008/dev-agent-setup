<div align="center">

# Dev Agent Setup

**A portable, harness-agnostic baseline for AI coding agents.**

One engineering standard · one MCP list · one pinned skill set.

Built to run alongside [Gentle AI](https://github.com/Gentleman-Programming/gentle-ai), the harness
layer I use — which is also where Context7 and Engram come from.

Works with **Pi** and **Claude Code** (the pair I recommend), OpenCode, Codex, Antigravity, Kilo Code,
Cursor, Gemini CLI, Oh My Pi, and anything else that reads an `AGENTS.md`-style rules file and speaks
MCP.

[English](README.md) · [Español](README.es.md)

</div>

---

## What this is

Not a product and not a framework. It is **my personal working setup**, cleaned up and shared because
it may save you an afternoon. Nothing here is load-bearing for anyone but me — fork it, delete half of
it, keep the parts that fit.

Minimal on purpose: three documents, no installer, no vendored skills, no framework to learn. You can
read the whole thing in ten minutes.

## What you get

| Piece | What it is | Where |
| --- | --- | --- |
| **Engineering standard** | One short, enforceable standard — versions, gates, tests, structure, observability, docs — with adoption prompts and the config for every gate. Written for coding agents, so the rules are backed by gates that fail, not by prose. | [`standards/`](standards/README.md) |
| **MCP servers** | The MCP servers I run and what each one is for: Tavily, Playwright, Context7, Engram — with Exa and Firecrawl as drop-in alternatives to Tavily. | [`mcps/MCPS.md`](mcps/MCPS.md) |
| **Skills** | 11 agent skills, installed globally from their upstream repos with the `skills` CLI and shared by every harness that reads `~/.agents/skills`. | [`skills/SKILLS.md`](skills/SKILLS.md) |

## Used with Gentle AI

This repo is one half of the setup; [**Gentle AI**](https://github.com/Gentleman-Programming/gentle-ai)
is the other. Gentle AI is the harness layer over [Pi](https://pi.dev): it plans, delegates to focused
subagents, reviews its own changes, and ships its own skills on top of the eleven listed below. Into
Pi it goes with `pi install npm:gentle-pi`.

It is also where **Context7** and **Engram** come from — that is why `mcps/MCPS.md` lists them without
asking you to configure them by hand.

The two are independent. Everything here is plain documents, so you can take the standard, the MCP list
and the skills and skip Gentle AI entirely.

## Layout

```
.
├── README.md               this file (en)
├── README.es.md            this file (es)
├── AGENTS.md               rules for working on this repo (not the standard you install)
├── LICENSE                 MIT
├── standards/
│   ├── README.md           the standard, index (en)
│   ├── README.es.md        the standard, index (es)
│   ├── en/
│   │   ├── Engineering_standards.md
│   │   ├── adopt.md
│   │   └── examples/       AGENTS.md, README.md, an ADR, gate config, CI
│   └── es/                 the same, in Spanish
├── mcps/
│   └── MCPS.md             the MCP servers I run
└── skills/
    └── SKILLS.md           install commands and inventory
```

## How to use it

### 1. The engineering standard

Copy `standards/en/Engineering_standards.md` into your repo (root or `docs/`) and hand your coding
agent the matching prompt from `standards/en/adopt.md`: it configures the gates for Python (uv) or
Node/React (pnpm) and creates a short `README.md` and `AGENTS.md`. An existing repo gets a read-only
audit first, then a retrofit with one commit per step.

Start at [`standards/README.md`](standards/README.md).

### 2. MCP servers

[`mcps/MCPS.md`](mcps/MCPS.md) lists the servers and the canonical `mcpServers` block. Translate it to
whatever shape your harness expects: every server is a plain `npx` stdio process, so only the JSON and
TOML keys differ.

### 3. Skills

Skills are **not vendored** here. They are installed globally from their upstream repos with the
[`skills`](https://skills.sh) CLI, which writes to `~/.agents/skills/` — the directory OMP, Claude
Code and most other harnesses read:

```bash
# run the two commands in skills/SKILLS.md, then:
npx skills ls -g
npx skills update -g -y
```

See [`skills/SKILLS.md`](skills/SKILLS.md) for the command set and the inventory.

### Quick start (let an agent do it)

Open any coding agent — in any directory — and paste:

```text
Set up this machine from https://github.com/umi008/dev-agent-setup (read its files over the network;
raw.githubusercontent.com works well). Do exactly this:

1. Install the global skills by running every command in skills/SKILLS.md verbatim, then run
   `npx skills ls -g` and show me the result.
2. Read mcps/MCPS.md and tell me, for each server, how to declare it in the harness I am using.
   Inspect the environment only: never print secret values, never write them to a file.
3. Report what you installed and what I still have to configure by hand.

Constraints: use the published files as-is — do not modify the repository, do not invent extra files.
```

## Credentials

Nothing secret lives in this repo. Provide these yourself:

| Credential | How |
| --- | --- |
| **Your model provider** | Whatever your harness expects — OAuth login (`/login` in OMP, `claude` login, `codex login`) or an API key such as `ANTHROPIC_API_KEY` / `OPENROUTER_API_KEY` exported from your shell rc. |
| **Tavily** (web search) | `export TAVILY_API_KEY=...` in your shell rc. The MCP entry reads it from the environment — no key is stored here. Skip the server entirely if your harness already talks to Tavily natively. |
| **Exa or Firecrawl** (only if you swap Tavily) | `export EXA_API_KEY=...` or `export FIRECRAWL_API_KEY=...` in your shell rc. Exa's hosted server also runs keyless, with no key at all. |

Context7 and Playwright need no credentials.

## Notes

- **Editing this repo?** `AGENTS.md` at the root holds the conventions. It is not the standard you
  install — that one is `standards/en/Engineering_standards.md`.
- **Skills stay upstream.** `npx skills update -g` keeps them current instead of freezing a copy here.

## License

MIT — see [`LICENSE`](LICENSE). Take it, fork it, strip it down.
