#!/usr/bin/env python3
"""Inspect an STM32CubeMX/Keil or MSPM0 SysConfig/CCS project without modifying it."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".svn",
    "__pycache__",
    "objects",
    "listings",
    "node_modules",
}
MAX_FILES = 20000


def walk_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [name for name in dirs if name.lower() not in SKIP_DIRS]
        base = Path(current)
        for name in names:
            files.append(base / name)
            if len(files) >= MAX_FILES:
                return files
    return files


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, limit: int = 2_000_000) -> str:
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
            return handle.read(limit)
    except OSError:
        return ""


def parse_key_values(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in read_text(path).splitlines():
        if not line or line.lstrip().startswith(("#", ";")) or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def lookup(data: dict[str, str], *keys: str) -> str:
    folded = {key.casefold(): value for key, value in data.items()}
    for key in keys:
        if key.casefold() in folded:
            return folded[key.casefold()]
    return ""


def add_finding(findings: list[dict[str, str]], severity: str, message: str) -> None:
    findings.append({"severity": severity, "message": message})


def inspect_user_markers(paths: list[Path], root: Path) -> dict[str, Any]:
    marked: list[str] = []
    unbalanced: list[str] = []
    for path in paths:
        if path.suffix.lower() not in {".c", ".h", ".cpp", ".hpp"}:
            continue
        text = read_text(path)
        begins = len(re.findall(r"USER CODE BEGIN", text, flags=re.IGNORECASE))
        ends = len(re.findall(r"USER CODE END", text, flags=re.IGNORECASE))
        if begins or ends:
            marked.append(relative(path, root))
            if begins != ends:
                unbalanced.append(relative(path, root))
    return {"files_with_markers": marked, "unbalanced_markers": unbalanced}


def inspect_stm32(root: Path, files: list[Path], findings: list[dict[str, str]]) -> dict[str, Any]:
    ioc_files = [path for path in files if path.suffix.lower() == ".ioc"]
    uvprojx = [path for path in files if path.suffix.lower() == ".uvprojx"]
    scatter = [path for path in files if path.suffix.lower() in {".sct", ".scf"}]
    startup = [path for path in files if path.name.lower().startswith("startup_")]
    generated_candidates = [
        path
        for path in files
        if path.suffix.lower() in {".c", ".h", ".cpp", ".hpp"}
        and any(part.lower() in {"core", "src", "inc"} for part in path.parts)
    ]
    markers = inspect_user_markers(generated_candidates, root)
    configs: list[dict[str, Any]] = []
    for path in ioc_files:
        values = parse_key_values(path)
        toolchain = lookup(values, "ProjectManager.TargetToolchain", "ProjectManager.ToolChainLocation")
        keep_user = lookup(values, "ProjectManager.KeepUserCode")
        config = {
            "path": relative(path, root),
            "mcu": lookup(values, "Mcu.Name", "Mcu.CPN"),
            "family": lookup(values, "Mcu.Family"),
            "package": lookup(values, "Mcu.Package"),
            "project_name": lookup(values, "ProjectManager.ProjectName"),
            "toolchain": toolchain,
            "firmware_package": lookup(values, "ProjectManager.FirmwarePackage"),
            "keep_user_code": keep_user,
        }
        configs.append(config)
        if toolchain and "mdk" not in toolchain.casefold():
            add_finding(findings, "warning", f"{config['path']} targets '{toolchain}', not an MDK-ARM toolchain.")
        if keep_user.casefold() in {"false", "0", "no"}:
            add_finding(findings, "warning", f"{config['path']} disables CubeMX user-code preservation.")
    if len(ioc_files) > 1:
        add_finding(findings, "info", "Multiple .ioc files were found; select the intended STM32 project root before regenerating.")
    if ioc_files and not uvprojx:
        add_finding(findings, "warning", "STM32CubeMX configuration found, but no Keil .uvprojx project was found.")
    if markers["unbalanced_markers"]:
        add_finding(findings, "warning", "Unbalanced CubeMX USER CODE markers were found.")
    return {
        "ioc": configs,
        "keil_projects": [relative(path, root) for path in uvprojx],
        "scatter_files": [relative(path, root) for path in scatter],
        "startup_files": [relative(path, root) for path in startup],
        "user_code_regions": markers,
    }


def syscfg_metadata(path: Path) -> dict[str, Any]:
    text = read_text(path)
    cli_lines = [line.strip() for line in text.splitlines() if "@cliArgs" in line or "@v2CliArgs" in line]
    versions = [line.strip() for line in text.splitlines() if "@versions" in line]

    def option(name: str) -> str:
        match = re.search(rf"--{re.escape(name)}(?:\s+|=)[\"']?([^\s\"']+)", text)
        return match.group(1) if match else ""

    instances = sorted(set(re.findall(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=", text)))
    return {
        "device": option("device"),
        "package": option("package"),
        "product": option("product"),
        "cli_metadata": cli_lines,
        "versions_metadata": versions,
        "declared_instances": instances[:100],
    }


def inspect_mspm0(root: Path, files: list[Path], findings: list[dict[str, str]]) -> dict[str, Any]:
    syscfg_files = [path for path in files if path.suffix.lower() == ".syscfg"]
    generated_headers = [path for path in files if path.name.lower() == "ti_msp_dl_config.h"]
    generated_sources = [path for path in files if path.name.lower() == "ti_msp_dl_config.c"]
    ccs_metadata = [
        path
        for path in files
        if path.name.lower() in {".project", ".cproject", ".ccsproject"}
        or path.suffix.lower() == ".projectspec"
    ]
    ccxml = [path for path in files if path.suffix.lower() == ".ccxml"]
    init_functions: list[dict[str, str]] = []
    for path in generated_headers:
        text = read_text(path)
        matches = re.findall(r"\bvoid\s+(SYSCFG_[A-Za-z0-9_]+)\s*\(\s*void\s*\)\s*;", text)
        for name in matches:
            init_functions.append({"header": relative(path, root), "name": name})
    configs: list[dict[str, Any]] = []
    for path in syscfg_files:
        item = {"path": relative(path, root), **syscfg_metadata(path)}
        configs.append(item)
        if not item["cli_metadata"]:
            add_finding(findings, "warning", f"{item['path']} has no visible @cliArgs/@v2CliArgs metadata.")
        if not item["device"] or not item["product"]:
            add_finding(findings, "warning", f"{item['path']} does not expose complete device/product metadata to this static check.")
    if len(syscfg_files) > 1:
        add_finding(findings, "info", "Multiple .syscfg files were found; select the intended CCS project root before regenerating.")
    if syscfg_files and not ccs_metadata:
        add_finding(findings, "warning", "MSPM0 SysConfig file found, but no common CCS project metadata was found.")
    if syscfg_files and not generated_headers:
        add_finding(findings, "info", "No generated ti_msp_dl_config.h was found; run SysConfig/CCS before relying on generated names.")
    return {
        "syscfg": configs,
        "ccs_project_files": [relative(path, root) for path in ccs_metadata],
        "target_configs": [relative(path, root) for path in ccxml],
        "generated_headers": [relative(path, root) for path in generated_headers],
        "generated_sources": [relative(path, root) for path in generated_sources],
        "generated_init_functions": init_functions,
    }


def inspect_project(root: Path) -> dict[str, Any]:
    files = walk_files(root)
    findings: list[dict[str, str]] = []
    has_ioc = any(path.suffix.lower() == ".ioc" for path in files)
    has_syscfg = any(path.suffix.lower() == ".syscfg" for path in files)
    has_uvprojx = any(path.suffix.lower() == ".uvprojx" for path in files)
    has_ccs = any(
        path.name.lower() in {".project", ".cproject", ".ccsproject"}
        or path.suffix.lower() in {".projectspec", ".ccxml"}
        for path in files
    )
    if has_ioc and has_syscfg:
        platform = "mixed"
        add_finding(findings, "warning", "Both .ioc and .syscfg files were found. Treat them as separate target projects.")
    elif has_ioc or has_uvprojx:
        platform = "stm32"
    elif has_syscfg or has_ccs:
        platform = "mspm0-or-ti"
    else:
        platform = "unknown"
        add_finding(findings, "warning", "No STM32CubeMX/Keil or MSPM0/CCS project evidence was found.")
    if len(files) >= MAX_FILES:
        add_finding(findings, "warning", f"Inspection stopped after {MAX_FILES} files; narrow the project root if needed.")
    build_outputs = [
        relative(path, root)
        for path in files
        if path.suffix.lower() in {".axf", ".elf", ".out", ".hex", ".bin", ".map"}
    ]
    return {
        "root": str(root),
        "platform": platform,
        "files_scanned": len(files),
        "stm32": inspect_stm32(root, files, findings) if has_ioc or has_uvprojx else {},
        "mspm0": inspect_mspm0(root, files, findings) if has_syscfg or has_ccs else {},
        "build_outputs": build_outputs[:200],
        "findings": findings,
    }


def print_text(result: dict[str, Any]) -> None:
    print(f"Project root: {result['root']}")
    print(f"Detected route: {result['platform']}")
    print(f"Files scanned: {result['files_scanned']}")
    stm32 = result.get("stm32") or {}
    if stm32:
        print("\nSTM32CubeMX / Keil")
        for config in stm32.get("ioc", []):
            details = ", ".join(
                item
                for item in (
                    config.get("mcu"),
                    config.get("package"),
                    config.get("toolchain"),
                )
                if item
            )
            print(f"  IOC: {config['path']}{' (' + details + ')' if details else ''}")
        for path in stm32.get("keil_projects", []):
            print(f"  Keil: {path}")
    mspm0 = result.get("mspm0") or {}
    if mspm0:
        print("\nMSPM0 SysConfig / CCS")
        for config in mspm0.get("syscfg", []):
            details = ", ".join(item for item in (config.get("device"), config.get("package")) if item)
            print(f"  SysConfig: {config['path']}{' (' + details + ')' if details else ''}")
        for path in mspm0.get("ccs_project_files", []):
            print(f"  CCS: {path}")
        for item in mspm0.get("generated_init_functions", []):
            print(f"  Generated init: {item['name']} [{item['header']}]")
    if result.get("build_outputs"):
        print(f"\nBuild outputs found: {len(result['build_outputs'])}")
    if result.get("findings"):
        print("\nFindings")
        for finding in result["findings"]:
            print(f"  [{finding['severity'].upper()}] {finding['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="Project or repository directory to inspect.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()
    root = args.project_dir.expanduser().resolve()
    if not root.is_dir():
        print(f"Project directory does not exist: {root}", file=sys.stderr)
        return 2
    result = inspect_project(root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 2 if result["platform"] == "unknown" else 0


if __name__ == "__main__":
    raise SystemExit(main())

