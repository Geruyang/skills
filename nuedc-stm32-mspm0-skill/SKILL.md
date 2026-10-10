---
name: nuedc-stm32-mspm0-skill
description: 'Develop, configure, regenerate, build, debug, and validate NUEDC-style MCU firmware across two vendor workflows: STM32CubeMX .ioc to Keil MDK-ARM projects, and TI MSPM0 SysConfig .syscfg to Code Composer Studio projects. Use for STM32 HAL/LL, CubeMX pin/clock/DMA/NVIC setup, Keil .uvprojx generation and builds, MSPM0 DriverLib, TI SysConfig and CCS builds, board bring-up, peripheral integration, serial protocols, control loops, or competition acceptance testing. Route each project to its native configuration source and never mix generated-code ownership between STM32 and TI.'
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# NUEDC-STM32-MSPM0-SKILL

Route each project through its native vendor workflow, preserve generated-code boundaries, and validate claims at the highest level actually observed.

## Start With Project Discovery

1. Run `python scripts/inspect_project.py <project-dir>`.
2. Locate configuration sources, editable application files, IDE project files, linker files, generated headers, build outputs, and debug configuration.
3. Classify the target before editing:
   - STM32: prefer an `.ioc` plus an MDK-ARM `.uvprojx`.
   - MSPM0: prefer a `.syscfg` plus CCS metadata such as `.project`, `.cproject`, `.ccsproject`, `.projectspec`, or `targetConfigs/*.ccxml`.
   - Mixed repository: identify separate board/project roots and handle each independently.
4. Identify whether the project is a single-file demo or a layered project with `app/`, `bsp/`, `components/`, `drivers/`, `middleware/`, `tasks/`, or RTOS code.
5. Record the MCU, package, board, SDK/firmware pack, compiler, IDE version, target configuration, and debug probe from local evidence. Do not infer missing values from a nearby example.

## Apply The Correct Configuration Route

### Route STM32CubeMX To Keil

- Treat the `.ioc` file as the source of truth for MCU/package selection, pinmux, clock tree, peripheral modes, DMA, NVIC, and generated initialization.
- Set the CubeMX project toolchain to the locally supported MDK-ARM target, then use full project generation. `generate code` alone does not guarantee a Keil project.
- Keep custom logic inside `USER CODE BEGIN/END` regions when editing generated files. Prefer separate user-owned `.c/.h` modules for substantial logic.
- Do not hand-edit CubeMX-owned initialization merely to make the current build pass. Change `.ioc`, regenerate, inspect the diff, and then adapt application code to the generated names.
- Treat `Drivers/`, startup assembly, generated `Core/Src` initialization, `.uvprojx`, scatter files, `Objects/`, `Listings/`, maps, and `.axf/.hex` outputs according to `references/stm32-cubemx-keil.md`.
- Read `references/stm32-cubemx-keil.md` before regenerating, changing clocks or memory layout, or invoking CubeMX/Keil from the command line.

### Route MSPM0 SysConfig To CCS

- Treat `.syscfg` as the source of truth for device/package metadata, clocks, pinmux, peripheral instances, DMA, events, and interrupts.
- Preserve `@cliArgs`, `@v2CliArgs`, `@versions`, `--device`, `--package`, and `--product` metadata exactly in valid comment syntax.
- Prefer SysConfig plus DriverLib. Do not hand-edit `ti_msp_dl_config.c/.h`, generated linker command files, generated makefiles, `Debug/`, `Release/`, objects, maps, or `.out` files.
- Inspect the local generated header before using instance, pin, IRQ, channel, or init-function names. Do not guess whether the function is `SYSCFG_DL_init()` or another spelling.
- Validate unfamiliar fields against the current project, the installed MSPM0 SDK examples, SDK `.meta/*.syscfg.js`, or SysConfig itself. Never invent fields or enum values.
- Read `references/mspm0-sysconfig-ccs.md` before editing `.syscfg`, changing CCS project metadata, regenerating, or using CCS command-line builds.

## Preserve Cross-Platform Boundaries

- Never copy STM32 HAL initialization into an MSPM0 project or translate TI generated files into an STM32 CubeMX-owned file.
- Never make one shared generated configuration file the source of truth for two MCUs. Share only portable application logic, protocol definitions, algorithms, and hardware-abstraction interfaces.
- Keep board-specific pin, clock, interrupt, DMA, linker, startup, and probe configuration in the target-specific project.
- If both platforms implement the same competition protocol, define one portable message format and write thin HAL/DriverLib adapters on each target.
- Do not rename generated handles or instances for cosmetic consistency. Adapt at a user-owned wrapper boundary.

