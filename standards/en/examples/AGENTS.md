# AGENTS.md

Orders API on Python 3.12. Full standard: `Engineering_standards.md`.

## Commands
- Install: `uv sync --locked`
- Gates, in this order:
  1. `uv run ruff check .`
  2. `uv run ruff format --check .`
  3. `uv run mypy src`
  4. `uv run pytest -m "not slow and not e2e" --cov=src`
  5. `uvx --python 3.12 pre-commit run secrets --all-files --hook-stage manual`
- In a Node/React project: `pnpm install --frozen-lockfile`, then `pnpm lint`, `pnpm format:check`, `pnpm typecheck`, `pnpm test` and the same secrets command.
- Before saying "green", run the gates and show their output.

## Structure
```
src/app/
├── routers/    HTTP: receive, validate and delegate
├── services/   business rules
└── models/     data contracts, no logic
tests/          mirrors src/
docs/decisions.md
```

## Rules for agents
- Zero comments. The why goes in names, tests or `docs/decisions.md`. Only a one-line docstring on the public API.
- Zero workarounds and zero suppressions (`noqa`, `type: ignore`, `pragma`, `fmt: off`): fix the cause.
- Dependencies only with `uv add`. Never edit `uv.lock` by hand.
- Secrets never in the repo: `.env` is git-ignored, `.env.example` lists names only.
- One pattern, one way: copy the existing example.
- A bug fix starts with a test that reproduces it.
- One concern per commit, in Conventional Commits.

## Stop and ask
- If a gate only passes by weakening it (lowering `fail_under`, disabling a rule).
- If existing tests have to be deleted or rewritten.
- If there is a lockfile conflict or a dependency does not resolve.
- If a secret shows up in the history: report it, it has to be rotated.
