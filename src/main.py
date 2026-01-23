import asyncio
from datetime import datetime, timedelta, timezone
import logging
from html import escape as html_escape
from typing import Dict, Optional
from urllib.parse import quote

from aiogram import Bot, Dispatcher, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from .config import (
    BOT_TOKEN,
    BOT_USERNAME,
    BRAND_NAME,
    DEEPLINK_REDIRECT_URL,
    ONE_CLICK_URL,
    V2RAY_URL,
    HAPP_URL,
    HAPP_APK_URL,
    HAPP_IOS_URL,
    HAPP_IOS_ALT_URL,
    V2RAYTUN_URL,
    FLCLASH_URL,
    V2RAYN_URL,
    V2RAYA_URL,
    IOS_V2RAYTUN_URL,
    SINGBOX_URL,
    ROUTER_URL,
    DEFAULT_KEY,
    SUBSCRIPTION_URL,
    ADMIN_IDS,
    REMINDER_INTERVAL_MINUTES,
    XUI_LIMIT_IP,
)
from .keyboards import (
    main_menu_kb,
    device_kb,
    help_device_kb,
    android_actions_kb,
    ios_actions_kb,
    desktop_actions_kb,
    macos_actions_kb,
    android_tv_actions_kb,
    apple_tv_actions_kb,
    v2ray_actions_kb,
    other_devices_kb,
    plans_kb,
    faq_kb,
    renew_kb,
    support_kb,
    channel_kb,
    profile_actions_kb,
)
from .texts import t
from .data import DEVICES_RU, DEVICES_EN, PLAN_DAYS, PLANS
from .media import asset_file
from .storage import (
    init_db,
    list_due_reminders,
    mark_reminded,
    set_status_expired,
    set_subscription,
    upsert_user,
    get_user_key as get_user_key_from_db,
    get_subscription,
    get_user_lang,
)
from .issue import issue_access, list_inbounds


router = Router()
user_lang: Dict[int, str] = {}
logging.basicConfig(level=logging.INFO)


def client_line(lang: str, device_code: str) -> str:
    if device_code == "ios":
        label = "V2RayTun (App Store)"
        url = IOS_V2RAYTUN_URL
    elif device_code == "windows":
        label = "v2rayN"
        url = V2RAYN_URL
    elif device_code in ("macos", "linux"):
        label = "v2rayA"
        url = V2RAYA_URL
    elif device_code == "android_tv":
        label = "Happ"
        url = HAPP_URL
    elif device_code == "apple_tv":
        label = "Настройка роутера" if lang != "en" else "Router setup"
        url = ROUTER_URL
    elif device_code == "router":
        label = "OpenWrt"
        url = ROUTER_URL
    else:
        label = ""
        url = ""
    if not url:
        return label
    sep = " — " if lang != "en" else " - "
    return f"{label}{sep}{url}"


def html_value(value: str) -> str:
    return html_escape(value or "")


def html_link(label: str, url: str) -> str:
    safe_label = html_escape(label or "")
    safe_url = html_escape(url or "")
    if not safe_url:
        return safe_label
    return f'<a href="{safe_url}">{safe_label}</a>'


def v2raytun_deeplink(sub_url: str) -> str:
    if not sub_url:
        return ""
    return f"v2raytun://import/{quote(sub_url, safe='')}"


def happ_deeplink(sub_url: str) -> str:
    if not sub_url:
        return ""
    return f"happ://add/{quote(sub_url, safe='')}"


def flclash_deeplink(sub_url: str) -> str:
    if not sub_url:
        return ""
    return f"flclash://install-config?url={quote(sub_url, safe='')}"


def redirect_deeplink(deeplink: str) -> str:
    if not deeplink:
        return ""
    if not DEEPLINK_REDIRECT_URL:
        return deeplink
    encoded = quote(deeplink, safe="")
    if "{url}" in DEEPLINK_REDIRECT_URL:
        return DEEPLINK_REDIRECT_URL.format(url=encoded)
    return f"{DEEPLINK_REDIRECT_URL}{encoded}"


