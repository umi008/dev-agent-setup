# Reference config

Every snippet was tested on 2026-10-14 in minimal projects (Python, and React with Vite): the gates pass green, and the zero-comments, coverage and secrets gates fail when they should.

## Python

`.python-version`
```
3.12
```

`pyproject.toml`
```toml
[project]
name = "my-service"
version = "0.1.0"
description = "What the service does, in one line"
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
markers = ["integration: real wiring", "slow: slow", "e2e: full flow"]

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 80
```

`tests/test_no_comments.py`: fails on any comment, suppressions included (`noqa`, `type: ignore`).
```python
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_no_comments() -> None:
    offenders = []
    for folder in ("src", "tests"):
        for path in (ROOT / folder).rglob("*.py"):
            with path.open("rb") as handle:
                for token in tokenize.tokenize(handle.readline):
                    if token.type == tokenize.COMMENT:
                        offenders.append(f"{path.relative_to(ROOT)}:{token.start[0]}")
    assert not offenders, offenders
```

`requires-python` is `==3.12.*`, not `>=3.12`: a range would contradict the pin.

First use: `uv lock && uv sync --locked`. Then, the gates from the table.

## Frontend (Node / React)

Setup. Nobody types a version: `pnpm init` writes the pnpm pin and `pnpm runtime set` writes the Node pin.
```bash
pnpm init
pnpm runtime set node lts
pnpm add react react-dom
pnpm add -D typescript@6 vite @vitejs/plugin-react vitest @vitest/coverage-v8 jsdom @testing-library/react @testing-library/dom @types/react @types/react-dom @types/node@24 eslint typescript-eslint eslint-plugin-react-hooks prettier
```

`package.json` (relevant parts only; the versions are what the tools wrote on the test date)
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

`.prettierignore`: `coverage`, `dist` and `pnpm-lock.yaml`. `.gitignore`: `node_modules`, `coverage`, `dist` and `.env`.

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

`tests/main.test.tsx`: the entrypoint is tested, not excluded from coverage.
```tsx
import { screen } from "@testing-library/react";
import { expect, test } from "vitest";

test("mounts the app in #root", async () => {
  document.body.innerHTML = '<div id="root"></div>';
  await import("../src/main");
  expect((await screen.findByRole("button")).textContent).toBe("Count: 0");
});
```

`eslint.config.js`: local rule that forbids every comment except JSDoc.
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

- **pnpm, not npm.** pnpm pins itself and Node in `package.json` and the lockfile, and downloads them when missing; npm only validates `devEngines`. `pnpm self-update` bumps the pnpm pin to the latest.
- **`noInlineConfig` is mandatory.** Without it, `/* eslint-disable */` switches off `local/no-comments` itself and the gate does not see it. With it, ESLint ignores the directive, reports it and `--max-warnings 0` fails.
- **TypeScript 6, not 7.** On 2026-10-14 `typescript-eslint` 8.71.2 requires `typescript <6.1.0`. Once it supports 7, bump it.
- **`@types/node` is needed.** `vitest/config` references Node types and `tsc` fails without them. Keep its major equal to the Node pin.
- **Testing Library needs `tests/setup.ts`.** Without globals it does not clean up between tests and the second one fails with "Found multiple elements".
- **`react-hooks`** is part of the lint gate: it fails on a hook called conditionally.

## Hooks and secrets

`.pre-commit-config.yaml` for Python. `rev` is left empty and `pre-commit autoupdate` fills it.
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

For Node, replace the ruff block with local hooks and keep the gitleaks block:
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

Install: `uvx --python 3.12 pre-commit autoupdate && uvx --python 3.12 pre-commit install`. The hooks need uv, also in Node projects.

- **Two gitleaks hooks on purpose.** `gitleaks` scans only the staged changes: it blocks the commit, but in CI nothing is staged, so it passes even with a secret already committed. `secrets` scans the history and is the gate that CI runs.
- **Rotate, do not delete.** Removing the file does not clear the history; the finding stays until the secret is rotated and the history is cleaned.
- **Pin the Python of `uvx`.** Without `--python`, a project with no `.python-version` (Node) gets the newest CPython, which built a dependency from source in a clean container.

## CI

See [`ci.md`](ci.md).
