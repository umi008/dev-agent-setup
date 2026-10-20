# CI example

The rule is in the standard (Structure): on every push and pull request, the same gates in the same order. This is one way to meet it on any host: the host runs one script and the script runs the gates.

The script was first run in a clean Ubuntu container with only `curl` and `git`. This version was rerun on 2026-10-20 against minimal Python and React projects: both pass, a project with a committed secret fails at the last step, and a vulnerable dependency fails the audit. The host snippets were validated against each host's documentation and parsed, but not run on the hosts.

## `scripts/ci.sh`

```sh
#!/bin/sh
set -eu

PNPM_HOME="${PNPM_HOME:-$HOME/.local/share/pnpm}"
export PNPM_HOME
export PATH="$HOME/.local/bin:$PNPM_HOME/bin:$PATH"

command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

if [ -f uv.lock ]; then
  uv sync --locked
  uv run ruff check .
  uv run ruff format --check .
  uv run mypy src
  uv run pytest -n auto -m "not slow and not e2e" --cov=src
  uv audit --locked --preview-features audit-command
fi

if [ -f pnpm-lock.yaml ]; then
  command -v pnpm >/dev/null || curl -fsSL https://get.pnpm.io/install.sh | SHELL=/bin/bash sh -
  pnpm install --frozen-lockfile
  pnpm lint
  pnpm format:check
  pnpm typecheck
  pnpm test
  pnpm audit --audit-level high
fi

uvx --python 3.14 pre-commit run secrets --all-files --hook-stage manual
```

The host needs only `curl`, `git` and a shell: `uv` downloads the Python from `.python-version`, and pnpm downloads itself and Node from `package.json`. The script has no versions of its own.

- **`SHELL=/bin/bash`:** the pnpm installer aborts with `ERR_PNPM_UNKNOWN_SHELL` when `SHELL` is unset, as it is in a clean container.
- **Full clone:** the secrets gate scans the history, so the checkout cannot be shallow.
- **The audit needs the network.** `uv audit` and `pnpm audit` query advisory databases; they run after the tests, which stay offline.

## Hosts

Each file only calls the script.

GitHub Actions, `.github/workflows/ci.yml`
```yaml
name: ci
on: [push, pull_request]
jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0
      - run: sh scripts/ci.sh
```

Azure Pipelines, `azure-pipelines.yml`
```yaml
trigger: [main]
pr: [main]
pool:
  vmImage: ubuntu-latest
steps:
  - checkout: self
    fetchDepth: 0
  - script: sh scripts/ci.sh
    displayName: Gates
```

AWS CodeBuild, `buildspec.yml`. In the project source, set the Git clone depth to Full.
```yaml
version: 0.2
phases:
  build:
    commands:
      - sh scripts/ci.sh
```

Oracle Cloud Infrastructure DevOps, `build_spec.yaml`
```yaml
version: 0.1
component: build
timeoutInSeconds: 1200
shell: bash
failImmediatelyOnError: true
steps:
  - type: Command
    name: Gates
    command: sh scripts/ci.sh
```

Vercel builds and deploys; it does not orchestrate gates. Run the script on the host that owns the repo and require it before merging. To also stop the Vercel build when a gate fails, `vercel.json`:
```json
{ "buildCommand": "sh scripts/ci.sh && pnpm build" }
```

If the host is not on this list, the contract does not change: run `scripts/ci.sh` on a Linux runner with a full clone. If the host is unknown, ask.
