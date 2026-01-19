from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from .config import CHANNEL, CHECK_URL, RENEW_URL, SUPPORT_BOT
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


def _check_button(lang: str) -> list[InlineKeyboardButton]:
    if not CHECK_URL:
        return []
    text = "Check connection" if lang == "en" else "Проверить соединение"
    return [InlineKeyboardButton(text=text, url=CHECK_URL)]


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
    return InlineKeyboardMarkup(inline_keyboard=rows)


def help_device_kb(lang: str) -> InlineKeyboardMarkup:
    rows = []
    devices = DEVICES_EN if lang == "en" else DEVICES_RU
    titles = {code: title for code, title in devices}
    order = ["android", "ios", "windows", "macos", "android_tv"]
    row = []
    for code in order:
        title = titles.get(code)
        if not title:
            continue
        row.append(InlineKeyboardButton(text=title, callback_data=f"device:{code}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def android_actions_kb(lang: str, one_click_url: str) -> InlineKeyboardMarkup:
    check_button = _check_button(lang)
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="Connect in 1 click!", url=one_click_url)],
            [InlineKeyboardButton(text="V2RayTUN", callback_data="android:v2ray")],
            [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Other devices", callback_data="menu")],
        ]
        if check_button:
            rows.insert(2, check_button)
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = [
        [InlineKeyboardButton(text="Подключиться в 1 клик!", url=one_click_url)],
        [InlineKeyboardButton(text="V2RayTUN", callback_data="android:v2ray")],
        [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
        [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
    ]
    if check_button:
        rows.insert(2, check_button)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def ios_actions_kb(lang: str, one_click_url: str) -> InlineKeyboardMarkup:
    check_button = _check_button(lang)
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="Connect in 1 click!", url=one_click_url)],
            [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Other devices", callback_data="menu")],
        ]
        if check_button:
            rows.insert(1, check_button)
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = [
        [InlineKeyboardButton(text="Подключиться в 1 клик!", url=one_click_url)],
        [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
        [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
    ]
    if check_button:
        rows.insert(1, check_button)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def desktop_actions_kb(lang: str, one_click_url: str) -> InlineKeyboardMarkup:
    check_button = _check_button(lang)
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="Connect in 1 click!", url=one_click_url)],
            [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Other devices", callback_data="menu")],
        ]
        if check_button:
            rows.insert(1, check_button)
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = [
        [InlineKeyboardButton(text="Подключиться в 1 клик!", url=one_click_url)],
        [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
        [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
    ]
    if check_button:
        rows.insert(1, check_button)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def macos_actions_kb(
    lang: str,
    one_click_url: str,
    singbox_url: str,
) -> InlineKeyboardMarkup:
    check_button = _check_button(lang)
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="Connect in 1 click!", url=one_click_url)],
        ]
        if singbox_url:
            rows.append([InlineKeyboardButton(text="Sing-box", url=singbox_url)])
        if check_button:
            rows.append(check_button)
        rows.extend(
            [
                [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
                [InlineKeyboardButton(text="Other devices", callback_data="menu")],
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = [
        [InlineKeyboardButton(text="Подключиться в 1 клик!", url=one_click_url)],
    ]
    if singbox_url:
        rows.append([InlineKeyboardButton(text="Sing-box", url=singbox_url)])
    if check_button:
        rows.append(check_button)
    rows.extend(
        [
            [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def android_tv_actions_kb(lang: str) -> InlineKeyboardMarkup:
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="V2RayTUN", callback_data="android:v2ray")],
            [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Other devices", callback_data="menu")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = [
        [InlineKeyboardButton(text="V2RayTUN", callback_data="android:v2ray")],
        [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
        [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def apple_tv_actions_kb(lang: str, singbox_url: str) -> InlineKeyboardMarkup:
    if lang == "en":
        rows = []
        if singbox_url:
            rows.append([InlineKeyboardButton(text="Sing-box", url=singbox_url)])
        rows.extend(
            [
                [InlineKeyboardButton(text="Something doesn't work", callback_data="faq:broken")],
                [InlineKeyboardButton(text="Other devices", callback_data="menu")],
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = []
    if singbox_url:
        rows.append([InlineKeyboardButton(text="Sing-box", url=singbox_url)])
    rows.extend(
        [
            [InlineKeyboardButton(text="Что-то не работает", callback_data="faq:broken")],
            [InlineKeyboardButton(text="Другие устройства", callback_data="menu")],
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def v2ray_actions_kb(lang: str, v2ray_url: str) -> InlineKeyboardMarkup:
    check_button = _check_button(lang)
    if lang == "en":
        rows = [
            [InlineKeyboardButton(text="Connect in 1 click!", url=v2ray_url)],
        ]
        if check_button:
            rows.append(check_button)
        rows.append([InlineKeyboardButton(text="Back", callback_data="device:android")])
        return InlineKeyboardMarkup(inline_keyboard=rows)
    rows = [
        [InlineKeyboardButton(text="Подключиться в 1 клик!", url=v2ray_url)],
    ]
    if check_button:
        rows.append(check_button)
    rows.append([InlineKeyboardButton(text="Назад", callback_data="device:android")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def plans_kb(lang: str) -> InlineKeyboardMarkup:
    rows = []
    for plan in PLANS:
        title = plan.title_en if lang == "en" else plan.title_ru
        price = plan.price_en if lang == "en" else plan.price_ru
        rows.append([InlineKeyboardButton(text=f"{title} — {price}", url=plan.pay_url)])
    support_url = _tg_url(SUPPORT_BOT)
    if support_url:
        text = "Payment issue" if lang == "en" else "Проблема с оплатой"
        rows.append([InlineKeyboardButton(text=text, url=support_url)])
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


def profile_actions_kb(
    lang: str,
    sub_url: str,
    check_url: str = CHECK_URL,
) -> InlineKeyboardMarkup:
    rows = []
    if lang == "en":
        rows.append([InlineKeyboardButton(text="Resend key", callback_data="profile:resend")])
        if sub_url:
            rows.append([InlineKeyboardButton(text="Switch server", url=sub_url)])
        if check_url:
            rows.append([InlineKeyboardButton(text="Check connection", url=check_url)])
    else:
        rows.append([InlineKeyboardButton(text="Отправить ключ", callback_data="profile:resend")])
        if sub_url:
            rows.append([InlineKeyboardButton(text="Переключить сервер", url=sub_url)])
        if check_url:
            rows.append([InlineKeyboardButton(text="Проверить соединение", url=check_url)])
    return InlineKeyboardMarkup(inline_keyboard=rows)
