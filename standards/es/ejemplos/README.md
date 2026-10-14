# mi-servicio

API de pedidos: crea, consulta y cancela pedidos.

## Requisitos
Python 3.12 y [uv](https://docs.astral.sh/uv/).

## Instalar
```bash
uv sync --locked
```

## Correr
```bash
uv run uvicorn app.main:app --reload
```

## Testear
```bash
uv run pytest -m "not slow and not e2e" --cov=src
```
Los gates completos están en `AGENTS.md`.

## Más
- Estructura y reglas de código: `AGENTS.md`
- Decisiones: `docs/decisiones.md`
