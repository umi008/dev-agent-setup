# MCP servers

The Model Context Protocol servers I run, and what each one is for. Two of them ship with
[Gentle AI](https://github.com/Gentleman-Programming/gentle-ai), the harness layer this repo is built
to run with; the rest you declare yourself. Nothing secret lives here: config files reference
environment variables, never literals.

| Server | What it is for | Where it comes from |
| --- | --- | --- |
| **Tavily** | Web search, for harnesses that do not ship a native search provider chain. | `npx -y tavily-mcp@latest` — reads `TAVILY_API_KEY` from the environment. |
| **Context7** | Live documentation for libraries and frameworks, instead of trusting memory. | Comes with Gentle AI — nothing to configure. |
| **Engram** | Persistent memory across sessions and compactions. | Comes with Gentle AI — nothing to configure. |

The browser is not an MCP server here: it is the `playwright-cli` skill from
[`skills/SKILLS.md`](../skills/SKILLS.md). Microsoft recommends the CLI for coding agents because it
does not load tool schemas and accessibility trees into the context; the Playwright MCP stays an
option for long autonomous browser loops (see below).

## Canonical block

Only Tavily is configured by hand; Context7 and Engram are provided by [Gentle
AI](https://github.com/Gentleman-Programming/gentle-ai).

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "${TAVILY_API_KEY}"
      }
    }
  }
}
```

## Alternatives to Tavily

Tavily is just the search server I settled on. Swap it for one of these and nothing else changes — the
shape is the same.

| Server | What it adds | How to declare it |
| --- | --- | --- |
| **Exa** | Web search, page fetching, code search and multi-step research (Exa Agent). | Hosted and keyless to start: `"url": "https://mcp.exa.ai/mcp"`. Local package: `npx -y exa-mcp-server` with `EXA_API_KEY`. |
| **Firecrawl** | Search, scrape and interact with the web, plus a parse tool. | Local package: `npx -y firecrawl-mcp` with `FIRECRAWL_API_KEY`. Hosted OAuth endpoint, no key: `https://mcp.firecrawl.dev/v2/mcp-oauth`. |

With Exa the hosted server is the shortest path: it starts keyless, you add `?login` for OAuth or an
`x-api-key` header once you want your own quota, and you only need the local package when the client
cannot speak remote MCP.

Pick **one** search server. Two search providers in the same session duplicate the tool surface and
burn two API calls for one question.

## Optional: Playwright MCP

For exploratory automation or long-running browser loops, where keeping the browser state in the
conversation is worth the tokens, add the MCP server next to Tavily:

```json
"playwright": {
  "command": "npx",
  "args": ["-y", "@playwright/mcp@latest", "--browser", "chromium", "--headless"]
}
```

It needs no credentials. Use it or the `playwright-cli` skill for a given task, not both at once.

## Notes

- **One shape, many harnesses.** Tavily, the Playwright MCP and the Exa and Firecrawl packages are plain
  stdio processes launched with `npx`; Exa and Firecrawl also offer remote endpoints that you declare
  with a URL instead. Only the surrounding JSON or TOML keys change: the `mcpServers` shape above is
  what most clients expect, so check your harness's docs for its own key and transport field names.
- **`${VAR}` expansion is not universal.** Claude Code expands it in MCP config; a harness that does
  not will pass the literal string. Inline the key in your own config file (never in a repo), or export
  the variable before launching the harness.
- **Drop Tavily where search is built in.** Oh My Pi reads `TAVILY_API_KEY` directly and exposes a
  native `web_search` tool. Running the MCP server too duplicates tools and burns two API calls for one
  question.
- **Drop Context7 and Engram where they are already provided.** Both ship with Gentle AI; declaring
  them again in your own config loads a second copy of the same tools.
