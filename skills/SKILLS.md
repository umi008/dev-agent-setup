# Skills

Eighteen agent skills, installed **globally** from their upstream repos with the
[`skills`](https://skills.sh) CLI. Nothing is vendored here: they stay upstream so
`npx skills update -g` keeps them current.

This is the general-purpose layer. [**Gentle AI**](https://github.com/Gentleman-Programming/gentle-ai),
the harness this repo is built to run with, brings its own skills for pull requests, commits, review,
documentation and skill authoring.

## Install

```bash
npx skills add addyosmani/agent-skills -g -a universal -a claude-code -y \
  -s api-and-interface-design \
  -s debugging-and-error-recovery \
  -s documentation-and-adrs \
  -s frontend-ui-engineering \
  -s observability-and-instrumentation \
  -s performance-optimization \
  -s security-and-hardening \
  -s source-driven-development \
  -s test-driven-development

npx skills add anthropics/skills -g -a universal -a claude-code -y \
  -s frontend-design \
  -s docx \
  -s pdf \
  -s pptx \
  -s xlsx

npx skills add vercel-labs/agent-skills -g -a universal -a claude-code -y \
  -s vercel-react-best-practices \
  -s web-design-guidelines

npx skills add trailofbits/skills -g -a universal -a claude-code -y \
  -s supply-chain-risk-auditor

npx skills add microsoft/playwright-cli -g -a universal -a claude-code -y \
  -s playwright-cli
npm install -g @playwright/cli@latest   # the binary the playwright-cli skill drives

npx skills ls -g           # list what is installed
npx skills update -g -y    # keep everything current
```

- **One `-s` per skill.** A comma list fails silently — it installs nothing and reports success.
- **`-g` installs at user level.** Drop it to install into one project instead.
- **`-a universal`** writes the harness-agnostic copy to `~/.agents/skills/`, which Pi, OMP, Kilo Code
  and other Agent Skills harnesses read.
- **`-a claude-code`** is needed as well: Claude Code reads only `~/.claude/skills/`, not
  `~/.agents/skills/`. With both flags the CLI keeps one copy and links it into `~/.claude/skills/`,
  so `npx skills update -g` still updates a single place.
- **`playwright-cli` drives a real browser.** By default it opens the installed Google Chrome; pick
  another with `--browser` (`firefox`, `webkit`, `msedge`).

## Inventory

| Skill | Upstream | For |
| --- | --- | --- |
| `api-and-interface-design` | addyosmani/agent-skills | Designing APIs, module boundaries and the type contracts between modules. |
| `debugging-and-error-recovery` | addyosmani/agent-skills | Systematic root-cause debugging instead of guessing. |
| `documentation-and-adrs` | addyosmani/agent-skills | Recording decisions and the context future engineers and agents need. |
| `frontend-ui-engineering` | addyosmani/agent-skills | Production-quality, accessible, responsive user interfaces. |
| `observability-and-instrumentation` | addyosmani/agent-skills | Logging, metrics, tracing and alerting, so production behavior is visible. |
| `performance-optimization` | addyosmani/agent-skills | Profiling and fixing regressions: Core Web Vitals, N+1 queries, slow paths. |
| `security-and-hardening` | addyosmani/agent-skills | OWASP Top Ten, input handling, auth, and triaging dependency audit findings. |
| `source-driven-development` | addyosmani/agent-skills | Grounding each implementation decision in the official docs; pairs with Context7. |
| `test-driven-development` | addyosmani/agent-skills | The red–green–refactor loop, driven by tests. |
| `frontend-design` | anthropics/skills | Distinctive visual design direction, away from templated defaults. |
| `docx` | anthropics/skills | Creating, reading and editing Word documents. |
| `pdf` | anthropics/skills | Reading, merging, splitting and generating PDFs. |
| `pptx` | anthropics/skills | Building and editing PowerPoint decks. |
| `xlsx` | anthropics/skills | Creating and editing spreadsheets. |
| `vercel-react-best-practices` | vercel-labs/agent-skills | React and Next.js performance patterns: rendering, data fetching, bundle size. |
| `web-design-guidelines` | vercel-labs/agent-skills | Reviewing UI code against web interface and accessibility guidelines. |
| `supply-chain-risk-auditor` | trailofbits/skills | Supply-chain risk of the dependency tree: advisories, abandoned upstreams, install scripts. |
| `playwright-cli` | microsoft/playwright-cli | Driving and verifying web apps in a browser through a CLI, cheaper in tokens than the Playwright MCP. |

The four document skills are also published as the Claude Code plugin
`document-skills@anthropic-agent-skills` (`/plugin install document-skills@anthropic-agent-skills`).
Pick one route, not both.

## Pinning

There is no `skills-lock.json` in this repo on purpose: the set is small enough to read from the
commands above, and `npx skills update -g` is the intended way to move forward. To freeze a set in one
project instead, run the same `npx skills add` commands with `--project` and commit the
`skills-lock.json` that the CLI writes next to it.
