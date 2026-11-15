#!/usr/bin/env python3
"""The Practice Exchange — static blog generator for ASEND360.

Usage:  python build.py            # publish posts dated today or earlier
        python build.py --preview  # include scheduled (future) posts
Output: dist/  (served at https://asend360.co.uk/practice-exchange/)
"""
import os, sys, glob, json, math, shutil, html, hashlib, datetime as dt
import markdown

BASE = '/practice-exchange/'
SITE = 'https://asend360.co.uk'
MAIN = ''                      # main-site links are root-relative (same domain via proxy)
PREVIEW = '--preview' in sys.argv
OUT = 'dist'
TODAY = dt.date.fromisoformat(os.environ['PX_TODAY']) if os.environ.get('PX_TODAY') else dt.date.today()
CATS = ['Practice', 'Policy & Compliance', 'Leadership', 'Inside ASEND360']
CAT_KEY = {c: c.lower().replace(' & ', '-').replace(' ', '-') for c in CATS}

def parse(path):
    raw = open(path, encoding='utf-8').read()
    _, fm, body = raw.split('---', 2)
    m = {}
    for line in fm.strip().split('\n'):
        k, v = line.split(':', 1); m[k.strip()] = v.strip()
    m['sources'] = [tuple(x.strip().split('|', 1)) for x in m.get('sources', '').split(';;') if '|' in x]
    m['html'] = markdown.markdown(body.strip(), extensions=['extra', 'sane_lists'])
    # an image on its own line becomes a figure; its title text becomes the caption
    import re as _re
    m['html'] = _re.sub(r'<p><img alt="([^"]*)" src="([^"]+)"(?: title="([^"]*)")? ?/?></p>',
        lambda g: f'<figure><img src="{g.group(2)}" alt="{g.group(1)}" loading="lazy" decoding="async">' + (f'<figcaption>{g.group(3)}</figcaption>' if g.group(3) else '') + '</figure>', m['html'])
    m['mins'] = max(2, math.ceil(len(body.split()) / 220))
    m['dt'] = dt.date.fromisoformat(m['date'])
    m['url'] = f"{BASE}{m['slug']}/"
    if m['category'] not in CATS: raise SystemExit(f"{path}: unknown category {m['category']}")
    return m

POSTS = sorted((parse(p) for p in glob.glob('posts/*.md')), key=lambda a: a['dt'], reverse=True)
LIVE = [p for p in POSTS if PREVIEW or p['dt'] <= TODAY]
fmt = lambda d: d.strftime('%-d %b %Y')
fmt_long = lambda d: d.strftime('%-d %B %Y')
esc = html.escape

