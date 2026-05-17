import os
import asyncio
import requests

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ShrutiMusic import app


def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"

    data = {
        "reqtype": "fileupload"
    }

    with open(file_path, "rb") as f:
        files = {
            "fileToUpload": f
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(
            url,
            data=data,
            files=files,
            headers=headers,
        )

    if response.status_code == 200:
        return True, response.text.strip()

    return False, f"Error: {response.status_code} - {response.text}"


@app.on_message(filters.command(["tgm"]))
async def get_link_group(client, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "❌ Reply to a media file."
        )

    media = message.reply_to_message

    file_size = 0

    if media.photo:
        file_size = media.photo.file_size

    elif media.video:
        file_size = media.video.file_size

    elif media.document:
        file_size = media.document.file_size

    else:
        return await message.reply_text(
            "❌ Unsupported media type."
        )

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text(
            "❌ File must be under 200MB."
        )

    msg = await message.reply_text(
        "<b>🚀 Initializing Upload...</b>"
    )

    loading = [
        "▰▱▱▱▱▱▱▱▱▱",
        "▰▰▱▱▱▱▱▱▱▱",
        "▰▰▰▱▱▱▱▱▱▱",
        "▰▰▰▰▱▱▱▱▱▱",
        "▰▰▰▰▰▱▱▱▱▱",
        "▰▰▰▰▰▰▱▱▱▱",
        "▰▰▰▰▰▰▰▱▱▱",
        "▰▰▰▰▰▰▰▰▱▱",
        "▰▰▰▰▰▰▰▰▰▱",
        "▰▰▰▰▰▰▰▰▰▰",
    ]

    for frame in loading:
        try:
            await msg.edit_text(
                f"<b>📥 Preparing Download...</b>\n\n<code>{frame}</code>"
            )
            await asyncio.sleep(0.15)

        except:
            pass

    async def progress(current, total):
        try:
            percentage = current * 100 / total

            bar_filled = int(percentage // 10)
            bar = "▰" * bar_filled + "▱" * (10 - bar_filled)

            await msg.edit_text(
                f"<b>📥 Downloading File...</b>\n\n"
                f"<code>{bar}</code>\n"
                f"<b>{percentage:.1f}%</b>"
            )

        except:
            pass

    local_path = None

    try:
        local_path = await media.download(progress=progress)

        upload_animation = [
            "⬆️ Uploading.",
            "⬆️ Uploading..",
            "⬆️ Uploading...",
        ]

        for _ in range(3):
            for anim in upload_animation:
                try:
                    await msg.edit_text(
                        f"<b>{anim}</b>"
                    )
                    await asyncio.sleep(0.4)

                except:
                    pass

        success, upload_url = upload_file(local_path)

        if success:

            await msg.edit_text(
                f"<b>✅ Upload Successful</b>\n\n"
                f"🌐 <a href='{upload_url}'>Tap Here To Open File</a>",
                disable_web_page_preview=False,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🌍 Open Link",
                                url=upload_url
                            )
                        ]
                    ]
                ),
            )

        else:

            await msg.edit_text(
                f"<b>❌ Upload Failed</b>\n\n"
                f"<code>{upload_url}</code>"
            )

    except Exception as e:

        await msg.edit_text(
            f"<b>❌ File Upload Failed</b>\n\n"
            f"<code>{e}</code>"
        )

    finally:

        try:
            if local_path and os.path.exists(local_path):
                os.remove(local_path)

        except:
            pass