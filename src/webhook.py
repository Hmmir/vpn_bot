import asyncio
import logging
from typing import Any, Optional

from aiohttp import web
from aiogram import Bot

from .config import BOT_TOKEN
from .issue import issue_access


logging.basicConfig(level=logging.INFO)

WEBHOOK_TOKEN = ""
WEBHOOK_BIND = "127.0.0.1"
WEBHOOK_PORT = 8080


def load_env() -> None:
    global WEBHOOK_TOKEN, WEBHOOK_BIND, WEBHOOK_PORT
    from .config import _get_env  # local import to avoid circular init

    WEBHOOK_TOKEN = _get_env("WEBHOOK_TOKEN", "")
    WEBHOOK_BIND = _get_env("WEBHOOK_BIND", "127.0.0.1")
    WEBHOOK_PORT = int(_get_env("WEBHOOK_PORT", "8080") or "8080")


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


async def init_app() -> web.Application:
    load_env()
    app = web.Application()
    app.router.add_post("/payment/paid", handle_payment)
    return app


def main() -> None:
    app = asyncio.run(init_app())
    web.run_app(app, host=WEBHOOK_BIND, port=WEBHOOK_PORT)


if __name__ == "__main__":
    main()
