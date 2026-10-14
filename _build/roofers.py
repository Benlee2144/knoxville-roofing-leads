"""East Tennessee roofer directory: map page, get-listed page, and per-location roofer lists."""
import hashlib
import json
import os
from urllib.parse import urlparse

SERVICE_LABELS = {
    'residential': 'Residential', 'commercial': 'Commercial', 'metal': 'Metal roofing', 'repair': 'Repairs',
    'storm': 'Storm damage', 'gutters': 'Gutters', 'flat': 'Flat roofs',
}


def load(g):
    path = os.path.join(g['BUILD'], 'data', 'roofers.json')
    if not os.path.exists(path):
        return []
    with open(os.path.join(g['BUILD'], 'data', 'tn_places.json')) as f:
        places = json.load(f)
    with open(path, encoding='utf-8') as f:
        raw = json.load(f)
    out = []
    for r in raw:
        coords = places.get(r['city'].strip().lower())
        if not coords:
            print(f"  roofers: no coordinates for city {r['city']!r} ({r['name']}), skipped")
            continue
        # Pins sit near the city centre (business addresses are often homes), spread a little so they don't stack.
        h = hashlib.md5(r['name'].encode('utf-8')).digest()
        out.append({**r, 'lat': round(coords[0] + (h[0] / 255 - 0.5) * 0.014, 5),
                    'lon': round(coords[1] + (h[1] / 255 - 0.5) * 0.018, 5)})
    return sorted(out, key=lambda r: (r['county'], r['city'], r['name'].lower()))


def domain(url):
    return urlparse(url).netloc.replace('www.', '') if url else ''


def card(g, r, compact=False):
    esc, icon = g['esc'], g['icon']
    tags = ''.join(f'<span class="roofer-tag">{SERVICE_LABELS[s]}</span>' for s in r.get('services', []) if s in SERVICE_LABELS)
    phone = (f'<a class="roofer-phone" href="tel:+1{"".join(c for c in r["phone"] if c.isdigit())[-10:]}" data-roofer="{esc(r["name"])}">'
             f'{icon("phone")}{esc(r["phone"])}</a>') if r.get('phone') else ''
    site = (f'<a class="roofer-site" href="{esc(r["website"])}" target="_blank" rel="nofollow noopener" data-roofer="{esc(r["name"])}">'
            f'{esc(domain(r["website"]))} {icon("arrow-right")}</a>') if r.get('website') else ''
    locate = '' if compact else f'<button type="button" class="roofer-locate" data-name="{esc(r["name"])}">{icon("map-pin")}Show on map</button>'
    return f'''<article class="roofer-card" data-county="{esc(r["county"])}" data-services="{esc(" ".join(r.get("services", [])))}" data-search="{esc((r["name"] + " " + r["city"]).lower())}">
                    <h3>{esc(r["name"])}</h3>
                    <p class="roofer-city">{icon("map-pin")}{esc(r["city"])}, {esc(r["county"])} County</p>
                    <div class="roofer-tags">{tags}</div>
                    <div class="roofer-links">{phone}{site}{locate}</div>
                </article>'''


def location_block(g, roofers, d):
    """Roofers based in a city (or county) for a location page."""
    if not roofers:
        return ''
    esc = g['esc']
    county = d['county'].strip()
    if d['kind'] == 'county':
        local = [r for r in roofers if r['county'].lower() == county.lower()]
        heading = f'Roofing Companies in {esc(d["name"])}'
    else:
        local = [r for r in roofers if r['city'].lower() == d['name'].lower()]
        heading = f'Roofing Companies Based in {esc(d["name"])}'
        if len(local) < 3:
            local += [r for r in roofers if r['county'].lower() == county.lower() and r not in local]
            heading = f'Roofing Companies In and Near {esc(d["name"])}'
    if not local:
        return ''
    shown = local[:9]
    cards = '\n'.join('                ' + card(g, r, compact=True) for r in shown)
    return f'''    <section class="local-roofers-section">
        <div class="container">
            <div class="section-header">
                <span class="section-badge">LOCAL ROOFERS</span>
                <h2 class="section-title">{heading}</h2>
                <p class="section-subtitle">Compiled from each company's own website. Want quotes without calling around? <a href="#quote">Let us match you with up to 3</a>.</p>
            </div>
            <div class="roofer-grid">
{cards}
            </div>
            <div class="center"><a class="text-link" href="/roofers/?county={esc(county)}">See all {len([r for r in roofers if r['county'].lower() == county.lower()])} roofers in {esc(county)} County on the map {g['icon']('arrow-right')}</a></div>
        </div>
    </section>'''


