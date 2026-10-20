# Engineering Standards

## Idea central
Un estándar único para que todo proyecto arranque con calidad y observabilidad resueltas. La herramienta se puede cambiar con una razón escrita; lo que cada gate detecta, no. Una regla vale lo que vale su mecanismo: lo que no se ejecuta se degrada a texto y se ignora. Está pensado para agentes, que copian lo que ven: un comentario viejo o una supresión se multiplican, y la revisión humana no escala.

## Reglas duras (MUST / NEVER)
Lockfile commiteado e instalación con `--locked` / `--frozen-lockfile`; dependencias solo con `uv add` / `pnpm add`, nunca editando un lockfile ni activando un venv a mano. Las defensas de supply chain del gestor quedan activas: `minimumReleaseAge` y `blockExoticSubdeps` de pnpm nunca se bajan ni se desactivan. Los secretos nunca entran al repo: `.env` va en `.gitignore`, `.env.example` lista solo los nombres, y los valores vienen del entorno. Tipos strict en verde y coverage de 80%, sin bajarlos para ponerse en verde. Un concern por commit, con los tests junto al código, y nunca `--no-verify`, `--force`, `|| true` ni marcadores de skip. Cero comentarios (el porqué va en nombres, tests o ADR; solo docstrings o JSDoc de API pública) y cero workarounds o supresiones (`noqa`, `type: ignore`, `@ts-ignore`, `eslint-disable`, `pragma`, `fmt: off`): se arregla la causa, y si hoy no se puede, se detiene y se pregunta. Un patrón, una forma: se copia el ejemplo existente. Nada se declara "verde" sin correr los gates y mostrar su salida.

## Versiones
Siempre LTS o la última estable, nunca versiones experimentales (alpha, beta, RC, nightly) a menos que el usuario lo pida explícitamente.
- **Python:** 3.14 fijo, no un rango. Un minor nuevo se adopta cuando las herramientas de los gates lo soportan.
- **Node:** la LTS activa; nunca un major impar, que no llega a LTS.
- **pnpm:** la última estable (`pnpm self-update`).
- **Librerías y hooks:** las resuelve el gestor (`uv add`, `pnpm add`, `pre-commit autoupdate`), nunca versiones escritas a mano.
- **Pin:** el runtime y el gestor de paquetes se fijan en el repo y los escribe la herramienta, nunca a mano: `.python-version`, y en `package.json` `devEngines` y `packageManager` (`pnpm runtime set node lts`, `pnpm self-update`). El CI lee esos archivos y nunca duplica la versión.
- **Actualizaciones:** un bot (Renovate o Dependabot) abre los pull requests de actualización de dependencias y los gates los validan.
- **Excepción escrita:** `uv audit` es una función preview de uv. Es la única herramienta experimental que usa el estándar, porque es la auditoría de dependencias nativa de uv; cuando sea estable, se quita `--preview-features audit-command`.

## Gates

| #   | Gate               | Qué detecta                                               | Python                                                                     | Node / React (pnpm)                       |
| --- | ------------------ | --------------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------- |
| 1   | Gestor de paquetes | Entornos distintos entre dev y CI                         | `uv sync --locked`                                                         | `pnpm install --frozen-lockfile`          |
| 2   | Lint               | Imports sin usar, nombres indefinidos, patrones inseguros | `uv run ruff check .`                                                      | `pnpm lint` (ESLint, `--max-warnings 0`)  |
| 3   | Formato            | Estilo inconsistente; se verifica, no solo se aplica      | `uv run ruff format --check .`                                             | `pnpm format:check` (Prettier)            |
| 4   | Tipos              | Tipos mal usados                                          | `uv run mypy src` (strict)                                                 | `pnpm typecheck` (`tsc --noEmit`, strict) |
| 5   | Tests y coverage   | Regresiones y tests que pasan sin probar nada             | `uv run pytest -n auto -m "not slow and not e2e" --cov=src`                | `pnpm test` (Vitest con coverage)         |
| 6   | Comentarios        | Comentarios y supresiones en el código                    | `tests/test_sin_comentarios.py`                                            | regla ESLint `local/no-comments`          |
| 7   | Dependencias       | Dependencias con vulnerabilidades conocidas               | `uv audit --locked --preview-features audit-command`                       | `pnpm audit --audit-level high`           |
| 8   | Secretos           | Credenciales commiteadas en el historial                  | `uvx --python 3.14 pre-commit run secrets --all-files --hook-stage manual` | igual                                     |

## Coverage
- El piso se declara **solo en la config de la herramienta**, nunca en el pipeline.
- El umbral es 80%: `fail_under = 80` en Python y el umbral de 80 en la config de Vitest.
- En brownfield el piso arranca en el valor medido hoy y solo sube. La brecha frente a 80 se registra como deuda con un plan de subida.

