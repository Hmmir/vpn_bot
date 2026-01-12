import os


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
