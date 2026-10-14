# Decisiones

Solo decisiones estructurales o difíciles de revertir. No se reescriben: uno nuevo supersede al viejo y solo se le cambia el estado (`aceptado` o `superseded por NNNN`).

## ADR 0001: uv como gestor de paquetes

**Fecha:** 2026-10-14 · **Estado:** aceptado

**Contexto.** Dev y CI instalaban versiones distintas ("en mi máquina funciona") y las dependencias se editaban a mano.

**Decisión.** uv con `uv.lock` commiteado. Instalar con `uv sync --locked` y agregar dependencias solo con `uv add`.

**Alternativas descartadas.**
- pip + venv sin lockfile: no es reproducible.
- pip-tools: más pasos para el mismo resultado.
