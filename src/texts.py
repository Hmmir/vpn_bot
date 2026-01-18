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
        "{brand} — быстрый и безопасный VPN на протоколе VLESS.\n"
        "Просто вставьте ключ в приложение и выберите локацию."
    ),
    "device_prompt": "Выберите ваше устройство:",
    "steps_banner": "Подключение в 3 шага",
    "android_setup": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте Happ из Google Play или APK-файл: {happ_url}\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n\n"
        "Если автоматическая настройка не сработала:\n"
        "1. Скопируйте ключ:\n"
        "{key}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь.\n\n"
        "Если приложение не работает, рекомендуем V2RayTUN: {v2raytun_url}"
    ),
    "android_setup_no_key": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте Happ из Google Play или APK-файл: {happ_url}\n"
        "2. Оплатите тариф — ключ появится в профиле.\n"
        "3. Вставьте ключ и подключитесь.\n\n"
        "Если приложение не работает, рекомендуем V2RayTUN: {v2raytun_url}"
    ),
    "android_v2ray": (
        "Для настройки VPN через V2RayTUN:\n"
        "1. Установите V2RayTUN: {v2raytun_url}\n"
        "2. Нажмите кнопку ниже, чтобы Подключиться в 1 клик!\n\n"
        "Если автоматическая настройка не сработала:\n"
        "1. Скопируйте ключ:\n"
        "{key}\n"
        "2. Откройте V2RayTUN, нажмите “+” и выберите “Импорт из буфера”.\n"
        "3. Выберите локацию и подключитесь."
    ),
    "android_v2ray_no_key": (
        "Для настройки VPN через V2RayTUN:\n"
        "1. Установите V2RayTUN: {v2raytun_url}\n"
        "2. Оплатите тариф — ключ появится в профиле.\n"
        "3. Импортируйте ключ и подключитесь."
    ),
    "generic_setup": (
        "Для настройки VPN на {device}:\n"
        "1. Установите клиент с поддержкой VLESS.\n"
        "2. Вставьте ключ в приложение.\n"
        "3. Выберите локацию и подключитесь.\n\n"
        "Рекомендуемый клиент: {client_line}\n"
        "Нужна помощь? Напишите в поддержку: {support}."
    ),
    "generic_setup_no_key": (
        "Для настройки VPN на {device}:\n"
        "1. Установите клиент с поддержкой VLESS.\n"
        "2. Оплатите тариф — ключ появится в профиле.\n"
        "3. Вставьте ключ и подключитесь.\n\n"
        "Рекомендуемый клиент: {client_line}\n"
        "Нужна помощь? Напишите в поддержку: {support}."
    ),
    "tariffs_banner": "Тарифы",
    "tariffs": (
        "Тарифы:\n"
        "- 1 мес: 100 руб\n"
        "- 3 мес: 250 руб\n"
        "- 12 мес: 900 руб\n\n"
        f"Пробный период: {TRIAL_PRICE_RUB} за {TRIAL_DAYS} дней "
        "(спишем 25 руб за привязку карты).\n"
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
        "Ссылка:\n"
        "{ref_link}"
    ),
    "profile_empty": (
        "У вас пока нет ключа.\n"
        "Оплатите тариф — ключ появится в профиле."
    ),
    "need_payment": (
        "Чтобы получить ключ, выберите тариф и оплатите доступ."
    ),
    "faq_main": "Выберите вопрос:",
    "faq_pro": "PRO включает максимальную скорость, стабильность и все функции.",
    "faq_broken": (
        "Что-то не работает\n\n"
        "1. Обновите ключ в приложении.\n"
        "2. Переподключитесь.\n"
        "3. Попробуйте альтернативный клиент (Happ или V2RayTUN).\n\n"
        "Если проблема остаётся — напишите в поддержку: {support}."
    ),
    "faq_about": (
        "{brand} — быстрый и безопасный VPN.\n"
        "Работаем на протоколе VLESS.\n"
        "Поддерживаем телефоны, компьютеры и ТВ.\n"
        "До 10 устройств одновременно."
    ),
    "faq_jobs": "Вакансии\n\nНапишите нам. Свяжемся с вами в поддержке.",
    "faq_support": "Тех. поддержка: {support}",
    "faq_cancel": "Отменить подписку\n\nНапишите в поддержку: {support}.",
    "renew_3d": "Напоминание: подписка истекает через 3 дня. Продлите доступ.",
    "renew_1d": "Напоминание: подписка истекает завтра. Продлите доступ.",
    "renew_0d": "Напоминание: подписка истекает сегодня. Продлите доступ.",
    "renew_expired": "Подписка истекла. Продлите доступ, чтобы пользоваться VPN.",
    "referral_banner": "+1 месяц за друга",
    "invite_friend": (
        "Получите +1 месяц за каждого приглашенного друга, который стал PRO!\n\n"
        "Отправьте ссылку другу или перешлите текст:\n"
        f"Я использую {BRAND_NAME}. Он быстро и стабильно открывает сайты.\n\n"
        "Ссылка:\n"
        "{ref_link}"
    ),
    "lang_switched": "Язык переключен.",
    "menu_hint": "Меню внизу. Выберите раздел.",
    "support_banner": "Поддержка 24/7",
    "support_text": (
        "Нужна помощь? Напишите в поддержку: {support}\n"
        "Отвечаем быстро и по делу."
    ),
    "channel_banner": "Канал",
    "channel_text": "Новости и обновления: {channel}",
}

