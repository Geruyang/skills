# 迁移说明

目标：智谱 ZCode / Claude Code。来源：`C:\Users\ruyangge\.codex\plugins\cache\openai-bundled\computer-use\26.1007.21434\skills\computer-use`。

本技能原先使用 Codex/ChatGPT 专属服务。先检查目标客户端是否具备对应能力；有等价工具才按其实际接口执行。缺少能力时只完成可验证的本地部分，并说明缺少的集成。不得把工具名改成 Claude/ZCode 工具名后假定功能存在。

使用当前可用的浏览器/桌面自动化工具并阅读其 API 文档。@oai/sky、cua_node、node_repl 是原平台运行时，导出不会提供这些运行时。随附 docs 仅在同一运行时可用时参考。

原平台 metadata 可以忽略；脚本、模板和资源完整复制，未包含客户端专属运行时、账号配置或外部工程。硬件与业务软件依赖仍须按原说明核对。
