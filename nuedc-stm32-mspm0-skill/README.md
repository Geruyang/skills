# NUEDC-STM32-MSPM0-SKILL

面向全国大学生电子设计竞赛（NUEDC）单片机项目的 Codex Skill，同时覆盖两套常见开发链：

- STM32CubeMX 配置 `.ioc`，生成 Keil MDK-ARM 工程并在 µVision 中编译、下载和调试。
- TI MSPM0 SysConfig 配置 `.syscfg`，在 Code Composer Studio（CCS）中生成 DriverLib 配置代码、编译、下载和调试。

本 Skill 的重点不是把两套厂商代码强行统一，而是先识别工程类型，再遵守各自的生成代码边界，并将可移植的协议、算法、状态机和控制逻辑放在用户代码层共享。

## 功能概览

| 能力 | STM32 路线 | MSPM0 路线 |
|---|---|---|
| 配置真源 | STM32CubeMX `.ioc` | TI SysConfig `.syscfg` |
| 主要 IDE | Keil MDK-ARM / µVision | Code Composer Studio |
| 运行时库 | STM32 HAL 或 LL | TI DriverLib |
| 工程入口 | `.uvprojx` | `.project`、`.cproject`、`.ccsproject`、`.projectspec` |
| 调试配置 | Keil Target/Debug 设置 | `targetConfigs/*.ccxml` |
| 常见输出 | `.axf`、`.hex`、`.map` | `.out`、`.hex`、`.map` |
| 生成代码保护 | `USER CODE BEGIN/END` 区域 | 不手改 `ti_msp_dl_config.c/.h` |

Skill 可以帮助 Codex：

- 检查工程属于 STM32、MSPM0，还是包含两个独立目标的混合仓库。
- 识别 `.ioc`、`.syscfg`、Keil、CCS、链接、启动、生成代码和构建输出。
- 配置 GPIO、UART、SPI、I2C、ADC、PWM、Timer、DMA、NVIC/IRQ 和时钟树。
- 处理串口协议、环形缓冲区、DMA 收发、RTOS 任务、中断与控制环。
- 在重新生成代码前保护用户逻辑，生成后检查句柄、宏、IRQ 和初始化函数变化。
- 在下载前只读探测 ST-Link、J-Link、XDS110、CMSIS-DAP/DAPLink。
- 按“静态检查 → 生成 → 编译链接 → 下载校验 → 板级观察 → 仪器测量 → 验收”逐级报告结果。

## 设计原则

### 1. 配置文件是唯一真源

STM32 工程以 `.ioc` 管理 MCU、封装、引脚、时钟、外设、DMA 和 NVIC。MSPM0 工程以 `.syscfg` 管理设备、封装、时钟、引脚、外设、事件、DMA 和中断。

不要为了临时通过编译而直接改生成代码。应修改配置真源、重新生成、检查差异，再让用户代码适配新的生成名称。

### 2. 不猜生成名称

不要从示例工程复制 `huart1`、`MX_USART1_UART_Init()`、`TIMER_0_INST` 或 `SYSCFG_DL_init()` 等名称。必须读取当前工程生成的头文件和源文件，使用本地真实名称。

### 3. 不混用厂商配置边界

STM32 HAL/LL 初始化与 TI DriverLib/SysConfig 初始化分别留在目标工程。两个平台可以共享协议定义、CRC、滤波、控制算法、状态机和测试向量，但应通过薄适配层访问 GPIO、Timer、UART、ADC、PWM 和 DMA。

### 4. 不把编译成功等同于硬件成功

Skill 会分别报告：

1. 源码与配置静态检查
2. CubeMX 或 SysConfig 生成
3. 编译和链接
4. 下载工具校验
5. MCU 启动和基础 I/O
6. 串口或逻辑协议观察
7. 示波器、逻辑分析仪、负载或闭环测量
8. 电赛题目验收结果

如果没有连接实物并完成测量，不会声称硬件功能已经验证。

## 目录结构

```text
nuedc-stm32-mspm0-skill/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── stm32-cubemx-keil.md
│   ├── mspm0-sysconfig-ccs.md
│   ├── nuedc-runtime-validation.md
│   └── flash-debug.md
└── scripts/
    ├── inspect_project.py
    └── detect_probe.py
```

