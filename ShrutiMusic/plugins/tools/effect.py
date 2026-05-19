
from pyrogram import filters
from pyrogram.types import Message

from syncedlyrics import search

from ShrutiMusic import app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.core.mongo import mongodb

from config import BANNED_USERS


# =========================
# Mongo Collections
# =========================

effectsdb = mongodb.effects
loopdb = mongodb.loopmode
vcdb = mongodb.vc247


# =========================
# Audio Effects
# =========================

EFFECTS = {
    "bass": "bass=g=10",
    "nightcore": "asetrate=48000*1.25,atempo=1.1",
    "reverb": "aecho=0.8:0.9:1000:0.3",
    "8d": "apulsator=hz=0.125",
    "slowreverb": "atempo=0.8,aecho=0.8:0.9:1000:0.3",
    "normal": "anull",
}


@app.on_message(filters.command("effect") & ~BANNED_USERS)
async def effect_command(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>🎧 ᴜꜱᴀɢᴇ :</b>\n"
            "<code>/effect bass</code>\n\n"
            "<b>ᴀᴠᴀɪʟᴀʙʟᴇ ᴇꜰꜰᴇᴄᴛꜱ :</b>\n"
            "• ʙᴀꜱꜱ\n"
            "• ɴɪɢʜᴛᴄᴏʀᴇ\n"
            "• ʀᴇᴠᴇʀʙ\n"
            "• 8ᴅ\n"
            "• ꜱʟᴏᴡʀᴇᴠᴇʀʙ\n"
            "• ɴᴏʀᴍᴀʟ"
        )

    chat_id = message.chat.id

    effect = message.command[1].lower()

    if effect not in EFFECTS:
        return await message.reply_text(
            "<b>❌ ɪɴᴠᴀʟɪᴅ ᴇꜰꜰᴇᴄᴛ.</b>"
        )

    await effectsdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"effect": effect}},
        upsert=True
    )

    try:

        await Nand.set_audio_filter(
            chat_id,
            EFFECTS[effect]
        )

    except Exception as e:

        return await message.reply_text(
            f"<b>❌ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )

    await message.reply_text(
        f"<b>✅ ᴀᴜᴅɪᴏ ᴇꜰꜰᴇᴄᴛ ꜱᴇᴛ ᴛᴏ :</b> <code>{effect}</code>"
    )


# =========================
# Lyrics Command
# =========================

@app.on_message(filters.command(["lyrics", "ly"]) & ~BANNED_USERS)
async def lyrics_command(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>🎤 ᴜꜱᴀɢᴇ :</b>\n"
            "<code>/lyrics faded</code>"
        )

    query = message.text.split(None, 1)[1]

    m = await message.reply_text(
        "<b>🔍 ꜱᴇᴀʀᴄʜɪɴɢ ʟʏʀɪᴄꜱ...</b>"
    )

    try:

        lyr = search(query)

        if not lyr:
            return await m.edit_text(
                "<b>❌ ʟʏʀɪᴄꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ.</b>"
            )

        if len(lyr) > 4000:
            lyr = lyr[:4000]

        await m.edit_text(
            f"<b>🎵 ʟʏʀɪᴄꜱ ꜰᴏʀ :</b> <code>{query}</code>\n\n{lyr}"
        )

    except Exception as e:

        await m.edit_text(
            f"<b>❌ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )


# =========================
# Loop Mode
# =========================

@app.on_message(filters.command("loop") & ~BANNED_USERS)
async def loop_command(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>🔁 ᴜꜱᴀɢᴇ :</b>\n"
            "<code>/loop song</code>\n"
            "<code>/loop queue</code>\n"
            "<code>/loop off</code>"
        )

    mode = message.command[1].lower()

    if mode not in ["song", "queue", "off"]:
        return await message.reply_text(
            "<b>❌ ɪɴᴠᴀʟɪᴅ ʟᴏᴏᴘ ᴍᴏᴅᴇ.</b>"
        )

    await loopdb.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"mode": mode}},
        upsert=True
    )

    await message.reply_text(
        f"<b>✅ ʟᴏᴏᴘ ᴍᴏᴅᴇ ꜱᴇᴛ ᴛᴏ :</b> <code>{mode}</code>"
    )


# =========================
# 24/7 Mode
# =========================

@app.on_message(filters.command(["247", "24/7"]) & ~BANNED_USERS)
async def mode_247(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>📡 ᴜꜱᴀɢᴇ :</b>\n"
            "<code>/247 on</code>\n"
            "<code>/247 off</code>"
        )

    mode = message.command[1].lower()

    if mode not in ["on", "off"]:
        return await message.reply_text(
            "<b>❌ ᴜꜱᴇ ᴏɴ / ᴏꜰꜰ.</b>"
        )

    status = True if mode == "on" else False

    await vcdb.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"enabled": status}},
        upsert=True
    )

    if status:

        return await message.reply_text(
            "<b>✅ 24/7 ᴍᴏᴅᴇ ᴇɴᴀʙʟᴇᴅ.</b>\n\n"
            "🎧 ᴠᴄ ɴᴇᴠᴇʀ ʟᴇᴀᴠᴇ ᴡʜᴇɴ ɴᴏ ꜱᴏɴɢ."
        )

    await message.reply_text(
        "<b>❌ 24/7 ᴍᴏᴅᴇ ᴅɪꜱᴀʙʟᴇᴅ.</b>"
    )


# =========================
# Check 24/7
# =========================

async def is_247(chat_id):

    data = await vcdb.find_one(
        {"chat_id": chat_id}
    )

    if not data:
        return False

    return data.get("enabled", False)


# =========================
# Get Loop Mode
# =========================

async def get_loop_mode(chat_id):

    data = await loopdb.find_one(
        {"chat_id": chat_id}
    )

    if not data:
        return "off"

    return data.get("mode", "off")


# =========================
# Get Effect
# =========================

async def get_effect(chat_id):

    data = await effectsdb.find_one(
        {"chat_id": chat_id}
    )

    if not data:
        return "normal"

    return data.get("effect", "normal")