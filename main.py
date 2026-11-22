#!/usr/bin/env python3
"""The World in One Day -- 22 November 2026.

A newspaper front page summing up the world's news of Sunday
22 November 2026, drawn entirely with the Python standard library
(zlib + struct PNG encoder, hand-built 5x7 bitmap font).

Writes /output/entry.png (1024x1024, deterministic, no network).
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font -----
# 5x7 bitmap font, written for this entry. '#' is an ink pixel.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "#": ("10101", "10101", "11111", "10101", "11111", "10101", "10101"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
}

CHAR_W = 6  # 5 px glyph + 1 px gap, at scale 1
CHAR_H = 7


def text_width(text, scale):
    return len(text) * CHAR_W * scale - scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if text_width(trial, scale) <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ------------------------------------------------------------- canvas ------
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, color):
        self.rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.rect(x, y, 1, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def text(self, s, x, y, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch.upper(), FONT["?"])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += CHAR_W * scale
        return cx

    def text_center(self, s, cx, y, scale, color):
        self.text(s, cx - text_width(s, scale) // 2, y, scale, color)

    def text_right(self, s, x_right, y, scale, color):
        self.text(s, x_right - text_width(s, scale), y, scale, color)


# --------------------------------------------------------- PNG encoder -----
def png_bytes(canvas):
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * canvas.w * 3:(y + 1) * canvas.w * 3]
    comp = zlib.compress(bytes(raw), 6)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ------------------------------------------------------------- palette -----
PAPER = (247, 242, 232)
INK = (18, 18, 18)
RED = (172, 32, 24)
NAVY = (16, 34, 66)
SEA = (24, 68, 104)
SKY_ORANGE = (224, 122, 44)
SMOKE = (120, 118, 110)
LIGHT = (247, 242, 232)
GOLD = (214, 164, 60)

W, H = 1024, 1024
M = 36                      # page margin
CW = W - 2 * M              # content width = 952


def draw_photo(c, x, y, w, h):
    """Stylised night scene over the Gulf: sky, sea, ships, missile arcs."""
    # sky: dark navy bands warming toward the horizon
    bands = [(16, 34, 66), (24, 46, 82), (38, 62, 96), (66, 84, 108),
             (120, 96, 84), (196, 116, 52)]
    horizon = y + int(h * 0.62)
    for i, col in enumerate(bands):
        y0 = y + i * (horizon - y) // len(bands)
        y1 = y + (i + 1) * (horizon - y) // len(bands)
        c.rect(x, y0, w, y1 - y0, col)
    # low sun / glow on the horizon
    c.disc(x + w // 2, horizon - 6, 26, (238, 176, 96))
    c.disc(x + w // 2, horizon - 6, 16, (246, 214, 150))
    # sea
    c.rect(x, horizon, w, y + h - horizon, SEA)
    for k in range(5):
        wy = horizon + 12 + k * 14
        c.hline(x + 20 + k * 40, wy, w - 40 - k * 80, (90, 140, 170))
    # two ships, dark silhouettes
    for sx, sw in ((x + 90, 150), (x + w - 300, 190)):
        c.rect(sx, horizon - 26, sw, 26, (10, 14, 20))
        c.rect(sx + sw // 3, horizon - 44, 16, 20, (10, 14, 20))
        c.rect(sx + sw // 2 + 20, horizon - 36, 10, 12, (10, 14, 20))
        for wx in range(sx + 12, sx + sw - 12, 22):
            c.rect(wx, horizon - 18, 8, 6, (240, 190, 90))
    # smoke columns rising from the ships
    for sx in (x + 150, x + w - 220):
        for k in range(6):
            c.disc(sx + (k % 2) * 8 - 4, horizon - 52 - k * 12,
                   10 + k, SMOKE)
    # missile arcs: bright dots along quadratic curves
    arcs = [((x + 60, horizon - 40), (x + w // 2, y + 6),
             (x + w - 120, horizon - 30)),
            ((x + 220, horizon - 20), (x + w // 2 + 140, y + 30),
             (x + w - 60, horizon - 55))]
    for (p0, p1, p2) in arcs:
        for t_i in range(0, 41):
            t = t_i / 40.0
            bx = int((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0]
                     + t * t * p2[0])
            by = int((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1]
                     + t * t * p2[1])
            c.disc(bx, by, 2, (250, 240, 210))
    # frame
    c.rect(x, y, w, 3, INK)
    c.rect(x, y + h - 3, w, 3, INK)
    c.rect(x, y, 3, h, INK)
    c.rect(x + w - 3, y, 3, h, INK)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT", "/output")
    os.makedirs(out_dir, exist_ok=True)

    c = Canvas(W, H, PAPER)

    # ---- masthead ----
    c.text_center("THE WORLD IN ONE DAY", W // 2, 26, 7, INK)
    c.hline(M, 92, CW, INK)
    c.hline(M, 96, CW, INK)
    c.text("SUNDAY, 22 NOVEMBER 2026", M, 108, 2, INK)
    c.text_right("No. 326", W - M, 108, 2, INK)
    c.hline(M, 130, CW, INK)
    c.hline(M, 134, CW, INK)

    # ---- lead story ----
    y = 150
    c.text_center("LEAD STORY - THE GULF WAR WIDENS", W // 2, y, 2, RED)
    y = 176
    c.text_center("IRAN STRIKES U.S. BASES", W // 2, y, 5, INK)
    y = 216
    c.text_center("IN BAHRAIN AGAIN", W // 2, y, 5, INK)
    y = 262
    sub = ("Sirens sound across Manama as Revolutionary Guards hit Sheikh Isa "
           "air base and the U.S. Navy's Fifth Fleet home at Juffair - the "
           "fourth attack on Bahrain in nine days.")
    for line in wrap_text(sub, 860, 2):
        c.text_center(line, W // 2, y, 2, INK)
        y += 18

    # ---- photo panel ----
    photo_y = y + 12
    photo_h = 190
    draw_photo(c, M, photo_y, CW, photo_h)
    y = photo_y + photo_h + 10
    c.text_center("NIGHT OVER THE GULF: DRONES AND MISSILES TRADE BLOWS AS "
                  "THE WAR SPREADS TO AMERICA'S ALLIES.", W // 2, y, 1, INK)
    y += 22
    c.hline(M, y, CW, INK)
    y += 14

    # ---- two columns ----
    col_x = M
    col_w = 560
    side_x = M + col_w + 24
    side_w = CW - col_w - 24
    top = y

    # left column: Kyiv bridges
    ly = top
    for line in wrap_text("KYIV'S BRIDGES HIT IN", col_w, 3):
        c.text(line, col_x, ly, 3, INK)
        ly += 26
    for line in wrap_text("515-MISSILE NIGHT", col_w, 3):
        c.text(line, col_x, ly, 3, INK)
        ly += 26
    ly += 4
    body1 = ("Russia fired 27 ballistic missiles, 84 cruise missiles and 404 "
             "drones at Ukraine overnight on 19-20 November - its biggest "
             "barrage of the month. Three bridges over the Dnipro in Kyiv "
             "were damaged and at least eight people were killed. Missiles "
             "and a drone also came down in Poland.")
    for line in wrap_text(body1, col_w, 2):
        c.text(line, col_x, ly, 2, INK)
        ly += 16
    ly += 8
    for line in wrap_text("KRYVYI RIH: CHILD AND", col_w, 3):
        c.text(line, col_x, ly, 3, INK)
        ly += 26
    for line in wrap_text("PARAMEDIC KILLED", col_w, 3):
        c.text(line, col_x, ly, 3, INK)
        ly += 26
    ly += 4
    body2 = ("A Russian double-tap strike on the city on 20 November killed "
             "a seven-year-old boy and a 20-year-old paramedic and injured "
             "52 people, on World Children's Day.")
    for line in wrap_text(body2, col_w, 2):
        c.text(line, col_x, ly, 2, INK)
        ly += 16

    # right column: also today
    ry = top
    c.rect(side_x, ry, side_w, 30, INK)
    c.text("ALSO TODAY", side_x + 10, ry + 8, 2, PAPER)
    ry += 42
    items = [
        ("COP31 DEADLOCK", "Climate talks stall as nations split over fossil fuels."),
        ("PERU QUAKE", "Magnitude 6.9 earthquake shakes the Andes."),
        ("BALTIC DRONES", "Drones hit a Russian cargo ship in the Gulf of Finland."),
        ("CYCLONE AKVAN", "Storm disrupts flights in eastern India."),
        ("KINGPIN CAUGHT", "Mexican army captures drug lord 'El Chapo Isidro'."),
        ("FBI HACK PROBE", "FBI probes an apparent hack of its crime database."),
    ]
    for head, body in items:
        c.text(head, side_x, ry, 2, RED)
        ry += 18
        for line in wrap_text(body, side_w, 2):
            c.text(line, side_x, ry, 2, INK)
            ry += 15
        ry += 6

    # ---- sport strip + footer ----
    fy = max(ly, ry) + 14
    c.hline(M, fy, CW, INK)
    fy += 12
    sport = ("SPORT: India v New Zealand in windy Wellington; Cummins keeps "
             "Test captaincy.")
    for line in wrap_text(sport, CW, 2):
        c.text(line, M, fy, 2, INK)
        fy += 18
    fy += 6
    c.hline(M, fy, CW, INK)
    fy += 10
    c.text_center("SOURCES: REUTERS - AP - BBC - ISW - U.S. CENTRAL COMMAND",
                  W // 2, fy, 1, INK)
    fy += 12
    c.text_center("ONE IMAGE, THE WHOLE WORLD - 22 NOVEMBER 2026",
                  W // 2, fy, 1, INK)

    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(png_bytes(c))
    print("wrote", path)


if __name__ == "__main__":
    main()