## Tests
- **Unit:** cada regla de negocio, rama y ruta de error, sin I/O.
- **Integration:** solo el wiring real, marcado con `-m integration`.
- **E2E:** opcional, solo los flujos importantes.
- **Herméticos y paralelos:** sin estado compartido, con `tmp_path`, puertos efímeros, cero red tras el sync y sin orden entre tests. Deben correr igual desde un clon limpio. En Python, `pytest-xdist` (`-n auto`) los corre en paralelo y `pytest-randomly` baraja su orden en cada corrida; Vitest ya corre los archivos de test en paralelo.
- **Bug fix:** empieza con un test que reproduce el bug. Sin ese test, el fix está pospuesto.
- **Comportamiento, no implementación:** los tests afirman lo observable. Un test flaky pasa a cuarentena, no se tolera.

## Estructura
- **Raíz común:** `README.md`, `AGENTS.md`, `.pre-commit-config.yaml`, pipeline, `.gitignore`, manifiesto con lockfile y runtime pineado.
- **Hooks:** lint, formato y secretos corren en cada commit, y el mensaje del commit se verifica contra Conventional Commits. Un hook se puede saltar, así que el CI es el respaldo.
- **CI:** en cada push y pull request, los mismos gates en el mismo orden, con el runtime leído de los archivos de pin. El clon incluye el historial, que el gate de secretos escanea.

## Observabilidad
Objetivo: reconstruir un incidente con un solo id.
- **Contexto de traza:** OpenTelemetry con el header W3C `traceparent`. El `trace_id` se genera en el borde cuando la petición no trae uno, se propaga dentro del proceso con el contexto de OpenTelemetry (`contextvars` en Python) y viaja en cada llamada saliente.
- **Logs JSON:** `trace_id` del span activo, `level`, `ts` (UTC) y `event` (`structlog` en Python). Nunca texto libre; un evento por línea.
- **Redacción:** PII y secretos se redactan antes de emitir, prompts incluidos.
- **Niveles:** `ERROR` es lo que nadie manejó y alguien debe abrir; lo manejado (retry, fallback) es `WARN`; `DEBUG` va apagado o muestreado en producción.
- **Eventos de negocio:** nombre estable `dominio.hecho` y sin PII. No reemplazan al log.
- **Sampling y alertas:** se muestrea `DEBUG` y el tráfico alto, nunca `ERROR`. Las alertas van sobre latencia (p95) y tasa de error, no solo sobre excepciones.
- **Anti-patrones:** loguear en vez de lanzar, loguear PII, todo en `ERROR`, doble logging por capa.

## Documentación
Mínima: un agente lee el código directamente, así que la documentación no lo repite.
- **`README.md`:** qué es, cómo instalar, correr y testear.
- **`AGENTS.md`:** estructura real, convención por carpeta y las reglas de código para agentes.
- **API pública:** docstring de una línea en Python y JSDoc en TS. Es el único comentario permitido.
- **ADR (Architecture Decision Record, en `docs/decisiones.md`):** solo para decisiones estructurales o difíciles de revertir. Cortos: contexto, decisión y alternativas descartadas. No se reescriben: uno nuevo supersede al viejo.
- **Un dato, un dueño:** si una tabla vive en dos archivos, diverge.
- **Sin documentación fantasma:** no hay esqueletos con `TODO`.
- **Mismo commit:** la documentación se escribe con el código, no después.

## Commits y entrega
- Conventional Commits, verificados por el hook `commit-msg`, y SemVer.
- Nunca se mezcla un refactor con un commit de adopción o retrofit.

## Cuándo detenerse y preguntar
- La estructura contradice los gates y arreglarla mueve medio repo. No se fuerza ni se hace a medias: se reporta el alcance real del movimiento.
- Un gate solo pasa si se debilita.
- Hay conflicto de lockfile, o una dependencia no resuelve bajo el runtime pineado.
- Aparece un secreto en el historial: primero se rota. Borrar el archivo no lo arregla.
- No se conoce la plataforma de CI ni el host de VCS.

**Se reporta el bloqueo. Nunca se debilita en silencio.**

## Escala de enforcement
De más fuerte a más débil: **arquitectura** (el error es imposible por diseño) > **lint, tipos y tests** (el gate falla) > **reglas y skills** (un agente puede ignorarlas) > **revisión humana** (último recurso). Si algo se corrige dos veces, se sube un peldaño: se escribe el guard, se ve fallar (RED), se arregla la causa y se limpian las instancias hasta que pase.

## Adopción y auditoría
- **Proyecto nuevo:** este documento vive en el repo desde el inicio, y los gates quedan en verde antes de escribir código de dominio.
- **Repo existente:** se agrega este documento al repo y se le pide al agente que lo aplique. Primero una auditoría de solo lectura, donde cada `roto` lleva el comando y su salida real; no se arregla nada mientras se audita. Después, un retrofit con un commit por paso: reproducibilidad → lint, formato y hooks → tipos (`src/` primero) → tests y piso → limpieza de comentarios y supresiones → auditoría de dependencias → CI → estructura, docs y observabilidad.
- **Veredicto:** por área (reproducibilidad, gates, hooks y CI, estructura y docs, observabilidad, tests, entrega), cada una `verde`, `falta` o `roto`. Un gate que no pasa, no pasa.
