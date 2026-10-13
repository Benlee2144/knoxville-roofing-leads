#!/usr/bin/env python3
"""Builds the generated pages of knoxvilleroofingquotes.com.

Run from anywhere:  python3 _build/build.py

- Location, county, service, hub, legal and blog pages are rendered from _build/data/*.json
  and _build/blog/*.html.
- The homepage (index.html) is hand-written; the build refreshes the blocks between
  <!-- shared:NAME --> ... <!-- /shared:NAME --> markers and the CSS/JS version.
- sitemap.xml and zips.json are regenerated.
GitHub Pages does not publish folders that start with "_", so this folder stays private.
"""
import hashlib
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, '_build')
SITE = 'https://knoxvilleroofingquotes.com'
BRAND = 'Knoxville Roofing Quotes'
GA_ID = 'G-RPJS68684E'
ADSENSE = 'ca-pub-5819445292295786'
FORMSPREE = 'https://formspree.io/f/xdeawzlj'
CONTACT_NAME = 'Ben Arp'
PHONE_DISPLAY = '(423) 920-4333'
PHONE_TEL = '+14239204333'
SMS_HREF = f'sms:{PHONE_TEL}?&body=' + 'Hi%20Ben%2C%20I%20need%20help%20with%20my%20roof.%20My%20ZIP%20is%20'
TODAY = date.today().isoformat()
YEAR = date.today().year


def load(name, default=None):
    path = os.path.join(BUILD, 'data', name)
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s), quote=True)


def write(rel_path, content):
    path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def asset_version():
    h = hashlib.sha1()
    for name in ('styles.css', 'script.js'):
        with open(os.path.join(ROOT, name), 'rb') as f:
            h.update(f.read())
    return h.hexdigest()[:10]


VERSION = asset_version()

# ---------------------------------------------------------------------------
# Icons (Lucide, ISC licence)
# ---------------------------------------------------------------------------

ICONS = {
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'map-pin': '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    'lock': '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    'hammer': '<path d="m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>',
    'house': '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    'cloud-lightning': '<path d="M6 16.326A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 .5 8.973"/><path d="m13 12-3 5h4l-3 5"/>',
    'clipboard-check': '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    'droplets': '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
    'building': '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    'arrow-left': '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    'arrow-right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'book-open': '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    'shield-check': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'phone-call': '<path d="M13 2a9 9 0 0 1 9 9"/><path d="M13 6a5 5 0 0 1 5 5"/><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>',
    'scale': '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    'layers': '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    'calculator': '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'menu': '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
    'x-circle': '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    'phone': '<path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>',
    'message': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
}


def icon(name, cls='icon'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# Site structure
# ---------------------------------------------------------------------------

SERVICES = [
    ('roof-replacement', 'Roof Replacement', 'house', 'Tear-off and new shingles or metal, with up to 3 quotes to compare.'),
    ('roof-repair', 'Roof Repair', 'hammer', 'Leaks, missing shingles, flashing, vent boots and worn spots.'),
    ('storm-damage-roof-repair', 'Storm & Hail Damage', 'cloud-lightning', 'Wind and hail inspections, repairs and photo documentation.'),
    ('roof-insurance-claims', 'Insurance Claims', 'clipboard-check', 'Roofers who know how to document damage for your adjuster.'),
    ('emergency-roof-repair', 'Emergency Repairs', 'alert', 'Active leaks, fallen trees and tarping after a storm.'),
    ('metal-roofing', 'Metal Roofing', 'layers', 'Standing seam and exposed-fastener metal for homes and barns.'),
    ('commercial-roofing', 'Commercial Roofing', 'building', 'Flat roofs, TPO, EPDM, coatings and metal for businesses.'),
]
SERVICE_NAMES = {s[0]: s[1] for s in SERVICES}

COUNTY_ORDER = ['knox-county', 'blount-county', 'anderson-county', 'loudon-county', 'sevier-county',
                'jefferson-county', 'roane-county', 'union-county', 'grainger-county', 'campbell-county', 'morgan-county']

PROJECT_OPTIONS = [
    ('Roof leak', 'droplets'),
    ('Storm / hail damage', 'cloud-lightning'),
    ('Roof replacement', 'house'),
    ('Roof repair', 'hammer'),
    ('Inspection', 'search'),
    ('Commercial roof', 'building'),
]

LOCATIONS = []
for name in ('existing.json', 'cities_a.json', 'cities_b.json', 'counties.json'):
    LOCATIONS += load(name, [])
LOC = {d['slug']: d for d in LOCATIONS}
SERVICE_DATA = {d['slug']: d for d in load('services.json', [])}
FACTS = load('facts.json', {})
POSTS = load('blog.json', [])
POST = {p['slug']: p for p in POSTS}


def county_slug_of(d):
    return d['county'].strip().lower().replace(' county', '').replace(' ', '-') + '-county'


# ---------------------------------------------------------------------------
# Shared partials
# ---------------------------------------------------------------------------

def jsonld(obj):
    return '    <script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + '\n    </script>'


def head(title, description, path, *, schema=(), og_type='website', noindex=False, ads=False,
         image='/images/og-image.jpg'):
    url = SITE + path
    robots = 'noindex, follow' if noindex else 'index, follow, max-image-preview:large'
    parts = [f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}');
    </script>
    <meta name="google-adsense-account" content="{ADSENSE}">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}">
    <meta name="robots" content="{robots}">
    <link rel="canonical" href="{url}">
    <meta name="theme-color" content="#FF8200">
    <meta property="og:site_name" content="{BRAND}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}{image}">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/svg+xml" href="/logo.svg">
    <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css?v={VERSION}">''']
    parts += [jsonld(s) for s in schema]
    if ads:
        parts.append(f'    <!-- Google AdSense -->\n    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>')
    parts.append('</head>')
    return '\n'.join(parts)


NAV = [('/roof-replacement/', 'Roof Replacement'), ('/storm-damage-roof-repair/', 'Storm Damage'),
       ('/service-areas/', 'Service Areas'), ('/roof-cost-calculator/', 'Cost Calculator')]
MOBILE_NAV = NAV + [('/blog/', 'Homeowner Guides'), ('/contact/', 'Contact')]


