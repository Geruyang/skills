# Upstream provenance

- Repository: https://github.com/QingquanYao/xilinx-skill
- Reviewed commit: `ccffd3704c0cd133a763a805eee893bd9c6fcf56`
- Upstream skill path: `plugins/xilinx-suite/skills/xilinx-suite`
- Upstream references path: `plugins/xilinx-suite/references`
- License declaration: MIT in the upstream README

Local packaging changes:

1. Bundled the referenced knowledge files under `references/` so the skill is self-contained.
2. Rewrote broken `../../references/` links to local `references/` links.
3. Added FPGAVibecoding board-fact guardrails for MYD/MYC-CZU3EG-V3.
4. Did not run or copy the upstream installer and did not modify any global `AGENTS.md` file.
