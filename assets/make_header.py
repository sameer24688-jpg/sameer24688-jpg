from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

assets = Path(__file__).resolve().parent
head = Image.open(assets / "headshot.jpg").convert("RGBA")

W, H = 1280, 360
img = Image.new("RGBA", (W, H), (8, 32, 29, 255))
draw = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    r = int(8 + (15 - 8) * t)
    g = int(32 + (92 - 32) * t * 0.35)
    b = int(29 + (84 - 29) * t * 0.3)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.ellipse([980, -80, 1380, 320], fill=(192, 106, 44, 40))
od.ellipse([-120, 180, 280, 520], fill=(22, 137, 124, 50))
img = Image.alpha_composite(img, overlay)
draw = ImageDraw.Draw(img)

size = 220
head = head.resize((size, size), Image.Resampling.LANCZOS)
mask = Image.new("L", (size, size), 0)
ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
ring = Image.new("RGBA", (size + 10, size + 10), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse([0, 0, size + 9, size + 9], fill=(217, 164, 65, 255))
hx, hy = 70, (H - size) // 2
img.paste(ring, (hx - 5, hy - 5), ring)
img.paste(head, (hx, hy), mask)

candidates = [
    r"C:\Windows\Fonts\georgia.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]
font_path = next((p for p in candidates if Path(p).exists()), None)
title = ImageFont.truetype(font_path, 46) if font_path else ImageFont.load_default()
sub = ImageFont.truetype(font_path, 22) if font_path else ImageFont.load_default()
small = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()

tx = hx + size + 48
ty = H // 2 - 70
draw.text((tx, ty), "Dr. Sameer Reddy Marri", fill=(246, 244, 238, 255), font=title)
draw.text(
    (tx, ty + 62),
    "Medicinal Chemist  ·  Synthetic Organic Chemist",
    fill=(224, 160, 96, 255),
    font=sub,
)
draw.text(
    (tx, ty + 110),
    "Ph.D., MRSC, CSci  ·  Boston University Center for Molecular Discovery",
    fill=(180, 200, 196, 255),
    font=small,
)

out = assets / "header.png"
img.convert("RGB").save(out, "PNG", optimize=True)
print("wrote", out, out.stat().st_size)
