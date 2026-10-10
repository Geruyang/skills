---
name: alientek-apollo-stm32f429
description: 'Develop, port, build, flash, and debug firmware for the ALIENTEK/正点原子 Apollo STM32F429IGT6 board using the local Apollo material disk, including HAL/Keil projects, board peripherals, RTOS, USB, Ethernet, displays, and storage. Use for 阿波罗 STM32F429, 正点原子 F429, ALIENTEK Apollo, or the E: Apollo disk; also use when this exact board is mistakenly called 野火. Never apply this board map to a Wildfire/野火 board.'
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# 正点原子阿波罗 STM32F429 开发

## 定位板卡与资料

- 将本技能限定为 **正点原子/ALIENTEK 阿波罗 STM32F429**：核心板 MCU 为 STM32F429IGT6，搭配 Apollo STM32F4/F7 MotherBoard。用户口误称“野火”时先纠正品牌，不要套用野火板卡引脚。
- 把 `E:\阿波罗STM32F429 资料盘(A盘)` 当作只读资料库。不要原地修改、解压或编译；把选中的工程复制到用户工作区后再改。
- 先读 [references/board-map.md](references/board-map.md) 判断硬件资源、跳帽和冲突，再用 [references/materials-and-examples.md](references/materials-and-examples.md) 选择最接近的例程或手册章节。
- 移植旧工程、换编译器、接入 RTOS/USB/网络或使用 DMA/外部存储器时，再读 [references/legacy-modernization.md](references/legacy-modernization.md)。

## 证据优先级

按以下顺序解决矛盾，并明确标记“已核实”与“推断”：

1. 用户正在构建的目标工程及其实际源码、编译日志、硬件现象
2. 与板卡版本匹配的原理图和 IO 引脚分配表
3. 资料盘中最接近目标的可编译例程源码
4. 开发指南、例程 README 和视频说明
5. 芯片通用知识或经验推断

README 存在复制错误，不能单独作为引脚、时钟或实验行为的最终依据。

## 开发工作流

1. 确认目标板卡、核心板/底板版本、已连接模块、供电方式、跳帽位置和调试接口。只有这些信息会改变实现时才询问用户。
2. 明确采用“复现原例程”还是“现代化工程”。复现模式尽量保留原 HAL、Pack、ARMCC5 和目录结构；现代化模式允许升级，但逐项处理兼容性，不做无说明的整库替换。
3. 从资料盘选择一个最接近的工程，复制到工作区。保留原工程作对照，优先做小步、可回退的修改。
4. 在写代码前列出时钟、引脚复用、DMA、NVIC、存储区、缓存、RTOS tick 和外设依赖。检查共享引脚与跳帽冲突。
5. 采用原工程的层次：`CORE`、`HALLIB`、`SYSTEM`、`HARDWARE`、`USER`、`OBJ`。新增板级定义时集中管理，避免在业务代码中散落端口和地址常量。
6. 构建后检查警告、链接脚本/分散加载文件、RAM/Flash 占用、生成的 AXF/HEX/BIN 和 map 文件。涉及外部 SDRAM/NAND/SPI NOR、DMA 或缓存时做边界与一致性验证。
7. 只有用户授权并且工具/硬件可用时才下载和实机调试。下载后至少核对启动、串口日志、关键外设和异常处理；不能实测时明确说明验证边界。

## 不可直接照搬的约束

- HSE 是 25 MHz。STM32F429 生产配置不得超过 180 MHz；USB、SDIO、RNG 等 48 MHz 域必须重新计算并校验。不要沿用旧 USB 例程的 192 MHz 主频。
- 内部 SRAM 主区是 `0x20000000` 起的 192 KiB，CCM 是 `0x10000000` 起的 64 KiB。DMA 不能访问 CCM；DMA 缓冲区放在可达 SRAM/外部存储器，并检查对齐与缓存一致性。
- SDRAM、NAND、TFT、LTDC、SDIO、DCMI、Ethernet 等共享大量 FMC/GPIO 资源。先初始化底层时钟、GPIO、FMC/SDRAM 和扩展 IO，再访问高层设备。
- 旧 `delay.c` 可能接管 SysTick，旧 `sys.c`/串口重定向依赖 ARMCC5。接入 HAL tick、FreeRTOS 或 ARMClang/GCC 前必须消除所有权冲突。
- 原 LCD 驱动部分路径依赖 USART1 初始化才能输出检测信息；复现旧例程时遵守初始化顺序，现代化时解除这种隐式依赖。
- 保持旧源码的原始编码和换行，除非已经有受控的编码迁移计划，避免中文注释和 Keil 工程文件损坏。