def map_page(g, roofers):
    esc, icon, site = g['esc'], g['icon'], g['SITE']
    counties = sorted({r['county'] for r in roofers})
    n = len(roofers)
    data = json.dumps([{k: r.get(k) for k in ('name', 'city', 'county', 'phone', 'website', 'services', 'lat', 'lon')} for r in roofers],
                      separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')
    county_opts = ''.join(f'<option value="{esc(c)}">{esc(c)} County</option>' for c in counties)
    service_opts = ''.join(f'<option value="{k}">{v}</option>' for k, v in SERVICE_LABELS.items())
    groups = []
    for c in counties:
        cards = '\n'.join('                ' + card(g, r) for r in roofers if r['county'] == c)
        groups.append(f'''            <div class="roofer-county" data-county="{esc(c)}">
                <h2 class="roofer-county-title">Roofing Companies in {esc(c)} County</h2>
                <div class="roofer-grid">
{cards}
                </div>
            </div>''')
    form = g['lead_form'](f'{g["BRAND"]} - Roofer Map', 'Knoxville, TN', '37919', title='Get Matched with Up to 3 Roofers')
    crumb_html, crumb_schema = g['breadcrumbs']([('Home', '/'), ('Roofer Map', '/roofers/')])
    collection = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'East Tennessee Roofer Map',
                  'url': site + '/roofers/', 'about': 'Roofing companies in Knoxville and East Tennessee'}
    extra_head = ('    <link rel="stylesheet" href="/vendor/leaflet/leaflet.css">\n'
                  '    <link rel="stylesheet" href="/vendor/markercluster/MarkerCluster.css">\n'
                  '    <link rel="stylesheet" href="/vendor/markercluster/MarkerCluster.Default.css">')
    title = 'Roofing Companies Map: Knoxville & East Tennessee Roofers'
    desc = (f'Browse {n} roofing companies across Knoxville and East Tennessee on one free map, with websites, '
            f'phone numbers and services. Or get matched with up to 3 roofers.')[:160]
    body = f'''    <section class="page-hero">
        <div class="container narrow">
            <h1>East Tennessee Roofer Map</h1>
            <p class="page-intro">{n} roofing companies across Knoxville and the surrounding counties, all on one map. Click a pin for each company's website, phone and services, or <a href="#quote">let us match you with up to 3 licensed roofers</a> for free.</p>
        </div>
    </section>
{crumb_html}
    <section class="map-section">
        <div class="container">
            <div class="map-filters" role="search">
                <input type="search" id="roofer-q" placeholder="Search by company or town" aria-label="Search roofers">
                <select id="roofer-county" aria-label="County"><option value="">All counties</option>{county_opts}</select>
                <select id="roofer-service" aria-label="Service"><option value="">All services</option>{service_opts}</select>
                <span class="map-count" id="roofer-count" aria-live="polite">{n} roofers</span>
            </div>
            <div id="roofer-map" class="roofer-map" role="region" aria-label="Map of roofing companies"></div>
            <p class="map-note">Pins show each company's town, not its exact address. Listings come from each company's own website, checked {g['TODAY']}. Being listed isn't an endorsement, and listed companies aren't necessarily part of our referral network. Always <a href="/how-it-works/#verify">verify a roofer's license</a>.</p>
        </div>
    </section>
    <section class="roofer-list-section">
        <div class="container">
{chr(10).join(groups)}
            <p class="roofer-empty" hidden>No roofers match those filters. Try a different town or service.</p>
        </div>
    </section>
    <section class="form-section">
        <div class="container hero-content">
            <div class="form-section-text">
                <span class="section-badge">SKIP THE PHONE CALLS</span>
                <h2 class="section-title left">Not sure who to call?</h2>
                <p class="section-lead">Tell us about your roof once and up to 3 licensed, insured local roofers will reach out with free estimates. No cost, no obligation.</p>
                <ul class="check-list">
                    <li>{icon('check')}<span>Matched to your town and type of project</span></li>
                    <li>{icon('check')}<span>Compare written quotes side by side</span></li>
                    <li>{icon('check')}<span>Or call or text {g['CONTACT_NAME']} at {g['PHONE_DISPLAY']}</span></li>
                </ul>
            </div>
{form}
        </div>
    </section>
    <section class="cta-band">
        <div class="container cta-band-inner">
            <div>
                <h2>Own a roofing company?</h2>
                <p>Add your business, fix your details, or grab a free badge for your website.</p>
            </div>
            <a href="/roofers/get-listed/" class="btn-primary btn-large">Get Listed Free {icon('arrow-right')}</a>
        </div>
    </section>
    <script type="application/json" id="roofer-data">{data}</script>'''
    page = [
        g['head'](title, desc, '/roofers/', schema=[collection, crumb_schema], extra_head=extra_head),
        '<body>', g['header'](), body, g['footer'](), g['floating_cta'](),
        '    <script src="/vendor/leaflet/leaflet.js" defer></script>',
        '    <script src="/vendor/markercluster/leaflet.markercluster.js" defer></script>',
        f'    <script src="/roofer-map.js?v={g["VERSION"]}" defer></script>',
        g['scripts'](),
    ]
    g['write']('roofers/index.html', '\n'.join(page))


