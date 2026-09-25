"""Prepare photos for the website.

Reads every image in fotos_originales/ (never committed), skips duplicates,
fixes orientation, resizes to at most MAX_SIDE pixels on the long side,
strips ALL metadata (EXIF, GPS, camera, timestamps), and writes JPEG files
plus site/photos/manifest.json in filename order.

Duplicate detection:
  * exact copies       -> same MD5 of the file bytes
  * re-encoded copies  -> perceptual hash (16x16 average hash) within
                          NEAR_DISTANCE bits of an already accepted photo
Anything skipped is printed with the reason so nothing disappears silently.

Usage:  python tools/prepare_photos.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "fotos_originales"
DST = ROOT / "site" / "photos"
MAX_SIDE = 1600
QUALITY = 84
NEAR_DISTANCE = 2          # hamming distance on a 256-bit hash; 0-2 = same picture
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def average_hash(im: Image.Image) -> int:
    small = im.convert("L").resize((16, 16), Image.LANCZOS)
    px = list(small.get_flattened_data()) if hasattr(small, "get_flattened_data") else list(small.getdata())
    mean = sum(px) / len(px)
    bits = 0
    for v in px:
        bits = (bits << 1) | (1 if v > mean else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def main() -> int:
    DST.mkdir(parents=True, exist_ok=True)
    for old in DST.glob("*.jpg"):
        old.unlink()                      # no orphans from a previous run

    sources = sorted(p for p in SRC.iterdir() if p.suffix.lower() in EXTS)
    seen_md5: dict[str, str] = {}
    accepted: list[tuple[int, str]] = []   # (perceptual hash, filename)
    manifest: list[dict] = []
    skipped: list[str] = []
    n = 0

    for src in sources:
        md5 = hashlib.md5(src.read_bytes()).hexdigest()
        if md5 in seen_md5:
            skipped.append(f"{src.name}: exact copy of {seen_md5[md5]}")
            continue
        seen_md5[md5] = src.name

        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            h = average_hash(im)
            near = next(((d, name) for hh, name in accepted if (d := hamming(h, hh)) <= NEAR_DISTANCE), None)
            if near:
                skipped.append(f"{src.name}: same picture as {near[1]} (distance {near[0]})")
                continue
            accepted.append((h, src.name))

            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            w, hgt = im.size
            n += 1
            name = f"{n:02d}.jpg"
            # No exif= argument -> nothing from the original is carried over.
            im.save(DST / name, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        manifest.append({"src": f"photos/{name}", "w": w, "h": hgt})
        print(f"  {src.name} -> {name} ({w}x{hgt})")

    (DST / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if skipped:
        print(f"\nskipped {len(skipped)} duplicate(s):")
        for s in skipped:
            print(f"  - {s}")
    total_mb = sum(p.stat().st_size for p in DST.glob("*.jpg")) / 1e6
    print(f"\n{len(manifest)} photo(s), {total_mb:.1f} MB -> {DST / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
