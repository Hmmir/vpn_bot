import asyncio
from datetime import datetime, timedelta, timezone
import logging
from typing import Dict, Optional
import uuid

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from .config import (
    BOT_TOKEN,
    BOT_USERNAME,
    ONE_CLICK_URL,
    V2RAY_URL,
    DEFAULT_KEY,
    SUBSCRIPTION_URL,
    ADMIN_IDS,
    REMINDER_INTERVAL_MINUTES,
    XUI_BASE_URL,
    XUI_USERNAME,
    XUI_PASSWORD,
    XUI_API_PATH,
    XUI_INBOUND_ID,
    XUI_FLOW,
    XUI_TOTAL_GB,
    XUI_LIMIT_IP,
    XUI_PUBLIC_HOST,
    XUI_PUBLIC_PORT,
    XUI_SUB_BASE_URL,
    XUI_SSL_VERIFY,
)
from .keyboards import (
    main_menu_kb,
    device_kb,
    android_actions_kb,
    v2ray_actions_kb,
    plans_kb,
    faq_kb,
    renew_kb,
    support_kb,
    channel_kb,
)
from .texts import t
from .data import DEVICES_RU, DEVICES_EN, PLAN_DAYS
from .media import asset_file
from .storage import (
    init_db,
    list_due_reminders,
    mark_reminded,
    set_status_expired,
    set_subscription,
    upsert_user,
    get_user_key as get_user_key_from_db,
    set_user_key,
)
from .xui_api import XuiApi, build_vless_uri, build_sub_url


router = Router()
user_lang: Dict[int, str] = {}
logging.basicConfig(level=logging.INFO)
xui_client: Optional[XuiApi] = None


def get_lang(user_id: int) -> str:
    return user_lang.get(user_id, "ru")


def set_lang(user_id: int, lang: str) -> None:
    user_lang[user_id] = lang
    upsert_user(user_id, lang)


def get_user_key(user_id: int) -> tuple[str, str]:
    stored_key, stored_sub = get_user_key_from_db(user_id)
    key = stored_key or DEFAULT_KEY
    sub = stored_sub or SUBSCRIPTION_URL
    return key, sub


def ref_link(user_id: int) -> str:
    username = BOT_USERNAME.lstrip("@")
    return f"https://t.me/{username}?start=ref_{user_id}"


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def _parse_inbound_id(value: str) -> Optional[int]:
    return int(value) if value.strip().isdigit() else None


def _public_port() -> Optional[int]:
    if not XUI_PUBLIC_PORT:
        return None
    if XUI_PUBLIC_PORT.strip().isdigit():
        return int(XUI_PUBLIC_PORT.strip())
    return None


def _public_host() -> str:
    if XUI_PUBLIC_HOST:
        return XUI_PUBLIC_HOST
    if XUI_BASE_URL.startswith("http"):
        return XUI_BASE_URL.split("://", 1)[1].split(":", 1)[0]
    return ""


async def ensure_xui() -> Optional[XuiApi]:
    global xui_client
    if xui_client:
        return xui_client
    if not (XUI_BASE_URL and XUI_USERNAME and XUI_PASSWORD):
        return None
    xui_client = XuiApi(
        XUI_BASE_URL,
        XUI_USERNAME,
        XUI_PASSWORD,
        api_path=XUI_API_PATH or "/panel/api",
        verify_ssl=XUI_SSL_VERIFY,
    )
    return xui_client


async def send_asset(
    message: Message,
    key: str,
    caption: Optional[str] = None,
    reply_markup=None,
) -> None:
    asset = asset_file(key)
    if asset:
        await message.answer_photo(asset, caption=caption, reply_markup=reply_markup)
        return
    if caption:
        await message.answer(caption, reply_markup=reply_markup)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(message, "welcome", t(lang, "welcome_banner"))
    await message.answer(t(lang, "welcome_text"), reply_markup=device_kb(lang))
    await message.answer(t(lang, "menu_hint"), reply_markup=main_menu_kb(lang))


