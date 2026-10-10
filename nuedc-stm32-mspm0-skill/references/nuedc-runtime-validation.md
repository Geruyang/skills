# NUEDC Runtime And Validation Rules

Use this reference when implementing competition logic, integrating modules, using interrupts/DMA/RTOS, or defining acceptance tests.

## Convert The Task Into Measurable Requirements

Record:

- operating modes and mode-switch conditions
- input range, output range, accuracy, resolution, update rate, and latency
- startup, timeout, communication-loss, sensor-fault, and emergency-stop behavior
- test points, instruments, data format, trial count, and pass/fail thresholds
- competition constraints such as supply, size, load, time, prohibited equipment, and reset procedure

Do not optimize code against an ambiguous phrase such as “fast,” “stable,” or “accurate.” Translate it into a measurable target or ask for one.

## Separate Portable And Target-Specific Code

Keep portable components independent of HAL and DriverLib where practical:

- protocol framing and CRC
- filtering and calibration math
- state machines
- control algorithms
- fault logic
- test vectors

Place GPIO, timer, UART, SPI, I2C, ADC, PWM, DMA, interrupt, and clock access behind thin target adapters. Keep generated handles/macros inside those adapters.

## Timing And Control

- Choose one authoritative time base for each control loop.
- Prefer hardware timer, PWM/ADC trigger chains, or RTOS periodic scheduling over main-loop busy waits.
- Measure execution time and jitter at the actual optimization level.
- Define saturation, integral anti-windup, derivative filtering, output slew limits, and safe actuator state when applicable.
- Keep telemetry from blocking the control path. Use rate limiting, buffering, DMA, or a lower-priority task.
- Recalculate periods after clock-tree changes on either platform.

## Interrupt And DMA Ownership

- Make each shared variable's owner explicit.
- Keep an ISR bounded and nonblocking; acknowledge the source, capture data/state, and notify deferred work.
- Use `volatile` for simple ISR-shared flags/counters, but do not treat it as atomicity or a lock.
- Protect multi-word state and ring-buffer indices against races.
- Do not reuse a DMA TX buffer until transfer completion is observed.
- For circular RX DMA, define how the consumer detects new data, wraparound, overrun, and partial frames.
- Handle cache maintenance on MCUs that require it; do not add it blindly on parts without data cache.

## Serial And Module Integration

Before writing a driver, obtain the exact module datasheet and verify:

- supply voltage and current
- logic voltage and level shifting
- ground and reference connections
- reset, enable, boot, address, and mode pins
- pull-ups, termination, chip select, UART TX/RX crossover, SPI mode, and I2C address
- frame format, byte order, checksum/CRC, timeout, retry, and error response

Create known-good test frames and parser tests before testing the full control system. Reject malformed lengths and out-of-range payloads safely.

## RTOS Projects

If `FreeRTOSConfig.h`, task creation, scheduler startup, queues, notifications, semaphores, or RTOS headers are present:

- preserve task and ISR ownership boundaries
- use only ISR-safe APIs from interrupts
- verify interrupt-priority rules for the selected port
- avoid unbounded blocking and priority inversion in time-critical paths
- size stacks using evidence when possible
- keep the hardware configuration workflow unchanged: `.ioc` for STM32 or `.syscfg` for MSPM0

## Validation Ladder

Use the lowest-cost checks first and preserve evidence:

1. Static inspection: configuration source, pin conflicts, names, ownership, bounds, and generated-code safety.
2. Generation: no generator errors; warnings recorded and evaluated.
3. Build: compiler/linker command, zero errors, warnings reported, fresh output artifact.
4. Flash: correct target/probe, program/verify/reset result.
5. Smoke test: boot indicator, watchdog behavior, basic UART/GPIO/peripheral response.
6. Protocol test: known frames, error injection, timeout, and recovery.
7. Instrumented test: logic analyzer, oscilloscope, multimeter, load, encoder, or calibrated reference.
8. Acceptance test: repeat the official conditions and record measurements for every criterion.

Use explicit result labels such as `source-checked`, `generated`, `built`, `flashed`, `observed`, and `acceptance-passed`.

## Hardware Debugging Order

When behavior fails, check in this order:

1. supply, ground, reset/boot state, and visible damage/heat
2. board revision, schematic, pin map, jumpers, and alternate pin functions
3. clock startup and actual clock-dependent signal frequency
4. probe connection and correct target configuration
5. generated init calls and peripheral enable/start calls
6. interrupt flags, priorities, DMA state, and buffer ownership
7. protocol timing, polarity, mode, address, and framing
8. application state machine and numeric scaling

Separate a firmware hypothesis from evidence. A clean build does not eliminate wiring, power, clock, or measurement errors.

