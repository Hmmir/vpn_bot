import os

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


BOT_TOKEN = _get_env("BOT_TOKEN")
BRAND_NAME = _get_env("BRAND_NAME", "GetniusVPN")
BOT_USERNAME = _get_env("BOT_USERNAME", "@GetniusVPN_bot")
SUPPORT_BOT = _get_env("SUPPORT_BOT", "@GetniusSupport_bot")
CHANNEL = _get_env("CHANNEL", "@GetniusVPN")
BASE_URL = _get_env("BASE_URL", "https://example.com")
ONE_CLICK_URL = _get_env("ONE_CLICK_URL", "https://example.com/one-click")
V2RAY_URL = _get_env("V2RAY_URL", "https://example.com/v2ray")
PRIVACY_EMAIL = _get_env("PRIVACY_EMAIL", "support@example.com")
DEFAULT_KEY = _get_env("DEFAULT_KEY", "vless://REPLACE_ME")
SUBSCRIPTION_URL = _get_env("SUBSCRIPTION_URL", "https://example.com/sub/REPLACE_ME")
RENEW_URL = _get_env("RENEW_URL", "")

_admin_raw = _get_env("ADMIN_IDS", "")
ADMIN_IDS = {
    int(value)
    for value in _admin_raw.split(",")
    if value.strip().isdigit()
}

REMINDER_INTERVAL_MINUTES = int(_get_env("REMINDER_INTERVAL_MINUTES", "60") or "60")

SUPPORT_BOT_TOKEN = _get_env("SUPPORT_BOT_TOKEN", "")
_support_chat_raw = _get_env("SUPPORT_ADMIN_CHAT_ID", "")
SUPPORT_ADMIN_CHAT_ID = (
    int(_support_chat_raw) if _support_chat_raw.lstrip("-").isdigit() else None
)
_support_admin_raw = _get_env("SUPPORT_ADMIN_IDS", "")
SUPPORT_ADMIN_IDS = {
    int(value)
    for value in _support_admin_raw.split(",")
    if value.strip().lstrip("-").isdigit()
}