- `SKILL.md`：Codex 触发后读取的核心工作流和安全规则。
- `agents/openai.yaml`：Codex Skill 的界面名称、简介和默认提示词。
- `references/`：按任务需要加载的 STM32、MSPM0、运行时验证和调试参考。
- `scripts/inspect_project.py`：只读工程类型与生成风险检查器。
- `scripts/detect_probe.py`：只读 USB 调试器探测器。

## 安装

### 安装到 Codex

将仓库克隆到 Codex Skills 目录，文件夹名称保持为 `nuedc-stm32-mspm0-skill`：

```powershell
git clone https://github.com/zww666-creater/NUEDC-STM32-MSPM0-SKILL.git "$env:USERPROFILE\.codex\skills\nuedc-stm32-mspm0-skill"
```

如果设置了 `CODEX_HOME`，也可以安装到：

```text
<CODEX_HOME>/skills/nuedc-stm32-mspm0-skill
```

重新打开 Codex 任务或刷新 Skill 列表后，使用以下名称触发：

```text
$nuedc-stm32-mspm0-skill
```

### 运行脚本的环境

- Python 3.10 或更高版本。
- `inspect_project.py` 支持常规 Windows、Linux 和 macOS 文件系统检查。
- `detect_probe.py` 当前实现 Windows 与 Linux 的只读 USB 探测。
- STM32CubeMX、Keil MDK、STM32Cube 固件包、TI MSPM0 SDK、SysConfig、CCS 和调试器驱动需要用户自行安装；本仓库不包含厂商工具或 SDK。

## 使用示例

### STM32CubeMX → Keil

```text
$nuedc-stm32-mspm0-skill
检查这个 STM32F407 的 CubeMX 工程，把 USART1 配成 115200 8N1，使用 DMA 循环接收和 IDLE 检测，然后重新生成 Keil 工程并编译。
```

Codex 应先确认板卡、封装、USART 引脚、时钟源、DMA 资源、缓冲区大小、帧格式、溢出策略、Keil 编译器和 Device Pack，再修改 `.ioc`。

典型 CubeMX 脚本形状：

```text
config load "C:\project\controller.ioc"
project toolchain MDK-Arm
project name controller
project path "C:\project"
project generate
exit
```

使用 `project generate` 生成完整工具链工程；`generate code` 不能替代完整的 Keil 项目生成。

Keil 命令行构建形状：

```powershell
UV4.exe -b controller.uvprojx -t"controller" -o build.log
```

实际可执行文件、目标名、编译器、器件包、源文件分组和 scatter 文件必须来自当前工程，不应重新猜测一套参数。

### MSPM0 SysConfig → CCS

```text
$nuedc-stm32-mspm0-skill
给这个 MSPM0G3507 CCS 工程增加 1 ms 定时器中断、ADC 定时采样和 UART DMA 上传，然后生成、编译并下载。
```

Codex 应读取 `.syscfg` 中的设备、封装、SDK、模块、引脚、时钟、事件和中断，并检查本地 `ti_msp_dl_config.h` 中的真实实例、IRQ、通道和初始化函数。

典型 SysConfig CLI 形状：

```powershell
<sysconfig-root>\sysconfig_cli.bat -o <output-dir> -s "<mspm0-sdk>\.metadata\product.json" --compiler ticlang <project>.syscfg
```

典型新版 CCS 命令行构建形状：

```powershell
ccs-server-cli -noSplash -workspace <workspace> -application com.ti.ccs.apps.buildProject -ccs.projects <project> -ccs.configuration Debug
```

CCS 不同版本的启动器、application 名称和参数可能不同，应先读取已安装版本的帮助，而不是混用新旧命令。

## 工程检查脚本

### 识别项目类型和风险

```powershell
python scripts\inspect_project.py <project-dir>
python scripts\inspect_project.py <project-dir> --json
```

检查内容包括：

