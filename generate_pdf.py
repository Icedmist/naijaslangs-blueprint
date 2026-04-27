from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import os

# Register fonts - Updated paths for this environment
pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold', '/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Bold', '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Mono-Bold', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Bold.ttf'))

W, H = A4

# ── Color palette ──────────────────────────────────────────────────────────────
G_DARKEST  = HexColor('#0A1F0D')   # near-black forest
G_DARK     = HexColor('#1A3320')   # deep forest
G_MID      = HexColor('#2D6A4F')   # rich forest
G_ACCENT   = HexColor('#52B788')   # vivid mint
G_LIGHT    = HexColor('#95D5B2')   # pale mint
G_LIGHTEST = HexColor('#D8F3DC')   # near-white mint
G_NEON     = HexColor('#74C69D')   # electric accent
GOLD       = HexColor('#F4A261')   # warm contrast
WHITE      = HexColor('#F0FFF4')
INK        = HexColor('#0D1B0F')

def hexagon(c, cx, cy, r, fill=None, stroke=None, lw=1):
    pts = [(cx + r*math.cos(math.radians(60*i-30)),
            cy + r*math.sin(math.radians(60*i-30))) for i in range(6)]
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    p.close()
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(lw)
    if fill and stroke: c.drawPath(p, fill=1, stroke=1)
    elif fill: c.drawPath(p, fill=1, stroke=0)
    else: c.drawPath(p, fill=0, stroke=1)

def draw_grid_bg(c, alpha_color=None):
    c.setStrokeColor(HexColor('#1E3D25'))
    c.setLineWidth(0.3)
    step = 18
    for x in range(0, int(W)+step, step):
        c.line(x, 0, x, H)
    for y in range(0, int(H)+step, step):
        c.line(0, y, W, y)

def draw_hex_pattern(c, x, y, count=6, radius=14, color=None, alpha=0.15):
    if color is None: color = G_ACCENT
    cols = ['#52B788','#2D6A4F','#74C69D','#1A3320','#95D5B2']
    for i in range(count):
        col = HexColor(cols[i % len(cols)])
        c.setFillColor(col)
        c.setFillAlpha(alpha)
        ox = (i % 3) * radius * 1.8
        oy = (i // 3) * radius * 1.6
        hexagon(c, x+ox, y+oy, radius-2, fill=col)
    c.setFillAlpha(1.0)

def section_header(c, title, subtitle, page_num, total=8):
    # Full bleed dark BG
    c.setFillColor(G_DARKEST)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_grid_bg(c)

    # Side accent bar
    c.setFillColor(G_ACCENT)
    c.rect(0, 0, 6, H, fill=1, stroke=0)

    # Top bar
    c.setFillColor(G_DARK)
    c.rect(0, H-18*mm, W, 18*mm, fill=1, stroke=0)
    c.setFillColor(G_ACCENT)
    c.setFont('Mono', 8)
    c.drawString(12*mm, H-10*mm, f'NAIJASLANGS API  ·  OPEN SOURCE ROADMAP 2025–2026')
    c.setFont('Mono', 8)
    c.setFillColor(G_LIGHT)
    c.drawRightString(W-10*mm, H-10*mm, f'{page_num:02d} / {total:02d}')

    # Decorative hexagons top-right
    c.saveState()
    draw_hex_pattern(c, W-80, H-60, count=6, radius=20, alpha=0.3)
    c.restoreState()

    # Section pill
    c.setFillColor(G_MID)
    c.roundRect(12*mm, H-38*mm, 50*mm, 8*mm, 4, fill=1, stroke=0)
    c.setFillColor(G_NEON)
    c.setFont('Mono-Bold', 7)
    c.drawString(14*mm, H-33.5*mm, f'§ SECTION {page_num:02d}')

    # Main title
    c.setFillColor(WHITE)
    c.setFont('Serif-Bold', 28)
    c.drawString(12*mm, H-54*mm, title)

    # Accent line under title
    c.setStrokeColor(G_ACCENT)
    c.setLineWidth(2)
    c.line(12*mm, H-57*mm, 80*mm, H-57*mm)

    # Subtitle
    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 10)
    c.drawString(12*mm, H-64*mm, subtitle)

