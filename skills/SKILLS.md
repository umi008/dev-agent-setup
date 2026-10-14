# Skills

Eleven agent skills, installed **globally** from their upstream repos with the
[`skills`](https://skills.sh) CLI. Nothing is vendored here: they stay upstream so
`npx skills update -g` keeps them current.

This is the general-purpose layer. [**Gentle AI**](https://github.com/Gentleman-Programming/gentle-ai),
the harness this repo is built to run with, brings its own skills for pull requests, commits, review,
documentation and skill authoring.

## Install

```bash
npx skills add addyosmani/agent-skills -g -a universal -y \
  -s api-and-interface-design \
  -s debugging-and-error-recovery \
  -s documentation-and-adrs \
  -s frontend-ui-engineering \
  -s observability-and-instrumentation \
  -s test-driven-development

npx skills add anthropics/skills -g -a universal -y \
  -s frontend-design \
  -s docx \
  -s pdf \
  -s pptx \
  -s xlsx

npx skills ls -g           # list what is installed
npx skills update -g -y    # keep everything current
```

- **One `-s` per skill.** A comma list fails silently — it installs nothing and reports success.
- **`-g` installs at user level**, into `~/.agents/skills/`, the directory every harness that reads it
  (OMP, Claude Code, Kilo Code, …) picks up. Drop `-g` to install into one project instead.
- **`-a universal`** writes the harness-agnostic layout rather than a per-harness copy.

## Inventory

| Skill | Upstream | For |
| --- | --- | --- |
| `api-and-interface-design` | addyosmani/agent-skills | Designing APIs, module boundaries and the type contracts between modules. |
| `debugging-and-error-recovery` | addyosmani/agent-skills | Systematic root-cause debugging instead of guessing. |
| `documentation-and-adrs` | addyosmani/agent-skills | Recording decisions and the context future engineers and agents need. |
| `frontend-ui-engineering` | addyosmani/agent-skills | Production-quality, accessible, responsive user interfaces. |
| `observability-and-instrumentation` | addyosmani/agent-skills | Logging, metrics, tracing and alerting, so production behavior is visible. |
| `test-driven-development` | addyosmani/agent-skills | The red–green–refactor loop, driven by tests. |
| `frontend-design` | anthropics/skills | Distinctive visual design direction, away from templated defaults. |
| `docx` | anthropics/skills | Creating, reading and editing Word documents. |
| `pdf` | anthropics/skills | Reading, merging, splitting and generating PDFs. |
| `pptx` | anthropics/skills | Building and editing PowerPoint decks. |
| `xlsx` | anthropics/skills | Creating and editing spreadsheets. |

The four document skills are also published as the Claude Code plugin
`document-skills@anthropic-agent-skills` (`/plugin install document-skills@anthropic-agent-skills`).
Pick one route, not both.

## Pinning

There is no `skills-lock.json` in this repo on purpose: the set is small enough to read from the
commands above, and `npx skills update -g` is the intended way to move forward. To freeze a set in one
project instead, run the same `npx skills add` commands with `--project` and commit the
`skills-lock.json` that the CLI writes next to it.
