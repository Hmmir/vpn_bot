from typing import Dict

from .config import BRAND_NAME, BOT_USERNAME, SUPPORT_BOT, CHANNEL, ONE_CLICK_URL, V2RAY_URL
from .data import TRIAL_DAYS, TRIAL_PRICE_RUB


def _fmt(text: str, **kwargs: str) -> str:
    return text.format(**kwargs)


RU: Dict[str, str] = {
    "welcome": (
        "Добро пожаловать в {brand}! 👋\n\n"
        "Мы выдаем VPN-ключи для доступа к быстрым и безопасным серверам "
        "на протоколе VLESS. Просто вставьте ключ в приложение.\n\n"
        "Меню находится в клавиатуре (≡) — выберите нужный раздел "
        "или сразу установите VPN.\n\n"
        "Выберите ваше устройство:"
    ),
    "device_prompt": "Выберите ваше устройство:",
    "android_setup": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте Happ из «Google Play» или «APK-файл».\n"
        "2. Нажмите кнопку ниже, чтобы подключиться в 1 клик.\n\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key}\n"
        "2. Откройте Happ и нажмите кнопку «Вставить/Из буфера».\n"
        "3. Выберите локацию и подключитесь.\n\n"
        "Если приложение не работает, попробуйте V2RayTUN по кнопке."
    ),
    "android_v2ray": (
        "Для настройки через V2RayTUN:\n"
        "1. Скачайте V2RayTUN из «Google Play» или «APK-файл».\n"
        "2. Нажмите кнопку ниже, чтобы подключиться в 1 клик.\n\n"
        "Если автоматическая настройка не сработала:\n"
        "1. Скопируйте ключ:\n"
        "{key}\n"
        "2. Откройте V2RayTUN, нажмите «+» → «Импорт из буфера».\n"
        "3. Выберите локацию и нажмите синюю кнопку.\n"
        "4. Разрешите подключение."
    ),
    "generic_setup": (
        "Для настройки на {device}:\n"
        "1. Скачайте VPN-клиент, который поддерживает VLESS.\n"
        "2. Вставьте ваш ключ в приложение.\n"
        "3. Выберите локацию и подключитесь.\n\n"
        "Если нужна помощь — напишите в поддержку: {support}."
    ),
    "thanks_pro": (
        "Спасибо за выбор {brand}! 🙌\n\n"
        "Мы включили PRO-функции в вашем ключе — бесплатно на {trial_days} дня:\n"
        "— Обход «Белого списка» сайтов\n"
        "— Фильтрация рекламы на YouTube\n"
        "— Безлимитный трафик\n"
        "— Безлимитное количество устройств\n\n"
        "После пробного периода вы сможете остаться на PRO или перейти на бесплатный тариф."
    ),
    "tariffs": (
        "Тарифы\n\n"
        "У нашего сервиса есть PRO-тариф, на котором доступны:\n"
        "— Обход «Белого списка» сайтов\n"
        "— Фильтрация рекламы на YouTube\n"
        "— Безлимитный трафик\n"
        "— Безлимитное количество устройств\n\n"
        "Пробный период: {trial_price} за {trial_days} дня.\n"
        "Выберите тариф и присоединяйтесь к тысячам довольных пользователей!"
    ),
    "profile": (
        "Вы используете {brand} ✨\n\n"
        "Ваш ключ — со всеми локациями для всех устройств:\n"
        "{key}\n\n"
        "Потребление трафика: {traffic}\n"
        "Действует до: {expires}\n\n"
        "Получите +1 месяц за каждого приглашенного друга, который стал PRO!\n"
        "Поделитесь ссылкой:\n"
        "{ref_link}\n\n"
        "⚠ Привяжите Email к аккаунту, чтобы в случае блокировки Telegram "
        "управлять VPN на сайте."
    ),
    "faq_main": (
        "Выберите вопрос, который вас интересует:"
    ),
    "faq_pro": (
        "Вопросы о PRO\n\n"
        "PRO включает максимальные скорости, безлимитный трафик и доступ ко всем локациям."
    ),
    "faq_broken": (
        "Что-то не работает\n\n"
        "1. Проверьте подключение и обновите ключ в приложении.\n"
        "2. Переключите локацию.\n"
        "3. Попробуйте альтернативный клиент (например, V2RayTUN).\n\n"
        "Если не помогло — напишите в поддержку: {support}."
    ),
    "faq_about": (
        "{brand} — надежный, быстрый и безопасный VPN.\n"
        "Полное шифрование трафика и современный протокол VLESS.\n"
        "Высокая скорость без ограничений по трафику.\n"
        "Подключайте до 5 устройств одновременно.\n"
        "Совместимость с популярными VPN-клиентами."
    ),
    "faq_jobs": (
        "Вакансии\n\n"
        "Мы растем. Пишите в поддержку, чтобы узнать об актуальных ролях."
    ),
    "faq_support": (
        "Тех. поддержка: {support}"
    ),
    "faq_cancel": (
        "Отмена подписки\n\n"
        "Для отмены подписки напишите в поддержку: {support}."
    ),
    "invite_friend": (
        "Получите +1 месяц использования за каждого приглашенного друга, "
        "который стал PRO! 😎\n\n"
        "Поделитесь ссылкой или просто перешлите сообщение:\n"
        "Я использую {brand}. Он умеет убирать рекламу с YouTube и "
        "его можно поставить на все устройства.\n\n"
        "Ссылка:\n"
        "{ref_link}"
    ),
    "lang_switched": "Язык переключен на русский.",
    "menu_hint": "Меню открыто. Выберите раздел.",
}