def page_cover(c):
    # Full dark bg
    c.setFillColor(G_DARKEST)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Grid
    draw_grid_bg(c)

    # Large background hex mandala
    c.saveState()
    sizes = [120, 90, 65, 45, 30, 20, 12]
    alphas = [0.04, 0.07, 0.1, 0.14, 0.18, 0.22, 0.3]
    cols = [G_MID, G_MID, G_ACCENT, G_ACCENT, G_NEON, G_LIGHT, G_LIGHTEST]
    for r, a, col in zip(sizes, alphas, cols):
        c.setFillColor(col)
        c.setFillAlpha(a)
        hexagon(c, W*0.72, H*0.38, r*2, fill=col)
    c.setFillAlpha(1.0)
    c.restoreState()

    # Hex grid decoration bottom-left
    c.saveState()
    for row in range(5):
        for col in range(4):
            ox = 20 + col * 28
            oy = 30 + row * 24
            shade = HexColor('#1A3320') if (row+col)%3==0 else (G_MID if (row+col)%3==1 else G_DARK)
            hexagon(c, ox, oy, 11, fill=shade)
    c.setFillAlpha(1.0)
    c.restoreState()

    # Left accent bar
    c.setFillColor(G_ACCENT)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    # Bottom accent strip
    c.setFillColor(G_MID)
    c.rect(0, 0, W, 16*mm, fill=1, stroke=0)
    c.setFillColor(G_ACCENT)
    c.rect(0, 0, W, 2, fill=1, stroke=0)

    # Version badge
    c.setFillColor(G_ACCENT)
    c.roundRect(16*mm, H-24*mm, 38*mm, 9*mm, 4, fill=1, stroke=0)
    c.setFillColor(G_DARKEST)
    c.setFont('Mono-Bold', 8)
    c.drawString(18*mm, H-19*mm, 'VERSION 2.0  ·  OPEN SOURCE')

    # Main title
    c.setFillColor(WHITE)
    c.setFont('Serif-Bold', 52)
    c.drawString(16*mm, H-60*mm, 'Naija')
    c.setFillColor(G_ACCENT)
    c.drawString(16*mm, H-84*mm, 'Slangs')
    c.setFillColor(G_LIGHT)
    c.setFont('Serif-Bold', 22)
    c.drawString(16*mm, H-96*mm, 'Dictionary API')

    # Thin separator
    c.setStrokeColor(G_ACCENT)
    c.setLineWidth(1.5)
    c.line(16*mm, H-101*mm, W-16*mm, H-101*mm)

    # Tagline
    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 11)
    c.drawString(16*mm, H-110*mm, 'The definitive open-source API for Nigerian slang,')
    c.drawString(16*mm, H-118*mm, 'pidgin expressions & street lingo.')

    # Stat boxes
    stats = [('5,000+', 'Slang Words'), ('50+', 'Contributors'), ('100K+', 'API Calls/Mo'), ('MIT', 'License')]
    bw = 38*mm
    for i, (val, lbl) in enumerate(stats):
        bx = 16*mm + i*(bw+3*mm)
        by = H - 148*mm
        c.setFillColor(G_DARK)
        c.roundRect(bx, by, bw, 18*mm, 4, fill=1, stroke=0)
        c.setStrokeColor(G_ACCENT)
        c.setLineWidth(0.8)
        c.roundRect(bx, by, bw, 18*mm, 4, fill=0, stroke=1)
        c.setFillColor(G_ACCENT)
        c.setFont('Serif-Bold', 14)
        c.drawCentredString(bx+bw/2, by+10*mm, val)
        c.setFillColor(G_LIGHT)
        c.setFont('Sans', 7)
        c.drawCentredString(bx+bw/2, by+5*mm, lbl)

    # Sections index
    sections = ['01 · The Problem & Vision', '02 · Dataset Sources', '03 · Tech Stack', '04 · Build Roadmap', '05 · Community & Contribution', '06 · Promotion Strategy']
    c.setFillColor(G_DARK)
    c.roundRect(16*mm, H-195*mm, W-32*mm, 42*mm, 6, fill=1, stroke=0)
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(20*mm, H-162*mm, 'CONTENTS')
    c.setStrokeColor(G_ACCENT); c.setLineWidth(0.5)
    c.line(20*mm, H-164*mm, 60*mm, H-164*mm)
    for i, s in enumerate(sections):
        col = 0 if i < 3 else 1
        row = i % 3
        tx = 20*mm + col*(W/2-20*mm)
        ty = H-170*mm - row*8*mm
        c.setFillColor(G_NEON if i==0 else G_LIGHT)
        c.setFont('Sans', 8)
        c.drawString(tx, ty, s)

    # Footer
    c.setFillColor(G_LIGHT)
    c.setFont('Mono', 7)
    c.drawString(16*mm, 8*mm, '@icedmist / NEXA Technologies  ·  naijaslangs.dev  ·  2025–2026')
    c.drawRightString(W-16*mm, 8*mm, 'Confidential Product Roadmap')

