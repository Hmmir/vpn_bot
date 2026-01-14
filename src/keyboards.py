from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from .config import CHANNEL, RENEW_URL, SUPPORT_BOT
from .data import DEVICES_EN, DEVICES_RU, PLANS


def _tg_url(handle: str) -> str:
    value = (handle or "").strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith("@"):
        return f"https://t.me/{value[1:]}"
    return f"https://t.me/{value}"


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    if lang == "en":
        buttons = [
            ["Install VPN", "Plans"],
            ["Profile", "Questions"],
            ["Invite a friend", "Channel"],
            ["Support", "Switch to Russian"],
        ]
    else:
        buttons = [
            ["Установить VPN", "Тарифы"],
            ["Профиль", "Вопросы"],
            ["Пригласить друга", "Канал"],
            ["Поддержка", "Switch to English"],
        ]
    keyboard = [[KeyboardButton(text=text) for text in row] for row in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def device_kb(lang: str) -> InlineKeyboardMarkup:
    rows = []
    devices = DEVICES_EN if lang == "en" else DEVICES_RU
    row = []
    for code, title in devices:
        row.append(InlineKeyboardButton(text=title, callback_data=f"device:{code}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    if lang == "en":
        rows.append([InlineKeyboardButton(text="Back to menu", callback_data="menu")])
    else:
        rows.append([InlineKeyboardButton(text="Назад", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def android_actions_kb(lang: str, one_click_url: str) -> InlineKeyboardMarkup:
    if lang == "en":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Connect in 1 click", url=one_click_url)],
                [InlineKeyboardButton(text="V2RayTUN", callback_data="android:v2ray")],
                [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
                [InlineKeyboardButton(text="Other devices", callback_data="menu")],
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подключиться в 1 клик!", url=one_click_url)],
            [InlineKeyboardButton(text="V2RayTUN", callback_data="android:v2ray")],
            [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
        ]
    )


def v2ray_actions_kb(lang: str, v2ray_url: str) -> InlineKeyboardMarkup:
    if lang == "en":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Connect in 1 click", url=v2ray_url)],
                [InlineKeyboardButton(text="Back", callback_data="device:android")],
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подключиться в 1 клик!", url=v2ray_url)],
            [InlineKeyboardButton(text="Назад", callback_data="device:android")],
        ]
    )


def plans_kb(lang: str) -> InlineKeyboardMarkup:
    rows = []
    for plan in PLANS:
        title = plan.title_en if lang == "en" else plan.title_ru
        price = plan.price_en if lang == "en" else plan.price_ru
        rows.append([InlineKeyboardButton(text=f"{title} — {price}", url=plan.pay_url)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def faq_kb(lang: str) -> InlineKeyboardMarkup:
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="PRO questions", callback_data="faq:pro")],
            [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
            [InlineKeyboardButton(text="About the service", callback_data="faq:about")],
            [InlineKeyboardButton(text="Jobs", callback_data="faq:jobs")],
            [InlineKeyboardButton(text="Support", callback_data="faq:support")],
            [InlineKeyboardButton(text="Cancel subscription", callback_data="faq:cancel")],
        ]
    else:
        rows = [
            [InlineKeyboardButton(text="Вопросы о PRO", callback_data="faq:pro")],
            [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
            [InlineKeyboardButton(text="О сервисе", callback_data="faq:about")],
            [InlineKeyboardButton(text="Вакансии", callback_data="faq:jobs")],
            [InlineKeyboardButton(text="Тех. поддержка", callback_data="faq:support")],
            [InlineKeyboardButton(text="Отменить подписку", callback_data="faq:cancel")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def renew_kb(lang: str) -> InlineKeyboardMarkup:
    text = "Renew" if lang == "en" else "Продлить"
    if RENEW_URL:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=text, url=RENEW_URL)]]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data="tariffs")]]
    )


def support_kb(lang: str) -> InlineKeyboardMarkup | None:
    url = _tg_url(SUPPORT_BOT)
    if not url:
        return None
    text = "Contact support" if lang == "en" else "Написать в поддержку"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]]
    )


def channel_kb(lang: str) -> InlineKeyboardMarkup | None:
    url = _tg_url(CHANNEL)
    if not url:
        return None
    text = "Open channel" if lang == "en" else "Открыть канал"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]]
    )
