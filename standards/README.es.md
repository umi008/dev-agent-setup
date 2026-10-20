# Engineering Standards

> Un estándar corto y ejecutable para que todo proyecto arranque con calidad y observabilidad resueltas.

[English](README.md) · [Español](README.es.md)

Pensado para agentes de código, que copian lo que ven: un comentario viejo o una supresión se
multiplica, y la revisión humana no escala. Cada regla está respaldada por un gate que falla, no por
prosa.

## Qué contiene

|                     | English                                                      | Español                                                      |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| El estándar         | [`en/Engineering_standards.md`](en/Engineering_standards.md) | [`es/Engineering_standards.md`](es/Engineering_standards.md) |
| Prompts de adopción | [`en/adopt.md`](en/adopt.md)                                 | [`es/adoptar.md`](es/adoptar.md)                             |
| Ejemplos y config   | [`en/examples/`](en/examples/)                               | [`es/ejemplos/`](es/ejemplos/)                               |

Los ejemplos cubren `AGENTS.md`, `README.md`, un ADR corto, la config de cada gate y un script de CI
que corre en cualquier host Linux (GitHub Actions, Azure Pipelines, AWS CodeBuild, Oracle DevOps,
Vercel).

## De un vistazo

- **Reproducible:** lockfile commiteado, instalación con `--locked`, runtime fijado.
- **Con gates:** lint, formato, tipos strict, tests con piso de 80% de coverage, verificación de
  cero comentarios y auditoría de dependencias. Nada está «en verde» hasta correr los gates y mostrar su salida.
- **Sin supresiones:** ni `noqa`, ni `type: ignore`, ni `eslint-disable`. Se arregla la causa, o se
  detiene y pregunta.
- **Sin secretos en el repo:** un hook bloquea el commit y el CI escanea el historial.
- **Supply chain:** las defensas de pnpm por antigüedad de versión y dependencias exóticas quedan
  activas; un bot abre los PRs de actualización.
- **Observable:** logs JSON con un `trace_id` de OpenTelemetry generado en el borde.
- **Docs mínimas:** `README.md`, `AGENTS.md` y ADR cortos. Un dato, un dueño.
- **Versiones estables:** LTS o la última estable; experimental solo si lo pides.

Stacks: Python 3.14 con [uv](https://docs.astral.sh/uv/), y Node/React con
[pnpm](https://pnpm.io/).

## Uso

1. Copia `es/Engineering_standards.md` (o `en/Engineering_standards.md`) a tu repo — raíz o `docs/`.
2. Pásale a tu agente de código un prompt de `es/adoptar.md`:
   - **Proyecto nuevo:** configura los gates y crea `README.md` y `AGENTS.md`. Sin código de dominio
     hasta que los gates estén en verde.
   - **Repo existente:** una auditoría de solo lectura con veredicto por área (`verde`, `falta`,
     `roto`), y luego un retrofit con un commit por paso.

## Verificación

Los snippets de `es/ejemplos/config.md` se corrieron el 2026-10-14 y de nuevo el 2026-10-20 en
proyectos mínimos de Python y React: los gates pasan en verde, y las verificaciones de cero
comentarios, coverage, dependencias, secretos y mensaje de commit fallan cuando deben.
`scripts/ci.sh` se corrió primero en un contenedor Ubuntu limpio y de nuevo el 2026-10-20. Los snippets de host de `es/ejemplos/ci.md`
se contrastaron con la documentación de cada host, no se corrieron en los hosts. Los límites
conocidos están anotados en esos archivos.

## Mantenimiento

Los dos idiomas son copias separadas: un cambio en una se repite en la otra.

## Licencia

[MIT](../LICENSE).
