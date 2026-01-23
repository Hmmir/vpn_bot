import asyncio
import hashlib
import hmac
import json
import logging
from typing import Any, Optional
from urllib.parse import unquote, urlparse

from aiohttp import web
from aiogram import Bot

from .config import BOT_TOKEN
from .issue import issue_access


logging.basicConfig(level=logging.INFO)

WEBHOOK_TOKEN = ""
WEBHOOK_BIND = "127.0.0.1"
WEBHOOK_PORT = 8080
ALLOWED_REDIRECT_SCHEMES = {"happ", "v2raytun", "flclash"}
TRIBUTE_API_KEY = ""
TRIBUTE_DEFAULT_PLAN = "trial"
TRIBUTE_PRODUCT_MAP: dict[str, str] = {}


def load_env() -> None:
    global WEBHOOK_TOKEN, WEBHOOK_BIND, WEBHOOK_PORT
    global TRIBUTE_API_KEY, TRIBUTE_DEFAULT_PLAN, TRIBUTE_PRODUCT_MAP
    from .config import _get_env  # local import to avoid circular init

    WEBHOOK_TOKEN = _get_env("WEBHOOK_TOKEN", "")
    WEBHOOK_BIND = _get_env("WEBHOOK_BIND", "127.0.0.1")
    WEBHOOK_PORT = int(_get_env("WEBHOOK_PORT", "8080") or "8080")
    TRIBUTE_API_KEY = _get_env("TRIBUTE_API_KEY", "")
    TRIBUTE_DEFAULT_PLAN = _get_env("TRIBUTE_DEFAULT_PLAN", "trial") or "trial"
    TRIBUTE_PRODUCT_MAP = _parse_plan_map(_get_env("TRIBUTE_PRODUCT_MAP", ""))


def _parse_plan_map(raw: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for part in (raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        key, sep, value = part.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if key and value:
            mapping[key] = value
    return mapping


def _verify_tribute_signature(raw: bytes, signature: str) -> bool:
    if not TRIBUTE_API_KEY:
        return True
    if not signature:
        return False
    expected = hmac.new(TRIBUTE_API_KEY.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def _extract_tribute_user_id(payload: dict[str, Any]) -> Optional[int]:
    for key in ("telegram_user_id", "telegramUserId", "telegram_user", "user_id"):
        value = payload.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def extract_tribute_payment(data: dict[str, Any]) -> tuple[Optional[int], str]:
    payload = data.get("payload") if isinstance(data.get("payload"), dict) else {}
    user_id = _extract_tribute_user_id(payload) or _extract_tribute_user_id(data)
    product_id = (
        payload.get("product_id")
        or payload.get("digital_product_id")
        or payload.get("product")
        or data.get("product_id")
    )
    plan_code = TRIBUTE_PRODUCT_MAP.get(str(product_id), TRIBUTE_DEFAULT_PLAN)
    return user_id, plan_code


def extract_payment(data: dict[str, Any]) -> Optional[tuple[int, str]]:
    if "user_id" in data and "plan" in data:
        return int(data["user_id"]), str(data["plan"])
    if "metadata" in data and isinstance(data["metadata"], dict):
        meta = data["metadata"]
        if "user_id" in meta and "plan" in meta:
            return int(meta["user_id"]), str(meta["plan"])
    obj = data.get("object", {})
    if isinstance(obj, dict):
        meta = obj.get("metadata", {})
        if isinstance(meta, dict) and "user_id" in meta and "plan" in meta:
            return int(meta["user_id"]), str(meta["plan"])
    return None


def is_success_event(data: dict[str, Any]) -> bool:
    event = str(data.get("event", "")).lower()
    if not event:
        return True
    return "succeed" in event or "paid" in event


async def handle_payment(request: web.Request) -> web.Response:
    token = request.headers.get("X-Webhook-Token") or request.query.get("token", "")
    if WEBHOOK_TOKEN and token != WEBHOOK_TOKEN:
        return web.json_response({"ok": False, "error": "unauthorized"}, status=401)
    data = await request.json()
    if not is_success_event(data):
        return web.json_response({"ok": True, "ignored": True})
    extracted = extract_payment(data)
    if not extracted:
        return web.json_response({"ok": False, "error": "missing user_id/plan"}, status=400)
    user_id, plan_code = extracted
    try:
        key = await issue_access(user_id, plan_code)
    except Exception as exc:
        logging.exception("Issue access failed")
        return web.json_response({"ok": False, "error": str(exc)}, status=500)

    if BOT_TOKEN:
        bot = Bot(BOT_TOKEN)
        await bot.send_message(
            user_id,
            "Оплата подтверждена. Вот ваш доступ:\n\n"
            f"Ключ:\n{key.vless_uri}\n\n"
            f"Подписка:\n{key.sub_url}\n\n"
            "Нажмите на ключ, чтобы скопировать.",
        )
        await bot.session.close()

    return web.json_response({"ok": True})


async def handle_tribute(request: web.Request) -> web.Response:
    raw = await request.read()
    signature = request.headers.get("trbt-signature", "")
    if not _verify_tribute_signature(raw, signature):
        return web.json_response({"ok": False, "error": "unauthorized"}, status=401)
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return web.json_response({"ok": False, "error": "invalid json"}, status=400)

    user_id, plan_code = extract_tribute_payment(data)
    if not user_id:
        return web.json_response({"ok": False, "error": "missing telegram_user_id"}, status=400)
    try:
        key = await issue_access(user_id, plan_code)
    except Exception as exc:
        logging.exception("Issue access failed")
        return web.json_response({"ok": False, "error": str(exc)}, status=500)

    if BOT_TOKEN:
        bot = Bot(BOT_TOKEN)
        await bot.send_message(
            user_id,
            "گ?گُگ>گّ‘'گّ گُگ?গ?‘'گ?গç‘?گگ?گçগ?গّ. گ'গ?‘' গ?গّ‘? গ?গ?‘?‘'‘?गُ:\n\n"
            f"گ?গ>‘?‘ط:\n{key.vless_uri}\n\n"
            f"گ?گ?গ?গُগٌ‘?গَগّ:\n{key.sub_url}\n\n"
            "گ?গّগग?গٌ‘'গç গ?গّ گَগ>‘?‘ط, ‘ط‘'গ?গ+‘< ‘?গَগ?গُগٌ‘?গ?গ?গّ‘'‘?.",
        )
        await bot.session.close()

    return web.json_response({"ok": True})


def _is_allowed_redirect(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in ALLOWED_REDIRECT_SCHEMES


async def handle_redirect(request: web.Request) -> web.Response:
    target = request.query.get("url", "")
    if not target:
        return web.json_response({"ok": False, "error": "missing url"}, status=400)
    target = unquote(target)
    if not _is_allowed_redirect(target):
        return web.json_response({"ok": False, "error": "invalid scheme"}, status=400)
    raise web.HTTPFound(location=target)


async def init_app() -> web.Application:
    load_env()
    app = web.Application()
    app.router.add_get("/api/v1/redirect_dl", handle_redirect)
    app.router.add_post("/payment/paid", handle_payment)
    app.router.add_post("/payment/tribute", handle_tribute)
    return app


def main() -> None:
    app = asyncio.run(init_app())
    web.run_app(app, host=WEBHOOK_BIND, port=WEBHOOK_PORT)


if __name__ == "__main__":
    main()
