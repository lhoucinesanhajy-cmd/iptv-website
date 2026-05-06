"""
Generates favicon.png for OttOcean IPTV.
Design: circular icon — orange/green/red swirl + black play button.
Uses only Python built-ins (struct, zlib, math). No Pillow needed.
"""
import struct, zlib, math

SIZE = 512

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def make_png(pixels, width, height):
    """Encode raw RGBA pixels into a PNG bytestream."""
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))  # RGB

    # Build raw image rows (filter byte 0 + RGB data)
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type None
        for x in range(width):
            r, g, b, a = pixels[y][x]
            # blend over white background
            r2 = clamp(r * a / 255 + 255 * (255 - a) / 255)
            g2 = clamp(g * a / 255 + 255 * (255 - a) / 255)
            b2 = clamp(b * a / 255 + 255 * (255 - a) / 255)
            raw += bytes([r2, g2, b2])

    idat = chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend

def lerp_color(c1, c2, t):
    return tuple(clamp(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))

# ── Colour palette ──────────────────────────────────────────────────────────
ORANGE1 = (255, 149,  0, 255)
ORANGE2 = (255, 107,  0, 255)
GREEN1  = ( 52, 199,  89, 255)
GREEN2  = ( 39, 160,  69, 255)
RED1    = (255,  59,  48, 255)
RED2    = (214,  32,  32, 255)
WHITE   = (255, 255, 255, 255)
BLACK   = ( 26,  26,  26, 255)
TRANSP  = (  0,   0,   0,   0)

cx = cy = SIZE // 2
R_OUTER = SIZE // 2 - 4   # outer radius of the swirl ring
R_INNER = SIZE // 2 - 4   # circle bounding radius (same → full disk)
R_WHITE = int(SIZE * 0.28) # inner white circle radius
R_BORDER= SIZE // 2 - 3   # soft border

print("Rendering pixels…")
pixels = []
for y in range(SIZE):
    row = []
    for x in range(SIZE):
        dx, dy = x - cx, y - cy
        dist = math.hypot(dx, dy)

        if dist > R_OUTER:
            row.append(TRANSP)
            continue

        # Angle in [0, 2π)
        angle = math.atan2(dy, dx) % (2 * math.pi)
        # Normalise to [0,1)
        t = angle / (2 * math.pi)

        # ── Inner white circle ───────────────────────────────────────────
        if dist < R_WHITE:
            row.append(WHITE)
            continue

        # ── Swirl colouring ─────────────────────────────────────────────
        # Divide the circle into 3 sectors with smooth feathering
        # Sector boundaries (in fractions of full rotation):
        # Orange : 0.00 – 0.33
        # Green  : 0.33 – 0.67
        # Red    : 0.67 – 1.00

        blend_width = 0.06   # fraction of circle used for cross-fade

        def sector_blend(lo, hi):
            """Return blend factor [0..1] for how much we're inside [lo,hi]."""
            mid_lo = lo + blend_width
            mid_hi = hi - blend_width
            if lo <= t < mid_lo:
                return (t - lo) / blend_width
            elif mid_lo <= t <= mid_hi:
                return 1.0
            elif mid_hi < t <= hi:
                return (hi - t) / blend_width
            return 0.0

        # Also compute distance fade for radial gradient inside ring
        radial_t = (dist - R_WHITE) / (R_OUTER - R_WHITE)  # 0=inner edge, 1=outer

        w_orange = sector_blend(0.00, 0.33) + sector_blend(0.88, 1.0)
        w_green  = sector_blend(0.30, 0.63)
        w_red    = sector_blend(0.60, 0.93)

        total = w_orange + w_green + w_red
        if total == 0:
            # fallback
            col = lerp_color(ORANGE1, ORANGE2, radial_t)
        else:
            w_orange /= total
            w_green  /= total
            w_red    /= total

            c_orange = lerp_color(ORANGE1, ORANGE2, radial_t)
            c_green  = lerp_color(GREEN1,  GREEN2,  radial_t)
            c_red    = lerp_color(RED1,    RED2,    radial_t)

            col = tuple(clamp(
                c_orange[i]*w_orange + c_green[i]*w_green + c_red[i]*w_red
            ) for i in range(4))

        # Soft outer anti-alias fade
        if dist > R_OUTER - 2:
            fade = (R_OUTER - dist) / 2
            col = tuple(list(col[:3]) + [clamp(col[3] * fade)])

        row.append(tuple(col))
    pixels.append(row)

# ── Draw play button triangle ────────────────────────────────────────────────
print("Drawing play button…")
# Triangle vertices (pointing right)
margin = int(SIZE * 0.07)
tx1, ty1 = cx - int(SIZE*0.09), cy - int(SIZE*0.115)   # top-left
tx2, ty2 = cx - int(SIZE*0.09), cy + int(SIZE*0.115)   # bottom-left
tx3, ty3 = cx + int(SIZE*0.14), cy                      # right tip

for y in range(SIZE):
    for x in range(SIZE):
        if pixels[y][x] == TRANSP:
            continue
        # Point-in-triangle test (barycentric)
        def sign(p1x,p1y, p2x,p2y, p3x,p3y):
            return (p1x-p3x)*(p2y-p3y)-(p2x-p3x)*(p1y-p3y)
        d1 = sign(x,y, tx1,ty1, tx2,ty2)
        d2 = sign(x,y, tx2,ty2, tx3,ty3)
        d3 = sign(x,y, tx3,ty3, tx1,ty1)
        has_neg = (d1<0) or (d2<0) or (d3<0)
        has_pos = (d1>0) or (d2>0) or (d3>0)
        if not (has_neg and has_pos):
            # Soft shadow: darken nearby pixels slightly
            pixels[y][x] = BLACK

# ── Encode & save ────────────────────────────────────────────────────────────
print("Encoding PNG…")
png_data = make_png(pixels, SIZE, SIZE)
out_path = 'favicon.png'
with open(out_path, 'wb') as f:
    f.write(png_data)
print(f"Done! favicon.png written ({len(png_data)//1024} KB)")
