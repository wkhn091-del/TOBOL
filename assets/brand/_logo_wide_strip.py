"""Create wide logo strip for header — no postage-stamp square."""
from PIL import Image, ImageDraw
import os

BRAND = r"C:\Users\user\_docs\assets\brand"
PAPER = (225, 216, 199)
src = Image.open(os.path.join(BRAND, "yaelie-logo.jpg")).convert("RGB")
w, h = src.size
px = src.load()

# Normalize paper
norm = Image.new("RGB", (w, h), PAPER)
np = norm.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        brightness = (r + g + b) / 3
        if brightness > 178 and abs(r - g) < 30 and abs(g - b) < 40 and abs(r - b) < 50:
            np[x, y] = PAPER
        else:
            np[x, y] = (r, g, b)

# Find content bbox ignoring paper
tol = 10
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(h):
    for x in range(int(w * 0.72)):  # ignore nail tips zone
        r, g, b = np[x, y]
        if abs(r - PAPER[0]) > tol or abs(g - PAPER[1]) > tol or abs(b - PAPER[2]) > tol:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)

# Expand a bit
pad = 8
minx = max(0, minx - pad)
miny = max(0, miny - pad)
maxx = min(int(w * 0.72), maxx + pad)
maxy = min(h, maxy + pad)
content = norm.crop((minx, miny, maxx, maxy))
cw, ch = content.size

# Build wide canvas (aspect ~ 3.2:1) with content centered
out_h = 180
out_w = int(out_h * 3.4)
canvas = Image.new("RGB", (out_w, out_h), PAPER)
# scale content to fit height with margins
margin_y = 16
target_h = out_h - margin_y * 2
scale = target_h / ch
nw, nh = int(cw * scale), int(ch * scale)
if nw > out_w - 24:
    scale = (out_w - 24) / cw
    nw, nh = int(cw * scale), int(ch * scale)
resized = content.resize((nw, nh), Image.Resampling.LANCZOS)
ox = (out_w - nw) // 2
oy = (out_h - nh) // 2
canvas.paste(resized, (ox, oy))
path = os.path.join(BRAND, "yaelie-logo-wide.jpg")
canvas.save(path, "JPEG", quality=96)
print("wide", canvas.size, path)

# Hero: taller card banner, still paper, content top-centered
hero_h = 220
hero_w = 720
hero = Image.new("RGB", (hero_w, hero_h), PAPER)
scale2 = min((hero_w - 40) / cw, (hero_h - 30) / ch)
nw2, nh2 = int(cw * scale2), int(ch * scale2)
resized2 = content.resize((nw2, nh2), Image.Resampling.LANCZOS)
hero.paste(resized2, ((hero_w - nw2) // 2, 18))
hero_path = os.path.join(BRAND, "yaelie-logo-hero.jpg")
hero.save(hero_path, "JPEG", quality=96)
print("hero", hero.size)
