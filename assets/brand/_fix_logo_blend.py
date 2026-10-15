"""Force logo canvas to exact paper hex and export blend-ready assets."""
from PIL import Image
import os

BRAND = r"C:\Users\user\_docs\assets\brand"
PAPER = (225, 216, 199)  # #E1D8C7
src = Image.open(os.path.join(BRAND, "yaelie-logo.jpg")).convert("RGB")
w, h = src.size

# Replace near-paper pixels with exact PAPER so it vanishes on matching CSS bg
pixels = src.load()
out = Image.new("RGB", (w, h), PAPER)
op = out.load()
for y in range(h):
    for x in range(w):
        r, g, b = pixels[x, y]
        brightness = (r + g + b) / 3
        # speckled paper / cream
        if brightness > 178 and abs(r - g) < 30 and abs(g - b) < 40 and abs(r - b) < 50:
            op[x, y] = PAPER
        else:
            op[x, y] = (r, g, b)

# Header: crop left 70% (drop nail tips), pad with PAPER
crop_w = int(w * 0.70)
header = out.crop((0, 0, crop_w, h))
# Trim empty-ish top/bottom by scanning non-paper rows
def content_bbox(im, paper=PAPER, tol=8):
    px = im.load()
    iw, ih = im.size
    minx, miny, maxx, maxy = iw, ih, 0, 0
    found = False
    for yy in range(ih):
        for xx in range(iw):
            r, g, b = px[xx, yy]
            if abs(r - paper[0]) > tol or abs(g - paper[1]) > tol or abs(b - paper[2]) > tol:
                found = True
                minx = min(minx, xx)
                miny = min(miny, yy)
                maxx = max(maxx, xx)
                maxy = max(maxy, yy)
    if not found:
        return (0, 0, iw, ih)
    return (minx, miny, maxx + 1, maxy + 1)

bb = content_bbox(header)
header = header.crop(bb)
pad = 18
canvas = Image.new("RGB", (header.size[0] + pad * 2, header.size[1] + pad * 2), PAPER)
canvas.paste(header, (pad, pad))
canvas.save(os.path.join(BRAND, "yaelie-logo-header.jpg"), "JPEG", quality=96)

# Hero version: slightly wider crop still without tips
hero = out.crop((0, 0, int(w * 0.74), h))
bb2 = content_bbox(hero)
hero = hero.crop(bb2)
canvas2 = Image.new("RGB", (hero.size[0] + pad * 2, hero.size[1] + pad * 2), PAPER)
canvas2.paste(hero, (pad, pad))
canvas2.save(os.path.join(BRAND, "yaelie-logo-hero.jpg"), "JPEG", quality=96)
print("header", canvas.size, "hero", canvas2.size)
print("paper #E1D8C7")
