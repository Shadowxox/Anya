from datetime import datetime
import asyncio

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from ShrutiMusic import app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import language
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):

    await message.reply_photo(
        photo=PING_IMG_URL,
        caption=(
            "<b>╭━━〔 ⚡ ᴘɪɴɢ ꜱʏꜱᴛᴇᴍ 〕━━╮</b>\n\n"
            "<blockquote>"
            "⌯ ᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ\n"
            "⌯ ᴛᴏ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴘɪɴɢ"
            "</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚡ ᴄʜᴇᴄᴋ ᴘɪɴɢ",
                        callback_data="check_ping"
                    )
                ]
            ]
        )
    )


@app.on_callback_query(filters.regex("^check_ping$"))
async def ping_callback(client, query: CallbackQuery):

    start = datetime.now()

    loading_frames = [
        "▱▱▱▱▱",
        "▰▱▱▱▱",
        "▰▰▱▱▱",
        "▰▰▰▱▱",
        "▰▰▰▰▱",
        "▰▰▰▰▰",
    ]

    try:

        for frame in loading_frames:

            await query.message.edit_caption(
                caption=(
                    "<b>╭━━〔 ⚡ ᴘɪɴɢɪɴɢ 〕━━╮</b>\n\n"
                    f"<blockquote>\n"
                    f"⌯ {frame}\n"
                    f"⌯ ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛ ꜱᴘᴇᴇᴅ...\n"
                    f"</blockquote>"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⚡ ᴘɪɴɢɪɴɢ...",
                                callback_data="nothing"
                            )
                        ]
                    ]
                )
            )

            await asyncio.sleep(0.08)

    except:
        pass

    pytgping = await Nand.ping()

    UP, CPU, RAM, DISK = await bot_sys_stats()

    resp = (datetime.now() - start).microseconds / 1000

    popup = (
        f"⚡ ᴘɪɴɢ ᴘᴏɴɢ\n\n"
        f"⌯ ᴘɪɴɢ : {resp:.2f} ms\n"
        f"⌯ ᴘʏᴛɢᴄᴀʟʟs : {pytgping} ms"
    )

    await query.answer(
        text=popup,
        show_alert=True
    )

    await query.message.edit_caption(
        caption=(
            "<b>╭━━〔 ✅ ᴘɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ 〕━━╮</b>\n\n"
            "<blockquote>"
            "⌯ ᴘɪɴɢ ᴄʜᴇᴄᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ\n"
            "⌯ ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ"
            "</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚡ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ",
                        callback_data="check_ping"
                    )
                ]
            ]
        )
    )


@app.on_callback_query(filters.regex("^nothing$"))
async def nothing_callback(client, query: CallbackQuery):
    await query.answer()