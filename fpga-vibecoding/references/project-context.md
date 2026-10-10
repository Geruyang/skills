<!-- fz3b-application-current-20261009 -->
> 当前接续（2026-10-09）：本项目已完成MobileCLIP-S1的V10.5/A0005实板混合推理、PS加载服务、正常切换及受控重启，后续重点PS应用。先读[PS应用接续](fz3b-ps-application-handoff.md)和项目`docs/handoffs/2026-10-09-ps-application-development-handoff.md`；下文旧目标/未部署描述是2026-10-01历史，不覆盖新资格回执。
>
> LiteSeg源码、报告、讲义、配音和发布包已按用户要求删除，旧`liteseg_vivado`路径不存在。新应用复用`releases/current/`；未知实物revision及XA/XC差异仍按证据保留，不阻挡已验证平台上的普通PS软件开发。

# FPGAVibecoding 本地历史与目标更正

此文件只适用于 `E:/AIProject/FPGAVibecoding`，不是所有 FZ3B 用户的默认工程配置。检查日期：2026-10-01。

## 目标身份

- 用户本轮明确声明：“我的开发板就是其中的 FZ3B”。以百度 EdgeBoard FZ3B 作为后续任务默认板型。
- 2026-09-13 建立的 `docs/hardware/MYC-CZU3EG-V3/` 来自用户此前提供的 MYC/MYD 产品与合规资料包。它仍然有资料价值，但不能证明现在的 FZ3B 使用其电源、Bank、pinout、DDR/MIO 或 BSP。
- 项目 `AGENTS.md` 和新 `docs/hardware/FZ3B/README.md` 记录本次更正。旧设计文档、报告、PPT 和音频是历史快照，不能据旧目标字样认定当前实物。
- 已有 `xilinx-suite` 技能内含此项目采用 MYD 的旧快照。调用它做工具辅助时，应结合本轮用户指示和新项目入口，不能把其中 MYD 声明或模板值套回 FZ3B。没有因这次工作修改该通用技能。

## 已检查的既有工程证据

| 文件（相对项目根） | 本次读取到的事实 | 对新 FZ3B 的适用范围 |
|---|---|---|
| `liteseg_vivado/reports/PART_EVIDENCE.md` | 工程目标 `xczu3eg-sfvc784-1-i`，本机曾查询到该 part；未配置 board_part、真实 pinout 或 PS preset | 证明旧逻辑验证目标，不证明 FZ3B 实物 part；百度历史 FZ3B 文档的 XA/XC 差异需核验 |
| `liteseg_vivado/system/VALIDATION.md` | 2026-09-15 记录 Vivado/Vitis HLS 2026.1、主机对拍、HLS cosim 和 OOC 实现 | 属历史记录，本次未重新运行，不写作本轮硬件验证 |
| 同上 | 32×32 完整小图最大 16,471,024 周期，10 ns 仿真时钟约 164.71 ms；320×320 未做全图 RTL 性能验证 | 不满足“仅凭 100 MHz 时序通过即可声称实时”的推论 |
| 同上 | 缺真实平台 BSP/XSA/PS preset、内核构建树、训练权重和实板连接 | 驱动加载、UVC、真实 DDR DMA、模型精度及整机性能均需另验 |

这些文件的相对位置只用于查找，不强制新工程依赖 LiteSeg。新的项目应单独建立版本记录，不改写旧报告让它看起来适用于 FZ3B。

## 复用方式

复用算法、RTL、主机测试、可移植 HLS 和测试向量；先在明确标记的器件级目标重新验证。若部署器件、IP 或工具版改变，再比较利用率、时序、接口与数值结果。板级 XDC、PS 配置、地址/中断、驱动、设备树、启动文件需在 FZ3B 的匹配资料上重新确认。

任何真实上板前，从 `docs/hardware/FZ3B/board-profile.json` 的未知项补齐当前任务所需证据。此档案不是完整采购/BOM 数据库，也不要求无关外设全部确认后才能做局部开发。
