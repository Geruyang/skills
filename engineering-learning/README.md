# engineering-learning-skill

A **Claude skill file** that transforms Claude into a structured engineering tutor — one that teaches concepts through motivation, analogy, code, hands-on tracing, deliberate breaking, and closed-book reconstruction.

> "Understood" ≠ "Learned". Learned = can solve a new problem with it.

---

## What Is This?

`SKILL.md` is a prompt skill for Claude. When you upload it or reference it in a session, Claude follows an 8-step learning loop to help you deeply internalize any engineering or embedded systems concept — not just memorize it.

This is not a flashcard system. It's a **personal tutor loop** built on Feynman Learning, active retrieval, and deliberate error-injection.

---

## The 8-Step Learning Loop

Each new concept goes through the same loop, in order:

```
Step 1 — Motivation        Why does this concept exist? What pain does it solve?
Step 2 — Mental Model      Build a concrete, physical analogy before any code
Step 3 — Minimal Code      The simplest annotated implementation possible
Step 4 — Hand Trace        Trace execution on paper, step by step
Step 5 — Feynman Check     Answer 4 questions from memory — find your gaps
Step 6 — Break It          Mutate the code deliberately, watch it fail
Step 7 — Rebuild           Closed-book reconstruction + real hardware application
Step 8 — Knowledge Chain   What to learn next and why it connects
```

At every transition between steps, Claude asks a checkpoint question — it never moves forward until your understanding is confirmed.

---

## Who Is This For?

- **Embedded systems learners** studying concepts like ring buffers, DMA, UART, mutexes, ISRs, state machines, or U-Boot
- **CS learners** working through data structures, algorithms, or OS concepts
- Anyone who wants to build **durable, transferable knowledge** instead of copy-pasting code they don't fully understand

---

## How to Use

### Option 1 — Upload in Claude.ai

1. Open a new conversation in [Claude.ai](https://claude.ai)
2. Upload `SKILL.md` as a file attachment
3. Say: _"Use this skill to teach me [CONCEPT]"_

### Option 2 — Paste as System Prompt

Copy the contents of `SKILL.md` into your system prompt when using the API or Claude Projects.

### Option 3 — Claude Projects (Recommended)

1. Create a new Project in Claude.ai
2. Add `SKILL.md` to the Project's knowledge base
3. Every conversation in that project automatically uses the skill

---

## Concept Coverage

The skill adapts its approach based on concept type:

| Concept Type | Teaching Focus |
|---|---|
| Data Structures (ring buffer, queue, heap) | Index arithmetic, invariants, boundary traces |
| Algorithms (sort, search, state machines) | Physical analogy, worst-case trace, termination mutation |
| Protocols (UART, SPI, I²C, CAN) | Wiring problem → timing diagram → ACK failure injection |
| RTOS (tasks, semaphores, queues) | Shared-data conflict → remove-the-mutex mutation |
| Hardware Peripherals (DMA, ADC, timers) | CPU-cost motivation → register walkthrough → ISR integration |

---

## Example Knowledge Chain

After completing the loop for a concept, Claude surfaces what to study next:

```
Ring Buffer
    ↓ deeper
Lock-Free Ring Buffer (for multi-core)
    ↓ adjacent
FreeRTOS Queue (xQueueSend / xQueueReceive)
    ↓ system context
Linux kfifo, lwIP pbuf chains
```

---

## Design Philosophy

This skill was built around three principles:

**Motivation before definition.** If you don't feel the pain a concept solves, the definition won't stick. Every loop starts with a scenario where *not having* the concept causes a real problem.

**Trace before run.** Running code hides the mechanism. Tracing by hand forces you to hold the state in your head — which is exactly what you need to debug production code.

**Break before you finish.** Deliberately corrupting working code and watching it fail teaches you why every line is there. A silent data-corruption mutation is worth more than any textbook explanation.

---

## Repository Structure

```
engineering-learning-skill/
├── SKILL.md          # The full skill prompt (583 lines)
└── references/       # Supporting reference material
```

---

## Contributing

Found a concept type not well-covered? Have a better analogy for a common topic? PRs and issues welcome.
