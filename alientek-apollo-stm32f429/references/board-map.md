# 板卡资源、内存与冲突速查

## 权威本地资料

- 资料根目录：`E:\阿波罗STM32F429 资料盘(A盘)`
- 核心板原理图：`3，ALIENTEK阿波罗STM32F429开发板原理图\Apollo STM32F429_CORE_V1.6.pdf`
- 底板原理图：`3，ALIENTEK阿波罗STM32F429开发板原理图\Apollo STM32F4&F7_MotherBoard_V1.5.pdf`
- 完整引脚表：`3，ALIENTEK阿波罗STM32F429开发板原理图\阿波罗STM32F429开发板IO引脚分配表.xlsx`
- 若用户的 PCB 版本不同，先核对丝印和该版本原理图，不要假定本表完全适用。

## 核心器件与存储空间

| 资源 | 容量/地址 | 开发约束 |
|---|---:|---|
| STM32F429IGT6 内部 Flash | 1 MiB，`0x08000000` | 原 Keil 工程 IROM 大小 `0x100000` |
| 主 SRAM | 192 KiB，`0x20000000` | DMA 可访问 |
| CCM SRAM | 64 KiB，`0x10000000` | DMA 不可访问，适合 CPU 私有高速数据 |
| W9825G6KH SDRAM | 32 MiB，`0xC0000000` | 使用前完成 FMC/SDRAM 初始化；大帧缓冲常放这里 |
| MT29F4G08 NAND | 512 MiB，FMC Bank3 `0x80000000` | 命令/地址偏移分别为 `1<<16`/`1<<17`；必须做坏块/ECC策略评估 |
| W25Q256 SPI NOR | 32 MiB | SPI5；超过 16 MiB 地址需 4 字节地址处理 |
| 24C02 EEPROM | 256 B | 与多个器件共用软件 I2C 总线 |
| MCU TFT 控制口 | FMC NE1 + A18，基址宏约 `0x6007FFFE` | 与 SDRAM/NAND 共用大量 FMC 引脚 |

原内存管理例程把主 SRAM 约 160 KiB、SDRAM 约 28.2 MiB、CCM 约 60 KiB 划为内存池。只有在沿用该分配器时采用这些数值。

## 时钟与调试

- HSE：25 MHz，PH0/PH1；LSE：32.768 kHz，PC14/PC15。
- 通用例程常用 `Stm32_Clock_Init(360,25,2,8)`，对应约 180 MHz SYSCLK 和 45 MHz PLLQ 域。
- 部分 USB 例程用 `Stm32_Clock_Init(384,25,2,8)` 获得 48 MHz PLLQ，但 SYSCLK 达 192 MHz，超过 STM32F429 额定值。现代工程必须重新设计时钟；一个合规起点是 PLLM=25、PLLN=336、PLLP=2、PLLQ=7，对应 168/48 MHz，仍须按实际外设完整校验。
- 优先使用 SWD：PA13 SWDIO、PA14 SWCLK。PA15/PB3/PB4 的 JTAG 功能与摄像头信号冲突。

## 板载人机接口

- LED：PB1 红色 DS0、PB0 绿色 DS1，均为低电平点亮。
- 按键：PA0 `WK_UP` 高电平有效；PH3 `KEY0`、PH2 `KEY1`、PC13 `KEY2` 低电平有效。
- USART1 调试口：PA9 TX、PA10 RX，经 P4 接 CH340，常用 115200 8N1。
- USB_232 第一次枚举时，CH340 的 DTR/RTS 可能导致 MCU 连续复位数次；诊断启动异常时先排除此因素。

## 常用总线与板载器件

