# Engineering Standards

> One short, enforceable standard so every project starts with quality and observability already solved.

[English](README.md) · [Español](README.es.md)

Written for coding agents, which copy what they see: a stale comment or a suppression multiplies, and
human review does not scale. Every rule is backed by a gate that fails, not by prose.

## What's inside

|                     | English                                                      | Español                                                      |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| The standard        | [`en/Engineering_standards.md`](en/Engineering_standards.md) | [`es/Engineering_standards.md`](es/Engineering_standards.md) |
| Adoption prompts    | [`en/adopt.md`](en/adopt.md)                                 | [`es/adoptar.md`](es/adoptar.md)                             |
| Examples and config | [`en/examples/`](en/examples/)                               | [`es/ejemplos/`](es/ejemplos/)                               |

The examples cover `AGENTS.md`, `README.md`, a short ADR, the tool config for each gate and a CI
script that runs on any Linux host (GitHub Actions, Azure Pipelines, AWS CodeBuild, Oracle DevOps,
Vercel).

## At a glance

- **Reproducible:** lockfile committed, installs with `--locked`, runtime pinned.
- **Gated:** lint, format, strict types, tests with an 80% coverage floor, a zero-comments check and a
  dependency audit.
  Nothing is "green" until the gates run and their output is shown.
- **No suppressions:** no `noqa`, `type: ignore` or `eslint-disable`. Fix the cause, or stop and ask.
- **No secrets in the repo:** a hook blocks the commit and CI scans the history.
- **Supply chain:** pnpm's release-age and exotic-dependency guards stay on; a bot opens the update PRs.
- **Observable:** JSON logs with an OpenTelemetry `trace_id` generated at the edge.
- **Minimal docs:** `README.md`, `AGENTS.md` and short ADRs. One fact, one owner.
- **Stable versions:** LTS or latest stable; experimental only when you ask for it.

Stacks: Python 3.14 with [uv](https://docs.astral.sh/uv/), and Node/React with
[pnpm](https://pnpm.io/).

## Usage

1. Copy `en/Engineering_standards.md` (or `es/Engineering_standards.md`) into your repo — root or
   `docs/`.
2. Give your coding agent a prompt from `en/adopt.md`:
   - **New project:** configures the gates and creates `README.md` and `AGENTS.md`. No domain code
     until the gates are green.
   - **Existing repo:** a read-only audit with a verdict per area (`green`, `missing`, `broken`),
     then a retrofit with one commit per step.

## Verification

The snippets in `en/examples/config.md` were run on 2026-10-14 and again on 2026-10-20 in minimal
Python and React projects: the gates pass green, and the zero-comments, coverage, dependency, secrets
and commit-message checks fail when they should. `scripts/ci.sh` was first run in a clean Ubuntu
container and rerun on 2026-10-20. The host snippets in `en/examples/ci.md` were
checked against each host's documentation, not run on the hosts. Known limits are listed in those
files.

## Maintenance

The two languages are separate copies: a change in one is mirrored in the other.

## License

[MIT](../LICENSE).