def get_listed_page(g):
    esc, icon, site = g['esc'], g['icon'], g['SITE']
    snippet = (f'<a href="{site}/roofers/" title="East Tennessee Roofer Map">'
               f'<img src="{site}/images/roofer-map-badge.svg" alt="Find us on the East Tennessee Roofer Map" width="240" height="80"></a>')
    body = f'''    <section class="content-section">
        <div class="container narrow">
            <div class="getlisted-grid">
                <div class="prose">
                    <h2>Add or update your listing</h2>
                    <p>The <a href="/roofers/">East Tennessee Roofer Map</a> lists roofing companies across Knoxville and the surrounding counties, with each company's town, phone, website and services. Listing is free. Use this form to add your company, correct your details, or ask us to remove a listing.</p>
                    <form class="contact-form" action="{g['FORMSPREE']}" method="POST">
                        <div class="form-group"><label for="gl-type">What do you need?</label>
                            <select id="gl-type" name="request"><option>Add my company</option><option>Update my listing</option><option>Remove my listing</option></select></div>
                        <div class="form-group"><label for="gl-company">Company name</label><input id="gl-company" name="company" required></div>
                        <div class="form-group"><label for="gl-site">Website</label><input id="gl-site" name="website" type="url" placeholder="https://"></div>
                        <div class="form-group"><label for="gl-phone">Business phone</label><input id="gl-phone" name="business_phone" type="tel"></div>
                        <div class="form-group"><label for="gl-city">Town</label><input id="gl-city" name="town" placeholder="e.g. Maryville"></div>
                        <div class="form-group"><label for="gl-email">Your email</label><input id="gl-email" name="email" type="email" required></div>
                        <div class="form-group"><label for="gl-notes">Services or notes</label><textarea id="gl-notes" name="message" rows="3" placeholder="Residential, commercial, metal, storm damage..."></textarea></div>
                        <input type="hidden" name="_subject" value="Roofer map listing request">
                        <input type="text" name="_gotcha" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
                        <button type="submit" class="submit-btn"><span class="btn-text">Send Request</span></button>
                    </form>
                    <h2>Want more jobs from us?</h2>
                    <p>We also connect homeowners with licensed, insured roofers through our free quote service. If you'd like to receive roofing leads in your area, call or text {g['CONTACT_NAME']} at <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>.</p>
                </div>
                <aside class="aside-card badge-card">
                    <h3>Free badge for your website</h3>
                    <p>Show customers where to find you. Copy this code into your site's footer or "about" page.</p>
                    <img src="/images/roofer-map-badge.svg" alt="Find us on the East Tennessee Roofer Map" width="240" height="80">
                    <textarea class="badge-code" readonly rows="5" aria-label="Badge HTML code">{esc(snippet)}</textarea>
                    <button type="button" class="btn-outline btn-block badge-copy">Copy code</button>
                    <p class="aside-meta">Free, whether or not you add it. Your listing stays the same either way.</p>
                </aside>
            </div>
        </div>
    </section>'''
    g['simple_page']('/roofers/get-listed/', f'Get Your Roofing Company Listed | East Tennessee Roofer Map',
                     'Add your roofing company to the free East Tennessee Roofer Map, update your details, or grab a free "Find us on the map" badge for your website.',
                     'Get Your Roofing Company Listed', 'Free listings for East Tennessee roofing companies.', body,
                     crumbs=[('Home', '/'), ('Roofer Map', '/roofers/'), ('Get Listed', '/roofers/get-listed/')], cta=False)