## Make Competition Firmware Changes Safely

1. Restate the measurable requirement: input, output, timing, accuracy, fault behavior, and acceptance method.
2. Confirm schematic, pin map, voltage levels, external module model, protocol, sampling/control rate, and resource conflicts.
3. Map ownership of each peripheral, buffer, ISR, DMA channel, timer, and task.
4. Make the smallest configuration and application-code change.
5. Regenerate using the native tool, then review the diff before accepting it.
6. Compile and link through the existing IDE/toolchain configuration.
7. Detect the connected probe before flash/debug with `python scripts/detect_probe.py`.
8. Validate in layers and report the highest completed layer.

Read `references/nuedc-runtime-validation.md` for interrupts, DMA, RTOS, control loops, serial protocols, external modules, board-specific cautions, and acceptance evidence.

## Handle Missing Parameters

Ask before editing when a missing choice materially changes hardware behavior or generated configuration. Important choices include:

- exact MCU, package, board revision, and clock source
- pin and peripheral instance
- UART baud/data/parity/stop bits and framing
- timer period and clock source
- PWM frequency, duty, polarity, dead time, and safe state
- ADC channel, reference, sample time, trigger, rate, and scaling
- DMA direction, width, circular/normal mode, buffer ownership, and completion event
- interrupt priority and RTOS-safe API constraints
- external-module supply, I/O voltage, address/mode pins, and required pull-ups

Use a low-risk local default only when it is reversible and does not risk hardware. State the applied default. Never silently choose a power pin, motor polarity, flash recovery, clock source, or probe backend.

## Keep Runtime Code Predictable

- Initialize generated hardware before first use.
- Keep ISRs short: clear/acknowledge the source, capture minimal state, and defer parsing or control work.
- Mark shared ISR state appropriately and protect multi-byte/shared-buffer access.
- Use DMA ownership rules that prevent the CPU, ISR, and peripheral from mutating the same buffer concurrently.
- Avoid blocking UART, I2C, SPI, delays, logging, or floating-point-heavy work inside ISRs.
- Preserve existing RTOS task, queue, notification, semaphore, and priority boundaries.
- Use hardware timers or trigger chains for real timing. Use busy-loop delays only for bounded smoke tests.
- Add timeouts and safe-state behavior for sensors, communications, and actuators.

## Build, Flash, And Debug

- Build through the active generated project instead of recreating compiler/linker flags manually.
- For Keil, use the existing `.uvprojx`, selected target, device pack, compiler, and scatter file.
- For CCS, distinguish modern `ccs-server-cli` from legacy Eclipse-based commands by inspecting the installed version and its help output.
- Treat build success, flash success, and physical behavior as separate results.
- Detect probes before choosing ST-Link, J-Link, CMSIS-DAP/DAPLink, or XDS110. If multiple probes are present, the probe conflicts with project configuration, or detection is uncertain, stop before flashing.
- Never perform mass erase, unlock, factory reset, option-byte changes, or protection changes without explicit user authorization.

Read `references/flash-debug.md` before flashing, setting breakpoints, inspecting live control firmware, or diagnosing repeated connection failures.

## Validate In Layers

Report these levels separately:

1. Source/static inspection
2. CubeMX or SysConfig generation
3. Compile and link
4. Flash tool verification
5. Target boot and basic I/O
6. Serial/logical protocol observation
7. Oscilloscope, logic-analyzer, load, or closed-loop measurement
8. Competition acceptance criteria

Do not claim a physical result from source inspection or a successful build. Report all generator and compiler warnings separately from success.

## Bundled Tools

- `python scripts/inspect_project.py <project-dir>`: identify STM32/MSPM0 project shape, configuration sources, IDE files, generated surfaces, metadata, generated init names, and regeneration risks. Add `--json` for structured output.
- `python scripts/detect_probe.py`: read-only detection of common ST-Link, J-Link, XDS110, CMSIS-DAP, and DAPLink devices. Add `--json` for structured output.

The scripts inspect only. They do not regenerate, build, flash, reset, unlock, or erase hardware.
