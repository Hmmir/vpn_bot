from __future__ import annotations

import json
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Dict
from urllib.parse import urlencode, urlparse
from urllib.request import urlopen

from ..config import (
    BOT_TOKEN,
    ADMIN_IDS,
    XUI_PUBLIC_HOST,
    XUI_PUBLIC_PORT,
    XUI_BASE_URL,
    XUI_SUB_BASE_URL,
)


BASE_DIR = Path(__file__).resolve().parents[2]
STATE_FILE = BASE_DIR / "data" / "healthcheck_state.json"


def _get_env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


COOLDOWN_SECONDS = int(_get_env("HEALTHCHECK_COOLDOWN_SECONDS", "1800") or "1800")
DISK_FREE_GB = float(_get_env("HEALTHCHECK_DISK_FREE_GB", "1") or "1")
MEM_FREE_MB = float(_get_env("HEALTHCHECK_MEM_FREE_MB", "200") or "200")
LOAD1_MAX = float(_get_env("HEALTHCHECK_LOAD_1", "2.0") or "2.0")
SERVICES_RAW = _get_env(
    "HEALTHCHECK_SERVICES",
    "x-ui.service,getnius-bot.service,getnius-support.service,getnius-webhook.service",
)


def _load_state() -> Dict[str, float]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save_state(state: Dict[str, float]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state), encoding="utf-8")


def _should_notify(state: Dict[str, float], key: str) -> bool:
    last = state.get(key, 0)
    return (time.time() - last) > COOLDOWN_SECONDS


def _notify(state: Dict[str, float], key: str, message: str) -> None:
    if not BOT_TOKEN or not ADMIN_IDS:
        return
    if not _should_notify(state, key):
        return
    for admin_id in ADMIN_IDS:
        params = urlencode({"chat_id": admin_id, "text": message})
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?{params}"
        try:
            with urlopen(url, timeout=10):
                pass
        except Exception:
            pass
    state[key] = time.time()


def _systemctl_active(name: str) -> bool:
    result = subprocess.run(
        ["systemctl", "is-active", name],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "active"


def _check_services(state: Dict[str, float]) -> None:
    services = [s.strip() for s in SERVICES_RAW.split(",") if s.strip()]
    for service in services:
        if not _systemctl_active(service):
            _notify(state, f"service:{service}", f"[ALERT] {service} is not active")


def _check_ports(state: Dict[str, float]) -> None:
    host = XUI_PUBLIC_HOST
    if not host and XUI_BASE_URL.startswith("http"):
        host = XUI_BASE_URL.split("://", 1)[1].split(":", 1)[0]
    port = int(XUI_PUBLIC_PORT or "443")
    try:
        with socket.create_connection((host or "127.0.0.1", port), timeout=5):
            pass
    except OSError:
        _notify(state, "port:public", f"[ALERT] Port {port} is not reachable")

    sub_url = XUI_SUB_BASE_URL
    if sub_url:
        parsed = urlparse(sub_url)
        sub_host = parsed.hostname or host or "127.0.0.1"
        sub_port = parsed.port or (443 if parsed.scheme == "https" else 80)
        try:
            with socket.create_connection((sub_host, sub_port), timeout=5):
                return
        except OSError:
            _notify(
                state,
                "port:sub",
                f"[ALERT] Subscription port {sub_port} is not reachable",
            )


def _check_disk(state: Dict[str, float]) -> None:
    stat = os.statvfs("/")
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
    if free_gb < DISK_FREE_GB:
        _notify(state, "disk", f"[ALERT] Low disk space: {free_gb:.2f} GB free")


def _check_memory(state: Dict[str, float]) -> None:
    meminfo = Path("/proc/meminfo").read_text(encoding="utf-8")
    info = {}
    for line in meminfo.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()
    free_kb = int(info.get("MemAvailable", "0").split()[0])
    free_mb = free_kb / 1024
    if free_mb < MEM_FREE_MB:
        _notify(state, "mem", f"[ALERT] Low memory: {free_mb:.0f} MB free")


def _check_load(state: Dict[str, float]) -> None:
    load1, _, _ = os.getloadavg()
    if load1 > LOAD1_MAX:
        _notify(state, "load", f"[ALERT] High load: {load1:.2f}")


def main() -> None:
    state = _load_state()
    _check_services(state)
    _check_ports(state)
    _check_disk(state)
    _check_memory(state)
    _check_load(state)
    _save_state(state)


if __name__ == "__main__":
    main()
