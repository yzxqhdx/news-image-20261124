#!/usr/bin/env python3
"""Rebuild the entry image for make.fun news-image-20261124.

A dark-navy vertical timeline for Tuesday, 24 November 2026: one
day, seven stories. The headline feature sits on top (Nvidia / Huang
back at HQ, drawn as a scene, never a portrait); six illustrated
stories follow, each with its own flat panel picture.

Everything here is drawn from scratch with Pillow primitives. No
photos, no downloaded pictures, no AI art. A reference photo, if one
is supplied, is composition reference only and is never pasted in.

Run: python3 draw.py  ->  writes entry.png (1024x1024) beside it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = CANVAS_H = 1024
OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---
NAVY = (11, 21, 38)          # deep navy
NAVY_HI = (16, 32, 54)       # slightly lighter navy at the top
CARD = (19, 37, 63)          # illustration panel
AMBER = (242, 169, 0)        # spine / accents
LEAF = (118, 185, 0)         # Nvidia green
SNOW = (255, 255, 255)
MIST = (169, 184, 204)       # sub-label grey-blue
FOG = (126, 143, 168)        # footer grey
HAIRLINE = (255, 255, 255, 26)
SOOT = (5, 8, 15)            # silhouette black
LIT = (118, 185, 0)
DIM = (38, 78, 58)

BOLD_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(pen, text, face, max_w):
    """Greedy word wrap, returns the lines that fit inside max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if pen.textlength(trial, font=face) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def headline_font(pen, text, max_w, start_size, min_size=22):
    """Largest bold size at which the headline still fits on one line."""
    size = start_size
    while size > min_size:
        face = load_font(BOLD_FONT, size)
        if pen.textlength(text, font=face) <= max_w:
            return face
        size -= 1
    return load_font(BOLD_FONT, min_size)


def sub_font(pen, text, max_w, max_lines, start_size, min_size=16):
    """Largest regular size at which the sub still fits in max_lines lines."""
    size = start_size
    while size > min_size:
        face = load_font(REG_FONT, size)
        if len(wrap_text(pen, text, face, max_w)) <= max_lines:
            return face
        size -= 1
    return load_font(REG_FONT, min_size)


# --- flat pictures, each painted inside its panel (x, y, w, h) ---
def paint_ruin(pen, x, y, w, h, tint):
    """Damaged apartment block with a broken roofline, smoke rising."""
    mx = x + w // 2
    floor = y + h - 8
    left, right = x + 42, x + 108
    roof = y + 20
    # body with a jagged broken top
    pen.polygon([(left, floor), (left, roof + 16), (left + 16, roof + 6),
                 (left + 30, roof + 14), (left + 46, roof + 2),
                 (left + 66, roof + 10), (right, roof + 6), (right, floor)],
                fill=(215, 222, 232))
    # broken edge picked out in the story colour
    pen.line([(left, roof + 16), (left + 16, roof + 6), (left + 30, roof + 14),
              (left + 46, roof + 2), (left + 66, roof + 10), (right, roof + 6)],
             fill=tint, width=3, joint="curve")
    # dark windows, one row missing where the wall broke
    for col in (left + 10, left + 38):
        for row in (roof + 22, roof + 36, roof + 50):
            if col == left + 38 and row == roof + 22:
                continue
            pen.rectangle([col, row, col + 12, row + 9], fill=NAVY)
    # crack down the facade
    pen.line([(left + 52, roof + 30), (left + 46, roof + 42),
              (left + 54, roof + 54)], fill=NAVY, width=2, joint="curve")
    # smoke puffs drifting up-right (kept low so they clear the
    # feature sub-line above the first row)
    for (sx, sy, r) in ((mx - 14, roof - 4, 9), (mx + 2, roof - 14, 12),
                        (mx + 20, roof - 24, 8)):
        pen.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(185, 196, 212))


