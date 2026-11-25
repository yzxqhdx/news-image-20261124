#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261124.

One day, seven stories: a dark-navy vertical timeline for
Tuesday, 24 November 2026. Headline feature on top (Nvidia / Huang
returns to HQ - a drawn scene, never a portrait), six illustrated
stories below, each with its own flat scene panel.

Every pixel is drawn here from scratch with Pillow primitives -
no photos, no downloaded images, no AI art. A reference photo, if
one arrives, is reference only: it is never pasted into the image.

Run: python3 draw.py  ->  writes entry.png (1024x1024) next to it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---
BG = (11, 21, 38)          # deep navy
BG_TOP = (16, 32, 54)      # slightly lighter navy at the top
PANEL = (19, 37, 63)       # illustration panel
GOLD = (242, 169, 0)       # spine / accents
GREEN = (118, 185, 0)      # Nvidia green
WHITE = (255, 255, 255)
SUB = (169, 184, 204)      # sub-label grey-blue
FAINT = (126, 143, 168)    # footer grey
SEPARATOR = (255, 255, 255, 26)
DARK = (5, 8, 15)          # silhouette black
GLASS_LIT = (118, 185, 0)
GLASS_DIM = (38, 78, 58)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, max_w, start_size, min_size=22):
    """Largest bold size at which the headline fits on one line."""
    size = start_size
    while size > min_size:
        fnt = font(FONT_BOLD, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(FONT_BOLD, min_size)


def fit_sub(draw, text, max_w, max_lines, start_size, min_size=16):
    """Largest regular size at which the sub fits in max_lines lines."""
    size = start_size
    while size > min_size:
        fnt = font(FONT_REG, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt
        size -= 1
    return font(FONT_REG, min_size)


# --- flat scenes, each drawn inside its panel (px, py, pw, ph) ---
def scene_building(d, px, py, pw, ph, accent):
    """Damaged apartment block, broken roofline, smoke rising."""
    cx = px + pw // 2
    base = py + ph - 8
    x0, x1 = px + 42, px + 108
    top = py + 20
    # body with a jagged broken top
    d.polygon([(x0, base), (x0, top + 16), (x0 + 16, top + 6),
               (x0 + 30, top + 14), (x0 + 46, top + 2), (x0 + 66, top + 10),
               (x1, top + 6), (x1, base)], fill=(215, 222, 232))
    # broken edge highlighted in the story colour
    d.line([(x0, top + 16), (x0 + 16, top + 6), (x0 + 30, top + 14),
            (x0 + 46, top + 2), (x0 + 66, top + 10), (x1, top + 6)],
           fill=accent, width=3, joint="curve")
    # dark windows, one row missing where the wall broke
    for col in (x0 + 10, x0 + 38):
        for row in (top + 22, top + 36, top + 50):
            if col == x0 + 38 and row == top + 22:
                continue
            d.rectangle([col, row, col + 12, row + 9], fill=BG)
    # crack down the facade
    d.line([(x0 + 52, top + 30), (x0 + 46, top + 42), (x0 + 54, top + 54)],
           fill=BG, width=2, joint="curve")
    # smoke puffs drifting up-right (kept low so they clear the
    # feature sub-line above the first row)
    for (sx, sy, r) in ((cx - 14, top - 4, 9), (cx + 2, top - 14, 12),
                        (cx + 20, top - 24, 8)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(185, 196, 212))


def scene_ship(d, px, py, pw, ph, accent):
    """Warship at sea: hull, superstructure, mast and flag, waves."""
    cy = py + ph // 2
    base = py + ph - 10
    # waves
    d.arc([px + 12, base - 8, px + 68, base + 8], 180, 360, fill=WHITE, width=3)
    d.arc([px + 88, base - 8, px + 156, base + 8], 180, 360, fill=WHITE, width=3)
    d.arc([px + 48, base + 2, px + 104, base + 16], 180, 360, fill=accent, width=3)
    # hull
    d.polygon([(px + 34, cy + 2), (px + 136, cy + 2), (px + 124, cy + 24),
               (px + 46, cy + 24)], fill=WHITE)
    # superstructure + funnel
    d.rectangle([px + 76, cy - 16, px + 108, cy + 2], fill=WHITE)
    d.rectangle([px + 80, cy - 26, px + 90, cy - 16], fill=accent)
    # mast + flag
    d.line([px + 98, cy - 16, px + 98, cy - 36], fill=WHITE, width=3)
    d.polygon([(px + 98, cy - 36), (px + 118, cy - 31), (px + 98, cy - 26)],
              fill=accent)


def scene_shield_globe(d, px, py, pw, ph, accent):
    """Globe with a shield over it: NATO defending its territory."""
    cy = py + ph // 2
    gx, gy, r = px + 52, cy, 30
    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(22, 50, 79),
              outline=WHITE, width=3)
    d.ellipse([gx - 13, gy - r, gx + 13, gy + r], outline=WHITE, width=2)
    d.line([gx - r, gy, gx + r, gy], fill=WHITE, width=2)
    # shield overlapping the globe, lower right
    sx, sy = px + 112, cy + 4
    d.polygon([(sx - 24, sy - 22), (sx + 24, sy - 22), (sx + 24, sy + 2),
               (sx, sy + 26), (sx - 24, sy + 2)], fill=accent,
              outline=WHITE, width=2)
    d.line([sx - 12, sy + 2, sx - 3, sy + 11, sx + 13, sy - 8],
           fill=WHITE, width=4, joint="curve")


def scene_skyline(d, px, py, pw, ph, accent):
    """Night city skyline under a moon, one roofline broken."""
    base = py + ph - 8
    # moon + stars
    d.ellipse([px + 22, py + 10, px + 36, py + 24], fill=WHITE)
    d.ellipse([px + 128, py + 14, px + 132, py + 18], fill=WHITE)
    d.ellipse([px + 140, py + 26, px + 143, py + 29], fill=WHITE)
    # blocks, alternating light tones, third one broken
    blocks = [(px + 14, 30, (232, 238, 245)), (px + 40, 48, (185, 196, 212)),
              (px + 66, 38, (232, 238, 245)), (px + 92, 56, (185, 196, 212)),
              (px + 120, 34, (232, 238, 245))]
    for (bx, bh, col) in blocks:
        if bx == px + 66:
            d.polygon([(bx, base), (bx, base - bh + 12), (bx + 8, base - bh + 4),
                       (bx + 16, base - bh + 12), (bx + 24, base - bh + 6),
                       (bx + 24, base)], fill=col)
        else:
            d.rectangle([bx, base - bh, bx + 24, base], fill=col)
    # lit windows on the two tallest blocks
    for (wx, wy) in ((px + 46, base - 40), (px + 58, base - 28),
                     (px + 98, base - 48), (px + 110, base - 34)):
        d.rectangle([wx, wy, wx + 5, wy + 5], fill=accent)


def scene_globe_thermo(d, px, py, pw, ph, accent):
    """Globe beside a thermometer with the mercury running high."""
    cy = py + ph // 2
    gx, gy, r = px + 48, cy, 29
    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(22, 50, 79),
              outline=accent, width=3)
    d.ellipse([gx - 12, gy - r, gx + 12, gy + r], outline=WHITE, width=2)
    d.line([gx - r, gy, gx + r, gy], fill=WHITE, width=2)
    # thermometer: white tube, red mercury, bulb at the bottom
    tx = px + 108
    d.rounded_rectangle([tx, py + 10, tx + 16, py + ph - 22], radius=8,
                        fill=WHITE)
    d.ellipse([tx - 6, py + ph - 30, tx + 22, py + ph - 14], fill=WHITE)
    d.rectangle([tx + 5, py + ph - 52, tx + 11, py + ph - 22],
                fill=(229, 72, 77))
    d.ellipse([tx + 1, py + ph - 25, tx + 15, py + ph - 11],
              fill=(229, 72, 77))
    # tick marks
    for ty in (py + 18, py + 30, py + 42):
        d.line([tx + 16, ty, tx + 22, ty], fill=BG, width=2)


