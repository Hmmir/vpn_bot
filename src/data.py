from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    code: str
    title_ru: str
    title_en: str
    price_ru: str
    price_en: str
    pay_url: str


TRIAL_DAYS = 3
TRIAL_PRICE_RUB = "10 ₽"

PLANS = [
    Plan(
        code="trial",
        title_ru="Пробный период",
        title_en="Trial period",
        price_ru="10 ₽ за 3 дня",
        price_en="10 RUB for 3 days",
        pay_url="https://example.com/pay/trial",
    ),
    Plan(
        code="1m",
        title_ru="1 мес",
        title_en="1 month",
        price_ru="199 ₽",
        price_en="199 RUB",
        pay_url="https://example.com/pay/1m",
    ),
    Plan(
        code="3m",
        title_ru="3 мес",
        title_en="3 months",
        price_ru="159 ₽ / мес",
        price_en="159 RUB / mo",
        pay_url="https://example.com/pay/3m",
    ),
    Plan(
        code="12m",
        title_ru="12 мес",
        title_en="12 months",
        price_ru="99 ₽ / мес",
        price_en="99 RUB / mo",
        pay_url="https://example.com/pay/12m",
    ),
]


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
