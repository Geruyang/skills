# 迁移说明

目标：智谱 ZCode / Claude Code。来源：`C:\Users\ruyangge\.codex\plugins\cache\openai-primary-runtime\template-creator\26.1007.11041\skills\template-creator`。

文档/表格/幻灯片的本地工作使用目标环境中已经验证可用的 Python/Node 与库。可用 python-docx、openpyxl、PptxGenJS/python-pptx、pypdf/pdfplumber 和 LibreOffice/Poppler；选择与任务相符的工具，保留渲染和质量验证。原文的 load_workspace_dependencies、@oai/artifact-tool、artifact_session 和操作开始计量脚本只在实际存在且适用时执行，不作为其他客户端的前置门槛。展示结果用普通 Markdown 文件链接，替代 :codex-file-citation 等专属标记。云端编辑/导入必须具备对应集成，本地文件不能冒充云端结果。

新技能/模板写入由 AGENT_SKILLS_DIR 指定的目录；默认 E:/AIProject/skills。安装到客户端可显式设为用户的 .claude/skills 或 .zcode/skills。不再用 CODEX_HOME 决定目标。agents/openai.yaml 作为可选原平台元数据保留，目标客户端发现技能依靠 SKILL.md。

原平台 metadata 可以忽略；脚本、模板和资源完整复制，未包含客户端专属运行时、账号配置或外部工程。硬件与业务软件依赖仍须按原说明核对。
