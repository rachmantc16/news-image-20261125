#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page for Tuesday 25 November 2026.

Build-time only. Renders a 1024x1024 PNG with Pillow using bold shapes
and short, carefully spelled capital-letter labels. Stories are the top
world news found in news search results for 25 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (24, 62, 140)
TEAL = (10, 110, 105)
ORANGE = (214, 116, 18)
GREEN = (28, 120, 52)
PURPLE = (92, 44, 140)


def f(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_REG, size)


def centered(d, cx, y, text, font, fill=INK):
    box = d.textbbox((0, 0), text, font=font)
    w = box[2] - box[0]
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + (box[3] - box[1])


def panel(img, d, x, y, w, h, color, lines, icon):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(255, 255, 255),
                        outline=color, width=5)
    d.rectangle([x, y, x + w, y + 46], fill=color)
    centered(d, x + w / 2, y + 8, lines[0], f(26), fill=(255, 255, 255))
    # Draw the icon on its own canvas, then scale it into the compact panel.
    icon_img = Image.new("RGB", (360, 220), (255, 255, 255))
    icon_draw = ImageDraw.Draw(icon_img)
    icon(icon_draw, 180, 110)
    icon_small = icon_img.resize((216, 132))
    img.paste(icon_small, (x + w // 2 - 108, y + 50))
    ty = y + 190
    for line in lines[1:]:
        ty = centered(d, x + w / 2, ty, line, f(25)) + 6


def icon_ship(d, cx, cy):
    d.polygon([(cx - 90, cy + 20), (cx + 90, cy + 20), (cx + 60, cy + 55),
               (cx - 60, cy + 55)], fill=INK)
    d.rectangle([cx - 40, cy - 25, cx + 30, cy + 20], fill=BLUE)
    d.rectangle([cx + 38, cy - 45, cx + 58, cy + 20], fill=RED)
    for i in range(3):
        d.ellipse([cx - 110 + i * 80, cy + 66, cx - 70 + i * 80, cy + 86],
                  outline=TEAL, width=5)


def icon_chart(d, cx, cy):
    d.line([(cx - 95, cy - 50), (cx - 95, cy + 60)], fill=INK, width=6)
    d.line([(cx - 95, cy + 60), (cx + 95, cy + 60)], fill=INK, width=6)
    pts = [(cx - 80, cy - 30), (cx - 35, cy + 5), (cx + 5, cy - 5),
           (cx + 45, cy + 35), (cx + 85, cy + 50)]
    d.line(pts, fill=RED, width=8)
    d.polygon([(cx + 85, cy + 50), (cx + 62, cy + 48), (cx + 80, cy + 28)],
              fill=RED)


def icon_anchor(d, cx, cy):
    d.ellipse([cx - 16, cy - 62, cx + 16, cy - 30], outline=INK, width=7)
    d.line([(cx, cy - 30), (cx, cy + 55)], fill=INK, width=7)
    d.line([(cx - 55, cy - 5), (cx + 55, cy - 5)], fill=INK, width=7)
    d.arc([cx - 62, cy - 10, cx + 62, cy + 90], start=20, end=160, fill=INK,
          width=7)
    d.polygon([(cx - 62, cy + 38), (cx - 38, cy + 42), (cx - 58, cy + 62)],
              fill=INK)
    d.polygon([(cx + 62, cy + 38), (cx + 38, cy + 42), (cx + 58, cy + 62)],
              fill=INK)


def icon_store(d, cx, cy):
    d.rectangle([cx - 85, cy - 10, cx + 85, cy + 60], outline=INK, width=6)
    d.polygon([(cx - 100, cy - 10), (cx - 78, cy - 55), (cx + 78, cy - 55),
               (cx + 100, cy - 10)], fill=ORANGE)
    d.rectangle([cx - 22, cy + 12, cx + 22, cy + 60], fill=BLUE)
    d.rectangle([cx - 68, cy + 8, cx - 38, cy + 34], fill=TEAL)
    d.rectangle([cx + 38, cy + 8, cx + 68, cy + 34], fill=TEAL)


def icon_rocket(d, cx, cy):
    d.ellipse([cx - 28, cy - 70, cx + 28, cy + 30], fill=PURPLE)
    d.ellipse([cx - 11, cy - 42, cx + 11, cy - 20], fill=(255, 255, 255))
    d.polygon([(cx - 28, cy + 5), (cx - 58, cy + 48), (cx - 24, cy + 34)],
              fill=RED)
    d.polygon([(cx + 28, cy + 5), (cx + 58, cy + 48), (cx + 24, cy + 34)],
              fill=RED)
    d.polygon([(cx - 14, cy + 32), (cx + 14, cy + 32), (cx, cy + 78)],
              fill=ORANGE)


def icon_trophy(d, cx, cy):
    d.rectangle([cx - 42, cy - 60, cx + 42, cy + 5], fill=(232, 176, 20))
    d.arc([cx - 85, cy - 58, cx - 38, cy + 2], start=90, end=270,
          fill=(232, 176, 20), width=9)
    d.arc([cx + 38, cy - 58, cx + 85, cy + 2], start=270, end=90,
          fill=(232, 176, 20), width=9)
    d.rectangle([cx - 9, cy + 5, cx + 9, cy + 34], fill=(232, 176, 20))
    d.rectangle([cx - 34, cy + 34, cx + 34, cy + 52], fill=INK)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 196], fill=INK)
    centered(d, W / 2, 18, "THE WORLD TODAY", f(44), fill=(232, 176, 20))
    centered(d, W / 2, 74, "TUESDAY 25 NOVEMBER 2026", f(56),
             fill=(255, 255, 255))
    centered(d, W / 2, 148, "ONE PAGE - THE DAY IN SIX STORIES", f(26),
             fill=(200, 200, 200))

    stories = [
        (RED, ["HORMUZ", "TWO TANKERS HIT", "MINES IN STRAIT"], icon_ship),
        (BLUE, ["UKRAINE", "RUSSIAN CORVETTE", "SUNK OFF LIBYA"], icon_anchor),
        (PURPLE, ["MARKETS", "NVIDIA DOWN 7 PCT", "NIKKEI FALLS 2.76"], icon_chart),
        (ORANGE, ["COLOMBIA", "HOSTAGES HELD IN", "CARTAGENA STORE"], icon_store),
        (TEAL, ["PAKISTAN", "FIRST ASTRONAUT AT", "CHINA STATION"], icon_rocket),
        (GREEN, ["SENEGAL", "AFCON TITLE BACK", "AFTER CAS RULING"], icon_trophy),
    ]
    pw, ph, gap, x0, y0 = 488, 262, 10, 16, 210
    for i, (color, lines, icon) in enumerate(stories):
        x = x0 + (i % 2) * (pw + gap)
        y = y0 + (i // 2) * (ph + gap)
        panel(img, d, x, y, pw, ph, color, lines, icon)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
