"""Render a US-Letter sheet with one QR code per game (2 columns x 5 rows).

Reads ../site/games.json (single source of truth shared with the website),
draws the sheet with Pillow at 300 dpi, saves PNG + PDF, and then decodes
every QR back from the rendered image to prove each one points to the right URL.

Usage:  python qr/make_qr_sheet.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.constants import ERROR_CORRECT_M

ROOT = Path(__file__).resolve().parents[1]
GAMES_JSON = ROOT / "site" / "games.json"
OUT_DIR = ROOT / "qr" / "out"
SITE_URL = "https://kmortizva-data.github.io/para-natalia/"

# Letter at 300 dpi
DPI = 300
PAGE_W, PAGE_H = 2550, 3300
MARGIN = 150

# Palette shared with the website (warm, calm)
CREAM = (247, 241, 232)
INK = (43, 36, 31)
TERRACOTTA = (196, 87, 58)
SAGE = (94, 138, 106)
GOLD = (217, 164, 65)
MUTED = (138, 127, 116)
LINE = (222, 211, 197)
WHITE = (255, 255, 255)

FONTS = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


F_TITLE = font("georgiab.ttf", 96)
F_SUB = font("georgiai.ttf", 40)
F_NAME = font("georgiab.ttf", 50)
F_SITE = font("segoeui.ttf", 28)
F_CAT = font("segoeuib.ttf", 24)
F_BLURB = font("segoeui.ttf", 30)
F_URL = font("segoeui.ttf", 24)
F_NUM = font("georgiab.ttf", 34)
F_FOOT = font("segoeui.ttf", 28)
F_FOOT_B = font("segoeuib.ttf", 28)


def make_qr(data: str, size_px: int) -> Image.Image:
    """Return a QR image (with quiet zone) scaled to exactly size_px."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=INK, back_color=WHITE).convert("RGB")
    return img.resize((size_px, size_px), Image.NEAREST)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded(draw: ImageDraw.ImageDraw, box, radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def render(games: list[dict]) -> Image.Image:
    page = Image.new("RGB", (PAGE_W, PAGE_H), CREAM)
    d = ImageDraw.Draw(page)

    # Header
    y = MARGIN
    d.text((MARGIN, y), "Para Natalia", font=F_TITLE, fill=INK)
    y += 118
    d.text((MARGIN, y), "Diez planes para seguir jugando aunque estemos lejos.", font=F_SUB, fill=MUTED)
    y += 70
    d.text((MARGIN, y), "Escanea el código con el celular, crea la sala y mándame el link.", font=F_SITE, fill=MUTED)
    y += 60
    d.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=LINE, width=3)
    grid_top = y + 40

    # Footer geometry (reserve space)
    footer_h = 230
    grid_bottom = PAGE_H - MARGIN - footer_h
    cols, rows = 2, 5
    gutter = 60
    cell_w = (PAGE_W - 2 * MARGIN - gutter) // cols
    cell_h = (grid_bottom - grid_top - gutter * (rows - 1)) // rows
    qr_px = cell_h - 60
    pad = 30

    for i, g in enumerate(games):
        c, r = i % cols, i // cols
        x0 = MARGIN + c * (cell_w + gutter)
        y0 = grid_top + r * (cell_h + gutter)
        rounded(d, (x0, y0, x0 + cell_w, y0 + cell_h), 28, fill=WHITE, outline=LINE, width=3)

        # QR block
        qr_img = make_qr(g["url"], qr_px)
        page.paste(qr_img, (x0 + pad, y0 + (cell_h - qr_px) // 2))

        # Number badge on the QR corner
        bx, by = x0 + pad - 12, y0 + (cell_h - qr_px) // 2 - 12
        d.ellipse((bx, by, bx + 64, by + 64), fill=TERRACOTTA)
        num = str(g["n"])
        tw = d.textlength(num, font=F_NUM)
        d.text((bx + 32 - tw / 2, by + 10), num, font=F_NUM, fill=WHITE)

        # Text block
        tx = x0 + pad + qr_px + 34
        tw_max = x0 + cell_w - pad - tx
        ty = y0 + pad + 4
        cat = g["category"].upper()
        cw = d.textlength(cat, font=F_CAT)
        rounded(d, (tx, ty, tx + cw + 28, ty + 40), 20, fill=SAGE)
        d.text((tx + 14, ty + 5), cat, font=F_CAT, fill=WHITE)
        ty += 58
        d.text((tx, ty), g["name"], font=F_NAME, fill=INK)
        ty += 62
        if g["site"].lower() != g["name"].lower():
            d.text((tx, ty), g["site"], font=F_SITE, fill=MUTED)
            ty += 40
        ty += 6
        for line in wrap(d, g["blurb"], F_BLURB, tw_max)[:4]:
            d.text((tx, ty), line, font=F_BLURB, fill=INK)
            ty += 38
        url_txt = g["url"].replace("https://", "").rstrip("/")
        d.text((tx, y0 + cell_h - pad - 26), url_txt, font=F_URL, fill=TERRACOTTA)

    # Footer: site mini-QR + line
    fy = grid_bottom + 40
    d.line([(MARGIN, fy), (PAGE_W - MARGIN, fy)], fill=LINE, width=3)
    fy += 30
    mini = make_qr(SITE_URL, 160)
    page.paste(mini, (MARGIN, fy))
    d.text((MARGIN + 190, fy + 30), "La versión web, con fotos y todo:", font=F_FOOT_B, fill=INK)
    d.text((MARGIN + 190, fy + 72), SITE_URL.replace("https://", ""), font=F_FOOT, fill=TERRACOTTA)
    d.text((MARGIN + 190, fy + 114), "Hecho con cariño por Kevin.", font=F_FOOT, fill=MUTED)
    return page


def verify(png_path: Path, games: list[dict]) -> bool:
    """Decode every QR back from the rendered PNG and compare with games.json."""
    import zxingcpp

    img = Image.open(png_path)
    found = {r.text for r in zxingcpp.read_barcodes(img)}
    ok = True
    for g in games:
        hit = g["url"] in found
        ok &= hit
        print(f"  [{'OK' if hit else 'FAIL'}] {g['n']:>2}  {g['url']}")
    site_hit = SITE_URL in found
    ok &= site_hit
    print(f"  [{'OK' if site_hit else 'FAIL'}] web {SITE_URL}")
    return ok


def main() -> int:
    games = json.loads(GAMES_JSON.read_text(encoding="utf-8"))
    assert len(games) == 10, f"expected 10 games, got {len(games)}"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    page = render(games)
    png = OUT_DIR / "qr_natalia.png"
    pdf = OUT_DIR / "qr_natalia.pdf"
    page.save(png, dpi=(DPI, DPI))
    page.save(pdf, "PDF", resolution=DPI)
    print(f"wrote {png}\nwrote {pdf}")
    print("verifying QR codes from the rendered sheet:")
    return 0 if verify(png, games) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