def paint_ship(pen, x, y, w, h, tint):
    """Warship at sea: hull, superstructure, mast and flag, waves."""
    mid = y + h // 2
    floor = y + h - 10
    # waves
    pen.arc([x + 12, floor - 8, x + 68, floor + 8], 180, 360, fill=SNOW, width=3)
    pen.arc([x + 88, floor - 8, x + 156, floor + 8], 180, 360, fill=SNOW, width=3)
    pen.arc([x + 48, floor + 2, x + 104, floor + 16], 180, 360, fill=tint, width=3)
    # hull
    pen.polygon([(x + 34, mid + 2), (x + 136, mid + 2), (x + 124, mid + 24),
                 (x + 46, mid + 24)], fill=SNOW)
    # superstructure + funnel
    pen.rectangle([x + 76, mid - 16, x + 108, mid + 2], fill=SNOW)
    pen.rectangle([x + 80, mid - 26, x + 90, mid - 16], fill=tint)
    # mast + flag
    pen.line([x + 98, mid - 16, x + 98, mid - 36], fill=SNOW, width=3)
    pen.polygon([(x + 98, mid - 36), (x + 118, mid - 31), (x + 98, mid - 26)],
                fill=tint)


def paint_shield(pen, x, y, w, h, tint):
    """Globe with a shield over it: NATO defending its territory."""
    mid = y + h // 2
    gx, gy, r = x + 52, mid, 30
    pen.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(22, 50, 79),
                outline=SNOW, width=3)
    pen.ellipse([gx - 13, gy - r, gx + 13, gy + r], outline=SNOW, width=2)
    pen.line([gx - r, gy, gx + r, gy], fill=SNOW, width=2)
    # shield overlapping the globe, lower right
    sx, sy = x + 112, mid + 4
    pen.polygon([(sx - 24, sy - 22), (sx + 24, sy - 22), (sx + 24, sy + 2),
                 (sx, sy + 26), (sx - 24, sy + 2)], fill=tint,
                outline=SNOW, width=2)
    pen.line([sx - 12, sy + 2, sx - 3, sy + 11, sx + 13, sy - 8],
             fill=SNOW, width=4, joint="curve")


def paint_city(pen, x, y, w, h, tint):
    """Night city skyline under a moon, one roofline broken."""
    floor = y + h - 8
    # moon + stars
    pen.ellipse([x + 22, y + 10, x + 36, y + 24], fill=SNOW)
    pen.ellipse([x + 128, y + 14, x + 132, y + 18], fill=SNOW)
    pen.ellipse([x + 140, y + 26, x + 143, y + 29], fill=SNOW)
    # blocks, alternating light tones, third one broken
    blocks = [(x + 14, 30, (232, 238, 245)), (x + 40, 48, (185, 196, 212)),
              (x + 66, 38, (232, 238, 245)), (x + 92, 56, (185, 196, 212)),
              (x + 120, 34, (232, 238, 245))]
    for (bx, bh, col) in blocks:
        if bx == x + 66:
            pen.polygon([(bx, floor), (bx, floor - bh + 12),
                         (bx + 8, floor - bh + 4), (bx + 16, floor - bh + 12),
                         (bx + 24, floor - bh + 6), (bx + 24, floor)], fill=col)
        else:
            pen.rectangle([bx, floor - bh, bx + 24, floor], fill=col)
    # lit windows on the two tallest blocks
    for (wx, wy) in ((x + 46, floor - 40), (x + 58, floor - 28),
                     (x + 98, floor - 48), (x + 110, floor - 34)):
        pen.rectangle([wx, wy, wx + 5, wy + 5], fill=tint)


