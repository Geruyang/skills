---
name: teach-me-the-codebase
description: On-the-fly conversational tutor that teaches you an unfamiliar repo's domain, architecture, and conventions interactively — reading the canonical docs and code, never writing them. Use when onboarding to a new codebase, when you ask to be taught or walked through how a repo works, or when you want to understand a project's structure before changing it.
disable-model-invocation: true
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# Teach Me The Codebase

An interactive onboarding tutor. You're new to this repo (or returning to a corner
of it you've forgotten) and want to *understand* it — the domain it models, how
it's put together, and the conventions it follows — before you touch anything. This
skill teaches that, conversationally, in the session. It produces **no persisted
artefacts**: there are no `lessons/`, no `learning-records/`, no progress files. The
value is the understanding you walk away with, not a folder of notes.

## Teacher-only boundary

This skill **reads, it never writes** the repo's canonical knowledge. It is a
teacher, not an author:

- It reads the existing **`CONTEXT.md`** (and `CONTEXT-MAP.md` if the repo is
  multi-context), the **ADRs** in `docs/adr/`, **`CLAUDE.md`** / `AGENTS.md`, and
  the **code** itself.
- It **never** writes `CONTEXT.md`, never creates a parallel glossary, never edits
  ADRs. If, while teaching, you hit a term the docs don't define or a decision the
  ADRs don't record, that's a gap in the canonical docs — and authoring them is a
  *different* job. Hand it off:
  - **An undocumented domain term** → `/grill-with-docs` (it sharpens the term and
    writes it into `CONTEXT.md` using the `domain-modeling` skill (if installed; not present in this export)
    CONTEXT format).
  - **A load-bearing decision the code makes but no ADR explains** → `/grill-with-docs`
    again, which offers an ADR via the `domain-modeling` skill (if installed; not present in this export)
    ADR format when the decision is hard-to-reverse, surprising, and a real
    trade-off.

  Surface the gap to the user and offer the hand-off; don't silently paper over it
  with your own glossary.

## How to teach

1. **Get your bearings from the canonical docs first.** Read `CONTEXT.md`, the ADRs,
   and `CLAUDE.md`/`AGENTS.md` before diving into code — they're the repo's own
   account of its domain language, decisions, and conventions. Use that vocabulary
   when you explain, so the user learns the repo's real terms (not invented ones).
2. **Ask what they want to learn, and at what altitude.** "The whole system at a
   glance", "how requests flow end-to-end", "this one module", "the domain model" —
   pick a starting altitude and zoom from there.
3. **Teach in a loop, one thread at a time.** Explain a piece, ground it in the
   actual files (cite `path:line`), then check understanding and follow the user's
   questions. Prefer the code and docs as evidence over assertion. When the user
   uses a fuzzy term, reach for the canonical one from `CONTEXT.md` and say where it
   came from.
4. **Connect each piece back to the whole.** Architecture is only useful in context —
   relate a module to the layer it sits in, the seam it lives behind, the ADR that
   shaped it.

## Optional cheat-sheet (on demand, never persisted)

If the user wants something to refer back to, offer to render a one-page summary of
what you covered as a **self-contained HTML cheat-sheet** via the `md-to-html`
skill — handed to them as a file to keep or discard. This is **opt-in and ephemeral**:
offer it, don't auto-generate it, and never commit it into the repo (no
`docs/onboarding/`, no checked-in notes). The teaching lives in the conversation; the
cheat-sheet is a convenience, not an artefact the repo carries.

## When to reach for a different skill

- **The docs are missing the term/decision you needed** → `/grill-with-docs` (author
  it properly; this skill won't).
- **You want to *change* the architecture, not just understand it** → `/improve-codebase-architecture`.
- **You're about to build a slice and want to align on the plan** → `/grill-with-docs`
  then `/to-prd`.
