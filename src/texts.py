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
        "{brand} — надежный ВПН без рекламы.\n\n"
        "Добро пожаловать в {brand}!\n\n"
        "Мы выдаём VPN-ключи для доступа к быстрым и безопасным серверам на протоколе "
        "VLESS. Просто вставьте ключ в приложение.\n\n"
        "Меню находится в клавиатуре (☰) — выберите нужный раздел или сразу установите VPN."
    ),
    "device_prompt": "Выберите ваше устройство:",
    "paywall_device": (
        "Для подключения нужен ключ.\n"
        "Оплатите пробный доступ {trial_days} дней за {trial_price} — ключ появится в профиле.\n"
        "После оплаты снова выберите устройство."
    ),
    "steps_banner": "Подключение в 3 шага",
    "android_setup": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте Happ из «{happ_gp}» или «{happ_apk}».\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key_link}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь.\n"
        "\n"
        "Если данное приложение у вас не работает, то рекомендуем настроить V2RayTUN по кнопке."
    ),
    "android_setup_no_key": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте Happ из «{happ_gp}» или «{happ_apk}».\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key_link}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь.\n"
        "\n"
        "Если данное приложение у вас не работает, то рекомендуем настроить V2RayTUN по кнопке."
    ),
    "android_v2ray": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте V2RayTUN из «{v2ray_gp}» или «{v2ray_apk}».\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{sub_url_link}\n"
        "2. Откройте V2RayTUN, в правом верхнем углу нажмите на кнопку \"+\".\n"
        "3. Выберите Импорт из буфера обмена.\n"
        "4. Выберите локацию и нажмите синюю кнопку.\n"
        "5. Разрешите подключение."
    ),
    "android_v2ray_no_key": (
        "Для настройки VPN на Android:\n"
        "1. Скачайте V2RayTUN из «{v2ray_gp}» или «{v2ray_apk}».\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{sub_url_link}\n"
        "2. Откройте V2RayTUN, в правом верхнем углу нажмите на кнопку \"+\".\n"
        "3. Выберите Импорт из буфера обмена.\n"
        "4. Выберите локацию и нажмите синюю кнопку.\n"
        "5. Разрешите подключение."
    ),
    "ios_setup": (
        "Для настройки VPN на iPhone:\n"
        "1. Скачайте {happ_ios_ru} для России ({happ_ios_alt} для других регионов)\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key_link}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь."
    ),
    "ios_setup_no_key": (
        "Для настройки VPN на iPhone:\n"
        "1. Скачайте {happ_ios_ru} для России ({happ_ios_alt} для других регионов)\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key_link}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь."
    ),
    "windows_setup": (
        "Для настройки VPN на Windows:\n"
        "1. Скачайте {flclash_link}.\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "3. Нажмите кнопку ▶ в нижнем правом углу для включения VPN. Выбрать локацию можно внутри раздела Прокси.\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{sub_url_link}\n"
        "2. Откройте FlClash и перейдите в раздел Профили.\n"
        "3. Нажмите плюс в нижнем углу и выберите URL.\n"
        "4. В появившемся окне вставьте скопированный ключ.\n"
        "5. Перейдите в раздел Прокси и выберите нужную локацию.\n"
        "6. Далее перейдите на Панель управления и нажмите кнопку ▶ в нижнем правом углу для включения VPN."
    ),
    "windows_setup_no_key": (
        "Для настройки VPN на Windows:\n"
        "1. Скачайте {flclash_link}.\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "3. Нажмите кнопку ▶ в нижнем правом углу для включения VPN. Выбрать локацию можно внутри раздела Прокси.\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{sub_url_link}\n"
        "2. Откройте FlClash и перейдите в раздел Профили.\n"
        "3. Нажмите плюс в нижнем углу и выберите URL.\n"
        "4. В появившемся окне вставьте скопированный ключ.\n"
        "5. Перейдите в раздел Прокси и выберите нужную локацию.\n"
        "6. Далее перейдите на Панель управления и нажмите кнопку ▶ в нижнем правом углу для включения VPN."
    ),
    "macos_setup": (
        "Для настройки VPN на Macbook (от 2020 года)\n"
        "1. Скачайте {happ_ios_ru} для России ({happ_ios_alt} для других регионов)\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key_link}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь.\n"
        "\n"
        "Если данное приложение у вас не работает или ваш Macbook выпущен до 2020 года, то рекомендуем настроить Sing-box."
    ),
    "macos_setup_no_key": (
        "Для настройки VPN на Macbook (от 2020 года)\n"
        "1. Скачайте {happ_ios_ru} для России ({happ_ios_alt} для других регионов)\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{key_link}\n"
        "2. Откройте Happ и нажмите кнопку Вставить/Из буфера.\n"
        "3. Выберите локацию и подключитесь.\n"
        "\n"
        "Если данное приложение у вас не работает или ваш Macbook выпущен до 2020 года, то рекомендуем настроить Sing-box."
    ),
    "linux_setup": (
        "Для подключения VPN на Linux:\n"
        "1. Скачайте «{flclash_link}».\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{sub_url_link}\n"
        "2. Откройте FlClash и перейдите в раздел Профили.\n"
        "3. Нажмите плюс в нижнем углу и выберите URL.\n"
        "4. В появившемся окне вставьте скопированный ключ.\n"
        "5. Перейдите в раздел Прокси и выберите нужную локацию.\n"
        "6. Далее перейдите на Панель управления.\n"
        "7. Убедитесь, что у вас включен TUN, а также установлен \"Режим исходящего трафика\" Глобальный.\n"
        "8. Нажмите кнопку ▶ в нижнем правом углу для включения VPN."
    ),
    "linux_setup_no_key": (
        "Для подключения VPN на Linux:\n"
        "1. Скачайте «{flclash_link}».\n"
        "2. Нажмите на кнопку ниже, чтобы Подключиться в 1 клик!\n"
        "\n"
        "Если автоматическая настройка не сработала, следуйте инструкции:\n"
        "1. Скопируйте ключ, нажав на него:\n"
        "{sub_url_link}\n"
        "2. Откройте FlClash и перейдите в раздел Профили.\n"
        "3. Нажмите плюс в нижнем углу и выберите URL.\n"
        "4. В появившемся окне вставьте скопированный ключ.\n"
        "5. Перейдите в раздел Прокси и выберите нужную локацию.\n"
        "6. Далее перейдите на Панель управления.\n"
        "7. Убедитесь, что у вас включен TUN, а также установлен \"Режим исходящего трафика\" Глобальный.\n"
        "8. Нажмите кнопку ▶ в нижнем правом углу для включения VPN."
    ),
    "android_tv_setup": (
        "Если у вас телевизор с usb-разъемом, то рекомендуем вставить мышку — так удобнее😉\n"
        "\n"
        "1. На TV откройте Google Play и установите приложение Happ из «{happ_gp}» или «{happ_apk}».\n"
        "2. Откройте Happ на TV, перед вами появится QR-код.\n"
        "3. Откройте Happ на телефоне, нажмите на кнопку QR-код и отсканируйте QR-код с TV.\n"
        "4. На телефоне появится окно выбора ключей, выберите {brand} и нажмите Отправить.\n"
        "5. На TV нажмите кнопку пропустить — на главной в Happ вы должны будете увидеть перечень локаций и кнопку включения.\n"
        "6. Нажмите на нее и выдайте разрешение, чтобы подключиться к VPN.\n"
        "\n"
        "Если у вас что-то не получается, попробуйте альтернативный способ настройки через приложение V2rayTUN."
    ),
    "android_tv_setup_no_key": (
        "Если у вас телевизор с usb-разъемом, то рекомендуем вставить мышку — так удобнее😉\n"
        "\n"
        "1. На TV откройте Google Play и установите приложение Happ из «{happ_gp}» или «{happ_apk}».\n"
        "2. Откройте Happ на TV, перед вами появится QR-код.\n"
        "3. Откройте Happ на телефоне, нажмите на кнопку QR-код и отсканируйте QR-код с TV.\n"
        "4. На телефоне появится окно выбора ключей, выберите {brand} и нажмите Отправить.\n"
        "5. На TV нажмите кнопку пропустить — на главной в Happ вы должны будете увидеть перечень локаций и кнопку включения.\n"
        "6. Нажмите на нее и выдайте разрешение, чтобы подключиться к VPN.\n"
        "\n"
        "Если у вас что-то не получается, попробуйте альтернативный способ настройки через приложение V2rayTUN."
    ),
    "apple_tv_setup": (
        "Для установки VPN на Apple TV:\n"
        "1. На TV откройте {app_store_link} и установите приложение {happ_ios_ru}\n"
        "2. Откройте Happ на TV, перед вами появится QR-код.\n"
        "3. Откройте Happ на телефоне, нажмите на кнопку QR-код и отсканируйте QR-код с TV.\n"
        "4. На телефоне появится окно выбора ключей, выберите {brand} и нажмите Отправить.\n"
        "5. На TV нажмите кнопку пропустить — на главной в Happ вы должны будете увидеть перечень локаций и кнопку включения.\n"
        "6. Нажмите на нее и выдайте разрешение, чтобы подключиться к VPN.\n"
        "\n"
        "Если у вас что-то не получается, попробуйте альтернативный способ настройки через приложение Sing Box."
    ),
    "apple_tv_setup_no_key": (
        "Для установки VPN на Apple TV:\n"
        "1. На TV откройте {app_store_link} и установите приложение {happ_ios_ru}\n"
        "2. Откройте Happ на TV, перед вами появится QR-код.\n"
        "3. Откройте Happ на телефоне, нажмите на кнопку QR-код и отсканируйте QR-код с TV.\n"
        "4. На телефоне появится окно выбора ключей, выберите {brand} и нажмите Отправить.\n"
        "5. На TV нажмите кнопку пропустить — на главной в Happ вы должны будете увидеть перечень локаций и кнопку включения.\n"
        "6. Нажмите на нее и выдайте разрешение, чтобы подключиться к VPN.\n"
        "\n"
        "Если у вас что-то не получается, попробуйте альтернативный способ настройки через приложение Sing Box."
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
        "Вы открыли базу самопомощи, здесь вы можете самостоятельно найти решение своей проблемы.\n\n"
        "Проверить работоспособность VPN можно на speedtest.net или check-host.net.\n\n"
        "Если решить проблему не получилось, свяжитесь с нами в {support}."
    ),
    "help_prompt": "Выберите раздел, который вас интересует:",
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
    "paywall_device": (
        "A key is required to connect.\n"
        "Pay for the trial access ({trial_days} days for {trial_price}) — the key will appear in your profile.\n"
        "After payment, choose your device again."
    ),
    "steps_banner": "Connect in 3 steps",
    "android_setup": (
        "Android setup:\n"
        "1. Install Happ from Google Play {happ_url}{happ_apk_suffix}.\n"
        "2. Tap the button below to connect in 1 click!\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key by tapping it:\n"
        "{key}\n"
        "2. Open Happ and tap “Paste/From clipboard”.\n"
        "3. Choose a location and connect.\n\n"
        "If the app doesn't work, try V2RayTUN via the button."
    ),
    "android_setup_no_key": (
        "Android setup:\n"
        "1. Install Happ from Google Play {happ_url}{happ_apk_suffix}.\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Paste the key and connect.\n\n"
        "If the app doesn't work, try V2RayTUN via the button."
    ),
    "android_v2ray": (
        "Android setup (V2RayTUN):\n"
        "1. Install V2RayTUN from Google Play or APK: {v2raytun_url}\n"
        "2. Tap the button below to connect in 1 click!\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key by tapping it:\n"
        "{key}\n"
        "2. Open V2RayTUN, tap “+” in the top-right corner.\n"
        "3. Choose “Import from clipboard”.\n"
        "4. Pick a location and tap the blue button.\n"
        "5. Allow the connection."
    ),
    "android_v2ray_no_key": (
        "Android setup (V2RayTUN):\n"
        "1. Install V2RayTUN: {v2raytun_url}\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Import the key and connect."
    ),
    "ios_setup": (
        "iPhone setup:\n"
        "1. Install Happ for Russia {happ_ios_url}{happ_ios_alt_suffix}.\n"
        "2. Tap the button below to connect in 1 click!\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key by tapping it:\n"
        "{key}\n"
        "2. Open Happ and tap “Paste/From clipboard”.\n"
        "3. Choose a location and connect."
    ),
    "ios_setup_no_key": (
        "iPhone setup:\n"
        "1. Install Happ for Russia {happ_ios_url}{happ_ios_alt_suffix}.\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Paste the key and connect."
    ),
    "windows_setup": (
        "Windows setup:\n"
        "1. Download FlClash: {flclash_url}\n"
        "2. Tap the button below to connect in 1 click!\n"
        "3. Press ▶ in the lower-right corner to enable VPN. "
        "Locations are available in Proxy.\n\n"
        "If auto-setup fails:\n"
        "1. Copy the key by tapping it:\n"
        "{sub_url}\n"
        "2. Open FlClash and go to Profiles.\n"
        "3. Tap the plus in the lower corner and choose URL.\n"
        "4. Paste the copied key.\n"
        "5. Go to Proxy and choose a location.\n"
        "6. Open Control panel and press ▶ in the lower-right corner to enable VPN."
    ),
    "windows_setup_no_key": (
        "Windows setup:\n"
        "1. Download FlClash: {flclash_url}\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Add the key to FlClash and connect."
    ),
    "macos_setup": (
        "Macbook setup (2020+):\n"
        "1. Install Happ for Russia {happ_ios_url}{happ_ios_alt_suffix}.\n"
        "2. Tap the button below to connect in 1 click!\n\n"
        "If auto-setup fails:\n"
        "1. Copy your key by tapping it:\n"
        "{key}\n"
        "2. Open Happ and tap “Paste/From clipboard”.\n"
        "3. Choose a location and connect.\n\n"
        "If the app doesn't work or your Macbook is older than 2020, try Sing-box."
    ),
    "macos_setup_no_key": (
        "Macbook setup (2020+):\n"
        "1. Install Happ for Russia {happ_ios_url}{happ_ios_alt_suffix}.\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Paste the key and connect.\n\n"
        "If the app doesn't work or your Macbook is older than 2020, try Sing-box."
    ),
    "linux_setup": (
        "Linux setup:\n"
        "1. Download FlClash: {flclash_url}\n"
        "2. Tap the button below to connect in 1 click!\n\n"
        "If auto-setup fails:\n"
        "1. Copy the key by tapping it:\n"
        "{sub_url}\n"
        "2. Open FlClash and go to Profiles.\n"
        "3. Tap the plus and choose URL.\n"
        "4. Paste the copied key.\n"
        "5. Go to Proxy and choose a location.\n"
        "6. Open Control panel.\n"
        "7. Ensure TUN is enabled and outbound mode is Global.\n"
        "8. Press ▶ in the lower-right corner to enable VPN."
    ),
    "linux_setup_no_key": (
        "Linux setup:\n"
        "1. Download FlClash: {flclash_url}\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Add the key to FlClash and connect."
    ),
    "android_tv_setup": (
        "If your TV has a USB port, using a mouse is easier.\n\n"
        "1. On the TV, open Google Play and install Happ from Google Play "
        "{happ_url}{happ_apk_suffix}.\n"
        "2. Open Happ on the TV — you'll see a QR code.\n"
        "3. Open Happ on your phone, tap QR code, and scan the TV QR code.\n"
        "4. On the phone you'll see the key list, choose {brand} and tap Send.\n"
        "5. On the TV, tap Skip — on the main screen you'll see locations and "
        "a power button.\n"
        "6. Tap it and grant permission to connect.\n\n"
        "If this doesn't work, try the alternative setup via V2RayTUN."
    ),
    "android_tv_setup_no_key": (
        "Android TV setup:\n"
        "1. On the TV, open Google Play and install Happ.\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Repeat setup via QR code."
    ),
    "apple_tv_setup": (
        "Apple TV setup:\n"
        "1. On the TV, open the App Store and install Happ.\n"
        "2. Open Happ on the TV — you'll see a QR code.\n"
        "3. Open Happ on your phone, tap QR code, and scan the TV QR code.\n"
        "4. On the phone you'll see the key list, choose {brand} and tap Send.\n"
        "5. On the TV, tap Skip — on the main screen you'll see locations and "
        "a power button.\n"
        "6. Tap it and grant permission to connect.\n\n"
        "If this doesn't work, try the alternative setup via Sing-box."
    ),
    "apple_tv_setup_no_key": (
        "Apple TV setup:\n"
        "1. On the TV, open the App Store and install Happ.\n"
        "2. Pay for a plan — the key will appear in your profile.\n"
        "3. Repeat setup via QR code."
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
        "You've opened the self-help base, where you can find a solution to your issue.\n\n"
        "Check VPN status at speedtest.net or check-host.net.\n\n"
        "If it didn't help, contact support: {support}."
    ),
    "help_prompt": "Choose the section you need:",
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
        "happ_gp": kwargs.get("happ_gp", ""),
        "happ_apk": kwargs.get("happ_apk", ""),
        "happ_ios_ru": kwargs.get("happ_ios_ru", ""),
        "happ_ios_alt": kwargs.get("happ_ios_alt", ""),
        "app_store_link": kwargs.get("app_store_link", ""),
        "flclash_link": kwargs.get("flclash_link", ""),
        "v2ray_gp": kwargs.get("v2ray_gp", ""),
        "v2ray_apk": kwargs.get("v2ray_apk", ""),
        "key_link": kwargs.get("key_link", ""),
        "sub_url": kwargs.get("sub_url", ""),
        "sub_url_link": kwargs.get("sub_url_link", ""),
        "happ_url": kwargs.get("happ_url", ""),
        "v2raytun_url": kwargs.get("v2raytun_url", ""),
        "client_line": kwargs.get("client_line", ""),
    }
    base.update(kwargs)
    text = data.get(text_id, "")
    return _fmt(text, **base)
