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
            "⌯ ᴛᴏ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴘɪɴɢ & ꜱᴛᴀᴛᴜꜱ"
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
                text=f"⚡ ᴘɪɴɢɪɴɢ... {frame}",
                show_alert=False
            )
            await asyncio.sleep(0.08)
        except:
            pass

    pytgping = await Nand.ping()

    UP, CPU, RAM, DISK = await bot_sys_stats()

    resp = (datetime.now() - start).microseconds / 1000

    popup = (
        f"⚡ ᴘɪɴɢ ᴘᴏɴɢ\n\n"
        f"⌯ ᴘɪɴɢ : {resp:.3f} ms\n"
        f"⌯ ᴘʏᴛɢᴄᴀʟʟs : {pytgping} ms\n"
        f"⌯ ᴄᴘᴜ : {CPU}\n"
        f"⌯ ʀᴀᴍ : {RAM}\n"
        f"⌯ ᴅɪꜱᴋ : {DISK}"
    )

    await query.answer(
        text=popup[:190],
        show_alert=True
    )