@router.message(F.text.in_(["Установить VPN", "Install VPN"]))
async def install_vpn(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    await message.answer(t(lang, "device_prompt"), reply_markup=device_kb(lang))


@router.message(F.text.in_(["Тарифы", "Plans"]))
async def show_tariffs(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(message, "pricing", t(lang, "tariffs_banner"))
    await message.answer(t(lang, "tariffs"), reply_markup=plans_kb(lang))
    await send_asset(message, "pro", t(lang, "pro_features"))


@router.message(F.text.in_(["Профиль", "Profile"]))
async def show_profile(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    key, sub_url = get_user_key(message.from_user.id)
    await message.answer(
        t(
            lang,
            "profile",
            key=key,
            traffic="0.0 GB",
            expires="—",
            ref_link=ref_link(message.from_user.id),
        )
    )
    if sub_url:
        line = "Ссылка подписки:" if lang != "en" else "Subscription URL:"
        await message.answer(f"{line}\n{sub_url}")


@router.message(F.text.in_(["Вопросы", "Questions"]))
async def show_faq(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await message.answer(t(lang, "faq_main"), reply_markup=faq_kb(lang))


@router.message(F.text.in_(["Пригласить друга", "Invite a friend"]))
async def invite_friend(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(message, "referral", t(lang, "referral_banner"))
    await message.answer(
        t(lang, "invite_friend", ref_link=ref_link(message.from_user.id))
    )


@router.message(F.text.in_(["Поддержка", "Support"]))
async def show_support(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(
        message,
        "support",
        t(lang, "support_banner"),
        reply_markup=support_kb(lang),
    )
    await message.answer(t(lang, "support_text"), reply_markup=support_kb(lang))


@router.message(F.text.in_(["Канал", "Channel"]))
async def show_channel(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(
        message,
        "channel",
        t(lang, "channel_banner"),
        reply_markup=channel_kb(lang),
    )
    await message.answer(t(lang, "channel_text"), reply_markup=channel_kb(lang))


@router.message(F.text == "Switch to English")
async def switch_to_english(message: Message) -> None:
    set_lang(message.from_user.id, "en")
    await message.answer(t("en", "lang_switched"), reply_markup=main_menu_kb("en"))


@router.message(F.text == "Switch to Russian")
async def switch_to_russian(message: Message) -> None:
    set_lang(message.from_user.id, "ru")
    await message.answer(t("ru", "lang_switched"), reply_markup=main_menu_kb("ru"))


@router.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    await callback.message.answer(t(lang, "device_prompt"), reply_markup=device_kb(lang))
    await callback.answer()


@router.callback_query(F.data.startswith("device:"))
async def cb_device(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    code = callback.data.split(":", 1)[1]
    key, sub_url = get_user_key(callback.from_user.id)
    if code == "android":
        one_click = sub_url or SUBSCRIPTION_URL or ONE_CLICK_URL
        await send_asset(callback.message, "steps", t(lang, "steps_banner"))
        await callback.message.answer(
            t(lang, "android_setup", key=key),
            reply_markup=android_actions_kb(lang, one_click),
        )
    else:
        devices = DEVICES_EN if lang == "en" else DEVICES_RU
        device_title = dict(devices).get(code, code)
        await callback.message.answer(
            t(lang, "generic_setup", device=device_title),
        )
    await callback.answer()


@router.callback_query(F.data == "android:v2ray")
async def cb_android_v2ray(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    key, sub_url = get_user_key(callback.from_user.id)
    one_click = sub_url or SUBSCRIPTION_URL or V2RAY_URL
    await send_asset(callback.message, "steps", t(lang, "steps_banner"))
    await callback.message.answer(
        t(lang, "android_v2ray", key=key),
        reply_markup=v2ray_actions_kb(lang, one_click),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("faq:"))
async def cb_faq(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    code = callback.data.split(":", 1)[1]
    key = f"faq_{code}"
    text = t(lang, key)
    if not text:
        text = t(lang, "faq_main")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "tariffs")
async def cb_tariffs(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    await send_asset(callback.message, "pricing", t(lang, "tariffs_banner"))
    await callback.message.answer(t(lang, "tariffs"), reply_markup=plans_kb(lang))
    await send_asset(callback.message, "pro", t(lang, "pro_features"))
    await callback.answer()


@router.message(Command("set_expire"))
async def set_expire_cmd(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) < 3:
        await message.answer("Формат: /set_expire USER_ID YYYY-MM-DD [HH:MM]")
        return
    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("USER_ID должен быть числом.")
        return
    date_str = " ".join(parts[2:])
    expires = None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M"):
        try:
            expires = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            break
        except ValueError:
            continue
    if not expires:
        await message.answer(
            "Неверный формат даты. Пример: 2026-01-20 или 2026-01-20 12:00"
        )
        return
    set_subscription(user_id, expires.isoformat(timespec="seconds"))
    await message.answer(
        f"Готово. Подписка до {expires.isoformat(timespec='minutes')}."
    )


@router.message(Command("set_plan"))
async def set_plan_cmd(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) < 3:
        await message.answer("Формат: /set_plan USER_ID trial|1m|3m|12m")
        return
    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("USER_ID должен быть числом.")
        return
    plan_code = parts[2]
    days = PLAN_DAYS.get(plan_code)
    if not days:
        await message.answer("План должен быть trial, 1m, 3m или 12m.")
        return
    expires = datetime.now(timezone.utc) + timedelta(days=days)
    set_subscription(user_id, expires.isoformat(timespec="seconds"), plan_code=plan_code)
    await message.answer(
        f"Готово. План {plan_code}, до {expires.isoformat(timespec='minutes')}."
    )


@router.message(Command("xui_inbounds"))
async def xui_inbounds_cmd(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    xui = await ensure_xui()
    if not xui:
        await message.answer("XUI не настроен. Проверьте XUI_BASE_URL и учетные данные.")
        return
    items = await xui.list_inbounds()
    if not items:
        await message.answer("Список инбаундов пуст.")
        return
    lines = ["Inbounds:"]
    for inbound in items:
        inbound_id = inbound.get("id")
        remark = inbound.get("remark") or ""
        port = inbound.get("port") or ""
        protocol = inbound.get("protocol") or ""
        lines.append(f"{inbound_id} | {protocol} | {port} | {remark}")
    await message.answer("\n".join(lines))


@router.message(Command("issue"))
async def issue_cmd(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) < 3:
        await message.answer("Формат: /issue USER_ID trial|1m|3m|12m")
        return
    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("USER_ID должен быть числом.")
        return
    plan_code = parts[2]
    days = PLAN_DAYS.get(plan_code)
    if not days:
        await message.answer("План должен быть trial, 1m, 3m или 12m.")
        return
    inbound_id = _parse_inbound_id(XUI_INBOUND_ID)
    if inbound_id is None:
        await message.answer("XUI_INBOUND_ID не задан.")
        return
    xui = await ensure_xui()
    if not xui:
        await message.answer("XUI не настроен. Проверьте XUI_BASE_URL и учетные данные.")
        return

    expires = datetime.now(timezone.utc) + timedelta(days=days)
    expiry_ms = int(expires.timestamp() * 1000)
    client_id = str(uuid.uuid4())
    email = f"tg_{user_id}"
    sub_id = uuid.uuid4().hex[:16]
    client_settings = {
        "id": client_id,
        "email": email,
        "limitIp": XUI_LIMIT_IP,
        "totalGB": XUI_TOTAL_GB,
        "expiryTime": expiry_ms,
        "enable": True,
        "flow": XUI_FLOW or None,
        "tgId": str(user_id),
        "subId": sub_id,
    }
    # Remove None values to keep payload clean.
    client_settings = {k: v for k, v in client_settings.items() if v is not None}
    result = await xui.add_client(inbound_id, client_settings)
    if not result.get("success"):
        await message.answer(f"XUI ошибка: {result}")
        return
    inbound = await xui.get_inbound(inbound_id)
    if not inbound:
        await message.answer("Не удалось получить inbound для сборки ссылки.")
        return
    host = _public_host()
    port = _public_port()
    vless_uri = build_vless_uri(
        inbound,
        client_id,
        email,
        host=host,
        flow=XUI_FLOW,
        public_port=port,
    )
    sub_url = build_sub_url(XUI_SUB_BASE_URL or XUI_BASE_URL, sub_id)
    set_user_key(user_id, vless_uri, sub_url, client_id, email, sub_id)
    set_subscription(user_id, expires.isoformat(timespec="seconds"), plan_code=plan_code)
    await message.answer(
        "Готово. Доступ выдан.\n\n"
        f"Ключ:\n{vless_uri}\n\n"
        f"Подписка:\n{sub_url}"
    )


async def reminder_loop(bot: Bot) -> None:
    while True:
        now = datetime.now(timezone.utc)
        for reminder in list_due_reminders(now):
            key = f"renew_{reminder.kind}"
            text = t(reminder.lang, key)
            if reminder.kind == "expired":
                set_status_expired(reminder.user_id)
            try:
                await bot.send_message(
                    reminder.user_id,
                    text,
                    reply_markup=renew_kb(reminder.lang),
                )
                mark_reminded(reminder.user_id, reminder.kind)
            except Exception:
                logging.exception("Failed to send reminder to %s", reminder.user_id)
        await asyncio.sleep(REMINDER_INTERVAL_MINUTES * 60)


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    init_db()
    asyncio.create_task(reminder_loop(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
