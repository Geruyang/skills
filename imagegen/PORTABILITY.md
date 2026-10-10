# 迁移说明

目标：智谱 ZCode / Claude Code。来源：`C:\Users\ruyangge\.codex\skills\.system\imagegen`。

优先使用当前已配置的图像生成服务，按实际返回路径保存。没有服务时可使用随附 scripts/image_gen.py，但需用户允许调用 API 且具备 OPENAI_API_KEY；不得假定目标客户端自带 image_gen。脚本以项目当前可用的 Python 执行。

原平台 metadata 可以忽略；脚本、模板和资源完整复制，未包含客户端专属运行时、账号配置或外部工程。硬件与业务软件依赖仍须按原说明核对。
