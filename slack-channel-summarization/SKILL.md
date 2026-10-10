---
name: slack-channel-summarization
description: Summarize activity from one Slack channel and return a concise recap, post-ready update, or summary doc.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。

本技能需要已配置的 Slack/Google Calendar 连接器或官方 API。导出不包含连接器服务器、账号授权或令牌；调用与发消息仍按用户授权和当前工具接口执行。

# Slack Channel Summarization

Use this skill to summarize activity from one Slack channel, using a requested time window when provided or the last 100 messages otherwise, and optionally deliver the result back into Slack.

## Related Skills

| Workflow | Skill |
| --- | --- |
| Draft, send, or rewrite the final Slack update | [../slack-outgoing-message/SKILL.md](../slack-outgoing-message/SKILL.md) |

## Start Here

- If the user did not name a channel, ask which channel to review.
- If the user provided a window, use it. For requests like "today" or "this week," resolve the user's timezone with `slack_read_user_profile`.
- If the user did not provide a window, default to the last `100` messages in the channel.

## Workflow

1. Resolve the named channel with `slack_search_channels`.
2. Collect the initial pass with `slack_read_channel` and `limit: 100`. If the user gave a window, set `oldest` and `latest`. If not, read the latest messages.
3. Read a thread using `slack_read_thread` when the parent message looks important to the summary, for example a decision, blocker, launch, incident, or open question. Default to the last `50` replies unless the request requires more.
4. Read the full `## Formatting Rules` section below.
5. Consolidate the channel activity into a short summary grouped by topic. The summary should include recurring conversations, key decisions or follow-ups, notable updates, and important threads.
6. Match the delivery format to the request:
   - short recap or brief: reply in chat or use `../slack-outgoing-message/SKILL.md` for a Slack message
   - summary doc or canvas: use `slack_create_canvas`
7. Delivery intent rules:
   - if the user explicitly asked to post or send the summary in Slack, write it directly
   - if the user explicitly asked for a draft or review-first flow, create a draft
   - if the user asked for a canvas or summary doc in Slack, treat that as an immediate write, not a draft
   - if the user did not ask for Slack delivery, return the summary in chat

## Formatting Rules

- For a concise Slack or chat summary, you MUST use exactly this structure unless the user explicitly requests a different format.
- If you use `../slack-outgoing-message/SKILL.md` to draft or send the final message, this output contract remains binding. The downstream skill does not relax or rename these sections.


```md
**Channel Summary - <channel>**
**Overview**
<1-2 sentence summary>

**Topic: <topic 1>**
- ...
- ...

**Topic: <topic 2>**
- ...
- ...

**Notes**
- <gaps, caveats, or sparse activity>
```

- Group the summary into 2–4 topics when possible.
- Keep each topic to 1–5 bullets.
- Use the overview to explain what the channel was focused on overall.
- Start each bullet with the main update. Add an owner or next step only when it is clear from the channel.
- Within each topic, capture decisions, action items, notable updates, and thread outcomes.
- Note if a thread is still open or unresolved instead of implying it concluded.
- Omit **Notes** when there are no caveats, gaps, or sparse-activity disclaimers to add.
- For a canvas, expand each topic into a short section and use `slack_create_canvas`. Do this only when the user explicitly asked for a canvas, doc, or Slack-hosted summary.
