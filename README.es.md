<div align="center">

# Dev Agent Setup

**Una base portable y agnóstica de harness para agentes de código.**

Un estándar de ingeniería · una lista de MCPs · un set de skills fijo.

Pensado para usarse junto a [Gentle AI](https://github.com/Gentleman-Programming/gentle-ai), la capa
de harness que uso — que es también de donde vienen Context7 y Engram.

Funciona con **Pi** y **Claude Code** (la pareja que recomiendo), OpenCode, Codex, Antigravity, Kilo
Code, Cursor, Gemini CLI, Oh My Pi, y con cualquier otro que lea un archivo de reglas tipo `AGENTS.md`
y hable MCP.

[English](README.md) · [Español](README.es.md)

</div>

---

## Qué es esto

No es un producto ni un framework. Es **mi setup personal de trabajo**, ordenado y compartido porque
puede ahorrarte una tarde. Nada de esto sostiene a nadie más que a mí: hazle fork, borra la mitad,
quédate con lo que te sirva.

Mínimo a propósito: tres documentos, sin instalador, sin skills vendorizadas, sin framework que
aprender. Puedes leerlo completo en diez minutos.

## Qué incluye

| Pieza | Qué es | Dónde |
| --- | --- | --- |
| **Estándar de ingeniería** | Un estándar corto y ejecutable — versiones, gates, tests, estructura, observabilidad, docs — con prompts de adopción y la config de cada gate. Está escrito para agentes de código, así que cada regla se respalda con un gate que falla, no con prosa. | [`standards/README.es.md`](standards/README.es.md) |
| **Servidores MCP** | Los MCPs que uso y para qué sirve cada uno: Tavily, Playwright, Context7, Engram — con Exa y Firecrawl como alternativas directas a Tavily. | [`mcps/MCPS.md`](mcps/MCPS.md) |
| **Skills** | 11 skills de agente, instaladas globalmente desde sus repos upstream con el CLI `skills` y compartidas por todo harness que lea `~/.agents/skills`. | [`skills/SKILLS.md`](skills/SKILLS.md) |

## Se usa con Gentle AI

Este repo es la mitad del setup; [**Gentle AI**](https://github.com/Gentleman-Programming/gentle-ai)
es la otra. Gentle AI es la capa de harness sobre [Pi](https://pi.dev): planifica, delega en subagentes
enfocados, revisa sus propios cambios y trae sus propias skills además de las once de abajo. Se instala
en Pi con `pi install npm:gentle-pi`.

También es de donde vienen **Context7** y **Engram** — por eso `mcps/MCPS.md` los lista sin pedirte que
los configures a mano.

Los dos son independientes. Aquí todo son documentos, así que puedes quedarte con el estándar, la lista
de MCPs y las skills y prescindir de Gentle AI.

## Estructura

```
.
├── README.md               este archivo (en)
├── README.es.md            este archivo (es)
├── AGENTS.md               reglas para trabajar en este repo (no es el estándar que instalas)
├── LICENSE                 MIT
├── standards/
│   ├── README.md           el estándar, índice (en)
│   ├── README.es.md        el estándar, índice (es)
│   ├── en/
│   │   ├── Engineering_standards.md
│   │   ├── adopt.md
│   │   └── examples/       AGENTS.md, README.md, un ADR, config de gates, CI
│   └── es/                 lo mismo, en español
├── mcps/
│   └── MCPS.md             los servidores MCP que uso
└── skills/
    └── SKILLS.md           comandos de instalación e inventario
```

## Cómo se usa

### 1. El estándar de ingeniería

Copia `standards/es/Engineering_standards.md` a tu repo (raíz o `docs/`) y pásale a tu agente de
código el prompt correspondiente de `standards/es/adoptar.md`: configura los gates para Python (uv) o
Node/React (pnpm) y crea un `README.md` y un `AGENTS.md` cortos. Un repo existente primero recibe una
auditoría de solo lectura y después un retrofit con un commit por paso.

Empieza en [`standards/README.es.md`](standards/README.es.md).

### 2. Servidores MCP

[`mcps/MCPS.md`](mcps/MCPS.md) lista los servidores y el bloque canónico `mcpServers`. Tradúcelo a la
forma que espere tu harness: todos son procesos stdio con `npx`, así que solo cambian las claves JSON
o TOML.

### 3. Skills

Las skills **no se vendorizan** aquí. Se instalan globalmente desde sus repos upstream con el CLI
[`skills`](https://skills.sh), que escribe en `~/.agents/skills/` — el directorio que leen OMP,
Claude Code y la mayoría de los harnesses:

```bash
# corre los dos comandos de skills/SKILLS.md y luego:
npx skills ls -g
npx skills update -g -y
```

Mira [`skills/SKILLS.md`](skills/SKILLS.md) para los comandos y el inventario.

### Arranque rápido (que lo haga un agente)

Abre cualquier agente de código — en cualquier directorio — y pega:

```text
Configura esta máquina desde https://github.com/umi008/dev-agent-setup (lee sus archivos por red;
raw.githubusercontent.com funciona bien). Haz exactamente esto:

1. Instala las skills globales corriendo literalmente cada comando de skills/SKILLS.md, luego corre
   `npx skills ls -g` y muéstrame el resultado.
2. Lee mcps/MCPS.md y dime, para cada servidor, cómo declararlo en el harness que estoy usando.
   Inspecciona solo el entorno: nunca imprimas valores de secretos ni los escribas a un archivo.
3. Reporta qué instalaste y qué me queda por configurar a mano.

Restricciones: usa los archivos publicados tal cual — no modifiques el repositorio ni inventes
archivos extra.
```

## Credenciales

En este repo no vive nada secreto. Estas las pones tú:

| Credencial | Cómo |
| --- | --- |
| **Tu proveedor de modelo** | Lo que espere tu harness — login OAuth (`/login` en OMP, `claude` login, `codex login`) o una API key como `ANTHROPIC_API_KEY` / `OPENROUTER_API_KEY` exportada desde tu shell rc. |
| **Tavily** (búsqueda web) | `export TAVILY_API_KEY=...` en tu shell rc. La entrada MCP la lee del entorno — aquí no se guarda ninguna key. Omite el servidor si tu harness ya habla con Tavily de forma nativa. |
| **Exa o Firecrawl** (solo si cambias Tavily) | `export EXA_API_KEY=...` o `export FIRECRAWL_API_KEY=...` en tu shell rc. El servidor hospedado de Exa también funciona sin key. |

Context7 y Playwright no necesitan credenciales.

## Notas

- **¿Vas a editar este repo?** `AGENTS.md` en la raíz tiene las convenciones. No es el estándar que
  instalas — ese es `standards/es/Engineering_standards.md`.
- **Las skills se quedan upstream.** `npx skills update -g` las mantiene al día en vez de congelar una
  copia aquí.

## Licencia

MIT — mira [`LICENSE`](LICENSE). Tómalo, hazle fork, recórtalo.