def page_problem(c):
    section_header(c, 'The Problem\n& Vision', 'Why NaijaSlangs needs to exist', 1)

    y = H - 82*mm

    # Problem cards
    problems = [
        ('NO STRUCTURED API', 'Developers building Naija-focused apps hardcode slang manually — no reliable, machine-readable source exists.', G_ACCENT),
        ('SUBTITLING FAILURE', 'Nollywood & Afrobeats subtitling tools break on pidgin and street lingo, failing millions of global viewers.', G_NEON),
        ('NLP DATA GAP', 'AI/ML models trained on Nigerian social media lack labelled data, causing poor sentiment analysis for African languages.', G_LIGHT),
        ('CULTURAL BARRIER', 'Tourists, foreigners, and diaspora have no reliable lookup tool for Nigerian culture, slang & identity.', HexColor('#B7E4C7')),
    ]

    for i, (title, desc, col) in enumerate(problems):
        col_x = 12*mm if i%2==0 else W/2+3*mm
        row_y = y - (i//2)*38*mm
        bw = W/2 - 18*mm

        # Card bg
        c.setFillColor(G_DARK)
        c.roundRect(col_x, row_y-28*mm, bw, 32*mm, 6, fill=1, stroke=0)
        # Left accent
        c.setFillColor(col)
        c.rect(col_x, row_y-28*mm, 3, 32*mm, fill=1, stroke=0)
        # Title
        c.setFillColor(col)
        c.setFont('Sans-Bold', 8)
        c.drawString(col_x+6*mm, row_y-5*mm, title)
        # Desc
        c.setFillColor(G_LIGHTEST)
        c.setFont('Sans', 7.5)
        # Word wrap
        words = desc.split()
        line = ''; lines = []
        for w in words:
            test = line+' '+w if line else w
            if c.stringWidth(test, 'Sans', 7.5) < bw-8*mm: line=test
            else: lines.append(line); line=w
        if line: lines.append(line)
        for li, ln in enumerate(lines[:3]):
            c.drawString(col_x+6*mm, row_y-13*mm-li*9, ln)

    # Vision block
    vy = y - 82*mm
    c.setFillColor(G_MID)
    c.roundRect(12*mm, vy-30*mm, W-24*mm, 34*mm, 8, fill=1, stroke=0)
    c.setFillColor(G_DARKEST)
    c.roundRect(12*mm, vy-30*mm, W-24*mm, 34*mm, 8, fill=0, stroke=1)
    c.setStrokeColor(G_ACCENT)

    # Hex icon
    hexagon(c, 24*mm, vy-13*mm, 8*mm, fill=G_DARKEST)
    c.setFillColor(G_ACCENT)
    c.setFont('Serif-Bold', 10)
    c.drawCentredString(24*mm, vy-15*mm, '◆')

    c.setFillColor(WHITE)
    c.setFont('Serif-Bold', 12)
    c.drawString(35*mm, vy-7*mm, 'The Vision')
    c.setFillColor(G_LIGHTEST)
    c.setFont('Sans', 8.5)
    vision = 'A free, community-driven API with a contributor portal, open dataset on GitHub, and full developer tooling — becoming the definitive linguistic infrastructure for Nigerian digital culture. Built with FastAPI, PostgreSQL, Redis & Elasticsearch.'
    words = vision.split(); line=''; lines=[]
    for w in words:
        test=line+' '+w if line else w
        if c.stringWidth(test,'Sans',8.5)<W-50*mm: line=test
        else: lines.append(line); line=w
    if line: lines.append(line)
    for li, ln in enumerate(lines):
        c.drawString(35*mm, vy-16*mm-li*10, ln)

    # Year targets
    ty = vy - 40*mm
    c.setFillColor(G_DARK)
    c.roundRect(12*mm, ty-24*mm, W-24*mm, 28*mm, 6, fill=1, stroke=0)
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(16*mm, ty-6*mm, 'YEAR 1 TARGETS')
    targets = [('5,000+\nWords', W*0.18), ('500+\nAPI Keys', W*0.35), ('1,000+\nGitHub Stars', W*0.53), ('100K+\nMonthly Calls', W*0.72), ('50+\nContributors', W*0.89)]
    for val, tx in targets:
        lines2 = val.split('\n')
        c.setFillColor(G_ACCENT)
        c.setFont('Serif-Bold', 11)
        c.drawCentredString(tx, ty-14*mm, lines2[0])
        c.setFillColor(G_LIGHT)
        c.setFont('Sans', 6.5)
        c.drawCentredString(tx, ty-20*mm, lines2[1])

def page_datasets(c):
    section_header(c, 'Dataset\nSources', 'Where to get your slang data', 2)
    y = H - 82*mm

    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 9)
    c.drawString(12*mm, y, 'The content layer is the hardest part. Here are your best real sources — tiered by quality and reliability.')

    y -= 12*mm

    categories = [
        {
            'tier': 'TIER 1 — COMMUNITY GOLD',
            'color': G_ACCENT,
            'sources': [
                ('Twitter / X API v2', 'twitter.com/developer', 'Scrape trending Nigerian slang in real-time using hashtags like #Naija, #PidginEnglish, #LagosStreet. Use academic access for bulk historical data.'),
                ('Nairaland.com', 'nairaland.com', 'Largest Nigerian forum with millions of posts. Rich pidgin and slang usage in natural context. Scrape threads in /entertainment, /romance, /jokes.'),
                ('Urban Dictionary (Nigeria tag)', 'urbandictionary.com', 'Filter entries tagged Nigeria, Pidgin, Yoruba, Igbo, Hausa. Use their API. Quality varies — needs moderation layer.'),
            ]
        },
        {
            'tier': 'TIER 2 — ACADEMIC & STRUCTURED',
            'color': G_NEON,
            'sources': [
                ('AfriSenti Dataset', 'github.com/hausanlp/AfriSenti', 'Multilingual sentiment dataset covering Hausa, Yoruba, Igbo with annotated tweets. MIT Licensed. Ready-to-use JSON.'),
                ('MENYO-20k / Masakhane', 'github.com/masakhane-io', 'Open-source African NLP datasets. Yoruba/Igbo/Hausa translations, great for etymology and cross-referencing definitions.'),
                ('Wikitionary (Yoruba/Igbo/Hausa)', 'wiktionary.org', 'Structured lexical data with etymology, phonetics. Download full dump in XML — filter for Nigerian languages. Free, CC-BY-SA.'),
            ]
        },
        {
            'tier': 'TIER 3 — MANUAL & COMMUNITY',
            'color': G_LIGHT,
            'sources': [
                ('Manual Contributor Portal', 'your own site', 'Build a web form for community submissions. Each word gets definition, example sentence, region tag, language group. Moderate before merge.'),
                ('Nigerian Music Lyrics', 'genius.com', 'Scrape annotated lyrics from Burna Boy, Wizkid, Davido. Genius annotations often explain slang terms inline. High cultural accuracy.'),
            ]
        },
    ]

    for cat in categories:
        c.setFillColor(HexColor('#1A3320'))
        c.roundRect(12*mm, y-6*mm, W-24*mm, 7*mm, 3, fill=1, stroke=0)
        c.setStrokeColor(cat['color']); c.setLineWidth(0.8)
        c.line(12*mm, y-6*mm, 12*mm+4, y-6*mm+7*mm)
        c.setFillColor(cat['color'])
        c.setFont('Mono-Bold', 7)
        c.drawString(16*mm, y-3.5*mm, cat['tier'])
        y -= 10*mm

        for name, url, desc in cat['sources']:
            bh = 22*mm
            c.setFillColor(G_DARK)
            c.roundRect(14*mm, y-bh, W-28*mm, bh, 4, fill=1, stroke=0)
            # accent dot
            c.setFillColor(cat['color'])
            c.circle(19*mm, y-8*mm, 3, fill=1, stroke=0)
            # name
            c.setFillColor(WHITE)
            c.setFont('Sans-Bold', 9)
            c.drawString(23*mm, y-6*mm, name)
            # url
            c.setFillColor(cat['color'])
            c.setFont('Mono', 7)
            c.drawString(23*mm, y-11*mm, url)
            # desc
            c.setFillColor(G_LIGHTEST)
            c.setFont('Sans', 7)
            words = desc.split(); line=''; lines=[]
            for w in words:
                test=line+' '+w if line else w
                if c.stringWidth(test,'Sans',7)<W-45*mm: line=test
                else: lines.append(line); line=w
            if line: lines.append(line)
            for li, ln in enumerate(lines[:2]):
                c.drawString(23*mm, y-17*mm-li*8, ln)
            y -= bh + 2*mm
        y -= 4*mm

