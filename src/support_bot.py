import asyncio
import logging
from typing import Dict, Optional

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from .config import SUPPORT_BOT_TOKEN, SUPPORT_ADMIN_CHAT_ID, SUPPORT_ADMIN_IDS, BRAND_NAME


router = Router()
logging.basicConfig(level=logging.INFO)
user_lang: Dict[int, str] = {}


def detect_lang(message: Message) -> str:
    code = (message.from_user.language_code or "").lower()
    return "en" if code.startswith("en") else "ru"


def is_admin_message(message: Message) -> bool:
    if SUPPORT_ADMIN_CHAT_ID and message.chat.id == SUPPORT_ADMIN_CHAT_ID:
        return True
    return message.from_user.id in SUPPORT_ADMIN_IDS


def admin_targets() -> list[int]:
    if SUPPORT_ADMIN_CHAT_ID:
        return [SUPPORT_ADMIN_CHAT_ID]
    return list(SUPPORT_ADMIN_IDS)


def format_user_header(user: Message) -> str:
    tg = user.from_user
    username = f"@{tg.username}" if tg.username else "—"
    return (
        "Новая заявка в поддержку\n"
        f"Имя: {tg.full_name}\n"
        f"Username: {username}\n"
        f"ID: {tg.id}"
    )


@router.message(CommandStart())
async def support_start(message: Message) -> None:
    lang = detect_lang(message)
    user_lang[message.from_user.id] = lang
    if lang == "en":
        text = (
            f"Welcome to {BRAND_NAME} Support.\n"
            "Send your message and we will reply soon."
        )
    else:
        text = (
            f"Здравствуйте! Это поддержка {BRAND_NAME}.\n"
            "Опишите проблему или вопрос — мы ответим в ближайшее время."
        )
    await message.answer(text)


@router.message(Command("reply"))
async def admin_reply(message: Message) -> None:
    if not is_admin_message(message):
        return
    parts = (message.text or "").split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Формат: /reply USER_ID текст ответа")
        return
    try:
        target_id = int(parts[1])
    except ValueError:
        await message.answer("USER_ID должен быть числом.")
        return
    await message.bot.send_message(target_id, parts[2])
    await message.answer("Отправлено.")


@router.message(F.reply_to_message)
async def admin_reply_to_forward(message: Message) -> None:
    if not is_admin_message(message):
        return
    reply = message.reply_to_message
    if not reply or not reply.forward_from:
        return
    target_id = reply.forward_from.id
    await message.bot.send_message(target_id, message.text or "")


@router.message()
async def relay_user_message(message: Message) -> None:
    if is_admin_message(message):
        return
    targets = admin_targets()
    if not targets:
        await message.answer("Поддержка пока не настроена. Попробуйте позже.")
        return
    header = format_user_header(message)
    for chat_id in targets:
        await message.bot.send_message(chat_id, header)
        await message.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )
    await message.answer("Спасибо! Мы получили сообщение и скоро ответим.")


async def main() -> None:
    if not SUPPORT_BOT_TOKEN:
        raise RuntimeError("SUPPORT_BOT_TOKEN is missing")
    if not SUPPORT_ADMIN_CHAT_ID and not SUPPORT_ADMIN_IDS:
        raise RuntimeError("Support admin chat or IDs are missing")
    bot = Bot(SUPPORT_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
