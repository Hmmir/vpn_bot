from pathlib import Path
from typing import Optional

from aiogram.types import FSInputFile


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

ASSET_MAP = {
    "welcome": "welcome.png",
    "pricing": "pricing.png",
    "pro": "pro.png",
    "referral": "referral.png",
    "steps": "steps.png",
    "support": "support.png",
    "channel": "channel.png",
}


def asset_file(key: str) -> Optional[FSInputFile]:
    filename = ASSET_MAP.get(key)
    if not filename:
        return None
    path = ASSETS_DIR / filename
    if not path.exists():
        return None
    return FSInputFile(str(path))
