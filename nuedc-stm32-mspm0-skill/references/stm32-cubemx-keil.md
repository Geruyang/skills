# STM32CubeMX To Keil Workflow

Use this reference for `.ioc` edits, CubeMX regeneration, MDK-ARM project generation, Keil builds, clocks, startup, and memory layout.

## Project Surfaces

Treat these as normal editable sources:

- the active `.ioc`
- user-owned application modules and headers
- code inside matched `USER CODE BEGIN/END` regions
- explicit project configuration only when the requested change requires it

Treat these as generator-, pack-, or build-owned unless the task specifically requires a deliberate change:

- `Core/Src/main.c`, `gpio.c`, `dma.c`, peripheral init files, `stm32*_hal_msp.c`, and `stm32*_it.c` outside user regions
- `Core/Inc` generated headers outside user regions
- `Drivers/CMSIS/` and `Drivers/STM32*xx_HAL_Driver/`
- startup assembly, system files, and generated linker/scatter files
- `.uvoptx`, `Objects/`, `Listings/`, `.o`, `.d`, `.map`, `.axf`, and generated `.hex/.bin`

Do not assume every STM32 project uses the default `Core/` layout. Follow the local `.ioc` and project structure.

## Inspect Before Editing

1. Read the `.ioc` as key/value configuration and record MCU, package, firmware pack, toolchain, clock sources, enabled IP, pins, DMA, and NVIC settings.
2. Locate the `.uvprojx`, active target, scatter file, compiler selection, device pack, include paths, and preprocessor symbols.
3. Inspect generated handle and init names in local headers and source. Do not copy `huart1`, `htim3`, or `MX_*_Init()` from an unrelated example.
4. Find every user-code region in a generated file before modifying it. Ensure markers are balanced.
5. Confirm whether substantial application logic already lives in a separate `App/`, `BSP/`, `Drivers/`, `Tasks/`, or similar user-owned layer.

## Edit And Regenerate

Prefer the CubeMX GUI for hardware configuration when available. For repeatable command-line generation, create a short script using local paths and values, for example:

```text
config load "C:\project\controller.ioc"
project toolchain MDK-Arm
project name controller
project path "C:\project"
project generate
exit
```

The exact accepted toolchain spelling can vary with CubeMX generation/version and existing `.ioc` metadata. Inspect the installed tool's help and the current project instead of force-rewriting a known-good value.

On Windows, current official documentation describes quiet script execution from the STM32CubeMX install directory in this form:

```powershell
jre\bin\java -jar STM32CubeMX.exe -q <script-file>
```

Use `project generate` for a full toolchain project. `generate code <path>` generates CubeMX-owned code but is not a substitute for creating all toolchain project files.

Before regeneration:

- require a clean or understood diff when Git is available
- preserve the exact firmware-pack version unless the user requests an upgrade
- enable CubeMX user-code preservation and still verify the resulting diff
- avoid simultaneous manual edits and generation

After regeneration:

- inspect changed `.ioc`, `.uvprojx`, source, startup, and scatter files
- verify custom code survived only inside user regions or separate modules
- check for renamed handles, IRQ handlers, DMA handles, and clock-derived timer values
- report generator warnings independently

## Clock, Timer, ADC, PWM, And DMA Checks

- Derive timer rates from the actual timer kernel clock, prescaler, counter mode, and auto-reload value. Account for the STM32 timer-clock multiplier rule where applicable to the selected family and bus prescaler.
- Verify PLL input range, voltage scaling, flash latency, peripheral clock selection, and external-crystal frequency from the board schematic and device documentation.
- Recalculate UART baud error, PWM frequency, ADC clock/sample time, and control-loop periods after clock changes.
- Confirm DMA request, stream/channel mapping, direction, width, increment mode, circular mode, interrupt, and buffer lifetime.
- Confirm NVIC enablement and priority relationships, especially with FreeRTOS API-call priority limits.
- Do not mix HAL and LL ownership of the same peripheral unless the project already has a deliberate pattern.

## Keil Build

Use the installed Keil executable and active project target. A typical command shape is:

```powershell
UV4.exe -b <project>.uvprojx -t"<target>" -o <build-log>
```

Use the target already defined by the project. Do not invent pack paths, compiler paths, CPU flags, scatter files, or preprocessor symbols outside the project to simulate a successful build.

Inspect the log for errors and warnings, then confirm the expected `.axf` and optional `.hex/.bin` were produced. Do not infer success from the presence of an old output file; compare timestamps or clean/rebuild when appropriate.

## Common Failure Modes

- Generated code overwrites logic placed outside user regions.
- The `.ioc` targets another IDE, so no usable `.uvprojx` is generated.
- The local Cube firmware pack or Keil device pack differs from the project version.
- Clock changes invalidate baud rate, PWM, ADC, or delay assumptions.
- The selected target links a different scatter file or source group than expected.
- An interrupt name or handler does not match the exact STM32 family/startup vector.
- DMA is configured but the peripheral handle is not linked in the generated MSP initialization.
- A successful compile uses stale generated files because CubeMX was not rerun.

## Official References

- STM32CubeMX user manual and command-line workflow: https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
- Keil µVision command-line reference: https://www.keil.com/support/man/docs/uv4/uv4_commandline.asp

