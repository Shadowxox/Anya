from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from ShrutiMusic.core.mongo import mongodb
from ShrutiMusic.misc import SUDOERS


gmute_db = mongodb.gmuted_users


async def is_gmuted(user_id: int):
    user = await gmute_db.find_one(
        {"user_id": user_id}
    )
    return bool(user)


@app.on_message(filters.command("gmute") & SUDOERS)
async def gmute_user(_, message: Message):

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>❌ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ.</b>"
        )

    user = message.reply_to_message.from_user

    if not user:
        return

    if user.id in SUDOERS:
        return await message.reply_text(
            "<b>❌ ᴄᴀɴ'ᴛ ɢᴍᴜᴛᴇ ꜱᴜᴅᴏᴇʀ.</b>"
        )

    already = await is_gmuted(user.id)

    if already:
        return await message.reply_text(
            "<b>❌ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ɢᴍᴜᴛᴇᴅ.</b>"
        )

    await gmute_db.insert_one(
        {
            "user_id": user.id,
            "name": user.first_name,
        }
    )

    await message.reply_text(
        f"<b>🔇 ɢʟᴏʙᴀʟʟʏ ᴍᴜᴛᴇᴅ :</b>\n\n"
        f"⌯ {user.mention}\n"
        f"⌯ <code>{user.id}</code>"
    )


@app.on_message(filters.command("gunmute") & SUDOERS)
async def gunmute_user(_, message: Message):

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>❌ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ.</b>"
        )

    user = message.reply_to_message.from_user

    if not user:
        return

    already = await is_gmuted(user.id)

    if not already:
        return await message.reply_text(
            "<b>❌ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ɢᴍᴜᴛᴇᴅ.</b>"
        )

    await gmute_db.delete_one(
        {"user_id": user.id}
    )

    await message.reply_text(
        f"<b>🔊 ɢʟᴏʙᴀʟʟʏ ᴜɴᴍᴜᴛᴇᴅ :</b>\n\n"
        f"⌯ {user.mention}\n"
        f"⌯ <code>{user.id}</code>"
    )


@app.on_message(filters.command(["gmuted", "gmuteusers"]) & SUDOERS)
async def gmuted_list(_, message: Message):

    users = gmute_db.find({})

    text = "<b>🔇 ɢᴍᴜᴛᴇᴅ ᴜꜱᴇʀꜱ :</b>\n\n"

    count = 0

    async for user in users:

        count += 1

        text += (
            f"{count}. "
            f"{user.get('name', 'Unknown')} "
            f"(<code>{user['user_id']}</code>)\n"
        )

    if count == 0:
        return await message.reply_text(
            "<b>✅ ɴᴏ ɢᴍᴜᴛᴇᴅ ᴜꜱᴇʀꜱ.</b>"
        )

    await message.reply_text(text)


@app.on_message(group=-1)
async def gmute_watcher(_, message: Message):

    if not message.from_user:
        return

    if message.from_user.id in SUDOERS:
        return

    muted = await is_gmuted(
        message.from_user.id
    )

    if muted:

        try:
            await message.delete()
        except:
            pass