def header(cta_href='#quote'):
    links = '\n'.join(f'                    <a href="{h}">{t}</a>' for h, t in NAV)
    mobile_links = '\n'.join(f'                        <a href="{h}">{t}</a>' for h, t in MOBILE_NAV)
    return f'''    <!-- shared:header -->
    <header class="header">
        <div class="container header-content">
            <a href="/" class="logo">
                <img src="/logo.svg" alt="" class="logo-icon-img" width="45" height="45">
                <div class="logo-text">
                    <span class="logo-name">{BRAND}</span>
                    <span class="logo-tagline">Compare Local Contractors Free</span>
                </div>
            </a>
            <nav class="site-nav" aria-label="Main">
{links}
            </nav>
            <div class="header-right">
                <a href="tel:{PHONE_TEL}" class="header-phone" aria-label="Call or text {PHONE_DISPLAY}">{icon('phone')}<span>{PHONE_DISPLAY}</span></a>
                <a href="{cta_href}" class="btn-primary header-cta">Get Free Quotes</a>
                <details class="mobile-nav">
                    <summary aria-label="Menu">{icon('menu')}</summary>
                    <div class="mobile-nav-panel">
{mobile_links}
                        <a href="tel:{PHONE_TEL}" class="mobile-nav-phone">{icon('phone')}Call {PHONE_DISPLAY}</a>
                        <a href="{SMS_HREF}" class="mobile-nav-phone">{icon('message')}Text {PHONE_DISPLAY}</a>
                    </div>
                </details>
            </div>
        </div>
    </header>
    <!-- /shared:header -->'''


def footer():
    services = '\n'.join(f'                    <a href="/{s}/">{n}</a>' for s, n, _, _ in SERVICES)
    counties = '\n'.join(f'                    <a href="/{c}/">{esc(LOC[c]["name"])}</a>' for c in COUNTY_ORDER if c in LOC)
    return f'''    <!-- shared:footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="logo">
                        <img src="/logo.svg" alt="" class="logo-icon-img" width="45" height="45">
                        <div class="logo-text">
                            <span class="logo-name">{BRAND}</span>
                            <span class="logo-tagline">Compare Local Contractors Free</span>
                        </div>
                    </a>
                    <p class="footer-description">A free service that connects East Tennessee homeowners and businesses with up to 3 licensed, insured local roofing contractors. No cost, no obligation.</p>
                    <p class="footer-phone">Questions? Call or text {CONTACT_NAME}:<br><a href="tel:{PHONE_TEL}">{icon('phone')}{PHONE_DISPLAY}</a></p>
                    <a href="/#quote" class="btn-primary">Get Free Quotes</a>
                </div>
                <div class="footer-col">
                    <h4>Roofing Services</h4>
{services}
                </div>
                <div class="footer-col">
                    <h4>Service Areas</h4>
                    <a href="/">Knoxville</a>
{counties}
                    <a href="/service-areas/">All service areas</a>
                </div>
                <div class="footer-col">
                    <h4>Resources</h4>
                    <a href="/roof-cost-calculator/">Roof Cost Calculator</a>
                    <a href="/compare-roofing-quotes/">Quote Comparison Worksheet</a>
                    <a href="/blog/">Homeowner Guides</a>
                    <a href="/how-it-works/">How It Works</a>
                    <a href="/contact/">Contact</a>
                    <a href="/privacy/">Privacy Policy</a>
                    <a href="/terms/">Terms &amp; Consent</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {YEAR} {BRAND}. All rights reserved.</p>
                <p class="footer-legal">{BRAND} is a free referral service, not a roofing contractor. We may receive compensation from the independent contractors in our network. Always verify a contractor's license and insurance before hiring.</p>
            </div>
        </div>
    </footer>
    <!-- /shared:footer -->'''


def floating_cta(quote_href='#quote'):
    return f'''    <!-- shared:floating -->
    <div class="floating-cta">
        <a href="tel:{PHONE_TEL}" class="floating-action" data-loc="floating">{icon('phone')}<span>Call</span></a>
        <a href="{SMS_HREF}" class="floating-action" data-loc="floating">{icon('message')}<span>Text</span></a>
        <a href="{quote_href}" class="floating-btn">Get Free Quotes</a>
    </div>
    <!-- /shared:floating -->'''


def hero_phone():
    return (f'                <!-- shared:herophone -->\n                <p class="hero-phone">Prefer to talk? Call or text {CONTACT_NAME} at '
            f'<a href="tel:{PHONE_TEL}" data-loc="hero">{PHONE_DISPLAY}</a></p>\n                <!-- /shared:herophone -->')


def scripts():
    return f'    <script src="/script.js?v={VERSION}" defer></script>\n</body>\n</html>\n'


def breadcrumbs(items):
    """items: [(name, path), ...] ending with the current page."""
    links = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            links.append(f'<span aria-current="page">{esc(name)}</span>')
        else:
            links.append(f'<a href="{path}">{esc(name)}</a>')
    nav = ('    <nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container">'
           + '<span class="crumb-sep">/</span>'.join(links) + '</div></nav>')
    schema = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p}
                            for i, (n, p) in enumerate(items)],
    }
    return nav, schema


def pills(name, options):
    out = []
    for i, (value, label) in enumerate(options):
        req = ' required' if i == 0 else ''
        out.append(f'<label class="pill"><input type="radio" name="{name}" value="{value}"{req}><span>{label}</span></label>')
    return '\n                                    '.join(out)


