"""Prepare photos and videos for the website.

Reads everything in fotos_originales/ (never committed), skips duplicates,
and writes:
  site/photos/NN.jpg      photos, orientation fixed, max MAX_SIDE px, no metadata
  site/videos/NN.mp4      videos re-encoded (H.264, <= 854 px wide, ~1 Mbps) + NN.jpg poster
  site/photos/manifest.json   one list, photos and videos mixed in WhatsApp order

Duplicate detection:
  * exact copies       -> same MD5 of the file bytes (photos and videos)
  * re-encoded copies  -> photos only: 16x16 average hash within NEAR_DISTANCE bits
Anything skipped is printed with the reason so nothing disappears silently.

Video encodes are slow, so they are cached in .cache/videos/<md5>.mp4 (ignored by git)
and only re-encoded when the source changes.

Usage:  python tools/prepare_photos.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "fotos_originales"
DST_PHOTOS = ROOT / "site" / "photos"
DST_VIDEOS = ROOT / "site" / "videos"
CACHE = ROOT / ".cache" / "videos"
FFMPEG = Path.home() / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
FFPROBE = Path.home() / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"

MAX_SIDE = 1600
QUALITY = 84
NEAR_DISTANCE = 4          # hamming distance on a 256-bit hash; <= 4 = same shot (bursts included)
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v"}

# WhatsApp names: "WhatsApp Image 2026-09-25 at 6.31.03 PMRT.jpeg"
WA_RE = re.compile(r"(\d{4}-\d{2}-\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2})\s*(AM|PM)", re.I)


def sort_key(p: Path):
    m = WA_RE.search(p.name)
    if not m:
        return (datetime.max, p.name)
    date, hh, mm, ss, ap = m.groups()
    h = int(hh) % 12 + (12 if ap.upper() == "PM" else 0)
    return (datetime.strptime(f"{date} {h:02d}:{mm}:{ss}", "%Y-%m-%d %H:%M:%S"), p.name)


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


def md5_of(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> dict:
    out = subprocess.run(
        [str(FFPROBE), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:stream_tags=rotate:stream_side_data=rotation:format=duration",
         "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    s = data["streams"][0]
    w, h = int(s["width"]), int(s["height"])
    rot = int((s.get("tags") or {}).get("rotate", 0) or 0)
    for sd in s.get("side_data_list") or []:
        rot = int(sd.get("rotation", rot) or rot)
    if rot % 180:
        w, h = h, w
    return {"w": w, "h": h, "dur": round(float(data["format"]["duration"]), 1)}


def encode_video(src: Path, md5: str) -> tuple[Path, Path]:
    """Return (mp4, poster) from the cache, encoding if needed."""
    CACHE.mkdir(parents=True, exist_ok=True)
    mp4, poster = CACHE / f"{md5}.mp4", CACHE / f"{md5}.jpg"
    if not mp4.exists():
        print(f"    encoding {src.name} ...")
        subprocess.run(
            [str(FFMPEG), "-y", "-v", "error", "-i", str(src),
             "-vf", "scale='min(854,iw)':-2",
             "-c:v", "libx264", "-preset", "medium", "-crf", "30", "-maxrate", "1000k", "-bufsize", "2000k",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-ac", "2",
             "-map_metadata", "-1", "-movflags", "+faststart", str(mp4)],
            check=True)
    if not poster.exists():
        subprocess.run(
            [str(FFMPEG), "-y", "-v", "error", "-ss", "1", "-i", str(mp4), "-frames:v", "1", str(poster)],
            check=True)
    return mp4, poster


def main() -> int:
    DST_PHOTOS.mkdir(parents=True, exist_ok=True)
    DST_VIDEOS.mkdir(parents=True, exist_ok=True)
    for old in list(DST_PHOTOS.glob("*.jpg")) + list(DST_VIDEOS.glob("*.mp4")) + list(DST_VIDEOS.glob("*.jpg")):
        old.unlink()                      # no orphans from a previous run

    # Manual exclusions (cropped re-sends the hashes cannot see): fotos_originales/EXCLUIR.txt
    exclude_file = SRC / "EXCLUIR.txt"
    excluded = set()
    if exclude_file.exists():
        excluded = {ln.strip() for ln in exclude_file.read_text(encoding="utf-8").splitlines()
                    if ln.strip() and not ln.startswith("#")}
    sources = sorted((p for p in SRC.iterdir() if p.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS), key=sort_key)
    for p in sources:
        if p.name in excluded:
            print(f"  (excluded by EXCLUIR.txt) {p.name}")
    sources = [p for p in sources if p.name not in excluded]
    seen_md5: dict[str, str] = {}
    accepted: list[tuple[int, str]] = []   # (perceptual hash, filename) for photos
    manifest: list[dict] = []
    skipped: list[str] = []
    n_photo = n_video = 0

    for src in sources:
        md5 = md5_of(src)
        if md5 in seen_md5:
            skipped.append(f"{src.name}: exact copy of {seen_md5[md5]}")
            continue
        seen_md5[md5] = src.name

        if src.suffix.lower() in VIDEO_EXTS:
            info = probe(src)
            mp4, poster_src = encode_video(src, md5)
            n_video += 1
            name = f"{n_video:02d}"
            shutil.copyfile(mp4, DST_VIDEOS / f"{name}.mp4")
            with Image.open(poster_src) as im:
                im = im.convert("RGB")
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
                im.save(DST_VIDEOS / f"{name}.jpg", "JPEG", quality=QUALITY, optimize=True, progressive=True)
                pw, ph = im.size
            manifest.append({"type": "video", "src": f"videos/{name}.mp4", "poster": f"videos/{name}.jpg",
                             "w": pw, "h": ph, "dur": info["dur"]})
            size_mb = (DST_VIDEOS / f"{name}.mp4").stat().st_size / 1e6
            print(f"  {src.name} -> videos/{name}.mp4 ({info['w']}x{info['h']}, {info['dur']}s, {size_mb:.1f} MB)")
            continue

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
            n_photo += 1
            name = f"{n_photo:02d}.jpg"
            # No exif= argument -> nothing from the original is carried over.
            im.save(DST_PHOTOS / name, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        manifest.append({"type": "image", "src": f"photos/{name}", "w": w, "h": hgt})
        print(f"  {src.name} -> {name} ({w}x{hgt})")

    (DST_PHOTOS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if skipped:
        print(f"\nskipped {len(skipped)} duplicate(s):")
        for s in skipped:
            print(f"  - {s}")
    photos_mb = sum(p.stat().st_size for p in DST_PHOTOS.glob("*.jpg")) / 1e6
    videos_mb = sum(p.stat().st_size for p in DST_VIDEOS.glob("*.mp4")) / 1e6
    print(f"\n{n_photo} photo(s) {photos_mb:.1f} MB, {n_video} video(s) {videos_mb:.1f} MB -> {DST_PHOTOS / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
