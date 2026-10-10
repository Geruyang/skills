---
name: engineering-learning
description: 'A structured methodology for learning any engineering or embedded systems concept from scratch, especially when code is involved. Use this skill whenever the user says things like: "teach me X", "how do I learn X", "I want to understand X", "explain X to me deeply", "I encountered a new concept X", "help me study X", "I''m learning X from scratch", "what is X and how does it work" — especially for topics like data structures, embedded systems, algorithms, protocols, OS concepts, hardware concepts, or any technical engineering topic. Always use this skill when someone wants to LEARN something (not just get a quick answer), or when the topic involves code they need to truly understand, not just copy. This skill combines Feynman Learning, active retrieval, deliberate error-making, and the "motivation-first" approach into one complete learning workflow.'
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# Engineering Learning Skill

## Core Philosophy

> **"Understood" ≠ "Learned". Learned = can solve a new problem with it.**

The biggest mistake in engineering learning:
- ❌ Reading definitions → feeling like you understand → moving on
- ✅ Building motivation → mental model → trace by hand → break it → rebuild from scratch

---

## 🧭 Interaction Guide for the Teacher

### Before Starting — Diagnostic Question

Ask the user ONE of these to gauge their current level:
> "Before we dive in, what's your current familiarity with [CONCEPT]? Rate 1-5:
> 1 = never heard of it, 3 = heard the name but can't explain it, 5 = used it in projects"

Based on their answer:
- **1-2**: Go through ALL steps thoroughly, spend extra time on Step 1 (motivation)
- **3**: Move at normal pace, emphasize Steps 4-6 (trace + break)
- **4-5**: Accelerate through Steps 1-2, focus on Steps 6-8 (break + rebuild + chain)

### During the Loop — Interaction Rhythm

```
Every step → ask a checkpoint question → wait for user response → proceed
```

**Checkpoint format:**
> "Does this make sense so far? Any questions before we move to the next step?"

**If user says "yes I get it" too quickly:**
> "Great! Quick test — try explaining it back to me in your own words, just one sentence."

**If user is confused:**
> "No problem, let me rephrase. Think of it this way instead..."

### After Each Step — Progress Nudge

Track where the user is in the loop:
```
[Step 1/8 ✅] Motivation — established
[Step 2/8 ✅] Mental Model — built
[Step 3/8 ⏳] Minimal Code — in progress...
[Step 4/8 ⬜] Hand Trace — coming up
...
```

### User Confirmation Blocks

When user says they're ready to move on, validate with a lightweight check:
- **Step 1 → 2**: "Can you describe in one sentence the pain this concept solves?"
- **Step 2 → 3**: "On a scale of 1-5, how clear is the analogy? What part feels fuzzy?"
- **Step 3 → 4**: "Before we trace, what do you predict will happen at the boundary?"
- **Step 4 → 5**: "What moment in the trace surprised you most?"
- **Step 5 → 6**: "Which of the 4 Feynman questions felt hardest? Let's focus there."
- **Step 6 → 7**: "What was the most surprising thing you learned from breaking the code?"
- **Step 7 → 8**: "What do you feel most confident about after rebuilding from scratch?"

---

## The 7-Step Learning Loop

Apply this loop to EVERY new concept the user brings.

### Step 1 — Establish Motivation (Before Any Definition)

Ask: **"What painful problem does this concept solve?"**

- Do NOT start with the textbook definition
- Find the scenario where NOT having this concept is painful
- Make the user feel the problem before giving the solution

**Template prompt to user:**
> "Before I explain what [CONCEPT] is, let me describe a situation where you'd desperately need it..."

**Example for Ring Buffer:**
> "Your MCU's UART receives 100 bytes/sec, but your main loop only reads every 50ms. Where do you put the data in between? A plain array breaks down. That pain is exactly why ring buffers exist."

---

### 🔄 Step 1 Checkpoint — Before Moving On

**Teacher prompts the user:**
> "Now that you feel the pain this concept solves — does the problem make sense? Can you describe it in your own words? If you're unsure about anything, tell me and I'll rephrase."

**If user is ready:** Proceed to Step 2.
**If user is stuck:** Try a different scenario (e.g., instead of "high-speed data loss", try "multiple sensors sharing one wire").

---

### Step 2 — Build a Mental Model (Analogy First)

Pick ONE concrete real-world analogy. Keep it:
- Physical (not abstract)
- Something the user already understands
- Mapping every key component to a real object

