import asyncio
import os
import shutil
import socket
from datetime import datetime
import sys

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

    response = await message.reply_text(
        "<b>⚡ ᴄʜᴇᴄᴋɪɴɢ ꜰᴏʀ ᴜᴘᴅᴀᴛᴇꜱ...</b>"
    )

    try:
        repo = Repo()

    except InvalidGitRepositoryError:
        return await response.edit_text(
            "<b>❌ ɪɴᴠᴀʟɪᴅ ɢɪᴛ ʀᴇᴘᴏ.</b>"
        )

    except GitCommandError as e:
        return await response.edit_text(
            f"<b>❌ ɢɪᴛ ᴇʀʀᴏʀ :</b>\n<code>{e}</code>"
        )

    origin = repo.remotes.origin

    try:
        origin.fetch()

    except Exception as e:
        return await response.edit_text(
            f"<b>❌ ꜰᴇᴛᴄʜ ꜰᴀɪʟᴇᴅ :</b>\n<code>{e}</code>"
        )

    commits = list(
        repo.iter_commits(
            f"HEAD..origin/{config.UPSTREAM_BRANCH}"
        )
    )

    if not commits:
        return await response.edit_text(
            "<b>✅ ʙᴏᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴜᴘ ᴛᴏ ᴅᴀᴛᴇ.</b>"
        )

    changelog = ""

    for commit in commits[:10]:

        changelog += (
            f"• <b>{commit.summary}</b>\n"
            f"⌯ {commit.author}\n"
            f"⌯ {datetime.fromtimestamp(commit.committed_date).strftime('%d %b %Y')}\n\n"
        )

    await response.edit_text(
        "<b>⚡ ɴᴇᴡ ᴜᴘᴅᴀᴛᴇ ꜰᴏᴜɴᴅ</b>\n\n"
        f"{changelog}"
    )

    await asyncio.sleep(2)

    await response.edit_text(
        "<b>⬇️ ᴘᴜʟʟɪɴɢ ᴜᴘᴅᴀᴛᴇꜱ...</b>"
    )

    try:

        repo.git.reset("--hard")
        repo.git.pull(
            "origin",
            config.UPSTREAM_BRANCH
        )

    except Exception as e:

        return await response.edit_text(
            f"<b>❌ ɢɪᴛ ᴘᴜʟʟ ꜰᴀɪʟᴇᴅ :</b>\n<code>{e}</code>"
        )

    await response.edit_text(
        "<b>📦 ɪɴꜱᴛᴀʟʟɪɴɢ ᴘᴀᴄᴋᴀɢᴇꜱ...</b>"
    )

    os.system("pip3 install -U -r requirements.txt")

    await asyncio.sleep(2)

    await response.edit_text(
        "<b>🚀 ʀᴇꜱᴛᴀʀᴛɪɴɢ ʙᴏᴛ...</b>"
    )

    os.execl(
        sys.executable,
        sys.executable,
        "-m",
        "ShrutiMusic"
    )



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