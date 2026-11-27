"""Draw the Friday 27 November 2026 one-page newspaper (v2).

v2 changes (per Asep): every column story gets a small drawn thumbnail,
the brief list uses coloured text, and each map pin number wears the same
colour as its story number in the list below.
"""
import colorsys
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
PAPER_DARK = (238, 229, 200)
INK = (22, 22, 26)
NAVY = (16, 34, 64)
NAVY2 = (32, 60, 100)
RULE = (128, 118, 92)
MUTE = (96, 90, 74)
SEA = (183, 212, 229)
LAND = (231, 213, 174)
ROW_TINT = (240, 232, 208)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif(size, bold=False):
    return _font("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def sans(size, bold=False):
    return _font("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def pal(n):
    """One distinct dark colour per story number (golden-angle hue)."""
    h = ((n * 137.508) % 360.0) / 360.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.72, 0.42)
    return (int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5))


def wrap(d, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, num, size=15):
    """Coloured rounded number chip with white bold digits; returns width."""
    c = pal(num)
    w = size + 6 if num < 10 else size + 13
    d.rounded_rectangle([x, y, x + w, y + size], radius=size // 2, fill=c)
    d.text((x + w / 2, y + size / 2 + 0.5), str(num),
           font=sans(max(8, size - 5), bold=True), fill=(255, 255, 255), anchor="mm")
    return w


def pin(d, cx, cy, num, r=9):
    """Coloured map pin: filled circle, white ring, white bold number."""
    c = pal(num)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=(255, 255, 255), width=1)
    d.text((cx, cy + 0.5), str(num), font=sans(8, bold=True),
           fill=(255, 255, 255), anchor="mm")