def paint_heat(pen, x, y, w, h, tint):
    """Globe beside a thermometer with the mercury running high."""
    mid = y + h // 2
    gx, gy, r = x + 48, mid, 29
    pen.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(22, 50, 79),
                outline=tint, width=3)
    pen.ellipse([gx - 12, gy - r, gx + 12, gy + r], outline=SNOW, width=2)
    pen.line([gx - r, gy, gx + r, gy], fill=SNOW, width=2)
    # thermometer: white tube, red mercury, bulb at the bottom
    tx = x + 108
    pen.rounded_rectangle([tx, y + 10, tx + 16, y + h - 22], radius=8,
                          fill=SNOW)
    pen.ellipse([tx - 6, y + h - 30, tx + 22, y + h - 14], fill=SNOW)
    pen.rectangle([tx + 5, y + h - 52, tx + 11, y + h - 22],
                  fill=(229, 72, 77))
    pen.ellipse([tx + 1, y + h - 25, tx + 15, y + h - 11],
                fill=(229, 72, 77))
    # tick marks
    for ty in (y + 18, y + 30, y + 42):
        pen.line([tx + 16, ty, tx + 22, ty], fill=NAVY, width=2)


def paint_bars(pen, x, y, w, h, tint):
    """Rising bars and an arrow: Asian chip stocks surging."""
    floor = y + h - 12
    pen.line([x + 24, y + 10, x + 24, floor], fill=SNOW, width=3)
    pen.line([x + 24, floor, x + 148, floor], fill=SNOW, width=3)
    heights = [16, 28, 42, 56]
    for k, bh in enumerate(heights):
        bx = x + 36 + k * 26
        pen.rectangle([bx, floor - bh, bx + 16, floor], fill=tint)
    pen.line([(x + 32, floor - 26), (x + 62, floor - 40),
              (x + 92, floor - 50), (x + 136, floor - 64)],
             fill=SNOW, width=4, joint="curve")
    pen.polygon([(x + 136, floor - 64), (x + 138, floor - 48),
                 (x + 122, floor - 62)], fill=SNOW)