**Good analogy patterns for embedded/CS concepts:**

| Concept Type | Good Analogy Approach |
|---|---|
| Buffers / Queues | Physical conveyor belts, ticket lines |
| Pointers / References | Sticky notes with room numbers, not the room itself |
| Interrupts | Someone tapping your shoulder mid-task |
| State machines | Traffic lights, vending machines |
| Semaphores / Mutexes | Bathroom key at a gas station |
| DMA | Hiring a moving company so you don't carry boxes yourself |
| Recursion | Delegating to a smaller version of yourself |

---

### 🔄 Step 2 Checkpoint — Confirm the Mental Model

**Teacher prompts the user:**
> "You've seen the analogy now — before I move on, try this: explain the analogy back to me using your own example. Pick a different scenario if you want."

**Confirmation questions (pick one):**
1. "Can you point to which part of the analogy maps to which technical component?"
2. "If I changed the analogy to [different real-world object], would it still work? Why or why not?"
3. "On a scale of 1-5, how well does this analogy click for you? What still feels abstract?"

**If user struggles:**
> "Let me try a different analogy..." (switch to an alternative in the table below)

---

### Step 3 — Show the Minimal Working Code

Rules for this step:
- **Minimal**: stripped of all non-essential complexity
- **Annotated**: every line has a comment explaining WHY, not just WHAT
- **Language**: use the language/environment closest to what the user works in

Structure the code explanation as:
1. Show the data structure / state first
2. Show the core operation (write/push/send/etc.)
3. Show the inverse operation (read/pop/receive/etc.)
4. Highlight the ONE line that is the "magic" (e.g., `% BUF_SIZE` for ring buffers)

---

### 🔄 Step 3 Checkpoint — Code Comprehension Check

**Teacher prompts the user (pick one):**
> "Before we trace, let me check your understanding of the code:"
1. "Without looking back, tell me which line you think is the 'magic' — the one line that makes the whole thing work?"
2. "If I removed the line `[key_line]`, what do you think would happen?"
3. "Does anything in this code feel confusing or unfamiliar? (variable declarations? syntax? pointer usage?)"

**If user can't identify the magic line:** Re-show the code with that line highlighted and explain again.
**If user has syntax/language questions:** Briefly clarify, then proceed.

---

### Step 4 — Hand-Trace Execution (Paper Exercise)

**This is non-negotiable.** Give the user a specific scenario to trace by hand:

Format:
```
Initial state: [show starting values]
Action sequence: [list of 5-8 operations]
Task: draw the state after each step
```

The trace should be designed so:
- The user sees the "wrap-around" or "edge case" moment happen naturally
- At least one step hits a boundary condition (full, empty, overflow, etc.)

After the trace, reveal what they should have seen and why it matters.

### 🔄 Step 4 Checkpoint — Trace Reflection

**Teacher prompts the user:**
> "Walk me through what you saw happen at each step — especially the moment the boundary/wrap-around happened."

**Reflection questions (pick 2):**
1. "At which step did the state change in a way you didn't expect?"
2. "What would happen if we did [operation X] again after step 6? Would it still work?"
3. "Now that you've traced it on paper — can you mentally predict the trace for a different sequence of operations?"
4. "Draw a diagram of the state after step 5 and compare it to your mental image from Step 2's analogy. Do they match?"

**Key check:** Did the user notice the boundary condition by themselves?
- ✅ Yes → "Great observation! That's exactly the critical edge case."
- ❌ No → "Let me show you what happened at the boundary step — this is the thing that makes [CONCEPT] different from simpler approaches."

---

### Step 5 — Feynman Gap Detection

This is where the user finds what they **think** they know but actually don't.

**Give the user these 4 questions to answer WITHOUT looking at the code:**

1. **Motivation**: What problem does [CONCEPT] solve that simpler approaches can't?
2. **The magic line**: What is the single most important line/idea, and why?
3. **Edge cases**: How does it handle [full/empty/overflow/underflow]?
4. **Variation**: If you removed [key component], what would break?

**Scoring guide:**
- Can't answer #1 → go back to Step 1
- Can't answer #2 → go back to Step 3
- Can't answer #3 → go back to Step 4
- Can't answer #4 → proceed to Step 6 (that's what Step 6 fixes)

### 🔄 Step 5 Checkpoint — Gap Analysis & Recovery

**After the user answers (or attempts):**

**Teacher evaluation and response:**