def build_one_click_url(deeplink: str, fallback_url: str) -> str:
    if not deeplink:
        return fallback_url
    if deeplink.startswith(("http://", "https://")):
        return deeplink
    if not DEEPLINK_REDIRECT_URL:
        return fallback_url
    return redirect_deeplink(deeplink)


def happ_apk_suffix(lang: str) -> str:
    if not HAPP_APK_URL:
        return ""
    if lang == "en":
        return f" or APK file {HAPP_APK_URL}"
    return f" или «APK-файл» {HAPP_APK_URL}"


def happ_ios_alt_suffix(lang: str) -> str:
    if not HAPP_IOS_ALT_URL:
        return ""
    if lang == "en":
        return f" (Happ for other regions {HAPP_IOS_ALT_URL})"
    return f" (Happ для других регионов {HAPP_IOS_ALT_URL})"


def get_lang(user_id: int) -> str:
    if user_id not in user_lang:
        user_lang[user_id] = get_user_lang(user_id)
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


def format_expires(value: str) -> str:
    if not value:
        return "—"
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return value
    return parsed.strftime("%Y-%m-%d")


def format_plan(lang: str, code: str) -> str:
    if not code:
        return "—"
    for plan in PLANS:
        if plan.code == code:
            return plan.title_en if lang == "en" else plan.title_ru
    return code


def format_limit(lang: str) -> str:
    if XUI_LIMIT_IP <= 0:
        return "без ограничений" if lang != "en" else "no limit"
    return str(XUI_LIMIT_IP)


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


async def edit_asset_message(
    message: Message,
    key: str,
    caption: str,
    reply_markup=None,
) -> None:
    asset = asset_file(key)
    try:
        if message.photo:
            if asset:
                await message.edit_media(
                    InputMediaPhoto(media=asset, caption=caption),
                    reply_markup=reply_markup,
                )
            else:
                await message.edit_caption(caption=caption, reply_markup=reply_markup)
            return
        if asset:
            await message.answer_photo(asset, caption=caption, reply_markup=reply_markup)
            return
        await message.edit_text(caption, reply_markup=reply_markup)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc):
            raise


async def edit_text_message(
    message: Message,
    text: str,
    reply_markup=None,
    parse_mode: Optional[str] = None,
    disable_web_page_preview: Optional[bool] = None,
) -> None:
    try:
        if message.photo:
            await message.edit_caption(
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            return
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
        )
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc):
            raise


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await message.answer(t(lang, "welcome_text"), reply_markup=main_menu_kb(lang))
    await message.answer(t(lang, "device_prompt"), reply_markup=device_kb(lang))


