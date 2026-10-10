# 板卡版本、引脚与硬件约束

## 版本识别

| 项目 | 挑战者 V1 | 挑战者 V2 |
|---|---|---|
| MCU | STM32F429IGT6，LQFP176 | STM32F429IGT6，LQFP176 |
| 核心板尺寸 | 84.4 × 47.5 mm | 55 × 55 mm |
| 底板尺寸 | 177.8 × 126.4 mm | 200 × 130.5 mm |
| HSE / LSE | 25 MHz / 32.768 kHz | 25 MHz / 32.768 kHz |
| SDRAM | IS42S16400J，8 MB，16 位 | W9825G6，32 MB，16 位 |
| SDRAM FMC | Bank2，`0xD0000000`，12 行/8 列 | Bank2，`0xD0000000`，13 行/9 列 |
| SPI NOR | W25Q128，16 MB | W25Q256，32 MB；16 MB 以上需 4 字节地址 |
| NAND | 无 | W29N01GVSIAA，128 MB；与 SDRAM 共享 FMC 信号 |
| EEPROM | AT24C02 在底板 | AT24C02 在核心板 |
| Wi-Fi | EMW1062 | AP6181 |
| 模拟旋钮 | 100 kΩ，PC3 | 1 kΩ，PC3 |
| 环境传感 | GL5516 光敏电阻，PA4 | AP3216C ALS/PS/IR，I2C1 |
| USB Device | Mini USB | Micro USB |
| RS232 | 1 路 | 2 路 |
| V2 特有 | — | LVDS/背光、EBF 模块口、扬声器、更多 GPIO 引出 |

V1 核心板插到底板时，Micro-USB 口应朝向 RGB LCD 接口；反插可能损坏器件。不要以项目名替代实物版本核验。

## 已核对的公共引脚

| 功能 | 引脚/配置 | 极性与说明 |
|---|---|---|
| RGB LED | PH10 红、PH11 绿、PH12 蓝 | 共阳，低电平点亮；V1 J35、V2 J73；与 DCMI 数据复用 |
| K1 / K2 | PA0 / PC13 | 配套 HAL 例程中按下读高；只有 PA0 具备 WKUP 功能 |
| 蜂鸣器 | PI11 | 高电平响 |
| USART1 调试 | PA9 TX、PA10 RX、AF7 | CH340：V1 J12/J11，V2 J80/J81；例程常用 115200 8-N-1 |
| USART2 | PD5 TX、PD6 RX | 可经跳帽选择 RS232/RS485 |
| RS485 方向 | V1 PD11；V2 PB8 | 必须使用匹配版本 BSP |
| I2C1 | PB6 SCL、PB7 SDA | 共用总线；V2 还连接摄像头控制、MPU6050、WM8978、AP3216C 等 |
| SPI5 NOR | PF6 CS、PF7 SCK、PF8 MISO、PF9 MOSI | V1/V2 容量及寻址方式不同 |
| 电位器 ADC | PC3 | V1 J21；V2 J77 |
| 电容按键 | PA5 | V1 J17；V2 J78 |
| V1 光敏电阻 | PA4 | J43；同时复用 DCMI HSYNC |
| CAN1 | PB8 RX、PB9 TX | 与 LTDC B6/B7 冲突，CAN 与屏幕不能同时直接使用 |
| SDIO | PC8~PC11 D0~D3、PC12 CK、PD2 CMD | 与板载 Wi-Fi 复用，按板卡版本关闭或隔离正确模块 |
| Ethernet RMII | PA1 REF_CLK、PA2 MDIO、PA7 CRS_DV、PB11 TX_EN、PC1 MDC、PC4/PC5 RXD0/1、PG13/PG14 TXD0/1 | PHY 为 LAN8720A |
| SWD | PA13 SWDIO、PA14 SWCLK、NRST | 同时连接 VREF/3V3 与 GND |

## 复用与跳帽审计

在写初始化代码前完成以下检查：

- RGB LED 与 DCMI：使用摄像头时断开相应 RGB LED 跳帽或保持冲突引脚安全。
- CAN 与 LTDC：PB8/PB9 被 LCD 蓝色数据占用，不能依赖软件初始化顺序解决电气复用。
- SDIO 与 Wi-Fi：查匹配 V1/V2 原理图及版本例程，确认模块禁用引脚和跳帽状态。
- USART2、RS232、RS485：确认物理路由跳帽和 V1/V2 不同的收发方向脚。
- I2C1：核对所有板载从设备地址、上拉和驱动方式，避免重复初始化或地址冲突。
- V2 NAND 与 SDRAM：两个器件共享 FMC 总线；未使用的器件片选/控制脚必须处于禁止状态。较新的 V2 SDRAM BSP 包含 `SDRAM_Enable_NAND_Disable()` 一类的仲裁逻辑。
- V1 J33：禁止短接；厂商资料明确警告可能损坏硬件。

## 电源与调试

- 可使用 USB 5 V 或 DC 6–12 V 供电。LCD、网络和外设负载较大时优先使用足额 DC 电源。
- 下载调试优先使用 SWD；至少连接 VREF/3V3、GND、SWDIO、SWCLK、NRST。
- 调试异常时先确认供电、电源选择、BOOT、跳帽和复用冲突，再检查软件。

## 时钟陷阱

- 实物晶振为 25 MHz。资料中部分近期工程的注释仍写 12 MHz、216 MHz、54 MHz 或 108 MHz，但代码实际可能是 `PLLM=25, PLLN=360, PLLP=2`，即 SYSCLK 180 MHz、APB1 45 MHz、APB2 90 MHz。
- 上述普通配置若 `PLLQ=4`，PLL48 域为 90 MHz，不能用于 USB。
- USB Host 示例使用 `PLLM=25, PLLN=336, PLLP=2, PLLQ=7`，得到 SYSCLK 168 MHz 和精确 48 MHz USB 时钟。
- 用配置值计算并用 `HAL_RCC_Get*Freq()`、寄存器或 MCO/示波器验证；不以注释为证据。
- APB 分频不为 1 时，对应定时器内核通常是 APB 时钟的 2 倍。

## 内存约束

- 片内 Flash：`0x08000000`，1 MB。
- SRAM1+SRAM2：`0x20000000` 起，共 192 KB；MDK 常配置 `IRAM1 size=0x30000`。
- CCM：`0x10000000` 起，64 KB；MDK 常配置 `IRAM2 size=0x10000`。
- DMA 不能访问 CCM。DMA 缓冲区必须放在 `0x20000000` 区域或相应外部 DMA 可访问内存。
- SDRAM V1/V2 的容量和行列地址不同，初始化参数与链接/堆区边界必须一起核对。

## 证据来源

本页结论来自资料包中的 V1/V2 核心板和底板原理图、两版硬件规格书、两版 IO 引脚分配表，以及匹配版本的 HAL/标准库 BSP。若手中板卡的丝印或器件型号不同，以实物和对应原理图为准。
