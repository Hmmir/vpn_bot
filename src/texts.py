from typing import Dict

from .config import (
    BRAND_NAME,
    BOT_USERNAME,
    SUPPORT_BOT,
    CHANNEL,
    ONE_CLICK_URL,
    V2RAY_URL,
    PRIVACY_EMAIL,
)
from .data import TRIAL_DAYS, TRIAL_PRICE_RUB


def _fmt(text: str, **kwargs: str) -> str:
    return text.format(**kwargs)


RU: Dict[str, str] = {
    "welcome_banner": "Привет! Подключи VPN за 1 минуту.",
    "welcome_text": (
        "{brand} - быстрый и безопасный VPN на протоколе VLESS.\n"
        "Просто вставьте ключ в приложение и выберите локацию.\n\n"
        "Выберите ваше устройство:"
    ),
    "device_prompt": "Выберите устройство:",
    "steps_banner": "Подключение в 3 шага",
    "android_setup": (
        "Для настройки VPN на Android:\n"
        "1. Установите Happ из Google Play или APK.\n"
        "2. Нажмите кнопку ниже, чтобы подключиться в 1 клик.\n\n"
        "Если автоматическая настройка не сработала:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key}\n"
        "2. Откройте Happ и нажмите «Вставить/Из буфера».\n"
        "3. Выберите локацию и подключитесь.\n\n"
        "Если приложение не работает, попробуйте V2RayTUN."
    ),
    "android_v2ray": (
        "Для настройки VPN через V2RayTUN:\n"
        "1. Установите V2RayTUN из Google Play или APK.\n"
        "2. Нажмите кнопку ниже, чтобы подключиться в 1 клик.\n\n"
        "Если автоматическая настройка не сработала:\n"
        "1. Скопируйте ключ:\n"
        "{key}\n"
        "2. Откройте V2RayTUN, нажмите «+» -> «Импорт из буфера».\n"
        "3. Выберите локацию и подключитесь."
    ),
    "generic_setup": (
        "Для настройки VPN на {device}:\n"
        "1. Установите клиент с поддержкой VLESS.\n"
        "2. Вставьте ключ в приложение.\n"
        "3. Выберите локацию и подключитесь.\n\n"
        "Альтернативные клиенты: Happ / V2RayTUN.\n"
        "Нужна помощь? Напишите в поддержку: {support}."
    ),
    "tariffs_banner": "Тарифы GetniusVPN",
    "tariffs": (
        "Тарифы:\n"
        "- 1 мес: 100 руб\n"
        "- 3 мес: 270 руб\n"
        "- 12 мес: 960 руб\n\n"
        f"Пробный период: {TRIAL_PRICE_RUB} за {TRIAL_DAYS} дня.\n"
        "PRO включает все функции и максимальную скорость.\n"
        "Если оплата прошла, а ключ не пришёл — напишите в поддержку."
    ),
    "pro_features": (
        "PRO-функции:\n"
        "- Безопасность и шифрование\n"
        "- Высокая скорость\n"
        "- До 10 устройств\n"
        "- Блокировка рекламы"
    ),
    "profile": (
        "Вы используете {brand}\n\n"
        "Ваш ключ:\n"
        "{key}\n"
        "Нажмите на ключ, чтобы скопировать.\n\n"
        "Тариф: {plan}\n"
        "Лимит устройств: {limit}\n"
        "Потребление трафика: {traffic}\n"
        "Действует до: {expires}\n\n"
        "Получите +1 месяц за каждого приглашенного друга, который стал PRO.\n"
        "Поделитесь ссылкой:\n"
        "{ref_link}"
    ),
    "profile_empty": (
        "У вас пока нет активного ключа.\n"
        "Оплатите тариф — бот автоматически выдаст ключ и ссылку на подписку."
    ),
    "need_payment": "Чтобы получить ключ, выберите тариф и оплатите доступ.",
    "faq_main": "Выберите вопрос:",
    "faq_pro": "PRO включает максимальную скорость, все локации и расширенные функции.",
    "faq_broken": (
        "Что-то не работает\n\n"
        "1. Обновите ключ в приложении.\n"
        "2. Переключите локацию.\n"
        "3. Попробуйте другой клиент (Happ или V2RayTUN).\n\n"
        "Если проблема осталась — напишите в поддержку: {support}."
    ),
    "faq_about": (
        "{brand} — быстрый и безопасный VPN.\n"
        "Полное шифрование трафика на VLESS.\n"
        "Высокая скорость без ограничений по трафику.\n"
        "До 10 устройств одновременно.\n"
        "Совместим с популярными VPN-клиентами."
    ),
    "faq_jobs": "Вакансии\n\nМы растем. Напишите в поддержку по любым вопросам.",
    "faq_support": "Тех. поддержка: {support}",
    "faq_cancel": "Отменить подписку\n\nНапишите в поддержку: {support}.",
    "renew_3d": "Важно: подписка закончится через 3 дня. Продлите доступ заранее.",
    "renew_1d": "Важно: подписка закончится завтра. Продлите, чтобы избежать отключения.",
    "renew_0d": "Важно: подписка заканчивается сегодня. Продлите доступ.",
    "renew_expired": "Подписка закончилась. Продлите доступ, чтобы снова подключиться.",
    "referral_banner": "+1 месяц за друга",
    "invite_friend": (
        "Получите +1 месяц за каждого приглашенного друга, который стал PRO!\n\n"
        "Поделитесь сообщением:\n"
        f"Я использую {BRAND_NAME}. Он убирает рекламу на YouTube и работает на всех устройствах.\n\n"
        "Ссылка:\n"
        "{ref_link}"
    ),
    "lang_switched": "Язык переключен на русский.",
    "menu_hint": "Меню внизу. Выберите раздел.",
    "support_banner": "Поддержка 24/7",
    "support_text": (
        "Напишите в поддержку: {support}\n"
        "Отвечаем быстро и по делу."
    ),
    "channel_banner": "Канал GetniusVPN",
    "channel_text": "Новости, обновления и полезные советы: {channel}",
}

