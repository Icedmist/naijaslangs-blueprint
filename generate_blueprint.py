from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black, transparent
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import math
import os

# Register Google Fonts available in the system
pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold', '/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/google-crosextra-caladea-fonts/Caladea-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Bold', '/usr/share/fonts/google-crosextra-caladea-fonts/Caladea-Bold.ttf'))
# Fallback for Mono if not found, otherwise use liberation
pdfmetrics.registerFont(TTFont('Mono', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Mono-Bold', '/usr/share/fonts/liberation-mono-fonts/LiberationMono-Bold.ttf'))

W, H = A4

# ── Premium Color Palette ──────────────────────────────────────────────────────
G_DARKEST  = HexColor('#0A1F0D')
G_DARK     = HexColor('#1A3320')
G_MID      = HexColor('#2D6A4F')
G_ACCENT   = HexColor('#52B788')
G_LIGHT    = HexColor('#95D5B2')
G_LIGHTEST = HexColor('#D8F3DC')
G_GOLD     = HexColor('#F4A261')
WHITE      = HexColor('#FFFFFF')
OFF_WHITE  = HexColor('#F8FFF9')
GLASS      = HexColor('#FFFFFFCC') # Semi-transparent white

def draw_glass_rect(c, x, y, width, height, radius=4, alpha=0.8):
    c.saveState()
    c.setFillColor(WHITE)
    c.setFillAlpha(alpha)
    c.roundRect(x, y, width, height, radius, fill=1, stroke=0)
    c.restoreState()

def section_header(c, title, subtitle, page_num, image_path=None):
    # Background
    c.setFillColor(OFF_WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Accent bar at the top
    c.setFillColor(G_DARK)
    c.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    
    c.setFillColor(G_ACCENT)
    c.setFont('Mono', 7)
    c.drawString(15*mm, H-7*mm, 'THE NAIJASLANGS BLUEPRINT // 2025–2026')
    c.drawRightString(W-15*mm, H-7*mm, f'PAGE {page_num:02d}')

    # Visual Asset
    if image_path and os.path.exists(image_path):
        img = ImageReader(image_path)
        # Place image as a sidebar or background element
        c.drawImage(img, W-90*mm, H-120*mm, width=80*mm, height=80*mm, mask='auto', preserveAspectRatio=True)

    # Title
    c.setFillColor(G_DARK)
    c.setFont('Serif-Bold', 32)
    c.drawString(15*mm, H-35*mm, title)
    
    c.setStrokeColor(G_ACCENT)
    c.setLineWidth(1.5)
    c.line(15*mm, H-39*mm, 60*mm, H-39*mm)
    
    c.setFillColor(G_MID)
    c.setFont('Sans', 11)
    c.drawString(15*mm, H-46*mm, subtitle)

def page_cover(c):
    # Full bleed background image
    if os.path.exists('assets/cover.png'):
        img = ImageReader('assets/cover.png')
        c.drawImage(img, 0, 0, width=W, height=H, preserveAspectRatio=True, anchor='c')
    else:
        c.setFillColor(G_DARKEST)
        c.rect(0, 0, W, H, fill=1, stroke=0)

    # Dark overlay for contrast (gradient-like)
    c.saveState()
    c.setFillColor(G_DARKEST)
    c.setFillAlpha(0.4)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()

    # Glassmorphism Center Card
    cw, ch = 140*mm, 90*mm
    cx, cy = (W-cw)/2, H*0.4
    draw_glass_rect(c, cx, cy, cw, ch, radius=8, alpha=0.85)

    # Content on Card
    c.setFillColor(G_DARK)
    c.setFont('Serif-Bold', 48)
    c.drawCentredString(W/2, cy + 60*mm, 'The NaijaSlangs')
    c.setFillColor(G_MID)
    c.drawCentredString(W/2, cy + 42*mm, 'Blueprint')
    
    c.setStrokeColor(G_ACCENT)
    c.setLineWidth(2)
    c.line(W/2-40*mm, cy+38*mm, W/2+40*mm, cy+38*mm)

    c.setFillColor(G_DARK)
    c.setFont('Sans', 12)
    c.drawCentredString(W/2, cy + 28*mm, 'A Linguistic Infrastructure Roadmap for Nigerian Digital Culture')
    
    c.setFont('Mono-Bold', 8)
    c.setFillColor(G_MID)
    c.drawCentredString(W/2, cy + 15*mm, 'VERSION 2.0 // OPEN SOURCE STRATEGY')

    # Footer
    c.setFillColor(WHITE)
    c.setFont('Mono', 7)
    c.drawString(15*mm, 10*mm, '@icedmist / NEXA Technologies')
    c.drawRightString(W-15*mm, 10*mm, 'naijaslangs.dev // 2025')

def page_problem(c):
    section_header(c, 'The Challenge & Vision', 'Addressing the digital gap in Nigerian linguistics', 1, 'assets/problem.png')
    
    y = H - 65*mm
    problems = [
        ('Fragmentation', 'Nigerian slang is currently scattered and undocumented in machine-readable formats.'),
        ('AI Bias', 'Global NLP models fail to capture the nuances of pidgin and street lingo accurately.'),
        ('Cultural Preservation', 'As culture evolves rapidly, a centralized open-source repository is vital for preservation.'),
        ('Developer UX', 'Building apps with local context requires structured, reliable API access to terminology.')
    ]

    for i, (title, desc) in enumerate(problems):
        ty = y - i*25*mm
        c.setFillColor(G_DARK)
        c.setFont('Serif-Bold', 12)
        c.drawString(15*mm, ty, f'0{i+1}. {title}')
        
        c.setFillColor(G_MID)
        c.setFont('Sans', 9)
        # Simple word wrap
        words = desc.split()
        line = ''; lines = []
        for w in words:
            if c.stringWidth(line + ' ' + w, 'Sans', 9) < 100*mm: line += ' ' + w
            else: lines.append(line); line = w
        lines.append(line)
        for li, ln in enumerate(lines):
            c.drawString(18*mm, ty - 5*mm - li*4.5*mm, ln.strip())

    # Vision Statement
    vy = y - 110*mm
    draw_glass_rect(c, 15*mm, vy-25*mm, W-30*mm, 35*mm, radius=6, alpha=0.5)
    c.setFillColor(G_DARK)
    c.setFont('Serif-Bold', 14)
    c.drawString(20*mm, vy, 'Our North Star')
    c.setFillColor(G_MID)
    c.setFont('Sans', 10)
    vision = 'To become the definitive linguistic infrastructure for Africa\'s most populous nation, empowering developers and researchers with high-quality, community-vetted slang data.'
    c.drawString(20*mm, vy-8*mm, vision[:80])
    c.drawString(20*mm, vy-13*mm, vision[80:])

def page_datasets(c):
    section_header(c, 'Strategic Data Sourcing', 'Tiered approach to building a world-class dataset', 2, 'assets/datasets.png')
    
    y = H - 65*mm
    tiers = [
        ('Tier 1: Social Scraped', 'Real-time extraction from X/Twitter and social trends using advanced NLP tagging.'),
        ('Tier 2: Community Vetted', 'Direct submissions through our contributor portal, reviewed by language experts.'),
        ('Tier 3: Academic/Open', 'Integration with Masakhane and Wiktionary dumps for historical and structural depth.')
    ]

    for i, (title, desc) in enumerate(tiers):
        ty = y - i*30*mm
        c.setFillColor(G_ACCENT)
        c.circle(18*mm, ty+2*mm, 2, fill=1, stroke=0)
        c.setFillColor(G_DARK)
        c.setFont('Serif-Bold', 13)
        c.drawString(22*mm, ty, title)
        c.setFillColor(G_MID)
        c.setFont('Sans', 10)
        c.drawString(22*mm, ty-6*mm, desc)

def page_techstack(c):
    section_header(c, 'The Technology Stack', 'Built for performance, scalability, and developer experience', 3, 'assets/techstack.png')
    
    y = H - 65*mm
    stack = [
        ('Core Backend', 'FastAPI, Pydantic, Python 3.12'),
        ('Persistence', 'PostgreSQL (Relational), Redis (Caching)'),
        ('Search Engine', 'Elasticsearch for fuzzy, high-speed slang lookups'),
        ('Deployment', 'Docker, GitHub Actions, Kubernetes on Render')
    ]

    for i, (cat, tools) in enumerate(stack):
        ty = y - i*22*mm
        c.setFillColor(G_DARK)
        c.setFont('Mono-Bold', 8)
        c.drawString(15*mm, ty, f'[{cat.upper()}]')
        c.setFillColor(G_MID)
        c.setFont('Serif', 11)
        c.drawString(45*mm, ty, tools)

def page_roadmap(c):
    section_header(c, 'The Build Roadmap', 'A four-phase execution plan for 2025', 4, 'assets/roadmap.png')
    
    y = H - 65*mm
    phases = [
        ('Phase 1: Alpha', 'Core API development and initial 1,000 word seeding.'),
        ('Phase 2: Beta', 'Contributor portal launch and search optimization.'),
        ('Phase 3: Public V1', 'Public launch with SDKs for JS/Python/Flutter.'),
        ('Phase 4: Expansion', 'GraphQL support and NLP researcher data exports.')
    ]

    for i, (title, desc) in enumerate(phases):
        ty = y - i*25*mm
        c.setStrokeColor(G_ACCENT)
        c.setLineWidth(1)
        c.line(15*mm, ty+5*mm, 15*mm, ty-15*mm)
        
        c.setFillColor(G_DARK)
        c.setFont('Serif-Bold', 12)
        c.drawString(20*mm, ty, title)
        c.setFillColor(G_MID)
        c.setFont('Sans', 10)
        c.drawString(20*mm, ty-6*mm, desc)

def page_community(c):
    section_header(c, 'Community & Impact', 'Empowering contributors and scaling culture', 5, 'assets/community.png')
    
    y = H - 65*mm
    points = [
        'Contributor Leaderboards to gamify data entry.',
        'Annual "State of Slang" report for linguistic researchers.',
        'Hackathons focused on building apps with local context.',
        'Partnering with Nigerian universities for student-led data vetting.'
    ]

    for i, p in enumerate(points):
        ty = y - i*15*mm
        c.setFillColor(G_ACCENT)
        c.setFont('Mono-Bold', 10)
        c.drawString(15*mm, ty, '→')
        c.setFillColor(G_MID)
        c.setFont('Sans', 11)
        c.drawString(22*mm, ty, p)

def page_closing(c):
    # Darker, more dramatic closing
    c.setFillColor(G_DARKEST)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Large logo-like text
    c.setFillColor(WHITE)
    c.setFont('Serif-Bold', 42)
    c.drawCentredString(W/2, H*0.6, 'Let\'s build the infrastructure')
    c.setFillColor(G_ACCENT)
    c.drawCentredString(W/2, H*0.52, 'of Nigerian Culture.')
    
    c.setStrokeColor(G_ACCENT)
    c.setLineWidth(1)
    c.line(W/2-30*mm, H*0.48, W/2+30*mm, H*0.48)
    
    c.setFillColor(G_LIGHT)
    c.setFont('Sans', 14)
    c.drawCentredString(W/2, H*0.42, 'The Blueprint is ready. Execution begins now.')
    
    # Call to action
    c.setFillColor(G_MID)
    c.setFont('Mono-Bold', 10)
    c.drawCentredString(W/2, H*0.3, 'JOIN THE MOVEMENT')
    c.drawCentredString(W/2, H*0.26, 'github.com/icedmist/naijaslangs-api')

# ══════════════════════════════════════════════════════════════════════════════
# RENDER FINAL BLUEPRINT
# ══════════════════════════════════════════════════════════════════════════════

output = 'The_NaijaSlangs_Blueprint.pdf'
c = canvas.Canvas(output, pagesize=A4)
c.setTitle('The NaijaSlangs Blueprint // 2025–2026')
c.setAuthor('@icedmist / NEXA Technologies')

page_cover(c); c.showPage()
page_problem(c); c.showPage()
page_datasets(c); c.showPage()
page_techstack(c); c.showPage()
page_roadmap(c); c.showPage()
page_community(c); c.showPage()
page_closing(c); c.showPage()

c.save()
print('PDF created successfully:', os.path.abspath(output))
