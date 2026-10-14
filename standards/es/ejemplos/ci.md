# Ejemplo de CI

La regla está en el estándar (Estructura): en cada push y pull request, los mismos gates en el mismo orden. Esta es una forma de cumplirla en cualquier host: el host corre un script y el script corre los gates.

El script se corrió en un contenedor Ubuntu limpio con solo `curl` y `git`: los proyectos Python y React pasan, y uno con un secreto commiteado falla en el último paso. Los snippets de cada host se validaron contra su documentación y se parsearon, pero no se corrieron en los hosts.

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
  uv run pytest -m "not slow and not e2e" --cov=src
fi

if [ -f pnpm-lock.yaml ]; then
  command -v pnpm >/dev/null || curl -fsSL https://get.pnpm.io/install.sh | SHELL=/bin/bash sh -
  pnpm install --frozen-lockfile
  pnpm lint
  pnpm format:check
  pnpm typecheck
  pnpm test
fi

uvx --python 3.12 pre-commit run secrets --all-files --hook-stage manual
```

El host solo necesita `curl`, `git` y un shell: `uv` descarga el Python de `.python-version`, y pnpm se descarga a sí mismo y a Node desde `package.json`. El script no lleva versiones propias.

- **`SHELL=/bin/bash`:** el instalador de pnpm aborta con `ERR_PNPM_UNKNOWN_SHELL` cuando `SHELL` no está definido, como pasa en un contenedor limpio.
- **Clon completo:** el gate de secretos escanea el historial, así que el checkout no puede ser superficial.

## Hosts

Cada archivo solo llama al script.

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

AWS CodeBuild, `buildspec.yml`. En el source del proyecto, se pone Git clone depth en Full.
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

Vercel construye y despliega; no orquesta gates. El script se corre en el host que tiene el repo y se exige antes de mergear. Para además detener el build de Vercel cuando falla un gate, `vercel.json`:
```json
{ "buildCommand": "sh scripts/ci.sh && pnpm build" }
```

Si el host no está en la lista, el contrato no cambia: se corre `scripts/ci.sh` en un runner Linux con clon completo. Si no se conoce el host, se pregunta.
