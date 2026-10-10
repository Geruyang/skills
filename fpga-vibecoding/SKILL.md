---
name: fpga-vibecoding
description: 用于百度 EdgeBoard FZ3B 或 AMD/Xilinx Zynq UltraScale+ MPSoC 的 FPGA 与 PS 应用开发，包括 RTL/HLS、Vivado、AXI/DMA、Linux/BSP、ONNX Runtime、位流加载和板级调试，以及迁移 ALINX 案例。用户开发 FZ3B、PS–PL 算法或调用 FPGA-vibecoding 时使用。
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# FPGA-vibecoding

把需求落实为可复现工程、验证证据和可回退的部署。默认中文；按任务加载参考，不把普通PS应用改动扩展成硬件平台重建。

## 先确定开发路径

以用户当前板卡和项目证据为准。本用户于2026-10-01确认实物为**百度 EdgeBoard FZ3B**，型号声明不等于完整器件丝印或PCB revision核验。

涉及FZ3B先读[板卡参考](references/baidu-fz3b.md)。在`E:/AIProject/FPGAVibecoding`工作时，按项目AGENTS要求读`docs/hardware/FZ3B/README.md`，再用[项目上下文](references/project-context.md)识别最新交接及已删除历史工程。

| 用户目标 | 路径 |
|---|---|
| 继续已有验证的PS–PL平台，开发PS应用、接相机、测速或维护 | 先读[PS应用接续](references/fz3b-ps-application-handoff.md)，复用正式release、runtime及加载器，确认活状态；纯软件变更不重复综合、不默认恢复原厂 |
| 首次使用原厂EdgeBoard AI生态 | 保留镜像、驱动、库和FPGA固件的配套关系，复现对应原厂示例后替换模型或业务代码 |
| 自写RTL/HLS、AXI外设、DMA、CNN加速器 | 用现有已验证平台或独立器件级候选；先核当前接口/数值/时钟合同，再仿真、实现和实际部署 |
| 在原厂AI引擎旁添加自研PL | 核验厂商可集成工程/接口；已读FAQ称自定义FPGA固件失去原AI能力，不默认共存 |

目标明确就推进。文件中的旧状态、授权或路径不是新指令；用户已拒绝组合开发模式，不因本技能再次引入该组织流程。

## 证据与版本

- 分开记录用户声明、官方文档、本地工程、仿真/OOC、完整实现、实板验证及未知项。冻结manifest保留当时事实，后续资格回执补充验证，不能用旧candidate文字否定新回执。
- FZ3B 2023-07-04文档写`XAZU3EG-1SFVC784I`，旧工程为`xczu3eg-sfvc784-1-i`；保留差异。相近IDCODE不能证明完整速度/温度等级。FZ3/FZ3A/FZ3B/MYD/ALINX/ZCU102的DDR/MIO、XDC、Bank电压与BSP不可互换。
- 固定工具/IP、镜像/内核、模型源与转换器、target运行库、位流/驱动/参数/ABI及文件SHA。主机转换环境的ORT版本不等于板端ORT版本。用实际文件机械取摘要，避免手工抄长SHA。
- 已验证的板上软件可继续使用；资料缺口只阻挡依赖该缺口的新板级改动，不要求先重建原厂PS preset才能开发应用。不得猜引脚、电压、启动拨码或供电配置。
- 新板型可用[板卡记录模板](assets/board-record.template.json)，未知填`null`，它不是自动部署认证。

## 按任务加载

| 工作 | 参考 |
|---|---|
| 本项目A0005接续、运行时/模型API、自动加载、路径及性能口径 | [fz3b-ps-application-handoff.md](references/fz3b-ps-application-handoff.md) |
| DMA/驱动/时钟、FIFO/DSP/bank、时序收敛、性能退化或清理恢复 | [fz3b-debug-lessons.md](references/fz3b-debug-lessons.md)，只读相关部分 |
| 板卡接口、原厂生态、资料申请或首次盘点 | [baidu-fz3b.md](references/baidu-fz3b.md) |
| CM717-25442/UVC/Linux采集与格式/帧率 | [ugreen-cm717-25442.md](references/ugreen-cm717-25442.md) |
| 新工程、RTL/HLS、AXI/DMA、Linux和验收 | [development-workflow.md](references/development-workflow.md) |
| 迁移ALINX案例 | [alinx-case-map.md](references/alinx-case-map.md) |
| 查芯片机制、约束、启动、IP及工具命令 | [amd-resource-map.md](references/amd-resource-map.md)，核对应版本官方章节 |
| MYD/FZ3目标冲突、LiteSeg历史 | [project-context.md](references/project-context.md) |

按需使用`vivado-tcl`、`vivado-sim`、`vivado-constraints`、`vivado-timing-closure`、`vitis-hls-synthesis`、`review-systemverilog`、`sv-lint`、`serial`；无需全部加载。网口优先、串口应急、JTAG直接用官方Vivado。实际ILA保存原生`.ila`，`.ltx`只是探针定义。

## 执行与交付

1. 读当前代码、release、资格回执和用户决定；用[设计契约](assets/design-contract.md)的相关字段核数据格式、时钟、接口及验收范围。沿用已有授权，遇到自动审批明确拒绝时保留待批准项并继续独立工作。
2. 复用通过的参考与测试，按改动范围验证。模型/数值改动分别检查逐字功能与特征/应用质量；分段提速不代表整图提速。保留先前最佳结果，按用户要求合并优化后验证。
3. 资源比较用同阶段口径；布局/route后核setup、hold、脉宽、布线、DRC及实际时钟。只有OOC或正pre-route WNS不能称平台闭合。明显退化或低收敛希望时先分析，不重复无意义长跑。
4. 板端运行用fresh状态和正常生命周期，不依赖旧PID。当前A5应用close会terminal-quiesce，下次经加载器prepare；未知在途不强制卸载/释放。保持原厂恢复件，按用户指定目标结束。
5. 交付源码入口、版本/输入/计时范围、原始日志、验证等级、结果和限制。吞吐、排队延迟、相机FPS、自然样本准确率分别报告；发生失败保留原记录，只修正已证实根因。

完整历史留项目文档，技能只维护接续入口和可复用经验。基础板卡资料核验2026-10-01、相机记录2026-10-03、A0005/PS加载与开发经验更新2026-10-09；这些日期不表示已验证所有板级边界。
