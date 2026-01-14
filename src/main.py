import asyncio
from datetime import datetime, timedelta, timezone
import logging
from typing import Dict, Optional

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
)


router = Router()
user_lang: Dict[int, str] = {}
logging.basicConfig(level=logging.INFO)


def get_lang(user_id: int) -> str:
    return user_lang.get(user_id, "ru")


def set_lang(user_id: int, lang: str) -> None:
    user_lang[user_id] = lang
    upsert_user(user_id, lang)


def get_user_key(_: int) -> str:
    return DEFAULT_KEY


def ref_link(user_id: int) -> str:
    username = BOT_USERNAME.lstrip("@")
    return f"https://t.me/{username}?start=ref_{user_id}"


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


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
    await message.answer(
        t(
            lang,
            "profile",
            key=get_user_key(message.from_user.id),
            traffic="0.0 GB",
            expires="—",
            ref_link=ref_link(message.from_user.id),
        )
    )


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
    key = get_user_key(callback.from_user.id)
    if code == "android":
        one_click = SUBSCRIPTION_URL or ONE_CLICK_URL
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
    key = get_user_key(callback.from_user.id)
    one_click = SUBSCRIPTION_URL or V2RAY_URL
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
