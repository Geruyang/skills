---
name: build-system
description: Build system management for Zephyr RTOS. Covers West workspace initialization, manifest management, Sysbuild multi-image builds, Kconfig symbols, and CMake integration. Trigger when setting up workspaces, configuring builds, or troubleshooting build-time errors.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# Zephyr Build System

Efficiently manage the complex build and configuration stack of Zephyr RTOS.

## Core Workflows

### 1. West Workspace & Manifests
Manage multi-repo projects and dependency allow-lists.
- **Reference**: **[west.md](references/west.md)**
- **Key Tools**: `west init`, `west update`, `west manifest --resolve`, `name-allowlist`.

### 2. Kconfig Configuration
Tune software features and hardware parameters.
- **Reference**: **[kconfig.md](references/kconfig.md)**
- **Key Tools**: `west build -t menuconfig`, symbol searching (`/`), help (`?`).

### 3. Sysbuild & Multi-Image
Configure complex projects like MCUboot + Application.
- **Reference**: **[cmake.md](references/cmake.md)**
- **Key Tools**: `west build --sysbuild`, `sysbuild.conf`.

### 4. CMake & Project Structure
Core build logic for applications and modules.
- **Reference**: **[cmake.md](references/cmake.md)**
- **Key Tools**: `CMakeLists.txt`, `zephyr_library()`, `target_sources()`.

## Quick Start (Workspace + Build)
```bash
west init -m <manifest-repo-url> zephyr-workspace
cd zephyr-workspace
west update
west build -b native_sim samples/hello_world
```

## Validation Checklist
- [ ] `west update` resolves all manifest projects without errors.
- [ ] `west build` succeeds for at least one known target board.
- [ ] Required Kconfig symbols are present in `build/zephyr/.config`.
- [ ] `scripts/find_modules.sh` reports module names that match the current manifest allow-list.

## Automation Tools

- **[find_modules.sh](scripts/find_modules.sh)**: Scan your `build/` directory to automatically identify which modules you should add to your manifest's `name-allowlist`.

## Examples & Templates

- **[west_manifest_template.yml](assets/west_manifest_template.yml)**: Minimal starter manifest for west workspaces.

## Resources

- **[References](references/)**:
  - `west.md`: West commands, manifests, and allow-lists.
  - `kconfig.md`: Project configuration and menuconfig usage.
  - `cmake.md`: Sysbuild and CMake API integration.
- **[Scripts](scripts/)**:
  - `find_modules.sh`: Automated allow-list discovery utility.
- **[Assets](assets/)**:
  - `west_manifest_template.yml`: Base west manifest template.
