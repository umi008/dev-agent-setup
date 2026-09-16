# Skills

Skills are installed **globally** with the [`skills`](https://skills.sh) CLI, not vendored in this
repo. Global scope lands in `~/.agents/skills/`, which OMP, Claude Code, and most other harnesses
read directly.

Install everything (four commands, 38 skills):

```bash
npx skills add addyosmani/agent-skills -g -a universal -y \
  -s api-and-interface-design -s browser-testing-with-devtools -s ci-cd-and-automation \
  -s code-review-and-quality -s context-engineering -s debugging-and-error-recovery \
  -s deprecation-and-migration -s documentation-and-adrs -s doubt-driven-development \
  -s frontend-ui-engineering -s git-workflow-and-versioning -s idea-refine \
  -s incremental-implementation -s interview-me -s observability-and-instrumentation \
  -s performance-optimization -s planning-and-task-breakdown -s security-and-hardening \
  -s shipping-and-launch -s source-driven-development -s spec-driven-development \
  -s using-agent-skills

npx skills add anthropics/skills -g -a universal -y \
  -s docx -s pdf -s pptx -s xlsx -s frontend-design -s mcp-builder -s skill-creator \
  -s webapp-testing

npx skills add mattpocock/skills -g -a universal -y \
  -s domain-modeling -s resolving-merge-conflicts -s grilling -s writing-for-agents \
  -s prototype -s research

npx skills add obra/superpowers -g -a universal -y \
  -s test-driven-development -s verification-before-completion
```

> Each skill needs its own `-s` flag. A comma-separated list fails with
> `No matching skills found` — the CLI treats the whole string as one name.
>
> `-a universal` installs into `~/.agents/skills/`. Use `-a '*'` to also link the skills into every
> agent-specific directory the CLI knows about, or `-a claude-code,codex,opencode,…` to pick.

Verify and maintain:

```bash
npx skills ls -g          # list installed global skills
npx skills update -g -y   # refresh to latest upstream versions
```

## Reproducible installs

[`skills-lock.json`](../skills-lock.json) at the repo root pins all 38 skills to their source repo,
path, and content hash. Copy it into a project and restore the exact set:

```bash
cp /path/to/this-repo/skills-lock.json .
npx skills experimental_install     # installs into ./.agents/skills/
```

The lockfile is project-scoped by design — the global commands above always take upstream `main`.
Regenerate it after changing the skill set by re-running the four commands with `--project` instead
of `-g` in a scratch directory and copying the resulting `skills-lock.json` back here.

## Inventory

| Source | Skills |
| --- | --- |
| [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) | api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, using-agent-skills |
| [`anthropics/skills`](https://github.com/anthropics/skills) | docx, pdf, pptx, xlsx, frontend-design, mcp-builder, skill-creator, webapp-testing |
| [`mattpocock/skills`](https://github.com/mattpocock/skills) | domain-modeling, resolving-merge-conflicts, grilling, writing-for-agents, prototype, research |
| [`obra/superpowers`](https://github.com/obra/superpowers) | test-driven-development, verification-before-completion |

`spec-driven-development`, `test-driven-development`, `verification-before-completion`,
`interview-me`, `grilling`, `prototype`, `research`, `writing-for-agents`, and `webapp-testing` are
the ones the shared ruleset (`rules/AGENTS.md`) names directly — keep those even if you trim the
list.