def star(d, cx, cy, r, fill):
    """Five-point star centred on (cx, cy)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

# ---------------------------------------------------------------- data ---

MASTHEAD = "Friday 27 November 2026"
QUOTE = ("EU leaders haggle into day two, New Zealand counts its final votes, "
         "and Wall Street reopens for Black Friday.")

UTC_ITEMS = [
    ("01:00 UTC", "NZ count due"),
    ("morning", "EU summit, day 2"),
    ("07:45 CET", "French CPI"),
    ("10:00 CET", "EZ sentiment"),
    ("14:30 UTC", "Wall St reopens"),
    ("18:00 UTC", "Early close"),
]

BIG_NUMBERS = [
    ("\u20ac1.58tn", "EU budget on table"),
    ("400,000", "NZ special votes"),
    ("1.5\u20131.5", "Chess, level"),
    ("13:00 ET", "Early Wall St close"),
    ("8 days", "Tube strike run"),
]

REGIONS = [
    ("ASIA", 7), ("AMERICAS", 9), ("EUROPE", 17),
    ("MIDDLE EAST", 7), ("AFRICA", 2), ("PACIFIC", 3),
]

LEADS = [
    dict(n=1, city="BRUSSELS", tag="EU SUMMIT",
         head="EU summit, day two: \u20ac1.58tn budget still split",
         body=("27 leaders haggle over the 2028\u201334 budget and a \u20ac45bn Ukraine "
               "loan; Merz threatens a veto; deal eyed for 17\u201318 Dec."),
         src="Reuters"),
    dict(n=2, city="WELLINGTON", tag="VOTE",
         head="New Zealand's final count lands today",
         body=("Official result due 14:00 local; 400,000 special votes decide if "
               "the coalition keeps its two-seat majority; four seats could flip."),
         src="Reuters"),
    dict(n=3, city="NEW YORK", tag="MARKETS",
         head="Black Friday: Wall Street reopens, closes early",
         body=("Stocks resume after Thanksgiving and the nor'easter; Asia rose Thu "
               "\u2014 Nikkei +1.6%, Kospi +1.5%; gold near $3,590, Brent near $91."),
         src="Reuters"),
    dict(n=4, city="GAZA", tag="WAR",
         head="Seven killed in Gaza strikes; Katz warns of wider push",
         body=("Israeli fire kills seven, including a deputy education minister; "
               "minister Katz warns an operation could displace 1m Palestinians."),
         src="Reports"),
]

STORIES = [
    dict(n=5, city="KATHMANDU", tag="JAZAN",
         head="Nepal mourns worker killed at Jazan refinery",
         body=("Kathmandu condoles the death of a Nepali worker and three injured "
               "in Thu's Houthi strike; urges restraint."),
         tag2="OFFICIAL", src="ANI"),
    dict(n=6, city="LONDON", tag="STRIKE",
         head="Tube strike drags into Friday commute",
         body=("First of eight RMT strike days runs to noon Fri; Piccadilly shut "
               "till midday, normal service by 18:00."),
         tag2="CONFIRMED", src="Reuters / TfL"),
    dict(n=7, city="GENEVA", tag="CHESS",
         head="Chess rests after Game 3 thriller",
         body=("60-move draw leaves Gukesh and Sindarov level 1.5\u20131.5; "
               "Game 4 on Sat, Gukesh White."),
         tag2="CONFIRMED", src="Chess.com / FIDE"),
    dict(n=8, city="BANGKOK", tag="BLAST",
         head="Blast at Thai oil refinery injures seven",
         body=("Four seriously hurt in the explosion at the plant; cause under "
               "investigation."),
         tag2="REPORTED", src="Reports"),
    dict(n=9, city="PARIS", tag="INFLATION",
         head="French, Spanish CPI due today",
         body=("Eurozone sentiment and ECB inflation expectations also land; "
               "France Q3 GDP final seen -0.1%."),
         tag2="FORECAST", src="Eurostat / INSEE"),
    dict(n=10, city="LONDON", tag="ROYALS",
         head="Two held over burglary at William and Kate's home",
         body=("Arrests reported today after a break-in at the couple's country "
               "home."),
         tag2="REPORTED", src="Reports"),
    dict(n=11, city="BAGHDAD", tag="TALKS",
         head="Iraq judge calls national dialogue",
         body=("Top judge to convene talks on the Erbil\u2013Baghdad disputes over "
               "Kurdistan salaries."),
         tag2="REPORTED", src="Reports"),
    dict(n=12, city="KHARTOUM", tag="WAR",
         head="Sudan dismisses Ethiopia peace bid",
         body=("Khartoum rejects Addis Ababa's initiative to settle the war."),
         tag2="REPORTED", src="Reports"),
    dict(n=13, city="JERUSALEM", tag="PEACE",
         head="Kushner: drop the 'permanent war' mindset",
         body=("US envoy urges Israel to move past endless war in new Gaza "
               "remarks."),
         tag2="REPORTED", src="Reports"),
    dict(n=14, city="BEIJING", tag="ECONOMY",
         head="China industrial profits due today",
         body=("Plus Japan inflation; Friday's Asian data round out a "
               "holiday-thin week."),
         tag2="FORECAST", src="NBS"),
]

VOICES = [
    ("Mitsotakis",
     "\u201cIt is politically imperative to reach a definitive solution in December.\u201d",
     "PM of Greece, at the EU summit. Reuters."),
    ("Merz",
     "\u201cWe must ensure that Ukraine receives sufficient support in the coming years.\u201d",
     "Chancellor of Germany, Brussels. Reuters."),
    ("Dempsey",
     "\u201cWe will not accept it being used as a vehicle for job cuts and intensified working.\u201d",
     "RMT general secretary, on the Tube strike. RMT."),
]

BRIEFS = [
    "EU summit ends Fri; Costa to table new plan.",
    "Merz: Ukraine must get enough support for years.",
    "Mitsotakis: Dec deal \u2018politically imperative\u2019.",
    "NZ closest seats: Wairarapa 139, Mt Roskill 262.",
    "Opportunity Party crossed 5%, a first in a decade.",
    "US markets shut Thu; Fri session ends 13:00 ET.",
    "Nor\u2019easter: gusts to 50 mph, up to 3 in of rain.",
    "NBC airs 2025 parade rerun; 100th march is Sat.",
    "Gold near $3,590 after a 14-month low near $3,425.",
    "Brent holds near $91 after Gulf shipping attacks.",
    "S&P futures +0.5%, Nasdaq +0.4% in thin trade.",
    "Dollar at 159.14 yen; euro at $1.0961.",
    "Sudanese return to Khartoum, find homes in ruins.",
    "UK to get \u2018Swiss-like\u2019 rights under new EU deals.",
    "European states join to buy BAE combat vehicles.",
    "French factory-gate prices rose 9.6% in Oct.",
    "Germany expands return plan for Syrian refugees.",
    "Myanmar rejects parts of the genocide ruling.",
    "Erdogan welcomes Libya\u2019s Haftar in Ankara.",
    "IISS: Kremlin threat to Europe\u2019s railways, grids.",
    "UN trade body backs Palestinian recovery plan.",
    "Jolie and Pitt settle French winery lawsuit.",
    "Hong Kong marks a year since the tower fire.",
    "France cyber chief warns of unprecedented threat.",
    "Estonia moves to shut rail border with Russia.",
    "Armenia plans full exit of Russian border troops.",
    "Putin pushes broad AI use in Russia.",
    "Brazil condemns Trump\u2019s new tariff proposals.",
    "Vietnam hurries to seal a US trade deal.",
    "India disputes US \u2018overcapacity\u2019 claims.",
    "Iraq court jails eight Frenchmen for life over ISIS.",
]

CHART = [
    ("Nikkei", "+1.6%"), ("Kospi", "+1.5%"), ("Hang Seng", "+1.9%"),
    ("Shanghai", "+0.0%"), ("DAX", "+1.8%"),
]

TAGS = [
    ("CONFIRMED", "verified"),
    ("REPORTED", "one outlet"),
    ("CLAIM", "one side\u2019s word"),
    ("FORECAST", "due / expected"),
    ("OFFICIAL", "official source"),
]

WATCH = ("Macy\u2019s 100th parade marches, 08:30 ET \u00b7 Chess Game 4, Gukesh White "
         "\u00b7 NZ coalition talks begin \u00b7 EU budget talks resume.")

DATECHECK = [
    ("THU 26 NOV: ", "Kim tours nuclear plants, orders wider tactical nukes; "
     "Houthis hit Jazan refinery, 1 Nepali worker killed; Chess Game 3 drawn, "
     "1.5\u20131.5; Tube strike begins; EU summit opens; Indonesia mine flood kills 14."),
    ("WED 25 NOV: ", "Cairo tanker fire kills 31; PCE + GDP land; Shenzhen-24 "
     "lifts off; Macy\u2019s parade moved; $621.9m F-16 sale."),
    ("TUE 24 NOV: ", "Dow tops 50,000; Chen probe; CIA breach.  12 NOV: "
     "Gibran quits as VP."),
]

FOOTER_SOURCES = ("Sources: Reuters, AP, ANI, Chess.com, FIDE, TfL, NWS, INSEE, "
                  "Eurostat, UNCTAD, IISS, 1News, NBC, NYSE, WSJ \u00b7 Original drawings")
FOOTER_NOTE = ("Every story here happened, or was first reported, on Fri 27 Nov 2026. "
               "Claims attributed.")

# ------------------------------------------------------- illustrations ---

def lead_art(d, n, x, y, w, h):
    """Big hand-drawn illustration for each lead story."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 200), outline=RULE)
    if n == 1:
        # EU flag: blue field, twelve gold stars in a circle.
        d.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], fill=(28, 52, 110))
        cx, cy = x + w // 2, y + h // 2
        for i in range(12):
            ang = -math.pi / 2 + i * math.pi / 6
            star(d, cx + 30 * math.cos(ang), cy + 30 * math.sin(ang), 6,
                 (255, 204, 0))
    elif n == 2:
        # Ballot box with a red check.
        bx, by, bw, bh = x + w // 2 - 46, y + 16, 92, 52
        d.rectangle([bx, by, bx + bw, by + bh], fill=(250, 248, 240),
                    outline=NAVY, width=2)
        d.rectangle([bx + 18, by - 6, bx + bw - 18, by + 2], fill=NAVY)
        d.line([bx + 8, by + 30, bx + 34, by + 48, bx + 84, by + 6],
               fill=(200, 30, 30), width=6)
    elif n == 3:
        # SALE tag with a rising market line.
        d.polygon([(x + 18, y + 14), (x + 78, y + 14), (x + 96, y + 32),
                   (x + 78, y + 50), (x + 18, y + 50)], fill=(196, 28, 28))
        d.ellipse([x + 82, y + 26, x + 90, y + 34], fill=PAPER)
        d.text((x + 52, y + 32), "SALE", font=sans(13, bold=True),
               fill=(255, 255, 255), anchor="mm")
        pts = [(x + 110, y + 62), (x + 140, y + 48), (x + 168, y + 54),
               (x + 196, y + 30), (x + 224, y + 18)]
        d.line(pts, fill=(24, 130, 60), width=4)
        d.polygon([(x + 224, y + 18), (x + 216, y + 18), (x + 224, y + 10)],
                  fill=(24, 130, 60))
    else:
        # Gaza buildings under a grey sky.
        d.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], fill=(196, 188, 168))
        for bx, bw, bh in ((int(x + 18), 44, 46), (int(x + 74), 52, 60),
                           (int(x + 138), 40, 38), (int(x + 188), 46, 54)):
            d.rectangle([bx, y + h - 6 - bh, bx + bw, y + h - 6],
                        fill=(88, 84, 76))
            for wy in range(y + h - 6 - bh + 8, y + h - 10, 12):
                for wx in range(bx + 6, bx + bw - 6, 12):
                    d.rectangle([wx, wy, wx + 6, wy + 6], fill=(220, 210, 180))
        d.ellipse([x + 120, y + 8, x + 138, y + 26], fill=(120, 112, 96))
        d.ellipse([x + 138, y + 4, x + 152, y + 18], fill=(120, 112, 96))