# ---------- illustrations (no photos of children; brand-coloured, deterministic) ----------
def _designs(gid, seed):
    """Brand illustrations, drawn in a 640x280 frame. Navy, white, soft blue lines, one gradient accent."""
    N, W, L, T = '#003574', '#fff', '#C9D6E8', '#08ACAC'
    D = {}
    # original four
    r = ''
    for i in range(7):
        x = 90 + i * 76; y = 150 + (seed >> i) % 3 * 6 - 6; C = 2 * math.pi * 26; frac = min(1, (i + 1) / 5)
        r += f'<circle cx="{x}" cy="{y}" r="26" fill="{W}" stroke="#DDE2EA" stroke-width="7"/>'
        if i < 5: r += f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{gid}" stroke-width="7" stroke-dasharray="{C*frac:.0f} {C:.0f}" transform="rotate(-90 {x} {y})"/>'
    D['rings'] = r + f'<path d="M70 222 H570" stroke="{T}" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 12"/>'
    D['shield'] = (f'<rect x="170" y="62" width="190" height="160" rx="14" fill="{W}" stroke="{L}" stroke-width="3"/>'
        + ''.join(f'<rect x="196" y="{92+i*26}" width="{138-(i%2)*40}" height="9" rx="4.5" fill="#D2E0F1"/>' for i in range(5))
        + f'<path d="M420 70 l70 26 v52 c0 40 -30 66 -70 80 c-40 -14 -70 -40 -70 -80 v-52z" fill="{gid}"/>'
        + f'<path d="M392 150 l20 20 l38 -42" fill="none" stroke="{W}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    D['bars'] = (''.join(f'<rect x="{150+i*58}" y="{232-hgt}" width="38" height="{hgt}" rx="8" fill="{gid if i==4 else W}" stroke="{L}" stroke-width="{0 if i==4 else 3}"/>' for i, hgt in enumerate([60, 90, 80, 120, 150]))
        + f'<circle cx="500" cy="96" r="42" fill="{W}" stroke="{L}" stroke-width="3"/><path d="M500 64 l12 32 l-12 32 l-12 -32z" fill="{N}"/>')
    D['window'] = (f'<rect x="120" y="50" width="400" height="190" rx="14" fill="{W}" stroke="{L}" stroke-width="3"/><rect x="120" y="50" width="400" height="30" rx="14" fill="{N}"/><rect x="120" y="66" width="400" height="14" fill="{N}"/>'
        + ''.join(f'<circle cx="{142+i*16}" cy="65" r="4" fill="{W}" opacity=".7"/>' for i in range(3))
        + '<rect x="140" y="98" width="90" height="124" rx="8" fill="#E6EEF7"/>'
        + ''.join(f'<rect x="250" y="{100+i*30}" width="250" height="20" rx="6" fill="#F3F5F8"/><rect x="250" y="{100+i*30}" width="{60+((seed>>i)%5)*38}" height="20" rx="6" fill="{gid}"/>' for i in range(4)))
    # new designs
    D['stones'] = (f'<path d="M80 226 C 170 226, 210 176, 300 172 S 470 120, 560 92" fill="none" stroke="{T}" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>'
        + ''.join(f'<ellipse cx="{x}" cy="{y+8}" rx="{rx}" ry="{rx*0.32:.0f}" fill="#C9D6E8" opacity=".55"/><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*0.38:.0f}" fill="{gid if i==4 else W}" stroke="{L}" stroke-width="{0 if i==4 else 3}"/>'
                  for i, (x, y, rx) in enumerate([(110, 222, 44), (210, 196, 42), (310, 170, 42), (410, 140, 42), (510, 108, 46)]))
        + f'<path d="M512 96 v-48" stroke="{N}" stroke-width="5" stroke-linecap="round"/><path d="M514 48 l34 12 l-34 12z" fill="{N}"/>')
    _cy = ''
    for i, a in enumerate([-math.pi/2, 0, math.pi/2, math.pi]):
        x, y = 320 + 92*math.cos(a), 140 + 92*math.sin(a)
        _cy += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="32" fill="{gid if i==0 else W}" stroke="{L}" stroke-width="{0 if i==0 else 3}"/><rect x="{x-14:.0f}" y="{y-5:.0f}" width="28" height="10" rx="5" fill="{W if i==0 else "#D2E0F1"}"/>'
        b0, b1 = a + 0.44, a + math.pi/2 - 0.5
        sx, sy, ex, ey = 320+92*math.cos(b0), 140+92*math.sin(b0), 320+92*math.cos(b1), 140+92*math.sin(b1)
        _cy += f'<path d="M{sx:.1f} {sy:.1f} A92 92 0 0 1 {ex:.1f} {ey:.1f}" fill="none" stroke="{N}" stroke-width="5" stroke-linecap="round"/>'
        t = b1 + math.pi/2; ang = math.degrees(t)
        _cy += f'<path d="M0 -8 L12 0 L0 8" transform="translate({ex:.1f} {ey:.1f}) rotate({ang:.0f})" fill="none" stroke="{N}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    D['cycle'] = _cy
    cal = f'<rect x="170" y="48" width="300" height="196" rx="16" fill="{W}" stroke="{L}" stroke-width="3"/><rect x="170" y="48" width="300" height="44" rx="16" fill="{N}"/><rect x="170" y="74" width="300" height="18" fill="{N}"/>'
    cal += f'<rect x="215" y="36" width="10" height="26" rx="5" fill="{N}"/><rect x="415" y="36" width="10" height="26" rx="5" fill="{N}"/>'
    for rr in range(3):
        for c in range(5):
            x, y = 196 + c * 52, 110 + rr * 42
            on = (rr * 5 + c + seed) % 7 != 3
            cal += f'<rect x="{x}" y="{y}" width="38" height="30" rx="7" fill="{"#E3F5F3" if on else "#F3F5F8"}"/>'
            if on: cal += f'<path d="M{x+11} {y+15} l6 6 l11 -12" fill="none" stroke="{T}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    D['calendar'] = cal
    D['book'] = (f'<path d="M320 82 C 270 62, 200 62, 150 74 V 230 C 200 218, 270 218, 320 238 Z" fill="{W}" stroke="{L}" stroke-width="3"/>'
        f'<path d="M320 82 C 370 62, 440 62, 490 74 V 230 C 440 218, 370 218, 320 238 Z" fill="{W}" stroke="{L}" stroke-width="3"/>'
        + ''.join(f'<path d="M{176 if s<0 else 344} {104+i*24} h{120 - (i%2)*30}" stroke="#D2E0F1" stroke-width="8" stroke-linecap="round"/>' for s in (-1, 1) for i in range(5))
        + f'<path d="M440 60 v62 l-14 -10 l-14 10 v-62z" fill="{gid}"/>')
    pz = ''
    for i, (x, y, f) in enumerate([(210, 70, W), (320, 70, W), (210, 160, W), (320, 160, gid)]):
        pz += f'<rect x="{x}" y="{y}" width="110" height="90" rx="12" fill="{f}" stroke="{L}" stroke-width="{0 if f!=W else 3}"/>'
    pz += f'<circle cx="320" cy="115" r="16" fill="{W}" stroke="{L}" stroke-width="3"/><circle cx="265" cy="160" r="16" fill="{W}" stroke="{L}" stroke-width="3"/><circle cx="375" cy="160" r="16" fill="{W}" stroke="{L}" stroke-width="3"/><circle cx="320" cy="205" r="16" fill="#3FB8A5"/>'
    D['puzzle'] = pz
    D['signpost'] = (f'<rect x="312" y="60" width="16" height="190" rx="6" fill="{N}"/>'
        f'<path d="M330 74 h150 l26 22 l-26 22 h-150z" fill="{gid}"/>'
        f'<path d="M310 128 h-150 l-26 22 l26 22 h150z" fill="{W}" stroke="{L}" stroke-width="3"/>'
        f'<path d="M330 182 h110 l22 18 l-22 18 h-110z" fill="{W}" stroke="{L}" stroke-width="3"/>'
        f'<rect x="352" y="90" width="90" height="10" rx="5" fill="{W}" opacity=".8"/><rect x="186" y="145" width="96" height="10" rx="5" fill="#D2E0F1"/><rect x="352" y="195" width="60" height="10" rx="5" fill="#D2E0F1"/>'
        f'<ellipse cx="320" cy="250" rx="70" ry="8" fill="#C9D6E8" opacity=".6"/>')
    D['clipboard'] = (f'<rect x="220" y="46" width="200" height="210" rx="16" fill="{W}" stroke="{L}" stroke-width="3"/><rect x="280" y="34" width="80" height="28" rx="10" fill="{N}"/>'
        + ''.join(f'<rect x="248" y="{88+i*38}" width="24" height="24" rx="6" fill="{"#E3F5F3" if i<3 else "#F3F5F8"}" stroke="{T if i<3 else L}" stroke-width="2"/>'
                  + (f'<path d="M253 {100+i*38} l5 5 l10 -11" fill="none" stroke="{T}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' if i < 3 else '')
                  + f'<rect x="284" y="{94+i*38}" width="{110-(i%2)*30}" height="11" rx="5.5" fill="#D2E0F1"/>' for i in range(4))
        + f'<circle cx="430" cy="210" r="34" fill="{gid}"/><path d="M416 210 l10 10 l18 -20" fill="none" stroke="{W}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    D['target'] = (''.join(f'<circle cx="300" cy="150" r="{r}" fill="{f}" stroke="{L}" stroke-width="3"/>' for r, f in [(96, W), (68, "#E6EEF7"), (40, W)])
        + f'<circle cx="300" cy="150" r="16" fill="{gid}"/>'
        + f'<path d="M488 52 L 316 142" stroke="{N}" stroke-width="7" stroke-linecap="round"/>'
        + f'<path d="M488 52 l-4 -24 M488 52 l24 2 M472 60 l-4 -24 M472 60 l24 2" stroke="{T}" stroke-width="5" stroke-linecap="round"/>'
        + f'<path d="M306 147 l26 -2 l-12 -20z" fill="{N}"/>')
    D['home-school'] = (f'<path d="M100 140 l70 -56 l70 56 v86 h-140z" fill="{W}" stroke="{L}" stroke-width="3" stroke-linejoin="round"/><rect x="152" y="176" width="36" height="50" rx="6" fill="#D2E0F1"/>'
        f'<path d="M400 226 v-110 l60 -38 l60 38 v110z" fill="{W}" stroke="{L}" stroke-width="3" stroke-linejoin="round"/><rect x="440" y="170" width="40" height="56" rx="6" fill="{N}"/>'
        f'<rect x="418" y="122" width="22" height="22" rx="4" fill="#D2E0F1"/><rect x="480" y="122" width="22" height="22" rx="4" fill="#D2E0F1"/>'
        f'<path d="M250 180 C 300 130, 340 130, 390 180" fill="none" stroke="{T}" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>'
        f'<path d="M262 64 h86 a14 14 0 0 1 14 14 v30 a14 14 0 0 1 -14 14 h-56 l-16 14 v-14 h-14 a14 14 0 0 1 -14 -14 v-30 a14 14 0 0 1 14 -14z" fill="{gid}"/>'
        f'<rect x="270" y="80" width="60" height="9" rx="4.5" fill="{W}" opacity=".9"/><rect x="270" y="96" width="40" height="9" rx="4.5" fill="{W}" opacity=".9"/>')
    D['signal'] = (''.join(f'<path d="M{320-r} {170} a{r} {r} 0 0 1 {2*r} 0" fill="none" stroke="{gid if i==0 else L}" stroke-width="{8 if i==0 else 5}" stroke-linecap="round" opacity="{1 - i*0.2}"/>' for i, r in enumerate([50, 90, 130]))
        + f'<circle cx="320" cy="170" r="22" fill="{N}"/><path d="M180 232 h280" stroke="{T}" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>')
    D['padlock'] = (f'<rect x="170" y="62" width="180" height="170" rx="14" fill="{W}" stroke="{L}" stroke-width="3"/>'
        + ''.join(f'<rect x="194" y="{90+i*26}" width="{130-(i%2)*36}" height="9" rx="4.5" fill="#D2E0F1"/>' for i in range(5))
        + f'<path d="M398 120 v-26 a40 40 0 0 1 80 0 v26" fill="none" stroke="{N}" stroke-width="14" stroke-linecap="round"/>'
        + f'<rect x="378" y="118" width="120" height="100" rx="18" fill="{gid}"/><circle cx="438" cy="160" r="12" fill="{W}"/><rect x="433" y="164" width="10" height="26" rx="5" fill="{W}"/>')
    D['scales'] = (f'<rect x="312" y="70" width="16" height="160" rx="6" fill="{N}"/><rect x="250" y="226" width="140" height="18" rx="9" fill="{N}"/>'
        f'<path d="M180 86 L 460 70" stroke="{N}" stroke-width="10" stroke-linecap="round"/><circle cx="320" cy="78" r="14" fill="{N}"/>'
        f'<path d="M180 86 l-40 70 h80z" fill="none" stroke="{L}" stroke-width="3"/><path d="M460 70 l-40 70 h80z" fill="none" stroke="{L}" stroke-width="3"/>'
        f'<path d="M136 156 a44 22 0 0 0 88 0z" fill="{W}" stroke="{L}" stroke-width="3"/><path d="M416 140 a44 22 0 0 0 88 0z" fill="{gid}"/>'
        f'<rect x="150" y="126" width="22" height="22" rx="5" fill="#D2E0F1"/><rect x="176" y="118" width="22" height="30" rx="5" fill="#D2E0F1"/>')
    D['heart'] = (f'<path d="M320 238 C 240 190, 196 154, 196 116 a48 48 0 0 1 124 -22 a48 48 0 0 1 124 22 c0 38 -44 74 -124 122z" fill="{W}" stroke="{L}" stroke-width="3"/>'
        f'<path d="M222 146 h52 l16 -30 l24 58 l18 -38 l12 20 h76" fill="none" stroke="{gid}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    D['magnifier'] = (f'<rect x="150" y="60" width="270" height="170" rx="14" fill="{W}" stroke="{L}" stroke-width="3"/>'
        + ''.join(f'<rect x="{176+i*44}" y="{204-h}" width="28" height="{h}" rx="6" fill="#D2E0F1"/>' for i, h in enumerate([50, 80, 64, 104, 120]))
        + f'<circle cx="430" cy="118" r="58" fill="{W}" fill-opacity=".85" stroke="{N}" stroke-width="12"/><path d="M472 160 l50 50" stroke="{N}" stroke-width="16" stroke-linecap="round"/>'
        + f'<path d="M402 130 l20 -20 l14 12 l24 -26" fill="none" stroke="{gid}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    return D

ART_FOR_CATEGORY = {'practice': ['rings', 'stones', 'book', 'heart', 'puzzle'], 'policy-compliance': ['shield', 'clipboard', 'padlock', 'calendar'],
                    'leadership': ['bars', 'signpost', 'scales', 'target', 'magnifier'], 'inside-asend360': ['window', 'magnifier', 'target']}

def art(post, w=640, h=280):
    """Brand illustration: the post's own `art:` choice, or one picked from its topic's set."""
    seed = int(hashlib.md5(post['slug'].encode()).hexdigest(), 16)
    k = CAT_KEY[post['category']]
    bg = {'practice': ('#E3F5F3', '#C9EBE6'), 'policy-compliance': ('#E6EEF7', '#D2E0F1'),
          'leadership': ('#E9F1FB', '#D6E6F7'), 'inside-asend360': ('#E6EEF7', '#E3F5F3')}[k]
    gid = f'g{seed % 99999}'
    g = f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="#0381CA"/><stop offset=".5" stop-color="#08ACAC"/><stop offset="1" stop-color="#40CD70"/></linearGradient></defs>'
    D = _designs(f'url(#{gid})', seed)
    pool = ART_FOR_CATEGORY[k]
    name = post.get('art') if post.get('art') in D else pool[seed % len(pool)]
    dx, dy = (w - 640) / 2, (h - 280) / 2
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Illustration for {esc(post["category"])}" preserveAspectRatio="xMidYMid slice">{g}'
            f'<rect width="{w}" height="{h}" fill="{bg[0]}"/><circle cx="{w-60}" cy="30" r="120" fill="{bg[1]}"/><circle cx="40" cy="{h}" r="90" fill="{bg[1]}"/>'
            f'<g transform="translate({dx:.0f} {dy:.0f})">{D[name]}</g></svg>')

