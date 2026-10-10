# 智谱 ZCode 运行说明

技能用当前 ZCode 会话中实际可用的工具执行。按客户端技能机制加载 SKILL.md；读取、搜索、编辑、终端、待办及子 Agent 能力以当前工具目录为准，不把 Codex 的 spawn_agent、followup_task、wait_agent 或 config.toml 当成 ZCode API。

技能位于 `~/.zcode/skills/<name>/SKILL.md`，更新后在“设置 → 技能”刷新并按需启用；可用 `$skill-name` 或斜杠菜单调用。子 Agent 的角色文件和模型参数须按本机 ZCode 的配置向导/官方文档核对。当前环境没有子 Agent 时，可在用户允许且任务适用的情况下按 executing-plans 顺序执行；不得把普通终端进程描述为客户端原生子 Agent。

参考：[ZCode 技能官方说明](https://zcode.z.ai/cn/docs/skill)。
