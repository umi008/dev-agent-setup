# MCP servers

The Model Context Protocol servers I run, and what each one is for. Two of them ship with
[Gentle AI](https://github.com/Gentleman-Programming/gentle-ai), the harness layer this repo is built
to run with; the rest you declare yourself. Nothing secret lives here: config files reference
environment variables, never literals.

| Server | What it is for | Where it comes from |
| --- | --- | --- |
| **Tavily** | Web search, for harnesses that do not ship a native search provider chain. | `npx -y tavily-mcp@latest` — reads `TAVILY_API_KEY` from the environment. |
| **Playwright** | Headless browser: driving and verifying local web apps, screenshots, logs. | `npx -y @playwright/mcp@0.0.79 --browser chromium --headless` |
| **Context7** | Live documentation for libraries and frameworks, instead of trusting memory. | Comes with Gentle AI — nothing to configure. |
| **Engram** | Persistent memory across sessions and compactions. | Comes with Gentle AI — nothing to configure. |

## Canonical block

Only Tavily and Playwright are configured by hand; Context7 and Engram are provided by [Gentle
AI](https://github.com/Gentleman-Programming/gentle-ai).

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@0.0.79", "--browser", "chromium", "--headless"]
    },
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

## Notes

- **One shape, many harnesses.** Tavily, Playwright and the Exa and Firecrawl packages are plain
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