def picture(post, banner=False):
    """Use the post's own image if it has one, otherwise the brand illustration."""
    img = post.get('image')
    if img:
        alt = esc(post.get('image_alt', ''))
        pos = post.get('image_position', '50% 50%')
        return f'<img src="{img}" alt="{alt}" loading="{"eager" if banner else "lazy"}" decoding="async" style="object-position:{pos}">'
    return art(post, 960, 320) if banner else art(post)

def byline(p):
    meta = f"{fmt_long(p['dt'])} &middot; {icon('clock')} {p['mins']} min read"
    if p.get('author'):
        av = f'<img class="avatar" src="{p["author_photo"]}" alt="" width="44" height="44">' if p.get('author_photo') else ''
        tag = '<span class="guest-pill">Guest spot</span>' if p.get('guest') else ''
        return (f'<div class="byline">{av}<div><p class="by-name">{tag}By <b>{esc(p["author"])}</b>'
                f'{", " + esc(p["author_role"]) if p.get("author_role") else ""}</p><p class="art-meta">{meta}</p></div></div>')
    return f'<p class="art-meta">By Sean Lenahan, special school headteacher and founder of ASEND360 &middot; {meta}</p>'

def author_box(p):
    if not p.get('author'): return ''
    av = f'<img src="{p["author_photo"]}" alt="{esc(p["author"])}" width="88" height="88">' if p.get('author_photo') else ''
    link = f'<a href="{p["author_url"]}" rel="noopener">{esc(p.get("author_url_label") or p["author_url"])} {icon("arrow")}</a>' if p.get('author_url') else ''
    if p.get('author_url2'):
        link += f' <a href="{p["author_url2"]}" rel="noopener" style="margin-left:14px">{esc(p.get("author_url2_label") or p["author_url2"])} {icon("arrow")}</a>'
    return (f'<aside class="author-box">{av}<div><p class="eyebrow">About the author</p><h3>{esc(p["author"])}</h3>'
            f'<p class="role">{esc(p.get("author_role", ""))}</p><p>{esc(p.get("author_bio", ""))}</p>{link}</div></aside>')

