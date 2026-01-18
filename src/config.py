import os

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


BOT_TOKEN = _get_env("BOT_TOKEN")
BRAND_NAME = _get_env("BRAND_NAME", "Lagom VPN Pro")
BOT_USERNAME = _get_env("BOT_USERNAME", "@lagvpnbot")
SUPPORT_BOT = _get_env("SUPPORT_BOT", "@GetniusSupport_bot")
CHANNEL = _get_env("CHANNEL", "https://t.me/genialvpn")
BASE_URL = _get_env("BASE_URL", "https://example.com")
ONE_CLICK_URL = _get_env("ONE_CLICK_URL", "https://example.com/one-click")
V2RAY_URL = _get_env("V2RAY_URL", "https://example.com/v2ray")
CHECK_URL = _get_env("CHECK_URL", "https://check-host.net/check-ping")
HAPP_URL = _get_env(
    "HAPP_URL",
    "https://play.google.com/store/apps/details?id=com.happproxy",
)
V2RAYTUN_URL = _get_env(
    "V2RAYTUN_URL",
    "https://play.google.com/store/apps/details?id=com.v2raytun.android",
)
V2RAYN_URL = _get_env(
    "V2RAYN_URL",
    "https://github.com/2dust/v2rayN/releases",
)
IOS_V2RAYTUN_URL = _get_env(
    "IOS_V2RAYTUN_URL",
    "https://apps.apple.com/us/app/v2raytun/id6476628951",
)
ROUTER_URL = _get_env("ROUTER_URL", "https://openwrt.org/")
PRIVACY_EMAIL = _get_env("PRIVACY_EMAIL", "support@example.com")
DEFAULT_KEY = _get_env("DEFAULT_KEY", "vless://REPLACE_ME")
SUBSCRIPTION_URL = _get_env("SUBSCRIPTION_URL", "https://example.com/sub/REPLACE_ME")
RENEW_URL = _get_env("RENEW_URL", "")
XUI_BASE_URL = _get_env("XUI_BASE_URL", "")
XUI_USERNAME = _get_env("XUI_USERNAME", "")
XUI_PASSWORD = _get_env("XUI_PASSWORD", "")
XUI_API_PATH = _get_env("XUI_API_PATH", "/panel/api")
XUI_INBOUND_IDS = _get_env("XUI_INBOUND_IDS", "")
XUI_INBOUND_ID = _get_env("XUI_INBOUND_ID", "")
XUI_FLOW = _get_env("XUI_FLOW", "")
XUI_TOTAL_GB = int(_get_env("XUI_TOTAL_GB", "0") or "0")
XUI_LIMIT_IP = int(_get_env("XUI_LIMIT_IP", "0") or "0")
XUI_PUBLIC_HOST = _get_env("XUI_PUBLIC_HOST", "")
XUI_PUBLIC_PORT = _get_env("XUI_PUBLIC_PORT", "")
XUI_SUB_BASE_URL = _get_env("XUI_SUB_BASE_URL", "")
XUI_SSL_VERIFY = _get_env("XUI_SSL_VERIFY", "true").lower() not in ("0", "false", "no")
XUI_TIMEOUT_SECONDS = float(_get_env("XUI_TIMEOUT_SECONDS", "10") or "10")

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
