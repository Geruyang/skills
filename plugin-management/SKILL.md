---
name: plugin-management
description: Discover and suggest relevant plugins, inspect app permissions and dependencies, and manage plugin connections or removal. Use when the user asks about plugins or when a task would materially benefit from an external app, account, service, or data source that available tools cannot access.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。

本技能原先使用 Codex/ChatGPT 专属服务。先检查目标客户端是否具备对应能力；有等价工具才按其实际接口执行。缺少能力时只完成可验证的本地部分，并说明缺少的集成。不得把工具名改成 Claude/ZCode 工具名后假定功能存在。

# Plugin Management

Use the Plugin Management app to discover useful integrations and manage
existing plugins. Choose the most direct capability for the user's task before
searching for anything new.

## Choose the right capability

1. Use an available built-in tool when it already provides the needed
   capability. General web search, image generation, memory, and sites do not
   require a plugin unless the user requests a specific external provider or a
   capability unavailable natively.
2. Use an already connected plugin when it can complete the task.
3. Search for a plugin when an external app, account, service, or data source
   would materially improve the result and no available tool can access it.

Infer plugin intent from the user's actual task. Requests involving email,
calendars, messaging, documents, project management, customer systems, finance,
or analytics may need an external integration even when the user never says
"plugin," "install," or "connect."

Before saying an external service is unavailable, requesting pasted data, or
proposing a manual workaround, determine whether a relevant plugin exists.

## Find and suggest plugins

Call `search_plugins` with concise provider names, product names, or capability
keywords. For example, use `Gmail`, `calendar`, or `project management`, not
the entire user request. The currently available tools and any recommended
plugin list are not a complete directory.

When a relevant unconnected plugin would help, call `suggest_plugins` with its
exact returned plugin ID. Suggest the smallest useful set, preferably three or
fewer. Do not suggest plugins that are already installed or already pending.

Suggestions do not block the task. Continue any work that does not require the
connection and briefly explain what still needs the user's action. Never claim
a plugin is installed or connected without verification. Use its tools only
after its individual connection is confirmed.

## Manage existing plugins

- Use `get_app_permissions` to inspect a plugin's permissions.
- Use `update_app_permissions` only for a permission change the user requested.
  Ask before ambiguous, broad, or risky changes.
- Use `get_plugin_dependencies` to inspect required apps or dependencies.
- Use `uninstall_app` only when the user explicitly requests removal. Correct
  an obvious spelling mistake when the intended plugin is unambiguous, and pass
  its actual name without inventing an identifier.

Keep user-facing explanations focused on the task, connection state, and
requested change. Do not expose internal tool names or claim actions happened
without checking their results.
