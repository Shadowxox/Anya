from pyrogram.types import InlineKeyboardButton
import config
from ShrutiMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me{app.username}?startgroup=true",
                style="positive"  # <-- Isse ye button GREEN dikhega
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_11"],
                callback_data="about_page"
            ),
            InlineKeyboardButton(
                text=_["S_B_5"],
                user_id=config.OWNER_ID,
                style="primary"   # <-- Default Blue/Theme colour
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="help_page_1"
            )
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me{app.username}?startgroup=true",
                style="positive"  # <-- GREEN Colour
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_11"],
                callback_data="about_page"
            ),
            InlineKeyboardButton(
                text=_["S_B_5"],
                user_id=config.OWNER_ID
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="help_page_1"
            )
        ],
    ]
    return buttons


def about_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_6"],
                url=config.SUPPORT_CHANNEL
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_GROUP
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settingsback_helper",
                style="destructive"  # <-- Isse Back button RED dikhega
            ),
            InlineKeyboardButton(
                text="➕ Add Me",
                url=f"https://t.me{app.username}?startgroup=true",
                style="positive"     # <-- GREEN Colour
            ),
        ]
    ]
    return buttons