EN: Dict[str, str] = {
    "welcome_banner": "Hi! Connect VPN in 1 minute.",
    "welcome_text": (
        "{brand} is a fast and secure VPN on VLESS.\n"
        "Paste the key into the app and choose a location."
    ),
    "device_prompt": "Select your device:",
    "steps_banner": "Connect in 3 steps",
    "android_setup": (
        "Android setup:\n"
        "1. Install Happ: {happ_url}\n"
        "2. Tap the button below to connect in 1 click.\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key:\n"
        "{key}\n"
        "2. Open Happ and tap “Paste/From clipboard”.\n"
        "3. Choose a location and connect.\n\n"
        "If it still fails, try V2RayTUN: {v2raytun_url}"
    ),
    "android_setup_no_key": (
        "Android setup:\n"
        "1. Install Happ: {happ_url}\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Paste the key and connect.\n\n"
        "If it still fails, try V2RayTUN: {v2raytun_url}"
    ),
    "android_v2ray": (
        "V2RayTUN setup:\n"
        "1. Install V2RayTUN: {v2raytun_url}\n"
        "2. Tap the button below to connect in 1 click.\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key:\n"
        "{key}\n"
        "2. Open V2RayTUN, tap “+” and choose “Import from clipboard”.\n"
        "3. Choose a location and connect."
    ),
    "android_v2ray_no_key": (
        "V2RayTUN setup:\n"
        "1. Install V2RayTUN: {v2raytun_url}\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Import the key and connect."
    ),
    "generic_setup": (
        "Setup for {device}:\n"
        "1. Install a VLESS-compatible client.\n"
        "2. Paste the key into the app.\n"
        "3. Choose a location and connect.\n\n"
        "Recommended client: {client_line}\n"
        "Need help? Contact support: {support}."
    ),
    "generic_setup_no_key": (
        "Setup for {device}:\n"
        "1. Install a VLESS-compatible client.\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Paste the key and connect.\n\n"
        "Recommended client: {client_line}\n"
        "Need help? Contact support: {support}."
    ),
    "tariffs_banner": "Plans",
    "tariffs": (
        "Plans:\n"
        "- 1 month: 100 RUB\n"
        "- 3 months: 250 RUB\n"
        "- 12 months: 900 RUB\n\n"
        f"Trial: {TRIAL_PRICE_RUB} for {TRIAL_DAYS} days (card verification).\n"
        "PRO includes all features and maximum speed.\n"
        "If payment went through but the key didn’t arrive, contact support."
    ),
    "pro_features": (
        "PRO features:\n"
        "- Security and encryption\n"
        "- High speed\n"
        "- Up to 10 devices\n"
        "- Ad blocking"
    ),
    "profile": (
        "You are using {brand}\n\n"
        "Your key:\n"
        "{key}\n"
        "Tap the key to copy.\n\n"
        "Plan: {plan}\n"
        "Device limit: {limit}\n"
        "Traffic: {traffic}\n"
        "Valid until: {expires}\n\n"
        "Get +1 month for every friend who became PRO.\n"
        "Link:\n"
        "{ref_link}"
    ),
    "profile_empty": (
        "You don’t have a key yet.\n"
        "Pay for a plan — the key will appear in your profile."
    ),
    "need_payment": "To get a key, choose a plan and pay.",
    "faq_main": "Choose a question:",
    "faq_pro": "PRO includes maximum speed, stability, and all features.",
    "faq_broken": (
        "Something doesn't work\n\n"
        "1. Refresh the key in the app.\n"
        "2. Reconnect.\n"
        "3. Try an alternative client (Happ or V2RayTUN).\n\n"
        "If the issue remains, contact support: {support}."
    ),
    "faq_about": (
        "{brand} is a fast and secure VPN.\n"
        "We use the VLESS protocol.\n"
        "Works on phones, computers, and TVs.\n"
        "Up to 10 devices simultaneously."
    ),
    "faq_jobs": "Jobs\n\nContact us in support.",
    "faq_support": "Support: {support}",
    "faq_cancel": "Cancel subscription\n\nContact support: {support}.",
    "renew_3d": "Reminder: your subscription ends in 3 days. Renew access.",
    "renew_1d": "Reminder: your subscription ends tomorrow. Renew access.",
    "renew_0d": "Reminder: your subscription ends today. Renew access.",
    "renew_expired": "Your subscription expired. Renew to keep access.",
    "referral_banner": "+1 month for a friend",
    "invite_friend": (
        "Get +1 month for every invited friend who becomes PRO!\n\n"
        "Share this link:\n"
        "{ref_link}"
    ),
    "lang_switched": "Language switched.",
    "menu_hint": "Menu opened. Choose a section.",
    "support_banner": "Support 24/7",
    "support_text": "Contact support: {support}\nWe usually respond quickly.",
    "channel_banner": "Channel",
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
        "happ_url": kwargs.get("happ_url", ""),
        "v2raytun_url": kwargs.get("v2raytun_url", ""),
        "client_line": kwargs.get("client_line", ""),
    }
    base.update(kwargs)
    text = data.get(text_id, "")
    return _fmt(text, **base)
