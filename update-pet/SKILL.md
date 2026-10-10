---
name: update-pet
description: Inspect, validate, preview, repair, or update a custom pet in ChatGPT Work mode, including its name, description, or sprite sheet. Use for a pet in ChatGPT or established ChatGPT Pets context. Exclude real-world and other-app pets; clarify before invoking.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。

本技能原先使用 Codex/ChatGPT 专属服务。先检查目标客户端是否具备对应能力；有等价工具才按其实际接口执行。缺少能力时只完成可验证的本地部分，并说明缺少的集成。不得把工具名改成 Claude/ZCode 工具名后假定功能存在。

# Update Pet

Preserve the existing custom pet's stable ID throughout the workflow. This skill owns target resolution; do not load `pets` merely to repeat it. Never call `create_pet` to update or repair an existing pet.

## Resolve the pet

1. Reuse a stable pet ID only when it has already been resolved unambiguously in the conversation. Otherwise, call `list_pets` and follow each returned `cursor` until the target is found or every page has been checked.
2. For "current" or "active," match `active_pet_id` or `is_active`. For a name, collect exact matches across every relevant page because pet names are not unique.
3. If no pet matches, tell the user. If multiple pets could match, show the candidates and ask which one to update before making changes.
4. Confirm that the resolved pet has `is_custom: true`. Built-in pets cannot be updated.
5. Keep that stable pet ID as the target. Do not use a sprite-sheet URL as identity because custom-pet URLs expire.

## Choose the update path

### Metadata only

1. Call `update_pet` with the resolved `pet_id` and an `updates` object containing only the requested `name` and/or `description` fields.
2. Omit every field that should remain unchanged. Set `description` to `null` only when the user wants to clear it, and never set `name` to `null`. A cleared description is returned and listed as an empty string even though the update request uses `null`.
3. Do not call `prepare_pet_upload`, fetch the sprite sheet, or load the artwork contract for a metadata-only update.

### Sprite sheet inspection or change, with optional metadata

1. Call `get_pet_download_link` with the resolved stable ID immediately before inspecting or editing the artwork, then fetch the existing sprite sheet before its URL expires.
2. Read and follow [the shared sprite-sheet and preview contract](references/plugin-shared/sprite-sheet-contract.md) using the fetched encoded sheet. For validation or preview only, inspect the existing bytes and render the requested artifacts without regenerating the artwork.
3. For a requested visual repair or replacement, pass the fetched sprite sheet to `$imagegen` as a reference image so the new artwork preserves the existing pet's identity. If the sheet cannot be fetched or image generation fails, stop without mutating the pet.
4. Save validation output and preview revisions to Library as required by the shared contract, but keep them outside the persisted pet record until the final encoded bytes have been validated and shown to the user.
5. If the user did not request a persisted sprite-sheet change, apply any separately requested metadata through the metadata-only path, then stop. Do not call `prepare_pet_upload` or pass an `upload_session_id` to `update_pet`.
6. Call `validate_pet_spritesheet` with `file` set to the final local sprite-sheet path, and repair every structured row/frame error until it returns `valid: true`.
7. Read and follow [the shared upload-session contract](references/plugin-shared/upload-session.md) for the final encoded sheet.
8. Call `update_pet` with the resolved `pet_id` and an `updates` object whose `upload_session_id` is `upload.upload_session_id`. Include `name` and/or `description` in that same object only when the user requested those changes.

## Verify the update

1. Confirm that the returned `pet.id` is exactly the resolved stable ID. Treat a different ID as a failure and do not attempt to repair it by creating another pet.
2. Confirm the requested metadata and `is_custom` state from the returned pet.
3. Call `select_pet` only if the user separately asked to activate this pet. Otherwise, verify that the update preserved the prior active selection.
4. Page through `list_pets` until the same stable ID appears and verify its requested metadata and active state.
5. For a sprite-sheet update, call `get_pet_download_link` only when the user or a verification step needs the stored bytes. Keep the stable pet ID, not the returned URL, as durable identity.