# ---------- layout ----------
def icon(name):
    P = {'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>', 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
         'lock': '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
         'target': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/>',
         'doc': '<path d="M6 3h9l4 4v14H6z"/><path d="M14.5 3v4.5H19M9 13h6M9 17h4"/>',
         'team': '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-5.5 7-5.5s7 2 7 5.5M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.6c2.4.6 4 2.3 4 5.4"/>',
         'chart': '<path d="M4 20h16M7 16v-4M12 16V8M17 16v-7"/>', 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
         'rss': '<path d="M5 19a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16"/>', 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>'}
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{P[name]}</svg>'

NAV = [('/features', 'Features'), ('/compare', 'Compare'), ('/pricing', 'Pricing'), (BASE, 'Practice Exchange'), ('/security', 'Security'), ('/contact', 'Contact')]
SOLUTIONS = [('/send-management-software', 'SEND management software'), ('/ehcp-tracking-software', 'EHCP management and tracking'),
             ('/behaviour-recording-software', 'Behaviour recording and reporting'), ('/provision-mapping-software', 'Provision mapping'),
             ('/special-school-software', 'Special school software'), ('/attendance-analysis-software', 'Attendance analysis'),
             ('/pupil-premium-strategy-software', 'Pupil Premium strategy'), ('/single-central-record-software', 'Single Central Record'),
             ('/mis-integration', 'MIS integration (Wonde)')]
PLAUSIBLE = '<script defer data-domain="asend360.co.uk" src="https://plausible.io/js/script.js"></script>'
LI = 'https://www.linkedin.com/company/asend-360'; FB = 'https://www.facebook.com/people/ASEND-360/61593404010936/'

def page(path, title, desc, body, extra_head='', canonical=None, og_image=None, noindex=False):
    canonical = canonical or SITE + path
    links = ''.join(f'<a href="{h}"{" aria-current=page" if h == BASE else ""}>{t}</a>' for h, t in NAV)
    sol = '<details class="dd"><summary>Solutions</summary><div class="dd-menu">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in SOLUTIONS) + '</div></details>'
    links = links.replace('</a>', '</a>' + sol, 1)
    doc = f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">{"<meta name=robots content=noindex>" if noindex else ""}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{og_image or SITE + '/images/og-image.jpg'}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#003574"><link rel="icon" href="{BASE}favicon.ico" sizes="48x48"><link rel="icon" href="{BASE}favicon-32x32.png" type="image/png" sizes="32x32"><link rel="apple-touch-icon" href="{BASE}apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="The Practice Exchange" href="{BASE}feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap">
<link rel="stylesheet" href="{BASE}assets/px.css?v={VER}"><script src="{BASE}assets/px.js?v={VER}" defer></script>{PLAUSIBLE}{extra_head}</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap hdr-in"><a class="logo" href="/" aria-label="ASEND360 home"><picture><source srcset="{BASE}brand/asend360-logo-no-tagline-reversed.svg" media="(prefers-color-scheme: dark)"><img src="{BASE}brand/asend360-logo-no-tagline.svg" alt="" width="124" height="52"></picture></a>
<nav class="nav" id="nav" aria-label="Main">{links}</nav>
<div class="hdr-cta"><a class="btn ghost" href="https://app.asend360.co.uk">Sign in</a><a class="btn primary" href="/contact">Book a demo</a></div>
<button class="menu" type="button" aria-controls="nav" aria-expanded="false" aria-label="Open menu">{icon('menu')}</button></div></header>
<main id="main"{' data-limit=6' if path==BASE else ''}>{body}</main>
<footer class="ftr"><div class="wrap ftr-in"><div><picture><source srcset="{BASE}brand/asend360-logo-no-tagline-reversed.svg" media="(prefers-color-scheme: dark)"><img src="{BASE}brand/asend360-logo-no-tagline.svg" alt="ASEND360" width="150" height="63"></picture>
<p>Free, practical SEND and inclusion guidance from the team behind ASEND360.</p></div>
<nav aria-label="Footer"><a href="/">Home</a><a href="/features">Features</a><a href="/pricing">Pricing</a><a href="{BASE}">The Practice Exchange</a><a href="{BASE}articles/">Articles</a><a href="/privacy">Privacy</a><a href="/contact">Contact</a></nav>
<div class="social"><a href="{LI}" rel="noopener me" aria-label="ASEND360 on LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.95v5.66H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a><a href="{FB}" rel="noopener me" aria-label="ASEND360 on Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a><a href="{BASE}feed.xml" aria-label="RSS feed">{icon('rss')}</a></div></div>
<div class="wrap ftr-legal">&copy; {TODAY.year} ASEND360 Limited &middot; Registered in England and Wales, company no. 17492700 &middot; Registered office: 66 Paul Street, London, EC2A 4NA</div></footer>
</body></html>'''
    full = os.path.join(OUT, path.replace(BASE, '', 1).lstrip('/'))
    if full.endswith('/') or os.path.basename(full) == '': full = os.path.join(full, 'index.html')
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    open(full, 'w', encoding='utf-8').write(doc)

def card(p):
    sched = ' <span class="sched">Scheduled</span>' if p['dt'] > TODAY else ''
    return (f'<a class="card" href="{p["url"]}" data-cat="{CAT_KEY[p["category"]]}"><div class="card-art">{picture(p)}</div><div class="card-body">'
            f'<div class="card-top"><span class="tag t-{CAT_KEY[p["category"]]}">{p["category"]}</span><span class="date">{fmt(p["dt"])}{sched}</span></div>'
            + (f'<span class="guest-label">Guest spot &middot; {esc(p["author"])}</span>' if p.get('guest') and p.get('author') else '')
            + f'<h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p>'
            f'<div class="card-foot"><span class="read">{icon("clock")} {p["mins"]} min read</span><span class="go">{icon("arrow")}</span></div></div></a>')

FILTERS = '<div class="filters" role="group" aria-label="Filter by topic"><button type="button" class="on" data-cat="all" aria-pressed="true">All</button>' + ''.join(f'<button type="button" data-cat="{CAT_KEY[c]}" aria-pressed="false">{c}</button>' for c in CATS) + '</div>'
SUBSCRIBE = f'''<section class="wrap sub-box" id="subscribe"><span class="sub-ico">{icon('doc')}</span><div><p class="eyebrow">Stay up to date</p><h2>Get the latest from The Practice Exchange</h2><p>New articles twice a week. Follow us to see them first.</p></div>
<div class="sub-act"><a class="btn primary" href="{LI}" rel="noopener">Follow on LinkedIn</a><a class="btn ghost" href="{BASE}feed.xml">RSS feed</a></div></section>'''
EXPLORE = f'''<section class="explore"><div class="wrap explore-in"><div><p class="eyebrow light">Explore ASEND360</p><h2>The right support, at the right time</h2><p>See how one platform helps you track progress, stay compliant and make confident decisions &mdash; all in one place.</p><a class="btn light" href="/">Discover ASEND360 {icon('arrow')}</a></div>
<ul class="pillars"><li>{icon('target')}<b>Track</b><span>progress</span></li><li>{icon('doc')}<b>Stay</b><span>compliant</span></li><li>{icon('team')}<b>Support</b><span>your team</span></li><li>{icon('chart')}<b>Improve</b><span>outcomes</span></li></ul></div></section>'''
HERO_ART = '''<div class="hero-art" aria-hidden="true"><svg viewBox="0 0 420 420"><defs><linearGradient id="hg" x1="0" x2="1"><stop offset="0" stop-color="#0381CA"/><stop offset=".5" stop-color="#08ACAC"/><stop offset="1" stop-color="#40CD70"/></linearGradient></defs>
<circle cx="210" cy="210" r="200" fill="#0B4A8F"/><circle cx="210" cy="210" r="200" fill="none" stroke="url(#hg)" stroke-width="6" opacity=".9"/>''' + ''.join(
    f'<circle cx="{110+c*66}" cy="{120+r*66}" r="22" fill="#003574" stroke="#2A5B96" stroke-width="7"/>' +
    (f'<circle cx="{110+c*66}" cy="{120+r*66}" r="22" fill="none" stroke="url(#hg)" stroke-width="7" stroke-dasharray="{138*min(1,(r*4+c+1)/9):.0f} 140" transform="rotate(-90 {110+c*66} {120+r*66})"/>' if r*4+c < 10 else '')
    for r in range(4) for c in range(4)) + '''</svg><div class="quote">&ldquo;Small steps build lasting change.&rdquo;</div></div>'''

SEAN = {'@type': 'Person', 'name': 'Sean Lenahan', 'jobTitle': 'Headteacher', 'description': 'Serving special school headteacher and founder of ASEND360', 'url': SITE + '/'}
PUBLISHER = {'@type': 'Organization', 'name': 'ASEND360 Limited', 'url': SITE + '/', 'logo': {'@type': 'ImageObject', 'url': SITE + '/images/asend360-email-logo.png'}}

def build():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    shutil.copytree('static', OUT, dirs_exist_ok=True)
    # landing
    latest = ''.join(card(p) for p in LIVE[:6])
    allcards = ''.join(card(p) for p in LIVE)
    body = f'''<section class="hero"><div class="wrap hero-in"><div><p class="eyebrow light">ASEND360</p><h1>The Practice Exchange</h1>
<p class="hero-sub">Practical knowledge. Shared experience. Better outcomes.</p>
<p class="hero-lede">Articles, practical resources and perspectives from people working in SEND education &mdash; designed to support your day-to-day practice, inform your decisions and help you make progress, with or without the right tools.</p>
{FILTERS}</div>{HERO_ART}</div></section>
<section class="wrap latest"><div class="sec-head"><div><p class="eyebrow">Latest articles</p><h2>Practical ideas for real-world challenges</h2></div><a class="more" href="{BASE}articles/">View all articles {icon('arrow')}</a></div>
<div class="grid" id="grid">{allcards}</div><p class="empty" hidden>No articles in this topic yet &mdash; new ones are added twice a week.</p></section>
{SUBSCRIBE}{EXPLORE}'''
    page(BASE, 'The Practice Exchange: Free SEND Guidance | ASEND360',
         'Free, practical articles for UK schools on SEND practice, policy and compliance, and leadership, with new posts twice a week from ASEND360.', body,
         extra_head='<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'Blog', 'name': 'The Practice Exchange', 'url': SITE + BASE,
             'description': 'Free SEND and inclusion guidance for UK schools', 'inLanguage': 'en-GB', 'publisher': PUBLISHER,
             'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': SITE + p['url'], 'datePublished': p['date']} for p in LIVE if p['dt'] <= TODAY]}, ensure_ascii=False) + '</script>')
    # all articles
    body = f'''<section class="hero slim"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}">The Practice Exchange</a> › <span>All articles</span></nav><h1>All articles</h1>{FILTERS}</div></section>
