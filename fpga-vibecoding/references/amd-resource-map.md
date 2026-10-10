# AMD / Xilinx 官方资源与执行规则

核对日期：**2026-10-01（Asia/Shanghai）**。适用方向：FZ3B 所属 Zynq UltraScale+ MPSoC 的器件、RTL、PS/PL、嵌入式软件与调试。本文是按任务抽取的参考地图，不是全站、整本手册或 FZ3B 实板验证记录。

## 证据与版本边界

- `已读章节`：已取得该章节正文；只代表下面列出的范围。
- `已读索引`：可确认资源定位，尚未核对具体寄存器/流程正文。
- `仅定位`：只取得搜索索引或链接，正文访问失败，不能据此生成最终配置。
- `文档声明` 与 `实板验证` 必须分开。ZCU102 等 AMD 评估板案例提供方法，不能赋予 FZ3B 相同的 DDR、MIO、pinout、时钟、复位或电源配置。
- 文档地址中的 `/r/en-US/` 会随网站默认版本变化；使用时复核标题版本。需要复现的项目应保存对应 PDF/章节、版本、访问日期和文件哈希。下表版本是本次看到的版本，不是项目必须采用的版本。
- 不因本机安装 2026.1 或网站默认显示 2026.1 就升级原厂工程。原厂旧 SDK/Vivado/PetaLinux 流程与新工具实验应分别锁定，先复现基线，再评估迁移。
- 先核验**完整器件料号**，包含 `XA/XC` 前缀、容量、速度、封装和温度级。FZ3B 历史文档与现有 XCZU3EG 工程若存在前缀差异，保留为待核验差异；不能只凭“ZU3EG”判断 bitstream、DDR preset 或约束可直接复用。板卡身份及原厂出处以本技能的板卡资料为准。

## 按问题选择资料

