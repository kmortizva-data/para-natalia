"""Prepare photos for the website.

Reads every .jpg/.jpeg/.png in fotos_originales/ (never committed), resizes to
at most MAX_SIDE pixels on the long side, strips ALL metadata (EXIF, GPS,
camera, timestamps), fixes orientation first, and writes JPEG files plus
site/photos/manifest.json in filename order.

Usage:  python tools/prepare_photos.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "fotos_originales"
DST = ROOT / "site" / "photos"
MAX_SIDE = 1600
QUALITY = 84
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def main() -> int:
    DST.mkdir(parents=True, exist_ok=True)
    sources = sorted(p for p in SRC.iterdir() if p.suffix.lower() in EXTS)
    manifest: list[dict] = []
    for i, src in enumerate(sources, start=1):
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)  # apply rotation, then drop EXIF
            im = im.convert("RGB")
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            w, h = im.size
            name = f"{i:02d}.jpg"
            # No exif= argument -> nothing from the original is carried over.
            im.save(DST / name, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        manifest.append({"src": f"photos/{name}", "w": w, "h": h})
        print(f"  {src.name} -> {name} ({w}x{h})")
    (DST / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"{len(manifest)} photo(s) -> {DST / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
