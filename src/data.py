from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    code: str
    title_ru: str
    title_en: str
    price_ru: str
    price_en: str
    pay_url: str


TRIAL_DAYS = 7
TRIAL_PRICE_RUB = "25 руб"

PLANS = [
    Plan(
        code="trial",
        title_ru="Пробный период",
        title_en="Trial period",
        price_ru="7 дней (спишем 25 руб)",
        price_en="7 days (25 RUB card check)",
        pay_url="https://example.com/pay/trial",
    ),
    Plan(
        code="1m",
        title_ru="1 мес",
        title_en="1 month",
        price_ru="100 руб",
        price_en="100 RUB",
        pay_url="https://example.com/pay/1m",
    ),
    Plan(
        code="3m",
        title_ru="3 мес",
        title_en="3 months",
        price_ru="250 руб",
        price_en="250 RUB",
        pay_url="https://example.com/pay/3m",
    ),
    Plan(
        code="12m",
        title_ru="12 мес",
        title_en="12 months",
        price_ru="900 руб",
        price_en="900 RUB",
        pay_url="https://example.com/pay/12m",
    ),
]

PLAN_DAYS = {
    "trial": 7,
    "1m": 30,
    "3m": 90,
    "12m": 365,
}

DEVICES_RU = [
    ("android", "Android"),
    ("ios", "iOS (iPhone)"),
    ("windows", "Windows"),
    ("macos", "MacOS"),
    ("android_tv", "Android TV"),
    ("apple_tv", "Apple TV"),
    ("linux", "Linux"),
    ("router", "Роутеры"),
]

DEVICES_EN = [
    ("android", "Android"),
    ("ios", "iOS (iPhone)"),
    ("windows", "Windows"),
    ("macos", "MacOS"),
    ("android_tv", "Android TV"),
    ("apple_tv", "Apple TV"),
    ("linux", "Linux"),
    ("router", "Routers"),
]
