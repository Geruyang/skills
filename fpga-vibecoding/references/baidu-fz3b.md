# 百度 EdgeBoard FZ3B：官方资料与使用边界

检索日期：2026-10-01（Asia/Shanghai）。本文件是开发导航和核验规则，不是板级 XDC、PS preset 或已通过上板验证的 BSP。用户在本次对话明确实物为 **FZ3B**；芯片丝印、PCB revision、现有 TF 卡镜像与启动日志尚未核验。旧项目 MYD/MYC/MYB-CZU3EG-V3 的板级资料不能套用。

## 1. 板型与证据等级

官方目录的精确型号页是 [FZ3B 硬件说明](https://ai.baidu.com/ai-doc/HWCE/nkq9b5ncu)，页面日期 **2023-07-04**。以下均为该页的文档声明：

| 项目 | 文档声明 | 适用边界 |
|---|---|---|
| 器件 | `XAZU3EG-1SFVC784I` | 不擅自改成 `XCZU3EG`；创建工程前核对实物和 Vivado 可用 part |
| PS 内存/存储 | DDR4 4GB、64bit；eMMC 8GB；QSPI 256Mbit | 不据容量猜 DDR timing/preset |
| 接口 | USB 3.0/2.0、miniDP、千兆网、USB-UART、PCIe x1、TF、44pin、MIPI、BT1120 | 有连接器不代表当前镜像提供驱动 |
| 时钟 | PS 33.3333MHz；PL 25MHz，PL 时钟信号标为 1.8V | 不是所有 PL Bank 电压；详见第十九章 |
| 启动/电源 | JTAG、QSPI、eMMC、SD；12V/2A 适配器 | 拨码方向、极性须依实物与对应图核对 |

该页第十三至二十一章可查扩展接口、JTAG、启动拨码、LED、时钟和电源；按任务只读取需要的章节，逐信号登记来源，不批量复制网页生成约束。

[FZ3 系列介绍](https://ai.baidu.com/ai-doc/HWCE/9kr0f9lev)（2021-07-20）明确区分 **FZ3A：2GB/32bit** 与 **FZ3B：4GB/64bit**。`FZ3` 是系列称谓，不是可替代 `FZ3B` 的板级型号；系列性能表也不能直接作为用户系统的验收成绩。

## 2. 官方资料中的冲突与未决项

- 精确硬件页 QSPI 为 **256Mbit**，系列介绍写过 “max 256MB”；不得把后者当成实装容量。使用前对照料号、原理图及只读探测结果。
- 硬件页第十章写 MINI USB 并提到 USB 供电；[FZ3 简单上手](https://ai.baidu.com/ai-doc/HWCE/6kqqb1rp1)（2021-07-17）写 micro USB；[启动关机和重启](https://ai.baidu.com/ai-doc/HWCE/7kqg2gnxl)（2021-07-19）强调配套 12V 端子、其他口无供电功能。接口外形与供电路径必须核实，本技能不据冲突文字安排 USB 供电。
- 历史 [FZ3B 硬件介绍](https://ai.baidu.com/ai-doc/HWCE/Lkdfchunz)（2020-08-13）与当前页部分表格已有差异，例如 USB PS-GTR 的 lane 标注。不能把历史表、新表、社区 preset 拼成一份未经验证的板级设计。
- 当前硬件说明的 DP 段落与其信号表也存在 lane 描述不一致；MIPI 章节含多种电压、具体信号关系须结合原理图。遇到图文冲突时保留冲突，不以多数投票或相邻开发板推断。
- 当前资料核验未得到与用户 PCB revision 绑定的完整原理图、DDR 配置/走线延迟、参考 Vivado 工程、官方 board files 或完整可重建 BSP。网页有引脚表不等于工程初始化已完成。

## 3. 两条开发路线必须先选清楚

[硬件 FAQ](https://ai.baidu.com/ai-doc/HWCE/akqgdblqi)（2022-01-19）明确：百度未公开 EdgeBoard 的 Vivado 工程源码；支持加载自定义 FPGA 固件，但原百度 AI 能力随之不可用；购买后可以申请硬件原理图。申请表及联系地址在该页第四问，发送申请仍需用户授权，不能代发邮件。

### A. 保留百度 AI 软核

适合模型部署、图像采集、预后处理、Linux 应用和已有 GPIO/串口功能。保留板型对应启动文件、FPGA 驱动、预测库与运行时组合；先运行同版本官方示例，再改业务代码。

1. 只读记录系统、内核、文件系统分区、启动文件与库版本；对当前可启动系统建立备份与回滚信息。
2. 选择下面版本矩阵中的同一组合，核对算子、模型格式、输入尺寸与精度。
3. 从单张固定图片建立结果基线，然后接 USB/网络视频，最后才加入业务通信。
4. 保持预处理、模型输出和业务逻辑可分别测试；保存样本、输出、错误日志与端到端耗时。

### B. 自定义 PL / PS-PL / Linux BSP

适合自研 RTL/HLS 加速器、AXI 外设、DMA 与系统设计。此路线按通用 Zynq UltraScale+ MPSoC 流程实施，但**板级初始化必须由 FZ3B 资料支持**。

1. 取得精确 FZ3B 修订对应的原理图、PS/DDR 配置、器件/Bank 电压/时钟/复位证据，以及可以回退的原镜像。
2. 参数未核实时可以做 RTL 仿真、协议验证和明确标为候选 part 的器件级综合，不能称为可安全烧录工程。
3. 先验证最小工程，再添加 AXI 寄存器、IRQ、DMA、Linux 驱动/设备树及应用；每次只扩大一个验证层级。
4. 下载前审查约束、时序、CDC、地址映射和启动产物一致性；自定义 bitstream 与官方推理运行时不能默认共存。
5. 文档访问与技能创建不包含格式化 TF 卡、修改拨码、烧写 flash、替换启动文件或主动运行升级脚本的授权。

以上工作流程是技能的工程约束，不是百度官方提供了一套开源 Vivado 参考工程的声明。

## 4. 原厂软件版本链与资源

| 资料 | 页面日期 | 已读信息及用途 |
|---|---|---|
| [1.8.1 版本](https://ai.baidu.com/ai-doc/HWCE/Fkuqounlk) | 2022-01-19 | 必须配套 Ubuntu 18.04；PaddleLite 2.9、PaddlePaddle ≤1.8.5、PaddleClas `release/static`、PaddleDetection `release/0.5`。提供 FZ3B 系统镜像、软核、PaddleLiteDemo 与通信示例链接。 |
| [1.8.2 版本](https://ai.baidu.com/ai-doc/HWCE/xl1enuz4m) | 2022-06-23 | 同列 Ubuntu 18.04 / PaddleLite 2.9 / PaddlePaddle ≤1.8.5；有 FZ3B 专用软核升级包及 Python RTSP 相关更新。 |
| [1.8.1 C++ 示例](https://ai.baidu.com/ai-doc/HWCE/fkuqqcnvp) | 2021-10-14 | CMake/Make 构建分类、检测、分割程序；系统 JSON 指输入源/模型路径，模型 JSON 指尺寸、格式、归一化等。无显示器先关闭 display。 |
| [模型支持列表](https://ai.baidu.com/ai-doc/HWCE/4kr20cvrw) | 2022-06-23 | 模型与结果表绑定训练/部署版本；不保证新 Paddle 模型或任意算子都可用。 |
| [算子支持列表](https://ai.baidu.com/ai-doc/HWCE/Zkr20dhan) | 2021-07-16 | `Y`、`A`、`N` 分别表示支持、ARM 侧支持、不支持；不能把 ARM fallback 算成 PL 性能。 |
| [PaddlePaddle 模型部署](https://ai.baidu.com/ai-doc/HWCE/lkqhhig4t) | 2021-07-19 | 核对导出格式、标签、RGB/BGR、尺寸和归一化；需将训练端与部署端表达式对齐。 |

明确可记录的无签名资源地址：[FZ3B_install_1.8.2.zip](https://platform.bj.bcebos.com/edgeboard/1.8.2/softcore/FZ3B_install_1.8.2.zip)。这里只核对了它由官方版本页链接，**没有下载、校验归档或运行安装**。1.8.1 镜像/示例及申请表链接含官网签名参数，未来从对应版本页重新获取，不把旧签名硬编码进脚本。

“软核”包含启动镜像、驱动和推理运行时等组件，不应误解成普通可单独替换的 Python 包。版本页的示范目录/命令常使用 FZ3A 或 FZ5D；实际使用必须选择 FZ3B 包、阅读包内 README 和安装脚本。先检查会改写的路径及备份能力，再按授权实施。

Paddle 部署页提及较新导出文件名，并不能覆盖版本矩阵的支持约束。先实证当前运行时能加载并给出正确结果；不要仅因名字相似就将新模型重命名成旧模型文件。

归一化等价关系来自模型部署页：若训练使用 `(x / 255 - mean_train) / std_train`，而目标示例使用 `(x - mean_edge) * scale_edge`，则 `mean_edge = 255 * mean_train`、`scale_edge = 1 / (255 * std_train)`。还需逐通道核对通道顺序、resize、crop 与布局。

## 5. 首次连接、外设与排障

| 主题 | 已读官方来源 | 技能执行规则 |
|---|---|---|
| 串口 | [串口连接设备通讯](https://ai.baidu.com/ai-doc/HWCE/ekqg8j58i)，2023-05-08 | 文档用 CP210x 驱动、115200、无流控。从实际枚举结果选择 COM，不写死 COM4。原厂默认登录只适用于未改密码镜像；不猜用户密码。 |
| 开关机 | [启动关机和重启](https://ai.baidu.com/ai-doc/HWCE/7kqg2gnxl)，2021-07-19 | 参考配套 12V 电源与极性图；FZ3 上电启动；正常系统先 `poweroff` 后断电。串口保留完整启动日志。 |
| GPIO | [预留 GPIO 输出](https://ai.baidu.com/ai-doc/HWCE/ikqge503h)，2021-10-27 | 官方镜像为 FZ3A/B 在 J12 配置 6 个 GPIO。Linux gpiochip base 可能变化，不硬编码文档示例数字；先核对内核接口、line 和已有占用。 |
| 视频输入 | [视频输入](https://ai.baidu.com/ai-doc/HWCE/Akqgdqd0u)，2023-03-31 | USB 与网络视频分开验证；FZ5/FZ9D 的额外解码能力不套到 FZ3B。 |
| 视频输出 | [视频输出](https://ai.baidu.com/ai-doc/HWCE/Kkqgdr88o)，2022-01-17 | FZ3 使用 miniDP；接 HDMI 显示器按官方资料选择主动式转换。检测模型成功与窗口显示成功分开记录。 |

GPIO 的“板上存在 IO”“官方 bitstream 配置为 GPIO”“Linux 当前映射到哪条 line”是三个不同层次。旧 sysfs 示例可解释历史系统，迁移到新内核先查实际 GPIO ABI，不机械复制 export 数字。

官方 C++ 示例的预测计时不含图像处理；只有 FZ9D 对应其多通道输入功能。FZ3B 业务验收应额外测采集/解码、预处理、拷贝、预测、后处理、显示/发送与整条管线，标明分辨率、输入模式、模型和版本。

## 6. 官方仓库与第三方资料边界

- [PaddlePaddle/Paddle-Lite](https://github.com/PaddlePaddle/Paddle-Lite) 和 [PaddlePaddle/Paddle-Lite-Demo](https://github.com/PaddlePaddle/Paddle-Lite-Demo) 是已查看的 Paddle 官方仓库入口，用于通用 API/示例研究；本次没有核验其当前分支能重建 FZ3B 的专用 FPGA 后端，不能替换板型专用安装包。
- 当前未定位到可取代上述闭源 AI 工程的百度官方 FZ3B Vivado 源码仓库。“未定位到”不扩展成所有项目源码不存在。
- 检索出现 [zhutmost/edgeboard](https://github.com/zhutmost/edgeboard)，仓库自述由个人维护且与百度无关。它提供社区资料线索；未审计源码、归档、许可证范围和板型兼容性。本技能不把其中 board files、PYNQ 镜像或 FZ3A 原理图当成 FZ3B 官方 BSP。
- ALINX 其他板卡案例可以学习 AXI、DMA、视频或 Linux 的方法；引脚、DDR/MIO、PS-GTR、时钟/复位和启动链必须重新适配 FZ3B。

## 7. 阅读覆盖与可追溯性

本次实读了用户提供的 [官方目录](https://ai.baidu.com/ai-doc/HWCE/Yk3b86gvp)（页面日期 2022-03-31）、上述各链接的相关正文，以及历史 FZ3B 页。没有遍历网站全部内容，没有下载大镜像、供应商私有包或执行硬件动作。

`web` 对精确 FZ3B、FZ3 产品、串口和部分示例页面曾超时；随后通过获批的只读 `Invoke-WebRequest` 获得这些官方页面 HTTP 200，并实际读取正文，不能把最初失败写成资料不存在。下载包的内容/可安装性与用户实物兼容性仍未验证。

未来更新时记录：访问日期、页面日期、板型与修订、段落/表名、冲突、下载后的 SHA-256、工具/运行时版本和验证等级。只对已核验字段升级结论；保留“文档声明 / 推断 / 器件级验证 / 实板验证”的区别。
