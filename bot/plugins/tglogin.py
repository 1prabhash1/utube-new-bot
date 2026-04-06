from pyrogram import filters
from pyrogram.types import Message

from ..utubebot import UtubeBot
from ..services.telegram_login import start_login


@UtubeBot.on_message(filters.command("tglogin"))
async def tglogin(c, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(
            "📱 Usage:\n/tglogin +911234567890"
        )

    phone = m.command[1]
    user_id = m.from_user.id

    try:
        await start_login(user_id, phone)
        await m.reply_text(
            "📩 OTP sent to your Telegram.\n"
            "Send using:\n/tgotp 12345"
        )
    except Exception as e:
        await m.reply_text(f"❌ Failed:\n{e}")
