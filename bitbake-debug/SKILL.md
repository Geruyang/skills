---
name: bitbake-debug
description: Debug BitBake and Yocto build failures from task logs, run scripts, metadata expansion, packages, providers, rootfs errors, fetch/patch/configure/compile/install/package/image failures, and common QA messages. Use when the user provides BitBake output, tmp/work logs, do_* task failures, package/rootfs errors, or asks how to diagnose a Yocto build.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# BitBake Debug

Use this skill to diagnose Yocto/BitBake failures from concrete evidence. Prefer `log.do_*`, `run.do_*`, `bitbake -e`, `bitbake-layers`, and pkgdata over guesses.

## Evidence First

Ask for or inspect:

```text
failing target and task
first fatal error, not only the final summary
tmp/work/.../temp/log.do_<task>
tmp/work/.../temp/run.do_<task>
conf/local.conf
conf/bblayers.conf
affected recipe or bbappend
```

Useful commands:

```bash
bitbake-layers show-layers
bitbake-layers show-recipes <recipe>
bitbake-layers show-appends
bitbake -e <recipe>
bitbake -c listtasks <recipe>
bitbake -c devshell <recipe>
bitbake -g <target>
oe-pkgdata-util list-pkgs
oe-pkgdata-util find-path '*/path/or/file'
```

## Task Playbook

- `do_fetch`: verify `SRC_URI`, protocol, branch, `SRCREV`, checksums, network policy, mirrors, `DL_DIR`, and credentials only when the source is private.
- `do_unpack`: verify archive layout, `S`, multi-source unpack paths, and subdirectories.
- `do_patch`: verify patch path, strip level, order, fuzz, upstream status, and `apply=yes/no` only when automatic patch handling is wrong.
- `do_configure`: verify inherited class, `PACKAGECONFIG`, `EXTRA_OECONF`, `EXTRA_OECMAKE`, `EXTRA_OEMESON`, `DEPENDS`, and `recipe-sysroot`.
- `do_compile`: verify compiler command, generated files, missing `-native` tools, cross variables, and parallel race signs.
- `do_install`: verify installation under `${D}`, permissions, ownership, and paths using `${bindir}`, `${libdir}`, `${sysconfdir}`, etc.
- `do_package` / `do_package_qa`: verify package splits, `FILES:*`, runtime dependencies, and QA tags.
- `do_rootfs`: verify package names, providers, `IMAGE_INSTALL`, license policy, package conflicts, and postinstall scripts.
- `do_image`: verify rootfs completion, `IMAGE_FSTYPES`, WIC kickstart, boot artifacts, and deploy output.

## References

- Read [references/yocto-field-guide.md](references/yocto-field-guide.md) for the broader task playbook.
- Read [references/qa-errors.md](references/qa-errors.md) for common QA failures.
- Read [references/variables-core.md](references/variables-core.md) when the fix depends on variable semantics.

## Output

For every diagnosis, provide:

1. most likely cause
2. evidence that supports it
3. exact next command or metadata change
4. why this is the Yocto/BitBake fix
5. validation command
