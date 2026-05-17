import os
import asyncio
import requests

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ShrutiMusic import app


def upload_catbox(file_path):
    try:
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
                timeout=60
            )

        if response.status_code == 200:
            return True, response.text.strip()

        return False, response.text

    except Exception as e:
        return False, str(e)


def upload_ibb(file_path):
    try:
        api_key = "aca47fa434cbaad1f79a740e34db561f"

        with open(file_path, "rb") as file:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={
                    "key": api_key
                },
                files={
                    "image": file
                },
                timeout=60
            )

        data = response.json()

        if data.get("success"):
            return True, data["data"]["url"]

        return False, str(data)

    except Exception as e:
        return False, str(e)


@app.on_message(filters.command(["tgm"]))
async def get_link_group(client, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>❌ Reply To A Media File.</b>"
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
            "<b>❌ Unsupported Media Type.</b>"
        )

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text(
            "<b>❌ File Must Be Under 200MB.</b>"
        )

    msg = await message.reply_text(
        "<b>⚡ Initializing Upload...</b>"
    )

    flash_loading = [
        "⚡",
        "⚡⚡",
        "⚡⚡⚡",
        "⚡⚡⚡⚡",
        "⚡⚡⚡⚡⚡",
    ]

    for _ in range(2):
        for frame in flash_loading:
            try:
                await msg.edit_text(
                    f"<b>📥 Preparing Download...</b>\n\n<code>{frame}</code>"
                )
                await asyncio.sleep(0.07)

            except:
                pass

    async def progress(current, total):
        try:
            percentage = current * 100 / total

            filled = int(percentage // 10)

            bar = "▰" * filled + "▱" * (10 - filled)

            await msg.edit_text(
                f"<b>📥 Downloading Media...</b>\n\n"
                f"<code>{bar}</code>\n"
                f"<b>{percentage:.1f}%</b>"
            )

        except:
            pass

    local_path = None

    try:

        local_path = await media.download(
            progress=progress
        )

        upload_anim = [
            "⬆️",
            "⬆️⬆️",
            "⬆️⬆️⬆️",
            "⬆️⬆️⬆️⬆️",
        ]

        for _ in range(3):
            for anim in upload_anim:
                try:
                    await msg.edit_text(
                        f"<b>Uploading To Server</b>\n\n<code>{anim}</code>"
                    )
                    await asyncio.sleep(0.08)

                except:
                    pass

        success, upload_url = upload_catbox(local_path)

        if not success:

            await msg.edit_text(
                "<b>⚠️ Catbox Failed\n🔄 Trying ImgBB Backup...</b>"
            )

            success, upload_url = upload_ibb(local_path)

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