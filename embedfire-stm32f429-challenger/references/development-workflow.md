# 固件开发与验证工作流

## 1. 建立可复现基线

记录以下信息再改代码：

- 板卡：挑战者 V1 或 V2，PCB/核心板丝印和主要器件型号。
- 供电、屏幕/摄像头/模块型号、跳帽位置和连接方式。
- 编译器与版本、Keil Target、DFP/固件包版本、HAL 或标准库版本。
- 下载器、接口（SWD/JTAG）、串口号和波特率。
- 最接近需求的资料归档和归档内工程路径。

完全解压所选工程到较短路径，保持目录层次。不要直接从压缩包视图打开 `.uvprojx`，也不要把单个 Project 目录从共享 Libraries 中分离。

## 2. 快速找工程

在技能目录运行：

```powershell
./scripts/materials.ps1 -Action find -Pattern 'SDRAM|W9825|IS42S'
./scripts/materials.ps1 -Action list -Archive '1-程序源码_教程文档\0-[野火] 开发板实验应用源码\实验应用-F429IG_20260604.zip' -Pattern 'readme\.txt$|\.uvprojx$'
./scripts/materials.ps1 -Action extract -Archive '<相对或绝对 ZIP 路径>' -EntryPrefix '<归档内工程目录>' -Destination '<工作目录>'
```

选择顺序：匹配板卡版本和外设的完整例程 > 同库同架构的近似例程 > 通用 STM32Cube 示例。移植近似例程时先替换板级引脚、时钟、外部存储几何和中断/DMA映射，再改应用逻辑。

## 3. 审计工程配置

### Keil/MDK

- Target Device 是 `STM32F429IGTx`，启动文件为 `startup_stm32f429xx.s`。
- 预处理宏与库匹配，HAL 项目至少核对 `USE_HAL_DRIVER`、`STM32F429xx`。
- include path 和源文件没有红叉/叹号；相对路径没有因不完整解压而失效。
- IROM 为 1 MB；IRAM1 不超过 `0x30000`，IRAM2/CCM 不超过 `0x10000`。
- Scatter/链接脚本中的 SDRAM 起始地址、容量和段放置匹配 V1/V2。
- 编译器代际和选项与原工程一致；从 ARMCC5 迁到 ArmClang6 时单独处理汇编、内联汇编、库、对齐和告警差异。

### CubeMX

- 打开 `.ioc` 后先查看原始 MCU、固件包版本和 Toolchain，不立即覆盖生成。
- 核对 25 MHz HSE、时钟树和所有冲突引脚。
- 生成前保存用户代码；生成后审查差异，尤其是 MSP、IRQ、DMA、FMC、USB、ETH 和用户段。
- 若旧工程用不同 CubeF4 版本，只在有明确迁移目标时升级。

## 4. 计算时钟而不是读注释

对 PLL 源为 HSE 的常见配置：

```text
VCO_in  = 25 MHz / PLLM
VCO_out = VCO_in × PLLN
SYSCLK  = VCO_out / PLLP
PLL48   = VCO_out / PLLQ
```

随后应用 AHB/APB 分频，并计算 APB 定时器倍频。检查 STM32F429 数据手册规定的 VCO、总线和外设频率范围。USB、SDIO、RNG 使用 PLL48 域时必须满足各自容差，USB 目标是精确 48 MHz。

建议在早期启动阶段输出或断点检查：

- `SystemCoreClock`
- `HAL_RCC_GetSysClockFreq()`
- `HAL_RCC_GetHCLKFreq()`
- `HAL_RCC_GetPCLK1Freq()` / `HAL_RCC_GetPCLK2Freq()`
- RCC PLLCFGR、CFGR 和供电/OverDrive 状态

## 5. 外设实现检查表

### GPIO、EXTI、定时器

- 先使能 GPIO/SYSCFG/定时器时钟，再配置模式、速度、上拉和 AF。
- 清中断标志、设置 NVIC 优先级并保持中断处理短小。
- PWM/捕获频率按实际 timer kernel 计算；不要把 PCLK 当 timer kernel。
- LED 共阳低有效、蜂鸣器高有效、按键在示例中按下为高。

### UART、RS232、RS485、DMA

- 调试 USART1 通常为 PA9/PA10、115200 8-N-1；确认 CH340 跳帽。
- USART2 到 RS232/RS485 的物理跳帽必须匹配用途。
- RS485 DE/RE 方向脚按 V1/V2 选择；发送完成以 TC 而非仅 TXE 为准，再切回接收。
- UART IDLE + DMA 环形/双缓冲要处理溢出、半包、粘包和缓存生命周期。
- DMA 缓冲区不得放入 CCM。

### I2C、EEPROM、板载传感器