BADGE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="80" viewBox="0 0 240 80" role="img" aria-label="Find us on the East Tennessee Roofer Map">
  <defs><pattern id="c" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#fff"/><rect width="5" height="5" fill="#FF8200"/><rect x="5" y="5" width="5" height="5" fill="#FF8200"/></pattern></defs>
  <rect width="240" height="80" rx="12" fill="#1C1C1C"/>
  <rect x="0" y="0" width="240" height="10" fill="url(#c)"/>
  <rect x="0" y="0" width="240" height="80" rx="12" fill="none" stroke="#FF8200" stroke-width="2"/>
  <g transform="translate(14 22)">
    <path d="M18 2L2 15h5v13h22V15h5L18 2z" fill="#FF8200"/>
    <rect x="15" y="18" width="6" height="10" fill="#1C1C1C"/>
  </g>
  <text x="62" y="38" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" fill="#FF8200" letter-spacing="1.5">FIND US ON THE</text>
  <text x="62" y="56" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="#ffffff">East Tennessee</text>
  <text x="62" y="71" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="#ffffff">Roofer Map</text>
</svg>
'''


def ticker(g, roofers):
    """Scrolling strip of roofer names (names only; logos need each company's permission)."""
    if not roofers:
        return ''
    esc, icon = g['esc'], g['icon']
    from urllib.parse import quote
    ordered = sorted(roofers, key=lambda r: hashlib.md5(r['name'].encode('utf-8')).hexdigest())
    dot = '<span class="ticker-dot" aria-hidden="true"></span>'

    def run(hidden):
        attrs = ' tabindex="-1"' if hidden else ''
        return dot.join(f'<a href="/roofers/?q={quote(r["name"])}"{attrs}>{esc(r["name"])}</a>' for r in ordered) + dot

    return f'''    <!-- shared:ticker -->
    <section class="roofer-ticker" aria-label="Roofing companies on our East Tennessee Roofer Map">
        <a class="ticker-label" href="/roofers/">{icon('map-pin')}<span>{len(roofers)} local roofers on our map</span></a>
        <div class="ticker-viewport">
            <div class="ticker-track">
                <div class="ticker-run">{run(False)}</div>
                <div class="ticker-run" aria-hidden="true">{run(True)}</div>
            </div>
        </div>
    </section>
    <!-- /shared:ticker -->'''


def build(g):
    roofers = load(g)
    with open(os.path.join(g['ROOT'], 'images', 'roofer-map-badge.svg'), 'w') as f:
        f.write(BADGE_SVG)
    if roofers:
        map_page(g, roofers)
        get_listed_page(g)
    return roofers