EN: Dict[str, str] = {
    "welcome_banner": "Hi! Connect VPN in 1 minute.",
    "welcome_text": (
        "{brand} is a fast and secure VPN on VLESS.\n"
        "Paste the key into the app and choose a location.\n\n"
        "Select your device:"
    ),
    "device_prompt": "Select your device:",
    "steps_banner": "Connect in 3 steps",
    "android_setup": (
        "Android setup:\n"
        "1. Install Happ from Google Play or APK.\n"
        "2. Tap the button below to connect in 1 click.\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key:\n"
        "{key}\n"
        "2. Open Happ and tap “Paste/From clipboard”.\n"
        "3. Choose a location and connect.\n\n"
        "If it still fails, try V2RayTUN."
    ),
    "android_v2ray": (
        "V2RayTUN setup:\n"
        "1. Install V2RayTUN from Google Play or APK.\n"
        "2. Tap the button below to connect in 1 click.\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key:\n"
        "{key}\n"
        "2. Open V2RayTUN, tap “+” -> “Import from clipboard”.\n"
        "3. Choose a location and connect."
    ),
    "generic_setup": (
        "Setup for {device}:\n"
        "1. Install any client that supports VLESS.\n"
        "2. Paste the key into the app.\n"
        "3. Choose a location and connect.\n\n"
        "Alternative clients: Happ / V2RayTUN.\n"
        "Need help? Contact support: {support}."
    ),
    "tariffs_banner": "GetniusVPN Plans",
    "tariffs": (
        "Available plans:\n"
        "- 1 month: 100 RUB\n"
        "- 3 months: 270 RUB\n"
        "- 12 months: 960 RUB\n\n"
        f"Trial: {TRIAL_PRICE_RUB} for {TRIAL_DAYS} days.\n"
        "PRO includes all features and max speed.\n"
        "If payment went through but no key arrived — contact support."
    ),
    "pro_features": (
        "PRO features:\n"
        "- Security and encryption\n"
        "- High speed\n"
        "- Up to 10 devices\n"
        "- Ad blocking"
    ),
    "profile": (
        "You use {brand}\n\n"
        "Your key:\n"
        "{key}\n"
        "Tap the key to copy.\n\n"
        "Plan: {plan}\n"
        "Device limit: {limit}\n"
        "Traffic used: {traffic}\n"
        "Valid until: {expires}\n\n"
        "Get +1 month for each invited friend who becomes PRO.\n"
        "Share link:\n"
        "{ref_link}"
    ),
    "profile_empty": (
        "You don't have an active key yet.\n"
        "Pay for a plan — the bot will issue the key automatically."
    ),
    "need_payment": "To get a key, choose a plan and complete payment.",
    "faq_main": "Choose a topic:",
    "faq_pro": "PRO includes max speed, all locations, and advanced features.",
    "faq_broken": (
        "Something doesn't work\n\n"
        "1. Refresh your key in the app.\n"
        "2. Switch location.\n"
        "3. Try another client (Happ or V2RayTUN).\n\n"
        "If it still fails, contact support: {support}."
    ),
    "faq_about": (
        "{brand} is a fast and secure VPN.\n"
        "Full traffic encryption with VLESS.\n"
        "High speed with no traffic limits.\n"
        "Up to 10 devices at once.\n"
        "Compatible with popular clients."
    ),
    "faq_jobs": "Jobs\n\nWe are growing. Contact support for open roles.",
    "faq_support": "Support: {support}",
    "faq_cancel": "Cancel subscription\n\nContact support: {support}.",
    "renew_3d": "Important: subscription ends in 3 days. Renew to stay connected.",
    "renew_1d": "Important: subscription ends tomorrow. Renew now to avoid downtime.",
    "renew_0d": "Important: subscription ends today. Renew to keep access.",
    "renew_expired": "Your subscription has ended. Renew to regain access.",
    "referral_banner": "+1 month for a friend",
    "invite_friend": (
        "Get +1 month for each invited friend who becomes PRO!\n\n"
        "Share this message:\n"
        f"I use {BRAND_NAME}. It removes YouTube ads and works on all devices.\n\n"
        "Link:\n"
        "{ref_link}"
    ),
    "lang_switched": "Language switched to English.",
    "menu_hint": "Menu opened. Choose a section.",
    "support_banner": "Support 24/7",
    "support_text": "Contact support: {support}\nWe usually respond within minutes.",
    "channel_banner": "GetniusVPN Channel",
    "channel_text": "Updates and tips: {channel}",
}


def t(lang: str, text_id: str, **kwargs: str) -> str:
    data = EN if lang == "en" else RU
    base = {
        "brand": BRAND_NAME,
        "bot": BOT_USERNAME,
        "support": SUPPORT_BOT,
        "channel": CHANNEL,
        "trial_days": str(TRIAL_DAYS),
        "trial_price": TRIAL_PRICE_RUB,
        "one_click_url": ONE_CLICK_URL,
        "v2ray_url": V2RAY_URL,
        "privacy_email": PRIVACY_EMAIL,
    }
    base.update(kwargs)
    text = data.get(text_id, "")
    return _fmt(text, **base)
