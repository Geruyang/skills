---
name: yocto-bsp-kernel
description: Review and debug Yocto BSP, MACHINE configuration, kernel provider selection, kernel recipes, kernel config fragments, defconfig, devicetree, U-Boot, FIT images, deploy artifacts, and kernel module installation. Use for machine/BSP/kernel/devicetree/bootloader issues or when kernel artifacts are missing from deploy output.
---

## 跨客户端运行约定

本导出版本供智谱 ZCode、Claude Code 及支持 SKILL.md 的 Agent 使用。下文中的“当前 Agent/客户端”指实际执行环境；关于 Codex、OpenAI、ChatGPT 的产品说明仍指对应产品。
技能根目录以本 SKILL.md 所在目录为准，示例中的 E:/AIProject/skills 是本次导出库，可按安装位置调整。使用当前客户端真实提供的文件、终端、检索、任务与子 Agent 能力；旧工具名不是可用性证据。优先遵守当前客户端的权限规则和用户授权。
以下迁移约定优先于保留正文中涉及运行环境、专有工具和呈现语法的旧要求；领域流程、验证要求、硬件/数据接口和用户偏好继续适用。完整限制见 [PORTABILITY.md](PORTABILITY.md)。



# Yocto BSP Kernel

Use this skill for machine, BSP, kernel, devicetree, and bootloader work. Verify the selected machine, enabled BSP layers, kernel provider, and deploy artifacts before changing recipes.

## Evidence

Ask for or inspect:

```text
MACHINE
conf/machine/*.conf
enabled BSP layers
PREFERRED_PROVIDER_virtual/kernel
kernel recipe and bbappends
KERNEL_DEVICETREE
defconfig or config fragments
U-Boot variables
tmp/deploy/images/<machine>/
```

Useful commands:

```bash
bitbake-layers show-layers
bitbake-layers show-recipes virtual/kernel
bitbake-layers show-appends | rg 'linux|kernel|u-boot'
bitbake -e virtual/kernel | rg '^(MACHINE|PREFERRED_PROVIDER|KERNEL|UBOOT|SRC_URI|S)='
bitbake -c kernel_configme virtual/kernel
bitbake -c kernel_configcheck virtual/kernel
bitbake -c menuconfig virtual/kernel
bitbake -c diffconfig virtual/kernel
bitbake -c savedefconfig virtual/kernel
```

## Review Rules

- Machine config should express hardware policy; distro config should express product policy.
- Select kernel through `PREFERRED_PROVIDER_virtual/kernel` in machine or distro policy.
- Keep devicetree names aligned with kernel source and machine config.
- Use kernel config fragments or defconfig intentionally; validate with kernel config tasks.
- Verify deploy artifacts before debugging bootloader or flashing.
- Check vendor BSP branch compatibility before modernizing syntax.

## References

- Read [references/bsp-kernel.md](references/bsp-kernel.md).
- Read [references/classes-core.md](references/classes-core.md) for kernel and U-Boot classes.
- Read [references/migration.md](references/migration.md) for release compatibility risks.

## Output

Answer with:

1. selected machine and kernel provider
2. BSP/layer compatibility risk
3. kernel/devicetree/bootloader metadata issue
4. command to validate config or deploy artifacts
5. minimal metadata change
