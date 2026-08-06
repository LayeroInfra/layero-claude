#!/usr/bin/env python3
"""Сверяет плагин для Cursor с тем, что Cursor на самом деле читает.

Зачем. 06.08.2026 выяснилось, что диплинк `cursor://…/mcp/install` на новых
сборках Cursor не ставит сервер вообще: он лишь кладёт «предложение» в память,
а карточку подтверждения рисует старая панель настроек, которая после миграции
на редактор Customize больше не открывается. Рабочий путь остался один —
плагин в маркетплейсе (`/plugin/add?id=…`), и этот файл сторожит его форму.

Что проверяется:

1. Манифесты разбираются, имена подходят под регэксп загрузчика Cursor
   (`^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$`), `source` указывает на живую папку.
2. Логотип по указанному пути существует.
3. Правило и навык в папке плагина совпадают байт в байт с оригиналами в корне
   репозитория. Копии разъезжаются молча — это отдельный класс наших аварий.
4. Конфиг MCP: адрес канонический, тип http и — главное — НЕТ подстановок вида
   `${VAR}`. Cursor понимает только `${env:VAR}`; неразвёрнутая строка уходит
   на сервер как есть, и пользователь получает «Токен не принят: Invalid token»
   вместо честного «токена нет». Ровно поэтому у плагина для Cursor заголовок
   Authorization отсутствует, а у плагина для Claude Code он остаётся.
5. `_meta.ideToolTitles` сверяется с живым `tools/list` — подписи стареют так же
   тихо, как всё остальное скопированное. `--offline` пропускает этот шаг.

Запуск: python3 check-cursor-plugin.py [--offline]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP_URL = "https://mcp.layero.ru/mcp"
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$")
# Загрузчик Cursor (extensions/cursor-agent-exec) берёт первый из этих файлов.
MCP_FILES = (".mcp.json", "mcp.json")
# Копии внутри плагина ↔ оригиналы в корне репозитория.
MIRRORED = (
    ("rules/layero-deployment.mdc", "rules/layero-deployment.mdc"),
    ("skills/deploy-to-layero/SKILL.md", "skills/deploy-to-layero/SKILL.md"),
)

failures: list = []


def fail(msg: str) -> None:
    print("  ✗ " + msg)
    failures.append(msg)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"нет файла {path.relative_to(ROOT)}")
    except ValueError as exc:
        fail(f"{path.relative_to(ROOT)}: не разбирается — {exc}")
    return None


def live_tool_names():
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "check-cursor-plugin", "version": "1"},
                },
            }
        ).encode(),
        headers={
            "content-type": "application/json",
            "accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        session = resp.headers.get("mcp-session-id")
        resp.read()
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}).encode(),
        headers={
            "content-type": "application/json",
            "accept": "application/json, text/event-stream",
            "mcp-session-id": session or "",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        body = resp.read().decode("utf-8")
    line = [l for l in body.splitlines() if l.startswith("data: ")][-1][6:]
    return {t["name"] for t in json.loads(line)["result"]["tools"]}


def check_mcp(plugin_dir: Path) -> dict:
    path = next((plugin_dir / n for n in MCP_FILES if (plugin_dir / n).is_file()), None)
    if path is None:
        fail(f"{plugin_dir.name}: нет ни одного из {', '.join(MCP_FILES)}")
        return {}
    cfg = load(path) or {}
    servers = cfg.get("mcpServers", {})
    if list(servers) != ["layero"]:
        fail(f"{path.name}: ожидался единственный сервер `layero`, а не {list(servers)}")
    server = servers.get("layero", {})
    if server.get("url") != MCP_URL:
        fail(f"{path.name}: адрес {server.get('url')!r} вместо {MCP_URL}")
    if server.get("type") != "http":
        fail(f"{path.name}: тип {server.get('type')!r} вместо 'http'")
    blob = json.dumps(server, ensure_ascii=False)
    for var in re.findall(r"\$\{(?!env:)([^}]+)\}", blob):
        fail(
            f"{path.name}: подстановка ${{{var}}} — Cursor её не раскроет и отправит "
            "строку как есть; допустима только форма ${env:VAR}"
        )
    return server


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="не ходить на живой MCP")
    args = ap.parse_args()

    market = load(ROOT / ".cursor-plugin" / "marketplace.json")
    if market is None:
        return 1
    entries = market.get("plugins", [])
    if not entries:
        fail("marketplace.json: пустой список plugins")

    checked = 0
    for entry in entries:
        source = ROOT / entry.get("source", "")
        if not source.is_dir():
            fail(f"marketplace.json: source {entry.get('source')!r} не существует")
            continue
        manifest = load(source / ".cursor-plugin" / "plugin.json")
        if manifest is None:
            continue
        checked += 1
        name = manifest.get("name", "")
        if not NAME_RE.match(name):
            fail(f"{source.name}: имя {name!r} не подходит под регэксп загрузчика Cursor")
        if name != entry.get("name"):
            fail(f"{source.name}: имя в plugin.json ({name!r}) ≠ имени в marketplace.json ({entry.get('name')!r})")
        logo = manifest.get("logo")
        if logo and not (source / logo).is_file():
            fail(f"{source.name}: логотип {logo!r} не найден")

        for inside, origin in MIRRORED:
            copy, src = source / inside, ROOT / origin
            if not copy.is_file():
                fail(f"{source.name}: нет {inside}")
            elif not src.is_file():
                fail(f"нет оригинала {origin} — обновите MIRRORED")
            elif copy.read_bytes() != src.read_bytes():
                fail(f"{source.name}: {inside} разошёлся с {origin}")

        server = check_mcp(source)
        titles = server.get("_meta", {}).get("ideToolTitles", {})
        if titles and not args.offline:
            try:
                live = live_tool_names()
            except Exception as exc:  # noqa: BLE001
                print(f"  ⚠ живой tools/list недоступен ({exc}) — подписи не сверены")
            else:
                for extra in sorted(set(titles) - live):
                    fail(f"{source.name}: подпись для снятого инструмента `{extra}`")
                for missing in sorted(live - set(titles)):
                    fail(f"{source.name}: нет подписи для инструмента `{missing}`")

    print(f"проверено плагинов: {checked}")
    if failures:
        print(f"\nрасхождений: {len(failures)}")
        return 1
    print("плагин для Cursor сходится с манифестами, оригиналами и живым сервером")
    return 0


if __name__ == "__main__":
    sys.exit(main())
