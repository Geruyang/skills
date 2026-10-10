# skills

面向智谱 ZCode、Claude Code CLI 和兼容 SKILL.md 的 Agent 的技能集合。仓库收录 **167 个技能**，覆盖嵌入式开发、FPGA、金融研究、UI UX、工程协作、文档、自动化和成品模板。

每个技能保留独立的 `SKILL.md` 及相关 `scripts`、`references`、`assets`、`templates` 等资源。内容来自本机已有个人、系统和插件技能的迁移副本，已调整客户端绑定说明、部分固定路径和安装/模板脚本；对应的原始产品名称和 API 资料仍保留。

## 快速导航

- [安装与导入](#安装与导入)
- [全部技能及作用](#全部技能及作用)
- [每个技能的完整触发说明](docs/SKILL-CATALOG.md)
- [兼容性与外部依赖](#兼容性与外部依赖)
- [机器可读索引](docs/skills-index.json)
- [迁移清单](migration-manifest.json) · [验证记录](VALIDATION.json)

## 安装与导入

克隆到迁移脚本默认使用的 Windows 目录：

```powershell
git clone https://github.com/Geruyang/skills.git E:\AIProject\skills
```

如果本机该目录已有导出文件，请克隆到另一个空目录，或直接从已有目录执行导入脚本。不要覆盖有未保存修改的目录。

在仓库目录中执行：

```powershell
# 预览将导入到哪些目录，不实际复制
.\Import-Skills.ps1 -Client claude -WhatIf
.\Import-Skills.ps1 -Client zcode -WhatIf

# 导入全部技能
.\Import-Skills.ps1 -Client claude
.\Import-Skills.ps1 -Client zcode

# 只导入当前需要的技能
.\Import-Skills.ps1 -Client claude -Names keil,jlink,serial
```

脚本默认复制到当前 Windows 用户的 `~/.claude/skills` 或 `~/.zcode/skills`。它保留完整资源目录，遇到同名目录会跳过，不覆盖已有技能；支持 `-Destination` 指定项目技能目录等其他位置。该脚本只导入技能，不安装业务软件、MCP 服务或账号配置。

Claude Code 可通过 `/skill-name` 调用；智谱 ZCode 可通过 `$skill-name` 或斜杠菜单调用，并在“设置 → 技能”刷新、启用。也可把完整技能目录手动复制到对应客户端的技能目录。建议按实际任务启用技能，避免一次启用过多技能影响元数据发现。

如果 Claude Code 运行在 WSL/Linux，把目录放到实际 Linux 用户的 `~/.claude/skills`，同时调整 Windows 软件调用路径。仓库中的 `E:/AIProject/skills` 是迁移默认目录，其他位置以实际加载的 SKILL.md 所在目录为准。

安装器和模板创建脚本支持自定义目标目录：

```powershell
$env:AGENT_SKILLS_DIR = Join-Path $env:USERPROFILE '.claude\skills'
# 或使用 .zcode\skills / 自己的技能库路径
```

参见 [详细导入说明](README-导入说明.md)、[Claude Code 技能文档](https://code.claude.com/docs/en/skills) 和 [ZCode 技能文档](https://zcode.z.ai/cn/docs/skill)。

## 使用示例

| 任务 | 可组合的技能 |
|---|---|
| 构建 STM32 工程并读取运行日志 | `keil`、`jlink`、`serial`、对应开发板技能 |
| 检查 FPGA 约束与时序问题 | `vivado-constraints`、`vivado-analysis`、`vivado-timing-closure` |
| 分析 A 股行业与 ETF | `ashare-forward-expectations`、`china-market-data`、`etf-analysis` |
| 从产品需求完成界面原型 | `intentional-ui-design`、`ui-ux-pro-max`、`prototyping` |
| 为工程源码制作中文讲解演示 | `userskill-code-explainer-ppt`、`presentations`，按需搭配配音技能 |
| 创建新技能并核对效果 | `skill-creator`、`writing-skills`、`verification-before-completion` |

## 全部技能及作用

以下按用途分组，每个名称都链接到实际技能入口。完整触发条件以各技能的 SKILL.md 为准。

### 技能管理与 Agent 开发

9 个技能。

| 技能 | 作用 |
|---|---|
| [skill-creator](skill-creator/SKILL.md) | 创建和修改技能，组织 SKILL.md、辅助脚本、参考资料与资源，并检查元数据和触发范围。 |
| [skill-installer](skill-installer/SKILL.md) | 从 GitHub 仓库或 OpenAI 技能集合安装技能、列出可选技能，支持指定分支和目标目录。 |
| [writing-skills](writing-skills/SKILL.md) | 用验证场景设计、修改和测试技能，检查发现规则、说明质量及 Agent 执行效果。 |
| [using-superpowers](using-superpowers/SKILL.md) | 为开发会话选择并加载适用技能，按当前客户端工具能力适配后续工作流程。 |
| [agents](agents/SKILL.md) | 开发基于 OpenAI Agents API 或 Agents SDK 的应用，处理工具、会话、沙箱、交接、评估与部署。 |
| [openai-docs](openai-docs/SKILL.md) | 检索 OpenAI API、模型、Codex 和 ChatGPT 官方资料，用于配置、定价、迁移和故障说明。 |
| [openai-api-troubleshooting](openai-api-troubleshooting/SKILL.md) | 排查 OpenAI API 请求失败，区分认证、网络、额度与运行时问题并给出下一步。 |
| [openai-platform-api-key](openai-platform-api-key/SKILL.md) | 为使用 OpenAI 的应用检查和配置 API 密钥、访问方式与运行条件。 |
| [plugin-management](plugin-management/SKILL.md) | 发现适合任务的插件，核对依赖和连接状态，按授权管理或移除插件。 |

### 工程计划与代码质量

20 个技能。

| 技能 | 作用 |
|---|---|
| [brainstorming](brainstorming/SKILL.md) | 在新增功能或修改行为前澄清意图、需求、边界与设计方案。 |
| [writing-plans](writing-plans/SKILL.md) | 把多步骤工程需求整理成可执行的任务、实施顺序与验证计划。 |
| [executing-plans](executing-plans/SKILL.md) | 在当前会话按实施计划推进工作，分阶段执行并报告检查结果。 |
| [subagent-driven-development](subagent-driven-development/SKILL.md) | 将实施计划中的独立任务交给子 Agent，协调实现、规格复核和代码审查。 |
| [dispatching-parallel-agents](dispatching-parallel-agents/SKILL.md) | 识别可以独立推进的任务，分派并行 Agent 并汇总各自结果。 |
| [gas-centralized-development](gas-centralized-development/SKILL.md) | 采用统一指挥者协调下属 Agent 的职责、监督、整合与交付。 |
| [gas-decentralized-development](gas-decentralized-development/SKILL.md) | 采用规则制定、执行、裁决分离的协作方式处理工程任务与争议。 |
| [gas-combined-development](gas-combined-development/SKILL.md) | 把外层分权治理与内层集中执行结合，用于需要多层职责隔离的项目。 |
| [review-agent](review-agent/SKILL.md) | 对指定变更、提交或分支差异做只读代码审查，返回可验证的实际缺陷。 |
| [requesting-code-review](requesting-code-review/SKILL.md) | 在重要实现或合并前组织代码审查，检查结果是否满足需求和工程质量。 |
| [receiving-code-review](receiving-code-review/SKILL.md) | 核对审查意见的依据和适用性，再实施合理的修改并验证。 |
| [systematic-debugging](systematic-debugging/SKILL.md) | 从复现、证据收集和原因定位出发排查异常，避免未经验证的试错修复。 |
| [test-driven-development](test-driven-development/SKILL.md) | 按先失败测试、最小实现、测试通过和重构的循环开发功能或修复缺陷。 |
| [verification-before-completion](verification-before-completion/SKILL.md) | 在宣布完成、修复或通过之前运行相应验证，以实际输出支撑结论。 |
| [using-git-worktrees](using-git-worktrees/SKILL.md) | 为需要隔离的开发任务创建或复用 Git 工作树，并核对路径和分支环境。 |
| [finishing-a-development-branch](finishing-a-development-branch/SKILL.md) | 在验证通过后处理分支整合、提交、PR 和工作区收尾。 |
| [diagnosing-superpowers](diagnosing-superpowers/SKILL.md) | 复盘 Superpowers 工作流程中的重复工作、计划偏离、成本与执行问题。 |
| [teach-me-the-codebase](teach-me-the-codebase/SKILL.md) | 通过读取真实源码和项目资料，交互式讲解陌生代码库的业务、架构与约定。 |
| [engineering-learning](engineering-learning/SKILL.md) | 从基础概念、代码和实践验证出发，循序渐进学习工程与嵌入式知识。 |
| [jupyter-notebook-writing](jupyter-notebook-writing/SKILL.md) | 以 Markdown 为主编写 Milvus 应用示例 Notebook，并使用格式转换工具整理交付。 |

### MCU 与嵌入式开发

13 个技能。

| 技能 | 作用 |
|---|---|
| [embedded-systems](embedded-systems/SKILL.md) | 开发微控制器固件和 RTOS 应用，处理实时性、外设、裸机流程与功耗优化。 |
| [alientek-apollo-stm32f429](alientek-apollo-stm32f429/SKILL.md) | 针对正点原子 Apollo STM32F429IGT6 板开发、移植、构建、烧录和调试固件及外设。 |
| [embedfire-stm32f429-challenger](embedfire-stm32f429-challenger/SKILL.md) | 针对野火 STM32F429IGT6 挑战者 V1/V2 板核对资料、开发外设并构建和调试工程。 |
| [nuedc-stm32-mspm0-skill](nuedc-stm32-mspm0-skill/SKILL.md) | 处理 STM32CubeMX 到 Keil、TI MSPM0 SysConfig 到 CCS 的电赛 MCU 开发和验证流程。 |
| [esp32-development](esp32-development/SKILL.md) | 开发、配置、烧录与恢复 ESP32 系列固件，覆盖 ESP-IDF、Arduino、MicroPython 等常用框架。 |
| [embedded-vibecoding-multi-agent](embedded-vibecoding-multi-agent/SKILL.md) | 按采集、分析、实现职责拆分嵌入式和模型训练任务，先按原流程获得多 Agent 授权。 |
| [keil](keil/SKILL.md) | 扫描 Keil 工程、枚举 Target、构建或清理项目，解析日志并定位可烧录的产物。 |
| [jlink](jlink/SKILL.md) | 探测 J-Link 和目标芯片，烧录固件、读写内存、读取 RTT/SWO 并执行在线调试。 |
| [serial](serial/SKILL.md) | 扫描串口、监控和发送数据，记录日志并检查十六进制数据和通信协议。 |
| [build-system](build-system/SKILL.md) | 管理 Zephyr West 工作区、manifest、Sysbuild、Kconfig 和 CMake 构建配置。 |
| [devicetree](devicetree/SKILL.md) | 编写和核对 Zephyr Devicetree、绑定与 overlay，配置硬件拓扑和引脚。 |
| [testing-debugging](testing-debugging/SKILL.md) | 用 Zephyr Ztest、Twister 和运行时跟踪工具验证应用、排查系统问题。 |
| [pyadi-dt-cli](pyadi-dt-cli/SKILL.md) | 使用 Analog Devices adidtc CLI 检查、生成、校验和部署 Linux 设备树。 |

### FPGA 与 Xilinx 工具链

14 个技能。

| 技能 | 作用 |
|---|---|
| [xilinx-suite](xilinx-suite/SKILL.md) | 协调 Vivado、Vitis HLS、Vitis 软件开发和 PetaLinux 的完整 FPGA 与 MPSoC 工程流程。 |
| [fpga-vibecoding](fpga-vibecoding/SKILL.md) | 为百度 EdgeBoard FZ3B 或 Zynq UltraScale+ MPSoC 开发 RTL/HLS、AXI/DMA 和 PS 应用。 |
| [vitis-hls-synthesis](vitis-hls-synthesis/SKILL.md) | 将 C/C++ 算法综合成 RTL，配置接口和优化 pragma，解读 HLS 综合结果。 |
| [vivado-synth](vivado-synth/SKILL.md) | 配置 Vivado 综合策略、层次结构和资源推断，改善 RAM、DSP 等资源使用。 |
| [vivado-impl](vivado-impl/SKILL.md) | 配置布局布线和物理优化策略，分析拥塞并改善实现结果。 |
| [vivado-constraints](vivado-constraints/SKILL.md) | 编写和校验 XDC/SDC 时序及物理约束，处理时钟、I/O 延迟和例外路径。 |
| [vivado-analysis](vivado-analysis/SKILL.md) | 解读 Vivado 时序、slack、时钟偏差和 QoR 报告，定位关键路径问题。 |
| [vivado-timing-closure](vivado-timing-closure/SKILL.md) | 围绕约束、关键路径和实现策略系统推进 FPGA 时序收敛。 |
| [vivado-debug](vivado-debug/SKILL.md) | 配置 ILA/VIO、触发条件和硬件编程，进行 FPGA 板级与系统内调试。 |
| [vivado-sim](vivado-sim/SKILL.md) | 选择并运行 RTL、综合网表和实现后仿真，排查仿真行为与时序问题。 |
| [vivado-tcl](vivado-tcl/SKILL.md) | 生成、审查、解释和执行 Vivado/Vitis Tcl 脚本，并核对实际执行结果。 |
| [review-systemverilog](review-systemverilog/SKILL.md) | 审查 Verilog/SystemVerilog 的惯用写法、可综合性、结构和实现质量。 |
| [sv-lint](sv-lint/SKILL.md) | 运行 Verible 对 Verilog/SystemVerilog 进行 lint，整理诊断位置和问题说明。 |
| [formal-verification](formal-verification/SKILL.md) | 编写 SVA 属性和断言，配置形式验证引擎、分析反例和复杂度，支持 JasperGold/VC Formal。 |

### Yocto 与 Linux BSP

4 个技能。

| 技能 | 作用 |
|---|---|
| [bitbake-debug](bitbake-debug/SKILL.md) | 从 task 日志和元数据分析 BitBake 构建失败，覆盖 fetch 到镜像生成及常见 QA 问题。 |
| [yocto-bsp-kernel](yocto-bsp-kernel/SKILL.md) | 检查 MACHINE、BSP、内核配置、设备树、U-Boot、FIT 和内核模块部署。 |
| [yocto-image-rootfs](yocto-image-rootfs/SKILL.md) | 检查镜像配方、软件包组和 rootfs，排查包安装、postinstall 与缺失文件。 |
| [yocto-recipe-review](yocto-recipe-review/SKILL.md) | 审查和改进 recipe、bbappend、bbclass 的依赖、许可、补丁、安装和包拆分。 |

### 金融数据与投资研究

13 个技能。

| 技能 | 作用 |
|---|---|
| [ashare-forward-expectations](ashare-forward-expectations/SKILL.md) | 推演 A 股未来供需、盈利和政策变化，分析预期差、股价计价、历史类比及资金行为。 |
| [china-market-data](china-market-data/SKILL.md) | 查询 A 股和中国金融市场数据，在 iFind 等来源与 AkShare 之间选择合适接口。 |
| [hithink-finance](hithink-finance/SKILL.md) | 使用同花顺金融数据服务查询、分析、同步或导出股票、基金、衍生品和本地 DuckDB 数据。 |
| [akshare](akshare/SKILL.md) | 通过 AKShare 获取 A 股、港美股、期货、宏观与外汇等数据，作为免 API Key 的数据来源。 |
| [yfinance-data](yfinance-data/SKILL.md) | 通过 yfinance 获取行情、历史数据、财务、期权、分红和分析师相关数据。 |
| [company-valuation](company-valuation/SKILL.md) | 采用 DCF、可比公司估值和分部估值分析上市公司价值及情景差异。 |
| [asset-allocation](asset-allocation/SKILL.md) | 使用均值方差、Black-Litterman、风险预算和全天候框架配置资产与制定再平衡规则。 |
| [global-macro](global-macro/SKILL.md) | 分析央行政策、汇率、地缘风险和资金流，对照宏观因子形成跨资产配置判断。 |
| [etf-analysis](etf-analysis/SKILL.md) | 筛选和比较 ETF 的费率、跟踪误差、流动性与策略用途，组织中国市场 ETF 配置分析。 |
| [fund-analysis](fund-analysis/SKILL.md) | 分析基金风险收益、风格变化和基金经理，支持基金筛选和 FOF/ETF 组合构建。 |
| [stock-correlation](stock-correlation/SKILL.md) | 计算和比较股票相关性，寻找行业同类公司、关联标的和交易对。 |
| [backtesting-frameworks](backtesting-frameworks/SKILL.md) | 构建和核对策略回测，处理前视偏差、幸存者偏差、交易成本和结果可信度。 |
| [china-investment-proposal](china-investment-proposal/SKILL.md) | 面向中国财富管理场景编写投资建议，说明依据、产品选择与风险。 |

### UI UX 设计与实现

36 个技能。

| 技能 | 作用 |
|---|---|
| [intentional-ui-design](intentional-ui-design/SKILL.md) | 围绕产品意图、差异化方向和平台习惯完成界面设计、实现与视觉检查。 |
| [ui-ux-pro-max](ui-ux-pro-max/SKILL.md) | 检索设计规范、颜色、字体、组件和技术栈建议，生成可实施的 UI 设计系统。 |
| [ui-ux-designer](ui-ux-designer/SKILL.md) | 作为 UI UX Designer 的综合入口处理产品、网站和应用设计，并路由到细分能力。 |
| [ui-ux-help](ui-ux-help/SKILL.md) | 介绍 UI UX Designer 的能力范围，帮助选择适合任务的设计技能。 |
| [website-ui-design](website-ui-design/SKILL.md) | 设计多页面网站的结构、导航、内容、视觉风格和响应式行为。 |
| [landing-page-design](landing-page-design/SKILL.md) | 设计产品或营销落地页的首屏、价值说明、功能、价格、FAQ 和行动入口。 |
| [mobile-app-ui](mobile-app-ui/SKILL.md) | 设计 iOS/Android 应用页面、导航和状态，结合手势与平台习惯输出方案。 |
| [dashboard-saas-ui](dashboard-saas-ui/SKILL.md) | 设计 SaaS、管理后台和数据面板的 KPI、图表、表格、筛选器与复杂流程。 |
| [ecommerce-ux](ecommerce-ux/SKILL.md) | 设计商品浏览、详情、购物车、结账、订单和账户流程，改善信任和交易体验。 |
| [component-design](component-design/SKILL.md) | 设计按钮、输入框、卡片、导航、弹窗和表格等组件的变体、状态与规格。 |
| [design-system-builder](design-system-builder/SKILL.md) | 组织设计 token、组件库、使用规范和文档，建立可复用的设计系统。 |
| [color-typography-theming](color-typography-theming/SKILL.md) | 制定品牌色、字体、字号层级、语义颜色及明暗主题，检查可读性和对比度。 |
| [layout-grid-hierarchy](layout-grid-hierarchy/SKILL.md) | 调整网格、间距、对齐、留白和视觉层级，改善拥挤或缺少重点的布局。 |
| [microinteractions-motion](microinteractions-motion/SKILL.md) | 设计反馈、过渡、加载、手势和微交互的时序与动效，并考虑减少动态效果。 |
| [accessibility-audit](accessibility-audit/SKILL.md) | 依据 WCAG 2.2 检查对比度、键盘、焦点、读屏、表单和触控可访问性。 |
| [forms-onboarding-ux](forms-onboarding-ux/SKILL.md) | 设计注册、登录、多步表单、验证和首次使用流程，减少输入与完成障碍。 |
| [user-flows](user-flows/SKILL.md) | 梳理注册、购买、预订、搜索等任务流程，明确步骤、决策点和异常路径。 |
| [information-architecture](information-architecture/SKILL.md) | 规划站点地图、导航、信息分类、标签和内容层级，并设计结构验证方法。 |
| [wireframes](wireframes/SKILL.md) | 制作低保真或中保真的页面结构、内容层级和布局线框图。 |
| [high-fidelity-mockups](high-fidelity-mockups/SKILL.md) | 制作具有实际排版、颜色、图像方向和组件状态的高保真界面方案或 HTML 样稿。 |
| [prototyping](prototyping/SKILL.md) | 制作可点击原型和交互流程，用于验证页面切换、操作和产品想法。 |
| [design-to-code](design-to-code/SKILL.md) | 把界面设计转换成响应式、语义清晰且可访问的 HTML/CSS、Tailwind 或 React 实现。 |
| [figma-workflow](figma-workflow/SKILL.md) | 指导 Figma 自动布局、组件、变量、约束、原型、插件和团队素材管理。 |
| [design-handoff](design-handoff/SKILL.md) | 编写开发交付规格、间距与状态说明、响应式规则、资源和设计 QA 检查资料。 |
| [design-inspiration-trends](design-inspiration-trends/SKILL.md) | 整理设计方向、参考和情绪板，对比不同视觉风格的适用场景。 |
| [redesign-makeover](redesign-makeover/SKILL.md) | 评估既有网站或应用的问题，规划改版并输出新的视觉与体验方案。 |
| [ux-audit-critique](ux-audit-critique/SKILL.md) | 审查界面或截图的可用性与视觉问题，给出严重性、影响和修复优先级。 |
| [usability-testing](usability-testing/SKILL.md) | 设计可用性测试目标、任务、脚本和指标，并整理测试发现。 |
| [ux-research-plan](ux-research-plan/SKILL.md) | 规划用户研究、访谈、调查、竞品和数据分析，形成有依据的设计洞见。 |
| [personas-journey-maps](personas-journey-maps/SKILL.md) | 建立用户画像、需求、同理心地图和用户旅程，梳理行为与痛点。 |
| [ux-writing-microcopy](ux-writing-microcopy/SKILL.md) | 编写界面标题、按钮、标签、报错、空状态、引导和通知文案。 |
| [conversion-optimization](conversion-optimization/SKILL.md) | 分析转化漏斗、行动按钮、信任信号和流程阻力，提出可验证的改善方案。 |
| [ux-portfolio-case-study](ux-portfolio-case-study/SKILL.md) | 组织 UX/UI 作品集和项目案例，呈现问题、过程、设计决策与结果。 |
| [ux-career-interview](ux-career-interview/SKILL.md) | 规划设计学习与职业成长，准备面试、作品集讲解和实际设计题。 |
| [aidesigner-guide](aidesigner-guide/SKILL.md) | 指导 AIDesigner 的提示词、品牌设置、设计迭代、原型和图像转 HTML 流程。 |
| [recommended-tools](recommended-tools/SKILL.md) | 根据需要介绍推荐的 UI 设计工具，并保留工具关联推广的披露要求。 |

### 文档与表格演示

8 个技能。

| 技能 | 作用 |
|---|---|
| [documents](documents/SKILL.md) | 创建、编辑、修订和批注 DOCX/Word 文档，保留 OOXML 语义并渲染检查版面。 |
| [pdf](pdf/SKILL.md) | 提取 PDF 文本与表格，合并、拆分、旋转、加水印及执行常见 PDF 处理。 |
| [pdf-artifacts](pdf-artifacts/SKILL.md) | 生成和检查重视版面质量的 PDF，包括表单、页面渲染和视觉核对。 |
| [presentations](presentations/SKILL.md) | 读取、创建或修改 PowerPoint/Google Slides 演示，检查布局、结构和最终效果。 |
| [spreadsheets](spreadsheets/SKILL.md) | 创建、编辑与分析表格文件和 Google Sheets，处理公式、格式、图表和重算要求。 |
| [excel-live-control](excel-live-control/SKILL.md) | 通过已连接的 Excel/ChatGPT 会话操作当前工作簿，核对会话和目标文件。 |
| [template-creator](template-creator/SKILL.md) | 从参考文档、表格、幻灯片或图像创建可复用的个人模板技能与相关资源。 |
| [userskill-code-explainer-ppt](userskill-code-explainer-ppt/SKILL.md) | 根据工程真实源码制作或更新中文代码讲解 PPT，核对修改、配音同步与验证边界。 |

### 图像与浏览器自动化

5 个技能。

| 技能 | 作用 |
|---|---|
| [imagegen](imagegen/SKILL.md) | 用已配置图像服务或随附 API 脚本生成、编辑和变换栅格图像及透明背景素材。 |
| [visualize](visualize/SKILL.md) | 生成说明概念、过程、比较或变化的可视化及交互工具，支持本地 HTML/SVG 等交付。 |
| [playwright](playwright/SKILL.md) | 通过 Playwright CLI 自动化真实浏览器，完成页面导航、输入、截图、数据读取和 UI 流程排查。 |
| [computer-use](computer-use/SKILL.md) | 依据当前客户端提供的桌面/浏览器自动化能力操作应用，保留原运行时说明和授权边界。 |
| [sites](sites/SKILL.md) | 使用配置好的 Sites 服务创建和修改网站、落地页、门户、看板或交互工具。 |

### 协作服务与知识空间

15 个技能。

| 技能 | 作用 |
|---|---|
| [google-calendar](google-calendar/SKILL.md) | 读取 Google Calendar、比较空闲时间和冲突、准备提醒与日程变更。 |
| [google-calendar-daily-brief](google-calendar-daily-brief/SKILL.md) | 整理当天日历、重点会议、安排冲突和准备事项，生成日程简报。 |
| [google-calendar-free-up-time](google-calendar-free-up-time/SKILL.md) | 分析会议碎片化，寻找能腾出连续专注时间的最小日程调整方案。 |
| [google-calendar-group-scheduler](google-calendar-group-scheduler/SKILL.md) | 比较多人的可用时间，查找合适的集体会议时段并准备安排。 |
| [google-calendar-meeting-prep](google-calendar-meeting-prep/SKILL.md) | 结合日历事件、参与者和附件准备会议背景、资料与待处理事项。 |
| [slack](slack/SKILL.md) | 检索和读取 Slack 工作区内容，协助频道、讨论和消息工作流程。 |
| [slack-channel-summarization](slack-channel-summarization/SKILL.md) | 归纳指定 Slack 频道的主题、决定、行动项和未解决问题。 |
| [slack-daily-digest](slack-daily-digest/SKILL.md) | 将指定时间范围内的 Slack 更新汇总成每日摘要和需要关注的事项。 |
| [slack-notification-triage](slack-notification-triage/SKILL.md) | 整理 Slack 通知的优先级，区分需要回复、跟进或仅供了解的消息。 |
| [slack-outgoing-message](slack-outgoing-message/SKILL.md) | 按用户明确授权准备和发送 Slack 消息，核对接收对象与内容。 |
| [slack-reply-drafting](slack-reply-drafting/SKILL.md) | 根据 Slack 讨论上下文起草适合语气和目标的回复。 |
| [write-page](write-page/SKILL.md) | 创建或编辑 ChatGPT Page/Space 内容，遵循目标格式和写入范围。 |
| [maintain-space](maintain-space/SKILL.md) | 把新证据整合进现有 ChatGPT Pages/Space，更新内容并核对一致性。 |
| [organize-space](organize-space/SKILL.md) | 组织 ChatGPT Pages/Space 的层级、位置与结构，按请求调整信息组织。 |
| [manage-schedules](manage-schedules/SKILL.md) | 检查 ChatGPT Space 的页面和相关计划，建议并管理适用的自动化任务。 |

### 健康报告解释

3 个技能。

| 技能 | 作用 |
|---|---|
| [lab-result-interpreter](lab-result-interpreter/SKILL.md) | 提取和解释化验指标，对照参考范围说明异常和临床意义。 |
| [medical-report-processor](medical-report-processor/SKILL.md) | 从 PDF 体检报告提取患者信息与量化指标，生成结构化映射和数据文件。 |
| [patiently-ai](patiently-ai/SKILL.md) | 把医生来信、处方、化验、出院和临床记录解释成便于患者理解的语言。 |

### 陪伴角色与其他应用

7 个技能。

| 技能 | 作用 |
|---|---|
| [suqing-companion](suqing-companion/SKILL.md) | 与苏晴角色聊天、显示动态形象，按授权读取 EigenFlux 动态并发送 Agent 消息。 |
| [suqing-voice](suqing-voice/SKILL.md) | 使用本机苏晴参考音色生成朗读、配音或旁白音频，支持批量与取消操作。 |
| [create-pet](create-pet/SKILL.md) | 设计、修复、验证、预览和提交 ChatGPT Work 动态宠物的 v2 素材。 |
| [pets](pets/SKILL.md) | 在 ChatGPT Work 中查看、选择、下载或删除动态宠物。 |
| [update-pet](update-pet/SKILL.md) | 检查、修复和修改 ChatGPT Work 宠物的名称、说明或 sprite sheet。 |
| [genshin-companion](genshin-companion/SKILL.md) | 规划原神日常、树脂和角色培养，查询并提供经过核对的任务攻略。 |
| [devday-guide](devday-guide/SKILL.md) | 查询 OpenAI DevDay 日程、现场安排、直播与录播，帮助组织参加计划。 |

### 可复用成品模板

20 个技能。

| 技能 | 作用 |
|---|---|
| [artifact-template-analytics-dashboard](artifact-template-analytics-dashboard/SKILL.md) | 基于保留参考文件创建数据分析仪表盘，展示获客、参与、留存、收入和转化漏斗 KPI 与图表。 |
| [artifact-template-business-review](artifact-template-business-review/SKILL.md) | 基于保留参考文件创建业务复盘，组织业务表现、关键指标、问题与后续行动。 |
| [artifact-template-design-report](artifact-template-design-report/SKILL.md) | 基于保留参考文件创建设计报告，组织问题背景、设计决策、方案和交付说明。 |
| [artifact-template-experiment-analysis](artifact-template-experiment-analysis/SKILL.md) | 基于保留参考文件创建实验分析，整理实验数据、结果比较和结论。 |
| [artifact-template-financial-budget](artifact-template-financial-budget/SKILL.md) | 基于保留参考文件创建财务预算，组织预算假设、收入支出与差异分析。 |
| [artifact-template-investment-committee-memo](artifact-template-investment-committee-memo/SKILL.md) | 基于保留参考文件创建投委会备忘录，组织投资依据、风险、判断和待决策事项。 |
| [artifact-template-legal-memorandum](artifact-template-legal-memorandum/SKILL.md) | 基于保留参考文件创建法律备忘录，组织事实、问题、论证与结论。 |
| [artifact-template-market-trends-report](artifact-template-market-trends-report/SKILL.md) | 基于保留参考文件创建市场趋势报告，组织市场变化、证据与影响。 |
| [artifact-template-minimal-letterhead](artifact-template-minimal-letterhead/SKILL.md) | 基于保留参考文件创建简洁信头文档，保留信函排版与品牌信息位置。 |
| [artifact-template-operating-calendar](artifact-template-operating-calendar/SKILL.md) | 基于保留参考文件创建运营日历，安排业务活动、时间节点和责任。 |
| [artifact-template-operating-review](artifact-template-operating-review/SKILL.md) | 基于保留参考文件创建运营复盘，展示运营表现、差异和改善动作。 |
| [artifact-template-project-kickoff](artifact-template-project-kickoff/SKILL.md) | 基于保留参考文件创建项目启动演示，明确目标、范围、团队与推进安排。 |
| [artifact-template-project-tracker](artifact-template-project-tracker/SKILL.md) | 基于保留参考文件创建项目跟踪表，管理任务、里程碑、负责人和进度。 |
| [artifact-template-sales-pipeline](artifact-template-sales-pipeline/SKILL.md) | 基于保留参考文件创建销售管线，组织商机阶段、金额、预测和跟进。 |
| [artifact-template-simple-dark-mode](artifact-template-simple-dark-mode/SKILL.md) | 基于保留参考文件创建简洁深色幻灯片，保留深色主题、布局与字体层级。 |
| [artifact-template-simple-light-mode](artifact-template-simple-light-mode/SKILL.md) | 基于保留参考文件创建简洁浅色幻灯片，保留浅色主题、布局与字体层级。 |
| [artifact-template-strategy-memorandum](artifact-template-strategy-memorandum/SKILL.md) | 基于保留参考文件创建战略备忘录，组织现状、方向、选择与实施要点。 |
| [artifact-template-system-design](artifact-template-system-design/SKILL.md) | 基于保留参考文件创建系统设计，组织架构、组件、接口和技术决策。 |
| [artifact-template-team-alignment](artifact-template-team-alignment/SKILL.md) | 基于保留参考文件创建团队对齐演示，说明共同目标、角色和协作安排。 |
| [artifact-template-three-statement-forecast](artifact-template-three-statement-forecast/SKILL.md) | 基于保留参考文件创建三表预测，组织利润表、资产负债表和现金流预测。 |

## 兼容性与外部依赖

迁移后的入口优先使用当前客户端真实存在的工具，不把 Codex 工具名称当成目标客户端可用性证明。`PORTABILITY.md` 记录每个技能的来源和限制；[兼容性总表](COMPATIBILITY.md) 可按技能查阅。

| 类型 | 数量 | 使用条件 |
|---|---:|---|
| 通用技能或本地工具流程 | 137 | 指令可读取；Python、Node、硬件 SDK、数据源等按实际任务安装 |
| 本地文档库已适配 | 5 | 核对文档库、渲染工具、公式重算和云端导入能力 |
| 连接器或 API 流程 | 11 | 配置 Slack/Google Calendar 等账号与服务授权 |
| 原平台专属服务流程 | 12 | 配置对应服务或等价集成；包括 Computer Use、Pages/Pets、实时 Excel、Sites 等 |
| 外部项目流程 | 2 | 苏晴相关技能需要本地 ChatBot、音色/模型资源及后端 |

技能文件不包含这些服务本身。Office 工作可以使用已核对可用的 python-docx、openpyxl、PptxGenJS/python-pptx、pypdf 等本地库；云端编辑需要真实授权集成。本机开发板资料、金融账号、ChatBot 项目、Keil/Vivado/J-Link 等不随仓库分发。

`pdf` 与 `pdf-artifacts` 分别保留个人 PDF 技能和插件 PDF 技能，避免名称冲突。插件前缀式技能引用已按导出后的技能名适配；`agents/openai.yaml` 保留为可选来源平台元数据。

## 目录结构

```text
skills/
├── README.md
├── Import-Skills.ps1
├── docs/
│   ├── SKILL-CATALOG.md
│   └── skills-index.json
├── skill-name/
│   ├── SKILL.md
│   ├── PORTABILITY.md
│   ├── scripts/       # 若原技能有辅助脚本
│   ├── references/    # 若原技能有参考资料
│   └── assets/        # 若原技能有模板或素材
└── 其他技能目录
```

技能采用单层目录，适合按目录选择、复制和导入。GitHub 仓库中的 README、索引和验证文件用于维护与展示，不是独立技能。

## 验证与维护

本次迁移校验了 167 个技能元数据、资源完整性及 193 个 Python 文件语法；对安装器路径覆盖、UI 数据检索、模板实际生成和导入脚本做了本地检查。此前 2228 个原始文件的哈希核对保持不变。未逐一在两个目标客户端执行所有业务、硬件和云端流程。[验证记录](VALIDATION.json)

每个技能的能力与验证范围独立。修改时保持技能入口、脚本、数据和参考资源一致；若改变目录、依赖或行为，同步修改 README、[详细目录](docs/SKILL-CATALOG.md) 和机器可读索引。

`CLIENT-RULES.md` 保存本库维护者提供的两项个人规则，可按需要合并到客户端的 CLAUDE.md 或 AGENTS.md。技能启用、工程写入、硬件操作和发送消息仍遵守用户授权与当前客户端权限。

## 来源与许可

本库是已有技能的整理与迁移集合，包含个人技能和不同插件来源的内容，不代表全部内容为维护者原创。来源记录见 [迁移清单](migration-manifest.json)。已保留能定位到的原有 LICENSE、NOTICE 与来源说明。

不同技能、代码、图片和模板可能采用不同许可。请以对应目录和上游资料为准；本库不为第三方内容统一重新授予 MIT 或其他许可证。没有明确许可证的内容不能仅因公开可读就推断具有任意再分发权限。
