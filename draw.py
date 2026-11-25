#!/usr/bin/env python3
"""Render the 24 Nov 2026 world-news broadsheet, 1024x1024."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24  # margin
PAPER = (248, 244, 236)
INK = (17, 17, 17)
GREY = (110, 108, 100)
RED = (178, 34, 34)
RULE = (150, 145, 130)
BAND = (238, 232, 218)
MAP_BG = (223, 233, 236)
LAND = (232, 223, 200)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"

REGION_COLOR = {
    "EUROPE": (31, 78, 121),
    "MIDDLE EAST": (183, 121, 31),
    "AFRICA": (46, 125, 50),
    "ASIA": (183, 28, 28),
    "OCEANIA": (0, 131, 143),
    "AMERICAS": (106, 27, 154),
    "WORLD": (97, 97, 97),
}

# (n, region, tag, status, headline, dek, source, glyph)
LEADS = [
    (1, "ASIA", "POLITICS", "OFFICIAL",
     "China opens probe into Shanghai party chief Chen Jining",
     "Politburo member investigated for 'serious violations', state media say; the fourth Politburo member probed in two years.",
     "CCTV via Al Jazeera", "politics"),
    (2, "AMERICAS", "COURTS", "CONFIRMED",
     "US jury finds Huawei guilty on 10 of 12 counts",
     "Brooklyn jury convicts on bank fraud and trade-secrets conspiracy; acquits on racketeering. Huawei will appeal.",
     "BBC, AP", "courts"),
    (3, "EUROPE", "WAR", "REPORTED",
     "Ukraine hits Russian ships off Libya; two Libyan soldiers die",
     "Tripoli demands answers from Kyiv; Moscow vows retaliation after the strike near Benghazi.",
     "OneTurn, Horizon", "war"),
    (4, "MIDDLE EAST", "CONFLICT", "CONFIRMED",
     "Houthi drone hits Riyadh tower; 11 injured",
     "Saudi civil defence says the King Abdullah Financial District tower was struck; two Indians among the hurt.",
     "Al Jazeera", "conflict"),
    (5, "EUROPE", "PHARMA", "OFFICIAL",
     "Sanofi to buy Insmed for $41bn",
     "French drugmaker pays $175 a share in cash; biggest pharma deal since 2023. Closes in H1 2027.",
     "Sanofi, Reuters", "pharma"),
    (6, "EUROPE", "HEALTH", "OFFICIAL",
     "England records 5,258 heat deaths in 2026",
     "May\u2013September toll is the highest since records began; old record 2,985 in 2022.",
     "UKHSA", "health"),
    (7, "WORLD", "SPACE", "OFFICIAL",
     "Ariane 6 lofts 36 Amazon satellites",
     "VA271 lifts off from Kourou at 11:14 UTC; tenth Ariane 6 flight, all successful.",
     "Xinhua, ESA", "space"),
    (8, "MIDDLE EAST", "WAR", "CONFIRMED",
     "Israeli strike kills Hamas security chief in Gaza City",
     "Naeem Abu Nahel dies with his wife and two daughters; strikes kill at least three in Gaza.",
     "Al Jazeera", "war"),
    (9, "ASIA", "DEFENCE", "REPORTED",
     "Russian jets spark Korea air raid alert",
     "Ulleungdo told to shelter at 07:52 local time after jets near the island.",
     "Korea Herald", "defence"),
    (10, "OCEANIA", "DIPLOMACY", "CONFIRMED",
     "Solomons to let China pact lapse",
     "Won't renew the 2022 security deal ending 2027; Australia signs a rival pact with Honiara.",
     "SMH, ABC", "diplomacy"),
    (11, "AFRICA", "SPORT", "CONFIRMED",
     "Court gives Senegal the AFCON title back",
     "CAS restores the 1\u20130 final win; champions again after the appeal.",
     "CNN", "sport"),
    (12, "MIDDLE EAST", "CONFLICT", "REPORTED",
     "Iran says two tankers hit mines in Hormuz",
     "Revolutionary Guards Navy says the tankers caught fire; Tehran refuses talks until seven conditions are met.",
     "IRGC Navy via OneTurn", "conflict"),
    (13, "AMERICAS", "TECH", "CONFIRMED",
     "Nvidia brings back Jensen Huang as CEO",
     "Trump says he persuaded the board; Seoul shares jump 6%, Nikkei up 3.9%.",
     "Horizon, Medium", "tech"),
]

# (n, region, headline, dek, source, status)
MORE = [
    (14, "EUROPE", "UK warns Ukraine suppliers of sabotage",
     "MoD and MI5 issue a rare public alert to defence firms.", "BBC", "CONFIRMED"),
    (15, "EUROPE", "Sarkozy ordered to stand trial for corruption",
     "Former French president to face trial from 1 April 2027.", "REPORTED", "REPORTED"),
    (16, "ASIA", "5.6 quake strikes Nepal near China border",
     "Tremor hits Koshi province.", "REPORTED", "REPORTED"),
    (17, "ASIA", "14 nations back ICJ ruling on Rohingya genocide",
     "UK, Spain, Canada, Australia and ten more recognise the Myanmar verdict.", "CONFIRMED", "CONFIRMED"),
    (18, "WORLD", "UN chief wants AI rules agreed within a year",
     "Guterres calls for a multilateral framework to limit AI risks.", "CONFIRMED", "CONFIRMED"),
    (19, "AMERICAS", "Measles death toll rises across the US",
     "Pennsylvania records a ninth death; national tally nears 6,000 cases.", "CONFIRMED", "CONFIRMED"),
    (20, "ASIA", "Malaysia to send 6,500 Rohingya back to Myanmar",
     "Returns planned for December; UN urges a halt.", "REPORTED", "REPORTED"),
    (21, "MIDDLE EAST", "Coalition strike on Hodeidah port kills 11",
     "Saudi-led jets hit the Yemeni port after the Riyadh attack.", "REPORTED", "REPORTED"),
    (22, "MIDDLE EAST", "Houthis say dozens die in Saudi airstrikes",
     "Yemen's Houthis report heavy casualties in the latest raids.", "REPORTED", "REPORTED"),
    (23, "AFRICA", "Amnesty urges Ethiopia war-crimes probe",
     "Rights group calls for an inquiry into the Alamata killings.", "REPORTED", "REPORTED"),
    (24, "EUROPE", "Turkish helicopter crash kills five crew",
     "Air force helicopter goes down in training over Eskisehir.", "AP", "CONFIRMED"),
    (25, "MIDDLE EAST", "Bus hits truck in Ras Al Khaimah; 13 dead",
     "14 more injured in the UAE crash, police say.", "Gulf News", "CONFIRMED"),
    (26, "ASIA", "Hanoi hotpot blast kills seven",
     "Cooking-gas explosion wrecks a restaurant; nine injured.", "VnExpress", "CONFIRMED"),
    (27, "AFRICA", "Borno school enrolment nearly doubles",
     "Pupils return in north-east Nigeria despite years of conflict.", "Al Jazeera", "CONFIRMED"),
    (28, "ASIA", "Pakistan's Zeeshan Ali joins China's space station",
     "First foreign astronaut on Tiangong flies on Shenzhou-24.", "Straits Times", "CONFIRMED"),
    (29, "AMERICAS", "DOJ recovers $8bn in biggest anti-scam sweep",
     "More than 800 suspects charged in the fraud crackdown.", "Fox News", "CONFIRMED"),
    (30, "AMERICAS", "CIA unclassified system breached",
     "US media report a hack exposed unclassified material.", "REPORTED", "REPORTED"),
    (31, "OCEANIA", "Australia apologises to LGBTQ veterans",
     "Canberra formally says sorry for past treatment of gay service members.", "REPORTED", "REPORTED"),
    (32, "AMERICAS", "Abrego Garcia leaves US for Spain",
     "Salvadoran at the centre of the ICE fight departs.", "Independent", "CONFIRMED"),
    (33, "AMERICAS", "Democrats clinch historic House majority",
     "At least 259 seats, the largest since 1990.", "REPORTED", "REPORTED"),
    (34, "EUROPE", "Spain heads for snap election",
     "Housing and the far right dominate the campaign.", "REPORTED", "REPORTED"),
    (35, "MIDDLE EAST", "Eisenkot secures first coalition partner",
     "Israel's UTJ to seek rabbis' approval to open talks.", "Times of Israel", "CONFIRMED"),
    (36, "ASIA", "Korea minister quits after exam AI scandal",
     "Education chief resigns over cheating in the suneung entrance test.", "REPORTED", "REPORTED"),
    (37, "EUROPE", "Merz: Russia wants more than Ukraine",
     "German chancellor defends Kyiv aid; Ukraine seeks 115bn euros for 2027.", "REPORTED", "REPORTED"),
    (38, "AFRICA", "Libya demands answers over ship attack",
     "Tripoli presses Kyiv after the strike on Russian vessels off Benghazi.", "REPORTED", "REPORTED"),
]

CHIPS = [("Europe", 8), ("Middle East", 7), ("Africa", 4), ("Asia", 8),
         ("Oceania", 2), ("Americas", 7), ("World", 2)]

NUMBERS = [
    ("10 of 12", "Huawei guilty counts"),
    ("$41bn", "Sanofi buys Insmed"),
    ("5,258", "England heat deaths, record"),
    ("36", "Ariane 6 satellites"),
    ("13", "killed in UAE bus crash"),
    ("11", "injured in Riyadh drone attack"),
]

TIMELINE = [
    ("05:30", "Sanofi\u2013Insmed deal announced"),
    ("11:14", "Ariane 6 lifts off"),
    ("16:29", "DOJ $8bn scam sweep"),
    ("16:48", "UK sabotage warning"),
    ("21:32", "Huawei verdict"),
    ("21:33", "Houthi strike on Riyadh tower"),
]

# map pins: (lead n, fx, fy) fractions of map panel
PINS = [
    (1, 0.78, 0.34), (2, 0.11, 0.27), (3, 0.50, 0.47), (4, 0.585, 0.53),
    (5, 0.455, 0.30), (6, 0.44, 0.22), (7, 0.22, 0.62), (8, 0.545, 0.39),
    (9, 0.83, 0.34), (10, 0.90, 0.66), (11, 0.44, 0.60), (12, 0.635, 0.46),
    (13, 0.17, 0.48),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_glyph(d, x, y, s, kind, color):
    """Original geometric pictogram inside a s x s box at (x, y)."""
    d.rectangle([x, y, x + s, y + s], fill=color)
    w = (255, 255, 255)
    c = s // 2
    if kind == "politics":  # capitol: roof + columns
        d.polygon([(x + 3, y + s // 2), (x + c, y + 4), (x + s - 3, y + s // 2)], fill=w)
        for i in range(3):
            bx = x + 5 + i * (s - 10) // 2
            d.rectangle([bx, y + s // 2 + 2, bx + 3, y + s - 4], fill=w)
        d.rectangle([x + 3, y + s - 4, x + s - 3, y + s - 2], fill=w)
    elif kind == "courts":  # scales: beam + two pans
        d.rectangle([x + c - 1, y + 4, x + c + 1, y + s - 6], fill=w)
        d.rectangle([x + 4, y + 6, x + s - 4, y + 8], fill=w)
        d.polygon([(x + 4, y + 13), (x + 9, y + 13), (x + 6, y + 9)], outline=w)
        d.polygon([(x + s - 9, y + 13), (x + s - 4, y + 13), (x + s - 7, y + 9)], outline=w)
        d.rectangle([x + 4, y + s - 5, x + s - 4, y + s - 3], fill=w)
    elif kind == "war":  # burst star
        pts = []
        for i in range(16):
            r = s // 2 - 2 if i % 2 == 0 else s // 4
            import math
            a = math.pi * i / 8
            pts.append((x + c + r * math.cos(a), y + c + r * math.sin(a)))
        d.polygon(pts, fill=w)
        d.ellipse([x + c - 3, y + c - 3, x + c + 3, y + c + 3], fill=color)
    elif kind == "conflict":  # target rings
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=w, width=2)
        d.ellipse([x + 8, y + 8, x + s - 8, y + s - 8], outline=w, width=2)
        d.ellipse([x + c - 2, y + c - 2, x + c + 2, y + c + 2], fill=w)
    elif kind == "pharma":  # cross
        d.rectangle([x + c - 3, y + 4, x + c + 3, y + s - 4], fill=w)
        d.rectangle([x + 4, y + c - 3, x + s - 4, y + c + 3], fill=w)
    elif kind == "health":  # cross in ring
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=w, width=2)
        d.rectangle([x + c - 2, y + 8, x + c + 2, y + s - 8], fill=w)
        d.rectangle([x + 8, y + c - 2, x + s - 8, y + c + 2], fill=w)
    elif kind == "space":  # rocket
        d.polygon([(x + c, y + 3), (x + c + 5, y + 13), (x + c - 5, y + 13)], fill=w)
        d.rectangle([x + c - 4, y + 13, x + c + 4, y + s - 7], fill=w)
        d.ellipse([x + c - 2, y + 15, x + c + 2, y + 19], fill=color)
        d.polygon([(x + c - 4, y + s - 7), (x + c - 8, y + s - 3), (x + c - 1, y + s - 3)], fill=w)
        d.polygon([(x + c + 4, y + s - 7), (x + c + 8, y + s - 3), (x + c + 1, y + s - 3)], fill=w)
    elif kind == "defence":  # shield
        d.polygon([(x + 4, y + 4), (x + s - 4, y + 4), (x + s - 4, y + s // 2),
                   (x + c, y + s - 3), (x + 4, y + s // 2)], outline=w, width=2)
        d.rectangle([x + c - 1, y + 8, x + c + 1, y + s - 8], fill=w)
    elif kind == "diplomacy":  # linked rings
        d.ellipse([x + 3, y + 7, x + s // 2 + 3, y + s - 7], outline=w, width=2)
        d.ellipse([x + s // 2 - 3, y + 7, x + s - 3, y + s - 7], outline=w, width=2)
    elif kind == "sport":  # ball
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=w, width=2)
        d.polygon([(x + c, y + 9), (x + c + 4, y + 13), (x + c + 2, y + 18),
                   (x + c - 2, y + 18), (x + c - 4, y + 13)], fill=w)
        d.line([x + 5, y + c, x + s - 5, y + c], fill=w, width=1)
    else:  # tech: chip
        d.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], outline=w, width=2)
        d.rectangle([x + 9, y + 9, x + s - 9, y + s - 9], fill=w)
        for px in (x + 9, x + c - 1, x + s - 11):
            d.line([px, y + 2, px, y + 6], fill=w, width=2)
            d.line([px, y + s - 6, px, y + s - 2], fill=w, width=2)


def draw_masthead(d):
    f_small = font(SANS_B, 12)
    f_date = font(SERIF_B, 44)
    f_counts = font(SANS, 12)
    f_sub = font(SERIF, 15)
    d.text((W // 2, 12), "ONE DAY \u00b7 ONE PAGE \u00b7 THE WORLD",
           font=f_small, fill=GREY, anchor="ma")
    d.text((W // 2, 26), "24 NOVEMBER 2026", font=f_date, fill=INK, anchor="ma")
    d.text((W // 2, 74), "38 STORIES  \u00b7  7 REGIONS  \u00b7  13 LEADS  \u00b7  TUESDAY",
           font=f_counts, fill=INK, anchor="ma")
    d.line([M, 92, W - M, 92], fill=RED, width=3)
    d.text((W // 2, 98),
           "China probes Shanghai party chief \u00b7 US jury finds Huawei guilty \u00b7 Russian attacks hit ships off Libya",
           font=f_sub, fill=INK, anchor="ma")
    d.line([M, 120, W - M, 120], fill=RULE, width=1)


def draw_chips(d, y):
    f = font(SANS_B, 12)
    total = W - 2 * M
    cw = total // len(CHIPS)
    for i, (name, cnt) in enumerate(CHIPS):
        x = M + i * cw
        color = REGION_COLOR[name.upper()]
        d.ellipse([x + 6, y + 4, x + 16, y + 14], fill=color)
        d.text((x + 20, y + 2), "%s %d" % (name, cnt), font=f, fill=INK)
    d.line([M, y + 24, W - M, y + 24], fill=RULE, width=1)


def draw_timeline(d, y):
    f_h = font(SANS_B, 11)
    f_t = font(SANS_B, 11)
    f_x = font(SANS, 10)
    d.text((M, y), "THE DAY IN UTC", font=f_h, fill=RED)
    d.line([M, y + 16, W - M, y + 16], fill=RULE, width=1)
    colw = (W - 2 * M) // len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        x = M + i * colw + 2
        d.ellipse([x, y + 24, x + 7, y + 31], fill=RED)
        d.text((x + 11, y + 20), t, font=f_t, fill=INK)
        lines = wrap(txt, f_x, colw - 6)
        text_lines(d, x, y + 36, lines[:2], f_x, INK, 12)
    d.line([M, y + 62, W - M, y + 62], fill=RULE, width=1)


def draw_numbers(d, y):
    f_h = font(SANS_B, 11)
    f_n = font(SERIF_B, 22)
    f_l = font(SANS, 10)
    d.text((M, y), "IN NUMBERS", font=f_h, fill=RED)
    d.line([M, y + 16, W - M, y + 16], fill=RULE, width=1)
    colw = (W - 2 * M) // len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * colw
        d.text((x, y + 20), num, font=f_n, fill=INK)
        lines = wrap(lab, f_l, colw - 8)
        text_lines(d, x, y + 48, lines[:2], f_l, GREY, 11)
    d.line([M, y + 70, W - M, y + 70], fill=RULE, width=1)


def fit_lines(text, fnt, max_w, max_lines, leading):
    """Wrap text to at most max_lines, trimming the last line with an ellipsis."""
    lines = wrap(text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and fnt.getlength(lines[-1] + "\u2026") > max_w:
        words = lines[-1].split()
        if len(words) <= 1:
            lines[-1] = ""
            break
        lines[-1] = " ".join(words[:-1])
    if lines:
        lines[-1] = (lines[-1] + "\u2026").strip()
    return lines


def draw_leads(d, y0):
    f_tag = font(SANS_B, 10)
    f_stat = font(SANS_B, 8)
    f_head = font(SANS_B, 12)
    f_dek = font(SANS, 9)
    f_src = font(SANS, 8)
    card_w, card_h, gap = 320, 88, 2
    for idx, (n, region, tag, status, head, dek, src, glyph) in enumerate(LEADS):
        r, c = divmod(idx, 3)
        x = M + c * (card_w + 8)
        y = y0 + r * (card_h + gap)
        color = REGION_COLOR[region]
        d.rectangle([x, y, x + card_w, y + card_h], fill=(255, 255, 255),
                    outline=(210, 205, 190), width=1)
        draw_glyph(d, x + 3, y + 3, 22, glyph, color)
        d.text((x + 29, y + 5), "%d \u00b7 %s \u2014 %s" % (n, region, tag),
               font=f_tag, fill=color)
        d.text((x + card_w - 4, y + 6), status, font=f_stat, fill=GREY, anchor="ra")
        hl = fit_lines(head, f_head, card_w - 6, 2, 14)
        text_lines(d, x + 3, y + 28, hl, f_head, INK, 14)
        dl = fit_lines(dek, f_dek, card_w - 6, 2, 11)
        text_lines(d, x + 3, y + 57, dl, f_dek, INK, 11)
        d.text((x + 3, y + 79), src, font=f_src, fill=GREY)


def draw_list(d, y0):
    f_h = font(SANS_B, 11)
    f_b = font(SANS_B, 9)
    f_r = font(SANS, 9)
    d.text((M, y0), "ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE",
           font=f_h, fill=RED)
    d.line([M, y0 + 15, W - M, y0 + 15], fill=RULE, width=1)
    col_w = (W - 2 * M - 16) // 2
    row_h = 13
    for i, (n, region, head, dek, src, status) in enumerate(MORE):
        col = 0 if i < 13 else 1
        row = i if i < 13 else i - 13
        x = M + col * (col_w + 16)
        y = y0 + 19 + row * row_h
        dot = (46, 125, 50) if status == "CONFIRMED" else (183, 121, 31)
        d.ellipse([x, y + 2, x + 6, y + 8], fill=dot)
        tx = x + 9
        prefix = "%d. %s \u2014 " % (n, head)
        suffix = " \u00b7 " + src
        avail = col_w - 9 - f_b.getlength(prefix) - f_r.getlength(suffix)
        words = dek.split()
        dtext = dek
        while words and f_r.getlength(dtext) > avail:
            words = words[:-1]
            dtext = " ".join(words) + "\u2026"
        d.text((tx, y), prefix, font=f_b, fill=INK)
        px = tx + f_b.getlength(prefix)
        d.text((px, y), dtext, font=f_r, fill=INK)
        d.text((px + f_r.getlength(dtext), y), suffix, font=f_r, fill=GREY)


def draw_map(d, y0, h):
    f_t = font(SANS_B, 10)
    f_n = font(SANS_B, 8)
    d.rectangle([M, y0, W - M, y0 + h], fill=MAP_BG, outline=RULE, width=1)
    d.text((M + 6, y0 + 3), "WHERE IT HAPPENED \u2014 PINS 1\u201313",
           font=f_t, fill=INK)
    d.text((W - M - 6, y0 + 4), "PINS COLOURED BY REGION (SEE CHIPS ABOVE)",
           font=f_n, fill=GREY, anchor="ra")
    pw, ph = W - 2 * M, h
    blobs = [
        [(0.05, 0.30), (0.10, 0.22), (0.18, 0.24), (0.24, 0.30), (0.26, 0.40),
         (0.20, 0.44), (0.14, 0.50), (0.08, 0.46), (0.05, 0.38)],
        [(0.20, 0.52), (0.26, 0.52), (0.30, 0.60), (0.28, 0.78), (0.24, 0.88),
         (0.21, 0.72), (0.19, 0.60)],
        [(0.43, 0.24), (0.48, 0.22), (0.51, 0.28), (0.49, 0.36), (0.45, 0.34),
         (0.43, 0.30)],
        [(0.46, 0.40), (0.52, 0.38), (0.55, 0.46), (0.54, 0.58), (0.50, 0.68),
         (0.47, 0.58), (0.45, 0.48)],
        [(0.55, 0.24), (0.66, 0.18), (0.78, 0.20), (0.88, 0.28), (0.86, 0.42),
         (0.80, 0.50), (0.68, 0.52), (0.60, 0.44), (0.56, 0.34)],
        [(0.84, 0.62), (0.90, 0.60), (0.93, 0.68), (0.90, 0.76), (0.85, 0.74),
         (0.83, 0.68)],
    ]
    for blob in blobs:
        pts = [(M + fx * pw, y0 + 12 + fy * (ph - 14)) for fx, fy in blob]
        d.polygon(pts, fill=LAND, outline=(200, 190, 165))
    for n, fx, fy in PINS:
        region = LEADS[n - 1][1]
        color = REGION_COLOR[region]
        cx = M + fx * pw
        cy = y0 + 12 + fy * (ph - 14)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 5), str(n), font=f_n, fill=(255, 255, 255), anchor="ma")


def draw_footer(d, y):
    f_c = font(SANS, 10)
    f_b = font(SANS_B, 11)
    d.text((W // 2, y), "DATE CHECK \u2014 Left off as earlier news: ULA Vulcan lost 40 Amazon satellites, 15 Nov \u00b7 Ariane 6 delay announced 23 Nov.  Not yet: Huawei sentencing, Sept 2027 \u00b7 Sanofi\u2013Insmed close, H1 2027.",
           font=f_c, fill=GREY, anchor="ma")
    d.text((W // 2, y + 14),
           "Every story happened or was first reported on Tuesday 24 Nov 2026 (UTC) \u00b7 sources named on each item \u00b7 original drawings, no photos",
           font=f_b, fill=INK, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_chips(d, 124)
    draw_timeline(d, 152)
    draw_numbers(d, 214)
    draw_leads(d, 290)
    draw_list(d, 744)
    draw_map(d, 933, 62)
    draw_footer(d, 995)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
