"""Zrzut ekranu -> grafika do sklepu (1080x1920): tlo, naglowek, podpis, telefon ze zrzutem.
Uzycie: python promo.py <zrzut> <wyjscie.jpg> "<NAGLOWEK>" "<podpis>" <kolor_tla> <kolor_akcentu>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT = "/system/fonts/Roboto-Regular.ttf"  # zmienna czcionka (os wght)


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight] + [a["default"] for a in f.get_variation_axes()[1:]])
    return f


def hexc(s):
    return tuple(int(s.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    # jednoliterowe slowa (w, z, i, a) nie zostaja na koncu wiersza
    words = []
    for w in text.split():
        if words and len(words[-1]) == 1:
            words[-1] += "\u00a0" + w
        else:
            words.append(w)
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def main(src, out, title, sub, bg, accent):
    bg, accent = hexc(bg), hexc(accent)
    img = Image.new("RGB", (W, H), bg)
    # delikatny gradient: jasniej u gory
    top = tuple(min(255, int(c * 1.35 + 12)) for c in bg)
    grad = Image.linear_gradient("L").resize((W, H))
    img = Image.composite(Image.new("RGB", (W, H), bg), Image.new("RGB", (W, H), top), grad)
    d = ImageDraw.Draw(img)

    y = 110
    tf = font(92, 900)
    for line in wrap(d, title.upper(), tf, W - 140):
        d.text((W / 2, y), line, font=tf, fill=accent, anchor="ma")
        y += 104
    y += 24
    sf = font(42, 400)
    for line in wrap(d, sub, sf, W - 200):
        d.text((W / 2, y), line, font=sf, fill=(235, 240, 245), anchor="ma")
        y += 56

    # telefon: ekran 740 px szerokosci, ramka 22 px, dol uciety jak w Play
    shot = Image.open(src).convert("RGB")
    sw = 740
    sh = round(shot.height * sw / shot.width)
    shot = shot.resize((sw, sh), Image.LANCZOS)
    b = 22
    pw, ph = sw + 2 * b, sh + 2 * b
    px, py = (W - pw) // 2, max(y + 60, 600)

    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((px, py + 20, px + pw, py + ph + 20), 90, fill=150)
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shadow)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((px - 4, py - 4, px + pw + 4, py + ph + 4), 94, fill=(70, 72, 78))
    d.rounded_rectangle((px, py, px + pw, py + ph), 90, fill=(12, 12, 14))
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), 68, fill=255)
    img.paste(shot, (px + b, py + b), mask)
    img.save(out, quality=88, optimize=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
