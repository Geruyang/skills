# Codex 技能导出与迁移

导出日期：2026-10-10。目标目录：`E:\AIProject\skills`。目标客户端：智谱 ZCode、Claude Code CLI。

本目录包含 167 个技能，采用单层 `<skill-name>/SKILL.md` 结构，保留 scripts、references、assets、templates、examples 及相关许可证。范围包含 `~/.codex/skills`、`~/.agents/skills` 和本机 Codex 插件缓存中所有找到的技能，缓存技能可能未在当前会话启用。

## 导入

下面命令只用于你决定导入时执行；导出任务未替你安装到客户端。

在 Windows PowerShell 中先预览：

```powershell
powershell -ExecutionPolicy Bypass -File 'E:\AIProject\skills\Import-Skills.ps1' -Client claude -WhatIf
powershell -ExecutionPolicy Bypass -File 'E:\AIProject\skills\Import-Skills.ps1' -Client zcode -WhatIf
```

确认选择后去掉 `-WhatIf` 执行：

```powershell
powershell -ExecutionPolicy Bypass -File 'E:\AIProject\skills\Import-Skills.ps1' -Client claude
powershell -ExecutionPolicy Bypass -File 'E:\AIProject\skills\Import-Skills.ps1' -Client zcode
```

脚本分别复制到当前 Windows 用户的 `%USERPROFILE%\.claude\skills` 与 `%USERPROFILE%\.zcode\skills`，遇到同名目录会跳过，保留已有文件。可通过 `-Destination '路径'` 指定其他用户或项目目录；在 PowerShell 内直接调用脚本时可通过 `-Names keil,jlink,serial` 只导入选定技能。导入脚本不修改任何客户端的权限设置或全局指令。

Claude Code 用户技能位置为 `~/.claude/skills/<name>/SKILL.md`，可使用 `/skill-name` 调用。[Claude Code 官方说明](https://code.claude.com/docs/en/skills)

智谱 ZCode 用户技能位置为 `~/.zcode/skills/<name>/SKILL.md`。导入后在“设置 → 技能”刷新、按需启用，可以用 `$skill-name` 或斜杠菜单调用。也可先导入 Claude Code，再在 ZCode 的“设置 → 技能 → 导入”扫描 Claude Code 来源，选择复制。插件分发采用单层技能目录。[ZCode 官方说明](https://zcode.z.ai/cn/docs/skill)

若 Claude Code 运行在 WSL/Linux 中，Windows 用户目录不是它的用户技能目录；将需要的技能完整复制到该 Linux 用户的 `~/.claude/skills`，或在该环境创建可访问的目录链接。Windows 上的 E 盘路径与硬件命令要按运行环境调整。

## 本次适配

- 统一为合法、小写、唯一的技能名称。个人 `pdf` 保留原名，插件版为 `pdf-artifacts`，两套内容均保留。
- 将插件前缀式技能引用改为导出后的技能名；保留有效的跨技能相对链接。
- 修改技能目录和 Python 调用路径，UI UX Pro Max 不再绑定 AiStock 项目目录；原来的目录链接被复制为真实文件。
- 修改 skill-installer 的 Python 安装/列表脚本和 template-creator 的 Node 脚本，使默认目标为本导出库；可以显式设置 `AGENT_SKILLS_DIR`。原平台 `CODEX_HOME` 不再决定这些脚本的默认写入位置。
- 每个入口附有跨客户端运行约定；平台专属运行时要求由该约定覆盖。普通 Markdown 链接替代平台专属呈现指令，Office 文档工作允许使用目标环境已经核实可用的库。
- 保留 Codex/OpenAI 产品研究资料中的真实产品名称、URL、API 和代码接口名称，避免把产品资料误改成其他产品。
- 补齐技能目录之外能定位的插件共享文档。没有随导出打包账号、令牌、客户端配置、专属服务或硬件/工程目录。

每个技能的 `PORTABILITY.md` 记录来源和限制；`COMPATIBILITY.md` 是总清单；`migration-manifest.json` 包含源文件哈希、修改文件列表和共享资源，便于追溯。

## 使用边界

“技能已导入”表示指令和配套文件可被读取，不表示相关服务已安装。Computer Use、ChatGPT Pages/Pets、Excel 实时控制等需要对应服务或等价集成；Slack/日历需要账号授权；@oai/artifact-tool 等专属包不随技能复制。苏晴相关技能仍依赖 `E:\AIProject\ChatBot` 项目及其后端；硬件技能仍需 Keil、J-Link、串口、Vivado 等实际工具。

普通工具缺失时先检查实际环境并说明依赖，不得虚构 Codex 工具在目标客户端存在。脚本默认写入导出库；若希望新技能直接被某个客户端发现，运行前设置：

```powershell
$env:AGENT_SKILLS_DIR = Join-Path $env:USERPROFILE '.claude\skills'
# 或：
$env:AGENT_SKILLS_DIR = Join-Path $env:USERPROFILE '.zcode\skills'
```

建议导入后只启用当前工作需要的技能。全部技能的元数据会消耗客户端上下文；ZCode 官方说明指出大量启用技能可能使元数据退化为只保留名称。[ZCode 数量与上下文说明](https://zcode.z.ai/cn/docs/skill)

`CLIENT-RULES.md` 保留你在本次任务中提供的两个个人必用技能规则，可手动合并到 Claude Code 的 `CLAUDE.md` 或 ZCode 的 `AGENTS.md`。该文件没有自动写入全局配置。

## 验证范围

验证包括 YAML 元数据、资源完整性、源文件未修改、入口链接与名称、Python 语法和修改后的路径行为、导入脚本的实际临时目录复制。详见 `VALIDATION.json`。未在 ZCode/Claude Code 中对全部技能进行完整业务实测；外部项目、硬件、云端 API 和专属工具的运行效果不由本次导出保证。
