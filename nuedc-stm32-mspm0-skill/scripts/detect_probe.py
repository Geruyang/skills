#!/usr/bin/env python3
"""Detect common MCU debug probes without opening, resetting, or modifying a target."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass


KNOWN_USB_IDS = {
    "0451:BEF3": ("xds110", "TI XDS110"),
    "0D28:0204": ("cmsis-dap", "DAPLink CMSIS-DAP"),
    "EF1A:74E5": ("cmsis-dap", "CMSIS-DAP"),
}
STLINK_PIDS = {"3744", "3748", "374B", "374D", "3752"}


@dataclass
class Probe:
    kind: str
    display_name: str
    manufacturer: str
    usb_id: str
    serial_ports: list[str]
    confidence: str
    possible_backends: list[str]
    evidence: list[str]


def run(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out after {exc.timeout} seconds") from exc
    if completed.returncode:
        raise RuntimeError((completed.stderr or completed.stdout).strip() or "probe query failed")
    return completed.stdout


def usb_id(text: str) -> str:
    match = re.search(r"VID_([0-9A-F]{4}).*PID_([0-9A-F]{4})", text, flags=re.IGNORECASE)
    return f"{match.group(1).upper()}:{match.group(2).upper()}" if match else ""


def classify(text: str, identifier: str) -> tuple[str, str, list[str]] | None:
    lowered = text.casefold()
    if identifier in KNOWN_USB_IDS:
        kind, name = KNOWN_USB_IDS[identifier]
    else:
        vid, _, pid = identifier.partition(":")
        if vid == "1366" or re.search(r"\b(j-?link|segger)\b", lowered):
            kind, name = "jlink", "SEGGER J-Link"
        elif vid == "0483" and pid in STLINK_PIDS or re.search(r"\bst-?link\b", lowered):
            kind, name = "stlink", "ST-Link"
        elif re.search(r"\b(xds[- ]?110|tixds110)\b", lowered):
            kind, name = "xds110", "TI XDS110"
        elif re.search(r"\b(cmsis[- ]?dap|daplink)\b", lowered):
            kind, name = "cmsis-dap", "CMSIS-DAP"
        else:
            return None
    backends = {
        "stlink": ["Keil/uVision", "STM32CubeProgrammer", "OpenOCD"],
        "jlink": ["Keil/uVision", "J-Link tools", "CCS/DSLite when project-supported"],
        "xds110": ["CCS", "DSLite/UniFlash"],
        "cmsis-dap": ["Keil/uVision", "OpenOCD when target-supported"],
    }[kind]
    return kind, name, backends


def as_objects(value: object) -> list[dict[str, object]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def windows_query(script: str) -> list[dict[str, object]]:
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if not powershell:
        raise RuntimeError("PowerShell is unavailable")
    raw = run([powershell, "-NoProfile", "-Command", script]).strip()
    return as_objects(json.loads(raw or "[]"))


def detect_windows() -> list[Probe]:
    devices = windows_query(
        r'''[Console]::OutputEncoding=[Text.UTF8Encoding]::new(); @(
        Get-PnpDevice -PresentOnly -Class USB | ForEach-Object {
          [PSCustomObject]@{FriendlyName=$_.FriendlyName;Manufacturer=$_.Manufacturer;InstanceId=$_.InstanceId}
        }) | ConvertTo-Json -Depth 3 -Compress'''
    )
    try:
        ports = windows_query(
            r'''[Console]::OutputEncoding=[Text.UTF8Encoding]::new(); @(
            Get-CimInstance Win32_SerialPort | ForEach-Object {
              [PSCustomObject]@{DeviceID=$_.DeviceID;Name=$_.Name;PNPDeviceID=$_.PNPDeviceID}
            }) | ConvertTo-Json -Depth 3 -Compress'''
        )
    except (RuntimeError, json.JSONDecodeError):
        ports = []
    probes: list[Probe] = []
    seen: set[tuple[str, str]] = set()
    for device in devices:
        instance = str(device.get("InstanceId") or "")
        identifier = usb_id(instance)
        friendly = str(device.get("FriendlyName") or "")
        manufacturer = str(device.get("Manufacturer") or "")
        result = classify(f"{friendly} | {manufacturer}", identifier)
        if not result:
            continue
        kind, fallback_name, backends = result
        key = (kind, instance)
        if key in seen:
            continue
        seen.add(key)
        serial_ports: list[str] = []
        if identifier:
            vid, pid = identifier.split(":", 1)
            serial_ports = sorted(
                str(port.get("DeviceID"))
                for port in ports
                if port.get("DeviceID")
                and f"VID_{vid}&PID_{pid}" in str(port.get("PNPDeviceID") or "").upper()
            )
        probes.append(
            Probe(kind, friendly or fallback_name, manufacturer, identifier, serial_ports, "high", backends,
                  [item for item in (friendly, manufacturer, instance) if item])
        )
    return probes


def detect_linux() -> list[Probe]:
    sysfs = "/sys/bus/usb/devices"
    if not os.path.isdir(sysfs):
        return []
    probes: list[Probe] = []
    for entry in os.listdir(sysfs):
        base = os.path.join(sysfs, entry)
        values: dict[str, str] = {}
        for field in ("product", "manufacturer", "idVendor", "idProduct"):
            try:
                with open(os.path.join(base, field), encoding="utf-8", errors="replace") as handle:
                    values[field] = handle.read().strip()
            except OSError:
                values[field] = ""
        identifier = (
            f"{values['idVendor'].upper()}:{values['idProduct'].upper()}"
            if values["idVendor"] and values["idProduct"]
            else ""
        )
        result = classify(f"{values['product']} | {values['manufacturer']}", identifier)
        if result:
            kind, fallback_name, backends = result
            probes.append(
                Probe(kind, values["product"] or fallback_name, values["manufacturer"], identifier, [], "high",
                      backends, [item for item in (values["product"], values["manufacturer"], entry) if item])
            )
    return probes


def detect() -> list[Probe]:
    system = platform.system()
    if system == "Windows":
        return detect_windows()
    if system == "Linux":
        return detect_linux()
    raise RuntimeError(f"probe detection is not implemented on {system or 'this operating system'}")


def print_text(probes: list[Probe]) -> None:
    if not probes:
        print("No supported debug probe was detected.")
        print("Do not choose a flash backend until the USB connection and project configuration are confirmed.")
        return
    if len(probes) > 1:
        print(f"Detected {len(probes)} probes. Select the intended physical target before flashing.\n")
    for index, probe in enumerate(probes, 1):
        print(f"Probe {index}: {probe.kind}")
        print(f"  Device: {probe.display_name}")
        if probe.manufacturer:
            print(f"  Manufacturer: {probe.manufacturer}")
        if probe.usb_id:
            print(f"  USB ID: {probe.usb_id}")
        if probe.serial_ports:
            print(f"  Serial ports: {', '.join(probe.serial_ports)}")
        print(f"  Possible backends: {', '.join(probe.possible_backends)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()
    try:
        probes = detect()
    except (RuntimeError, json.JSONDecodeError) as exc:
        if args.json:
            print(json.dumps({"probes": [], "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"Probe detection failed: {exc}")
        return 2
    if args.json:
        print(json.dumps({"probes": [asdict(probe) for probe in probes]}, ensure_ascii=False, indent=2))
    else:
        print_text(probes)
    return 0 if probes else 1


if __name__ == "__main__":
    raise SystemExit(main())

