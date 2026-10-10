# ALINX 案例地图：面向 FZ3B 的方法迁移

核查日期：2026-10-01（Asia/Shanghai）。这是按开发任务挑选的实读记录，不表示已遍历 ALINX 全站。ALINX AXU 系列、AX7010 与用户的 EdgeBoard FZ3B 是不同板卡；本文件不提供 FZ3B 的引脚、电压或 PS 初始化依据。

## 1. 资料入口与实际读取范围

| 入口 | 本次证据状态 | 用途和版本边界 |
| --- | --- | --- |
| [ALINX 中文官网](https://www.alinx.com/) | 已访问，但本次正文提取为空 | 官方入口保留；不能称已读完其产品、课程、下载区 |
| [ALINX 文档中心](https://docs.alinx.com/index.html) | 已读导航和简介 | 产品手册入口。其 [MPSoC 分类](https://docs.alinx.com/wiki/AMD-Dev-Board/MPSoC.html) 本次仅返回分类标题，未提供可读 MPSoC 手册正文 |
| [ALINX MPSoC 博客目录](https://www.cnblogs.com/alinx/category/1918718.html) | 已读目录；下文指定章节已读正文 | 页面署名 ALINX 官方博客、声明创作为芯驿电子，链接官网；下列 MPSoC 章节发表于 2021 年，不能据此推定当前工具操作不变 |
| [ALINX AXU2CG-E / AXU3EG / AXU4EV-E / AXU5EV-E 仓库](https://github.com/alinxalinx/AXU2CG-E_AXU3EG_AXU4EV-E_AXU5EV-E) | 已读 README、根目录与 Linux 目录；未逐一审查全部源码 | README 要求 Vivado 2020.1，可参考 Tcl 重建工程的组织方式。实际采用前固定 commit，检查文件级许可证和工具版本 |
| [AX7010 在线教程](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/) | 已读总目录及下文标记章节 | 网站页脚为 ALINX 版权并链接官网；这是 Zynq-7000 教程，仅补充通用练习。不是 MPSoC/FZ3B 板级资料 |
| [AX7010 文档版本履历](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S1_RSTdocument_CN/00_%E6%96%87%E6%A1%A3%E7%89%88%E6%9C%AC%E5%B1%A5%E5%8E%86_CN.html) | 已读正文 | 明示 1.01，2024/1/12，由 2019v1.04 更新为 2023v1.01；下文 Linux 章节出现 Vivado 2023.1 路径。站点 `latest` 是移动链接，不能只凭域名判断精确构建版本 |
| [AXU3EG 用户手册 PDF 入口](https://www.alinx.com/public/upload/file/AXU3EG_User_Manual.pdf) | 仅索引；直接访问本次未取到 PDF 正文 | 不据搜索摘要提取型号参数，不作为 FZ3B 硬件证据 |

## 2. 优先使用的 MPSoC 案例

下面的“迁移任务与验收”是本技能对教程的工程化应用建议，不是 ALINX 宣称已在 FZ3B 上验证的结果。

| 案例与来源 | 本次实读要点 | 迁移任务与验收 |
| --- | --- | --- |
| [第 29 章：PL 端 AXI GPIO](https://www.cnblogs.com/alinx/p/14311788.html)；2021-01-22；`ps_axi_gpio` | 配置 GPIO 输出与输入、中断，连接 PS 访问路径，使用 Vitis 驱动例程、地址编辑器与寄存器文档 | 可作第一个 PS→PL 控制实验。使用 FZ3B 已核验基础工程；核对 AXI 时钟/复位、地址、IRQ，再做寄存器读写及中断计数。原文 LED/KEY 的 XDC 不可复用 |
| [第 30 章：自定义 IP](https://www.cnblogs.com/alinx/p/14311827.html)；2021-01-22；`custom_pwm_ip` | 以 PWM 演示 AXI4-Lite 寄存器、IP Packager、重打包与软件访问 | 可迁移“寄存器控制计算核”的组织方式。先明确寄存器宽度、偏移、复位值、读写属性和更新时机，再验证背压、字节使能和复位；原文 UI 步骤按已安装版本转换 |
| [第 32 章：PL 读写 PS DDR](https://www.cnblogs.com/alinx/p/14343483.html)；2021-01-29；`pl_read_write_ps_ddr` | PL AXI Master 经 PS 内存访问端口、分配地址并用 ILA/软件检查数据 | 适合学习数据路径，但不能用理论总线带宽代替实测吞吐。缓冲区必须避开程序和系统占用区；先验证小块读写，再扩大长度/并发，并记录错误响应与超时 |
| [第 33 章：BRAM 实现 PS/PL 交互](https://www.cnblogs.com/alinx/p/14415706.html)；2021-02-19；`bram_test` | AXI BRAM Controller 与双口 RAM，自定义 PL 控制器，中断通知 | 适合小批量共享数据或控制邮箱。定义缓冲区所有权、起止握手、字节地址与 BRAM 索引转换；验收两端数据一致和重复请求行为 |
| [第 23 章：PS 端 DP](https://www.cnblogs.com/alinx/p/14297999.html)；2021-01-19；`ps_dp` | 使用 PS DisplayPort/DPDMA 及 Vitis 示例输出图像 | 是 PS 显示路径参考；是否适用于 FZ3B 要由其真实接口电路和 BSP 决定。不能把“板上有 HDMI”自动解释成 PS DP 路径或沿用 ALINX 驱动选择 |

原文教程明确列出 AXU2CGA、AXU2CGB、AXU3EG、AXU4EV/AXU5EV 及若干其他 ALINX 型号，未列出 FZ3B。这一适用范围比“同属 Zynq UltraScale+”更具体，迁移时必须保留。

## 3. DMA、视频与 HLS 补充练习

本节来源全部为 AX7010（Zynq-7000），不是 FZ3B 参考工程。只提取数据流、调试和验证方法；PS IP、CPU 架构、端口、启动链和电气部分必须回到 FZ3B 与 MPSoC 文档。

| 案例与实读链接 | 可迁移的内容 | FZ3B 上必须重新验证 |
| --- | --- | --- |
| [DMA 环通测试](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S2_RSTdocument_CN/15_DMA%E7%8E%AF%E9%80%9A%E6%B5%8B%E8%AF%95_CN.html)；正文已读；`dma_loopback` | 内存→MM2S→AXI Stream FIFO→S2MM→内存；完成中断、缓存处理、ILA 捕获与数据对比 | 当前 IP 模式及长度限制、地址宽度/对齐、内存所有权、缓存一致性方案、TLAST/TKEEP、IRQ 映射。先完成环通，再接自定义流核；Linux 下采用对应内核 DMA API/驱动，不能直接搬裸机缓存代码 |
| [使用 VDMA 驱动 HDMI 显示](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S2_RSTdocument_CN/14_%E4%BD%BF%E7%94%A8VDMA%E9%A9%B1%E5%8A%A8HDMI%E6%98%BE%E7%A4%BA_CN.html)；正文已读；`vdma_hdmi_out` | 帧缓存、VDMA、VTC、AXI 流转视频、不同视频时钟的分工 | 真实输出芯片与拓扑、像素格式、stride、帧率、时钟域、帧同步、缓冲区切换。原文直接 TMDS 输出及其 XDC 不能套到 FZ3B；原文时钟数值不作为通用模板 |
| [初识 HLS](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S3_RSTdocument_CN/01_led_control_CN.html)；正文已读；`led_control` | C/C++ 顶层、接口指令、综合报告、IP 导出及 Vivado 集成的基本路径 | 工具版本、目标 part、时钟和控制协议。补齐自检 C 仿真与 C/RTL 协同仿真；HLS 估算时序不是布局布线后时序；不要把 C 循环次数直接当作硬件延时保证 |
| [边缘检测](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S3_RSTdocument_CN/08_edge_detector_CN.html)；正文/主要代码已读；`edge_detector` | 灰度转换、Sobel、阈值处理，`xf::cv::Mat`、DATAFLOW、AXI Stream 与 AXI-Lite 参数 | 库版本/API、数值范围和边界像素、帧尺寸、流协议、背压与 FIFO 深度。用固定图片与软件 golden model 对比，再检查综合资源/II、协同仿真和系统吞吐 |

建议的最小进阶链：寄存器控制 → BRAM 数据交换 → DMA 环通 → 接入自定义核 → 视频/采集真实外设。每一步保存输入、期望值、日志和报告；不要跳过环通，直接把算法、DMA、摄像头和显示同时接入后才排错。

## 4. Linux 资料与边界

1. [MPSoC 仓库 Linux README](https://github.com/alinxalinx/AXU2CG-E_AXU3EG_AXU4EV-E_AXU5EV-E/blob/master/linux/README.md)：已读。明确分开各 AXU 型号的 XSA、PetaLinux 工程、SD 启动说明和外设说明。可借鉴这种目录与交付物组织；其中 XSA、BSP、设备树、boot 文件属于 ALINX 板卡。
2. [MPSoC Linux 外设使用](https://github.com/alinxalinx/AXU2CG-E_AXU3EG_AXU4EV-E_AXU5EV-E/blob/master/linux/documents_CN/use_peripherals_interfaces.md)：已读 UART、CAN、MIPI、GPIO、网络与存储等段落。可借鉴按接口逐项测试，以及用媒体拓扑工具检查摄像头链路的思路。具体 `/dev` 节点、GPIO 编号、IP 地址、摄像头实体名、驱动和脚本路径全部为该系统实例，不能作为 FZ3B 常量；文中含分区/格式化示例，不自动执行。
3. [MPSoC SD 启动说明](https://github.com/alinxalinx/AXU2CG-E_AXU3EG_AXU4EV-E_AXU5EV-E/blob/master/linux/documents_CN/make_sd_for_runnging_linux.md)：已读。用于认识启动分区与根文件系统分离、启动日志留存等流程。其拨码、供电、账号、镜像和分区布局都不构成 FZ3B 指令。
4. [MPSoC PetaLinux 构建说明](https://github.com/alinxalinx/AXU2CG-E_AXU3EG_AXU4EV-E_AXU5EV-E/blob/master/linux/documents_CN/use_petalinux_to_make_linux.md)：仅索引，README 确认入口；本次正文抓取失败。按需重新读取后再用于步骤生成。
5. [AX7010 使用 PetaLinux 定制 Linux](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S4_RSTdocument_CN/05_%E4%BD%BF%E7%94%A8Petalinux%E5%AE%9A%E5%88%B6Linux%E7%B3%BB%E7%BB%9F_CN.html)：已读工程建立部分。可参考 XSA→系统工程→构建的交付链，但原文 `zynq` 模板属于 Zynq-7000；为 FZ3B 必须使用匹配其平台和版本的 MPSoC 工程，不能照搬命令。
6. [AX7010 Linux AXI DMA 读写测试](https://ax7010-20231-v101.readthedocs.io/zh-cn/latest/7010_S4_RSTdocument_CN/15_AXI%20DMA%E8%AF%BB%E5%86%99%E6%B5%8B%E8%AF%95_CN.html)：正文已读；`sg_dma_test` 用 SG DMA+FIFO 环通、内核 DMA 测试客户端和设备树描述验证传输。移植时核对实际内核驱动和设备树 binding；原文的测试通过与带宽只属于其例程，不是 FZ3B 性能数据。

## 5. 迁移清单：保留方法，替换板级配置

| 项目 | 可从案例借鉴 | 必须使用目标板证据重新建立 |
| --- | --- | --- |
| RTL/HLS 算法 | 架构、接口分层、参考算法、仿真思想 | 位宽、流水线、时钟、资源目标、许可证与可综合性 |
| AXI 控制/数据 | AXI-Lite 控制、AXI-MM/Stream 数据路径、BRAM/DMA 分工 | PS 端口类型、地址范围、宽度、时钟/复位、IRQ、缓存/内存属性 |
| 约束 | 文件分层、命名方法、约束审查步骤 | 全部 `PACKAGE_PIN`、`IOSTANDARD`、Bank 电压、差分/时钟/时序约束 |
| PS 初始化 | 配置项类别、XSA 交付思路 | DDR 芯片/拓扑/时序、MIO、外设 PHY、参考时钟、启动选项和 preset |
| 软件/系统 | 驱动调用模式、错误处理、日志、逐项验收 | 架构/工具链、BSP、设备树、驱动版本、boot components、rootfs 和启动介质 |
| 工程自动化 | Tcl 重建、源码与生成物分离 | part、board_part、IP 版本、路径、资源预算、时序目标 |

每次迁移先写差异表：源案例型号/版本 → FZ3B 型号/PCB revision/工具版本 → 保留项/替换项 → 证据 → 验收条件。若 FZ3B pinout 或 preset 缺失，仍可推进算法、自检仿真、接口设计和器件级分析，不能把 ALINX 的配置填进去伪装成已完成板级适配。

## 6. 已发现的文字问题与使用规则

- 第 32 章“PL 读写 PS DDR”的握手文字称发送方等待 READY 后才发 VALID，这会允许与合法接收方形成互等。AXI 发送方不得使 VALID 的拉起依赖 READY；拉起后保持有效信息到握手完成。对照 [AMD UG1483 的 AXI4-Stream 握手说明](https://docs.amd.com/r/en-US/ug1483-model-composer-sys-gen-user-guide/AXI4-Stream-Support-in-Model-Composer)及 [Arm AXI 规范 IHI0022H，A3.3.1](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)；迁移时测试 READY 初始低、延迟及背压。本次勘误针对教程文字，不代表已审计该案例全部 RTL。
- MPSoC 的 PL 读写 DDR 章节仍出现 Zynq-7000 的说明；BRAM 章节沿用 GP Master 术语。将其视为需要校对的教程表述，端口和地址以当前 AMD MPSoC 文档及实际 BD 为准。
- DMA 环通章节中，长度寄存器“23 bits”与后续幂次/字节数不一致，缓存函数名也存在排版拼写问题。不抄这些数字和拼写；直接查当前 PG021、IP 参数和随工具安装的驱动源码/示例。
- GPIO 文中把直接寄存器操作概括为更高效，并非此技能接受的性能结论；是否优化必须由生成代码和测量支持。
- 网页代码存在空格、引号、标点和代码块渲染问题。实际复用优先获取原始工程源文件，保留版权说明，再做语法检查、仿真和驱动编译。
- 复用之前查看各文件许可证。页面可公开阅读不等于整个仓库或教程可以无条件再分发；本文件仅保存链接、简要方法总结和迁移检查项。

## 7. 尚未展开的目录

AX7010 总目录还列出 ADC/DAC 与 SG DMA、OV5640、USB 摄像头 OpenCV、以太网采集、PYNQ overlay、Linux 字符设备/中断/platform/DMA 驱动等课题。本次只核实目录存在，未审读这些章节的实现。具体项目命中某课题时再进入正文与原始源码，不根据标题生成详细操作。

ALINX 的配套工程、图片说明、云盘或下载包未在本次全部获取；本记录没有 FZ3B 实板测试。所有实读结论只是资料证据，不等于工程已经能在用户板卡运行。
