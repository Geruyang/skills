# UI UX Pro Max 的使用

## 定位运行环境

先定位并读取实际安装的 `ui-ux-pro-max/SKILL.md`。通常与本技能同级，也可能位于当前个人技能目录。使用其 `scripts/search.py` 的绝对路径，不能直接使用 Claude 专属环境变量。

Python 优先使用项目已有解释器或可用的 `python` / `python3` / `py -3`。本机已验证的备用解释器为：

`python`

本机依赖技能的实体路径为：

`E:/AIProject/skills/ui-ux-pro-max`

这些是安装记录，不是跨机器的固定前提；使用前检查是否存在。缺少运行环境时报告限制，使用已读规范完成适当范围的设计，不自动安装系统软件。

## PowerShell 示例

在当前任务项目根目录运行。下面是查询示例，不是对当前产品的设计决定。

```powershell
$uiPython = (Get-Command python -ErrorAction Stop).Source
$uiSearch = 'E:/AIProject/skills/ui-ux-pro-max/scripts/search.py'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'

# 整体设计候选
& $uiPython $uiSearch 'analytics dashboard professional' --design-system -p 'Example' -f markdown

# 一个明确的问题
& $uiPython $uiSearch 'keyboard focus modal' --domain ux

# 仅当工程确实采用 WPF 时使用
& $uiPython $uiSearch 'keyboard navigation' --stack wpf
```

查询以 2–5 个具体英文关键词表达一个主要意图，中文需求先准确转译。核对匹配主题和平台。结果不符时缩小或明确 domain 后重试一次；仍无相关结果，说明回退到一般设计判断，不能杜撰命中。

对新设计先审阅结果再记录最终选择。需要工具持久化时显式传入 `--output-dir`，指向当前项目允许存放设计资料的目录；工具会在该目录下创建 `design-system/<project>/MASTER.md`。先读已存在的 MASTER 与页面 override，避免无意覆盖。输出命名与 `--force` 的使用遵循依赖技能及用户已给的授权。

不要把另一个项目的设计产物写入本技能或 AiStock。AiStock 本身的设计产物按其规则放在 `outputs/` 内，临时文件放 `work/tmp/`；这条只适用于 AiStock。

## 技术栈与数据的边界

先看工程文件再选 stack；用工具 `--help` 查看当前支持项。没有对应栈（例如 Qt/PySide）时查询通用 UX，并结合该平台官方文档或项目现有组件实现，不能声称拿到了专用数据库规则。

资料库的默认值需要适配真实场景。字体建议要补查中文覆盖与可用性；动效代码要匹配当前框架；营销页模式不直接移植到业务工作台。已有组件规范优先于自动推荐的风格。