def thumb(d, n, x, y, w, h):
    """Small hand-drawn strip (~196x36) for each small story 5-14."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 200), outline=RULE)
    cx, cy = x + w // 2, y + h // 2
    if n == 5:
        # Refinery with flame.
        d.rectangle([x + 8, cy + 2, x + w - 8, y + h - 4], fill=(120, 112, 96))
        d.rectangle([x + 20, cy - 12, x + 30, cy + 2], fill=(70, 66, 58))
        d.polygon([(cx - 6, cy - 2), (cx + 6, cy - 2), (cx, cy - 16)],
                  fill=(230, 110, 20))
        d.ellipse([cx - 3, cy - 8, cx + 3, cy - 2], fill=(255, 200, 60))
    elif n == 6:
        # Tube roundel and train.
        d.ellipse([cx - 34, cy - 12, cx - 10, cy + 12], outline=(200, 30, 30),
                  width=4)
        d.rectangle([cx - 40, cy - 3, cx - 4, cy + 3], fill=(28, 52, 110))
        d.rectangle([cx + 2, cy - 8, cx + 38, cy + 10], fill=(40, 60, 90))
        d.rectangle([cx + 8, cy - 4, cx + 16, cy + 2], fill=(190, 220, 240))
        d.rectangle([cx + 22, cy - 4, cx + 30, cy + 2], fill=(190, 220, 240))
    elif n == 7:
        # 4x4 chess board.
        bs = 7
        ox, oy = cx - 2 * bs, cy - 2 * bs
        for r in range(4):
            for c in range(4):
                col = (250, 248, 240) if (r + c) % 2 == 0 else (40, 40, 44)
                d.rectangle([ox + c * bs, oy + r * bs,
                             ox + (c + 1) * bs, oy + (r + 1) * bs], fill=col)
        d.rectangle([ox - 2, oy - 2, ox + 4 * bs + 2, oy + 4 * bs + 2],
                    outline=NAVY, width=1)
    elif n == 8:
        # Refinery with explosion starburst.
        d.rectangle([x + 8, cy + 4, x + w - 8, y + h - 4], fill=(120, 112, 96))
        d.rectangle([cx - 26, cy - 10, cx - 16, cy + 4], fill=(70, 66, 58))
        star(d, cx + 14, cy - 6, 12, (240, 140, 20))
        star(d, cx + 14, cy - 6, 6, (255, 210, 80))
    elif n == 9:
        # Bar chart with a percent sign.
        base = y + h - 6
        for i, bh in enumerate((10, 16, 22)):
            bx = cx - 34 + i * 14
            d.rectangle([bx, base - bh, bx + 9, base], fill=(32, 90, 150))
        d.text((cx + 22, cy), "%", font=sans(15, bold=True),
               fill=(32, 90, 150), anchor="mm")
    elif n == 10:
        # House with a crown.
        d.polygon([(cx - 22, cy + 2), (cx, cy - 12), (cx + 22, cy + 2)],
                  fill=(150, 40, 40))
        d.rectangle([cx - 18, cy + 2, cx + 18, cy + 12], fill=(210, 190, 150))
        d.polygon([(cx - 12, cy - 16), (cx - 6, cy - 24), (cx, cy - 17),
                   (cx + 6, cy - 24), (cx + 12, cy - 16)],
                  fill=(230, 180, 40))
    elif n == 11:
        # Two speech bubbles.
        d.rounded_rectangle([cx - 36, cy - 12, cx - 2, cy + 2], radius=5,
                            fill=(250, 248, 240), outline=NAVY)
        d.rounded_rectangle([cx + 2, cy - 2, cx + 36, cy + 12], radius=5,
                            fill=(220, 232, 244), outline=NAVY)
        d.line([cx - 10, cy - 12, cx + 8, cy - 12], fill=NAVY, width=1)
        d.line([cx + 8, cy + 2, cx + 26, cy + 2], fill=NAVY, width=1)
    elif n == 12:
        # Peace symbol.
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13],
                  outline=(32, 90, 60), width=3)
        d.line([cx, cy - 13, cx, cy + 13], fill=(32, 90, 60), width=3)
        d.line([cx, cy, cx - 10, cy + 10], fill=(32, 90, 60), width=3)
        d.line([cx, cy, cx + 10, cy + 10], fill=(32, 90, 60), width=3)
    elif n == 13:
        # Dove on blue.
        d.ellipse([cx - 18, cy - 8, cx + 10, cy + 8], fill=(250, 250, 250))
        d.ellipse([cx + 6, cy - 12, cx + 18, cy - 2], fill=(250, 250, 250))
        d.polygon([(cx + 16, cy - 8), (cx + 26, cy - 5), (cx + 16, cy - 3)],
                  fill=(230, 140, 40))
        d.arc([cx - 22, cy - 16, cx + 2, cy + 2], 200, 340,
              fill=(120, 130, 140), width=2)
    else:
        # Factory with a rising arrow.
        d.rectangle([cx - 34, cy - 2, cx + 6, cy + 12], fill=(90, 86, 78))
        d.polygon([(cx - 34, cy - 2), (cx - 26, cy - 12), (cx - 18, cy - 2),
                   (cx - 10, cy - 12), (cx - 2, cy - 2)], fill=(90, 86, 78))
        d.line([cx + 12, cy + 10, cx + 12, cy - 10], fill=(24, 130, 60), width=3)
        d.polygon([(cx + 12, cy - 14), (cx + 6, cy - 6), (cx + 18, cy - 6)],
                  fill=(24, 130, 60))

# ------------------------------------------------------------ sections ---

def draw_top_strip(d, y, h=16):
    d.rectangle([0, y, W, y + h], fill=NAVY)
    left = "45 STORIES  \u00b7  6 REGIONS  \u00b7  10 FIELDS  \u00b7  ALL FROM THIS FRIDAY"
    d.text((10, y + h // 2), left, font=sans(9, bold=True),
           fill=(255, 255, 255), anchor="lm")
    d.text((W - 10, y + h // 2), "FRIDAY EDITION", font=sans(9, bold=True),
           fill=(255, 214, 90), anchor="rm")
    return y + h


def draw_masthead(d, y):
    d.text((W // 2, y + 20), MASTHEAD, font=serif(36, bold=True),
           fill=INK, anchor="mm")
    y += 40
    d.text((W // 2, y + 9), QUOTE, font=serif(13), fill=NAVY2, anchor="mm")
    y += 18
    d.line([10, y, W - 10, y], fill=RULE, width=1)
    return y + 3


def draw_utc(d, y):
    d.text((10, y + 11), "THE DAY IN UTC", font=sans(9, bold=True),
           fill=NAVY, anchor="lm")
    x = 132
    seg = (W - 10 - x) / len(UTC_ITEMS)
    for i, (t, label) in enumerate(UTC_ITEMS):
        cx = x + seg * i + seg / 2
        d.text((cx, y + 4), t, font=sans(9, bold=True), fill=INK, anchor="ma")
        d.text((cx, y + 14), label, font=sans(8), fill=MUTE, anchor="ma")
    return y + 22


def draw_big_numbers(d, y):
    cols = len(BIG_NUMBERS)
    cw = (W - 20) / cols
    for i, (num, label) in enumerate(BIG_NUMBERS):
        x0 = 10 + i * cw
        cx = x0 + cw / 2
        if i:
            d.line([x0, y + 4, x0, y + 40], fill=RULE, width=1)
        d.text((cx, y + 12), num, font=serif(19, bold=True), fill=NAVY,
               anchor="ma")
        d.text((cx, y + 34), label, font=sans(8), fill=MUTE, anchor="ma")
    d.line([10, y + 42, W - 10, y + 42], fill=RULE, width=1)
    return y + 46


def draw_regions(d, y):
    parts, x = [], 10
    d.text((x, y + 9), "REGIONS", font=sans(9, bold=True), fill=NAVY,
           anchor="lm")
    x = 84
    total = sum(v for _, v in REGIONS)
    for name, v in REGIONS:
        t = "%s %d" % (name, v)
        d.text((x, y + 9), t, font=sans(10, bold=True), fill=INK, anchor="lm")
        x += d.textlength(t, font=sans(10, bold=True)) + 26
    d.text((W - 10, y + 9), "TOTAL %d" % total, font=sans(9, bold=True),
           fill=MUTE, anchor="rm")
    return y + 18


def draw_map(d, x, y, w, h):
    """World map: tan land on pale sea, pins 1-14 coloured to match numbers."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE)
    land = [
        (8, 60, 92, 128), (96, 34, 128, 62), (118, 66, 150, 108),
        (150, 30, 205, 66), (150, 68, 190, 112), (205, 26, 272, 74),
        (232, 78, 282, 108), (248, 140, 290, 168),
    ]
    for (lx, ly, rx, ry) in land:
        d.ellipse([x + lx, y + ly, x + rx, y + ry], fill=LAND)
    d.text((x + 8, y + 6), "THE WORLD", font=sans(9, bold=True), fill=NAVY,
           anchor="la")
    # (story, x, y) inside the map box; clusters spread by hand.
    pins = [
        (1, 158, 52), (2, 288, 176), (3, 52, 78), (4, 198, 100),
        (5, 240, 88), (6, 126, 40), (7, 168, 74), (8, 256, 112),
        (9, 140, 66), (10, 144, 30), (11, 210, 84), (12, 180, 132),
        (13, 186, 110), (14, 264, 68),
    ]
    for n, px, py in pins:
        pin(d, x + px, y + py, n, r=9)
    d.text((x + w // 2, y + h - 5),
           "Nos. 1\u201314 pictured \u2014 match the colour to the story number",
           font=sans(8), fill=NAVY, anchor="mb")

def draw_lead(d, x, y, w, lead):
    n = lead["n"]
    lead_art(d, n, x, y, w, 64)
    yy = y + 69
    cw = chip(d, x, yy, n, size=14)
    d.text((x + cw + 5, yy + 7),
           "%s \u00b7 %s" % (lead["city"], lead["tag"]),
           font=sans(9, bold=True), fill=NAVY, anchor="lm")
    yy += 16
    for line in wrap(d, lead["head"], serif(13, bold=True), w):
        d.text((x, yy), line, font=serif(13, bold=True), fill=INK, anchor="la")
        yy += 15
    for line in wrap(d, lead["body"], sans(10), w):
        d.text((x, yy), line, font=sans(10), fill=INK, anchor="la")
        yy += 12
    d.text((x, yy + 1), lead["src"], font=sans(8), fill=MUTE, anchor="la")
    return yy + 12


def draw_small(d, x, y, w, s):
    n = s["n"]
    thumb(d, n, x, y, w, 32)
    yy = y + 36
    cw = chip(d, x, yy, n, size=13)
    d.text((x + cw + 4, yy + 6),
           "%s \u00b7 %s" % (s["city"], s["tag"]),
           font=sans(8, bold=True), fill=NAVY, anchor="lm")
    yy += 14
    for line in wrap(d, s["head"], sans(11, bold=True), w)[:2]:
        d.text((x, yy), line, font=sans(11, bold=True), fill=INK, anchor="la")
        yy += 12
    for line in wrap(d, s["body"], sans(9), w)[:2]:
        d.text((x, yy), line, font=sans(9), fill=INK, anchor="la")
        yy += 11
    d.text((x, yy), "%s \u00b7 %s" % (s["tag2"], s["src"]),
           font=sans(8), fill=MUTE, anchor="la")
    return yy + 11


def draw_voices(d, y):
    d.text((10, y + 7), "VOICES OF THE DAY", font=sans(10, bold=True),
           fill=NAVY, anchor="la")
    d.line([10, y + 18, W - 10, y + 18], fill=RULE, width=1)
    yy = y + 22
    cols = len(VOICES)
    cw = (W - 20 - (cols - 1) * 12) / cols
    bottom = yy
    for i, (who, quote, attr) in enumerate(VOICES):
        x = 10 + i * (cw + 12)
        qy = yy
        for line in wrap(d, quote, serif(10), cw):
            d.text((x, qy), line, font=serif(10), fill=INK, anchor="la")
            qy += 13
        d.text((x, qy + 2), "\u2014 %s \u00b7 %s" % (who, attr),
               font=sans(8), fill=MUTE, anchor="la")
        bottom = max(bottom, qy + 14)
    return bottom + 4


def draw_briefs(d, x, y, w, h):
    """31 numbered briefs in two columns; coloured number chips, tinted rows."""
    d.text((x, y), "THE DAY IN BRIEF \u2014 31 STORIES",
           font=sans(10, bold=True), fill=NAVY, anchor="la")
    y0 = y + 14
    col_w = (w - 10) / 2
    row_h = 12
    for ci in range(2):
        cx = x + ci * (col_w + 10)
        items = BRIEFS[ci * 16:(ci + 1) * 16]
        for ri, text in enumerate(items):
            n = 15 + ci * 16 + ri
            ry = y0 + ri * row_h
            if ri % 2 == 0:
                d.rectangle([cx - 2, ry - 1, cx + col_w, ry + row_h - 1],
                            fill=ROW_TINT)
            chip(d, cx, ry, n, size=11)
            ink = INK if ri % 2 == 0 else NAVY2
            d.text((cx + 25, ry + 6), text, font=sans(9), fill=ink,
                   anchor="lm")
    return y0 + 16 * row_h + 2


def draw_chart_tags(d, y):
    d.text((10, y + 7), "THE DAY IN ONE CHART \u2014 THU 26 NOV CLOSES",
           font=sans(10, bold=True), fill=NAVY, anchor="la")
    d.text((W - 10, y + 7), "Asia and Europe rebound, led by chips. WSJ closes.",
           font=sans(9), fill=MUTE, anchor="ra")
    y += 20
    slots = (W - 20) / len(CHART)
    for i, (name, val) in enumerate(CHART):
        cx = 10 + slots * i + slots / 2
        v = float(val.strip("%"))
        bh = max(4, int(v * 8))
        d.rectangle([cx - 34, y + 20 - bh, cx + 34, y + 20],
                    fill=NAVY2)
        if bh >= 12:
            d.text((cx, y + 20 - bh + 2), val, font=sans(9, bold=True),
                   fill=(255, 255, 255), anchor="ma")
        else:
            d.text((cx, y + 20 - bh - 2), val, font=sans(9, bold=True),
                   fill=NAVY, anchor="mb")
        d.text((cx, y + 24), name, font=sans(9), fill=INK, anchor="ma")
    y += 34
    d.line([10, y, W - 10, y], fill=RULE, width=1)
    y += 3
    d.text((10, y + 6), "HOW TO READ THE TAGS", font=sans(9, bold=True),
           fill=NAVY, anchor="la")
    x = 172
    for tag, desc in TAGS:
        t = "%s %s" % (tag, desc)
        d.text((x, y + 6), t, font=sans(9), fill=INK, anchor="la")
        x += d.textlength(t, font=sans(9)) + 22
    return y + 15


def draw_watch(d, y):
    d.text((10, y + 5), "WHAT TO WATCH TOMORROW \u2014 SAT 28 NOV",
           font=sans(10, bold=True), fill=NAVY, anchor="la")
    d.text((10, y + 18), WATCH, font=sans(10), fill=INK, anchor="la")
    return y + 28


def draw_datecheck(d, y):
    d.rectangle([10, y, W - 10, y + 64], fill=PAPER_DARK, outline=RULE)
    d.text((18, y + 7), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
           font=sans(9, bold=True), fill=NAVY, anchor="la")
    d.text((W - 18, y + 7), "FIRST REPORTED BEFORE TODAY:",
           font=sans(9), fill=MUTE, anchor="ra")
    yy = y + 20
    for label, text in DATECHECK:
        line = label + text
        for ln in wrap(d, line, sans(9), W - 36):
            d.text((18, yy), ln, font=sans(9), fill=INK, anchor="la")
            yy += 11
    return y + 64


def draw_footer(d, y):
    d.text((W // 2, y + 4), FOOTER_SOURCES, font=sans(8), fill=MUTE,
           anchor="ma")
    d.text((W // 2, y + 13), FOOTER_NOTE, font=sans(8), fill=MUTE,
           anchor="ma")
    return y + 18

# -------------------------------------------------------------- render ---

def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 6
    y = draw_top_strip(d, y, 14)
    y = draw_masthead(d, y)
    y = draw_utc(d, y)
    y = draw_big_numbers(d, y)
    y = draw_regions(d, y)
    # 4 leads across.
    lw = (W - 20 - 3 * 8) / 4
    lead_bottom = y
    for i, lead in enumerate(LEADS):
        x = 10 + i * (lw + 8)
        lead_bottom = max(lead_bottom, draw_lead(d, x, y, lw, lead))
    y = lead_bottom + 4
    # 10 small stories: 2 rows of 5.
    sw = (W - 20 - 4 * 8) / 5
    for r in range(2):
        row_bottom = y
        for c in range(5):
            s = STORIES[r * 5 + c]
            x = 10 + c * (sw + 8)
            row_bottom = max(row_bottom, draw_small(d, x, y, sw, s))
        y = row_bottom + 4
    # Voices, then map + briefs side by side.
    y = draw_voices(d, y)
    map_h = 208
    draw_map(d, 10, y, 300, map_h)
    y2 = draw_briefs(d, 318, y, W - 10 - 318, map_h)
    y = max(y + map_h, y2) + 2
    y = draw_chart_tags(d, y)
    y = draw_watch(d, y)
    y = draw_datecheck(d, y)
    y = draw_footer(d, y)
    print("final y:", y)
    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    render("entry.png")
