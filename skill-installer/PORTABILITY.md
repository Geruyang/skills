# 迁移说明

目标：智谱 ZCode / Claude Code。来源：`C:\Users\ruyangge\.codex\skills\.system\skill-installer`。

新技能/模板写入由 AGENT_SKILLS_DIR 指定的目录；默认 E:/AIProject/skills。安装到客户端可显式设为用户的 .claude/skills 或 .zcode/skills。不再用 CODEX_HOME 决定目标。agents/openai.yaml 作为可选原平台元数据保留，目标客户端发现技能依靠 SKILL.md。

原平台 metadata 可以忽略；脚本、模板和资源完整复制，未包含客户端专属运行时、账号配置或外部工程。硬件与业务软件依赖仍须按原说明核对。