def paint_feature(pen, ox, oy, ow, oh, tint):
    """Headline scene, composed from the reference photo's layout only:
    the photo itself is never used, and its invented caption text is
    not copied. A leather-jacket silhouette holding a cardboard box in
    front of Nvidia's glass HQ, green wordmark on the glass. A scene,
    never a portrait: the figure is a plain black silhouette, no face,
    no likeness, no features."""
    floor = oy + oh - 14
    # glass tower, left
    tower_l, tower_r, tower_top = ox + 58, ox + 398, oy + 14
    pen.rectangle([tower_l, tower_top, tower_r, floor], fill=(18, 48, 36))
    # wordmark band at the top of the tower
    pen.rectangle([tower_l, tower_top, tower_r, tower_top + 30], fill=(10, 26, 20))
    pen.text(((tower_l + tower_r) // 2, tower_top + 15), "NVIDIA",
             font=load_font(BOLD_FONT, 22), fill=tint, anchor="mm")
    # window grid: mostly dim, some lit
    lit_cells = {(1, 2), (3, 1), (4, 4), (0, 5), (2, 6), (5, 3), (6, 0), (2, 3)}
    for col in range(8):
        for row in range(7):
            wx = tower_l + 14 + col * 40
            wy = tower_top + 40 + row * 14
            shade = LIT if (col, row) in lit_cells else DIM
            pen.rectangle([wx, wy, wx + 26, wy + 8], fill=shade)
    # lower glass block, right
    block_l, block_r, block_top = ox + 668, ox + 828, oy + 62
    pen.rectangle([block_l, block_top, block_r, floor], fill=(24, 44, 66))
    for col in range(5):
        for row in range(3):
            wx = block_l + 10 + col * 30
            wy = block_top + 12 + row * 18
            pen.rectangle([wx, wy, wx + 18, wy + 9],
                          fill=(120, 140, 165) if (col + row) % 3 else SNOW)
    # soft green glow behind the figure, so the black silhouette reads
    fig_x = ox + 548
    pen.ellipse([fig_x - 90, floor - 150, fig_x + 90, floor + 4],
                fill=(118, 185, 0, 36))
    # leather-jacket silhouette with a cardboard box, centre-right
    # legs
    pen.line([fig_x - 14, floor - 30, fig_x - 22, floor], fill=SOOT, width=9)
    pen.line([fig_x + 14, floor - 30, fig_x + 22, floor], fill=SOOT, width=9)
    # torso: broad-shouldered jacket
    pen.polygon([(fig_x - 38, floor - 110), (fig_x + 38, floor - 110),
                 (fig_x + 30, floor - 30), (fig_x - 30, floor - 30)], fill=SOOT)
    # collar + zipper, in dark grey so the jacket reads (still a silhouette)
    pen.polygon([(fig_x - 12, floor - 110), (fig_x, floor - 96),
                 (fig_x + 12, floor - 110)], fill=(40, 48, 60))
    pen.line([fig_x, floor - 98, fig_x, floor - 74], fill=(40, 48, 60), width=2)
    # head: plain circle, no face
    pen.ellipse([fig_x - 13, floor - 138, fig_x + 13, floor - 112], fill=SOOT)
    # arms reaching to the box
    pen.line([fig_x - 34, floor - 102, fig_x - 46, floor - 72], fill=SOOT, width=8)
    pen.line([fig_x + 34, floor - 102, fig_x + 46, floor - 72], fill=SOOT, width=8)
    # cardboard box held at waist height
    box_l, box_t, box_r, box_b = fig_x - 44, floor - 76, fig_x + 44, floor - 26
    pen.rectangle([box_l, box_t, box_r, box_b], fill=(201, 164, 110),
                  outline=(150, 116, 72), width=2)
    pen.rectangle([fig_x - 4, box_t, fig_x + 4, box_b], fill=(170, 134, 84))
    pen.line([box_l, box_t + 6, box_r, box_t + 6], fill=(150, 116, 72), width=2)
    # ground line + circuit dots along the bottom edge
    pen.line([ox + 16, floor, ox + ow - 16, floor], fill=(60, 80, 105), width=2)
    for dot_x in (ox + 40, ox + 850):
        pen.ellipse([dot_x - 3, floor + 6, dot_x + 3, floor + 12], outline=tint, width=2)


PAINTERS = {"ruin": paint_ruin, "ship": paint_ship,
            "shield": paint_shield, "city": paint_city,
            "heat": paint_heat, "bars": paint_bars}

# --- the six stories below the feature: (tag, headline, sub, tint, painter) ---
ITEMS = [
    ("UKRAINE", "2 KILLED, 40 WOUNDED IN ZAPORIZHZHIA",
     "Overnight Russian strike hits homes; four children hurt",
     (229, 72, 77), "ruin"),
    ("LIBYA", "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Seven sea drones sink the corvette Merkury; Kyiv: self-defence",
     (42, 165, 255), "ship"),
    ("NATO  ·  ESTONIA", "RUSSIA WARNS ESTONIA OF 'OPEN WAR'",
     "NATO vows to defend 'every inch' — space included",
     (139, 124, 255), "shield"),
    ("GAZA", "ISRAELI STRIKE KILLS 3 IN GAZA",
     "Airstrike near Khan Younis; the October 2025 ceasefire frays",
     (249, 115, 22), "city"),
    ("CLIMATE  ·  ANTALYA", "CLIMATE TALKS COLLAPSE WITH NO DEAL",
     "COP31 deadlocked over fossil fuels — first failure since 2009",
     (52, 211, 153), "heat"),
    ("ASIA  ·  MARKETS", "ASIAN CHIP STOCKS SURGE",
     "Taiwan +9%, Korea's Kospi +7% as the AI trade rebounds",
     (250, 204, 21), "bars"),
]


def build():
    sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), NAVY)
    pen = ImageDraw.Draw(sheet, "RGBA")

    # top glow band
    for y in range(0, 150):
        blend = 1.0 - y / 150.0
        r = int(NAVY[0] + (NAVY_HI[0] - NAVY[0]) * blend)
        g = int(NAVY[1] + (NAVY_HI[1] - NAVY[1]) * blend)
        b = int(NAVY[2] + (NAVY_HI[2] - NAVY[2]) * blend)
        pen.line([0, y, CANVAS_W, y], fill=(r, g, b))

    # --- header ---
    pen.text((CANVAS_W / 2, 22), "THE WORLD IN ONE DAY", font=load_font(BOLD_FONT, 24),
             fill=AMBER, anchor="ma")
    pen.text((CANVAS_W / 2, 50), "TUESDAY, 24 NOVEMBER 2026", font=load_font(BOLD_FONT, 48),
             fill=SNOW, anchor="ma")
    pen.text((CANVAS_W / 2, 110), "ONE DAY  ·  SEVEN STORIES THAT DEFINED IT",
             font=load_font(REG_FONT, 20), fill=MIST, anchor="ma")
    pen.line([72, 138, CANVAS_W - 72, 138], fill=AMBER, width=3)

    # --- headline feature: biggest illustration on top ---
    feat_x, feat_y, feat_w, feat_h = 72, 154, 880, 162
    pen.rounded_rectangle([feat_x, feat_y, feat_x + feat_w, feat_y + feat_h],
                          radius=12, fill=CARD, outline=LEAF, width=2)
    paint_feature(pen, feat_x, feat_y, feat_w, feat_h, LEAF)
    # feature text under the panel, aligned to the panel's left edge
    fx = feat_x
    pen.text((fx, 326), "NEW YORK  ·  MARKETS", font=load_font(BOLD_FONT, 18),
             fill=AMBER)
    pen.text((fx, 348), "OUT 11 DAYS. BACK AS CEO.",
             font=load_font(BOLD_FONT, 36), fill=SNOW)
    pen.text((fx, 390),
             "Trump pressed the board to rehire him — then spoke to the directors himself.",
             font=load_font(REG_FONT, 20), fill=MIST)
    pen.text((fx, 414),
             "Shares fell a third in two weeks, then soared 31% Monday — a record $952bn gain",
             font=load_font(REG_FONT, 20), fill=MIST)

    # --- timeline spine, from the feature down through the six rows ---
    axis_x = 54
    pen.line([axis_x, 235, axis_x, 970], fill=AMBER, width=4)
    pen.ellipse([axis_x - 17, 235 - 17, axis_x + 17, 235 + 17], fill=LEAF)
    pen.ellipse([axis_x - 17, 235 - 17, axis_x + 17, 235 + 17],
                outline=SNOW, width=2)

    # --- six illustrated rows ---
    rows_top, row_height = 446, 88
    txt_x, txt_w = 254, 984 - 254
    for i, (tag, head, sub, tint, painter) in enumerate(ITEMS):
        row_y = rows_top + i * row_height
        mid_y = row_y + row_height // 2

        if i > 0:
            pen.line([txt_x, row_y, 984, row_y], fill=HAIRLINE, width=1)

        # node disc on the spine
        pen.ellipse([axis_x - 15, mid_y - 15, axis_x + 15, mid_y + 15], fill=tint)
        pen.ellipse([axis_x - 15, mid_y - 15, axis_x + 15, mid_y + 15],
                    outline=SNOW, width=2)

        # illustration panel
        ix, iy, iw, ih = 84, mid_y - 40, 150, 80
        pen.rounded_rectangle([ix, iy, ix + iw, iy + ih], radius=8,
                              fill=CARD, outline=tint, width=2)
        PAINTERS[painter](pen, ix, iy, iw, ih, tint)

        # text: tag, headline, one-line sub
        pen.text((txt_x, row_y + 4), tag, font=load_font(BOLD_FONT, 16), fill=AMBER)
        head_face = headline_font(pen, head, txt_w, 26)
        pen.text((txt_x, row_y + 23), head, font=head_face, fill=SNOW)
        sub_face = sub_font(pen, sub, txt_w, 1, 19)
        pen.text((txt_x, row_y + 53), sub, font=sub_face, fill=MIST)

    # --- footer ---
    pen.text((CANVAS_W / 2, 996),
             "All stories reported on 24 November 2026  ·  Sources: Reuters, AP, CNN, WSJ",
             font=load_font(REG_FONT, 14), fill=FOG, anchor="ma")

    sheet.save(OUT_FILE, "PNG", optimize=True)
    print("wrote", OUT_FILE, os.path.getsize(OUT_FILE), "bytes")


if __name__ == "__main__":
    build()
