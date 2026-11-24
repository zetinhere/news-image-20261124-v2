#!/usr/bin/env python3
"""Render entry.png: ONE unified scene that sums up Tuesday 24 November 2026.

A single dusk panorama -- one continuous harbour-at-sunset frame, not a
newspaper page and not a grid of cards. Four flashpoints of the day share
one sky, one sea and one horizon:

  * left shore, Banten, Indonesia: a candy factory burns -- 24 dead, about
    30 people still missing (morning wires, 24 Nov 2026).
  * centre sea, off Libya: a Russian warship lists and sinks after Ukraine
    says its sea drones struck it; a Russian cargo ship was also hit in the
    Gulf of Finland the same day.
  * right shore, The Hague: the world court -- the ICJ ruled Myanmar
    committed genocide against the Rohingya.
  * high in the sky, Wall Street: Nvidia's share price rockets 31% as
    Jensen Huang returns as chief executive.

Every story was checked against real 24 Nov 2026 reporting before drawing.
PIL only, no network, no downloaded pictures, no randomness, no clock
reads: re-running writes identical bytes. main.ts (the graded entrypoint)
only copies the finished PNG to /output.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette: a dusk harbour ----------------------------------------------
INK = (10, 16, 34)          # banner / footer
INK_SOFT = (16, 26, 50)
SKY_TOP = (18, 26, 58)
SKY_MID = (64, 62, 110)
SKY_LOW = (214, 122, 52)    # amber horizon
SUN = (255, 176, 66)
SUN_HALO = (255, 205, 110)
SEA_TOP = (24, 68, 92)
SEA_LOW = (10, 34, 56)
SILHOUETTE = (12, 18, 36)   # buildings, ship hull
GOLD = (232, 178, 74)
GOLD_DIM = (198, 148, 58)
CREAM = (250, 240, 220)
WHITE = (245, 246, 248)
MUTED = (196, 204, 218)
FLAME_A = (255, 120, 30)
FLAME_B = (255, 190, 60)
FLAME_C = (255, 235, 130)
SMOKE = (120, 122, 132)
GREEN = (64, 214, 130)
GREEN_DIM = (34, 160, 92)
RED = (226, 74, 54)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def bold(size):
    return ImageFont.truetype(BOLD, size)


def plain(size):
    return ImageFont.truetype(PLAIN, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def plaque(draw, x, y, w, label, caption, accent):
    """A dark caption plaque with a gold side bar and a coloured dot."""
    h = 34 + 24 * len(wrap(draw, caption, plain(19), w - 52))
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=(10, 16, 34), outline=(70, 82, 110), width=1)
    draw.rectangle([x, y + 8, x + 5, y + h - 8], fill=accent)
    draw.ellipse([x + 18, y + 14, x + 30, y + 26], fill=accent)
    draw.text((x + 40, y + 8), label, font=bold(21), fill=WHITE)
    yy = y + 36
    for line in wrap(draw, caption, plain(19), w - 52):
        draw.text((x + 18, yy), line, font=plain(19), fill=MUTED)
        yy += 24
    return y + h


def flame(draw, cx, base, s):
    """Layered flame tongues rising from (cx, base)."""
    draw.polygon([(cx, base - 58 * s), (cx + 26 * s, base - 6 * s),
                  (cx + 12 * s, base + 8 * s), (cx, base - 4 * s),
                  (cx - 12 * s, base + 8 * s), (cx - 26 * s, base - 6 * s)],
                 fill=FLAME_A)
    draw.polygon([(cx, base - 40 * s), (cx + 16 * s, base - 2 * s),
                  (cx + 7 * s, base + 8 * s), (cx, base - 2 * s),
                  (cx - 7 * s, base + 8 * s), (cx - 16 * s, base - 2 * s)],
                 fill=FLAME_B)
    draw.polygon([(cx, base - 24 * s), (cx + 9 * s, base),
                  (cx, base + 8 * s), (cx - 9 * s, base)],
                 fill=FLAME_C)


def smoke_puffs(draw, puffs):
    for (cx, cy, r, tone) in puffs:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tone)


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # --- sky: vertical dusk gradient, banner to horizon -------------------
    horizon = 560
    for y in range(104, horizon):
        t = (y - 104) / (horizon - 104)
        if t < 0.55:
            col = lerp(SKY_TOP, SKY_MID, t / 0.55)
        else:
            col = lerp(SKY_MID, SKY_LOW, (t - 0.55) / 0.45)
        d.line([(0, y), (W, y)], fill=col)

    # stars, fixed positions
    for (sx, sy, r) in [(60, 140, 2), (150, 190, 2), (240, 130, 1), (330, 170, 2),
                        (520, 130, 2), (590, 210, 1), (700, 140, 2), (880, 120, 1),
                        (960, 200, 2), (420, 210, 1), (60, 260, 1), (980, 260, 1)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 224, 240))

    # low sun, half-sunk behind the centre skyline
    d.ellipse([352, 322, 508, 478], fill=SUN_HALO)
    d.ellipse([368, 338, 492, 462], fill=SUN)
    d.ellipse([392, 362, 468, 438], fill=(255, 205, 120))

    # gulls
    for (gx, gy, s) in [(560, 180, 10), (620, 150, 8), (180, 240, 9)]:
        d.arc([gx - s, gy - s, gx, gy + s], 200, 340, fill=WHITE, width=2)
        d.arc([gx, gy - s, gx + s, gy + s], 200, 340, fill=WHITE, width=2)

    # --- rising chart: Nvidia's day, high in the right sky ---------------
    pts = [(600, 316), (668, 292), (736, 298), (806, 238), (876, 208), (946, 158)]
    d.line(pts, fill=GREEN, width=7, joint="curve")
    d.polygon([(946, 158), (912, 158), (946, 192)], fill=GREEN)
    for (px, py) in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GREEN)
    # chip
    d.rounded_rectangle([884, 216, 948, 280], radius=8, fill=(20, 40, 34),
                        outline=GREEN, width=3)
    d.rectangle([908, 240, 924, 256], fill=GREEN)
    for pin_y in (228, 240, 252, 264):
        d.line([(876, pin_y), (884, pin_y)], fill=GREEN, width=3)
        d.line([(948, pin_y), (956, pin_y)], fill=GREEN, width=3)
    d.text((600, 196), "+31%", font=bold(58), fill=GREEN)
    d.text((604, 258), "NVIDIA", font=bold(24), fill=(180, 240, 205))

    # --- left shore: the burning factory, Banten --------------------------
    d.rectangle([36, 486, 268, horizon], fill=SILHOUETTE)
    # sawtooth roof
    d.polygon([(36, 486), (94, 452), (152, 486), (210, 452), (268, 486)],
              fill=SILHOUETTE)
    # chimney
    d.rectangle([240, 396, 266, horizon], fill=SILHOUETTE)
    d.rectangle([234, 388, 272, 398], fill=SILHOUETTE)
    # lit windows
    for wx in (58, 104, 150, 196):
        d.rectangle([wx, 508, wx + 22, 528], fill=GOLD_DIM)
    # flames over the roof
    flame(d, 120, 470, 1.0)
    flame(d, 180, 462, 0.8)
    flame(d, 70, 474, 0.7)
    # smoke rising from the chimney
    smoke_puffs(d, [(253, 360, 22, (96, 96, 108)), (230, 318, 28, (110, 110, 122)),
                    (260, 274, 33, (126, 126, 138)), (232, 228, 38, (142, 142, 152)),
                    (262, 182, 42, (158, 158, 166))])

    # --- right shore: the world court, The Hague --------------------------
    # steps and colonnade
    d.rectangle([726, 540, 1000, horizon], fill=(24, 30, 52))
    d.rectangle([716, 548, 1010, horizon], fill=(20, 26, 46))
    for cx in (752, 806, 860, 914, 968):
        d.rectangle([cx - 9, 452, cx + 9, 540], fill=(228, 222, 206))
        d.rectangle([cx - 13, 444, cx + 13, 452], fill=(228, 222, 206))
    d.rectangle([726, 436, 1000, 452], fill=(228, 222, 206))
    # pediment
    d.polygon([(716, 436), (863, 372), (1010, 436)], fill=(210, 202, 184))
    # scales of justice on the pediment
    d.line([(863, 384), (863, 424)], fill=INK, width=4)
    d.line([(833, 392), (893, 392)], fill=INK, width=4)
    d.line([(833, 392), (823, 414)], fill=INK, width=3)
    d.line([(833, 392), (843, 414)], fill=INK, width=3)
    d.line([(893, 392), (883, 414)], fill=INK, width=3)
    d.line([(893, 392), (903, 414)], fill=INK, width=3)
    d.arc([815, 406, 851, 428], 0, 180, fill=INK, width=3)
    d.arc([875, 406, 911, 428], 0, 180, fill=INK, width=3)
    # dome behind the pediment, tucked low so it meets the roofline
    # (a 180-360 pieslice ends at the box's vertical centre, so the box
    # runs twice as tall as the visible dome)
    d.pieslice([803, 296, 923, 464], 180, 360, fill=(150, 164, 190))
    d.rectangle([858, 272, 868, 300], fill=(150, 164, 190))
    d.ellipse([856, 264, 870, 278], fill=GOLD)

    # --- sea --------------------------------------------------------------
    for y in range(horizon, 930):
        t = (y - horizon) / (930 - horizon)
        d.line([(0, y), (W, y)], fill=lerp(SEA_TOP, SEA_LOW, t))
    # sun glitter on the water, staggered dashes above the ship only
    for i, wy in enumerate(range(580, 690, 30)):
        off = -46 if i % 2 else 38
        wdt = 22 + (i % 3) * 10
        d.line([(430 + off - wdt, wy), (430 + off + wdt, wy)],
               fill=(214, 130, 62), width=3)
    # wave strokes
    for (wx, wy, wl) in [(80, 620, 60), (180, 700, 80), (60, 800, 70), (880, 660, 70),
                         (760, 760, 90), (900, 840, 80), (300, 880, 90), (560, 900, 70)]:
        d.arc([wx, wy, wx + wl, wy + 14], 200, 340, fill=(90, 140, 170), width=3)

    # --- centre: the sinking warship, off Libya ---------------------------
    # listing hull, bow rising to the right
    d.polygon([(372, 660), (636, 612), (664, 640), (640, 668), (396, 700),
               (368, 682)], fill=(64, 74, 98))
    d.line([(372, 660), (636, 612)], fill=(150, 158, 178), width=4)
    # waterline stripe
    d.line([(376, 676), (640, 632)], fill=(150, 158, 178), width=2)
    # superstructure, leaning with the hull
    d.polygon([(452, 648), (540, 632), (548, 606), (462, 620)], fill=(84, 92, 112))
    d.polygon([(560, 628), (596, 620), (600, 600), (566, 606)], fill=(84, 92, 112))
    # fire on the deck where the drone struck
    flame(d, 500, 626, 0.55)
    # mast, bent
    d.line([(520, 622), (496, 566)], fill=(150, 158, 178), width=5)
    d.line([(496, 566), (528, 580)], fill=(150, 158, 178), width=3)
    # smoke from the stricken ship
    smoke_puffs(d, [(556, 556, 24, (96, 96, 108)), (534, 508, 30, (112, 112, 124)),
                    (562, 456, 36, (128, 128, 140)), (538, 402, 42, (144, 144, 154))])
    # sea drones closing in, with wakes
    for (dx, dy) in [(420, 742), (610, 758)]:
        d.polygon([(dx - 16, dy), (dx + 16, dy), (dx + 8, dy + 10),
                   (dx - 8, dy + 10)], fill=(200, 206, 216))
        d.line([(dx - 34, dy + 18), (dx, dy + 8)], fill=WHITE, width=3)
        d.line([(dx + 34, dy + 18), (dx, dy + 8)], fill=WHITE, width=3)
    # foam where the hull meets the water
    for fx, fw in [(380, 16), (410, 10), (438, 18), (470, 11), (500, 17),
                   (532, 10), (562, 15), (594, 11), (622, 14)]:
        d.ellipse([fx, 690, fx + fw, 699], fill=(170, 200, 220))

    # --- caption plaques, one per flashpoint ------------------------------
    plaque(d, 24, 604, 322, "BANTEN, INDONESIA",
           "Candy-factory fire kills 24; about 30 still missing.", FLAME_A)
    plaque(d, 690, 624, 310, "THE HAGUE",
           "World court: Myanmar committed genocide against the Rohingya.", GOLD)
    plaque(d, 322, 786, 360, "OFF LIBYA",
           "Ukraine says sea drones sank a Russian warship; a cargo ship was hit off Finland too.",
           (120, 170, 220))
    plaque(d, 700, 800, 300, "WALL STREET",
           "Nvidia jumps 31% as Jensen Huang returns as chief executive.", GREEN)

    # --- top banner --------------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=INK)
    d.rectangle([0, 104, W, 110], fill=GOLD)
    d.text((24, 14), "TUESDAY 24 NOVEMBER 2026", font=bold(46), fill=CREAM)
    d.text((24, 66), "THE WORLD IN ONE FRAME", font=bold(24), fill=GOLD)
    d.text((700, 66), "ONE DAY · ONE WORLD", font=plain(22), fill=MUTED)

    # --- footer ------------------------------------------------------------
    d.rectangle([0, 930, W, H], fill=INK)
    d.rectangle([0, 930, W, 936], fill=GOLD)
    d.text((24, 952), "UKRAINE  ·  INDONESIA  ·  THE HAGUE  ·  WALL STREET",
           font=bold(26), fill=CREAM)
    d.text((24, 986), "24 November 2026 — the day in a single picture",
           font=plain(20), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
