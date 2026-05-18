# =========================
# UPDATED AE STYLE THUMBNAIL
# =========================

import os
import random
import aiohttp
import aiofiles
import traceback
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from py_yt import VideosSearch
from ShrutiMusic import app
import math

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

CANVAS_W, CANVAS_H = 1320, 760

FONT_REGULAR_PATH = "ShrutiMusic/assets/font2.ttf"
FONT_BOLD_PATH = "ShrutiMusic/assets/font3.ttf"

# YOUR CUSTOM LOGO / PFP
BOT_LOGO = "ShrutiMusic/assets/logo.png"

# FALLBACK
DEFAULT_THUMB = "ShrutiMusic/assets/ShrutiBots.jpg"


# =========================
# TEXT WRAP
# =========================
def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word

        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines[:2]


# =========================
# RANDOM THEMES
# =========================
THEMES = [
    {
        "bg1": (18, 10, 40),
        "bg2": (70, 20, 120),
        "accent": (190, 120, 255),
    },
    {
        "bg1": (5, 15, 30),
        "bg2": (20, 80, 150),
        "accent": (80, 180, 255),
    },
    {
        "bg1": (20, 10, 10),
        "bg2": (120, 30, 30),
        "accent": (255, 120, 120),
    },
    {
        "bg1": (5, 25, 10),
        "bg2": (40, 120, 70),
        "accent": (120, 255, 170),
    },
]


# =========================
# GRADIENT BACKGROUND
# =========================
def apply_gradient(theme):
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H))
    draw = ImageDraw.Draw(canvas)

    for y in range(CANVAS_H):
        t = y / CANVAS_H

        r = int(theme["bg1"][0] * (1 - t) + theme["bg2"][0] * t)
        g = int(theme["bg1"][1] * (1 - t) + theme["bg2"][1] * t)
        b = int(theme["bg1"][2] * (1 - t) + theme["bg2"][2] * t)

        draw.line([(0, y), (CANVAS_W, y)], fill=(r, g, b))

    return canvas


# =========================
# GLOW
# =========================
def add_glow(canvas, x, y, w, h, color):
    glow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)

    for i in range(25):
        alpha = max(0, 120 - i * 4)

        gdraw.rounded_rectangle(
            [x - i, y - i, x + w + i, y + h + i],
            radius=35,
            outline=(*color, alpha),
            width=3,
        )

    glow = glow.filter(ImageFilter.GaussianBlur(12))

    canvas.alpha_composite(glow)


# =========================
# PARTICLES
# =========================
def add_particles(draw, accent):
    for _ in range(60):
        x = random.randint(0, CANVAS_W)
        y = random.randint(0, CANVAS_H)

        size = random.randint(2, 5)

        draw.ellipse(
            [x, y, x + size, y + size],
            fill=(*accent, random.randint(50, 180)),
        )