def page_techstack(c):
    section_header(c, 'Tech Stack', 'Architecture & tools — chosen for solo/small team builds', 3)
    y = H - 82*mm

    # Architecture diagram — 3D layered feel
    layers = [
        ('CLIENT LAYER', ['Web Browser', 'Mobile App', 'Dev / CLI', '3rd Party Apps'], G_ACCENT, H-90*mm),
        ('GATEWAY', ['API Rate Limiter', 'Auth (JWT)', 'Kong / AWS GW'], G_NEON, H-116*mm),
        ('APP LAYER', ['FastAPI + Pydantic', 'Slang Service', 'Search Service', 'Auth Service'], G_MID, H-142*mm),
        ('DATA LAYER', ['PostgreSQL', 'Redis Cache', 'Elasticsearch', 'ClickHouse Analytics'], G_DARK, H-168*mm),
    ]

    for label, items, col, ly in layers:
        # Layer bg with 3D shadow effect
        c.setFillColor(HexColor('#0D1B0F'))
        c.roundRect(14*mm+2, ly-16*mm-2, W-28*mm, 20*mm, 4, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(14*mm, ly-16*mm, W-28*mm, 20*mm, 4, fill=1, stroke=0)
        c.setFillColor(G_DARKEST)
        c.roundRect(14*mm, ly-16*mm, W-28*mm, 20*mm, 4, fill=0, stroke=1)
        c.setStrokeColor(G_DARKEST); c.setLineWidth(0.5)

        # Label
        c.setFillColor(G_DARKEST)
        c.setFont('Mono-Bold', 6.5)
        c.drawString(18*mm, ly-5*mm, label)

        # Items as pills
        pill_x = 50*mm
        for item in items:
            pw = c.stringWidth(item, 'Sans', 7) + 8*mm
            c.setFillColor(G_DARKEST)
            c.roundRect(pill_x, ly-13*mm, pw, 7*mm, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont('Sans', 7)
            c.drawString(pill_x+4*mm, ly-9.5*mm, item)
            pill_x += pw + 3*mm

        # Connector arrow down
        if ly > H-168*mm:
            c.setStrokeColor(G_ACCENT)
            c.setLineWidth(1)
            arr_x = W/2
            c.line(arr_x, ly-16*mm, arr_x, ly-20*mm)
            c.line(arr_x-3, ly-18*mm, arr_x, ly-20*mm)
            c.line(arr_x+3, ly-18*mm, arr_x, ly-20*mm)

    # Stack cards
    sy = H - 198*mm
    stacks = [
        ('BACKEND', ['FastAPI (Python)', 'Pydantic models', 'Uvicorn ASGI', 'SQLAlchemy ORM'], G_ACCENT),
        ('DATABASE', ['PostgreSQL (Neon.tech)', 'Redis (Upstash)', 'Elasticsearch (Bonsai)', 'Alembic migrations'], G_NEON),
        ('DEVOPS', ['Docker + Compose', 'GitHub Actions CI', 'Render.com hosting', 'Nginx reverse proxy'], G_LIGHT),
        ('DX / DOCS', ['Swagger UI + ReDoc', 'Postman Collection', 'JS SDK (npm)', 'Python SDK (PyPI)'], G_MID),
    ]
    sw = (W - 32*mm) / 4
    for i, (title, items, col) in enumerate(stacks):
        sx = 12*mm + i*(sw+2*mm)
        c.setFillColor(G_DARK)
        c.roundRect(sx, sy-32*mm, sw, 36*mm, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.rect(sx, sy-32*mm, sw, 3, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont('Mono-Bold', 7)
        c.drawCentredString(sx+sw/2, sy-8*mm, title)
        c.setStrokeColor(col); c.setLineWidth(0.4)
        c.line(sx+4*mm, sy-11*mm, sx+sw-4*mm, sy-11*mm)
        for j, item in enumerate(items):
            c.setFillColor(G_LIGHTEST)
            c.setFont('Sans', 7)
            c.drawString(sx+5*mm, sy-18*mm-j*7, '› '+item)

def page_roadmap(c):
    section_header(c, 'Build Roadmap', 'Phase-by-phase execution plan', 4)
    y = H - 82*mm

    phases = [
        ('01', 'FOUNDATION', 'Weeks 1–6', G_ACCENT, [
            'PostgreSQL schema design (slangs, categories, regions, contributors)',
            'Seed 500 slang words manually with definitions, examples, phonetics',
            'FastAPI project structure + Docker Compose (app + postgres + redis + ES)',
            'GitHub repo: CONTRIBUTING.md, CODE_OF_CONDUCT.md, MIT License',
            'Alembic migrations pipeline + initial data seeding scripts',
        ]),
        ('02', 'CORE API', 'Weeks 5–10', G_NEON, [
            'CRUD endpoints: GET/POST/PUT/DELETE /slangs with pagination & filtering',
            'API key auth (JWT) + rate limiting (free: 100 req/hr, open: unlimited)',
            'Input validation with Pydantic + automated test suite (80%+ coverage)',
            'CI/CD pipeline via GitHub Actions (lint + test + deploy to Render)',
        ]),
        ('03', 'SEARCH & DX', 'Weeks 9–14', G_LIGHT, [
            'Elasticsearch: full-text fuzzy search with typo tolerance + phonetics',
            'Swagger UI + ReDoc auto-generated docs + live API playground (Next.js)',
            'JavaScript SDK (npm: naijaslangs-js) + Python SDK (PyPI: naijaslangs-py)',
            'Webhook support for word-of-the-day subscriptions',
        ]),
        ('04', 'OPEN SOURCE LAUNCH', 'Weeks 13–18', HexColor('#B7E4C7'), [
            'Public GitHub launch: detailed README, badges, demo GIFs',
            'Contributor portal: web form to submit new slang words + moderation queue',
            'Launch on Product Hunt, Dev.to, Hashnode, Twitter/X with launch thread',
            'Submit to awesome-python, awesome-apis, African OSS directories',
        ]),
        ('05', 'GROWTH & SCALE', 'Month 5–12', HexColor('#74C69D'), [
            'GraphQL endpoint, mobile SDKs (React Native + Flutter)',
            'Nigerian university partnerships (UniLag, UNIABUJA) for student contributions',
            'Bulk dataset exports for NLP/AI researchers (CSV, JSON, JSONL)',
            'Annual "State of Naija Slang" report — trending words, regional shifts',
        ]),
    ]

    # Timeline spine
    spine_x = 22*mm
    c.setStrokeColor(G_MID); c.setLineWidth(1.5)
    c.line(spine_x, y+2*mm, spine_x, y - len(phases)*30*mm)

    for i, (num, title, time, col, tasks) in enumerate(phases):
        py = y - i*33*mm
        ph = 28*mm

        # Circle on spine
        c.setFillColor(col)
        c.circle(spine_x, py-4*mm, 5, fill=1, stroke=0)
        c.setFillColor(G_DARKEST)
        c.setFont('Mono-Bold', 5)
        c.drawCentredString(spine_x, py-5.5*mm, num)

        # Phase card
        c.setFillColor(G_DARK)
        c.roundRect(30*mm, py-ph, W-42*mm, ph, 4, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(30*mm, py-ph, 3, ph, 2, fill=1, stroke=0)

        # Title + time
        c.setFillColor(col)
        c.setFont('Sans-Bold', 9)
        c.drawString(35*mm, py-6*mm, title)
        c.setFillColor(G_MID)
        c.setFont('Mono', 7)
        c.drawRightString(W-16*mm, py-6*mm, time)

        # Tasks
        max_tasks = min(len(tasks), 3)
        for j in range(max_tasks):
            c.setFillColor(col)
            c.circle(37*mm, py-12*mm-j*7, 1.5, fill=1, stroke=0)
            c.setFillColor(G_LIGHTEST)
            c.setFont('Sans', 7)
            text = tasks[j][:72]+'…' if len(tasks[j])>72 else tasks[j]
            c.drawString(40*mm, py-13.5*mm-j*7, text)

def page_community(c):
    section_header(c, 'Community &\nContribution', 'Building the people layer', 5)
    y = H - 82*mm

    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 9)
    c.drawString(12*mm, y, 'Open source lives or dies by its community. Here\'s how to build one that sustains the project.')
    y -= 14*mm

    # Contributor journey flow
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(12*mm, y, 'CONTRIBUTOR JOURNEY')
    y -= 8*mm

    steps = ['Discover on GitHub / Twitter', 'Fork & read CONTRIBUTING.md', 'Submit slang via portal or PR', 'Moderation review (48hr)', 'Word approved → leaderboard', 'Repeat → recognized contributor']
    sw = (W - 24*mm) / len(steps)
    for i, step in enumerate(steps):
        sx = 12*mm + i*sw
        # Box
        col = G_ACCENT if i==0 else (G_NEON if i==len(steps)-1 else G_MID)
        c.setFillColor(col if i in [0, len(steps)-1] else G_DARK)
        c.roundRect(sx+1, y-16*mm, sw-3, 14*mm, 3, fill=1, stroke=0)
        # Number
        c.setFillColor(col)
        c.setFont('Mono-Bold', 7)
        c.drawCentredString(sx+sw/2, y-5*mm, str(i+1))
        # Text
        c.setFillColor(G_LIGHTEST if i not in [0,len(steps)-1] else G_DARKEST)
        c.setFont('Sans', 5.5)
        words = step.split()
        line=''; lines=[]
        for w in words:
            test=line+' '+w if line else w
            if c.stringWidth(test,'Sans',5.5)<sw-5: line=test
            else: lines.append(line); line=w
        if line: lines.append(line)
        for li, ln in enumerate(lines[:2]):
            c.drawCentredString(sx+sw/2, y-10*mm-li*5.5, ln)
        # Arrow
        if i < len(steps)-1:
            c.setStrokeColor(G_ACCENT); c.setLineWidth(0.8)
            ax = sx+sw-2
            ay = y-9*mm
            c.line(ax, ay, ax+2, ay)

    y -= 24*mm

    # Incentive cards
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(12*mm, y, 'CONTRIBUTOR INCENTIVES')
    y -= 10*mm

    incentives = [
        ('🏆', 'Public Leaderboard', 'Top contributors listed on naijaslangs.dev with GitHub handles and word count. Permanent recognition.'),
        ('🎖️', 'Contributor Badge', 'GitHub profile badge and README credit for approved contributors. Carries OSS credibility.'),
        ('📊', 'Slang of the Week', 'Top contributor\'s word featured weekly on Twitter/X tagging their handle. Organic social exposure.'),
        ('🎓', 'University Credits', 'Partner with CS departments — student contributions count toward open source coursework hours.'),
        ('🛠️', 'API Access', 'Top contributors get elevated rate limits and early access to new endpoints and dataset exports.'),
        ('📋', 'Co-author Credits', 'Significant contributors credited co-authors in academic dataset papers and publications.'),
    ]

    iw = (W-28*mm)/3
    for i, (icon, title, desc) in enumerate(incentives):
        col = i%3; row = i//3
        ix = 12*mm + col*(iw+2*mm)
        iy = y - row*26*mm
        c.setFillColor(G_DARK)
        c.roundRect(ix, iy-20*mm, iw, 22*mm, 5, fill=1, stroke=0)
        c.setFillColor(G_ACCENT)
        c.setFont('Sans-Bold', 12)
        c.drawString(ix+3*mm, iy-7*mm, icon)
        c.setFillColor(G_ACCENT)
        c.setFont('Sans-Bold', 7.5)
        c.drawString(ix+14*mm, iy-6*mm, title)
        c.setFillColor(G_LIGHTEST)
        c.setFont('Sans', 6.5)
        words = desc.split(); line=''; lines=[]
        for w in words:
            test=line+' '+w if line else w
            if c.stringWidth(test,'Sans',6.5)<iw-7*mm: line=test
            else: lines.append(line); line=w
        if line: lines.append(line)
        for li, ln in enumerate(lines[:2]):
            c.drawString(ix+3*mm, iy-13*mm-li*7, ln)

    # Schema quick ref
    sy = y - 58*mm
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(12*mm, sy, 'KEY DATABASE TABLES')
    sy -= 8*mm

    tables = [
        ('slangs', 'id, word, slug, definition, examples (JSONB), phonetic, audio_url, popularity_score'),
        ('contributors', 'id, github_handle, email, total_approved, joined_at'),
        ('submissions', 'id, word, definition, status, contributor_id, reviewed_at'),
        ('regions', 'id, name, code — Lagos, Abuja, Port Harcourt, Kano, etc.'),
    ]
    tw = (W-28*mm)/2
    for i, (tname, cols) in enumerate(tables):
        col = i%2; row = i//2
        tx2 = 12*mm + col*(tw+4*mm)
        ty2 = sy - row*14*mm
        c.setFillColor(G_DARK)
        c.roundRect(tx2, ty2-10*mm, tw, 12*mm, 3, fill=1, stroke=0)
        c.setFillColor(G_NEON)
        c.setFont('Mono-Bold', 7)
        c.drawString(tx2+3*mm, ty2-4*mm, tname)
        c.setFillColor(G_LIGHT)
        c.setFont('Mono', 5.5)
        display = cols[:65]+'…' if len(cols)>65 else cols
        c.drawString(tx2+3*mm, ty2-9*mm, display)

def page_promotion(c):
    section_header(c, 'Promotion\nStrategy', 'Reaching developers & Nigerian culture globally', 6)
    y = H - 82*mm

    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 9)
    c.drawString(12*mm, y, 'A free, open-source project lives by visibility. Here\'s a layered promotional strategy.')
    y -= 14*mm

    # Launch wave timeline
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(12*mm, y, 'LAUNCH WAVE TIMELINE')
    y -= 8*mm

    waves = [
        ('WAVE 1\nMonth 1–2', 'Soft Launch', ['GitHub repo public', 'Dev.to article', 'Twitter thread'], G_ACCENT),
        ('WAVE 2\nMonth 3–4', 'Community Push', ['Product Hunt launch', 'DevCareers Slack', '#NaijaSlangChallenge'], G_NEON),
        ('WAVE 3\nMonth 5–6', 'Media Reach', ['Techpoint Africa pitch', 'YouTube walkthrough', 'Reddit r/programming'], G_LIGHT),
        ('WAVE 4\nMonth 7–12', 'Scale & Partner', ['University partnerships', 'API Hackathon', 'State of Naija report'], HexColor('#B7E4C7')),
    ]

    ww = (W - 28*mm) / 4
    for i, (label, title, items, col) in enumerate(waves):
        wx = 12*mm + i*(ww+2.5*mm)
        c.setFillColor(G_DARK)
        c.roundRect(wx, y-38*mm, ww, 36*mm, 5, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(wx, y-38*mm, ww, 3, 2, fill=1, stroke=0)
        lines2 = label.split('\n')
        c.setFillColor(col)
        c.setFont('Mono-Bold', 7)
        c.drawCentredString(wx+ww/2, y-8*mm, lines2[0])
        c.setFillColor(G_MID)
        c.setFont('Mono', 6)
        c.drawCentredString(wx+ww/2, y-13*mm, lines2[1])
        c.setFillColor(WHITE)
        c.setFont('Sans-Bold', 7.5)
        c.drawCentredString(wx+ww/2, y-19*mm, title)
        c.setStrokeColor(col); c.setLineWidth(0.4)
        c.line(wx+4*mm, y-21*mm, wx+ww-4*mm, y-21*mm)
        for j, item in enumerate(items):
            c.setFillColor(col)
            c.circle(wx+6*mm, y-26*mm-j*7, 1.5, fill=1, stroke=0)
            c.setFillColor(G_LIGHTEST)
            c.setFont('Sans', 6.5)
            c.drawString(wx+9*mm, y-27.5*mm-j*7, item)

    y -= 48*mm

    # Channels table
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(12*mm, y, 'PROMOTION CHANNELS & EXPECTED REACH')
    y -= 8*mm

    channels = [
        ('Twitter / X', 'Launch thread with demo GIF + live API playground link', '5K–20K impressions', G_ACCENT),
        ('Dev.to / Hashnode', 'Full architecture write-up — how I built a Nigerian Slang API', '3K–10K reads', G_NEON),
        ('Product Hunt', 'Full product launch with video demo on launch day', '500–2K upvotes', G_LIGHT),
        ('GitHub Stars', 'Outreach to Nigerian dev Discord / Telegram groups', '500–1.5K stars', G_ACCENT),
        ('DevCareers Slack', 'Share in #projects — largest Nigerian dev community', '300–800 signups', G_NEON),
        ('Techpoint Africa', 'Pitch to podcast as African OSS infrastructure story', '5K–20K listeners', G_LIGHT),
        ('Reddit', 'r/programming, r/webdev, r/Nigeria — live demo post', '500–3K views', G_ACCENT),
        ('YouTube', '5-min "Building a Public API in Python" walkthrough', '1K–5K views', G_NEON),
    ]

    rh = 10*mm
    for i, (ch, tactic, reach, col) in enumerate(channels):
        row_y = y - i*rh
        bg = G_DARK if i%2==0 else HexColor('#162a1a')
        c.setFillColor(bg)
        c.rect(12*mm, row_y-rh+1, W-24*mm, rh-1, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont('Sans-Bold', 7.5)
        c.drawString(15*mm, row_y-6*mm, ch)
        c.setFillColor(G_LIGHTEST)
        c.setFont('Sans', 7)
        c.drawString(50*mm, row_y-6*mm, tactic[:60])
        c.setFillColor(G_ACCENT)
        c.setFont('Mono', 7)
        c.drawRightString(W-15*mm, row_y-6*mm, reach)

    # Community initiatives
    cy = y - len(channels)*rh - 8*mm
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 7)
    c.drawString(12*mm, cy, 'COMMUNITY GROWTH INITIATIVES')
    cy -= 8*mm

    initiatives = [
        ('Slang of the Week', 'Tweet a new slang word weekly — build to 1K+ followers organically'),
        ('#NaijaSlangChallenge', 'Twitter challenge: tweet your fav slang + tag @NaijaSlangsAPI'),
        ('API Hackathon', 'Sponsor a mini hackathon: "Build something with NaijaSlangs API"'),
        ('Uni Partnerships', 'Partner with UniLag, UNIABUJA CS depts for student contributions'),
    ]

    iw2 = (W-28*mm)/2
    for i, (name, desc) in enumerate(initiatives):
        col2 = i%2; row2 = i//2
        ix2 = 12*mm + col2*(iw2+4*mm)
        iy2 = cy - row2*14*mm
        c.setFillColor(G_DARK)
        c.roundRect(ix2, iy2-10*mm, iw2, 12*mm, 3, fill=1, stroke=0)
        c.setFillColor(G_NEON)
        c.setFont('Sans-Bold', 7.5)
        c.drawString(ix2+3*mm, iy2-4*mm, name)
        c.setFillColor(G_LIGHTEST)
        c.setFont('Sans', 6.5)
        c.drawString(ix2+3*mm, iy2-9*mm, desc[:68])

def page_closing(c):
    c.setFillColor(G_DARKEST)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_grid_bg(c)

    # Large hex bg center
    c.saveState()
    sizes2 = [140, 100, 70, 48, 30, 18]
    alphas2 = [0.03, 0.06, 0.09, 0.13, 0.2, 0.3]
    for r, a in zip(sizes2, alphas2):
        c.setFillColor(G_ACCENT)
        c.setFillAlpha(a)
        hexagon(c, W/2, H/2, r*2, fill=G_ACCENT)
    c.setFillAlpha(1.0)
    c.restoreState()

    # Hex grid top right decorative
    c.saveState()
    for row in range(4):
        for col2 in range(5):
            ox = W-120+col2*26
            oy = H-100+row*22
            hexagon(c, ox, oy, 10, fill=G_DARK if (row+col2)%2==0 else G_MID)
    c.restoreState()

    c.setFillColor(G_ACCENT)
    c.rect(0, 0, 8, H, fill=1, stroke=0)

    # Centered content
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 8)
    c.drawCentredString(W/2, H*0.72, 'NAIJASLANGS API — OPEN SOURCE ROADMAP 2025–2026')

    c.setStrokeColor(G_ACCENT); c.setLineWidth(1)
    c.line(W/2-50*mm, H*0.70, W/2+50*mm, H*0.70)

    c.setFillColor(WHITE)
    c.setFont('Serif-Bold', 36)
    c.drawCentredString(W/2, H*0.60, 'Ship It.')

    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 11)
    c.drawCentredString(W/2, H*0.53, 'The market is waiting.')

    c.setFillColor(G_MID)
    c.setFont('Sans', 9)
    c.drawCentredString(W/2, H*0.46, 'Nigeria\'s digital culture deserves world-class linguistic infrastructure.')
    c.drawCentredString(W/2, H*0.43, 'You\'re the one to build it.')

    # Links
    c.setFillColor(G_DARK)
    c.roundRect(W/2-50*mm, H*0.34, 100*mm, 22*mm, 6, fill=1, stroke=0)
    c.setStrokeColor(G_ACCENT); c.setLineWidth(0.8)
    c.roundRect(W/2-50*mm, H*0.34, 100*mm, 22*mm, 6, fill=0, stroke=1)
    c.setFillColor(G_ACCENT)
    c.setFont('Mono-Bold', 9)
    c.drawCentredString(W/2, H*0.38+5, 'naijaslangs.dev')
    c.setFillColor(G_LIGHT)
    c.setFont('Mono', 7.5)
    c.drawCentredString(W/2, H*0.36, 'github.com/icedmist/naijaslangs-api')

    # MIT badge
    c.setFillColor(G_ACCENT)
    c.roundRect(W/2-20*mm, H*0.27, 40*mm, 8*mm, 3, fill=1, stroke=0)
    c.setFillColor(G_DARKEST)
    c.setFont('Mono-Bold', 7)
    c.drawCentredString(W/2, H*0.285, 'MIT License — Free & Open Source')

    # Footer
    c.setFillColor(G_MID)
    c.setFont('Mono', 6.5)
    c.drawCentredString(W/2, 15*mm, '@icedmist / NEXA Technologies  ·  NaijaSlangs API  ·  Version 2.0')

# ══════════════════════════════════════════════════════════════════════════════
# RENDER ALL PAGES
# ══════════════════════════════════════════════════════════════════════════════

output = 'NaijaSlangs_Roadmap_v2.pdf'
c = canvas.Canvas(output, pagesize=A4)
c.setTitle('NaijaSlangs API — Revised Open Source Roadmap 2025–2026')
c.setAuthor('@icedmist / NEXA Technologies')

page_cover(c); c.showPage()
page_problem(c); c.showPage()
page_datasets(c); c.showPage()
page_techstack(c); c.showPage()
page_roadmap(c); c.showPage()
page_community(c); c.showPage()
page_promotion(c); c.showPage()
page_closing(c); c.showPage()

c.save()
print('PDF created:', os.path.abspath(output))
