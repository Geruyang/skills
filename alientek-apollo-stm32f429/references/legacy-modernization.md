# 旧工程复现、现代化与验证

## 已识别的工具链基线

- 标准例程说明以 Keil MDK 5.21 为主。
- 69 个工程均选择 `STM32F429IGTx`，大多数使用 `Keil.STM32F4xx_DFP` 2.7.0，另有 2.8.0/2.9.0。
- 标准工程多数含 STM32CubeF4 HAL 1.3.2；CubeMX 模板标记 STM32Cube FW_F4 1.11.0。
- 常见宏为 `USE_HAL_DRIVER,STM32F429xx`，启用 Cortex-M4 FPU。
- 原 HEX 通常位于各实验的 `OBJ` 目录。重新构建时不要把旧 HEX 当作当前源码的证明。

## 两种工作模式

### 复现原例程

- 尽量使用原 Pack/HAL/ARMCC5 配置和目录结构，先实现零修改构建。
- 不因警告而批量格式化或升级库；记录版本、构建命令、产物和实机现象。
- 原工程能运行但违反现代设计准则时，明确标为“遗留复现”，不要把风险隐藏起来。

### 现代化移植

- 先为原例程建立可观测基线，再逐层替换启动文件、CMSIS/HAL、编译器适配和应用代码。
- 每次只改变一个边界：编译器、HAL、时钟、链接布局、RTOS 或驱动，不要同时大换血。
- HAL/CMSIS 版本升级后复核结构体字段、回调、时钟 API、中断名、USB/lwIP glue 和编译器宏。

## 编译器相关陷阱

- `SYSTEM\sys\sys.c` 中常见 ARMCC5 的 `__asm void` 函数。ARMClang/GCC 移植时优先改为 CMSIS 内建函数，如 `__WFI()`、`__disable_irq()`、`__enable_irq()`、`__set_MSP()`，并核对屏障指令。
- `SYSTEM\usart\usart.c` 常用 `#pragma import(__use_no_semihosting)`、旧式 `struct __FILE` 和 `fputc` 重定向。按所用 C 库实现 retarget，不要保留无效 pragma。
- Keil 工程文件和旧中文源文件可能不是 UTF-8。只做必要的行级修改并复核编码。

## Tick、RTOS 与中断

- 原 `delay.c` 直接配置并使用 SysTick，`SYSTEM_SUPPORT_OS` 还会把它接入 uC/OS。HAL 自身、FreeRTOS 和其他时间基准也可能需要 SysTick。
- 现代化时指定唯一 tick 所有者；必要时把 HAL tick 移到通用定时器，或由 RTOS hook 驱动。不要重复安装 SysTick Handler。
- 资料中的 FreeRTOS 基线常见 1 kHz tick、32 个优先级、最小栈 130 words、动态分配和约 46 KiB heap；这些只是示例参数，必须按应用重新估算。
- Cortex-M4 NVIC 优先级分组、`configPRIO_BITS`、`configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY` 与每个使用 `FromISR` API 的中断必须一致。禁止在高于允许阈值的中断中调用 RTOS API。
- DCMI 原例程把中断优先级设置为 0；接入 FreeRTOS 后要审查其 ISR 是否调用 RTOS API，并据此调整设计或优先级。

## 时钟树

- 对 25 MHz HSE 明确列出 PLLM/N/P/Q、SYSCLK、AHB、APB1、APB2 和 48 MHz 域。
- 检查 APB 分频后的定时器倍频规则，以及 Flash latency、电压档位、OverDrive 和功耗限制。
- 原通用例程的 180/45 MHz 配置适合许多普通外设，但不满足严格 48 MHz 域。
- 原 USB 例程的 192/48 MHz 配置超过芯片额定主频，不能用于现代生产配置。重新设计合规时钟并在硬件上验证 USB/SDIO/RNG。

## 内存、DMA 与缓存

- 保持链接区与芯片真实容量一致：Flash 1 MiB、主 SRAM 192 KiB、CCM 64 KiB。
- DMA 缓冲区绝不放 CCM。外设 DMA 的目标地址、宽度、突发、FIFO、对齐和生命周期要逐项核对。
- 使用 SDRAM 前完成 GPIO/FMC/时序/刷新初始化和读写测试。帧缓冲、堆或大数组迁移到 SDRAM 后更新链接文件并做越界检查。
- STM32F429 没有 Cortex-M7 D-cache，但外部存储器、LTDC/DCMI 双缓冲和 DMA 仍需要处理并发访问、撕裂和内存屏障。
- NAND 需要坏块、ECC、擦写寿命和掉电一致性方案；示例的裸扇区读写不能直接等同于产品存储层。

## 外设依赖与文档错误

- Ethernet reset 经 PCF8574，所以 LAN8720 初始化依赖共享 I2C 与 PCF8574。
- 摄像头 PWDN 经 PCF8574，控制 I2C 与 DCMI 数据/同步信号分别初始化。
- 旧 LCD 驱动可能在初始化时 `printf` 检测信息；未先启用 USART1 时，表现可能与显示故障混淆。
- 实验 29 的 README 现象描述误复制了按键/LED 内容；实际源码配置 CAN1 500 kbit/s，KEY0 发送数据，WK_UP 切换 loopback/normal。
- 摄像头部分 README 把 HREF 写为 PH7或倒序描述数据线；原理图、引脚表和 DCMI 初始化应作为修正依据。

## 分层验证清单

1. **静态**：器件型号、宏、启动文件、链接区、时钟公式、引脚 AF、DMA 可达性、NVIC 规则。
2. **构建**：零错误，解释所有新增警告；记录工具链、Pack/HAL 版本、RAM/Flash 占用与产物路径。
3. **启动**：复位原因、SystemCoreClock、串口、HardFault 捕获、看门狗与电源稳定性。
4. **外设**：先做最小读写/回环/ID 测试，再叠加中断、DMA、RTOS 和高吞吐。
5. **组合**：验证共享引脚、跳帽、总线仲裁、PCF8574 位状态和总功耗。
6. **压力**：长时间、边界尺寸、掉电恢复、通信错误、存储耗尽和任务栈余量。
7. **交付**：区分“已编译”“已仿真”“已下载”“已实机通过”，没有证据时不要写成已验证。