def lead_form(source, location, zip_hint, preselect=None, title='Get Your Free Quotes'):
    if preselect:
        assert preselect in dict(PROJECT_OPTIONS), preselect
    tiles = '\n                                '.join(
        f'<label class="option-tile"><input type="radio" name="project" value="{v}"{" required" if i == 0 else ""}'
        f'{" checked" if v == preselect else ""}><span class="option-body">{icon(ic)}<span>{v}</span></span></label>'
        for i, (v, ic) in enumerate(PROJECT_OPTIONS))
    timeframe = pills('timeframe', [('Emergency - ASAP', 'ASAP / emergency'), ('Within 1 week', 'Within a week'),
                                    ('Within 1 month', 'Within a month'), ('Just planning', 'Just planning')])
    owner = pills('owner', [('Owner', 'Yes, I own it'), ('Property manager', 'I manage it'), ('Renter', 'No, I rent')])
    claim = pills('insurance_claim', [('Yes', 'Yes'), ('No', 'No'), ('Not sure', 'Not sure')]).replace(' required', '')
    preselect_attr = f' data-preselect="{esc(preselect)}"' if preselect else ''
    return f'''            <!-- shared:form -->
            <div class="hero-form-wrapper" id="quote">
                <div class="form-card">
                    <div class="form-header">
                        <div class="form-badge">100% FREE</div>
                        <h2 class="form-title">{esc(title)}</h2>
                        <p class="form-subtitle">Takes less than 60 seconds</p>
                    </div>
                    <form id="leadForm" class="lead-form" action="{FORMSPREE}" method="POST"{preselect_attr}>
                        <div class="form-progress" aria-hidden="true"><span class="form-progress-bar"></span></div>
                        <p class="form-step-count" aria-live="polite">1st down &middot; Step 1 of 3</p>

                        <fieldset class="form-step is-active" data-step="1">
                            <legend class="step-title">What do you need help with?</legend>
                            <div class="option-grid">
                                {tiles}
                            </div>
                        </fieldset>

                        <fieldset class="form-step" data-step="2">
                            <legend class="step-title">Tell us about the property</legend>
                            <div class="form-group">
                                <label for="zip">Property ZIP code</label>
                                <input type="text" id="zip" name="zip" inputmode="numeric" autocomplete="postal-code" pattern="[0-9]{{5}}" placeholder="{zip_hint}" required>
                                <p class="zip-hint" aria-live="polite"></p>
                            </div>
                            <div class="form-group">
                                <span class="group-label" id="timeframe-label">How soon do you need it?</span>
                                <div class="pill-group" role="radiogroup" aria-labelledby="timeframe-label">
                                    {timeframe}
                                </div>
                            </div>
                            <div class="form-group">
                                <span class="group-label" id="owner-label">Do you own the property?</span>
                                <div class="pill-group" role="radiogroup" aria-labelledby="owner-label">
                                    {owner}
                                </div>
                                <p class="renter-hint" hidden>No problem. Roofers will need the owner's OK before any work, so loop in your landlord or property manager.</p>
                            </div>
                            <div class="form-group">
                                <span class="group-label" id="claim-label">Insurance claim? <span class="optional">(optional)</span></span>
                                <div class="pill-group" role="radiogroup" aria-labelledby="claim-label">
                                    {claim}
                                </div>
                            </div>
                            <button type="button" class="submit-btn step-next"><span class="btn-text">Continue</span>{icon('arrow-right', 'icon btn-arrow')}</button>
                        </fieldset>

                        <fieldset class="form-step" data-step="3">
                            <legend class="step-title">Last step: where should we send your quotes?</legend>
                            <div class="form-group">
                                <label for="name">Full name</label>
                                <input type="text" id="name" name="name" autocomplete="name" placeholder="Your name" required>
                            </div>
                            <div class="form-group">
                                <label for="phone">Phone number</label>
                                <input type="tel" id="phone" name="phone" autocomplete="tel" inputmode="tel" placeholder="(865) 555-1234" required>
                            </div>
                            <div class="form-group">
                                <label for="email">Email <span class="optional">(optional)</span></label>
                                <input type="email" id="email" name="email" autocomplete="email" placeholder="you@example.com">
                            </div>
                            <div class="form-group">
                                <label for="details">Anything roofers should know? <span class="optional">(optional)</span></label>
                                <textarea id="details" name="details" rows="2" placeholder="e.g. leak over the kitchen, two-story, metal roof"></textarea>
                            </div>
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input type="checkbox" name="consent" value="yes" required>
                                    <span class="checkbox-text">I agree to be contacted by phone, text, or email by up to 3 roofing contractors about this project. Consent is not a condition of purchase. <a href="/terms/#consent" target="_blank" rel="noopener">Terms</a></span>
                                </label>
                            </div>
                            <button type="submit" class="submit-btn"><span class="btn-text">Get My Free Quotes</span>{icon('arrow-right', 'icon btn-arrow')}</button>
                            <p class="form-error" role="alert" hidden></p>
                        </fieldset>

                        <button type="button" class="step-back" hidden>{icon('arrow-left')}Back</button>

                        <input type="hidden" name="source" value="{esc(source)}">
                        <input type="hidden" name="location" value="{esc(location)}">
                        <input type="hidden" name="_subject" value="New roofing lead - {esc(location)}">
                        <input type="hidden" name="page" value="">
                        <input type="hidden" name="timestamp" value="">
                        <input type="hidden" name="referrer" value="">
                        <input type="hidden" name="utm" value="">
                        <input type="text" name="_gotcha" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">

                        <p class="form-privacy">{icon('lock')}Only shared with the roofers matched to your project. No spam.</p>
                    </form>
                </div>
            </div>
            <!-- /shared:form -->'''


def proof_bar():
    items = [('$0', 'Cost to you'), ('Up to 3', 'Local quotes'), ('60 sec', 'To request'), ('No', 'Obligation to hire')]
    inner = '\n                <div class="proof-divider"></div>\n'.join(
        f'                <div class="proof-item">\n                    <div class="proof-number">{n}</div>\n'
        f'                    <div class="proof-label">{l}</div>\n                </div>' for n, l in items)
    return f'''    <section class="social-proof-bar">
        <div class="container">
            <div class="proof-items">
{inner}
            </div>
        </div>
    </section>'''


def hero(badge, h1, subtitle, features, form_html, extra_class=''):
    feats = '\n'.join(f'''                    <div class="hero-feature">
                        <span class="feature-check">{icon('check')}</span>
                        <span>{esc(f)}</span>
                    </div>''' for f in features)
    h1_html = esc(h1)
    for phrase in ('Free Roofing Quotes', 'Roofing Quotes', 'Free Quotes'):
        if phrase in h1_html:
            h1_html = h1_html.replace(phrase, f'<span class="highlight">{phrase}</span>', 1)
            break
    return f'''    <section class="hero {extra_class}">
        <div class="hero-overlay"></div>
        <div class="container hero-content">
            <div class="hero-text">
                <div class="hero-badge">
                    <span class="badge-icon">{icon('map-pin')}</span>
                    <span>{esc(badge)}</span>
                </div>
                <h1 class="hero-title">{h1_html}</h1>
                <p class="hero-subtitle">{esc(subtitle)}</p>
                <div class="hero-features">
{feats}
                </div>
{hero_phone()}
            </div>
{form_html}
        </div>
    </section>'''


