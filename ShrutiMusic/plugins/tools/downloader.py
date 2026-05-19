from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app

import http.client
import json
import os
import uuid


API_TOKEN = "255|jPEBmEeCxHz3hV63Z680uq5nEUDOYKfNLxtFmuGV"


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

    try:

        conn = http.client.HTTPSConnection("flashapi.ru")

        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        endpoint = f"/api/download?url={url}"

        conn.request("GET", endpoint, headers=headers)

        res = conn.getresponse()

        data = res.read().decode("utf-8")

        response = json.loads(data)

        if not response.get("status"):

            return await msg.edit_text(
                "<b>❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ᴍᴇᴅɪᴀ.</b>"
            )

        media = response.get("result")

        if not media:

            return await msg.edit_text(
                "<b>❌ ɴᴏ ᴍᴇᴅɪᴀ ꜰᴏᴜɴᴅ.</b>"
            )

        media_url = media.get("url")

        title = media.get("title", "Media")

        ext = media_url.split(".")[-1].split("?")[0].lower()

        file_name = f"{uuid.uuid4()}.{ext}"

        await msg.edit_text(
            "<b>⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>"
        )

        import requests

        r = requests.get(media_url, stream=True)

        if r.status_code != 200:

            return await msg.edit_text(
                "<b>❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.</b>"
            )

        with open(file_name, "wb") as f:

            for chunk in r.iter_content(chunk_size=8192):

                if chunk:
                    f.write(chunk)

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