@router.message(F.text.in_(["Установить VPN", "Install VPN"]))
async def install_vpn(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    await message.answer(t(lang, "device_prompt"), reply_markup=device_kb(lang))


@router.message(F.text.in_(["Тарифы", "Plans"]))
async def show_tariffs(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(message, "pro", t(lang, "pro_features"))
    await send_asset(
        message,
        "pricing",
        t(lang, "tariffs"),
        reply_markup=plans_kb(lang),
    )


@router.message(F.text.in_(["Профиль", "Profile"]))
async def show_profile(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    stored_key, stored_sub = get_user_key_from_db(message.from_user.id)
    if not stored_key:
        await message.answer(t(lang, "profile_empty"), reply_markup=plans_kb(lang))
        return
    subscription = get_subscription(message.from_user.id)
    plan = format_plan(lang, subscription.plan_code if subscription else "")
    expires_at = format_expires(subscription.expires_at if subscription else "")
    await message.answer(
        t(
            lang,
            "profile",
            key=stored_key,
            traffic="0.0 GB",
            expires=expires_at,
            plan=plan,
            limit=format_limit(lang),
            ref_link=ref_link(message.from_user.id),
        ),
        reply_markup=profile_actions_kb(lang, stored_sub),
    )
    if stored_sub:
        line = "Ссылка подписки:" if lang != "en" else "Subscription URL:"
        await message.answer(f"{line}\n{stored_sub}")


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
        t(lang, "support_text"),
        reply_markup=support_kb(lang),
    )


@router.message(F.text.in_(["Канал", "Channel"]))
async def show_channel(message: Message) -> None:
    lang = get_lang(message.from_user.id)
    upsert_user(message.from_user.id, lang)
    await send_asset(
        message,
        "channel",
        t(lang, "channel_text"),
        reply_markup=channel_kb(lang),
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
    upsert_user(callback.from_user.id, lang)
    await edit_text_message(
        callback.message,
        t(lang, "device_prompt"),
        reply_markup=device_kb(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("device:"))
async def cb_device(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    code = callback.data.split(":", 1)[1]
    stored_key, stored_sub = get_user_key_from_db(callback.from_user.id)
    if not stored_key:
        await edit_text_message(
            callback.message,
            t(lang, "paywall_device"),
            reply_markup=plans_kb(lang, include_menu=True),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        await callback.answer()
        return
    key = stored_key
    sub_url = stored_sub or SUBSCRIPTION_URL
    apk_suffix = happ_apk_suffix(lang)
    ios_alt_suffix = happ_ios_alt_suffix(lang)
    key_link = html_link(key, key)
    sub_url_link = html_link(sub_url, sub_url)
    happ_gp = html_link("Google Play", HAPP_URL)
    happ_apk = html_link("APK-файл", HAPP_APK_URL)
    happ_ios_ru = html_link("Happ", HAPP_IOS_URL)
    happ_ios_alt = html_link("Happ", HAPP_IOS_ALT_URL)
    flclash_link = html_link("FLClash", FLCLASH_URL)
    app_store_link = html_link("AppStore", HAPP_IOS_URL)
    brand_html = html_value(BRAND_NAME)
    if code == "android":
        one_click = build_one_click_url(
            happ_deeplink(sub_url),
            sub_url or ONE_CLICK_URL,
        )
        text = t(
            lang,
            "android_setup",
            key_link=key_link,
            happ_gp=happ_gp,
            happ_apk=happ_apk,
            happ_url=HAPP_URL,
            happ_apk_suffix=apk_suffix,
        )
        reply_markup = android_actions_kb(lang, one_click)
    elif code == "ios":
        one_click = build_one_click_url(
            happ_deeplink(sub_url),
            sub_url or ONE_CLICK_URL,
        )
        text = t(
            lang,
            "ios_setup",
            key_link=key_link,
            happ_ios_ru=happ_ios_ru,
            happ_ios_alt=happ_ios_alt,
            happ_ios_url=HAPP_IOS_URL,
            happ_ios_alt_suffix=ios_alt_suffix,
        )
        reply_markup = ios_actions_kb(lang, one_click)
    elif code == "windows":
        one_click = build_one_click_url(
            flclash_deeplink(sub_url),
            sub_url or ONE_CLICK_URL,
        )
        text = t(
            lang,
            "windows_setup",
            flclash_link=flclash_link,
            sub_url_link=sub_url_link,
            flclash_url=FLCLASH_URL,
            sub_url=sub_url,
        )
        reply_markup = desktop_actions_kb(lang, one_click)
    elif code == "macos":
        one_click = build_one_click_url(
            happ_deeplink(sub_url),
            sub_url or ONE_CLICK_URL,
        )
        text = t(
            lang,
            "macos_setup",
            key_link=key_link,
            happ_ios_ru=happ_ios_ru,
            happ_ios_alt=happ_ios_alt,
            happ_ios_url=HAPP_IOS_URL,
            happ_ios_alt_suffix=ios_alt_suffix,
        )
        reply_markup = macos_actions_kb(lang, one_click, SINGBOX_URL)
    elif code == "linux":
        one_click = build_one_click_url(
            flclash_deeplink(sub_url),
            sub_url or ONE_CLICK_URL,
        )
        flclash_link_linux = html_link("FL Clash", FLCLASH_URL)
        text = t(
            lang,
            "linux_setup",
            flclash_link=flclash_link_linux,
            sub_url_link=sub_url_link,
            flclash_url=FLCLASH_URL,
            sub_url=sub_url,
        )
        reply_markup = desktop_actions_kb(lang, one_click)
    elif code == "android_tv":
        text = t(
            lang,
            "android_tv_setup",
            happ_gp=happ_gp,
            happ_apk=happ_apk,
            happ_url=HAPP_URL,
            happ_apk_suffix=apk_suffix,
            brand=brand_html,
        )
        reply_markup = android_tv_actions_kb(lang)
    elif code == "apple_tv":
        text = t(
            lang,
            "apple_tv_setup",
            app_store_link=app_store_link,
            happ_ios_ru=happ_ios_ru,
            brand=brand_html,
        )
        reply_markup = apple_tv_actions_kb(lang, SINGBOX_URL)
    else:
        devices = DEVICES_EN if lang == "en" else DEVICES_RU
        device_title = dict(devices).get(code, code)
        text = t(
            lang,
            "generic_setup",
            device=device_title,
            client_line=client_line(lang, code),
        )
        reply_markup = other_devices_kb(lang)
    await edit_text_message(
        callback.message,
        text,
        reply_markup=reply_markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    await callback.answer()


@router.callback_query(F.data == "android:v2ray")
async def cb_android_v2ray(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    stored_key, stored_sub = get_user_key_from_db(callback.from_user.id)
    if not stored_key:
        await edit_text_message(
            callback.message,
            t(lang, "paywall_device"),
            reply_markup=plans_kb(lang, include_menu=True),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        await callback.answer()
        return
    sub_url = stored_sub or SUBSCRIPTION_URL
    deeplink = v2raytun_deeplink(sub_url)
    one_click = build_one_click_url(deeplink, V2RAY_URL or sub_url)
    sub_url_link = html_link(sub_url, sub_url)
    v2ray_gp = html_link("Google Play", V2RAYTUN_URL)
    v2ray_apk = html_link("APK-файл", V2RAYTUN_URL)
    await edit_text_message(
        callback.message,
        t(
            lang,
            "android_v2ray",
            sub_url_link=sub_url_link,
            v2ray_gp=v2ray_gp,
            v2ray_apk=v2ray_apk,
            v2raytun_url=V2RAYTUN_URL,
        ),
        reply_markup=v2ray_actions_kb(lang, one_click),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("faq:"))
async def cb_faq(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    code = callback.data.split(":", 1)[1]
    if code == "broken":
        await callback.message.answer(t(lang, "faq_broken"))
        await callback.message.answer(
            t(lang, "help_prompt"),
            reply_markup=help_device_kb(lang),
        )
        await callback.answer()
        return
    text = t(lang, f"faq_{code}")
    if not text:
        text = t(lang, "faq_main")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "tariffs")
async def cb_tariffs(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    await send_asset(callback.message, "pro", t(lang, "pro_features"))
    await send_asset(
        callback.message,
        "pricing",
        t(lang, "tariffs"),
        reply_markup=plans_kb(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "profile:resend")
async def cb_profile_resend(callback: CallbackQuery) -> None:
    lang = get_lang(callback.from_user.id)
    upsert_user(callback.from_user.id, lang)
    stored_key, stored_sub = get_user_key_from_db(callback.from_user.id)
    if not stored_key:
        await callback.message.answer(t(lang, "profile_empty"), reply_markup=plans_kb(lang))
        await callback.answer()
        return
    await callback.message.answer(stored_key)
    if stored_sub:
        line = "Ссылка подписки:" if lang != "en" else "Subscription URL:"
        await callback.message.answer(f"{line}\n{stored_sub}")
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
    items = await list_inbounds()
    if not items:
        await message.answer("Список inbound пуст или XUI не настроен.")
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
    try:
        key = await issue_access(user_id, plan_code)
    except Exception as exc:
        await message.answer(f"XUI ошибка: {exc}")
        return
    await message.answer(
        "Готово. Доступ выдан.\n\n"
        f"Ключ:\n{key.vless_uri}\n\n"
        f"Подписка:\n{key.sub_url}"
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