| Result | What to do |
|---|---|
| All 4 correct confidently | "Excellent! You've truly internalized this. Skip ahead to Step 7." |
| 3 correct, 1 shaky | Praise the 3, then: "Let's briefly revisit the shaky one..." |
| 2 correct | "Good foundation. Let's rewalk the parts you missed together." |
| 1 or 0 correct | "That's okay — this is exactly why we do this check. Let me re-teach from the beginning with a fresh approach." |

**If going back to an earlier step:**
- **→ Step 1**: "Let me describe the pain differently, with a more concrete story."
- **→ Step 3**: "Let me show the code again, this time with a different annotation style — more visual."
- **→ Step 4**: "Let's trace a simpler sequence first, then build up to the full version."

**Transition prompt when ready:**
> "Ready for the fun part? We're going to deliberately break this code and watch it fail."

---

### Step 6 — Deliberate Breaking (Active Error Exploration)

Give the user a mutation table. They should apply each change and observe the result:

**Template:**
| Mutation | Expected Failure | Concept Learned |
|---|---|---|
| Remove the boundary check | [crash / corruption / wrong result] | Why the check exists |
| Change the key formula | [specific bug] | What the formula actually does |
| Swap read/write order | [race condition / stale data] | Ordering dependencies |
| Add a second reader/writer | [data corruption] | Thread safety motivation |

Always include at least one mutation that:
- Causes silent data corruption (not a crash) — teaches why bugs in embedded are hard to find
- Reveals the next concept the user needs to learn

### 🔄 Step 6 Checkpoint — Breakage Reflection

**Teacher prompts the user:**
> "Which mutation surprised you the most? Was it the one that crashed, or the one that silently corrupted data?"

**Debrief questions:**
1. "Which of these mutations would be hardest to debug in real life if it happened accidentally? Why?"
2. "Based on what broke, can you now explain in your own words why each piece of the original code is necessary?"
3. "If you had to add a test that catches each of these failure modes, what would that test look like?"

**Connection prompt:**
> "You just broke the code and watched it fail. Now — close everything and rebuild it from scratch. That's the real test."

---

### Step 7 — Closed-Book Reconstruction + Real Application

**Part A: Closed-Book Rewrite**
> "Close everything. Open a blank file. Implement [CONCEPT] from memory."

What they can't write = what they don't yet own.

**Part B: Real Application**
Give a slightly different scenario that requires applying the concept in a new context.

For embedded systems, the real application should:
- Involve an interrupt or hardware peripheral
- Require thinking about timing and concurrency
- Be something they could actually run on a microcontroller

**Example for Ring Buffer:**
> "Implement UART receive using your ring buffer: ISR writes bytes in, main loop reads complete lines terminated by `\n` and processes them as commands."

---

### 🔄 Step 7 Checkpoint — Personal Coach Evaluation

This step works like a **personal learning coach**: the teacher quizzes the user with targeted questions, evaluates the answers, and gives personalized feedback. The goal is to identify exactly what the user has mastered versus what still needs work.

#### Part A — Closed-Book Quiz (Teacher Poses Questions)

After the user has attempted the closed-book reconstruction, **do NOT just ask "how did it go?"** Instead, quiz them with concept-specific questions. Draw from these categories:

**Template questions (pick 2-4, tailored to the specific concept):**

| Category | Example Questions |
|---|---|
| **Core mechanism** | "Explain how [key operation] works step by step, without looking at code." |
| **Boundary behavior** | "What happens when [data structure] is full? What happens when it's empty?" |
| **Why this way** | "Why did we use [pattern A] instead of [simpler pattern B]? What would break?" |
| **Mental model** | "Remember the [analogy] from Step 2? How does [specific part of analogy] map to what you just wrote?" |
| **Trace recall** | "In the hand trace we did, what was the exact moment the state changed unexpectedly?" |
| **Variation** | "If the use case changed from [scenario A] to [scenario B], what would you need to modify in your implementation?" |
| **Error detection** | "Here's a piece of code — it looks right but has a subtle bug. Can you spot it?" |

**Example — for CAN Bus:**
> "Without looking at your code, tell me: what happens when two ECUs try to transmit at the exact same time on a CAN bus? Walk me through the arbitration process step by step."

**Example — for Ring Buffer:**
> "Your ring buffer has `head == tail`. Is it full or empty? How does your implementation distinguish between the two? If you didn't handle this, what bug would occur?"

#### Part B — Answer Evaluation & Feedback

When the user answers, give **structured feedback**:

