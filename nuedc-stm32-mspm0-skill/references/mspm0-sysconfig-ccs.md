# MSPM0 SysConfig To CCS Workflow

Use this reference for `.syscfg` edits, DriverLib integration, CCS/CCS Theia project generation, command-line builds, and generated-name validation.

## Source Of Truth

Keep hardware configuration in `.syscfg` whenever SysConfig owns it. Preserve these metadata elements and their existing comment syntax:

```text
@cliArgs
@v2CliArgs
@versions
--device
--package
--product
```

Do not hand-edit generated files in `Debug/`, `Release/`, a SysConfig output folder, or project-root `ti_msp_dl_config.c/.h` layouts. Inspect them to discover exact generated names and initialization behavior.

Normal editable surfaces are:

- the active `.syscfg`
- user-owned `.c/.h` files
- project metadata only when compiler, linker, product discovery, or debug configuration must deliberately change

## Edit Strategy

1. Inspect the existing `.syscfg` for the exact device, package, SDK product, SysConfig version, module names, instance names, pins, clocks, events, DMA, and interrupts.
2. Inspect `ti_msp_dl_config.h` for generated instance, pin, IRQ, channel, and init-function names.
3. Find a matching example in the installed MSPM0 SDK or inspect `source/ti/driverlib/.meta/*.syscfg.js` before adding an unfamiliar field or enum.
4. Preserve `$suggestSolution` and `$assign` solver statements unless the change is understood and validated.
5. Modify the smallest `.syscfg` and user-code surface.
6. Regenerate and review warnings before compiling.

Do not copy a whole `.syscfg` from a different MSPM0 device or package. Pin options and module fields can differ even inside one family.

## SysConfig CLI

Prefer the exact SysConfig command already emitted by the project build or documented for the installed SDK. A common MSPM0 shape is:

```powershell
<sysconfig-root>\sysconfig_cli.bat -o <output-dir> -s "<mspm0-sdk>\.metadata\product.json" --compiler ticlang <project>.syscfg
```

Compiler values and output placement depend on the project. Inspect CCS build rules, project properties, and `sysconfig_cli --help` instead of hard-coding a value from another IDE.

Treat any SysConfig Problems view or CLI warning as a validation finding even if C files were generated.

## DriverLib Runtime Rules

- Call the generated init function before using a configured peripheral.
- Use macros from the local generated header for instances, ports, pins, IRQs, channels, and clock-derived values.
- Prefer DriverLib for runtime control and keep pinmux, clocks, peripheral setup, DMA, events, and interrupts in SysConfig.
- Avoid direct register configuration unless DriverLib cannot express the required behavior and document why.
- Clear pending interrupt sources and keep handlers short.
- Start timers, ADC conversions, DMA, or communication peripherals only after their generated initialization and application state are ready.

## CCS Project And Build

Recognize both modern CCS and legacy Eclipse-based layouts. Common project evidence includes:

```text
.project
.cproject
.ccsproject
*.projectspec
targetConfigs/*.ccxml
Debug/
Release/
```

Do not casually edit `.project`, `.cproject`, `.ccsproject`, `.settings/`, or `.ccxml`. These can change products, compiler options, linker inputs, and the physical probe.

For current CCS versions, inspect `ccs-server-cli ... -ccs.help` and use the installed command's documented application and options. A current build shape is:

```powershell
ccs-server-cli -noSplash -workspace <workspace> -application com.ti.ccs.apps.buildProject -ccs.projects <name> -ccs.configuration Debug
```

Older CCS versions use Eclipse application names and launchers. Detect the installed version and help output; do not mix commands between generations.

If generated makefiles already exist and are portable, building them can be useful for validation. Do not treat generated makefiles as the configuration source or patch them to hide an IDE/product-discovery problem.

## Generated Names And Interrupts

Do not guess names such as:

```c
SYSCFG_DL_init();
TIMER_0_INST;
TIMER_0_INST_INT_IRQN;
GPIO_LEDS_PORT;
GPIO_LEDS_USER_LED_1_PIN;
```

Read the local header. For a timer ISR, verify the generated IRQ, pending-interrupt API result, period/load value, and actual CPU/timer clock after every clock change.

## Board Caution: LCKFB Tianmengxing MSPM0G3507

Apply this only when the user explicitly identifies that board:

- Avoid PA21, PA23, PA02, and PA18 for ordinary new assignments unless the schematic/project deliberately uses them.
- Treat PA10 and PA11 as special; they are commonly used for the board's default UART. Prefer them for that UART when appropriate, but warn before repurposing them for GPIO, PWM, SPI, I2C, or another peripheral.
- Do not move existing assignments silently. Explain the board conflict and preserve intent.

## Common Failure Modes

- Editing generated `ti_msp_dl_config.*` rather than `.syscfg`.
- Damaging metadata comment syntax and causing a JavaScript parse error.
- Guessing a generated init-function spelling or instance macro.
- Copying a solver field or enum from another SDK/device version.
- Building with a CCS project whose discovered product/compiler differs from the `.syscfg` metadata.
- Selecting an `.ccxml` for XDS110 while another probe is physically connected.
- Treating a SysConfig warning as a clean generation.
- Changing CPU clock without recalculating timer loads, baud rates, or delay loops.

## Official References

- MSPM0 SysConfig guide: https://software-dl.ti.com/msp430/esd/MSPM0-SDK/latest/docs/english/tools/sysconfig_guide/doc_guide/doc_guide-srcs/sysconfig_guide.html
- CCS SysConfig guide: https://software-dl.ti.com/ccs/esd/documents/ccs_sysconfig.html
- CCS command-line project build guide: https://software-dl.ti.com/ccs/esd/documents/ccs_project-command-line.html

