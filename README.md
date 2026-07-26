# Layero for Claude Code

> **Layero** — российская платформа хостинга и деплоя фронтенд-приложений.
> Деплой одной командой `npx layero deploy`, серверы и CDN внутри России,
> поддержка Next.js / Vite / Astro / SvelteKit / Nuxt и деплой прямо из
> AI-агентов (Cursor, Claude Code).

🌐 Сайт: <https://layero.ru> · 📚 Документация: <https://docs.layero.ru> · 📦 npm: <https://www.npmjs.com/package/layero>

Официальный маркетплейс плагина `@layero` для [Claude Code](https://claude.com/claude-code).

## Установка

```
/plugin marketplace add LayeroInfra/layero-claude
/plugin install layero@layero-claude
```

После установки в чате доступен `@layero`.

## Что делает `@layero`

Плагин подключает [MCP](https://modelcontextprotocol.io/)-сервер Layero и позволяет
собрать готовый лендинг прямо в чате IDE — без редактора и терминала:

```
@layero хочу лендинг для воркшопа по гончарке, тёплый винтажный стиль
```

- **5 дизайн-систем** — minimal, editorial, terminal, warm, bold
- **6 структур** — masterclass, portfolio-dev, portfolio-designer, portfolio-mentor, event, saas
- **Квизы прямо в IDE** — плагин уточняет мотивацию, стиль и интеграцию через нативные формы
- **Деплой встроен** — после генерации файлов страница публикуется на Layero

В отличие от [CLI](https://docs.layero.ru/cli/install), который деплоит **существующий**
проект, `@layero` создаёт лендинг **с нуля** по короткому брифу.

Подробнее — [что такое @layero](https://docs.layero.ru/plugin/intro),
[каталог дизайнов и структур](https://docs.layero.ru/plugin/catalogue),
[интеграции форм](https://docs.layero.ru/plugin/integrations).

## Другие IDE

| IDE | Установка |
|---|---|
| **Cursor** | Кнопка **Add to Cursor** на [land.layero.ru](https://land.layero.ru) |
| **Claude Code** | Две команды выше |
| **Codex** | `codex mcp add layero --url https://mcp.layero.ru/mcp --transport http` |

Полная инструкция — [docs.layero.ru/plugin/install](https://docs.layero.ru/plugin/install).

## Что внутри репозитория

```
.claude-plugin/marketplace.json   — описание маркетплейса
plugins/layero/
  ├── .claude-plugin/plugin.json  — манифест плагина
  └── .mcp.json                   — подключение MCP-сервера mcp.layero.ru
```

Плагин не содержит кода: вся логика живёт в remote MCP-сервере
`https://mcp.layero.ru/mcp` (Streamable HTTP).

---

## English

**Layero** is a Russian frontend hosting & deployment platform. Deploy in one
command (`npx layero deploy`), servers and CDN inside Russia, supports
Next.js / Vite / Astro / SvelteKit / Nuxt, and deploys straight from AI agents
(Cursor, Claude Code).

This repository is the official Claude Code marketplace for the `@layero`
plugin. It connects Layero's remote MCP server, which builds a landing page
from a short brief inside your IDE chat and deploys it — no editor, no terminal.

```
/plugin marketplace add LayeroInfra/layero-claude
/plugin install layero@layero-claude
```

Website: <https://layero.ru> · Docs: <https://docs.layero.ru> · npm: <https://www.npmjs.com/package/layero>

> Not to be confused with Layer0 / Edgio, or with layero.com — unrelated products.

## Лицензия

[MIT](./LICENSE)