# =========================
# MAIN
# =========================
async def gen_thumb(videoid: str):

    url = f"https://www.youtube.com/watch?v={videoid}"

    thumb_path = None

    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Song")
        duration = result.get("duration", "0:00")
        views = result.get("viewCount", {}).get("short", "0 Views")
        channel = result.get("channel", {}).get("name", "Unknown")

        thumburl = result["thumbnails"][0]["url"].split("?")[0]

        # DOWNLOAD YT THUMB
        async with aiohttp.ClientSession() as session:
            async with session.get(thumburl) as resp:

                if resp.status == 200:

                    thumb_path = CACHE_DIR / f"{videoid}.jpg"

                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())

        if thumb_path and thumb_path.exists():
            yt_thumb = Image.open(thumb_path).convert("RGBA")
        else:
            yt_thumb = Image.open(DEFAULT_THUMB).convert("RGBA")

    except Exception as e:
        print(e)

        yt_thumb = Image.open(DEFAULT_THUMB).convert("RGBA")

        title = "Unknown Song"
        duration = "0:00"
        views = "0 Views"
        channel = "Unknown"


    try:

        # =========================
        # THEME
        # =========================
        theme = random.choice(THEMES)

        canvas = apply_gradient(theme)
        canvas = canvas.convert("RGBA")

        accent = theme["accent"]

        # =========================
        # BIG BACKGROUND THUMB
        # =========================
        bg = yt_thumb.resize((CANVAS_W, CANVAS_H))

        bg = ImageEnhance.Brightness(bg).enhance(0.35)
        bg = bg.filter(ImageFilter.GaussianBlur(8))

        canvas.alpha_composite(bg)

        overlay = Image.new(
            "RGBA",
            (CANVAS_W, CANVAS_H),
            (*theme["bg1"], 120)
        )

        canvas.alpha_composite(overlay)

        draw = ImageDraw.Draw(canvas)

        add_particles(draw, accent)

        # =========================
        # RIGHT SIDE BIG THUMB
        # =========================
        card_w = 430
        card_h = 430

        card_x = CANVAS_W - 500
        card_y = 160

        # GLOW
        add_glow(canvas, card_x, card_y, card_w, card_h, accent)

        thumb_card = yt_thumb.resize((card_w, card_h))

        mask = Image.new("L", (card_w, card_h), 0)

        mdraw = ImageDraw.Draw(mask)

        mdraw.rounded_rectangle(
            [0, 0, card_w, card_h],
            radius=40,
            fill=255,
        )

        thumb_card.putalpha(mask)

        canvas.paste(
            thumb_card,
            (card_x, card_y),
            thumb_card,
        )

        # =========================
        # BOT LOGO LEFT BOTTOM
        # =========================
        if os.path.exists(BOT_LOGO):

            logo = Image.open(BOT_LOGO).convert("RGBA")

            logo_size = 100

            logo = logo.resize((logo_size, logo_size))

            lmask = Image.new("L", (logo_size, logo_size), 0)

            ldraw = ImageDraw.Draw(lmask)

            ldraw.ellipse([0, 0, logo_size, logo_size], fill=255)

            logo.putalpha(lmask)

            canvas.paste(
                logo,
                (40, 610),
                logo,
            )

        # =========================
        # BOT NAME
        # =========================
        bot_font = ImageFont.truetype(FONT_BOLD_PATH, 42)

        draw.text(
            (160, 635),
            app.username,
            fill=(255, 255, 255),
            font=bot_font,
        )

        # =========================
        # PLAYING TEXT
        # =========================
        play_font = ImageFont.truetype(FONT_BOLD_PATH, 70)

        draw.text(
            (80, 120),
            "PLAYING",
            fill=accent,
            font=play_font,
        )

        # =========================
        # TITLE
        # =========================
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 48)

        title_lines = wrap_text(
            draw,
            title.upper(),
            title_font,
            520,
        )

        title_text = "\n".join(title_lines)

        draw.multiline_text(
            (80, 240),
            title_text,
            fill=(255, 255, 255),
            font=title_font,
            spacing=12,
        )

        # =========================
        # META
        # =========================
        meta_font = ImageFont.truetype(FONT_REGULAR_PATH, 32)

        draw.text(
            (80, 430),
            views,
            fill=(220, 220, 220),
            font=meta_font,
        )

        draw.text(
            (80, 485),
            duration,
            fill=(220, 220, 220),
            font=meta_font,
        )

        draw.text(
            (80, 540),
            channel,
            fill=(220, 220, 220),
            font=meta_font,
        )

        # =========================
        # MUSIC WAVE
        # =========================
        wave_y = 705

        for i in range(65):

            bar_x = 500 + i * 10

            bar_h = random.randint(10, 50)

            draw.rounded_rectangle(
                [
                    bar_x,
                    wave_y - bar_h,
                    bar_x + 5,
                    wave_y + bar_h,
                ],
                radius=3,
                fill=accent,
            )

        # =========================
        # EXPORT
        # =========================
        out = CACHE_DIR / f"{videoid}_ae.png"

        canvas.save(out, quality=95)

        if thumb_path and thumb_path.exists():
            os.remove(thumb_path)

        return str(out)

    except Exception as e:
        traceback.print_exc()
        print(e)
        return None