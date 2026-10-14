# Adopt the standard

Copy `Engineering_standards.md` into the repo (root or `docs/`) and give your coding agent one of these prompts. The config snippets and the examples of `AGENTS.md`, `README.md` and an ADR are in `examples/`.

## New project

```text
Read Engineering_standards.md and apply it to this new repo.
1. Configure the gates and hooks from the table for the stack (Python with uv, or Node/React with pnpm), based on <path>/examples/config.md, and the CI based on <path>/examples/ci.md.
2. Create short README.md and AGENTS.md files, based on <path>/examples/.
3. Run the gates and show me the output. Do not write domain code until they are green.
One concern per commit. If something in the standard cannot be met, stop and ask.
```

## Existing repo

Phase 1: audit, without editing anything.

```text
Audit this repo against Engineering_standards.md. Read-only: do not edit anything.
- Run the gates the repo supports today, even if they fail. The measured coverage is the baseline.
- Count the existing comments and suppressions.
- Run the secrets scan. Report each finding by file and rule, never the secret itself.
- Report per area (reproducibility, gates, hooks and CI, structure and docs, observability, tests, delivery): green, missing or broken. Each broken item comes with the command and its real output.
End with the report and wait for my OK.
```

Phase 2: retrofit, only after the OK.

```text
Apply the retrofit, one commit per step and in this order: reproducibility (pinned runtime, lockfile) → lint, format and hooks → types (src/ first) → tests and coverage floor → comment and suppression cleanup → CI → structure, docs and observability.
- The coverage floor starts at the measured value and only goes up; the gap against 80 stays as debt.
- Never weaken a gate or mix a refactor into these commits.
- If tests have to be deleted, a gate only passes by weakening it, or a secret turns up in the history, stop and ask.
When done, run the gates and show me the output.
```