- 软件 I2C：PH4 SCL、PH5 SDA，4.7 kΩ 上拉；24C02、PCF8574、MPU9250、AP3216C、WM8978 共用。
- PCF8574：源码使用 8 位写地址 `0x40`。P0 BEEP、P1 AP3216C INT、P2 DCMI PWDN、P3 USB power、P4 扩展 IO、P5 MPU9250 INT、P6 RS485 RE、P7 Ethernet reset。保留位要采用读改写，避免误切换其他设备。
- W25Q256/SPI5：PF7 SCK、PF8 MISO、PF9 MOSI、PF6 CS。
- 无线 SPI2：PB13 SCK、PB14 MISO、PB15 MOSI、PG10 CS、PG12 CE、PI11 IRQ。
- USART2：PA2/PA3，经 P8 选择 RS232/RS485；PA2 还与 Ethernet MDIO 共用，PA3 还与 PWM DAC 共用。
- USART3：PB10/PB11，经 P9 接 RS232/ATK 模块；PB11 还与 RMII TX_EN 共用。

## Ethernet RMII

- LAN8720A：PA1 REF_CLK 50 MHz、PA2 MDIO、PC1 MDC、PA7 CRS_DV、PC4 RXD0、PC5 RXD1、PB11 TX_EN、PG13 TXD0、PG14 TXD1。
- PHY reset 由 PCF8574 P7 控制。初始化 Ethernet 前先初始化 I2C/PCF8574。
- PA1 常有 50 MHz 信号，不适合作为普通 GPIO。启用 Ethernet 时不能同时占用 PA2 或 PB11 的串口复用。

## 摄像头 DCMI 与 SDIO

- DCMI：PA6 PCLK、PA8 XCLK、PB7 VSYNC、PH8 HREF；D0..D7 依次为 PC6、PC7、PC8、PC9、PC11、PD3、PB8、PB9。
- 摄像头控制：PB3 SDA、PB4 SCL、PA15 RESET；PCF8574 P2 控制 PWDN。
- 个别 README 把 HREF 写成 PH7，或倒序描述 D0..D7。原理图、引脚表和 `实验37\HARDWARE\DCMI\dcmi.c` 的初始化确认 HREF 为 PH8；不要照抄错误说明。
- SDIO：PC8 D0、PC9 D1、PC10 D2、PC11 D3、PC12 CLK、PD2 CMD。PC8/PC9/PC11 与 DCMI 数据线冲突。
- PA8 接红外接收相关电路并用作 DCMI XCLK；资料建议不要将其当普通输入，输出用途也要先检查板上电路。

## 显示、触摸与音频

- MCU TFT：FMC NE1 + A18 RS；背光 PB5。
- 触摸：PG3 MISO、PH6 SCK、PI3 MOSI、PI8 CS、PH7 PEN。
- LTDC RGB565：PF10 DE、PG7 CLK、PI9 VSYNC、PI10 HSYNC；R 为 PH9..PH12/PG6，G 为 PH13..PH15/PI0..PI2，B 为 PG11/PI4..PI7。背光仍为 PB5。
- WM8978/SAI：PE2 MCLK、PE3 ADCDAT、PE4 LRCLK、PE5 BCLK、PE6 DACDAT；寄存器配置走共享 I2C。

## 模拟、USB、CAN 与跳帽

- PA5 为 STM_ADC/TPAD，经 P11 选择；PA4 为 DAC_OUT1 且与 ATK 模块 LED 相关；PA3 为 PWM DAC，经 P1/P11 选择。
- CAN 与 USB 共用 PA11/PA12，通过 P10 选择。USB HOST 与 SLAVE 也共用连接，不能同时使用。
- P5 默认把 VREF+ 接 3.3 V，会使核心板 PWR 与 DS0 指示灯不工作；移除跳帽后才能观察它们。核心板 DS0 仍与 PB1 共用。

## 供电与实物检查

- 大尺寸 LCD、网络、摄像头等组合负载可能超过单路 USB 供电能力。资料建议使用外接 6–16 V 电源，典型为 12 V/1 A。
- USB 供电按单口约 500 mA 评估；核心板 3.3 V 输出约不超过 300 mA，底板 3.3 V 约不超过 500 mA，底板 5 V 在 USB/外接供电下约分别不超过 500 mA/1 A。
- TFT 白屏先检查连接器、供电、背光及串口打印的 LCD ID。全尺寸 SD 卡槽使用 microSD 时需要转接套。
- NAND 示例仅在指定测试扇区操作；不要在不了解坏块和文件系统布局时写任意地址。
