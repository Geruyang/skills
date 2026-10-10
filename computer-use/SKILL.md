---
name: computer-use
description: Control Windows apps from ChatGPT
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。

本技能原先使用 Codex/ChatGPT 专属服务。先检查目标客户端是否具备对应能力；有等价工具才按其实际接口执行。缺少能力时只完成可验证的本地部分，并说明缺少的集成。不得把工具名改成 Claude/ZCode 工具名后假定功能存在。

使用当前可用的浏览器/桌面自动化工具并阅读其 API 文档。@oai/sky、cua_node、node_repl 是原平台运行时，导出不会提供这些运行时。随附 docs 仅在同一运行时可用时参考。

# Computer Use

Use this skill to automate the UI of Microsoft Windows apps. It uses SendInput, UI Automation, and Windows.Graphics.Capture screenshots that work even when windows are occluded.

If this plugin is available, read this entire `SKILL.md` once before Windows automation work, before saying Computer Use is unavailable, and before falling back to other Windows automation.

Start with the directions in the Initialize section below. Read these bundled Markdown files relative to this `SKILL.md` when you need information about the specific topic they cover:

- `references/plugin-shared/guidance.md`: core runtime behavior, target-window workflow, screenshot handling, and recovery guidance. You MUST read this before controlling Windows apps.
- `references/plugin-shared/api.md`: full `sky` API reference. Read this when you need method signatures or object shapes.
- `references/plugin-shared/confirmations.md`: you MUST read this before deciding whether a Windows UI action needs confirmation

## Initialize

The bundled `cua_node` `@oai/sky` package is the core entry point for Computer Use. Import it directly by package name from the JavaScript session. Do not spawn `codex-computer-use.exe`, search for the helper executable, or build a custom helper protocol client.

Run this once per fresh `node_repl` JavaScript session:

```js
if (!globalThis.sky) {
  const { sky } = await import("@oai/sky");
  globalThis.sky = sky;
}
```