EN: Dict[str, str] = {
    "welcome": (
        "Welcome to {brand}! 👋\n\n"
        "We provide VPN keys for fast and secure servers using the VLESS protocol. "
        "Just paste the key into your app.\n\n"
        "The menu is in the keyboard (≡) — pick a section or install VPN now.\n\n"
        "Select the device you want to set up:"
    ),
    "device_prompt": "Select your device:",
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
        "2. Open V2RayTUN, tap “+” → “Import from clipboard”.\n"
        "3. Choose a location and connect."
    ),
    "generic_setup": (
        "Setup for {device}:\n"
        "1. Install any client that supports VLESS.\n"
        "2. Paste your key into the app.\n"
        "3. Choose a location and connect.\n\n"
        "Need help? Contact support: {support}."
    ),
    "thanks_pro": (
        "Thanks for choosing {brand}! 🙌\n\n"
        "PRO features are enabled for {trial_days} days:\n"
        "— Bypass restricted sites\n"
        "— YouTube ad filtering\n"
        "— Unlimited traffic\n"
        "— Unlimited devices\n\n"
        "After the trial you can stay on PRO or switch to the free tier."
    ),
    "tariffs": (
        "Plans\n\n"
        "PRO includes:\n"
        "— Bypass restricted sites\n"
        "— YouTube ad filtering\n"
        "— Unlimited traffic\n"
        "— Unlimited devices\n\n"
        "Trial: {trial_price} for {trial_days} days."
    ),
    "profile": (
        "You use {brand} ✨\n\n"
        "Your key:\n"
        "{key}\n\n"
        "Traffic used: {traffic}\n"
        "Valid until: {expires}\n\n"
        "Get +1 month for each invited friend who becomes PRO.\n"
        "Share link:\n"
        "{ref_link}\n\n"
        "⚠ Attach email to manage VPN if Telegram is blocked."
    ),
    "faq_main": "Choose a topic:",
    "faq_pro": "PRO questions\n\nPRO includes max speed, unlimited traffic, all locations.",
    "faq_broken": (
        "Something doesn't work\n\n"
        "1. Refresh your key in the app.\n"
        "2. Switch location.\n"
        "3. Try another client (e.g., V2RayTUN).\n\n"
        "If it still fails, contact support: {support}."
    ),
    "faq_about": (
        "{brand} is a fast and secure VPN.\n"
        "Full traffic encryption with VLESS.\n"
        "High speed with no traffic limits.\n"
        "Up to 5 devices at once.\n"
        "Compatible with popular clients."
    ),
    "faq_jobs": "Jobs\n\nWe are growing. Contact support for open roles.",
    "faq_support": "Support: {support}",
    "faq_cancel": "Cancel subscription\n\nContact support: {support}.",
    "invite_friend": (
        "Get +1 month for each invited friend who becomes PRO! 😎\n\n"
        "Share this message:\n"
        "I use {brand}. It removes YouTube ads and works on all devices.\n\n"
        "Link:\n"
        "{ref_link}"
    ),
    "lang_switched": "Language switched to English.",
    "menu_hint": "Menu opened. Choose a section.",
}


def t(lang: str, key: str, **kwargs: str) -> str:
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
    }
    base.update(kwargs)
    text = data.get(key, "")
    return _fmt(text, **base)
