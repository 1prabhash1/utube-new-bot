from pyrogram import filters
from pyrogram.types import Message

from ..utubebot import UtubeBot
from ..services.telegram_login import verify_code


@UtubeBot.on_message(filters.command("tgotp"))
async def tgotp(c, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("❌ Usage: /tgotp 12345")

    code = m.command[1]
    user_id = m.from_user.id

    if await verify_code(user_id, code):
        await m.reply_text("✅ Telegram account logged in!")
    else:
        await m.reply_text("❌ Invalid OTP")