<section class="wrap latest"><div class="grid" id="grid">{allcards}</div><p class="empty" hidden>No articles in this topic yet.</p></section>{SUBSCRIBE}'''
    page(BASE + 'articles/', 'All Articles | The Practice Exchange | ASEND360', 'Every article from The Practice Exchange: free, practical SEND and inclusion guidance for UK schools, from ASEND360.', body)
    # articles
    for p in LIVE:
        rel = [x for x in LIVE if x['slug'] != p['slug'] and x['category'] == p['category']][:2]
        rel += [x for x in LIVE if x['slug'] != p['slug'] and x not in rel][:3 - len(rel)]
        srcs = ''.join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in p['sources'])
        abox = author_box(p)
        promo = (f'<aside class="promo"><p class="eyebrow">How ASEND360 helps</p><h3>{esc(p["feature_title"])}</h3><p>{esc(p["feature_text"])}</p><a href="{p["feature_url"]}">Find out more {icon("arrow")}</a></aside>') if p.get('feature_title') else ''
        ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['summary'], 'datePublished': p['date'], 'dateModified': p.get('updated', p['date']),
              'articleSection': p['category'], 'inLanguage': 'en-GB', 'mainEntityOfPage': SITE + p['url'], 'image': (SITE + p['image']) if p.get('image', '').startswith('/') else p.get('image') or SITE + '/images/og-image.jpg',
              'author': ({'@type': 'Person', 'name': p['author'], 'jobTitle': p.get('author_role', ''), **({'url': p['author_url']} if p.get('author_url') else {})}
                         if p.get('author') else SEAN),
              'publisher': PUBLISHER}
        body = f'''<article><header class="art-hero"><div class="wrap narrow"><nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}">The Practice Exchange</a> › <span>{p['category']}</span></nav>
