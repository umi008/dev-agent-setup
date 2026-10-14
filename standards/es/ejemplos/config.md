# Config de referencia

Cada snippet se probó el 2026-10-14 en proyectos mínimos (Python, y React con Vite): los gates pasan en verde, y los de cero comentarios, coverage y secretos fallan cuando deben.

## Python

`.python-version`
```
3.12
```

`pyproject.toml`
```toml
[project]
name = "mi-servicio"
version = "0.1.0"
description = "Qué hace el servicio, en una línea"
requires-python = "==3.12.*"
dependencies = []

[dependency-groups]
dev = ["mypy", "pytest", "pytest-cov", "ruff"]

[tool.ruff]
line-length = 100

[tool.mypy]
strict = true

[tool.pytest.ini_options]
pythonpath = ["src"]
markers = ["integration: wiring real", "slow: lento", "e2e: flujo completo"]

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 80
```

`tests/test_sin_comentarios.py`: falla ante cualquier comentario, incluidas las supresiones (`noqa`, `type: ignore`).
```python
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_sin_comentarios() -> None:
    offenders = []
    for folder in ("src", "tests"):
        for path in (ROOT / folder).rglob("*.py"):
            with path.open("rb") as handle:
                for token in tokenize.tokenize(handle.readline):
                    if token.type == tokenize.COMMENT:
                        offenders.append(f"{path.relative_to(ROOT)}:{token.start[0]}")
    assert not offenders, offenders
```

`requires-python` es `==3.12.*`, no `>=3.12`: un rango contradiría el pin.

Primer uso: `uv lock && uv sync --locked`. Después, los gates de la tabla.

## Frontend (Node / React)

Setup. Nadie teclea una versión: `pnpm init` escribe el pin de pnpm y `pnpm runtime set` escribe el de Node.
```bash
pnpm init
pnpm runtime set node lts
pnpm add react react-dom
pnpm add -D typescript@6 vite @vitejs/plugin-react vitest @vitest/coverage-v8 jsdom @testing-library/react @testing-library/dom @types/react @types/react-dom @types/node@24 eslint typescript-eslint eslint-plugin-react-hooks prettier
```

`package.json` (solo lo relevante; las versiones son las que escribieron las herramientas el día de la prueba)
```json
{
  "type": "module",
  "private": true,
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run --coverage"
  },
  "devEngines": {
    "packageManager": { "name": "pnpm", "version": "12.11.2", "onFail": "download" },
    "runtime": { "name": "node", "version": "24.22.0", "onFail": "download" }
  },
  "packageManager": "pnpm@12.11.2"
}
```

`tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true
  },
  "include": ["src", "tests", "vite.config.ts"]
}
```

`.prettierignore`: `coverage`, `dist` y `pnpm-lock.yaml`. `.gitignore`: `node_modules`, `coverage`, `dist` y `.env`.

`vite.config.ts`
```ts
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["tests/setup.ts"],
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      thresholds: { lines: 80, functions: 80, statements: 80 },
    },
  },
});
```

`tests/setup.ts`
```ts
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(cleanup);
```

`tests/main.test.tsx`: el entrypoint se prueba, no se excluye del coverage.
```tsx
import { screen } from "@testing-library/react";
import { expect, test } from "vitest";

test("mounts the app in #root", async () => {
  document.body.innerHTML = '<div id="root"></div>';
  await import("../src/main");
  expect((await screen.findByRole("button")).textContent).toBe("Count: 0");
});
```

`eslint.config.js`: regla local que prohíbe todo comentario salvo JSDoc.
```js
import { defineConfig } from "eslint/config";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

const noComments = {
  meta: {
    type: "problem",
    schema: [],
    messages: { comment: "Only public API JSDoc is allowed." },
  },
  create(context) {
    return {
      Program() {
        for (const comment of context.sourceCode.getAllComments()) {
          const isJsdoc =
            comment.type === "Block" && comment.value.startsWith("*");
          if (!isJsdoc) {
            context.report({ loc: comment.loc, messageId: "comment" });
          }
        }
      },
    };
  },
};

export default defineConfig([
  { ignores: ["coverage", "dist"] },
  { linterOptions: { noInlineConfig: true } },
  tseslint.configs.recommended,
  reactHooks.configs.flat.recommended,
  {
    files: ["src/**/*.{ts,tsx}", "tests/**/*.{ts,tsx}"],
    plugins: { local: { rules: { "no-comments": noComments } } },
    rules: { "local/no-comments": "error" },
  },
]);
```

- **pnpm, no npm.** pnpm fija su propia versión y la de Node en `package.json` y el lockfile, y las descarga si faltan; npm solo valida `devEngines`. `pnpm self-update` sube el pin de pnpm a la última.
- **`noInlineConfig` es obligatorio.** Sin él, `/* eslint-disable */` apaga la propia `local/no-comments` y el gate no lo ve. Con él, ESLint ignora la directiva, la reporta y `--max-warnings 0` falla.
- **TypeScript 6, no 7.** El 2026-10-14 `typescript-eslint` 8.71.2 exige `typescript <6.1.0`. Cuando soporte el 7, se sube.
- **Hace falta `@types/node`.** `vitest/config` referencia tipos de Node y `tsc` falla sin ellos. Su major debe ser el del pin de Node.
- **Testing Library necesita `tests/setup.ts`.** Sin globals no limpia entre tests y el segundo falla con "Found multiple elements".
- **`react-hooks`** es parte del gate de lint: falla ante un hook llamado de forma condicional.

## Hooks y secretos

`.pre-commit-config.yaml` para Python. El `rev` va vacío y lo llena `pre-commit autoupdate`.
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: ""
    hooks:
      - id: ruff-check
      - id: ruff-format
  - repo: https://github.com/gitleaks/gitleaks
    rev: ""
    hooks:
      - id: gitleaks
      - id: gitleaks
        alias: secrets
        name: secrets (history)
        entry: gitleaks git --redact --verbose
        stages: [manual]
```

Para Node, se cambia el bloque de ruff por hooks locales y se conserva el de gitleaks:
```yaml
  - repo: local
    hooks:
      - id: eslint
        name: eslint
        entry: pnpm lint
        language: system
        pass_filenames: false
      - id: prettier
        name: prettier
        entry: pnpm format:check
        language: system
        pass_filenames: false
```

Instalar: `uvx --python 3.12 pre-commit autoupdate && uvx --python 3.12 pre-commit install`. Los hooks necesitan uv, también en proyectos Node.

- **Dos hooks de gitleaks a propósito.** `gitleaks` escanea solo lo que está en staging: bloquea el commit, pero en CI no hay nada en staging, así que pasa aunque ya haya un secreto commiteado. `secrets` escanea el historial y es el gate que corre el CI.
- **Se rota, no se borra.** Quitar el archivo no limpia el historial; el hallazgo sigue hasta que se rota el secreto y se limpia el historial.
- **Se fija el Python de `uvx`.** Sin `--python`, un proyecto sin `.python-version` (Node) recibe el CPython más nuevo, que compiló una dependencia desde fuente en un contenedor limpio.

## CI

Ver [`ci.md`](ci.md).
