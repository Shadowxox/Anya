from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from config import BANNED_USERS


@app.on_message(filters.command("chatinfo") & filters.group & ~BANNED_USERS)
async def chat_info(client, message: Message):

    chat = message.chat

    admins_count = 0

    try:
        admins = []
        async for admin in app.get_chat_members(
            chat.id,
            filter="administrators"
        ):
            admins.append(admin)

        admins_count = len(admins)

    except:
        admins_count = "Unknown"

    try:
        members_count = await app.get_chat_members_count(chat.id)
    except:
        members_count = "Unknown"

    try:
        invite_link = await app.export_chat_invite_link(chat.id)
    except:
        invite_link = "No Permission"

    photo = None

    try:
        if chat.photo:
            photo = await app.download_media(chat.photo.big_file_id)
    except:
        photo = None

    text = (
        "<b>╭━━〔 📜 ᴄʜᴀᴛ ɪɴꜰᴏ 〕━━╮</b>\n\n"

        "<blockquote>"

        f"⌯ <b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> {chat.title}\n"
        f"⌯ <b>ɢʀᴏᴜᴘ ɪᴅ :</b> <code>{chat.id}</code>\n"
        f"⌯ <b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{chat.username if chat.username else 'None'}\n"
        f"⌯ <b>ᴄʜᴀᴛ ᴛʏᴘᴇ :</b> {chat.type}\n"
        f"⌯ <b>ᴍᴇᴍʙᴇʀs :</b> {members_count}\n"
        f"⌯ <b>ᴀᴅᴍɪɴs :</b> {admins_count}\n"
        f"⌯ <b>ɪɴᴠɪᴛᴇ :</b> {invite_link}\n"

        "</blockquote>"
    )

    if photo:

        await message.reply_photo(
            photo=photo,
            caption=text
        )

    else:

        await message.reply_text(text)