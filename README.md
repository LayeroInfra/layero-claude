# Layero for Claude Code

**[English](#english)** · Русский

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

## Как плагин себя ведёт

Правила поведения `@layero` — тон, что он решает сам, чего не делает никогда —
зафиксированы в [SOUL.md](./SOUL.md). Этот файл загружается в каждый диалог
как контекст высшего приоритета, так что он же и есть описание того, чего
ждать от плагина.

## Что внутри репозитория

```
.claude-plugin/marketplace.json   — описание маркетплейса
server.json                       — запись в официальном MCP-реестре
SOUL.md                           — правила поведения плагина
.mcp.json                         — подключение MCP-сервера из корня
rules/layero-deployment.mdc       — правило для Cursor: деплой через CLI
skills/deploy-to-layero/SKILL.md  — Agent Skill с тем же сценарием
plugins/layero/
  ├── .claude-plugin/plugin.json  — манифест плагина
  └── .mcp.json                   — подключение MCP-сервера mcp.layero.ru
```

Корневые `.mcp.json`, `rules/` и `skills/` лежат по стандарту
[Open Plugins](https://open-plugins.com) — по ним репозиторий находят сканеры
каталогов. Для самого плагина Claude Code источник правды — `plugins/layero/`.

Плагин не содержит кода: вся логика живёт в remote MCP-сервере
`https://mcp.layero.ru/mcp` (Streamable HTTP).

---

## English

**Layero** is a frontend hosting and deployment platform whose build servers
and CDN sit inside Russia — which is the point: sites load fast for Russian
visitors without a VPN, and deploys do not cross the border. It ships a local
directory in one command (`npx layero deploy`), with framework detection for
Next.js, Vite, Astro, SvelteKit and Nuxt.

This repository is the official Claude Code marketplace for the `@layero`
plugin, and the source of record for Layero's remote MCP server.

### Install

```
/plugin marketplace add LayeroInfra/layero-claude
/plugin install layero@layero-claude
```

| IDE | How |
|---|---|
| **Claude Code** | the two commands above |
| **Cursor** | the **Add to Cursor** button on [land.layero.ru](https://land.layero.ru) |
| **Codex** | `codex mcp add layero --url https://mcp.layero.ru/mcp --transport http` |

The server is remote (Streamable HTTP at `https://mcp.layero.ru/mcp`), so
there is nothing to install locally and no Node process on your side.

### What it does

It is not only a page generator. The endpoint currently exposes **16 tools**
covering the whole life of a site:

- **build** — `list_design_systems`, `list_structures`, `compose_landing`
- **ship** — `publish_landing`, `add_integration`
- **operate** — `site_status`, `diagnose_deploy`, `check_performance`
- **setup** — `env_vars`, `connect_domain`, `check_domain`, `list_domains`
- **analytics** — `connect_analytics`, `site_analytics`
- **account** — `whoami`, `my_projects`

Ask it for a landing page and it runs two or three short quizzes as native
IDE forms (through MCP elicitation), writes the files, and publishes them.
Later you can ask why a build failed, attach a custom domain, or compare page
speed against the previous deploy — in the same conversation.

The plugin ships no code of its own: all logic lives in the remote server.
How it behaves — what it decides on its own, what it never does — is written
down in [SOUL.md](./SOUL.md), which is loaded into every conversation as
top-priority context.

### Also in this repository

- [`rules/layero-deployment.mdc`](./rules/layero-deployment.mdc) — a Cursor
  rule for deploying an **existing** project through the CLI
- [`skills/deploy-to-layero/SKILL.md`](./skills/deploy-to-layero/SKILL.md) —
  the same procedure as a standalone Agent Skill
- [`server.json`](./server.json) — the record published to the official
  [MCP registry](https://registry.modelcontextprotocol.io) as `ru.layero/layero`

Docs: <https://docs.layero.ru/en/plugin/intro/> · Website: <https://layero.ru> ·
npm: <https://www.npmjs.com/package/layero>

> Not to be confused with Layer0 / Edgio, or with layero.com — unrelated products.

## Лицензия

[MIT](./LICENSE)
