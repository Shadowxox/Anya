from pyrogram import filters
from pyrogram.types import Message
import os
import platform
import socket
import requests
import psutil

from ShrutiMusic import app

OWNER_ID = 8982722712


def detect_platform():
    env = os.environ

    platforms = {
        "Render": "RENDER",
        "Railway": "RAILWAY_STATIC_URL",
        "Koyeb": "KOYEB_PUBLIC_DOMAIN",
        "Heroku": "DYNO",
        "Replit": "REPL_ID",
        "Fly.io": "FLY_APP_NAME",
        "Glitch": "PROJECT_DOMAIN",
        "Oracle Cloud": "OCI_COMPARTMENT_ID",
        "Google Colab": "COLAB_GPU",
    }

    for name, key in platforms.items():
        if key in env:
            return name

    if os.path.exists("/.dockerenv"):
        return "Docker Container"

    return "Unknown VPS / Localhost"

def get_public_ip():
    try:
        return requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text
    except:
        return "Unknown"


def get_system_info():
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    text = f"""
╭─❍ ʜᴏsᴛ ɪɴғᴏ
│
├ 🖥 ᴘʟᴀᴛғᴏʀᴍ: `{detect_platform()}`
├ 💻 ᴏs: `{platform.system()} {platform.release()}`
├ 🧠 ᴄᴘᴜ ᴄᴏʀᴇs: `{psutil.cpu_count()}`
├ 🐍 ᴘʏᴛʜᴏɴ: `{platform.python_version()}`
│
├ 💾 ʀᴀᴍ ᴜsᴇᴅ: `{round(ram.used / (1024**3), 2)} GB`
├ 💾 ʀᴀᴍ ᴛᴏᴛᴀʟ: `{round(ram.total / (1024**3), 2)} GB`
│
├ 📂 ᴅɪsᴋ ᴜsᴇᴅ: `{round(disk.used / (1024**3), 2)} GB`
├ 📂 ᴅɪsᴋ ᴛᴏᴛᴀʟ: `{round(disk.total / (1024**3), 2)} GB`
│
├ 🌐 ᴘᴜʙʟɪᴄ ɪᴘ: `{get_public_ip()}`
├ 🏷 ʜᴏsᴛɴᴀᴍᴇ: `{socket.gethostname()}`
│
╰───────────────
"""
    return text


@app.on_message(filters.command("hostinfo"))
async def hostinfo_command(_, message: Message):

    user_id = message.from_user.id

    if isinstance(OWNER_ID, list):
        if user_id not in OWNER_ID:
            return
    else:
        if user_id != OWNER_ID:
            return

    await message.reply_text(
        get_system_info()
    )