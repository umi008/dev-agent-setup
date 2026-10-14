# Decisions

Only structural or hard-to-reverse decisions. They are not rewritten: a new one supersedes the old one and only the old one's status changes (`accepted` or `superseded by NNNN`).

## ADR 0001: uv as the package manager

**Date:** 2026-10-14 · **Status:** accepted

**Context.** Dev and CI installed different versions ("works on my machine") and dependencies were edited by hand.

**Decision.** uv with `uv.lock` committed. Install with `uv sync --locked` and add dependencies only with `uv add`.

**Rejected alternatives.**
- pip + venv without a lockfile: not reproducible.
- pip-tools: more steps for the same result.
