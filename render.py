#!/usr/bin/env python3
"""Render a 1024x1024 newspaper front page for Tuesday 17 November 2026.
Deterministic; no network. Lead illustrations come from assets/ni1117/leadN.png
(Muse/fal.ai) when present, else original schematic fallbacks drawn here.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 241, 230)
INK = (24, 22, 20)
SOFT = (70, 66, 60)
RED = (179, 64, 42)
BLUE = (42, 91, 140)
RULE = (40, 38, 34)
CREAM_DARK = (232, 226, 210)

FD = "/usr/share/fonts/truetype"
def F(name, size):
    paths = {
        "serifb": f"{FD}/dejavu/DejaVuSerif-Bold.ttf",
        "serif": f"{FD}/dejavu/DejaVuSerif.ttf",
        "lserifb": f"{FD}/liberation/LiberationSerif-Bold.ttf",
        "lserif": f"{FD}/liberation/LiberationSerif-Regular.ttf",
        "lserifi": f"{FD}/liberation/LiberationSerif-Italic.ttf",
        "sans": f"{FD}/liberation/LiberationSans-Regular.ttf",
        "sansb": f"{FD}/liberation/LiberationSans-Bold.ttf",
        "sansi": f"{FD}/liberation/LiberationSans-Italic.ttf",
    }
    return ImageFont.truetype(paths[name], size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(s, f):
    b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]

def wrap(s, f, maxw):
    words = s.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def center(s, f, y, fill=INK):
    d.text(((W - tw(s, f)) / 2, y), s, font=f, fill=fill)

def hline(y, x0=36, x1=W-36, fill=RULE, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

# ---------- masthead ----------
hline(12, w=3); hline(17, w=1)
d.text((36, 24), "THE DAILY WORLD", font=F("lserifb", 22), fill=INK)
d.text((36, 50), "FRONT PAGE  ·  WORLD NEWS", font=F("sansb", 12), fill=SOFT)
right = "TUESDAY EDITION  ·  No. 317"
d.text((W-36-tw(right, F("sansb", 12)), 28), right, font=F("sansb", 12), fill=SOFT)
right2 = "ONE IMAGE  ·  ONE DAY"
d.text((W-36-tw(right2, F("sansi", 12)), 46), right2, font=F("sansi", 12), fill=SOFT)
hline(68, w=1)

# ---------- giant date ----------
center("TUESDAY", F("lserifb", 34), 76, INK)
center("17 NOVEMBER 2026", F("lserifb", 62), 112, INK)
hline(186, w=2)

# ---------- strip ----------
d.rectangle([36, 192, W-36, 216], fill=INK)
strip = "18 STORIES   ·   6 CONTINENTS   ·   EVERY ITEM FROM TUESDAY 17 NOVEMBER"
center(strip, F("sansb", 14), 197, PAPER)

# ---------- stories data ----------
LEADS = [
    ("01", "EUROPE / ASIA", "Kerch bridge struck again; road span falls into the sea",
     "A second day of attacks on the Crimea link. A road span collapsed into the strait; traffic halted. Kyiv and Moscow trade blame.", (36.5, 45.3)),
    ("02", "ASIA", "Iran drones target US radar; tanker mined in Hormuz",
     "Tehran flew drones at a US radar site in Bahrain; Washington struck Qeshm. A tanker hit a mine in the strait. Oil shipping on edge.", (56.0, 26.5)),
    ("03", "ASIA", "Trump's first Quad summit in Manila seals minerals pact",
     "The US, Japan, India and Australia met in Manila. A critical-minerals agreement headline a summit aimed at supply-chain leverage.", (121.0, 14.6)),
]
LIST = [
    ("04", "N. AMERICA", "Nvidia posts $115.8B quarter; Dow drops 849", (-74.0, 40.7)),
    ("05", "ASIA", "COP31 Antalya: draft text calls fossil-fuel phase-out", (30.7, 36.9)),
    ("06", "AMERICAS", "US, Mexico and Bolivia lose measles-free status", (-65.0, -17.0)),
    ("07", "AFRICA", "DR Congo Ebola response strained, WHO says", (23.0, -3.0)),
    ("08", "ASIA", "Mongolia's president announces resignation", (106.9, 47.9)),
    ("09", "EUROPE", "Serbia's students take seats in parliament", (20.5, 44.8)),
    ("10", "ASIA", "Bangladesh garment-wage clashes spread", (90.4, 23.8)),
    ("11", "AFRICA", "Mozambique: Mondlane tried on 5 charges", (32.6, -25.9)),
    ("12", "ASIA", "Russian An-12 crashes in Siberia; 19 dead", (100.0, 60.0)),
    ("13", "ASIA", "Japan scrambles jets over airspace breach", (140.0, 40.0)),
    ("14", "EUROPE", "Moldova closes its airspace", (28.8, 47.0)),
    ("15", "OCEANIA", "Cyclone Akvan tracked across the Pacific", (160.0, -15.0)),
    ("16", "SPACE", "Voyager 1 nears one light-day from Earth", None),
    ("17", "ASIA", "Gaza ceasefire under strain", (34.4, 31.5)),
    ("18", "AFRICA", "UN: 2,230 civilian deaths in Sudan", (30.0, 15.0)),
]

# ---------- lead illustrations ----------
ASSET = os.path.join(os.path.dirname(__file__), "assets", "ni1117")
def lead_image(i, w, h):
    p = os.path.join(ASSET, f"lead{i+1}.png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        # trim the fal.ai cream margin so the drawing itself fills the box
        from PIL import ImageChops
        bg = Image.new("RGB", im.size, PAPER)
        bbox = ImageChops.difference(im, bg).getbbox()
        if bbox:
            pad = 8
            bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad),
                    min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
            im = im.crop(bbox)
        im.thumbnail((w, h), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (w, h), PAPER)
        canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
        return canvas
    return fallback_lead(i, w, h)

def fallback_lead(i, w, h):
    im = Image.new("RGB", (w, h), CREAM_DARK); dd = ImageDraw.Draw(im)
    if i == 0:  # Kerch bridge
        dd.rectangle([0, h*0.62, w, h], fill=(150, 175, 190))  # sea
        dd.line([(0, h*0.5), (w, h*0.5)], fill=INK, width=5)  # deck
        for x in range(20, w, 46):
            dd.line([(x, h*0.5), (x, h*0.72)], fill=INK, width=3)
        # broken span
        dd.line([(w*0.45, h*0.5), (w*0.52, h*0.66)], fill=RED, width=5)
        dd.line([(w*0.58, h*0.5), (w*0.52, h*0.66)], fill=RED, width=5)
        dd.ellipse([w*0.47, h*0.36, w*0.57, h*0.46], outline=RED, width=3)
    elif i == 1:  # Hormuz
        dd.rectangle([0, h*0.66, w, h], fill=(150, 175, 190))
        dd.polygon([(w*0.2, h*0.66), (w*0.5, h*0.66), (w*0.44, h*0.56), (w*0.26, h*0.56)], fill=INK)  # tanker
        dd.rectangle([w*0.3, h*0.5, w*0.36, h*0.56], fill=INK)
        dd.polygon([(w*0.68, h*0.3), (w*0.8, h*0.34), (w*0.68, h*0.38)], fill=RED)  # drone
        dd.line([(w*0.8, h*0.34), (w*0.9, h*0.5)], fill=SOFT, width=2)
        dd.arc([w*0.84, h*0.44, w*0.98, h*0.6], 200, 340, fill=BLUE, width=3)  # radar
        dd.ellipse([w*0.55, h*0.74, w*0.6, h*0.79], outline=RED, width=2)  # mine
    else:  # Quad summit
        dd.rectangle([w*0.15, h*0.62, w*0.85, h*0.72], fill=INK)  # podium
        for k, fx in enumerate([0.25, 0.42, 0.58, 0.75]):
            dd.rectangle([w*fx, h*0.34, w*fx+16, h*0.46], fill=[BLUE, RED, SOFT, BLUE][k])
            dd.line([(w*fx, h*0.34), (w*fx, h*0.62)], fill=INK, width=2)
        dd.polygon([(w*0.46, h*0.8), (w*0.54, h*0.8), (w*0.5, h*0.9)], fill=RED)  # mineral
    return im

# ---------- three lead columns ----------
colw = 312; gap = 14; x0 = 36; ytop = 226
for i, (num, cont, head, body, _) in enumerate(LEADS):
    x = x0 + i * (colw + gap)
    im = lead_image(i, colw, 150)
    img.paste(im, (x, ytop))
    d.rectangle([x, ytop, x+colw, ytop+150], outline=RULE, width=1)
    yy = ytop + 156
    d.text((x, yy), f"STORY {num}  ·  {cont}", font=F("sansb", 11), fill=RED); yy += 16
    hf = F("lserifb", 18)
    for ln in wrap(head, hf, colw)[:3]:
        d.text((x, yy), ln, font=hf, fill=INK); yy += 21
    yy += 2
    bf = F("lserif", 13)
    for ln in wrap(body, bf, colw)[:4]:
        d.text((x, yy), ln, font=bf, fill=SOFT); yy += 16
    if i < 2:
        d.line([(x+colw+gap//2, ytop), (x+colw+gap//2, ytop+230)], fill=RULE, width=1)

# ---------- world map ----------
my = 486
d.text((36, my), "WHERE IT HAPPENED", font=F("sansb", 15), fill=INK)
d.text((W-36-tw("17 LOCATIONS  ·  ORIGINAL DRAWING", F("sansi", 11)), my+2),
       "17 LOCATIONS  ·  ORIGINAL DRAWING", font=F("sansi", 11), fill=SOFT)
hline(my+20, w=1)
MAPX0, MAPX1 = 40, 984; MAPY0, MAPY1 = my+26, my+186
def proj(lon, lat):
    x = MAPX0 + (lon + 180) / 360 * (MAPX1 - MAPX0)
    y = MAPY0 + (78 - lat) / 140 * (MAPY1 - MAPY0)
    return x, y
# sea background for land/sea contrast
d.rectangle([MAPX0, MAPY0, MAPX1, MAPY1], fill=(222, 230, 233))
# graticule
for lon in range(-150, 181, 30):
    x, _ = proj(lon, 0); d.line([(x, MAPY0), (x, MAPY1)], fill=CREAM_DARK, width=1)
for lat in range(-60, 79, 30):
    _, y = proj(0, lat); d.line([(MAPX0, y), (MAPX1, y)], fill=CREAM_DARK, width=1)
# simplified continents (lon,lat polygons) — original schematic
CONT = {
 "NA": [(-168,66),(-140,70),(-120,72),(-90,72),(-70,62),(-55,50),(-65,44),(-75,38),(-81,31),(-97,26),(-105,20),(-95,16),(-83,9),(-100,18),(-117,33),(-125,42),(-130,55),(-152,60),(-168,66)],
 "SA": [(-80,9),(-62,10),(-50,0),(-35,-8),(-40,-20),(-58,-35),(-70,-52),(-72,-40),(-70,-18),(-78,-2),(-80,9)],
 "EU": [(-10,36),(-9,43),(-2,48),(-5,58),(5,62),(15,68),(30,70),(40,66),(45,55),(40,48),(28,41),(20,40),(10,38),(0,36),(-10,36)],
 "AF": [(-17,15),(-10,32),(0,36),(10,37),(20,32),(32,31),(43,12),(51,11),(40,-5),(35,-20),(20,-35),(15,-30),(12,-18),(8,4),(-8,5),(-17,15)],
 "AS": [(40,66),(60,70),(90,75),(120,72),(150,66),(170,64),(160,58),(142,50),(130,42),(122,30),(108,20),(100,8),(95,16),(88,22),(80,8),(72,20),(60,25),(48,30),(40,48),(45,55),(40,66)],
 "AU": [(114,-22),(122,-18),(132,-12),(142,-11),(146,-18),(152,-25),(150,-35),(140,-38),(130,-32),(116,-34),(114,-22)],
 "GL": [(-45,60),(-25,70),(-20,78),(-40,82),(-58,76),(-52,66),(-45,60)],
}
for name, poly in CONT.items():
    pts = [proj(lo, la) for lo, la in poly]
    d.polygon(pts, fill=(206, 196, 172), outline=(90, 84, 72))
# pins (with leader lines when crowded)
allstories = [(n, c, pin) for n, c, _, _, pin in LEADS] + [(n, c, pin) for n, c, _, pin in LIST]
placed = []
nf = F("sansb", 9)
for num, cont, pin in allstories:
    if pin is None: continue
    x, y = proj(*pin)
    bx, by = x, y
    # nudge badge away from already-placed badges
    for _ in range(24):
        if all(math.hypot(bx-px, by-py) >= 17 for px, py in placed): break
        best = None
        for ang in range(0, 360, 30):
            nx = x + 20 * math.cos(math.radians(ang)); ny = y + 20 * math.sin(math.radians(ang))
            if not (MAPX0+8 <= nx <= MAPX1-8 and MAPY0+8 <= ny <= MAPY1-8): continue
            score = min((math.hypot(nx-px, ny-py) for px, py in placed), default=999)
            if best is None or score > best[0]: best = (score, nx, ny)
        if best is None: break
        bx, by = best[1], best[2]
    placed.append((bx, by))
    d.ellipse([x-2, y-2, x+2, y+2], fill=INK)
    if math.hypot(bx-x, by-y) > 3:
        d.line([(x, y), (bx, by)], fill=SOFT, width=1)
    d.ellipse([bx-8, by-8, bx+8, by+8], fill=RED, outline=PAPER, width=1)
    d.text((bx-tw(num, nf)/2, by-5), num, font=nf, fill=PAPER)
d.rectangle([MAPX0, MAPY0, MAPX1, MAPY1], outline=RULE, width=1)

# ---------- also-on list ----------
ly = MAPY1 + 12
d.text((36, ly), "ALSO ON TUESDAY", font=F("sansb", 15), fill=INK)
hline(ly+20, w=1)
ly += 26
cols = 3; per = 5; cw = (W - 72 - 2*16) // cols
lf = F("lserifb", 13); cf = F("sansb", 10)
for idx, (num, cont, head, pin) in enumerate(LIST):
    c = idx // per; r = idx % per
    x = 36 + c * (cw + 16); y = ly + r * 30
    d.text((x, y), num, font=F("sansb", 13), fill=RED)
    d.text((x+24, y-1), cont, font=cf, fill=SOFT)
    for j, ln in enumerate(wrap(head, lf, cw-24)[:1]):
        d.text((x+24, y+11), ln, font=lf, fill=INK)

# ---------- footer ----------
fy = 884
hline(fy, w=2)
d.text((36, fy+6), "DATE CHECK", font=F("sansb", 12), fill=RED)
dc = "Every story happened or was first reported on Tuesday 17 November 2026. Excluded as other dates: the Ebola 11,000-case milestone (10 Nov) and the Vulcan launch (15 Nov). Contested claims are attributed."
for j, ln in enumerate(wrap(dc, F("lserifi", 12), W-72)):
    d.text((36, fy+22+j*15), ln, font=F("lserifi", 12), fill=SOFT)
have_assets = all(os.path.exists(os.path.join(ASSET, f"lead{i+1}.png")) for i in range(3))
illus = "Illustrations: fal.ai (Muse)" if have_assets else "Illustrations: original drawings"
src = "Sources: Reuters · AP · AFP · BBC · Al Jazeera · WHO · UN   |   " + illus + "   |   Compiled by Hermes"
center(src, F("sans", 11), fy+70, SOFT)
hline(fy+88, w=1)

out = os.path.join(os.path.dirname(__file__), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes", img.size)
