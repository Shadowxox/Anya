import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

import config
from ShrutiMusic import app
from ShrutiMusic.misc import HAPP, SUDOERS, XCB
from ShrutiMusic.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from ShrutiMusic.utils.decorators.language import language
from ShrutiMusic.utils.pastebin import NandBin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()



@app.on_message(filters.command(["getlog", "logs", "getlogs"]) & SUDOERS)
@language
async def log_(client, message, _):

    lol = await message.reply_text(
        "<b>╭────────────────╮\n"
        "│ 📂 ᴄʜᴇᴄᴋɪɴɢ ʟᴏɢs...\n"
        "╰────────────────╯</b>"
    )

    animation = [
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

    for i in animation:
        await lol.edit_text(
            f"<b>📤 ᴜᴘʟᴏᴀᴅɪɴɢ ʟᴏɢ ғɪʟᴇ...</b>\n\n<code>{i}</code>"
        )
        await asyncio.sleep(0.3)

    try:
        await message.reply_document(
            document="log.txt",
            caption=(
                "<b>✨ ʜᴇʀᴇ ᴀʀᴇ ʏᴏᴜʀ ʙᴏᴛ ʟᴏɢs ✨</b>\n\n"
                "📂 ᴜsᴇ ᴛʜᴇᴍ ᴛᴏ ꜰɪx ᴇʀʀᴏʀs & ᴄʀᴀsʜᴇs."
            )
        )

        await lol.delete()

    except:
        await lol.edit_text(
            "<b>❌ ɴᴏ ʟᴏɢ ꜰɪʟᴇ ꜰᴏᴜɴᴅ.</b>"
        )



@app.on_message(filters.command(["update", "gitpull"]) & SUDOERS)
@language
async def update_(client, message, _):

    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(
                "<b>❌ ʜᴇʀᴏᴋᴜ ᴀᴘᴘ ɴᴏᴛ ᴄᴏɴꜰɪɢᴜʀᴇᴅ.</b>"
            )

    response = await message.reply_text(
        "<b>╭──────────────────╮\n"
        "│ ⚡ sᴛᴀʀᴛɪɴɢ ɢɪᴛᴘᴜʟʟ...\n"
        "╰──────────────────╯</b>"
    )

    loading_frames = [
        "◍━━━━━━━",
        "◍◍━━━━━━",
        "◍◍◍━━━━━",
        "◍◍◍◍━━━━",
        "◍◍◍◍◍━━━",
        "◍◍◍◍◍◍━━",
        "◍◍◍◍◍◍◍━",
        "◍◍◍◍◍◍◍◍",
    ]

    loading_texts = [
        "🔍 ᴄʜᴇᴄᴋɪɴɢ ꜰᴏʀ ᴜᴘᴅᴀᴛᴇs...",
        "📡 ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ɢɪᴛʜᴜʙ...",
        "⚙️ ꜰᴇᴛᴄʜɪɴɢ ʟᴀᴛᴇsᴛ ᴄᴏᴍᴍɪᴛs...",
        "🚀 ᴘʀᴇᴘᴀʀɪɴɢ ᴜᴘᴅᴀᴛᴇ...",
    ]

    for txt in loading_texts:
        for frame in loading_frames:
            await response.edit_text(
                f"<b>{txt}</b>\n\n<code>{frame}</code>"
            )
            await asyncio.sleep(0.2)

    try:
        repo = Repo()

    except GitCommandError:
        return await response.edit(
            "<b>❌ ɢɪᴛ ᴇʀʀᴏʀ.</b>"
        )

    except InvalidGitRepositoryError:
        return await response.edit(
            "<b>❌ ɪɴᴠᴀʟɪᴅ ɢɪᴛ ʀᴇᴘᴏ.</b>"
        )

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null")

    verification = ""

    REPO_ = repo.remotes.origin.url.split(".git")[0]

    for checks in repo.iter_commits(
        f"HEAD..origin/{config.UPSTREAM_BRANCH}"
    ):
        verification = str(checks.count())

    if verification == "":
        return await response.edit(
            "<b>✅ ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴜᴘ ᴛᴏ ᴅᴀᴛᴇ.</b>"
        )

    updates = ""

    for info in repo.iter_commits(
        f"HEAD..origin/{config.UPSTREAM_BRANCH}"
    ):

        updates += (
            f"➣ <b>{info.summary}</b>\n"
            f"👤 {info.author}\n"
            f"🕒 "
            f"{datetime.fromtimestamp(info.committed_date).strftime('%d %b %Y')}\n\n"
        )

    if len(updates) > 3500:

        url = await NandBin(updates)

        await response.edit_text(
            "<b>⚡ ɴᴇᴡ ᴜᴘᴅᴀᴛᴇ ꜰᴏᴜɴᴅ ⚡</b>\n\n"
            f"📜 <a href={url}>ᴄʜᴇᴄᴋ ᴄʜᴀɴɢᴇʟᴏɢ</a>"
        )

    else:

        await response.edit_text(
            "<b>⚡ ɴᴇᴡ ᴜᴘᴅᴀᴛᴇ ꜰᴏᴜɴᴅ ⚡</b>\n\n"
            "<b>📜 ᴄʜᴀɴɢᴇʟᴏɢ :</b>\n\n"
            f"{updates}",
            disable_web_page_preview=True,
        )

    await asyncio.sleep(3)

    await response.edit_text(
        "<b>⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴜᴘᴅᴀᴛᴇs...</b>"
    )

    os.system("git stash &> /dev/null && git pull")

    await asyncio.sleep(2)

    try:

        served_chats = await get_active_chats()

        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text=(
                        f"{app.mention} "
                        "ɪs ᴜᴘᴅᴀᴛɪɴɢ...\n\n"
                        "⏳ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ 10-15 sᴇᴄᴏɴᴅs."
                    ),
                )

                await remove_active_chat(x)
                await remove_active_video_chat(x)

            except:
                pass

    except:
        pass

    await response.edit_text(
        "<b>📦 ɪɴsᴛᴀʟʟɪɴɢ ɴᴇᴡ ᴘᴀᴄᴋᴀɢᴇs...</b>"
    )

    os.system("pip3 install -r requirements.txt")

    await asyncio.sleep(2)

    await response.edit_text(
        "<b>🚀 ʀᴇsᴛᴀʀᴛɪɴɢ ʙᴏᴛ...</b>\n\n"
        "⏳ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ 10-15 sᴇᴄᴏɴᴅs."
    )

    if await is_heroku():

        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}"
                f"{XCB[0]*2}{XCB[6]}{XCB[4]}"
                f"{XCB[8]}{XCB[1]}{XCB[5]}"
                f"{XCB[2]}{XCB[6]}{XCB[2]}"
                f"{XCB[3]}{XCB[0]}{XCB[10]}"
                f"{XCB[2]}{XCB[5]} "
                f"{XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return

        except Exception as err:

            await response.edit_text(
                f"<b>❌ ʜᴇʀᴏᴋᴜ ʀᴇsᴛᴀʀᴛ ꜰᴀɪʟᴇᴅ.</b>\n\n<code>{err}</code>"
            )

            return await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"🚨 ᴜᴘᴅᴀᴛᴇ ᴇʀʀᴏʀ :\n{err}",
            )

    else:

        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()



@app.on_message(filters.command(["restart"]) & SUDOERS)
async def restart_(_, message):

    response = await message.reply_text(
        "<b>🔄 ʀᴇsᴛᴀʀᴛɪɴɢ ʙᴏᴛ...</b>"
    )

    ac_chats = await get_active_chats()

    for x in ac_chats:

        try:
            await app.send_message(
                chat_id=int(x),
                text=(
                    f"{app.mention} "
                    "ɪs ʀᴇsᴛᴀʀᴛɪɴɢ...\n\n"
                    "⏳ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ 10-15 sᴇᴄᴏɴᴅs."
                ),
            )

            await remove_active_chat(x)
            await remove_active_video_chat(x)

        except:
            pass

    try:
        shutil.rmtree("downloads")
        shutil.rmtree("raw_files")
        shutil.rmtree("cache")

    except:
        pass

    await response.edit_text(
        "<b>🚀 ʀᴇsᴛᴀʀᴛ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ...</b>\n\n"
        "⏳ ᴡᴀɪᴛ ꜰᴏʀ 10-15 sᴇᴄᴏɴᴅs."
    )

    os.system(f"kill -9 {os.getpid()} && bash start")