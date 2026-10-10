# 本地资料导航

资料根目录：`E:\野火【STM32F429开发板-挑战者】资料`

本索引基于 2026-09-15 的只读盘点：329 个文件，约 7.65 GB，包括 124 份 PDF、121 份 PPTX、38 个 ZIP，以及原理图、表格、芯片资料和开发工具。资料会更新；使用时先通过 `scripts/materials.ps1 -Action inventory` 或 `find` 核实当前文件名。

## 先读和优先级

1. 根目录的 `[野火]STM32F429_挑战者开发板资料使用必读说明.pdf`：资料用法、解压要求和出厂资源恢复说明。
2. `2-开发板硬件资料_原理图_尺寸图_封装库_规格书\ebf_stm32_tiaozhanzhe_hardware.zip`：V1/V2 原理图、尺寸、封装、规格书、IO 表和器件手册。
3. 与目标版本匹配的例程和 BSP。
4. STM32F429 数据手册、参考手册、Cortex-M4 手册和勘误表。
5. 教程正文和通用协议资料。

注释、目录名和教程正文可能落后于代码或实物；冲突时遵守 SKILL.md 中的证据优先级。

## 主要目录

| 目录 | 用途 |
|---|---|
| `0-开机例程源码` | V1/V2 出厂演示、外部 Flash 资源写入、说明文档 |
| `1-程序源码_教程文档` | HAL、标准库、RTOS、GUI、LwIP、电机教程与源码 |
| `2-开发板硬件资料_原理图_尺寸图_封装库_规格书` | 板卡级硬件权威资料 |
| `3-STM32官方资料_固件包_参考资料` | STM32Cube F4、ST 手册和协议资料 |
| `4-开发软件` | Keil、CubeMX、串口/烧录等配套软件 |
| `5-配套模块资料` | LCD、OLED、OV2640、OV5640、DAP 等模块资料 |

## 首选工程归档

### 近期 HAL 应用例程

归档：

`1-程序源码_教程文档\0-[野火] 开发板实验应用源码\实验应用-F429IG_20260604.zip`

盘点结果：约 14,706 个条目、41 个 Keil 工程、2 个 `.ioc`、6,044 个 C 文件和 6,167 个头文件。典型工程结构：

```text
Doc/readme.txt
Libraries/CMSIS/...
Libraries/STM32F4xx_HAL_Driver/...
Project/Fire_F429IG.uvprojx
User/main.c
User/stm32f4xx_it.c
User/<peripheral>/bsp_*.c|h
```

已核对的简单模板工程采用：

- Device：STM32F429IGTx；启动文件 `startup_stm32f429xx.s`。
- HAL Driver V1.8.5；CubeMX 工程引用 STM32Cube FW_F4 V1.28.3。
- MDK-ARM 5；示例工程记录 ARMCC 5.06 update 7 build 960、DFP 2.15.0。
- 常见宏：`USE_HAL_DRIVER, STM32F429xx, USE_STM32F429I_DISCO`。
- 输出目录通常为 `Project\Output`，生成 HEX。

例程覆盖 GPIO/CubeMX、EXTI/蜂鸣器、SysTick/DWT、USART/多串口/RS232/RS485、DMA+UART IDLE、ADC、定时器/PWM/输入捕获、EEPROM、W25Q、NOR FatFs、SDIO/FatFs、SDRAM、RGB LCD/文本/触摸、裸机协作框架和 USB Host。

注意：近期 SDRAM 驱动可硬编码为 V2 的 32 MB、13 行/9 列配置，不可直接用于 V1。近期 SPI Flash 驱动能够识别 W25Q64/128/256，并为 W25Q256 启用 4 字节地址，移植时保留该逻辑。

### 标准库教程与例程

- 教程：`1-程序源码_教程文档\1-[野火]《STM32库开发实战指南》(标准库源码)【优先学习】\[野火EmbedFire]《STM32库开发实战指南——基于野火挑战者开发板》—20231009_1.pdf`
- 例程：同目录下 `1-书籍配套例程-F429IG-V1V2\1-书籍配套例程-F429IG-V1V2_20240202.zip`
- 盘点：约 27,966 个条目、154 个 Keil 工程。

版本说明指出：未分 V1/V2 的例程通常可共用；外部 SPI Flash、SDRAM、LTDC、SDIO/Wi-Fi 禁用、RS485 和部分 USB 工程应优先选择显式 V1/V2 分支。

快速页码（PDF 页）：Keil 34、DAP 50、工程 165、GPIO 181/197、RCC 228、EXTI 259、USART 292、DMA 332、I2C 369、SPI 415、NOR FatFs 463、SDRAM 498、LTDC/DMA2D 548、触摸 673、ADC 724、定时器 763/775、SDIO 857、SD FatFs 926、I2S 1028、Ethernet 1111、CAN 1210、RS485 1260、低功耗 1278、RTC 1320、MPU6050 1348、OV2640 1412、OV5640 1451、MDK/链接 1538。