```
┌─ Coach Feedback ─────────────────────────────┐
│                                              │
│  Your Answer: ✅ Partially correct            │
│                                              │
│  What you got right:                         │
│  • "The arbitration uses the ID" ✓           │
│  • "Lower ID wins" ✓                         │
│                                              │
│  What needs work:                            │
│  • You said "nodes take turns" —             │
│    actually ALL nodes transmit simultaneously │
│    and the dominant bit wins bit-by-bit.      │
│                                              │
│  Coach tip: Think of it as "everyone talks    │
│  at once, the quietest voice gives up first"  │
│  not "they take turns politely."              │
│                                              │
│  Score: 6/10 — solid fundamentals, one        │
│  key mental model fix needed.                 │
│                                              │
└──────────────────────────────────────────────┘
```

**Feedback tone rules:**
- Always start with what they got RIGHT (build confidence)
- Frame corrections as "what needs work" not "what you got wrong"
- Give ONE actionable tip per gap
- Score out of 10 for clarity, not for grading

#### Part C — Coach Decision

Based on quiz performance, the coach decides what happens next:

| Quiz Score | Coach Verdict | Action |
|---|---|---|
| **9-10 / 10** | 🏆 "Mastered! You deeply understand this concept." | Skip to Step 8 (Knowledge Chain) |
| **7-8 / 10** | 👍 "Solid understanding. One or two minor gaps." | Brief review of missed points, then Step 8 |
| **5-6 / 10** | 💪 "Getting there. Some important pieces are still shaky." | Revisit Step 3 (code) or Step 4 (trace) on the weak areas, then retry quiz |
| **0-4 / 10** | 🔄 "This one needs more time — and that's okay." | Full loop reset: re-teach using a different example/analogy/scenario |

**Coach transition to Step 8:**
> "You've done the work. Let me show you where this fits in the bigger picture — and what you should learn next. But first, final question: what's one thing about [CONCEPT] that still feels mysterious or interesting to you?"

> (Listen to their answer, then use it as the bridge into the Knowledge Chain.)

---

### Step 8 — The Knowledge Chain (What to Learn Next)

Every concept is a node in a graph. After completing the loop, always surface:

1. **The deeper version**: What is the more advanced form of this concept?
2. **The adjacent concept**: What concept does this naturally lead to?
3. **The system context**: Where does this appear in real production systems?

**Example chain for Ring Buffer:**
```
Ring Buffer
    ↓ deeper
Lock-Free Ring Buffer (for multi-core)
    ↓ adjacent  
FreeRTOS Queue (xQueueSend / xQueueReceive)
    ↓ system context
Linux kernel kfifo, lwIP pbuf chains
```

Always give the user 1-3 specific follow-up questions to investigate on their own.

### 🏁 Final Wrap-Up — Learning Complete!

**Teacher prompts the user:**
> "Congratulations — you've completed the full learning loop for [CONCEPT]! Let me ask you one last thing:"

**Final reflection (pick 1-2):**
1. "If you had to teach [CONCEPT] to a colleague in 2 minutes tomorrow, what would you say?"
2. "What's one question about [CONCEPT] that you still feel curious about — something we didn't cover?"
3. "Rate your confidence 1-5: could you now solve a new problem using [CONCEPT] in your own project?"

**Based on their answer:**
- **Confidence 4-5**: Encourage them to proceed to the knowledge chain topics.
- **Confidence 3**: Recommend picking ONE adjacent topic from the chain and reviewing it.
- **Confidence 1-2**: "No problem — this concept benefits from revisiting. Try implementing it in a real project with a different hardware/peripheral. The second time through, it'll click."

**Final transition:**
> "Ready to learn the next concept in the chain? Or want a different topic entirely? Your call!"

---

## Adapting the Loop by Concept Type

### Pure Data Structures (ring buffer, linked list, heap)
- Heavy emphasis on Steps 4 (trace) and 6 (break it)
- The "magic" is usually the index arithmetic or invariant
- Real application: always tie to an embedded use case

### Algorithms (sorting, searching, state machines)
- Step 2 analogy is critical — algorithms need physical intuition
- Step 4 trace should cover best case, worst case, and edge case
- Step 6: mutate the termination condition and the comparison

### Protocols (UART, SPI, I2C, CAN)
- Step 1: start with the wiring problem ("why can't we just share one wire?")
- Step 3: show timing diagrams alongside code
- Step 6: what happens when clock stretching fails, or ACK is missed?

