#!/usr/bin/env python3
"""Generate a 1200x630 OG image for haoel.github.io (科学上网 / 左耳朵).

Pillow-only, byte-reproducible. Clean card matching the Cayman theme:
light ground, #157878 teal accent (theme-color), CJK title + subtitle,
section pills + domain chip. Uses WenQuanYi Zen Hei for CJK glyphs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (246, 248, 250)          # near-white ground
TEAL = (21, 120, 120)         # #157878 Cayman theme-color
DARK = (43, 43, 43)           # #2b2b2b
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_TEAL = (224, 240, 240)

FONT_DIR = os.environ.get("FONT_DIR", "/usr/share/fonts/truetype/dejavu")
CJK_FONT = os.environ.get("CJK_FONT", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    p = os.path.join(FONT_DIR, name)
    if not os.path.exists(p):
        p = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf")
    return ImageFont.truetype(p, size)


def cjk(size):
    return ImageFont.truetype(CJK_FONT, size)


def rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # top accent bar (Cayman teal)
    d.rectangle([0, 0, W, 10], fill=TEAL)

    f_title = cjk(72)
    f_sub = cjk(36)
    f_pill = cjk(30)
    f_domain = font(30, bold=True)
    f_foot = font(24)

    # title + subtitle (CJK)
    d.text((70, 70), "科学上网", font=f_title, fill=DARK)
    d.text((70, 175), "左耳朵 · coolshell.cn", font=f_sub, fill=GREY)

    # separator
    d.line([70, 260, W - 70, 260], fill=(210, 218, 222), width=2)

    # section pills (CJK)
    pills = ["机场 vs 自建", "购买 VPS", "搭建代理服务", "客户端设置", "流量伪装", "家用网关"]
    x = 70
    y = 300
    for p_ in pills:
        w = d.textlength(p_, font=f_pill) + 44
        if x + w > 1130:  # wrap to next row before overflow
            x = 70
            y += 82
        rounded(d, [x, y, x + w, y + 62], 31, TEAL)
        d.text((x + 22, y + 13), p_, font=f_pill, fill=WHITE)
        x += w + 18

    # footer domain chip
    d.rounded_rectangle([70, H - 92, 470, H - 44], 24, fill=DARK)
    d.text((108, H - 84), "haoel.github.io", font=f_domain, fill=WHITE)

    # subtle motif: a network/globe line-art in the top-right (circumvention guide)
    cx, cy = W - 190, 150
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=TEAL, width=4)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=LIGHT_TEAL, width=4)
    d.line([cx - 70, cy, cx + 70, cy], fill=TEAL, width=3)
    d.line([cx, cy - 70, cx, cy + 70], fill=TEAL, width=3)

    out = "og-image.png"
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