### HAL 教程与例程

- 教程：`1-程序源码_教程文档\2-[野火]《STM32 HAL库开发实战指南》(HAL库源码)\[野火EmbedFire]《STM32 HAL库开发实战指南——基于野火F4系列开发板》—20220913_1.pdf`
- 例程：同目录下 `1-书籍配套例程-F429IG-V1V2\1-书籍配套例程-F429IG-V1V2_20240311.zip`
- 盘点：约 26,726 个条目、96 个 Keil 工程、1 个 `.ioc`。

显式分支包括 V1/V2 W25Q128/W25Q256、SDRAM、LTDC；NAND 和 AP3216C 为 V2 专用。

快速页码（PDF 页）：CubeMX 154、工程 174、GPIO 189/212、RCC 239、EXTI 269、USART 302、DMA 345、I2C 382、SPI 421、NOR FatFs 478、SDRAM 514、显示 550、触摸 687、ADC 746、定时器 789/801、SDIO 888、SD FatFs 961、I2S 977、Ethernet 1063、CAN 1144、RS485 1194、低功耗 1210、RTC 1252、MPU6050 1280、OV2640 1345、OV5640 1386、MDK/链接 1436。

## 专项中间件和系统

在 `1-程序源码_教程文档` 下按主题选用：

- `3-[野火]《FreeRTOS内核实现与应用开发实战指南》`：FreeRTOS 内核、教程和源码。
- `4-[野火]《uCOS-III内核实现与应用开发实战指南》`：`ebf_stm32f429_tiaozhanzhe_ucos_code.zip`。
- `5-[野火]《RT-Thread内核实现与应用开发实战指南》`：`ebf_stm32f429_tiaozhanzhe_rtthread_code.zip`。
- `6-[野火]《物联网操作系统 LiteOS开发实战指南》`：`ebf_stm32f429_tiaozhanzhe_liteos_code.zip`。
- `7-[野火]《emWin实战指南》`：`ebf_stm32f429_tiaozhanzhe_emwin_code_20240223.zip`。
- `8-[野火]《LwIP应用开发实战指南》`：`ebf_stm32f429_tiaozhanzhe_lwip_code.zip`，含 LAN8720A、MQTT 和抓包参考。
- `9-[野火]《电机应用开发实战指南—基于STM32》`：挑战者电机例程。
- `10-[野火]《emXGUI实战指南》系列`：MCU/PC 入门和 V1 综合例程。

这些包的版本可能较旧。优先保留其已验证端口层，再按需求更新内核或协议栈；不要把升级与业务功能改动混成一次不可验证的迁移。

## ST 官方资料

`3-STM32官方资料_固件包_参考资料` 中的重要材料：

- `HAL固件包\stm32cube_fw_f4_v1280.zip`
- `HAL固件包\stm32cube_fw_f4_v1283.zip`
- `STM32手册\2-STM32F429_427英文数据手册.pdf`
- `STM32手册\2-STM32F429_427中文数据手册（跟407稍有不同）.PDF`
- `STM32手册\1-STM32F4xx英文参考手册.pdf`
- 两册中文参考手册，其中第二册覆盖 DMA2D、LTDC、SAI、FMC。
- `PM0214_STM32F4xx-Cortex_M4内核参考手册.pdf`
- F427/F437/F429/F439 勘误表和系统存储器启动说明。

外设行为、寄存器、最大频率、DMA 可达性和勘误应以 ST 官方资料为最终依据。

## 配套模块

`5-配套模块资料` 下有：

- RGB 电容触摸屏 7/5/4.3 寸：`ebf_lcd_rgb_7_5_4.3_20260627.zip`
- I2C 0.96 寸 OLED：`野火OLED屏_I2C_0.96寸_20240517.zip`
- OV2640：`ebf_camera_ov2640_20240517.zip`
- OV5640：`ebf_camera_ov5640_20240517.zip`
- 普通/高速 DAP 下载器说明。

模块包只说明模块本身；接到挑战者板时仍需用板卡 IO 表检查复用、电平和连接器定义。

## 出厂演示恢复

`0-开机例程源码\开机测试例程_20231031.zip` 同时包含 V1/V2 出厂工程、说明和外部 SPI Flash 资源写入工程。出厂 GUI/图片/字库不全在 MCU 内部 Flash：

1. 先确认板卡版本。
2. 如果外部 NOR 被改写，先运行匹配版本的资源写入工程。
3. 再烧录匹配版本的 MCU 出厂演示。
4. 验证 LCD、触摸、音频、存储等实际功能；仅烧录成功不代表资源恢复完成。
