# AGENTS.md

API de pedidos en Python 3.12. Estándar completo: `Engineering_standards.md`.

## Comandos
- Instalar: `uv sync --locked`
- Gates, en este orden:
  1. `uv run ruff check .`
  2. `uv run ruff format --check .`
  3. `uv run mypy src`
  4. `uv run pytest -m "not slow and not e2e" --cov=src`
  5. `uvx --python 3.12 pre-commit run secrets --all-files --hook-stage manual`
- En un proyecto Node/React: `pnpm install --frozen-lockfile`, luego `pnpm lint`, `pnpm format:check`, `pnpm typecheck`, `pnpm test` y el mismo comando de secretos.
- Antes de decir "verde", correr los gates y mostrar su salida.

## Estructura
```
src/app/
├── routers/    HTTP: recibe, valida y delega
├── services/   reglas de negocio
└── models/     contratos de datos, sin lógica
tests/          espeja src/
docs/decisiones.md
```

## Reglas para agentes
- Cero comentarios. El porqué va en nombres, tests o `docs/decisiones.md`. Solo docstring de una línea en la API pública.
- Cero workarounds y cero supresiones (`noqa`, `type: ignore`, `pragma`, `fmt: off`): se arregla la causa.
- Dependencias solo con `uv add`. Nunca editar `uv.lock` a mano.
- Secretos nunca en el repo: `.env` va en `.gitignore`, `.env.example` lista solo los nombres.
- Un patrón, una forma: copiar el ejemplo existente.
- Un bug fix empieza con un test que lo reproduce.
- Un concern por commit, en Conventional Commits.

## Detente y pregunta
- Si un gate solo pasa debilitándolo (bajar `fail_under`, desactivar una regla).
- Si hay que borrar o reescribir tests existentes.
- Si hay conflicto de lockfile o una dependencia no resuelve.
- Si aparece un secreto en el historial: se reporta, hay que rotarlo.