- I2C1 为共享总线；扫描前确认不会干扰摄像头、音频 Codec 或其他设备。
- AT24C02 的容量是 2 Kbit（256 字节）；注意页写边界和写周期轮询。
- 驱动先验证器件 ID/ACK，再进行批量传输。

### SPI NOR、FatFs

- 读取 JEDEC ID 后选择 W25Q128/W25Q256 几何。
- W25Q256 地址超过 16 MB 前启用 4 字节模式，并验证复位/掉电后的模式策略。
- 擦除前确认区域，轮询忙状态并设置超时。
- FatFs 磁盘扇区大小、擦除粒度、缓存和同步必须与底层 Flash 匹配。
- 不覆盖出厂资源区，除非任务明确包含资源重建。

### SDRAM、NAND、LCD/DMA2D

- SDRAM 选择 Bank2、正确行列位数、CAS、刷新率和容量边界。
- 初始化后先做地址线/数据线测试、步进模式和全范围块测试，再放 framebuffer/heap。
- V2 NAND 与 SDRAM 共用 FMC 时保持片选互斥。
- framebuffer 大小按宽 × 高 × 每像素字节数和层数计算，检查不越过实际 SDRAM。
- DMA2D/LTDC 颜色格式、stride、cache/同步策略一致；F429 无 M7 D-cache，但仍需处理总线竞争和异步完成。
- CAN 与 LCD 的 PB8/PB9 复用冲突必须在硬件配置层解决。

### SDIO、USB、Ethernet

- SDIO 与 Wi-Fi 复用：使用匹配板卡例程控制禁用脚/跳帽。
- SD 卡和 U 盘例程通常面向不大于 32 GB、FAT/FatFs 组合；不要把容量假设当协议上限。
- USB 首先验证 PLL48=48 MHz、VBUS/ID/供电角色、USB 引脚和中断。
- Ethernet 使用 LAN8720A RMII；检查 50 MHz REF_CLK 来源、PHY 地址、复位、MDIO/MDC、描述符和缓冲区内存区域。
- 网络问题按 PHY link → MAC/DMA → ARP/ICMP → IP 配置 → TCP/UDP/应用层逐层定位。

## 6. 构建、烧录与观察

1. 原始基线先完整构建一次，保存错误/警告、map 文件和产物尺寸。
2. 每个小改动后重建，比较 code/RO/RW/ZI 和链接映射。
3. 下载前再次确认 V1/V2、目标芯片、Flash 算法、起始地址和是否涉及外部存储。
4. SWD 下载后复位运行；不要把“下载成功”当作功能通过。
5. 使用串口日志、LED、示波器/逻辑分析仪、J-Link 断点/寄存器、LCD 或网络抓包取得可重复证据。
6. 对启动早死问题先断在 `Reset_Handler`、`SystemInit`、`main`、`HardFault_Handler` 和 `Error_Handler`。

## 7. 常见故障分层

| 现象 | 先检查 |
|---|---|
| Keil 文件叹号/找不到头文件 | 是否完整解压、路径是否过长、相对目录是否被拆散 |
| 一上电或下载后无响应 | 电源、BOOT、NRST、时钟起振、启动文件、向量表、看门狗 |
| HardFault | 堆栈、非法地址、FMC 未初始化即访问、栈溢出、错误函数指针、对齐 |
| DMA 无数据/总线错误 | 缓冲区是否在 CCM、DMA stream/channel、IRQ、长度和生命周期 |
| USB 枚举失败 | PLL48 是否精确 48 MHz、VBUS/角色、引脚、描述符、中断优先级 |
| SDRAM 随机错误 | V1/V2 几何、刷新率、时序、走线/供电、NAND 互斥、越界 |
| SPI Flash 16 MB 后回卷 | W25Q256 未进入 4 字节地址模式 |
| LCD 颜色/撕裂异常 | pixel format、stride、buffer 边界、LTDC/DMA2D 时序和层配置 |
| SDIO 或 Wi-Fi 互相影响 | 复用跳帽/禁用脚使用了错误板卡版本 |
| RS485 只能发不能收 | 方向脚版本不匹配、TC 前过早切换、偏置/终端和跳帽 |
| CAN 开启后 LCD 异常 | PB8/PB9 与 LTDC 冲突 |

## 8. 验证边界

明确区分以下状态：

- 已静态核对：代码、原理图、IO 表、配置相互一致。
- 已构建：编译和链接成功，产物可定位。
- 已下载：探针报告烧录/校验成功。
- 已上板验证：实际观察到串口、波形、显示、存储、网络或传感器结果。
- 未验证：没有实物、模块、探针或观测渠道时，不能声称硬件功能通过。

最终交付至少给出基线、改动、构建结果、产物、硬件假设和未验证项。