| 主题 | 官方入口、观察到的版本 | 本次阅读范围与使用方式 |
|---|---|---|
| 官方入口 | [AMD 中文官网](https://www.amd.com/zh-cn.html)；动态网站 | 已读入口。专业参数应下钻到文档/IP guide/版本发行说明，不从营销页推导实现参数。 |
| SoC 架构、PS/PL、启动与一致性 | [UG1085 PDF](https://docs.amd.com/api/khub/documents/xzMsp_c5sG9J6A3u7NkJYQ/content)；索引显示 v2.5，2025-03-21 | **仅定位及索引摘录核对**。15 MB PDF 超过本次网页提取限制，未通读。实际修改前按主题读互连、地址图、时钟复位、启动和目标外设章节。 |
| 寄存器精确定义 | [UG1087 Register Reference](https://docs.amd.com/r/en-US/ug1087-zynq-ultrascale-registers)；在线参考，未确认独立版本号 | **已读索引**。写寄存器前查模块、绝对地址/偏移、访问类型、复位值、保留位及写入条件；不能把索引当成位定义。 |
| 启动链 | [UG1137 Boot Flow](https://docs.amd.com/r/en-US/ug1137-zynq-ultrascale-mpsoc-swdev/Boot-Flow)；2026.1，2026-07-22 | 已读章节。APU 常见非安全流程为 FSBL 交接 TF-A，再到 U-Boot/Linux；PMU firmware 与 FSBL 并行运行，不能误写成单一串行阶段。 |
| 启动镜像入口 | [UG1137 Creating a Bootable Image](https://docs.amd.com/r/en-US/ug1137-zynq-ultrascale-mpsoc-swdev/Creating-a-Bootable-Image)；2026.1，2026-07-22 | 已定位章节及版本；打包命令仍须使用工程对应版本的 Bootgen/BIF 说明。本文未提供 FZ3B 通用可烧录 BIF。 |
| PetaLinux 配置/构建/打包 | [UG1144 2025.2](https://docs.amd.com/r/2025.2-English/ug1144-petalinux-tools-reference-guide)；2025.2，2025-11-20 | 已读索引。已定位导入硬件、版本控制、设备树、FSBL、TF-A、PMUFW 和启动打包；导入硬件章节本次读取超时。 |
| 工具/系统升级边界 | [UG1144 Minor Releases](https://docs.amd.com/r/2025.2-English/ug1144-petalinux-tools-reference-guide/Upgrading-Between-Minor-Releases-2025.2-Tool-with-2025.x-Tool)；2025.2，2025-11-20 | 已读章节。软件组件升级与主机工具升级有区别；文档特别说明 2024.1 到 2024.2 的 SDK update 受 Yocto 版本变化限制。不能从“小版本”推断任意组合兼容。 |
| XDC 组织 | [UG903 Recommended Constraints Sequence](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/Recommended-Constraints-Sequence)；2026.1，2026-07-01 | 已读章节。时钟必须先定义再引用；跨文件依赖和读取次序也影响约束是否生效。 |
| CDC 同步器属性 | [UG903 CDC Synchronizers and ASYNC_REG](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/CDC-Synchronizers-and-ASYNC_REG-Property)；2026.1，2026-07-01 | 已读章节。同步器触发器需合适的 ASYNC_REG 属性，以保留同步结构并支持布局优化。属性不能替代正确 CDC 协议。 |
| 复位设计 | [UG949 Synchronous Reset vs. Asynchronous Reset](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Synchronous-Reset-vs.-Asynchronous-Reset)；2026.1，2026-06-23 | 已读章节。需要复位时优先评估同步复位；异步复位必须同步释放。同时评估 BRAM/DSP 推断、扇出与布线成本。 |
| 方法论与跨域资料 | [UG949](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology)；2026.1，2026-06-23 | 已读目录及上述复位章节。Multi-Bit CDC 的正文主要为决策图，未解析图内分支；使用时另查器件 Libraries Guide/XPM 定义。 |
| 时序签核 | [UG906 Check Timing Section](https://docs.amd.com/r/2025.2-English/ug906-vivado-design-analysis/Check-Timing-Section)；2025.2，2025-12-10 | 已读同版本中文正文并定位英文页。完整签核要求覆盖路径终点，不能用正 WNS 掩盖未约束路径。 |
| 时序根因 | [UG906 Category 1: Timing](https://docs.amd.com/r/2025.1-English/ug906-vivado-design-analysis/Category-1-Timing)；2025.1，2025-05-29 | 已读章节。先核对路径要求和时钟关系，再区分逻辑延迟、网线延迟；检查 multicycle 对 setup/hold 的配套影响。 |
| HLS 接口选择 | [UG1399 Interfaces for Vivado IP Flow](https://docs.amd.com/r/en-US/ug1399-vitis-hls/Interfaces-for-Vivado-IP-Flow)；2026.1，2026-09-11 | 已读章节。Vivado IP flow 可生成存储、流和寄存器接口；必须显式核对顶层端口及控制协议，不能假定与 Vitis kernel flow 默认值相同。 |
| HLS 验证 | [UG1399 Running C/RTL Co-Simulation](https://docs.amd.com/r/en-US/ug1399-vitis-hls/Running-C/RTL-Co-Simulation)；2026.1，2026-09-11 | 已读章节。联合仿真需要 testbench；随机数据应固定后重放；计算 II 至少需要两个 transaction。按版本启用 stall/波形/dataflow 诊断。 |
| ILA/Debug Hub 时钟 | [UG908 Debug Core Clocks](https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging/Debug-Core-Clocks)；2026.1，2026-06-23 | 已读章节。发现与测量阶段检查相关时钟稳定、持续运行；探针采样时钟须与被观测信号匹配，核对 MMCM/PLL LOCKED。 |
| 调试产物 | [UG908 Writing Debug Probes Information](https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging/Writing-Debug-Probes-Information)；2026.1，2026-06-23 | 已读章节。探针信息存于 `.ltx`；非工程流该版本要求在 `opt_design` 后显式写出。将 `.bit/.ltx` 作为同次构建配对产物保存。 |
| AXI DMA simple mode | [PG021 Direct Register Mode](https://docs.amd.com/r/en-US/pg021_axi_dma/Direct-Register-Mode-Simple-DMA)；v7.1，2025-06-24 | 已读章节。检查地址宽度及高位寄存器、DRE/对齐；长度寄存器最后写；S2MM 缓冲区不得小于接收包。Micro DMA 的约束需单独处理。 |
| AXI DMA 配置 | [PG021 Field Descriptions](https://docs.amd.com/r/en-US/pg021_axi_dma/Field-Descriptions)；v7.1，2025-06-24 | 已读检索正文。核对 MM2S/S2MM、数据宽度、burst、DRE 等参数。具体 DRE 宽度支持以项目生成的 IP 版本为准。 |

## DMA、缓存一致性与 Linux 的实用来源

### 官方裸机例程

[Xilinx embeddedsw：xaxidma_example_simple_poll.c](https://github.com/Xilinx/embeddedsw/blob/master/XilinxProcessorIPLib/drivers/axidma/examples/xaxidma_example_simple_poll.c)，本次已读 `master` 页面（未锁定 commit，访问 2026-10-01）。例程假设 AXI Stream 回环，检查 DMA 是否为 simple 模式，先准备接收再发送，包含 cache maintenance 和数据校验。移植时从项目匹配的 release tag 取代码，改写内存布局、驱动配置和超时错误处理，不直接复制示例 DDR 地址。

[AXI DMA 驱动 API 文档源码](https://github.com/Xilinx/embeddedsw.github.io/blob/master/axidma/src/xaxidma.h)，本次已读地址转换与 cache coherency 段。裸机驱动的硬件 buffer/descriptor 地址与 CPU 访问地址需正确对应；缓存开启时，发送交接前和接收访问前分别遵循驱动要求。它不是 Linux 用户态任意虚拟指针可用的证据。

### 硬件一致性

[Zynq UltraScale+ MPSoC Cache Coherency](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842098/Zynq+UltraScale+MPSoC+Cache+Coherency)，AMD Wiki，更新 2025-04-16；**已读主要正文**，原文案例验证平台为 **ZCU102 + Vivado/Vitis/PetaLinux 2024.2**。

可执行结论：HPC/LPD 的一致性路径、CCI snoop、内存 shareability、AxCACHE/AxPROT 与启动初始化必须相互匹配。`dma-coherent` 是向 Linux 声明硬件已提供一致性，单独添加不会把非一致性硬件变成一致性硬件。原文存在必须在 APU 复位期间设置的案例寄存器，不能照搬为运行中 `devmem` 操作。案例地址、性能及 ZCU102 配置均不属于 FZ3B 实测结论。

### Linux 用户空间 DMA

[Linux DMA From User Space 2.0](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1027702787/Linux)，AMD Wiki，更新 2023-08-23；本次已读检索正文，案例测试为 ZCU102 / 2020.1。相关源代码入口：[software-prototypes/linux-user-space-dma](https://github.com/Xilinx-Wiki-Projects/software-prototypes/tree/master/linux-user-space-dma)（**本次仅定位，未审计源码**）。

该原型采用内核 DMA client/proxy 与用户程序协作，可作为 AXI DMA Linux 方案起点；需要重新核对目标内核 API、DMA engine、device tree、内存映射、中断、背压及缓冲区管理。原型吞吐数字不作为 FZ3B 验收指标。

[Linux DMA From User Space 背景页](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842418/Linux+DMA+From+User+Space)，更新 2022-01-19；本次已读检索正文。明确区分内核 DMA API、DMA engine 与用户层；UIO 自身不解决连续 DMA 缓冲区分配和缓存一致性。

## 将资料转成工程行为

下面是综合上述资料形成的工程规则；不是某一原文的逐句摘录，也不代表已在 FZ3B 上执行。

### 1. 开始前冻结可复现输入

记录工具完整版本及补丁、完整器件 part、板卡 revision、原厂 BSP/镜像版本、IP VLNV/参数、HDF/XSA 来源、Linux/bootloader/固件版本或 commit、host OS、编译器和许可证需求。默认优先复现原厂组合；工具混用必须有对应版本兼容说明或受控验证证据。

原厂旧项目、新版工具试验、已有 XCZU3EG 工程各自维护基线和构建目录。升级导致的 IP 变化、HDF→XSA、SDK→Vitis、传统 DTG→SDT、Yocto 语法/API 变化，逐项核对；不要把新版本文档中的命令回填到旧工程。

### 2. PS/PL 集成先建立接口契约

在 RTL/HLS/驱动之前记录：时钟及复位域、AXI 控制地址、数据位宽/字节序/包边界、传输方向、DMA 模式、最大长度、中断号/触发方式、内存归属与一致性策略。软件控制和大吞吐数据通道分别指定协议。对 HLS IP 检查导出的实际端口和寄存器表；不能只读 C 函数签名。

所有时钟先建模；所有 CDC 说明所用同步/握手/FIFO 方法。多位信号不能简单逐位加两个寄存器就声称一致。异步 FIFO、XPM、异步复位同步释放仍须按目标器件/工具文档核对约束与参数。

### 3. DMA 首次验证采用小数据闭环

先核对 Vivado address editor 与软件/设备树一致、AXI 通路可达、时钟复位有效，再做固定模式小包回环。扩展到不同长度、边界、重复交易、随机但可重放的数据、背压和超时故障。记录发送/接收长度及逐字节或 CRC 比较，核对 AXI Stream 的 `TVALID/TREADY/TLAST/TKEEP` 契约。

不直接复制案例物理地址，不用 `volatile` 代替 cache maintenance。Linux 使用内核 DMA API 返回的 DMA 地址和受控缓冲区；由驱动管理生命周期、同步、错误恢复。选择硬件一致性时先证明整条链成立，再声明 `dma-coherent`。

### 4. 验收分层，性能按实测定义

- 仿真：testbench/golden model、输入种子、事务数、误差标准和失败波形。
- 综合：推断的 BRAM/DSP/寄存器、资源占用、锁存器、IP 配置及警告。
- 实现：`check_timing`、timing summary、DRC、CDC、clock interaction、未约束与被忽略路径；setup/hold 和路径覆盖共同评审。
- 上板：构建哈希、串口日志、JTAG 目标、`.bit/.ltx` 配对、ILA 触发条件、真实输入输出。
- 性能：明确传输字节、计时边界、重复次数、CPU 参与、cache 状态、时钟和精度；分别报告算法估算、HLS 估计、post-route 时序与实板吞吐。

### 5. 启动与调试按失效阶段收敛

按 BootROM/启动介质 → FSBL/PS 初始化 → PMUFW/TF-A → U-Boot → kernel/设备树 → rootfs/驱动 → 用户程序保留证据。PMUFW 不是简单串行链的一环；PL 配置也可能放在不同阶段。根据实际 BIF/启动日志确认镜像组成和装载位置。

ILA 无法发现时先查 Debug Hub 时钟、PS 生成 PL clock 是否已初始化、MMCM/PLL 锁定和 probes 配对；采样跨域信号时明确可解释范围。执行硬件写入前，应有匹配 FZ3B 实物的板级证据和可回滚启动介质。

## 按需补充与维护

实际任务涉及尚未读的模块时，再读对应版本正文；不要将“官方链接存在”升级成“参数已核验”。本次未完成 UG1085 全文、UG1087 寄存器位级审查、FZ3B PS preset/电气约束、DMA proxy 源码审计或任何上板测试。

每次解决新问题后记录：问题触发、完整版本、官方章节、最小复现、实际修复和证据层级。源码链接从 `master` 改为已验证 commit；失效链接先通过 AMD 文档编号与标题重新定位，保留旧版本语义。
