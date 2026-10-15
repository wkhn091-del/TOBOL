from PIL import Image
import os

logo_path = r"C:\Users\user\_docs\assets\brand\yaelie-logo.jpg"
out_dir = r"C:\Users\user\_docs\assets\brand"
img = Image.open(logo_path).convert("RGBA")
w, h = img.size
pixels = img.load()


def is_bg(r, g, b):
    if r < 150 or g < 140 or b < 110:
        return False
    if abs(r - g) > 28 or abs(g - b) > 35 or abs(r - b) > 45:
        return False
    brightness = (r + g + b) / 3
    if brightness < 175:
        return False
    return True


out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
op = out.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if is_bg(r, g, b):
            op[x, y] = (0, 0, 0, 0)
        else:
            op[x, y] = (r, g, b, 255)

out_path = os.path.join(out_dir, "yaelie-logo-clear.png")
out.save(out_path, "PNG")
print("saved", out_path, out.size)

bbox = out.getbbox()
print("bbox", bbox)
if bbox:
    pad = 16
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(w, x1 + pad)
    y1 = min(h, y1 + pad)
    cropped = out.crop((x0, y0, x1, y1))
    cw, ch = cropped.size
    # Keep emblem + wordmark; drop nail tips on the far right
    if cw > ch * 1.55:
        cropped = cropped.crop((0, 0, int(cw * 0.76), ch))
    mark_path = os.path.join(out_dir, "yaelie-logo-mark.png")
    cropped.save(mark_path, "PNG")
    print("mark", mark_path, cropped.size)

# Build matching paper background color token sample
print("paper_hex #E1D8C7")
