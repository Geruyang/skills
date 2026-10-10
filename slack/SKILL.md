---
name: slack
description: Read Slack context, route to the right Slack workflow, and prepare or perform Slack writes that match the user's intent.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。

本技能需要已配置的 Slack/Google Calendar 连接器或官方 API。导出不包含连接器服务器、账号授权或令牌；调用与发消息仍按用户授权和当前工具接口执行。

# Slack

## Overview

Use this skill as the router for Slack work. Read the relevant Slack context first, then hand off to the most specific Slack workflow.
If the task will produce outgoing Slack text or perform a Slack write, switch to [../slack-outgoing-message/SKILL.md](../slack-outgoing-message/SKILL.md) before finalizing and reread that file's `## Formatting Rules` section immediately before any send, draft, schedule, or canvas creation.

## Related Skills

| Workflow | Skill |
| --- | --- |
| Message composition, rewrites, drafts, and canvas-writing workflows | [../slack-outgoing-message/SKILL.md](../slack-outgoing-message/SKILL.md) |
| Bounded channel recaps and thematic Slack summaries | [../slack-channel-summarization/SKILL.md](../slack-channel-summarization/SKILL.md) |
| Daily digests across selected channels or topics | [../slack-daily-digest/SKILL.md](../slack-daily-digest/SKILL.md) |
| Find messages that likely need a response and prepare reply drafts | [../slack-reply-drafting/SKILL.md](../slack-reply-drafting/SKILL.md) |
| Triage for what the user needs to read, reply to, or do next | [../slack-notification-triage/SKILL.md](../slack-notification-triage/SKILL.md) |

## Reference Notes

| Task | Reference |
| --- | --- |
| Slack Markdown formatting rules and examples | [references/markdown.md](./references/markdown.md) |

## Support Checks

- Confirm the requested action is supported before asking the user for more input. If Slack does not support the action, say so immediately and offer the closest supported path instead of collecting unnecessary details.
- For broad Slack analysis requests, fail fast if the connector cannot establish the needed coverage or signals reliably. Do not invent channel names, imply the user is in a channel, or present workspace-wide conclusions as authoritative. Ask for a candidate list, a narrower scope, or a question that can be answered from specific channels, threads, profiles, or search results.
- The current Slack app surface here supports reading/searching channels, users, threads, and canvases plus writing messages, drafts, scheduled messages, and canvases. Do not claim support for creating channels, editing messages, deleting messages, or other unsupported Slack admin actions.

## Intent Routing

- If the user explicitly asks to send, post, reply, share, or create something in Slack, follow that write intent directly. Do not downgrade the request into a draft unless the user asked for a draft or review-first flow.
- If the user explicitly asks for a draft, rewrite, or review-first workflow, use a draft.
- If the user asks for Slack analysis only, return the result in chat unless they also asked for Slack delivery.
- If the user asks for an unsupported Slack write action, say so and offer the closest supported path instead of forcing a draft.

## DM Routing

- When the same message is meant for multiple specific people, first look for an existing group DM with the right people and prefer that over duplicate one-to-one DMs.
- If there is no suitable group DM, do not silently fan out separate DMs. Ask whether the user wants individual DMs instead, or ask them to create the group DM if that is the better path and the connector cannot create it.

## Write Safety

- Preserve exact channel names, thread context, links, code snippets, and owners from the source conversation unless the user asks for changes.
- Treat @channel, @here, mass mentions, and customer-facing channels as high-impact. Call them out before posting.
- Keep post-ready drafts short enough to scan quickly unless the user asks for a long-form announcement.
- If there are multiple channels or threads with similar topics, identify the intended destination before drafting or posting.

## Output Conventions

- Prefer a short opener, a few tight bullets, and a clear ask or next step.
- Use Markdown formatting rules from `references/markdown.md` for emphasis, lists, links, quotes, mentions, and code.
- For any outgoing Slack text, use the `slack-outgoing-message` skill.
- Distinguish clearly between a private summary for the user and a post-ready message for Slack.
- When summarizing a thread, lead with the latest status and then list blockers, decisions, and owners.
- When drafting a reply, match the tone of the channel and avoid over-formatting.

## Example Requests

- "Summarize the incident thread in #ops and draft a calm update for leadership."
- "Turn these meeting notes into a short Slack post for the team channel."
- "Read the product launch thread and draft a reply that confirms the timeline."
- "Rewrite this long update so it lands well in Slack and still keeps the important links."

## Light Fallback

If Slack messages are missing, say that Slack access may be unavailable, the workspace may be disconnected, or the wrong channel or thread may be in scope, then ask the user to reconnect or clarify the destination.
