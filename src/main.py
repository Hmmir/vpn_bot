import asyncio
from typing import Dict

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .config import (
    BOT_TOKEN,
    BOT_USERNAME,
    ONE_CLICK_URL,
    V2RAY_URL,
    DEFAULT_KEY,
    SUBSCRIPTION_URL,
)
from .keyboards import (
    main_menu_kb,
    device_kb,
    android_actions_kb,
    v2ray_actions_kb,
    plans_kb,
    faq_kb,
)
from .texts import t
from .data import DEVICES_RU, DEVICES_EN


router = Router()
user_lang: Dict[int, str] = {}


def get_lang(user_id: int) -> str:
    return user_lang.get(user_id, "ru")


def set_lang(user_id: int, lang: str) -> None:
    user_lang[user_id] = lang


def get_user_key(_: int) -> str:
    return DEFAULT_KEY


def ref_link(user_id: int) -> str:
    username = BOT_USERNAME.lstrip("@")
    return f"https://t.me/{username}?start=ref_{user_id}"


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    await message.answer(
        t(lang, "welcome"),
        reply_markup=device_kb(lang),
    )
    await message.answer(t(lang, "menu_hint"), reply_markup=main_menu_kb(lang))


@router.message(F.text.in_(["Установить VPN", "Install VPN"]))
async def install_vpn(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    await message.answer(t(lang, "device_prompt"), reply_markup=device_kb(lang))


@router.message(F.text.in_(["Тарифы", "Plans"]))
async def show_tariffs(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    await message.answer(t(lang, "tariffs"), reply_markup=plans_kb(lang))


@router.message(F.text.in_(["Профиль", "Profile"]))
async def show_profile(message: Message) -> None:
    lang = get_lang(message.from_user.id)
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
    await message.answer(t(lang, "faq_main"), reply_markup=faq_kb(lang))


@router.message(F.text.in_(["Пригласить друга", "Invite a friend"]))
async def invite_friend(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    await message.answer(
        t(lang, "invite_friend", ref_link=ref_link(message.from_user.id))
    )


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
    await callback.message.answer(t(lang, "device_prompt"), reply_markup=device_kb(lang))
    await callback.answer()


@router.callback_query(F.data.startswith("device:"))
async def cb_device(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    code = callback.data.split(":", 1)[1]
    key = get_user_key(callback.from_user.id)
    if code == "android":
        one_click = SUBSCRIPTION_URL or ONE_CLICK_URL
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
    key = get_user_key(callback.from_user.id)
    one_click = SUBSCRIPTION_URL or V2RAY_URL
    await callback.message.answer(
        t(lang, "android_v2ray", key=key),
        reply_markup=v2ray_actions_kb(lang, one_click),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("faq:"))
async def cb_faq(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    code = callback.data.split(":", 1)[1]
    key = f"faq_{code}"
    text = t(lang, key)
    if not text:
        text = t(lang, "faq_main")
    await callback.message.answer(text)
    await callback.answer()


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
