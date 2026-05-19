import asyncio
import random

from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.core.mongo import mongodb
from config import BANNED_USERS


radio_db = mongodb.radio_24x7


RADIOS = {
    "lofi": {
        "name": "ʟᴏꜰɪ ʀᴀᴅɪᴏ",
        "link": "https://streams.ilovemusic.de/iloveradio17.mp3",
    },
    "anime": {
        "name": "ᴀɴɪᴍᴇ ʀᴀᴅɪᴏ",
        "link": "https://listen.moe/stream",
    },
    "phonk": {
        "name": "ᴘʜᴏɴᴋ ʀᴀᴅɪᴏ",
        "link": "https://stream.zeno.fm/f3wvbbqmdg8uv",
    },
}


async def save_radio(chat_id, radio):
    await radio_db.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "radio": radio
            }
        },
        upsert=True
    )


async def remove_radio(chat_id):
    await radio_db.delete_one(
        {"chat_id": chat_id}
    )


async def get_radio(chat_id):
    return await radio_db.find_one(
        {"chat_id": chat_id}
    )


@app.on_message(
    filters.command(["radio"]) & filters.group & ~BANNED_USERS
)
async def start_radio(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>📻 ᴜꜱᴀɢᴇ :</b>\n\n"
            "<code>/radio lofi</code>\n"
            "<code>/radio anime</code>\n"
            "<code>/radio phonk</code>"
        )

    name = message.command[1].lower()

    if name not in RADIOS:
        return await message.reply_text(
            "<b>❌ ɪɴᴠᴀʟɪᴅ ʀᴀᴅɪᴏ ɴᴀᴍᴇ.</b>\n\n"
            "<b>ᴀᴠᴀɪʟᴀʙʟᴇ :</b>\n"
            "• ʟᴏꜰɪ\n"
            "• ᴀɴɪᴍᴇ\n"
            "• ᴘʜᴏɴᴋ"
        )

    radio = RADIOS[name]

    msg = await message.reply_text(
        f"<b>📡 ʟᴏᴀᴅɪɴɢ {radio['name']}...</b>"
    )

    try:

        await Nand.stream_call(
            message.chat.id,
            radio["link"],
        )

        await save_radio(
            message.chat.id,
            name
        )

        await msg.edit_text(
            "<b>╭━━〔 📻 ʀᴀᴅɪᴏ ꜱᴛᴀʀᴛᴇᴅ 〕━━╮</b>\n\n"
            f"<blockquote>\n"
            f"⌯ <b>ɴᴀᴍᴇ :</b> {radio['name']}\n"
            f"⌯ <b>ꜱᴛᴀᴛᴜꜱ :</b> 24/7 ʟɪᴠᴇ\n"
            f"</blockquote>"
        )

    except Exception as e:

        await msg.edit_text(
            f"<b>❌ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )


@app.on_message(
    filters.command(["stopradio"]) & filters.group & ~BANNED_USERS
)
async def stop_radio(_, message: Message):

    try:

        await Nand.stop_stream(
            message.chat.id
        )

        await remove_radio(
            message.chat.id
        )

        return await message.reply_text(
            "<b>⏹️ ʀᴀᴅɪᴏ ꜱᴛᴏᴘᴘᴇᴅ.</b>"
        )

    except Exception as e:

        return await message.reply_text(
            f"<b>❌ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )


@app.on_message(
    filters.command(["radiolist"]) & filters.group & ~BANNED_USERS
)
async def radio_list(_, message: Message):

    text = (
        "<b>📻 ᴀᴠᴀɪʟᴀʙʟᴇ ʀᴀᴅɪᴏ ꜱᴛᴀᴛɪᴏɴꜱ</b>\n\n"
        "• <b>ʟᴏꜰɪ</b>\n"
        "• <b>ᴀɴɪᴍᴇ</b>\n"
        "• <b>ᴘʜᴏɴᴋ</b>\n\n"
        "<b>ᴜꜱᴀɢᴇ :</b>\n"
        "<code>/radio lofi</code>"
    )

    await message.reply_text(text)


@app.on_message(
    filters.command(["randomradio"]) & filters.group & ~BANNED_USERS
)
async def random_radio(_, message: Message):

    picked = random.choice(
        list(RADIOS.keys())
    )

    radio = RADIOS[picked]

    msg = await message.reply_text(
        f"<b>🎲 ʀᴀɴᴅᴏᴍ ʀᴀᴅɪᴏ :</b> {radio['name']}"
    )

    try:

        await Nand.stream_call(
            message.chat.id,
            radio["link"],
        )

        await save_radio(
            message.chat.id,
            picked
        )

        await msg.edit_text(
            "<b>📻 ʀᴀɴᴅᴏᴍ ʀᴀᴅɪᴏ ꜱᴛᴀʀᴛᴇᴅ.</b>"
        )

    except Exception as e:

        await msg.edit_text(
            f"<b>❌ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )


@app.on_message(
    filters.command(["24x7radio"]) & filters.group & ~BANNED_USERS
)
async def radio_24x7(_, message: Message):

    data = await get_radio(
        message.chat.id
    )

    if not data:
        return await message.reply_text(
            "<b>❌ ɴᴏ ᴀᴄᴛɪᴠᴇ ʀᴀᴅɪᴏ.</b>"
        )

    radio_name = data["radio"]

    radio = RADIOS[radio_name]

    try:

        await Nand.stream_call(
            message.chat.id,
            radio["link"],
        )

        await message.reply_text(
            "<b>♻️ 24/7 ʀᴀᴅɪᴏ ʀᴇꜱᴜᴍᴇᴅ.</b>"
        )

    except Exception as e:

        await message.reply_text(
            f"<b>❌ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )