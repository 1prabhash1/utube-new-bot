import os
import requests

from pyrogram import filters
from pyrogram.types import Message

from ..utubebot import UtubeBot
from ..services.user_service import is_verified
from ..services.telegram_login import get_client


DOWNLOAD_DIR = "downloads"


@UtubeBot.on_message(filters.command("uploadurl"))
async def upload_url(c: UtubeBot, m: Message):
    user_id = m.from_user.id

    # ================= VERIFY USER =================
    if not is_verified(user_id):
        return await m.reply_text(
            "❌ You are not verified.\nUse /verify first."
        )

    # ================= CHECK URL =================
    if len(m.command) < 2:
        return await m.reply_text(
            "❌ Usage:\n/uploadurl <url>"
        )

    url = m.command[1].strip()

    await m.reply_text("🔍 Processing URL...")

    # ================= TELEGRAM LINK =================
    if "t.me" in url:
        client = get_client(user_id)

        if not client:
            return await m.reply_text(
                "❌ You need to login your Telegram account.\n"
                "Use:\n/tglogin +911234567890"
            )

        try:
            await m.reply_text("📥 Downloading from Telegram...")

            # handle different telegram link formats
            if "/c/" in url:
                # private channel link
                parts = url.split("/")
                chat_id = int("-100" + parts[-2])
                message_id = int(parts[-1])
            else:
                # public link
                parts = url.split("/")
                chat_id = parts[-2]
                message_id = int(parts[-1])

            msg = await client.get_messages(chat_id, message_id)

            if not msg:
                return await m.reply_text("❌ Message not found")

            if not msg.media:
                return await m.reply_text("❌ No downloadable media in message")

            os.makedirs(DOWNLOAD_DIR, exist_ok=True)

            file_path = await msg.download(file_name=DOWNLOAD_DIR)

            await m.reply_text(f"✅ Downloaded from Telegram:\n{file_path}")

            # 👉 You can call YouTube upload here later

        except Exception as e:
            await m.reply_text(f"❌ Telegram download failed:\n{e}")

        return

    # ================= NORMAL URL =================
    try:
        await m.reply_text("📥 Downloading from URL...")

        response = requests.get(url, stream=True, timeout=30)

        if response.status_code != 200:
            return await m.reply_text("❌ Failed to fetch file")

        filename = url.split("/")[-1] or "file.mp4"

        # clean filename
        filename = filename.split("?")[0]

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        await m.reply_text(f"✅ Downloaded from URL:\n{filepath}")

        # 👉 YouTube upload can be added here

    except Exception as e:
        await m.reply_text(f"❌ Download failed:\n{e}")
