from pyrogram.types import InlineKeyboardButton
import config
from ShrutiMusic import app


def start_panel(_):
    # 1. Pehle normal buttons banayein
    btn1 = InlineKeyboardButton(text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true")
    btn2 = InlineKeyboardButton(text=_["S_B_11"], callback_data="about_page")
    btn3 = InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID)
    btn4 = InlineKeyboardButton(text=_["S_B_4"], callback_data="help_page_1")

    # 2. Pyrogram ko bypass karke buttons me manually style/color daalein
    btn1.style = "positive"     # Green
    btn3.style = "primary"      # Blue

    # 3. List return karein
    return [[btn1], [btn2, btn3], [btn4]]


def private_panel(_):
    btn1 = InlineKeyboardButton(text=_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true")
    btn2 = InlineKeyboardButton(text=_["S_B_11"], callback_data="about_page")
    btn3 = InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID)
    btn4 = InlineKeyboardButton(text=_["S_B_4"], callback_data="help_page_1")

    # Colors set karein
    btn1.style = "positive"     # Green

    return [[btn1], [btn2, btn3], [btn4]]


def about_panel(_):
    btn1 = InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL)
    btn2 = InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP)
    btn3 = InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")
    btn4 = InlineKeyboardButton(text="➕ Add Me", url=f"https://t.me{app.username}?startgroup=true")

    # Colors set karein
    btn3.style = "destructive"  # Red
    btn4.style = "positive"     # Green

    return [[btn1, btn2], [btn3, btn4]]