def faq_section(faqs, title='Frequently Asked Questions'):
    items = '\n'.join(f'''                <details class="faq-accordion"{" open" if i == 0 else ""}>
                    <summary>{esc(f["q"])}</summary>
                    <p>{esc(f["a"])}</p>
                </details>''' for i, f in enumerate(faqs))
    html_ = f'''    <section class="faq-section">
        <div class="container narrow">
            <div class="section-header">
                <span class="section-badge">COMMON QUESTIONS</span>
                <h2 class="section-title">{esc(title)}</h2>
            </div>
            <div class="faq-list">
{items}
            </div>
        </div>
    </section>'''
    schema = {'@context': 'https://schema.org', '@type': 'FAQPage',
              'mainEntity': [{'@type': 'Question', 'name': f['q'],
                              'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in faqs]}
    return html_, schema


GENERAL_FAQS = [
    {'q': 'Is this service really free?',
     'a': 'Yes. Homeowners never pay us anything. Roofing contractors in our network pay a referral fee, and you are under no obligation to hire any of them.'},
    {'q': 'How many roofers will contact me?',
     'a': 'Up to 3. We match your request with local, licensed and insured roofers who handle your type of project, so you can compare quotes without calling around.'},
    {'q': 'Can I call or text instead of filling out the form?',
     'a': f'Yes. Call or text {CONTACT_NAME} at {PHONE_DISPLAY} with your address and what is going on with your roof, and your request will be passed to local roofers who serve your area. If no one picks up, leave a voicemail or send a text.'},
]


def services_grid(place=None):
    cards = '\n'.join(f'''                <a href="/{slug}/" class="service-link-card">
                    <span class="service-link-icon">{icon(ic)}</span>
                    <span class="service-link-text"><strong>{name}</strong><span>{blurb}</span></span>
                </a>''' for slug, name, ic, blurb in SERVICES)
    title = f'Roofing Services in {esc(place)}' if place else 'Roofing Services We Can Quote'
    return f'''    <section class="services-links-section">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">WHAT YOU CAN GET QUOTES FOR</span>
                <h2 class="section-title">{title}</h2>
            </div>
            <div class="service-link-grid">
{cards}
            </div>
        </div>
    </section>'''


def cost_snapshot(place, image='roof-before-after',
                  caption='Illustration: a worn asphalt roof next to the same house after a full shingle replacement.'):
    costs = FACTS.get('site_costs') or {}
    rows = [('Architectural asphalt shingles', 'architectural_per_sqft'),
            ('3-tab asphalt shingles', 'asphalt_3tab_per_sqft'),
            ('Metal, exposed fastener', 'metal_exposed_fastener_per_sqft'),
            ('Metal, standing seam', 'metal_standing_seam_per_sqft'),
            ('Flat roof (TPO)', 'flat_tpo_per_sqft')]
    body = []
    for label, key in rows:
        rng = costs.get(key)
        if not rng:
            continue
        life = costs['lifespans'][key]
        body.append(f'<tr><td>{label}</td><td>${rng[0]:.2f} - ${rng[1]:.2f}</td><td>{esc(life)}</td></tr>')
    if not body:
        return ''
    figure = illustration(image, caption)
    return f'''    <section class="cost-section">
        <div class="container cost-layout">
            <div>
                <span class="section-badge">BUDGETING</span>
                <h2 class="section-title left">What a New Roof Costs Around {esc(place)}</h2>
                <p class="section-lead">Typical installed prices per square foot of roof area, based on published Tennessee and national cost guides. Your quotes will depend on roof size, pitch, layers to tear off and the material you pick.</p>
                <div class="table-wrap">
                    <table class="data-table">
                        <thead><tr><th>Material</th><th>Installed cost / sq ft</th><th>Typical lifespan</th></tr></thead>
                        <tbody>
                            {"".join(body)}
                        </tbody>
                    </table>
                </div>
                <a href="/roof-cost-calculator/" class="text-link">{icon('calculator')} Estimate your roof in 30 seconds</a>
            </div>
{figure}
        </div>
    </section>'''


def illustration(name, caption, cls='illustration'):
    return f'''            <figure class="{cls}">
                <picture>
                    <source media="(max-width: 700px)" srcset="/images/{name}-640.webp">
                    <img src="/images/{name}.webp" alt="{esc(caption)}" width="1200" height="800" loading="lazy" decoding="async">
                </picture>
                <figcaption>{esc(caption)}</figcaption>
            </figure>''' if name == 'roof-before-after' else f'''            <figure class="{cls}">
                <img src="/images/{name}.webp" alt="{esc(caption)}" width="750" height="900" loading="lazy" decoding="async">
                <figcaption>{esc(caption)}</figcaption>
            </figure>'''


def final_cta(text_place):
    return f'''    <section class="final-cta-section">
        <div class="container">
            <div class="final-cta-content">
                <h2>Ready to Compare Roofing Quotes{" in " + esc(text_place) if text_place else ""}?</h2>
                <p>Tell us about your roof once and get up to 3 free quotes from licensed local roofers. No cost, no obligation.</p>
                <div class="final-cta-buttons">
                    <a href="#quote" class="btn-primary btn-large">Get Free Quotes {icon('arrow-right')}</a>
                </div>
                <p class="final-cta-note">{icon('clock')}Roofers usually reach out within 24-48 hours</p>
            </div>
        </div>
    </section>'''


def prose(paragraphs_sections, intro=None):
    out = []
    if intro:
        out.append(f'<p class="lead">{esc(intro)}</p>')
    for s in paragraphs_sections:
        out.append(f'<h2>{esc(s["heading"])}</h2>')
        out += [f'<p>{esc(p)}</p>' for p in s['body']]
    return '\n                '.join(out)


def link_tags(slugs):
    return ''.join(f'<a class="area-link" href="/{s}/">{icon("map-pin")}{esc(LOC[s]["name"])}</a>' for s in slugs if s in LOC)


def org_schema():
    return {
        '@context': 'https://schema.org', '@type': 'Organization', 'name': BRAND, 'url': SITE + '/',
        'logo': SITE + '/images/apple-touch-icon.png',
        'description': 'Free roofing quote referral service for Knoxville and East Tennessee.',
        'telephone': PHONE_TEL,
        'founder': {'@type': 'Person', 'name': CONTACT_NAME},
        'contactPoint': {'@type': 'ContactPoint', 'telephone': PHONE_TEL, 'contactType': 'customer service',
                         'areaServed': 'US-TN', 'availableLanguage': 'English'},
        'areaServed': ['Knoxville, TN'] + [LOC[c]['full_name'] for c in COUNTY_ORDER if c in LOC],
    }


def service_schema(name, area, path, description):
    return {
        '@context': 'https://schema.org', '@type': 'Service', 'name': name, 'serviceType': name,
        'description': description, 'url': SITE + path,
        'provider': {'@type': 'Organization', 'name': BRAND, 'url': SITE + '/'},
        'areaServed': area if isinstance(area, list) else [area],
    }


# ---------------------------------------------------------------------------
# Location + county pages
# ---------------------------------------------------------------------------

def location_page(d):
    slug, name = d['slug'], d['name']
    path = f'/{slug}/'
    is_county = d['kind'] == 'county'
    cslug = county_slug_of(d)
    crumbs = [('Home', '/'), ('Service Areas', '/service-areas/')]
    if not is_county and cslug in LOC:
        crumbs.append((LOC[cslug]['name'], f'/{cslug}/'))
    crumbs.append((name, path))
    crumb_html, crumb_schema = breadcrumbs(crumbs)

    faqs = d['faqs'] + GENERAL_FAQS
    faq_html, faq_schema = faq_section(faqs, f'Roofing Questions from {name} Homeowners')

    form = lead_form(f'{BRAND} - {name}', d['full_name'], d['zip'], title=f'Get {name} Roofing Quotes'
                     if len(name) <= 16 else 'Get Your Free Quotes')
    features = [f'Roofers who work in {name}', 'Licensed & insured contractors', 'Free, no-obligation estimates']

    areas = ''.join(f'<li>{esc(a)}</li>' for a in d.get('areas_served', []))
    notes = ''.join(f'<li>{icon("check")}<span>{esc(n)}</span></li>' for n in d.get('roofing_notes', []))
    zips = ', '.join(d.get('zips', []))
    aside = f'''            <aside class="content-aside">
                <div class="aside-card">
                    <h3>{'Communities' if is_county else 'Areas'} we cover{' in ' + esc(name) if not is_county else ''}</h3>
                    <ul class="tag-list">{areas}</ul>
                    {f'<p class="aside-meta">ZIP codes: {esc(zips)}</p>' if zips else ''}
                </div>
                <div class="aside-card">
                    <h3>Roofing in {esc(name)}: what to know</h3>
                    <ul class="check-list">{notes}</ul>
                </div>
                <a href="#quote" class="btn-primary btn-block">Get Free {esc(name)} Quotes</a>
            </aside>'''

    towns = ''
    if is_county:
        linked = [s for s in d.get('cities_in_county', []) if s in LOC]
        other = d.get('towns_in_county', [])
        towns = f'''    <section class="towns-section">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">TOWNS &amp; COMMUNITIES</span>
                <h2 class="section-title">Roofing Quotes Across {esc(name)}</h2>
            </div>
            <div class="area-link-grid">{link_tags(linked)}{''.join(f'<span class="area-link plain">{esc(t)}</span>' for t in other)}</div>
        </div>
    </section>'''

    nearby = [s for s in d.get('nearby', []) if s in LOC and s != slug]
    if not is_county and cslug in LOC and cslug not in nearby:
        nearby.append(cslug)
    nearby_html = f'''    <section class="nearby-section">
        <div class="container">
            <h2 class="nearby-title">Nearby Areas We Serve</h2>
            <div class="area-link-grid">{link_tags(nearby)}<a class="area-link" href="/">{icon("map-pin")}Knoxville</a></div>
        </div>
    </section>'''

    service = service_schema('Roofing quote matching', d['full_name'], path, d['meta_description'])
    page = [
        head(d['title'], d['meta_description'], path, schema=[service, faq_schema, crumb_schema]),
        '<body>',
        header(),
        hero(d['badge'], d['h1'], d['hero_subtitle'], features, form, 'location-hero'),
        crumb_html,
        proof_bar(),
        f'''    <section class="content-section">
        <div class="container content-layout">
            <div class="prose">
                {prose(d['sections'], d['intro'])}
            </div>
{aside}
        </div>
    </section>''',
        towns,
        services_grid(name),
        cost_snapshot(name),
        faq_html,
        nearby_html,
        final_cta(name),
        footer(),
        floating_cta(),
        scripts(),
    ]
    write(f'{slug}/index.html', '\n'.join(p for p in page if p))


# ---------------------------------------------------------------------------
# Service pages
# ---------------------------------------------------------------------------

def service_page(d):
    slug = d['slug']
    path = f'/{slug}/'
    crumb_html, crumb_schema = breadcrumbs([('Home', '/'), ('Roofing Services', '/#services'), (d['name'], path)])
    extra = [] if any('free' in f['q'].lower() for f in d['faqs']) else GENERAL_FAQS[:1]
    faq_html, faq_schema = faq_section(d['faqs'] + extra, f'{d["name"]} Questions')
    form = lead_form(f'{BRAND} - {d["name"]}', 'Knoxville, TN', '37919', preselect=d['project_value'],
                     title=f'Get {d["name"]} Quotes' if len(d['name']) <= 18 else 'Get Your Free Quotes')
    features = ['Up to 3 quotes from local roofers', 'Licensed & insured contractors', 'Free, no-obligation estimates']

    checklist = ''.join(f'<li>{icon("check")}<span>{esc(c)}</span></li>' for c in d.get('checklist', []))
    related = ''.join(f'<li><a href="/blog/{p}/">{esc(POST[p]["h1"])}</a></li>' for p in d.get('related_posts', []) if p in POST)
    aside = f'''            <aside class="content-aside">
                <div class="aside-card">
                    <h3>Before you sign: checklist</h3>
                    <ul class="check-list">{checklist}</ul>
                </div>
                {f'<div class="aside-card"><h3>Related guides</h3><ul class="link-list">{related}</ul></div>' if related else ''}
                <a href="#quote" class="btn-primary btn-block">Compare {esc(d["name"])} Quotes</a>
            </aside>'''

    table = ''
    ct = d.get('cost_table')
    if ct:
        head_cells = ''.join(f'<th>{esc(c)}</th>' for c in ct['columns'])
        rows = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in ct['rows'])
        table = f'''    <section class="cost-section">
        <div class="container narrow">
            <span class="section-badge">COSTS</span>
            <h2 class="section-title left">{esc(d["name"])} Costs Around Knoxville</h2>
            <p class="section-lead">{esc(ct["caption"])}</p>
            <div class="table-wrap">
                <table class="data-table"><thead><tr>{head_cells}</tr></thead><tbody>{rows}</tbody></table>
            </div>
            <p class="table-note">Rough ranges for planning only. Every roof is different, which is why comparing written quotes matters.</p>
            <a href="/roof-cost-calculator/" class="text-link">{icon('calculator')} Estimate your roof in 30 seconds</a>
        </div>
    </section>'''

    figure = ''
    if slug in ('roof-replacement', 'storm-damage-roof-repair', 'roof-repair', 'roof-insurance-claims'):
        figure = f'''    <section class="illustration-section">
        <div class="container narrow">
{illustration('roof-before-after', 'Illustration: weathered, storm-worn shingles compared with a newly replaced roof on the same house.')}
        </div>
    </section>'''

    counties = link_tags([c for c in COUNTY_ORDER if c in LOC])
    areas = f'''    <section class="nearby-section">
        <div class="container">
            <h2 class="nearby-title">{esc(d["name"])} Quotes Across East Tennessee</h2>
            <div class="area-link-grid"><a class="area-link" href="/">{icon("map-pin")}Knoxville</a>{counties}</div>
        </div>
    </section>'''

    area_names = ['Knoxville, TN'] + [LOC[c]['full_name'] for c in COUNTY_ORDER if c in LOC]
    page = [
        head(d['title'], d['meta_description'], path,
             schema=[service_schema(d['name'], area_names, path, d['meta_description']), faq_schema, crumb_schema]),
        '<body>',
        header(),
        hero(d['badge'], d['h1'], d['hero_subtitle'], features, form, 'service-hero'),
        crumb_html,
        proof_bar(),
        f'''    <section class="content-section">
        <div class="container content-layout">
            <div class="prose">
                {prose(d['sections'], d['intro'])}
            </div>
{aside}
        </div>
    </section>''',
        figure,
        table,
        faq_html,
        areas,
        final_cta(None),
        footer(),
        floating_cta(),
        scripts(),
    ]
    write(f'{slug}/index.html', '\n'.join(p for p in page if p))


# ---------------------------------------------------------------------------
# Simple content pages (hub, legal, calculator, blog)
# ---------------------------------------------------------------------------

def simple_page(path, title, description, h1, intro, body_html, *, crumbs=None, schema=(), noindex=False,
                ads=False, cta=True, og_type='website'):
    crumb_html, crumb_schema = breadcrumbs(crumbs or [('Home', '/'), (h1, path)])
    page = [
        head(title, description, path, schema=list(schema) + [crumb_schema], noindex=noindex, ads=ads, og_type=og_type),
        '<body>',
        header('/#quote'),
        crumb_html,
        f'''    <section class="page-hero">
        <div class="container narrow">
            <h1>{esc(h1)}</h1>
            {f'<p class="page-intro">{intro}</p>' if intro else ''}
        </div>
    </section>''',
        body_html,
        cta_band() if cta else '',
        footer(),
        floating_cta('/#quote'),
        scripts(),
    ]
    write(path.strip('/') + '/index.html' if path != '/404.html' else '404.html', '\n'.join(p for p in page if p))


def cta_band(text=None):
    text = text or 'Ready to compare quotes from local roofers?'
    return f'''    <section class="cta-band">
        <div class="container cta-band-inner">
            <div>
                <h2>{esc(text)}</h2>
                <p>Free, no obligation, and it takes about a minute.</p>
            </div>
            <a href="/#quote" class="btn-primary btn-large">Get Free Quotes {icon('arrow-right')}</a>
        </div>
    </section>'''


def service_areas_page():
    blocks = []
    for c in COUNTY_ORDER:
        if c not in LOC:
            continue
        d = LOC[c]
        cities = [s for s in d.get('cities_in_county', []) if s in LOC]
        if c == 'knox-county':
            cities = ['__knoxville'] + cities
        links = ''.join('<a class="area-link" href="/">' + icon('map-pin') + 'Knoxville</a>' if s == '__knoxville'
                        else f'<a class="area-link" href="/{s}/">{icon("map-pin")}{esc(LOC[s]["name"])}</a>' for s in cities)
        towns = ''.join(f'<span class="area-link plain">{esc(t)}</span>' for t in d.get('towns_in_county', []))
        blocks.append(f'''            <div class="county-block">
                <h2><a href="/{c}/">{esc(d["name"])}</a></h2>
                <p>{esc(d["intro"])}</p>
                <div class="area-link-grid">{links}{towns}</div>
            </div>''')
    body = f'''    <section class="content-section">
        <div class="container narrow">
{chr(10).join(blocks)}
        </div>
    </section>'''
    simple_page('/service-areas/', 'Roofing Service Areas | Knoxville & East Tennessee Counties',
                'Free roofing quotes across Knox, Blount, Anderson, Loudon, Sevier, Jefferson, Roane and nearby counties. Find your town and compare up to 3 local roofers.',
                'Roofing Service Areas', 'We connect homeowners and businesses across Knoxville and the surrounding East Tennessee counties with licensed local roofers. Pick your county or town below.',
                body, schema=[org_schema()])


def blog_index_page():
    groups = {}
    for p in POSTS:
        groups.setdefault(p['category'], []).append(p)
    order = ['Costs & Planning', 'Storm Damage & Insurance', 'Maintenance & Repairs', 'Roofing Materials', 'Hiring a Roofer', 'Commercial Roofing']
    sections = []
    for cat in order:
        cards = ''.join(f'''
                <a href="/blog/{p["slug"]}/" class="guide-card">
                    <span class="guide-icon">{icon("book-open")}</span>
                    <h3>{esc(p["h1"])}</h3>
                    <p>{esc(p["description"])}</p>
                    <span class="guide-link">Read the guide {icon("arrow-right")}</span>
                </a>''' for p in groups.get(cat, []))
        sections.append(f'''            <h2 class="guide-group-title">{esc(cat)}</h2>
            <div class="guides-grid">{cards}
            </div>''')
    body = f'''    <section class="content-section">
        <div class="container">
{chr(10).join(sections)}
        </div>
    </section>'''
    simple_page('/blog/', 'Roofing Guides for Knoxville Homeowners | Costs & Repairs',
                'Plain-English roofing guides for East Tennessee: replacement costs, storm and hail damage, insurance claims, materials, maintenance and hiring a roofer.',
                'Homeowner Roofing Guides', 'Straight answers about roof costs, storm damage, insurance claims, materials and hiring a roofer in East Tennessee.',
                body, schema=[{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Homeowner Roofing Guides', 'url': SITE + '/blog/'}])


# High-intent guides: no display ads, so readers aren't sent to competitors' ads.
NO_ADS = {'roof-replacement-cost-knoxville', 'storm-damage-insurance-claim', 'emergency-roof-tarp',
          'when-to-repair-leaking-roof', 'signs-you-need-new-roof', 'roof-repair-vs-replacement', 'hail-damage-what-to-know',
          'best-roofers-knoxville'}


def blog_post(p):
    slug = p['slug']
    path = f'/blog/{slug}/'
    with open(os.path.join(BUILD, 'blog', f'{slug}.html'), encoding='utf-8') as f:
        body = f.read()
    body = '\n'.join('                ' + l if l else '' for l in body.split('\n'))
    crumb_html, crumb_schema = breadcrumbs([('Home', '/'), ('Guides', '/blog/'), (p['h1'], path)])
    article = {
        '@context': 'https://schema.org', '@type': 'Article', 'headline': p['h1'], 'description': p['description'],
        'datePublished': p['date'], 'dateModified': p.get('modified', p['date']),
        'author': {'@type': 'Organization', 'name': BRAND, 'url': SITE + '/'},
        'publisher': {'@type': 'Organization', 'name': BRAND, 'logo': {'@type': 'ImageObject', 'url': SITE + '/images/apple-touch-icon.png'}},
        'mainEntityOfPage': SITE + path, 'image': SITE + '/images/og-image.jpg',
    }
    svc = p['service']
    related = [q for q in POSTS if q['category'] == p['category'] and q['slug'] != slug][:3]
    if len(related) < 3:
        related += [q for q in POSTS if q['slug'] != slug and q not in related][:3 - len(related)]
    rel_cards = ''.join(f'''
                <a href="/blog/{q["slug"]}/" class="guide-card">
                    <span class="guide-icon">{icon("book-open")}</span>
                    <h3>{esc(q["h1"])}</h3>
                    <span class="guide-link">Read the guide {icon("arrow-right")}</span>
                </a>''' for q in related)
    page = [
        head(p['title'], p['description'], path, schema=[article, crumb_schema], og_type='article', ads=slug not in NO_ADS),
        '<body>',
        header('/#quote'),
        crumb_html,
        f'''    <main class="post">
        <div class="container post-layout">
            <article class="prose post-body">
                <p class="post-category">{esc(p["category"])}</p>
                <h1>{esc(p["h1"])}</h1>
                <p class="post-meta">Updated {esc(p.get("modified_label", p["date_label"]))} &middot; {p["read_minutes"]} min read &middot; By the {BRAND} team</p>
{body}
            </article>
            <aside class="post-aside">
                <div class="aside-card sticky-card">
                    <h3>Get up to 3 free roofing quotes</h3>
                    <ul class="check-list">
                        <li>{icon("check")}<span>Licensed &amp; insured local roofers</span></li>
                        <li>{icon("check")}<span>Free, no obligation</span></li>
                        <li>{icon("check")}<span>Takes about a minute</span></li>
                    </ul>
                    <a href="/{svc}/#quote" class="btn-primary btn-block">Get Free Quotes</a>
                    <a href="/roof-cost-calculator/" class="text-link small">{icon("calculator")} Roof cost calculator</a>
                </div>
            </aside>
        </div>
    </main>''',
        f'''    <section class="guides-section">
        <div class="container">
            <h2 class="guide-group-title">Keep reading</h2>
            <div class="guides-grid">{rel_cards}
            </div>
        </div>
    </section>''',
        cta_band(f'Need {SERVICE_NAMES.get(svc, "roofing").lower()} quotes?' if svc in SERVICE_NAMES else None),
        footer(),
        floating_cta(f'/{svc}/#quote'),
        scripts(),
    ]
    write(f'blog/{slug}/index.html', '\n'.join(x for x in page if x))


# ---------------------------------------------------------------------------
# Homepage shared blocks, sitemap, zips
# ---------------------------------------------------------------------------

HOME_FAQS = [
    {'q': 'How much does a new roof cost in Knoxville, TN?',
     'a': 'Most Knoxville-area roof replacements fall somewhere between $8,000 and $25,000, depending on the size of the home, the material and how complex the roof is. Asphalt shingles are the most affordable option, while metal costs more but lasts longer. Try our roof cost calculator for a quick estimate, then compare written quotes.'},
    {'q': 'Do Knoxville roofers give free estimates?',
     'a': 'Most local roofers offer a free inspection and written estimate for roof replacements and storm damage. Some charge for small diagnostic visits or detailed reports, so ask up front. When you request quotes through us, the roofers you are matched with provide free estimates and there is no obligation to hire.'},
    {'q': 'Is this roofing quote service really free?',
     'a': 'Yes. The service is 100% free for homeowners. We connect you with up to 3 licensed, insured roofing contractors who provide free estimates, and there is no obligation to hire anyone. Contractors pay us a fee for the introduction.'},
    {'q': 'How quickly will I hear from roofers?',
     'a': 'Roofers usually reach out within 24-48 hours of your request. For emergencies like an active leak or storm damage, choose "ASAP / emergency" in the form so they know it is urgent.'},
    {'q': 'How do I know if I need a roof repair or a full replacement?',
     'a': 'A few missing shingles, a small leak or localized damage can usually be repaired. A roof that is 20 or more years old, has widespread damage, sagging, multiple leaks or daylight showing through the decking usually needs replacing. Roofers can inspect and tell you which makes sense.'},
    {'q': 'Will my homeowners insurance cover roof damage?',
     'a': 'Most policies cover damage from sudden events such as hail, wind, fallen trees or fire, but not normal wear and tear or lack of maintenance. Document the damage with dated photos and have a roofer inspect it before or while you file a claim.'},
    {'q': 'What roofing materials are best for Tennessee weather?',
     'a': 'Architectural asphalt shingles are the most popular choice in East Tennessee because they balance cost and durability. Metal roofing is growing in popularity for its long lifespan and energy efficiency, especially on cabins and rural homes. Flat commercial roofs usually use TPO or EPDM.'},
    {'q': 'How do I check that a roofer is licensed in Tennessee?',
     'a': 'Search the contractor on the State of Tennessee license lookup at verify.tn.gov. Roofing jobs of $25,000 or more require a state contractor license, and in Knox County residential jobs from $3,000 to $24,999 require a state Home Improvement license. Also ask for proof of liability insurance sent directly from their agent.'},
    {'q': 'Can I talk to a person instead of filling out the form?',
     'a': f'Yes. Call or text {CONTACT_NAME} at {PHONE_DISPLAY}. Share your address and what is going on with your roof, and your request will be passed to local roofers who serve your area. If no one picks up, leave a voicemail or send a text.'},
    {'q': 'Which areas do you serve?',
     'a': 'Knoxville and the surrounding East Tennessee counties, including Knox, Blount, Anderson, Loudon, Sevier, Jefferson, Roane, Union, Grainger, Campbell and Morgan. See our service areas page for every town we cover.'},
]


def areas_block():
    groups = []
    for c in COUNTY_ORDER:
        if c not in LOC:
            continue
        d = LOC[c]
        cities = [s for s in d.get('cities_in_county', []) if s in LOC]
        links = ''.join(f'<a href="/{s}/">{esc(LOC[s]["name"])}</a>' for s in cities)
        groups.append(f'''                <div class="area-group">
                    <h3><a href="/{c}/">{esc(d["name"])}</a></h3>
                    <div class="area-group-links">{'<a href="/">Knoxville</a>' if c == 'knox-county' else ''}{links}</div>
                </div>''')
    return f'''    <section class="areas-section" id="areas">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">SERVICE AREAS</span>
                <h2 class="section-title">Roofing Quotes Across East Tennessee</h2>
                <p class="section-subtitle">Pick your county or town to see local roofing information</p>
            </div>
            <div class="area-groups">
{chr(10).join(groups)}
            </div>
            <div class="center"><a href="/service-areas/" class="text-link">See all service areas {icon('arrow-right')}</a></div>
        </div>
    </section>'''


def refresh_shared(rel_path, form_args=None, home=False):
    path = os.path.join(ROOT, rel_path)
    with open(path, encoding='utf-8') as f:
        t = f.read()
    blocks = {'header': header(), 'footer': footer()}
    if form_args:
        blocks['form'] = lead_form(**form_args)
    if home:
        faq_html, faq_schema = faq_section(HOME_FAQS)
        blocks['homefaq'] = faq_html + '\n' + jsonld(faq_schema)
        blocks['services'] = services_grid().replace('class="services-links-section"', 'class="services-links-section" id="services"')
        blocks['areas'] = areas_block()
        blocks['orgschema'] = jsonld(org_schema())
        blocks['floating'] = floating_cta()
        blocks['herophone'] = hero_phone()
        blocks['costs'] = cost_snapshot('Knoxville', image='shingle-before-after',
                                        caption='Illustration: weathered, streaked shingles compared with new architectural shingles.')
    for name, content in blocks.items():
        pattern = re.compile(rf'[ \t]*<!-- shared:{name} -->.*?<!-- /shared:{name} -->', re.S)
        if pattern.search(t):
            if '<!-- shared:' not in content:
                content = f'    <!-- shared:{name} -->\n{content}\n    <!-- /shared:{name} -->'
            t = pattern.sub(lambda m: content, t)
    t = re.sub(r'styles\.css\?v=[\w]+', f'styles.css?v={VERSION}', t)
    t = re.sub(r'script\.js\?v=[\w]+', f'script.js?v={VERSION}', t)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)


def sitemap():
    urls = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(('.', '_')) and d not in ('images', 'thank-you')]
        if 'index.html' in filenames:
            rel = os.path.relpath(dirpath, ROOT)
            path = '/' if rel == '.' else f'/{rel}/'
            with open(os.path.join(dirpath, 'index.html'), encoding='utf-8') as f:
                if 'noindex' in f.read(3000):
                    continue
            urls.append(path)
    def prio(p):
        if p == '/':
            return '1.0'
        if p.startswith('/blog/') and p != '/blog/':
            return '0.6'
        return '0.8'
    urls.sort(key=lambda p: (p != '/', p.startswith('/blog/'), p))
    entries = '\n'.join(f'  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio(p)}</priority>\n  </url>' for p in urls)
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n')
    return len(urls)


def zips_json():
    zips = {}
    for d in sorted(LOCATIONS, key=lambda d: d['kind'] == 'county'):
        for z in d.get('zips', []):
            zips.setdefault(z, d['name'])
    write('zips.json', json.dumps(zips, separators=(',', ':'), sort_keys=True))


def main():
    for d in LOCATIONS:
        location_page(d)
    for d in SERVICE_DATA.values():
        service_page(d)
    for p in POSTS:
        blog_post(p)
    if POSTS:
        blog_index_page()
    if LOCATIONS:
        service_areas_page()
    import pages  # noqa: E402  (hub/legal/calculator pages live in pages.py)
    pages.build(globals())
    refresh_shared('index.html', form_args={'source': BRAND, 'location': 'Knoxville, TN', 'zip_hint': '37919'}, home=True)
    zips_json()
    n = sitemap()
    print(f'built {len(LOCATIONS)} locations, {len(SERVICE_DATA)} services, {len(POSTS)} posts; sitemap {n} urls; assets v={VERSION}')


if __name__ == '__main__':
    import sys
    sys.path.insert(0, BUILD)
    main()
