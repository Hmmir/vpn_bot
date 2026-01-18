from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..config import BOT_TOKEN, ADMIN_IDS


BASE_DIR = Path(__file__).resolve().parents[2]
STATE_FILE = BASE_DIR / "data" / "updatecheck_state.json"

COOLDOWN_HOURS = float(os.getenv("UPDATECHECK_COOLDOWN_HOURS", "24") or "24")
COOLDOWN_SECONDS = COOLDOWN_HOURS * 3600

VERSION_RE = re.compile(r"\b(\d+\.\d+\.\d+)\b")

REPOS = {
    "3x-ui": {
        "repo": "MHSanaei/3x-ui",
        "cmds": [
            ["x-ui", "version"],
            ["/usr/local/x-ui/x-ui", "version"],
            ["x-ui", "status"],
        ],
    },
    "xray": {
        "repo": "XTLS/Xray-core",
        "cmds": [
            ["xray", "-version"],
            ["/usr/local/x-ui/bin/xray-linux-amd64", "-version"],
            ["/usr/local/x-ui/bin/xray-linux-amd64", "version"],
        ],
    },
}


def _load_state() -> Dict[str, Dict[str, object]]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save_state(state: Dict[str, Dict[str, object]]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state), encoding="utf-8")


def _notify(message: str) -> None:
    if not BOT_TOKEN or not ADMIN_IDS:
        return
    for admin_id in ADMIN_IDS:
        params = urlencode({"chat_id": admin_id, "text": message})
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?{params}"
        try:
            with urlopen(url, timeout=10):
                pass
        except Exception:
            pass


def _fetch_latest(repo: str) -> tuple[Optional[str], str]:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = Request(url, headers={"User-Agent": "getnius-bot"})
    with urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    tag = data.get("tag_name") or data.get("name")
    return tag, data.get("html_url", url)


def _local_version(cmds: list[list[str]]) -> str:
    for cmd in cmds:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode != 0:
            continue
        combined = f"{result.stdout}\n{result.stderr}"
        match = VERSION_RE.search(combined)
        if match:
            return match.group(1)
    return "unknown"


def _should_notify(state: Dict[str, Dict[str, object]], key: str) -> bool:
    entry = state.get(key, {})
    last = float(entry.get("notified_at", 0) or 0)
    return (time.time() - last) > COOLDOWN_SECONDS


def main() -> None:
    state = _load_state()
    for name, meta in REPOS.items():
        try:
            latest, link = _fetch_latest(meta["repo"])
        except Exception:
            continue
        if not latest:
            continue
        entry = state.get(name, {})
        last_tag = entry.get("tag")
        if latest == last_tag:
            continue
        if not _should_notify(state, name):
            continue
        local = _local_version(meta["cmds"])
        _notify(
            f"[UPDATE] {name}: {latest} (local: {local})\n{link}"
        )
        state[name] = {"tag": latest, "notified_at": time.time()}
    _save_state(state)


if __name__ == "__main__":
    main()
