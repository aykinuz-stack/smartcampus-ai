"""SmartCampus AI app icon generator — Pillow ile 1024x1024 PNG olusturur.

Kullanim:
  pip install Pillow
  python generate_icon.py

Cikarti:
  assets/icon/app_icon.png      (1024x1024, tam ikon)
  assets/icon/app_icon_fg.png   (1024x1024, adaptive foreground — seffaf arka plan)
"""
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow gerekli: pip install Pillow")
    sys.exit(1)

OUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "icon")
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 1024
PRIMARY = (79, 70, 229)      # #4F46E5 — Indigo
PRIMARY_DARK = (55, 48, 163)  # #3730A3
GOLD = (197, 150, 46)         # #C5962E
WHITE = (255, 255, 255)
NAVY = (15, 23, 42)           # #0F172A


def draw_rounded_rect(draw, xy, radius, fill):
    """Rounded rectangle ciz."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def generate_full_icon():
    """Tam ikon — gradient arka plan + school/AI sembol."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Arka plan (rounded rect gradient efekti)
    for y in range(SIZE):
        ratio = y / SIZE
        r = int(PRIMARY[0] * (1 - ratio) + PRIMARY_DARK[0] * ratio)
        g = int(PRIMARY[1] * (1 - ratio) + PRIMARY_DARK[1] * ratio)
        b = int(PRIMARY[2] * (1 - ratio) + PRIMARY_DARK[2] * ratio)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    # Rounded corners mask
    mask = Image.new("L", (SIZE, SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    draw_rounded_rect(mask_draw, (0, 0, SIZE, SIZE), SIZE // 5, fill=255)
    img.putalpha(mask)

    # Gold accent line (ust kisim)
    draw.rectangle([SIZE // 8, SIZE // 12, SIZE * 7 // 8, SIZE // 12 + 8], fill=GOLD)

    # Mezuniyet kepesi (graduation cap) — basit geometrik
    cx, cy = SIZE // 2, SIZE // 2 - 40
    cap_w, cap_h = 400, 80

    # Kepe gövde (diamond shape)
    draw.polygon([
        (cx, cy - cap_h),          # ust
        (cx + cap_w, cy),          # sag
        (cx, cy + cap_h // 2),     # alt
        (cx - cap_w, cy),          # sol
    ], fill=WHITE)

    # Kepe alt kutu
    draw.rectangle([cx - 140, cy + cap_h // 2, cx + 140, cy + cap_h + 60], fill=WHITE)

    # AI yazisi
    try:
        font = ImageFont.truetype("arial.ttf", 140)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140)
        except (IOError, OSError):
            font = ImageFont.load_default()

    text = "AI"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, SIZE - 300), text, fill=GOLD, font=font)

    # Gold accent line (alt)
    draw.rectangle([SIZE // 8, SIZE - SIZE // 12, SIZE * 7 // 8, SIZE - SIZE // 12 + 8], fill=GOLD)

    path = os.path.join(OUT_DIR, "app_icon.png")
    img.save(path, "PNG")
    print(f"[OK] {path}")
    return path


def generate_foreground():
    """Adaptive icon foreground — seffaf arka plan."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2 - 60
    cap_w, cap_h = 320, 65

    # Kepe
    draw.polygon([
        (cx, cy - cap_h),
        (cx + cap_w, cy),
        (cx, cy + cap_h // 2),
        (cx - cap_w, cy),
    ], fill=WHITE)
    draw.rectangle([cx - 110, cy + cap_h // 2, cx + 110, cy + cap_h + 50], fill=WHITE)

    # AI
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        except (IOError, OSError):
            font = ImageFont.load_default()

    text = "AI"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, SIZE - 320), text, fill=GOLD, font=font)

    path = os.path.join(OUT_DIR, "app_icon_fg.png")
    img.save(path, "PNG")
    print(f"[OK] {path}")
    return path


if __name__ == "__main__":
    print("SmartCampus AI — App Icon Generator")
    print("=" * 40)
    generate_full_icon()
    generate_foreground()
    print("\nTamam! CI'da flutter_launcher_icons calistirilinca Android/iOS ikonlari olusur.")
