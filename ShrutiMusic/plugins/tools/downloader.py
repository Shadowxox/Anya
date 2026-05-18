from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from ShrutiMusic import app

import requests
import os
import asyncio


TEMP_VIDEOS = {}


@app.on_message(filters.command("vid"))
async def video_downloader(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>❌ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ʟɪɴᴋ.</b>\n\n"
            "<code>/vid url</code>"
        )

    video_url = message.text.split(None, 1)[1]

    msg = await message.reply_text(
        "<b>🔍 ꜰᴇᴛᴄʜɪɴɢ ᴍᴇᴅɪᴀ...</b>"
    )

    payload = {
        "url": video_url,
        "token": "c99f113fab0762d216b4545e5c3d615eefb30f0975fe107caab629d17e51b52d"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.post(
            "https://allvideodownloader.cc/wp-json/aio-dl/video-data/",
            data=payload,
            headers=headers
        )

        data = r.json()

        if "medias" not in data or not data["medias"]:
            return await msg.edit_text(
                "<b>❌ ɴᴏ ᴍᴇᴅɪᴀ ꜰᴏᴜɴᴅ.</b>"
            )

        medias = data["medias"]

        best_media = sorted(
            medias,
            key=lambda x: str(x.get("quality", "")),
            reverse=True
        )[0]

        media_link = best_media["url"]

        thumb = data.get("thumbnail")

        title = data.get("title", "Media")

        ext = best_media.get("extension", "mp4")

        TEMP_VIDEOS[message.from_user.id] = {
            "url": media_link,
            "title": title,
            "ext": ext
        }

        await msg.delete()

        media_type = "📸 ɪᴍᴀɢᴇ" if ext in ["jpg", "jpeg", "png", "webp"] else "🎬 ᴠɪᴅᴇᴏ"

        await message.reply_photo(
            photo=thumb,
            caption=(
                f"<b>╭━━〔 {media_type} ꜰᴏᴜɴᴅ 〕━━╮</b>\n\n"
                f"<blockquote>\n"
                f"⌯ <b>ᴛɪᴛʟᴇ :</b> {title}\n"
                f"⌯ <b>Qᴜᴀʟɪᴛʏ :</b> {best_media.get('quality', 'Unknown')}\n"
                f"⌯ <b>ᴛʏᴘᴇ :</b> {ext.upper()}\n"
                f"</blockquote>\n\n"
                f"<b>⌯ ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ</b>"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⬇️ ᴅᴏᴡɴʟᴏᴀᴅ",
                            callback_data=f"download_video_{message.from_user.id}"
                        )
                    ]
                ]
            )
        )

    except Exception as e:

        await msg.edit_text(
            f"<b>❌ Error :</b>\n<code>{e}</code>"
        )


@app.on_callback_query(filters.regex("^download_video_"))
async def download_video_callback(client, query: CallbackQuery):

    user_id = int(query.data.split("_")[-1])

    if query.from_user.id != user_id:
        return await query.answer(
            "❌ ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ʏᴏᴜʀ ᴍᴇᴅɪᴀ.",
            show_alert=True
        )

    if user_id not in TEMP_VIDEOS:
        return await query.answer(
            "❌ ᴍᴇᴅɪᴀ ᴇxᴘɪʀᴇᴅ.",
            show_alert=True
        )

    data = TEMP_VIDEOS[user_id]

    media_url = data["url"]
    title = data["title"]
    ext = data["ext"]

    loading = [
        "▱▱▱▱▱",
        "▰▱▱▱▱",
        "▰▰▱▱▱",
        "▰▰▰▱▱",
        "▰▰▰▰▱",
        "▰▰▰▰▰",
    ]

    for frame in loading:
        try:
            await query.answer(
                f"⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...\n{frame}",
                show_alert=False
            )
            await asyncio.sleep(0.05)
        except:
            pass

    file_name = f"{user_id}.{ext}"

    try:

        await query.edit_message_caption(
            caption="<b>⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ...</b>"
        )

        with requests.get(media_url, stream=True) as v:

            with open(file_name, "wb") as f:

                for chunk in v.iter_content(chunk_size=8192):
                    f.write(chunk)

        await query.message.delete()

        if ext.lower() in ["jpg", "jpeg", "png", "webp"]:

            await app.send_photo(
                chat_id=query.message.chat.id,
                photo=file_name,
                caption=(
                    f"<b>╭━━〔 📸 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ 〕━━╮</b>\n\n"
                    f"<blockquote>\n"
                    f"⌯ <b>{title}</b>\n"
                    f"</blockquote>"
                )
            )

        else:

            await app.send_video(
                chat_id=query.message.chat.id,
                video=file_name,
                caption=(
                    f"<b>╭━━〔 🎬 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ 〕━━╮</b>\n\n"
                    f"<blockquote>\n"
                    f"⌯ <b>{title}</b>\n"
                    f"</blockquote>"
                ),
                supports_streaming=True
            )

        os.remove(file_name)

        del TEMP_VIDEOS[user_id]

    except Exception as e:

        await query.message.reply_text(
            f"<b>❌ Error :</b>\n<code>{e}</code>"
        )







from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from ShrutiMusic import app

REPO_VIDEO = "https://files.catbox.moe/aoafwn.mp4"


@app.on_message(filters.command(["repo", "source"]))
async def send_repo(_, message: Message):
    await message.reply_video(
        video=REPO_VIDEO,
        caption="<b>🎥 Tap the button below 👇</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "😮‍💨 Tap Button",
                        callback_data="tap_button"
                    )
                ]
            ]
        ),
        supports_streaming=True,
    )


@app.on_callback_query(filters.regex("tap_button"))
async def tap_button_callback(_, query: CallbackQuery):
    await query.answer("FUCK U 😮‍💨", show_alert=True)