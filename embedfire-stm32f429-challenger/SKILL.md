---
name: embedfire-stm32f429-challenger
description: Develop, port, build, flash, and debug firmware for the EmbedFire/野火 STM32F429IGT6 挑战者 V1/V2 development boards using the local 野火 material set. Use for 野火 STM32F429 挑战者 board identification, HAL/Standard Library/Keil/CubeMX projects, GPIO, clocks, UART/RS485/CAN, SPI Flash, SDRAM/NAND, LCD/touch/camera, SDIO, USB, Ethernet, RTOS, middleware, pin conflicts, jumpers, factory-demo recovery, and board-specific troubleshooting. Do not use for 正点原子/ALIENTEK boards or unrelated STM32F429 hardware.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# 野火 STM32F429 挑战者开发

Use the local source of truth at `E:\野火【STM32F429开发板-挑战者】资料`. Treat the board revision as a required input whenever external memory, SDIO/Wi-Fi, RS485, LCD, sensors, or factory resources are involved.

## Establish the exact target

1. Identify the physical board as 挑战者 V1 or V2 from silkscreen, PCB layout, fitted devices, or a clear photo. Do not infer the revision only from a project folder name.
2. Confirm the MCU is `STM32F429IGT6` and record the intended toolchain, library family, and debugger.
3. If the revision is unknown, inspect read-only/common code first. Ask for the revision before choosing version-specific pins, memory geometry, or binaries.
4. Read [references/board-variants-and-pins.md](references/board-variants-and-pins.md) for hardware differences, verified common pins, jumpers, and conflicts.

Apply this evidence order when sources disagree:

1. The actual PCB, silkscreen, and fitted component marking.
2. The matching V1/V2 schematic and a matching version-specific example.
3. The matching IO table and hardware specification.
4. Generic book prose, copied comments, and filenames.

## Select a trustworthy baseline

- Prefer the 2026 HAL application archive for new practical work when it already contains the required peripheral.
- Use the HAL or Standard Library book examples when their explicit V1/V2 branch is a better match, especially for external Flash, SDRAM, NAND, LTDC, SDIO, RS485, and USB.
- Use dedicated FreeRTOS, uC/OS, RT-Thread, LiteOS, LwIP, emWin, emXGUI, and motor-control archives instead of reconstructing their ports from unrelated examples.
- Preserve the selected project's startup file, linker memory regions, CMSIS/HAL or Standard Library version, compiler family, and directory layout unless migration is part of the request.
- Fully extract an example to a short local path before building. Keil exclamation marks commonly indicate incomplete extraction or broken relative paths.
- Read [references/materials-catalog.md](references/materials-catalog.md) to route requests to the right archive, document, or book chapter.

Use `scripts/materials.ps1` to inventory or search the material tree without unpacking every multi-gigabyte archive:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/materials.ps1 -Action find -Pattern 'RS485|485'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/materials.ps1 -Action list -Archive '1-程序源码_教程文档\0-[野火] 开发板实验应用源码\实验应用-F429IG_20260604.zip' -Pattern '\.uvprojx$'
```

## Make the smallest board-aware change

1. Start from the closest verified example and retain its board support files.
2. Trace each peripheral from clock enable through GPIO alternate function, DMA/IRQ setup, peripheral initialization, application call site, and error path.
3. Check every selected pin against the conflict table before enabling a second peripheral.
4. Keep the BSP boundary clear: application logic should call board-level drivers rather than duplicating register and pin configuration.
5. Change one subsystem at a time and keep unrelated generated or vendor code untouched.
6. Follow [references/development-workflow.md](references/development-workflow.md) for build, flash, observation, and fault isolation.

## Enforce clock and memory invariants

- The board HSE is 25 MHz and LSE is 32.768 kHz. Recompute SYSCLK, AHB, APB1, APB2, timer kernels, and PLL48 from actual PLL register/configuration values; do not trust copied clock comments.
- Ordinary recent examples often run at 180 MHz, while USB examples may deliberately run at 168 MHz so `PLLQ` produces exactly 48 MHz. Reject a USB clock that merely compiles.
- APB timer kernels run at twice the APB clock when the APB prescaler is greater than one.
- Internal Flash is 1 MB. SRAM1+SRAM2 at `0x20000000` totals 192 KB; CCM at `0x10000000` is 64 KB.
- DMA cannot access CCM RAM. Place DMA descriptors, frame fragments, UART buffers, and SDIO/Ethernet buffers in DMA-visible SRAM.
- External SDRAM uses FMC Bank2 at `0xD0000000`, but V1 is 8 MB with 12 row/8 column bits and V2 is 32 MB with 13 row/9 column bits. Never reuse the V2 geometry on V1.
- V1 uses W25Q128 (16 MB); V2 uses W25Q256 (32 MB). Enable 4-byte addressing before accessing W25Q256 locations above 16 MB.
- V2 NAND and SDRAM share FMC signals. Keep the unused device deselected and use the matching V2 BSP arbitration sequence.

## Protect recoverability

- The factory demo depends on resource data stored in external SPI NOR. If that Flash was erased or overwritten, program the supplied external-Flash resource writer before restoring the MCU demo.
- Do not flash a V1 binary to V2 or a V2 binary to V1 when the project touches version-specific hardware.
- Prefer SWD and connect VREF/3V3, GND, SWDIO, SWCLK, and NRST. Preserve the board boot configuration unless the task explicitly changes it.
- Never short V1 jumper J33; the vendor documentation warns it can damage hardware.

## Finish with evidence

Report:

- board revision and hardware assumptions;
- exact baseline project/archive and library/toolchain versions;
- modified files and peripheral/pin choices;
- computed clock tree and relevant memory placement;
- build result and output artifact;
- flash, serial, display, network, or other on-target evidence actually observed;
- checks that remain unperformed and why.

Use `$keil` for MDK project discovery/builds, `$jlink` for probe/flash/debug work, and `$serial` for UART observation when those actions are requested and the corresponding tools are available.

## 相机、USB 与调试采样经验

挑战者相机/USB 组合、fireDAP 身份或无停机 trace 排查时，读取 [实板联调经验](references/camera-usb-debug-evidence.md)。
