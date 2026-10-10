# Flash And Debug Safety

Use this reference before connecting, flashing, setting breakpoints, or attempting recovery.

## Detect First

Run:

```powershell
python scripts\detect_probe.py
```

Probe detection is read-only and does not prove target connectivity. Reconcile detected hardware with the project:

| Probe | Common project route |
|---|---|
| ST-Link | STM32 Keil debug configuration or STM32CubeProgrammer |
| J-Link | Keil/J-Link for STM32, or a matching CCS/DSLite setup for supported TI targets |
| XDS110 | CCS/DSLite for MSPM0 |
| CMSIS-DAP/DAPLink | Keil/OpenOCD or another explicitly configured compatible backend |

Do not select a backend from probe type alone. Confirm MCU support, project configuration, voltage reference, interface, and reset method.

Stop before flash when:

- no supported probe is detected
- more than one probe is connected and the target is ambiguous
- the project selects another probe
- target voltage or wiring is uncertain
- the requested action would alter option bytes, protection, security, boot configuration, or calibration data

## STM32 With Keil

- Treat the `.uvprojx` target and Keil debug settings as the source for device, algorithm, and probe selection.
- Avoid rewriting `.uvoptx` merely to automate a flash; user-specific settings can be volatile.
- A typical µVision flash command shape is `UV4.exe -f <project>.uvprojx -t"<target>"`. Verify installed-command help and capture a log.
- Confirm the configured flash algorithm matches the exact STM32 device and memory region.
- After clock or low-power changes, distinguish a debug-connect problem from a firmware boot problem. Use an explicitly chosen connect-under-reset mode only when authorized and supported.
- Do not alter readout protection, write protection, option bytes, or secure areas during routine debugging.

## MSPM0 With CCS

- Treat `targetConfigs/*.ccxml` as the CCS debug path. Confirm it names a backend compatible with the physical probe.
- Build success does not validate `.ccxml` or probe connectivity.
- Use CCS/DSLite commands produced by the installed tools and project. A common explicit flow lists/opens the configured target, programs a fresh `.out`, verifies, and resets.
- Prefer a system reset after programming when clock-tree changes could leave the debugger and target in different states.
- Do not assume every OpenOCD distribution supports MSPM0. Report adapter/target recognition failures separately from firmware failures.

## Live Debug Caution

Breakpoints and register inspection can halt real-time control. Before halting:

- disable or place actuators in a safe state
- consider watchdog behavior
- consider PWM outputs, DMA, communication timeouts, and power-stage state while the CPU is stopped
- warn the user when a halt could damage hardware or invalidate timing measurements

Use watchpoints and logging sparingly. Observing a variable can perturb timing or bus load on constrained systems.

## Recovery Boundary

Never automatically mass erase, unlock, factory reset, change protection, or rewrite boot/option configuration. If ordinary connection fails:

1. close stale debug sessions
2. reconnect USB and target power safely
3. redetect the probe
4. verify target device, wiring, voltage reference, interface, reset, and project config
5. try a non-destructive connection mode supported by the chosen tool
6. stop and request explicit authorization before destructive recovery

## Report Separately

Report:

- probe detected
- target connected
- flash programmed
- verification passed
- reset/run issued
- firmware behavior observed

Do not collapse these into one “flash successful” statement when only part of the chain is known.

