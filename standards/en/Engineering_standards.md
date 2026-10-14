# Engineering Standards

## Core idea
One standard so every project starts with quality and observability already solved. The tool can be changed with a written reason; what each gate catches cannot. A rule is worth what its mechanism is worth: what is not executed degrades into text and gets ignored. It is designed for agents, which copy what they see: a stale comment or a suppression multiplies, and human review does not scale.

## Hard rules (MUST / NEVER)
Commit the lockfile and install with `--locked` / `--frozen-lockfile`; add dependencies only with `uv add` / `pnpm add`, never by editing a lockfile or activating a venv by hand. Secrets never enter the repo: `.env` is git-ignored, `.env.example` lists names only, and values come from the environment. Strict types passing and 80% coverage, never lowered to turn green. One concern per commit, with the tests alongside the code, and never `--no-verify`, `--force`, `|| true` or skip markers. Zero comments (the why goes in names, tests or ADRs; only docstrings or JSDoc on the public API) and zero workarounds or suppressions (`noqa`, `type: ignore`, `@ts-ignore`, `eslint-disable`, `pragma`, `fmt: off`): fix the cause, and if that is not possible today, stop and ask. One pattern, one way: copy the existing example. Nothing is declared "green" without running the gates and showing their output.

## Versions
Always LTS or the latest stable release, never experimental versions (alpha, beta, RC, nightly) unless the user explicitly asks for them.
- **Python:** 3.12 pinned, not a range.
- **Node:** the active LTS; never an odd-numbered major, which never reaches LTS.
- **pnpm:** the latest stable (`pnpm self-update`).
- **Libraries and hooks:** resolved by the tool (`uv add`, `pnpm add`, `pre-commit autoupdate`), never hand-written versions.
- **Pin:** the runtime and the package manager are pinned in the repo and written by the tool, never by hand: `.python-version`, and in `package.json` `devEngines` and `packageManager` (`pnpm runtime set node lts`, `pnpm self-update`). CI reads those files and never duplicates the version.

## Gates

| #   | Gate               | What it catches                                          | Python                                                                     | Node / React (pnpm)                       |
| --- | ------------------ | -------------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------- |
| 1   | Package manager    | Different environments between dev and CI                | `uv sync --locked`                                                         | `pnpm install --frozen-lockfile`          |
| 2   | Lint               | Unused imports, undefined names, unsafe patterns         | `uv run ruff check .`                                                      | `pnpm lint` (ESLint, `--max-warnings 0`)  |
| 3   | Format             | Inconsistent style; it is checked, not just applied      | `uv run ruff format --check .`                                             | `pnpm format:check` (Prettier)            |
| 4   | Types              | Misused types                                            | `uv run mypy src` (strict)                                                 | `pnpm typecheck` (`tsc --noEmit`, strict) |
| 5   | Tests and coverage | Regressions and tests that pass without proving anything | `uv run pytest -m "not slow and not e2e" --cov=src`                        | `pnpm test` (Vitest with coverage)        |
| 6   | Comments           | Comments and suppressions in the code                    | `tests/test_no_comments.py`                                                | ESLint rule `local/no-comments`           |
| 7   | Secrets            | Credentials committed to the history                     | `uvx --python 3.12 pre-commit run secrets --all-files --hook-stage manual` | same                                      |

## Coverage
- The floor is declared **only in the tool config**, never in the pipeline.
- The threshold is 80%: `fail_under = 80` in Python and the 80 threshold in the Vitest config.
- In brownfield the floor starts at the value measured today and only goes up. The gap against 80 is recorded as debt with a plan to close it.

## Tests
- **Unit:** every business rule, branch and error path, no I/O.
- **Integration:** only the real wiring, marked with `-m integration`.
- **E2E:** optional, only the key flows.
- **Hermetic and parallel:** no shared state; `tmp_path`, ephemeral ports, zero network after sync, no ordering between tests. They must run the same from a clean clone.
- **Bug fix:** starts with a test that reproduces the bug. Without it, the fix is postponed.
- **Behavior, not implementation:** tests assert what is observable. A flaky test goes to quarantine; it is not tolerated.

## Structure
- **Common root:** `README.md`, `AGENTS.md`, `.pre-commit-config.yaml`, pipeline, `.gitignore`, manifest with lockfile and pinned runtime.
- **Hooks:** lint, format and secrets run on every commit. A hook can be skipped, so CI is the backstop.
- **CI:** on every push and pull request, the same gates in the same order, with the runtime read from the pin files. The clone includes the history, which the secrets gate scans.

## Observability
Goal: reconstruct an incident from a single id.
- **`trace_id`:** generated at the edge, propagated with `contextvars` and sent on every outgoing call.
- **JSON logs:** `trace_id`, `level`, `ts` (UTC) and `event`. Never free text; one event per line.
- **Redaction:** PII and secrets are redacted before emitting, prompts included.
- **Levels:** `ERROR` is what nobody handled and someone must open; what was handled (retry, fallback) is `WARN`; `DEBUG` is off or sampled in production.
- **Business events:** stable name `domain.fact` and no PII. They do not replace the log.
- **Sampling and alerts:** sample `DEBUG` and high traffic, never `ERROR`. Alerts go on latency (p95) and error rate, not just on exceptions.
- **Anti-patterns:** logging instead of raising, logging PII, everything at `ERROR`, double logging per layer.

## Documentation
Minimal: an agent reads the code directly, so the documentation does not repeat it.
- **`README.md`:** what it is, how to install, run and test.
- **`AGENTS.md`:** real structure, per-folder convention and the code rules for agents.
- **Public API:** one-line docstring in Python and JSDoc in TS. It is the only comment allowed.
- **ADR (Architecture Decision Record, in `docs/decisions.md`):** only for structural or hard-to-reverse decisions. Short: context, decision and rejected alternatives. They are not rewritten: a new one supersedes the old one.
- **One fact, one owner:** if a table lives in two files, it drifts.
- **No ghost documentation:** no skeletons with `TODO`.
- **Same commit:** documentation is written with the code, not afterwards.

## Commits and delivery
- Conventional Commits and SemVer.
- A refactor is never mixed into an adoption or retrofit commit.

## When to stop and ask
- The structure contradicts the gates and fixing it moves half the repo. Do not force it or half-do it: report the real scope of the move.
- A gate only passes if it is weakened.
- There is a lockfile conflict, or a dependency does not resolve under the pinned runtime.
- A secret shows up in the history: it is rotated first. Deleting the file does not fix it.
- The CI platform or the VCS host is unknown.

**Report the blocker. Never weaken anything silently.**

## Enforcement ladder
From strongest to weakest: **architecture** (the error is impossible by design) > **lint, types and tests** (the gate fails) > **rules and skills** (an agent can ignore them) > **human review** (last resort). If something is corrected twice, climb one rung: write the guard, watch it fail (RED), fix the cause and clean up the existing instances until it passes.

## Adoption and audit
- **New project:** this document lives in the repo from the start, and the gates are green before any domain code is written.
- **Existing repo:** add this document to the repo and ask the agent to apply it. First a read-only audit, where each `broken` comes with the command and its real output; nothing is fixed while auditing. Then a retrofit with one commit per step: reproducibility → lint, format and hooks → types (`src/` first) → tests and floor → comment and suppression cleanup → CI → structure, docs and observability.
- **Verdict:** per area (reproducibility, gates, hooks and CI, structure and docs, observability, tests, delivery), each one `green`, `missing` or `broken`. A gate that does not pass, does not pass.
