# my-service

Orders API: creates, queries and cancels orders.

## Requirements
Python 3.14 and [uv](https://docs.astral.sh/uv/).

## Install
```bash
uv sync --locked
```

## Run
```bash
uv run uvicorn app.main:app --reload
```

## Test
```bash
uv run pytest -n auto -m "not slow and not e2e" --cov=src
```
The full gates are in `AGENTS.md`.

## More
- Structure and code rules: `AGENTS.md`
- Decisions: `docs/decisions.md`