- `.ioc`、`.syscfg`、`.uvprojx`、CCS 工程文件和 `.ccxml`
- MCU、封装、工具链、固件包或 SDK 元数据
- CubeMX 用户代码标记是否配对
- CubeMX 目标是否为 MDK-ARM
- SysConfig 元数据是否完整
- `ti_msp_dl_config.h` 中的生成初始化函数
- 启动、scatter/linker 文件和现有构建产物
- 同一目录是否同时包含两个需要分开处理的平台

返回码：

- `0`：识别到受支持的工程路线；警告会单独显示。
- `2`：路径无效或没有识别到目标工程。

### 探测调试器

```powershell
python scripts\detect_probe.py
python scripts\detect_probe.py --json
```

探测器只读取操作系统 USB/PnP 信息，不会连接 MCU、复位、擦除或下载程序。

返回码：

- `0`：检测到至少一个受支持的探针。
- `1`：没有检测到受支持的探针。
- `2`：系统查询失败或当前操作系统未实现探测。

探针类型只能用于缩小候选工具，不能单独决定下载后端。仍需核对 MCU 支持、工程配置、目标电压、SWD/JTAG 接线、复位方式和 `.ccxml`/Keil Debug 设置。

## 生成代码边界

### STM32

通常允许修改：

- `.ioc`
- 独立的用户模块
- 匹配的 `USER CODE BEGIN/END` 区域

通常不应直接修改：

- 生成文件用户区域之外的内容
- `Drivers/CMSIS/` 和 HAL Driver
- 自动生成的启动、system、linker/scatter 文件
- `.uvoptx`、`Objects/`、`Listings/`、`.axf`、`.map` 和 `.hex`

### MSPM0

通常允许修改：

- `.syscfg`
- 用户应用 `.c/.h`
- 确实需要变更时的 CCS 工程配置

通常不应直接修改：

- `ti_msp_dl_config.c/.h`
- 自动生成的 linker command、makefile 和 SysConfig 输出
- `Debug/`、`Release/`、对象、map 和 `.out`

## 下载与调试安全

执行下载前应先探测并核对调试器。以下情况应停止：

- 未检测到调试器。
- 同时检测到多个调试器，但目标不明确。
- 工程配置的探针与物理探针冲突。
- 目标电压、SWD/JTAG 接线或复位方式不明确。
- 操作会改变读保护、写保护、Option Bytes、安全区域、Boot 配置或校准数据。

本 Skill 不授权自动执行 mass erase、解锁、恢复出厂、保护位修改或其他破坏性恢复。实时控制系统打断点前，还应考虑电机、PWM、功率级、看门狗和通信超时在 CPU 停止时的状态。

## 验证情况

当前版本已经完成：

- Skill YAML/frontmatter 和目录结构校验
- 两个 Python 脚本的语法编译检查
- STM32 `.ioc + .uvprojx` 测试工程识别
- MSPM0 `.syscfg + CCS` 测试工程识别
- 非 MDK 工具链、关闭用户代码保护、缺少 Keil 工程和用户代码标记不配对的异常检查
- STM32 USART DMA 与 MSPM0 Timer IRQ 两个独立场景测试

这些验证证明了 Skill 和静态工具的行为，不代表已经在所有 STM32/MSPM0 型号、开发板、IDE 版本或实物硬件上完成验证。

## 官方参考

- [STM32CubeMX 用户手册 UM1718](https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf)
- [Keil µVision Command Line](https://www.keil.com/support/man/docs/uv4/uv4_commandline.asp)
- [TI MSPM0 SysConfig Guide](https://software-dl.ti.com/msp430/esd/MSPM0-SDK/latest/docs/english/tools/sysconfig_guide/doc_guide/doc_guide-srcs/sysconfig_guide.html)
- [TI CCS SysConfig Guide](https://software-dl.ti.com/ccs/esd/documents/ccs_sysconfig.html)
- [TI CCS Command-line Project Build](https://software-dl.ti.com/ccs/esd/documents/ccs_project-command-line.html)

## GitHub Topics

`nuedc` · `stm32` · `mspm0` · `stm32cubemx` · `keil` · `code-composer-studio` · `sysconfig` · `embedded-systems` · `firmware` · `codex-skill` · `driverlib` · `stm32-hal`
