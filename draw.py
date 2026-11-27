#!/usr/bin/env python3
"""Draw the Friday 27 November 2026 one-page newspaper (1024x1024)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 219)
PAPER = (250, 244, 228)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY = (18, 32, 66)
GOLD = (232, 184, 64)
TAN = (232, 217, 168)
BLUE = (70, 120, 170)
GREY = (90, 86, 76)
LIGHTBLUE = (178, 205, 222)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIFB = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANSB = "DejaVuSans-Bold.ttf"
SANSI = "DejaVuSerif.ttf"  # no serif italic shipped; regular serif reads as quote type

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 14
CW = W - 2 * MX


def wrap(text, f, width):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, lines, f, fill=INK, lh=None):
    if lh is None:
        lh = int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def bar(x, y, w, h, fill):
    d.rectangle([x, y, x + w, y + h], fill=fill)


def rrect(x, y, w, h, fill, outline=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill,
                        outline=outline, width=1 if outline else 0)


# ---------------------------------------------------------------- kicker
y = 6
d.text((MX, y), "THE WORLD IN ONE DAY", font=font(SANSB, 13), fill=RED)
ed = "FRIDAY EDITION"
d.text((W - MX - d.textlength(ed, font=font(SANSB, 13)), y), ed,
       font=font(SANSB, 13), fill=INK)
y = 22
# ---------------------------------------------------------------- counts strip
bar(MX, y, CW, 16, RED)
counts = "45 STORIES  \u00b7  6 REGIONS  \u00b7  10 FIELDS  \u00b7  ALL FROM THIS FRIDAY"
d.text((MX + 6, y + 1), counts, font=font(SANSB, 12), fill=(255, 255, 255))
y = 40
# ---------------------------------------------------------------- masthead
mast = "Friday 27 November 2026"
mf = font(SERIFB, 50)
d.text((MX, y), mast, font=mf, fill=INK)
y = 96
# ---------------------------------------------------------------- one sentence
sent = ("\u201cEU leaders haggle into day two, New Zealand counts its final "
        "votes, and Wall Street reopens for Black Friday.\u201d")
d.text((MX, y), sent, font=font(SANSI, 14), fill=DARKRED)
y = 116
# ---------------------------------------------------------------- UTC strip
bar(MX, y, CW, 18, RED)
d.text((MX + 6, y + 2), "THE DAY IN UTC", font=font(SANSB, 11), fill=(255, 255, 255))
utc_items = [
    ("01:00 UTC", "NZ count due"),
    ("morning", "EU summit, day 2"),
    ("07:45 CET", "French CPI"),
    ("10:00 CET", "EZ sentiment"),
    ("14:30 UTC", "Wall St reopens"),
    ("18:00 UTC", "Early close"),
]
ux = MX + 118
for t, s in utc_items:
    d.text((ux, y + 3), t, font=font(SANSB, 9), fill=GOLD)
    ux += d.textlength(t, font=font(SANSB, 9)) + 4
    d.text((ux, y + 3), s, font=font(SANS, 9), fill=(255, 255, 255))
    ux += d.textlength(s, font=font(SANS, 9)) + 12
y = 134
# ---------------------------------------------------------------- big numbers
bar(MX, y, CW, 32, NAVY)
nums = [("\u20ac1.58tn", "EU budget on table"),
        ("400,000", "NZ special votes"),
        ("1.5\u20131.5", "Chess, level"),
        ("13:00 ET", "Early Wall St close"),
        ("8 days", "Tube strike run")]
nx = MX + 8
seg = CW // 5
for i, (n, lab) in enumerate(nums):
    cx = MX + i * seg
    d.text((cx + 8, y + 1), n, font=font(SANSB, 16), fill=GOLD)
    d.text((cx + 8, y + 18), lab, font=font(SANS, 9), fill=(255, 255, 255))
y = 166
# ---------------------------------------------------------------- region strip
regions = [("ASIA", 7, (196, 120, 40)), ("AMERICAS", 9, (40, 110, 60)),
           ("EUROPE", 17, (60, 60, 160)), ("MIDDLE EAST", 7, (170, 60, 40)),
           ("AFRICA", 2, (120, 90, 30)), ("PACIFIC", 3, (30, 120, 130))]
rx = MX
seg = CW // 6
for i, (name, n, col) in enumerate(regions):
    cx = MX + i * seg
    bar(cx, y, seg - 3, 16, col)
    lab = "%s %d" % (name, n)
    d.text((cx + 6, y + 1), lab, font=font(SANSB, 11), fill=(255, 255, 255))
y = 182

# ---------------------------------------------------------------- leads
LEADS = [
    dict(num=1, tag="BRUSSELS \u00b7 EU SUMMIT", col=(60, 60, 160),
         head="EU summit, day two: \u20ac1.58tn budget still split",
         body=("27 leaders haggle over the 2028\u201334 budget and a \u20ac45bn "
               "Ukraine loan; Merz threatens a veto; deal eyed for 17\u201318 Dec."),
         src="Reuters", art="eu"),
    dict(num=2, tag="WELLINGTON \u00b7 VOTE", col=(30, 120, 130),
         head="New Zealand's final count lands today",
         body=("Official result due 14:00 local; 400,000 special votes decide "
               "if the coalition keeps its two-seat majority; four seats could flip."),
         src="Reuters", art="vote"),
    dict(num=3, tag="NEW YORK \u00b7 MARKETS", col=(196, 120, 40),
         head="Black Friday: Wall Street reopens, closes early",
         body=("Stocks resume after Thanksgiving and the nor'easter; Asia rose "
               "Thu \u2014 Nikkei +1.6%, Kospi +1.5%; gold near $3,590, Brent near $91."),
         src="Reuters", art="shop"),
    dict(num=4, tag="GAZA \u00b7 WAR", col=(170, 60, 40),
         head="Seven killed in Gaza strikes; Katz warns of wider push",
         body=("Israeli fire kills seven, including a deputy education "
               "minister; minister Katz warns an operation could displace 1m Palestinians."),
         src="Reports", art="city"),
]
LW = (CW - 3 * 4) // 4
ly = y


def lead_art(x, y0, w, h, kind):
    rrect(x, y0, w, h, (228, 222, 196), outline=(150, 140, 110))
    if kind == "eu":
        cx, cy = x + w // 2, y0 + h // 2
        d.ellipse([cx - 20, cy - 19, cx + 20, cy + 19], fill=(30, 60, 140))
        import math
        for k in range(12):
            a = math.pi * 2 * k / 12 - math.pi / 2
            sx, sy = cx + 14 * math.cos(a), cy + 14 * math.sin(a)
            d.polygon([(sx, sy - 3), (sx + 1, sy + 1), (sx + 3, sy + 1),
                       (sx + 1.4, sy + 2), (sx + 1.8, sy + 3.6),
                       (sx, sy + 2.6), (sx - 1.8, sy + 3.6), (sx - 1.4, sy + 2),
                       (sx - 3, sy + 1), (sx - 1, sy + 1)], fill=GOLD)
    elif kind == "vote":
        bx, by = x + w // 2 - 34, y0 + 10
        d.rectangle([bx, by, bx + 68, by + 38], fill=(250, 250, 250),
                    outline=NAVY, width=2)
        d.rectangle([bx + 22, by - 6, bx + 46, by + 2], fill=NAVY)
        d.line([bx + 12, by + 22, bx + 28, by + 34, bx + 56, by + 8],
               fill=RED, width=4)
    elif kind == "shop":
        sx, sy = x + w // 2 - 40, y0 + 6
        d.rectangle([sx, sy, sx + 80, sy + 32], fill=(250, 250, 250),
                    outline=DARKRED, width=2)
        d.polygon([(sx + 8, sy), (sx + 72, sy), (sx + 80, sy + 10),
                   (sx, sy + 10)], fill=RED)
        d.text((sx + 22, sy + 15), "SALE", font=font(SANSB, 13), fill=DARKRED)
        d.line([x + 12, y0 + h - 8, x + w - 12, y0 + h - 16],
               fill=(40, 110, 60), width=3)
        d.polygon([(x + w - 16, y0 + h - 20), (x + w - 8, y0 + h - 20),
                   (x + w - 12, y0 + h - 12)], fill=(40, 110, 60))
    elif kind == "city":
        bx = x + 10
        for i, bh in enumerate([34, 48, 28, 42, 24]):
            d.rectangle([bx + i * 34, y0 + h - 14 - bh, bx + i * 34 + 28,
                         y0 + h - 14], fill=(90, 90, 100))
            for wy in range(2):
                d.rectangle([bx + i * 34 + 6, y0 + h - 14 - bh + 6 + wy * 12,
                             bx + i * 34 + 12, y0 + h - 14 - bh + 10 + wy * 12],
                            fill=GOLD)
        for sx in (x + 60, x + 150):
            d.polygon([(sx, y0 + 6), (sx + 12, y0 + 6), (sx + 16, y0 + 26),
                       (sx + 4, y0 + 26)], fill=(150, 150, 150))


for i, L in enumerate(LEADS):
    x = MX + i * (LW + 4)
    d.text((x, ly), "%d \u00b7 %s" % (L["num"], L["tag"]),
           font=font(SANSB, 10), fill=L["col"])
    lead_art(x, ly + 14, LW, 54, L["art"])
    hy = ly + 72
    hl = wrap(L["head"], font(SANSB, 15), LW)
    hy = text_block(x, hy, hl, font(SANSB, 15), lh=17)
    bl = wrap(L["body"], font(SANS, 10), LW)
    hy = text_block(x, hy + 2, bl, font(SANS, 10), lh=11)
    d.text((x, hy + 2), L["src"], font=font(SANS, 9), fill=GREY)
y = ly + 164
# ---------------------------------------------------------------- smalls
SMALLS = [
    dict(num=5, tag="KATHMANDU \u00b7 JAZAN", col=(170, 60, 40),
         head="Nepal mourns worker killed at Jazan refinery",
         body=("Kathmandu condoles the death of a Nepali worker and three "
               "injured in Thu's Houthi strike; urges restraint."),
         badge="OFFICIAL", bcol=(30, 110, 60), src="ANI"),
    dict(num=6, tag="LONDON \u00b7 STRIKE", col=(178, 34, 34),
         head="Tube strike drags into Friday commute",
         body=("First of eight RMT strike days runs to noon Fri; Piccadilly "
               "shut till midday, normal service by 18:00."),
         badge="CONFIRMED", bcol=(30, 110, 60), src="Reuters / TfL"),
    dict(num=7, tag="GENEVA \u00b7 CHESS", col=(60, 60, 160),
         head="Chess rests after Game 3 thriller",
         body=("60-move draw leaves Gukesh and Sindarov level 1.5\u20131.5; "
               "Game 4 on Sat, Gukesh White."),
         badge="CONFIRMED", bcol=(30, 110, 60), src="Chess.com / FIDE"),
    dict(num=8, tag="BANGKOK \u00b7 BLAST", col=(196, 120, 40),
         head="Blast at Thai oil refinery injures seven",
         body=("Four seriously hurt in the explosion at the plant; cause "
               "under investigation."),
         badge="REPORTED", bcol=(178, 34, 34), src="Reports"),
    dict(num=9, tag="PARIS \u00b7 INFLATION", col=(30, 120, 130),
         head="French, Spanish CPI due today",
         body=("Eurozone sentiment and ECB inflation expectations also land; "
               "France Q3 GDP final seen -0.1%."),
         badge="FORECAST", bcol=(60, 60, 160), src="Eurostat / INSEE"),
    dict(num=10, tag="LONDON \u00b7 ROYALS", col=(120, 90, 30),
         head="Two held over burglary at William and Kate's home",
         body=("Arrests reported today after a break-in at the couple's "
               "country home."),
         badge="REPORTED", bcol=(178, 34, 34), src="Reports"),
    dict(num=11, tag="BAGHDAD \u00b7 TALKS", col=(40, 110, 60),
         head="Iraq judge calls national dialogue",
         body=("Top judge to convene talks on the Erbil\u2013Baghdad disputes "
               "over Kurdistan salaries."),
         badge="REPORTED", bcol=(178, 34, 34), src="Reports"),
    dict(num=12, tag="KHARTOUM \u00b7 WAR", col=(170, 60, 40),
         head="Sudan dismisses Ethiopia peace bid",
         body=("Khartoum rejects Addis Ababa's initiative to settle the war."),
         badge="REPORTED", bcol=(178, 34, 34), src="Reports"),
    dict(num=13, tag="JERUSALEM \u00b7 PEACE", col=(60, 60, 160),
         head="Kushner: drop the 'permanent war' mindset",
         body=("US envoy urges Israel to move past endless war in new Gaza "
               "remarks."),
         badge="REPORTED", bcol=(178, 34, 34), src="Reports"),
    dict(num=14, tag="BEIJING \u00b7 ECONOMY", col=(196, 120, 40),
         head="China industrial profits due today",
         body=("Plus Japan inflation; Friday's Asian data round out a "
               "holiday-thin week."),
         badge="FORECAST", bcol=(60, 60, 160), src="NBS"),
]
SW = (CW - 4 * 4) // 5
sy = y + 4
ROW_H = 108
for row in range(2):
    for c in range(5):
        S = SMALLS[row * 5 + c]
        x = MX + c * (SW + 4)
        yy = sy + row * ROW_H
        bar(x, yy, SW, 15, S["col"])
        d.text((x + 4, yy + 2), "%d \u00b7 %s" % (S["num"], S["tag"]),
               font=font(SANSB, 8), fill=(255, 255, 255))
        hl = wrap(S["head"], font(SANSB, 10), SW - 4)
        hy = text_block(x + 2, yy + 18, hl[:3], font(SANSB, 10), lh=12)
        bl = wrap(S["body"], font(SANS, 9), SW - 4)
        by = text_block(x + 2, hy + 1, bl[:3], font(SANS, 9), lh=11)
        d.rectangle([x + 2, by + 2, x + 2 + d.textlength(S["badge"], font=font(SANSB, 8)) + 6,
                     by + 11], fill=S["bcol"])
        d.text((x + 5, by + 2), S["badge"], font=font(SANSB, 8),
               fill=(255, 255, 255))
        d.text((x + 2 + d.textlength(S["badge"], font=font(SANSB, 8)) + 10, by + 2),
               S["src"], font=font(SANS, 8), fill=GREY)
y = sy + 2 * ROW_H
# ---------------------------------------------------------------- voices
bar(MX, y, CW, 18, RED)
d.text((MX + 6, y + 2), "VOICES OF THE DAY", font=font(SANSB, 11),
       fill=(255, 255, 255))
d.text((W - MX - d.textlength("IN THEIR OWN WORDS", font=font(SANSB, 9)), y + 3),
       "IN THEIR OWN WORDS", font=font(SANSB, 9), fill=(255, 255, 255))
vy = y + 20
VOICES = [
    ("\u201cIt is politically imperative to reach a definitive solution "
     "in December.\u201d", "Kyriakos Mitsotakis, PM of Greece, at the EU summit. Reuters."),
    ("\u201cWe must ensure that Ukraine receives sufficient support in "
     "the coming years.\u201d", "Friedrich Merz, Chancellor of Germany, Brussels. Reuters."),
    ("\u201cWe will not accept it being used as a vehicle for job cuts "
     "and intensified working.\u201d", "Eddie Dempsey, RMT general secretary, on the Tube strike. RMT."),
]
vx = MX
vw = CW // 3
for q, who in VOICES:
    ql = wrap(q, font(SANSI, 10), vw - 12)
    qy = text_block(vx + 4, vy, ql, font(SANSI, 10), fill=INK, lh=13)
    wl = wrap(who, font(SANS, 8), vw - 12)
    text_block(vx + 4, qy + 1, wl, font(SANS, 8), fill=GREY, lh=10)
    vx += vw
y = vy + 40
# ---------------------------------------------------------------- map + briefs
bar(MX, y, 440, 18, NAVY)
d.text((MX + 6, y + 2), "WHERE IT HAPPENED", font=font(SANSB, 11),
       fill=(255, 255, 255))
bx0 = MX + 448
bar(bx0, y, CW - 448, 18, NAVY)
d.text((bx0 + 6, y + 2), "ALSO ON FRIDAY 27 NOVEMBER \u2014 STORIES 15 TO 45",
       font=font(SANSB, 11), fill=(255, 255, 255))
my = y + 22
MAP_H = 176
d.rectangle([MX, my, MX + 440, my + MAP_H], fill=LIGHTBLUE,
            outline=(150, 140, 110))
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 38),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-115, 28), (-125, 40), (-125, 48), (-135, 58), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 76)],
    [(-80, 9), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
     (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -41),
     (-70, -50), (-73, -55), (-75, -45), (-72, -30), (-70, -18), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (32, 70), (40, 68),
     (45, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 42), (-2, 37), (-6, 36)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (33, 27),
     (35, 20), (38, 18), (43, 12), (48, 11), (51, 10), (46, 5), (42, 0),
     (40, -5), (40, -12), (36, -18), (33, -25), (28, -33), (20, -35),
     (16, -30), (13, -18), (12, -10), (9, 4), (0, 5), (-8, 5), (-13, 8),
     (-17, 12), (-17, 20), (-15, 27), (-10, 31)],
    [(30, 62), (45, 68), (55, 68), (65, 69), (75, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 58),
     (158, 52), (150, 45), (142, 42), (140, 38), (135, 34), (130, 33),
     (127, 35), (122, 38), (120, 30), (115, 23), (110, 20), (108, 12),
     (105, 9), (100, 8), (98, 15), (95, 16), (92, 21), (88, 22), (85, 19),
     (80, 13), (77, 8), (74, 20), (70, 24), (66, 25), (60, 25), (57, 26),
     (52, 28), (50, 29), (48, 30), (44, 29), (40, 30), (38, 25), (36, 20),
     (35, 15), (38, 18), (35, 22), (32, 28), (30, 36), (28, 45), (30, 50),
     (30, 55), (30, 62)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 41), (143, 43), (145, 44), (141, 42), (139, 38), (136, 35),
     (133, 34), (130, 32)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (174, -41),
     (171, -44), (168, -46)],
]


def project(lon, lat):
    px = MX + (lon + 170) / 360.0 * 440
    py = my + (75 - lat) / 130.0 * MAP_H
    return (px, py)


for poly in CONTINENTS:
    d.polygon([project(lo, la) for lo, la in poly], fill=TAN,
              outline=(150, 130, 90))
PINS = [(1, 4.35, 50.85), (2, 174.8, -41.3), (3, -74, 40.7), (4, 34.5, 31.5),
        (5, 85.3, 27.7), (6, -0.1, 51.5), (7, 6.1, 46.2), (8, 100.5, 13.75),
        (9, 2.35, 48.85), (10, -3.5, 52.5), (11, 44.4, 33.3),
        (12, 32.5, 15.6), (13, 36.5, 31.8), (14, 116.4, 39.9)]
for n, lo, la in PINS:
    px, py = project(lo, la)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255))
    lbl = str(n)
    d.text((px - d.textlength(lbl, font=font(SANSB, 8)) / 2, py - 5), lbl,
           font=font(SANSB, 8), fill=(255, 255, 255))
d.text((MX + 4, my + MAP_H - 12), "Nos. 1\u201314 pictured; 15\u201345 at right",
       font=font(SANS, 8), fill=(60, 60, 60))
BRIEFS = [
    (15, "EU summit ends Fri; Costa to table new plan.", "Reuters"),
    (16, "Merz: Ukraine must get enough support for years.", "Reuters"),
    (17, "Mitsotakis: Dec deal 'politically imperative'.", "Reuters"),
    (18, "NZ closest seats: Wairarapa 139, Mt Roskill 262.", "1News"),
    (19, "Opportunity Party crossed 5%, a first in a decade.", "Reports"),
    (20, "US markets shut Thu; Fri session ends 13:00 ET.", "NYSE"),
    (21, "Nor'easter: gusts to 50 mph, up to 3 in of rain.", "NWS"),
    (22, "NBC airs 2025 parade rerun; 100th march is Sat.", "NBC"),
    (23, "Gold near $3,590 after a 14-month low near $3,425.", "Reuters"),
    (24, "Brent holds near $91 after Gulf shipping attacks.", "Reuters"),
    (25, "S&P futures +0.5%, Nasdaq +0.4% in thin trade.", "Reuters"),
    (26, "Dollar at 159.14 yen; euro at $1.0961.", "Reports"),
    (27, "Sudanese return to Khartoum, find homes in ruins.", "Reports"),
    (28, "UK to get 'Swiss-like' rights under new EU deals.", "Reports"),
    (29, "European states join to buy BAE combat vehicles.", "Reports"),
    (30, "French factory-gate prices rose 9.6% in Oct.", "INSEE"),
    (31, "Germany expands return plan for Syrian refugees.", "Reports"),
    (32, "Myanmar rejects parts of the genocide ruling.", "Reports"),
    (33, "Erdogan welcomes Libya's Haftar in Ankara.", "Reports"),
    (34, "IISS: Kremlin threat to Europe's railways, grids.", "IISS"),
    (35, "UN trade body backs Palestinian recovery plan.", "UNCTAD"),
    (36, "Jolie and Pitt settle French winery lawsuit.", "Reports"),
    (37, "Hong Kong marks a year since the tower fire.", "Reports"),
    (38, "France cyber chief warns of unprecedented threat.", "Reports"),
    (39, "Estonia moves to shut rail border with Russia.", "Reports"),
    (40, "Armenia plans full exit of Russian border troops.", "Reports"),
    (41, "Putin pushes broad AI use in Russia.", "Reports"),
    (42, "Brazil condemns Trump's new tariff proposals.", "Reports"),
    (43, "Vietnam hurries to seal a US trade deal.", "Reports"),
    (44, "India disputes US 'overcapacity' claims.", "Reports"),
    (45, "Iraq court jails eight Frenchmen for life over ISIS.", "Reports"),
]
bf = font(SANS, 9)
col_w = (CW - 448 - 8) // 2
col_y = [my, my]
for i, (n, txt, src) in enumerate(BRIEFS):
    col = i // 16
    row_y = col_y[col]
    if row_y > my + MAP_H - 10:
        continue
    bx = bx0 + col * (col_w + 8)
    line = "%d. %s" % (n, txt)
    lines = wrap(line, bf, col_w)
    for j, ln in enumerate(lines[:2]):
        d.text((bx, row_y + j * 11), ln, font=bf, fill=INK)
    col_y[col] += 11 * len(lines[:2])
y = my + MAP_H + 4
# ---------------------------------------------------------------- chart + how to read
bar(MX, y, 640, 18, NAVY)
d.text((MX + 6, y + 2), "THE DAY IN ONE CHART \u2014 THU 26 NOV CLOSES",
       font=font(SANSB, 11), fill=(255, 255, 255))
hx = MX + 648
bar(hx, y, CW - 648, 18, RED)
d.text((hx + 6, y + 2), "HOW TO READ THE TAGS", font=font(SANSB, 11),
       fill=(255, 255, 255))
cy = y + 20
CHART = [("Nikkei", 1.6), ("Kospi", 1.5), ("Hang Seng", 1.9),
         ("Shanghai", 0.0), ("DAX", 1.8)]
for name, v in CHART:
    d.text((MX, cy), name, font=font(SANS, 10), fill=INK)
    bx = MX + 76
    bw = int(abs(v) * 90)
    col = (40, 110, 60) if v >= 0 else RED
    bar(bx, cy + 1, max(bw, 2), 9, col)
    d.text((bx + bw + 5, cy), "%+.1f%%" % v, font=font(SANSB, 10), fill=INK)
    cy += 11
d.text((MX, cy + 1), "Asia and Europe rebound, led by chips. WSJ closes.",
       font=font(SANS, 9), fill=GREY)
TAGS = [("CONFIRMED", (30, 110, 60), "verified"),
        ("REPORTED", (178, 34, 34), "one outlet"),
        ("CLAIM", (120, 60, 30), "one side's word"),
        ("FORECAST", (60, 60, 160), "due / expected"),
        ("OFFICIAL", (20, 60, 110), "official source")]
ty = y + 20
for name, col, mean in TAGS:
    d.rectangle([hx, ty, hx + 78, ty + 11], fill=col)
    d.text((hx + 4, ty + 1), name, font=font(SANSB, 8), fill=(255, 255, 255))
    d.text((hx + 84, ty + 1), mean, font=font(SANS, 9), fill=INK)
    ty += 11
y = cy + 12
# ---------------------------------------------------------------- what to watch
bar(MX, y, CW, 16, NAVY)
d.text((MX + 6, y + 1), "WHAT TO WATCH TOMORROW \u2014 SAT 28 NOV:",
       font=font(SANSB, 11), fill=GOLD)
wt = ("Macy's 100th parade marches, 08:30 ET  \u00b7  Chess Game 4, "
      "Gukesh White  \u00b7  NZ coalition talks begin  \u00b7  EU budget talks resume.")
d.text((MX + 322, y + 1), wt, font=font(SANS, 9), fill=(255, 255, 255))
y += 20
# ---------------------------------------------------------------- date check
bar(MX, y, CW, 16, RED)
d.text((MX + 6, y + 1), "DATE CHECK \u2014 LEFT OUT ON PURPOSE: FIRST REPORTED BEFORE TODAY",
       font=font(SANSB, 11), fill=(255, 255, 255))
y += 18
dc1 = ("THU 26 NOV: Kim tours nuclear plants, orders wider tactical nukes; "
       "Houthis hit Jazan refinery, 1 Nepali worker killed; Chess Game 3 drawn, "
       "1.5\u20131.5; Tube strike begins; EU summit opens; Indonesia mine flood kills 14.")
dc2 = ("WED 25 NOV: Cairo tanker fire kills 31; PCE + GDP land; Shenzhou-24 "
       "lifts off; Macy's parade moved; $621.9m F-16 sale.  TUE 24 NOV: Dow "
       "tops 50,000; Chen probe; CIA breach.  12 NOV: Gibran quits as VP.")
for ln in wrap(dc1, font(SANS, 9), CW):
    d.text((MX, y), ln, font=font(SANS, 9), fill=INK)
    y += 10
for ln in wrap(dc2, font(SANS, 9), CW):
    d.text((MX, y), ln, font=font(SANS, 9), fill=INK)
    y += 10
y += 2
# ---------------------------------------------------------------- sources
srcs = ("Sources: Reuters, AP, ANI, Chess.com, FIDE, TfL, NWS, INSEE, Eurostat, "
        "UNCTAD, IISS, 1News, NBC, NYSE, WSJ \u00b7 Original drawings")
d.text((MX, y), srcs, font=font(SANS, 9), fill=GREY)
y += 10
foot = ("Every story here happened, or was first reported, on Fri 27 Nov 2026. "
        "Claims attributed.")
d.text((MX, y), foot, font=font(SANSB, 9), fill=INK)
y += 10
print("final y =", y)
img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"),
         optimize=True)
print("saved entry.png")
