# Adoptar el estándar

Copia `Engineering_standards.md` al repo (raíz o `docs/`), y pásale a tu agente de código uno de estos prompts. Los snippets de config y los ejemplos de `AGENTS.md`, `README.md` y ADR están en `ejemplos/`.

## Proyecto nuevo

```text
Lee Engineering_standards.md y aplícalo a este repo nuevo.
1. Configura los gates y hooks de la tabla para el stack (Python con uv, o Node/React con pnpm), con base en <ruta>/ejemplos/config.md, y el CI con base en <ruta>/ejemplos/ci.md.
2. Crea README.md y AGENTS.md cortos, con base en <ruta>/ejemplos/.
3. Corre los gates y muéstrame la salida. No escribas código de dominio hasta que estén en verde.
Un concern por commit. Si algo del estándar no se puede cumplir, detente y pregunta.
```

## Repo existente

Fase 1: auditoría, sin editar nada.

```text
Audita este repo contra Engineering_standards.md. Solo lectura: no edites nada.
- Corre los gates que el repo soporta hoy, aunque fallen. El coverage medido es la línea base.
- Cuenta los comentarios y supresiones existentes.
- Corre el escaneo de secretos. Reporta cada hallazgo por archivo y regla, nunca el secreto en sí.
- Reporta por área (reproducibilidad, gates, hooks y CI, estructura y docs, observabilidad, tests, entrega): verde, falta o roto. Cada roto lleva el comando y su salida real.
Termina con el reporte y espera mi OK.
```

Fase 2: retrofit, solo después del OK.

```text
Aplica el retrofit, un commit por paso y en este orden: reproducibilidad (runtime pineado, lockfile) → lint, formato y hooks → tipos (src/ primero) → tests y piso de coverage → limpieza de comentarios y supresiones → CI → estructura, docs y observabilidad.
- El piso de coverage arranca en el valor medido y solo sube; la brecha frente a 80 queda como deuda.
- Nunca debilites un gate ni mezcles un refactor en estos commits.
- Si hay que borrar tests, un gate solo pasa debilitándolo, o aparece un secreto en el historial, detente y pregunta.
Al terminar, corre los gates y muéstrame la salida.
```
