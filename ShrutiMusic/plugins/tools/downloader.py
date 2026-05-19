from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app

import requests
import os
import uuid
import asyncio


API_URL = "https://allvideodownloader.cc/wp-json/aio-dl/video-data/"

TOKEN = "c99f113fab0762d216b4545e5c3d615eefb30f0975fe107caab629d17e51b52d"


@app.on_message(filters.command(["vid", "ig", "pin"]))
async def universal_downloader(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>❌ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ʟɪɴᴋ.</b>\n\n"
            "<code>/vid link</code>\n"
            "<code>/ig link</code>\n"
            "<code>/pin link</code>"
        )

    url = message.text.split(None, 1)[1]

    msg = await message.reply_text(
        "<b>🔍 ꜰᴇᴛᴄʜɪɴɢ ᴍᴇᴅɪᴀ...</b>"
    )

    payload = {
        "url": url,
        "token": TOKEN
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.post(
            API_URL,
            data=payload,
            headers=headers
        )

        data = r.json()

        medias = data.get("medias")

        if not medias:
            return await msg.edit_text(
                "<b>❌ ɴᴏ ᴍᴇᴅɪᴀ ꜰᴏᴜɴᴅ.</b>"
            )

        best_media = medias[0]

        media_url = best_media.get("url")

        ext = best_media.get("extension", "mp4").lower()

        title = data.get("title", "Media")

        file_name = f"{uuid.uuid4()}.{ext}"

        await msg.edit_text(
            "<b>⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>"
        )

        with requests.get(media_url, stream=True) as response:

            if response.status_code != 200:
                return await msg.edit_text(
                    "<b>❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.</b>"
                )

            with open(file_name, "wb") as f:

                for chunk in response.iter_content(chunk_size=8192):

                    if chunk:
                        f.write(chunk)

        if not os.path.exists(file_name):
            return await msg.edit_text(
                "<b>❌ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ.</b>"
            )

        if os.path.getsize(file_name) == 0:

            os.remove(file_name)

            return await msg.edit_text(
                "<b>❌ ᴇᴍᴘᴛʏ ꜰɪʟᴇ.</b>"
            )

        await msg.delete()

        if ext in ["jpg", "jpeg", "png", "webp"]:

            await app.send_photo(
                chat_id=message.chat.id,
                photo=file_name,
                caption=f"<b>📸 {title}</b>"
            )

        else:

            await app.send_video(
                chat_id=message.chat.id,
                video=file_name,
                caption=f"<b>🎬 {title}</b>",
                supports_streaming=True
            )

        os.remove(file_name)

    except Exception as e:

        await msg.edit_text(
            f"<b>❌ Error :</b>\n<code>{e}</code>"
        )