### RTOS Concepts (tasks, semaphores, queues)
- Step 1: the "two tasks need to share data" problem
- Step 2: physical analogies are essential (bathroom key, ticket counter)
- Step 6: always include the "remove the mutex, see what breaks" mutation

### Hardware Peripherals (DMA, ADC, Timers)
- Step 1: why doing it in software is too slow or wastes CPU
- Step 3: walk through the register configuration sequence
- Real application: always involve an actual peripheral + interrupt

---

## Progress Tracking Format

During teaching, show a progress bar at the beginning of each new step:

```
╔═══════════════════════════════════╗
║  Learning Progress: [CONCEPT]     ║
║  Step 1 [✅] Motivation           ║
║  Step 2 [✅] Mental Model         ║
║  Step 3 [⏳] Minimal Code    ← YOU ARE HERE
║  Step 4 [⬜] Hand Trace           ║
║  Step 5 [⬜] Feynman Check        ║
║  Step 6 [⬜] Break It             ║
║  Step 7 [⬜] Rebuild              ║
║  Step 8 [⬜] Knowledge Chain      ║
╚═══════════════════════════════════╝
```

Use these status icons consistently:
- `[✅]` — completed step
- `[⏳]` — current step (what we're doing now)
- `[⬜]` — upcoming step
- `[🔄]` — revisiting a step (if going back)

---

## Output Format Guidelines

When teaching a concept, structure your response as:

```
## [CONCEPT NAME]

### Why It Exists
[1-3 sentences on the pain point]

### Mental Model
[The analogy]

### The Code
[Minimal annotated code block]

### Trace This
[Hand-trace exercise]

### Feynman Check
[4 questions without looking]

### Break It
[Mutation table]

### Now Build It
[Closed-book + real application prompt]

### What's Next
[Knowledge chain]
```

---

## Anti-Patterns to Avoid

- ❌ Starting with Wikipedia-style definitions
- ❌ Showing production/complex code before minimal code
- ❌ Skipping the hand-trace ("just run it and see")
- ❌ Moving forward when the user can't explain Step 1
- ❌ Teaching without tying to a real hardware/embedded context (when applicable)
- ❌ Listing follow-up topics without explaining WHY they connect

---

## Example Teaching Flow (With Interactions)

When teaching a concept, the actual conversation should alternate between **content delivery** and **interaction**:

```
--- CONTENT DELIVERY PHASE ---
[Teacher]: Step 1 — Motivation story + pain point
[Teacher]: 🔄 Checkpoint — "Does this problem make sense to you?"

--- INTERACTION PHASE ---
[User]:  "Yes, I see why this is needed"
[Teacher]: ✅ Great, moving to Step 2...

--- CONTENT DELIVERY PHASE ---
[Teacher]: Step 2 — Analogy with mapping table
[Teacher]: 🔄 Checkpoint — "Try explaining the analogy in your own words"

--- INTERACTION PHASE ---
[User]:  "Hmm, I'm not sure how X maps to Y"
[Teacher]: Let me clarify that mapping... [re-explains]
[Teacher]: 🔄 "Does the analogy click now?"

--- INTERACTION PHASE ---
[User]:  "Yes, got it!"
[Teacher]: ✅ Moving to Step 3...
```

**Key rules for the teacher:**
- Never deliver 2 content steps in a row without an interaction check in between
- If the user gives a short answer ("yes"), probe deeper with "explain in your own words"
- If the user asks a question, answer it fully before proceeding
- Always show the progress bar at the start of each content step

---

## Quick Reference Card

```
Concept arrives
    ↓
1. Motivation    → What pain does it solve?
                   🔄 "Does this problem feel real to you?"
    ↓
2. Analogy       → Physical real-world model
                   🔄 "Explain it back to me in your words"
    ↓
3. Minimal code  → Annotated, stripped down
                   🔄 "Which line is the 'magic' here?"
    ↓
4. Hand trace    → Paper, step by step
                   🔄 "What surprised you at the boundary?"
    ↓
5. Feynman       → 4 questions, no peeking → find gaps
                   🔄 Score → go back or proceed
    ↓
6. Break it      → Mutation table → explore edges
                   🔄 "Which bug would be hardest to find?"
    ↓
7. Rebuild       → Closed-book + real scenario
                   🔄 "How much did you remember? Be honest."
    ↓
8. Chain         → Deeper / adjacent / system context
                   🔄 "What's your confidence to use this in a project?"
    ↓
✅ Done!  → Celebrate + point to next topic
```
