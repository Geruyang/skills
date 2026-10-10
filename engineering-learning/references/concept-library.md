# Embedded Systems Concept Reference

A lookup table of pre-built analogies, magic lines, and knowledge chains
for common embedded systems / CS concepts. Read this file when the user
asks about any of these topics to get a head start on the teaching loop.

---

## Ring Buffer (Circular Buffer)

**Pain point**: Fixed memory, variable-rate producer/consumer, no heap allocation.

**Analogy**: Rotating sushi conveyor belt. Chef (ISR) places dishes, customer (main loop) takes them. Belt length is fixed; the belt wraps around.

**Magic line**: `head = (head + 1) % BUF_SIZE` — modulo makes a linear array circular.

**Critical edge case**: head == tail can mean FULL or EMPTY. Solution: keep a `count` variable, OR sacrifice one slot (full = (head+1)%N == tail).

**Feynman traps** (things people think they know but don't):
- Why modulo, not if-else reset?
- What breaks without the count/sacrificed-slot trick?
- What happens if ISR writes while main loop reads simultaneously?

**Knowledge chain**:
```
Ring Buffer → Lock-free ring buffer (atomic head/tail) → FreeRTOS Queue → Linux kfifo
```

---

## Interrupt (ISR)

**Pain point**: CPU can't poll every peripheral constantly. Polling wastes cycles and misses fast events.

**Analogy**: You're reading a book. You don't keep checking your phone every second — you set it to vibrate. The vibration IS the interrupt. You bookmark your page (save context), check the phone (ISR), then return to your page (restore context).

**Magic concept**: The vector table — a lookup table that maps interrupt number → ISR address.

**Critical edge cases**:
- ISR must be SHORT (no blocking, no heavy computation)
- Shared variables between ISR and main loop MUST be `volatile`
- Nested interrupts: priority levels and preemption

**Feynman traps**:
- Why `volatile` on shared variables?
- What happens if an ISR takes too long?
- What's the difference between IRQ priority and task priority?

**Knowledge chain**:
```
Interrupt → NVIC priority → Critical section / disable IRQ → FreeRTOS task notification from ISR
```

---

## DMA (Direct Memory Access)

**Pain point**: CPU is too busy copying bytes from peripheral to RAM. At high data rates (ADC, SPI, USB), the CPU can't keep up and misses everything else.

**Analogy**: You're moving house. You could carry every box yourself (polling/IRQ-driven), or you hire a moving company (DMA) and tell them: "Take everything from address A, put it at address B, call me when done." You go do something else.

**Magic concept**: The DMA transfer descriptor — source, destination, length, and what to do when done.

**Critical edge cases**:
- Cache coherency on Cortex-M7/A: you must flush/invalidate cache before/after DMA
- Circular DMA mode for streaming data (pairs naturally with ring buffer concept)
- Half-transfer interrupt + transfer-complete interrupt for double-buffering

**Feynman traps**:
- Who sets up the DMA — you or the peripheral?
- What happens if CPU and DMA access the same memory simultaneously?
- Why does DMA on M7 require cache management but not on M0/M3/M4?

**Knowledge chain**:
```
DMA → Double buffering → Cache coherency (MPU) → MDMA/BDMA on STM32H7
```

---

## Mutex / Semaphore

**Pain point**: Two tasks need the same resource. Without protection, they corrupt each other's work.

**Mutex analogy**: Single bathroom key at a gas station. Only one person can have it. You wait at the door until the key is returned.

**Semaphore analogy**: Parking lot with N spaces. Counter starts at N. Each car entering decrements it; each car leaving increments it. When 0, you wait.

**Magic distinction**:
- Mutex: ownership (only the locker can unlock), for mutual exclusion
- Binary semaphore: no ownership, for signaling ("I'm done, you can go")
- Counting semaphore: for resource pools

**Critical edge cases**:
- Priority inversion: low-priority task holds mutex, high-priority task starves
- Priority inheritance: RTOS solution to inversion
- Deadlock: Task A holds mutex 1, waits for 2; Task B holds mutex 2, waits for 1

**Feynman traps**:
- What's the difference between mutex and binary semaphore in FreeRTOS?
- Can you take a mutex from an ISR? (No — use binary semaphore or task notification)
- What is priority inversion and why does Mars Pathfinder matter?

**Knowledge chain**:
```
Mutex → Priority inversion → Priority inheritance → Deadlock prevention → Lock-free structures
```

---

## State Machine (FSM)

**Pain point**: Code with many if/else flags becomes unmaintainable. Complex behavior with modes needs structure.

**Analogy**: Traffic light. It has states (RED, GREEN, YELLOW), events (timer expired, sensor triggered), and transitions (RED + timer → GREEN). Each state has defined behavior; transitions are explicit.

**Magic concept**: The transition table — a 2D lookup: `next_state = table[current_state][event]`

**Critical edge cases**:
- What happens on an undefined/unexpected event in a state?
- Entry/exit actions vs. transition actions
- Hierarchical state machines (super-states) for complex behavior

**Feynman traps**:
- How is a state machine different from nested if/else?
- What is a "guard condition" on a transition?
- When would you use HSM (UML statecharts) instead of flat FSM?

**Knowledge chain**:
```
FSM → HSM (hierarchical) → Statechart (UML) → QP framework / Miro Samek's approach
```

---

## Watchdog Timer

**Pain point**: Embedded system gets stuck in a loop, deadlock, or hard fault. Nobody is watching. System hangs forever.

**Analogy**: Dead-man's switch on a train. The driver must press a pedal regularly to prove they're alive. If they don't, the train stops automatically. Your firmware is the driver. The watchdog is the pedal. If you stop "kicking" it, the MCU resets.

**Magic concept**: The watchdog window — some watchdogs require you to kick within a time RANGE (not too early, not too late), preventing a stuck loop that kicks too fast.

**Critical edge cases**:
- Where to kick: not inside a fast ISR (masks hang in main loop)
- Window watchdog (WWDG) vs. Independent watchdog (IWDG) on STM32
- What resets the watchdog at startup before your kick code runs?

**Knowledge chain**:
```
Basic Watchdog → Window Watchdog → Reset cause detection → Safe state on watchdog reset
```

---

## Volatile Keyword (C/C++)

**Pain point**: Compiler optimizes away reads of a variable because it doesn't know an ISR or hardware can change it.

**Analogy**: You have a whiteboard in the hall. Your colleague (ISR) can change what's written on it at any time. If you only check it once and then assume it never changes (compiler optimization), you'll miss updates. `volatile` tells the compiler: "Always re-read this from memory, never cache it in a register."

**Magic line**: `volatile uint32_t *reg = (volatile uint32_t *)0x40020000;` — hardware register access

**Feynman traps**:
- Does `volatile` make code thread-safe? (NO. It only prevents optimization, not atomicity.)
- Do you need `volatile` for FreeRTOS shared variables? (Usually no — RTOS API provides barriers)
- Why must memory-mapped peripheral registers always be `volatile`?

**Knowledge chain**:
```
volatile → Memory barriers → Atomic operations (__atomic builtins) → Memory ordering (C11 stdatomic)
```

---

## Recursion

**Pain point**: Problems with self-similar structure (trees, graphs, nested parsing) are awkward with loops because the depth is unknown at compile time.

**Analogy**: Russian nesting dolls. To open the innermost doll, you open the outer one, hand it to a helper, who opens the next, hands to another helper… until someone holds a doll they can open directly. Then everyone hands back their result.

**Magic concept**: Base case + recursive case. Without the base case, infinite recursion = stack overflow.

**Critical edge cases**:
- Stack depth: each call frame consumes stack. On embedded (often 4KB stack), deep recursion kills you.
- Tail recursion: if the recursive call is the LAST thing, compiler can optimize to a loop (TCO)

**Feynman traps**:
- Why does removing the base case cause a crash (not just wrong output)?
- What is the call stack actually doing during recursion?
- Why is recursion often avoided in embedded/safety-critical code?

**Knowledge chain**:
```
Recursion → Call stack visualization → Stack overflow on embedded → Iterative rewrite with explicit stack → Tail call optimization
```
