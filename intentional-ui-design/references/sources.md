# 来源与设计取舍

核查日期：2026-09-24。

## 文章：思想来源

[How to turn your AI into a world-class designer](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world)，Anshu Chimala，Lenny’s Newsletter，2026-09-01。

已读公开正文至 Technique 6。Technique 7 仅见标题，其后为付费订阅提示；没有取得或推断隐藏正文。

公开部分的启发：先广泛探索再收敛；用具体创意方向或外部随机种子增加差异；以截图反馈促进迭代；按需用图像和视频丰富表达；交付时删减无价值元素。本文只保留这一简要摘要，不复制原文提示词或示例。

## UI UX Pro Max：执行资料

- [官方仓库](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- 安装版本：[v2.15.0](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases/tag/v2.15.0)
- 安装源目录：`.claude/skills/ui-ux-pro-max`，已适配 Codex 路径。
- 许可：MIT；完整许可随依赖技能保存。
- 保留其本地检索工具与数据，不把资料库复制进本技能。

## 本技能的综合设计

下列是面向本用户环境的实现决策，并非声称来自文章：按任务规模裁剪流程；保留项目技术栈；把设计候选转成语义 tokens 与状态；增加中文、桌面和移动检查；缺少 GUI 时如实标记；将多 agent 评审限定为另行获授权后使用。

文章用来指导探索和评审，Pro Max 用来查找可落实的设计依据。本技能不绑定文章里的模型名称、费用比例或特定视频服务，不将个人审美分数当作客观质量认证。