def scene_chart(d, px, py, pw, ph, accent):
    """Rising bars and an arrow: Asian chip stocks surging."""
    base = py + ph - 12
    d.line([px + 24, py + 10, px + 24, base], fill=WHITE, width=3)
    d.line([px + 24, base, px + 148, base], fill=WHITE, width=3)
    heights = [16, 28, 42, 56]
    for k, bh in enumerate(heights):
        bx = px + 36 + k * 26
        d.rectangle([bx, base - bh, bx + 16, base], fill=accent)
    d.line([(px + 32, base - 26), (px + 62, base - 40),
            (px + 92, base - 50), (px + 136, base - 64)],
           fill=WHITE, width=4, joint="curve")
    d.polygon([(px + 136, base - 64), (px + 138, base - 48),
               (px + 122, base - 62)], fill=WHITE)


def scene_hq(d, fx0, fy0, fw, fh, accent):
    """Headline scene, composed after the reference photo (composition
    only - the photo itself is never used, and its invented caption
    text is not copied): a leather-jacket silhouette holding a
    cardboard box in front of Nvidia's glass HQ, green wordmark on
    the glass. A scene, never a portrait: the figure is a plain black
    silhouette, no face, no likeness, no features."""
    ground = fy0 + fh - 14
    # glass tower, left
    tx0, tx1, ttop = fx0 + 58, fx0 + 398, fy0 + 14
    d.rectangle([tx0, ttop, tx1, ground], fill=(18, 48, 36))
    # wordmark band at the top of the tower
    d.rectangle([tx0, ttop, tx1, ttop + 30], fill=(10, 26, 20))
    d.text(((tx0 + tx1) // 2, ttop + 15), "NVIDIA",
           font=font(FONT_BOLD, 22), fill=accent, anchor="mm")
    # window grid: mostly dim, some lit
    lit = {(1, 2), (3, 1), (4, 4), (0, 5), (2, 6), (5, 3), (6, 0), (2, 3)}
    for col in range(8):
        for row in range(7):
            wx = tx0 + 14 + col * 40
            wy = ttop + 40 + row * 14
            colr = GLASS_LIT if (col, row) in lit else GLASS_DIM
            d.rectangle([wx, wy, wx + 26, wy + 8], fill=colr)
    # lower glass block, right
    bx0, bx1, btop = fx0 + 668, fx0 + 828, fy0 + 62
    d.rectangle([bx0, btop, bx1, ground], fill=(24, 44, 66))
    for col in range(5):
        for row in range(3):
            wx = bx0 + 10 + col * 30
            wy = btop + 12 + row * 18
            d.rectangle([wx, wy, wx + 18, wy + 9],
                        fill=(120, 140, 165) if (col + row) % 3 else WHITE)
    # soft green glow behind the figure, so the black silhouette reads
    sx = fx0 + 548
    d.ellipse([sx - 90, ground - 150, sx + 90, ground + 4],
              fill=(118, 185, 0, 36))
    # leather-jacket silhouette with a cardboard box, centre-right
    # legs
    d.line([sx - 14, ground - 30, sx - 22, ground], fill=DARK, width=9)
    d.line([sx + 14, ground - 30, sx + 22, ground], fill=DARK, width=9)
    # torso: broad-shouldered jacket
    d.polygon([(sx - 38, ground - 110), (sx + 38, ground - 110),
               (sx + 30, ground - 30), (sx - 30, ground - 30)], fill=DARK)
    # collar + zipper, in dark grey so the jacket reads (still a silhouette)
    d.polygon([(sx - 12, ground - 110), (sx, ground - 96),
               (sx + 12, ground - 110)], fill=(40, 48, 60))
    d.line([sx, ground - 98, sx, ground - 74], fill=(40, 48, 60), width=2)
    # head: plain circle, no face
    d.ellipse([sx - 13, ground - 138, sx + 13, ground - 112], fill=DARK)
    # arms reaching to the box
    d.line([sx - 34, ground - 102, sx - 46, ground - 72], fill=DARK, width=8)
    d.line([sx + 34, ground - 102, sx + 46, ground - 72], fill=DARK, width=8)
    # cardboard box held at waist height
    bx0, by0, bx1, by1 = sx - 44, ground - 76, sx + 44, ground - 26
    d.rectangle([bx0, by0, bx1, by1], fill=(201, 164, 110),
                outline=(150, 116, 72), width=2)
    d.rectangle([sx - 4, by0, sx + 4, by1], fill=(170, 134, 84))
    d.line([bx0, by0 + 6, bx1, by0 + 6], fill=(150, 116, 72), width=2)
    # ground line + circuit dots along the bottom edge
    d.line([fx0 + 16, ground, fx0 + fw - 16, ground], fill=(60, 80, 105), width=2)
    for dx in (fx0 + 40, fx0 + 850):
        d.ellipse([dx - 3, ground + 6, dx + 3, ground + 12], outline=accent, width=2)


SCENES = {"building": scene_building, "ship": scene_ship,
          "shield_globe": scene_shield_globe, "skyline": scene_skyline,
          "globe_thermo": scene_globe_thermo, "chart": scene_chart}

# --- the six stories below the feature: (tag, headline, sub, accent, scene) ---
STORIES = [
    ("UKRAINE",
     "2 KILLED, 40 WOUNDED IN ZAPORIZHZHIA",
     "Overnight Russian strike hits homes; four children hurt",
     (229, 72, 77), "building"),
    ("LIBYA",
     "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Seven sea drones sink the corvette Merkury; Kyiv: self-defence",
     (42, 165, 255), "ship"),
    ("NATO  ·  ESTONIA",
     "RUSSIA WARNS ESTONIA OF 'OPEN WAR'",
     "NATO vows to defend 'every inch' — space included",
     (139, 124, 255), "shield_globe"),
    ("GAZA",
     "ISRAELI STRIKE KILLS 3 IN GAZA",
     "Airstrike near Khan Younis; the October 2025 ceasefire frays",
     (249, 115, 22), "skyline"),
    ("CLIMATE  ·  ANTALYA",
     "CLIMATE TALKS COLLAPSE WITH NO DEAL",
     "COP31 deadlocked over fossil fuels — first failure since 2009",
     (52, 211, 153), "globe_thermo"),
    ("ASIA  ·  MARKETS",
     "ASIAN CHIP STOCKS SURGE",
     "Taiwan +9%, Korea's Kospi +7% as the AI trade rebounds",
     (250, 204, 21), "chart"),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")

    # top glow band
    for y in range(0, 150):
        blend = 1.0 - y / 150.0
        r = int(BG[0] + (BG_TOP[0] - BG[0]) * blend)
        g = int(BG[1] + (BG_TOP[1] - BG[1]) * blend)
        b = int(BG[2] + (BG_TOP[2] - BG[2]) * blend)
        d.line([0, y, W, y], fill=(r, g, b))

    # --- header ---
    d.text((W / 2, 22), "THE WORLD IN ONE DAY", font=font(FONT_BOLD, 24),
           fill=GOLD, anchor="ma")
    d.text((W / 2, 50), "TUESDAY, 24 NOVEMBER 2026", font=font(FONT_BOLD, 48),
           fill=WHITE, anchor="ma")
    d.text((W / 2, 110), "ONE DAY  ·  SEVEN STORIES THAT DEFINED IT",
           font=font(FONT_REG, 20), fill=SUB, anchor="ma")
    d.line([72, 138, W - 72, 138], fill=GOLD, width=3)

    # --- headline feature: biggest illustration on top ---
    fx0, fy0, fw, fh = 72, 154, 880, 162
    d.rounded_rectangle([fx0, fy0, fx0 + fw, fy0 + fh], radius=12,
                        fill=PANEL, outline=GREEN, width=2)
    scene_hq(d, fx0, fy0, fw, fh, GREEN)
    # feature text under the panel
    d.text((72, 326), "NEW YORK  ·  MARKETS", font=font(FONT_BOLD, 18),
           fill=GOLD)
    d.text((72, 348), "OUT 11 DAYS. BACK AS CEO.",
           font=font(FONT_BOLD, 36), fill=WHITE)
    d.text((72, 390),
           "Trump pressed the board to rehire him — then spoke to the directors himself.",
           font=font(FONT_REG, 20), fill=SUB)
    d.text((72, 414),
           "Shares fell a third in two weeks, then soared 31% Monday — a record $952bn gain",
           font=font(FONT_REG, 20), fill=SUB)

    # --- timeline spine, from the feature down through the six rows ---
    spine_x = 54
    d.line([spine_x, 235, spine_x, 970], fill=GOLD, width=4)
    d.ellipse([spine_x - 17, 235 - 17, spine_x + 17, 235 + 17], fill=GREEN)
    d.ellipse([spine_x - 17, 235 - 17, spine_x + 17, 235 + 17],
              outline=WHITE, width=2)

    # --- six illustrated rows ---
    row_top, row_h = 446, 88
    text_x, text_w = 254, 984 - 254
    for i, (tag, head, sub, accent, scene) in enumerate(STORIES):
        top = row_top + i * row_h
        cy = top + row_h // 2

        if i > 0:
            d.line([text_x, top, 984, top], fill=SEPARATOR, width=1)

        # node disc on the spine
        d.ellipse([spine_x - 15, cy - 15, spine_x + 15, cy + 15], fill=accent)
        d.ellipse([spine_x - 15, cy - 15, spine_x + 15, cy + 15],
                  outline=WHITE, width=2)

        # illustration panel
        px, py, pw, ph = 84, cy - 40, 150, 80
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=8,
                            fill=PANEL, outline=accent, width=2)
        SCENES[scene](d, px, py, pw, ph, accent)

        # text: tag, headline, one-line sub
        d.text((text_x, top + 4), tag, font=font(FONT_BOLD, 16), fill=GOLD)
        head_fnt = fit_headline(d, head, text_w, 26)
        d.text((text_x, top + 23), head, font=head_fnt, fill=WHITE)
        sub_fnt = fit_sub(d, sub, text_w, 1, 19)
        d.text((text_x, top + 53), sub, font=sub_fnt, fill=SUB)

    # --- footer ---
    d.text((W / 2, 996),
           "All stories reported on 24 November 2026  ·  Sources: Reuters, AP, CNN, WSJ",
           font=font(FONT_REG, 14), fill=FAINT, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