<span class="tag t-{CAT_KEY[p['category']]}">{p['category']}</span><h1>{esc(p['title'])}</h1><p class="art-lede">{esc(p['summary'])}</p>
{byline(p)}</div></header>
<div class="art-banner wrap narrow{' photo' if p.get('image') else ''}">{picture(p, banner=True)}</div>
<div class="wrap narrow prose">{p['html']}{abox}{promo}<p class="rel-sol">Explore: <a href="/send-management-software">SEND management software</a> &middot; <a href="/ehcp-tracking-software">EHCP management software</a> &middot; <a href="/special-school-software">special school software</a></p>{f'<h2>Sources</h2><ul class="sources">{srcs}</ul>' if srcs else ''}
<p class="disclaimer">General guidance for school staff, last reviewed {fmt_long(p['dt'])}. Statutory guidance changes, so always check the latest version on GOV.UK.</p></div></article>
<section class="wrap latest"><div class="sec-head"><div><p class="eyebrow">Keep reading</p><h2>More from The Practice Exchange</h2></div><a class="more" href="{BASE}articles/">All articles {icon('arrow')}</a></div><div class="grid">{''.join(card(x) for x in rel)}</div></section>{SUBSCRIBE}'''
        st = p.get('seo_title') or p['title']
        page(p['url'], st if len(st) > 49 else st + ' | ASEND360', p.get('seo_description') or p['summary'], body, extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>', og_image=((SITE + p['image']) if p.get('image', '').startswith('/') else p.get('image')))
    # feed + sitemap + 404
    items = ''.join(f'<item><title>{esc(p["title"])}</title><link>{SITE}{p["url"]}</link><guid>{SITE}{p["url"]}</guid><pubDate>{dt.datetime.combine(p["dt"], dt.time(7, 0)).strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate><category>{esc(p["category"])}</category><description>{esc(p["summary"])}</description></item>' for p in LIVE if p['dt'] <= TODAY)
    open(f'{OUT}/feed.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet type="text/xsl" href="{BASE}assets/feed.xsl"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>The Practice Exchange — ASEND360</title><link>{SITE}{BASE}</link><atom:link href="{SITE}{BASE}feed.xml" rel="self" type="application/rss+xml"/><description>Free SEND and inclusion guidance for UK schools</description><language>en-gb</language>{items}</channel></rss>\n')
    urls = [SITE + BASE, SITE + BASE + 'articles/'] + [SITE + p['url'] for p in LIVE if p['dt'] <= TODAY]
    open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    page(BASE + '404.html', 'Page not found | ASEND360', 'Page not found.', f'<section class="hero slim"><div class="wrap"><h1>Page not found</h1><p class="hero-lede">That article may have moved. <a href="{BASE}">Browse all articles</a>.</p></div></section>', noindex=True)
    print(f'built {len(LIVE)} of {len(POSTS)} posts ({"preview" if PREVIEW else "live"}) -> {OUT}/')

VER = hashlib.sha1(open('static/assets/px.css', 'rb').read() + open('static/assets/px.js', 'rb').read()).hexdigest()[:8] if os.path.exists('static/assets/px.css') else '1'
if __name__ == '__main__':
    build()
