#!/usr/bin/env python3
"""Consistency checks for this repository — the same ones CI runs.

Run locally with `python3 scripts/check_sync.py`. Standard library only.
Exits non-zero with a list of failures when any invariant is broken.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

SKILL_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
LOCK_ENTRY_KEYS = {"source", "sourceType", "skillPath", "computedHash"}
SKIP_DIRS = {".git", "node_modules", ".venv"}

# Conservative, high-signal patterns: machine-specific paths and common
# credential shapes. Referenced env vars like ${TAVILY_API_KEY} are fine.
SECRET_PATTERNS = [
    ("machine-specific path", re.compile(r"(?<![A-Za-z0-9_])/(?:home|Users)/[A-Za-z0-9._-]")),
    ("machine-specific path", re.compile(r"[A-Za-z]:\\{1,2}Users\\")),
    ("API key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Tavily key", re.compile(r"\btvly-[A-Za-z0-9]{10,}")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def walk_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path != SELF and not (set(path.relative_to(ROOT).parts) & SKIP_DIRS)
    )


def load_json(path: Path) -> object:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(f"{rel(path)}: invalid JSON — {exc}")
        return None


# --- checks -----------------------------------------------------------------


def check_json_files() -> None:
    """every .json file parses"""
    for path in walk_files():
        if path.suffix == ".json":
            load_json(path)


def check_mcp_servers() -> None:
    """mcp/mcp-servers.json is a stdio-only mcpServers block with env placeholders"""
    servers = load_json(ROOT / "mcp" / "mcp-servers.json")
    if servers is None:
        return
    block = servers.get("mcpServers") if isinstance(servers, dict) else None
    if not isinstance(block, dict) or not block:
        fail("mcp/mcp-servers.json: missing or empty top-level `mcpServers` object")
        return
    for name, entry in block.items():
        args = entry.get("args") if isinstance(entry, dict) else None
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("command"), str)
            or not isinstance(args, list)
            or not all(isinstance(arg, str) for arg in args)
        ):
            fail(f"mcp/mcp-servers.json: `{name}` needs a string `command` and a string-list `args`")
            continue
        for key, value in (entry.get("env") or {}).items():
            if not isinstance(value, str) or not re.fullmatch(r"\$\{[A-Z][A-Z0-9_]*\}", value):
                fail(f"mcp/mcp-servers.json: `{name}.env.{key}` must be a ${{VAR}} placeholder, never a literal")


def check_skill_sync() -> None:
    """skill set matches across skills-lock.json, skills/SKILLS.md and rules/AGENTS.md"""
    lock = load_json(ROOT / "skills-lock.json")
    entries = lock.get("skills") if isinstance(lock, dict) else None
    if not isinstance(entries, dict) or not entries:
        fail("skills-lock.json: missing or empty top-level `skills` object")
        return

    locked: set[str] = set()
    sources: dict[str, str] = {}
    for name, entry in entries.items():
        if not SKILL_NAME.fullmatch(name):
            fail(f"skills-lock.json: `{name}` is not a kebab-case skill name")
        if not isinstance(entry, dict) or set(entry) != LOCK_ENTRY_KEYS:
            fail(f"skills-lock.json: `{name}` must have exactly {sorted(LOCK_ENTRY_KEYS)}")
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", entry["computedHash"]):
            fail(f"skills-lock.json: `{name}` has a malformed computedHash")
        locked.add(name)
        sources[name] = entry["source"]

    skills_md = read(ROOT / "skills" / "SKILLS.md")

    commands = re.finditer(r"npx skills add (\S+)(.*?)(?=\n\s*npx skills add|\Z)", skills_md.replace("\\\n", " "), re.DOTALL)
    installed: set[str] = set()
    for command in commands:
        source = command.group(1)
        for name in re.findall(r"-s\s+(\S+)", command.group(2)):
            installed.add(name)
            if sources.get(name) != source:
                fail(f"skills/SKILLS.md: `{name}` is installed from {source} but pinned to {sources.get(name, 'nothing')} in skills-lock.json")
    if installed != locked:
        fail(
            "skills/SKILLS.md install commands vs skills-lock.json: "
            f"only in SKILLS.md {sorted(installed - locked)}, only in lockfile {sorted(locked - installed)}"
        )

    inventory_block = skills_md.split("## Inventory", 1)[1] if "## Inventory" in skills_md else ""
    inventory: set[str] = set()
    for line in inventory_block.splitlines():
        row = re.match(r"\|\s*\[[^\]]+\]\([^)]+\)\s*\|([^|]+)\|", line)
        if row:
            inventory.update(item.strip() for item in row.group(1).split(",") if item.strip())
    if inventory != locked:
        fail(
            "skills/SKILLS.md inventory table vs skills-lock.json: "
            f"only in the table {sorted(inventory - locked)}, only in lockfile {sorted(locked - inventory)}"
        )

    named = set()
    for line in read(ROOT / "rules" / "AGENTS.md").splitlines():
        if "skill" in line.lower():
            named.update(token for token in re.findall(r"`([^`]+)`", line) if SKILL_NAME.fullmatch(token))
    missing = sorted(named - locked)
    if missing:
        fail(f"rules/AGENTS.md names skills outside the installed set: {missing}")

    for label, text in {"README.md": read(ROOT / "README.md"), "skills/SKILLS.md": skills_md}.items():
        counts = {int(count) for count in re.findall(r"\b(\d+)\s+(?:[a-z-]+\s+)?skills\b", text)}
        if counts != {len(locked)}:
            fail(f"{label}: declared skill counts {sorted(counts)} do not match the {len(locked)} skills in skills-lock.json")


def check_no_secrets() -> None:
    """no secrets or machine-specific paths in any tracked file"""
    for path in walk_files():
        try:
            text = read(path)
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pattern in SECRET_PATTERNS:
                match = pattern.search(line)
                if match:
                    context = (line[: match.start()].strip() or "…")[-60:]
                    fail(f"{rel(path)}:{lineno}: {label} — {context}[redacted]")


CHECKS = [
    ("JSON files parse", check_json_files),
    ("MCP block shape", check_mcp_servers),
    ("skill set in sync", check_skill_sync),
    ("no secrets or machine paths", check_no_secrets),
]


def main() -> int:
    for label, check in CHECKS:
        before = len(failures)
        check()
        print(f"[{'ok' if len(failures) == before else 'FAIL'}] {label}")
    if failures:
        print(f"\n{len(failures)} problem(s) found:")
        for message in failures:
            print(f"  - {message}")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
