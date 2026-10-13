(function () {
    const mapEl = document.getElementById('roofer-map');
    const dataEl = document.getElementById('roofer-data');
    if (!mapEl || !dataEl || !window.L) return;

    const roofers = JSON.parse(dataEl.textContent);
    const search = document.getElementById('roofer-q');
    const countySel = document.getElementById('roofer-county');
    const serviceSel = document.getElementById('roofer-service');
    const countEl = document.getElementById('roofer-count');
    const cards = Array.from(document.querySelectorAll('.roofer-list-section .roofer-card'));
    const groups = Array.from(document.querySelectorAll('.roofer-county'));
    const emptyEl = document.querySelector('.roofer-empty');

    const LABELS = {
        residential: 'Residential', commercial: 'Commercial', metal: 'Metal roofing', repair: 'Repairs',
        storm: 'Storm damage', gutters: 'Gutters', flat: 'Flat roofs'
    };

    const map = L.map(mapEl, { scrollWheelZoom: false }).setView([35.98, -83.95], 9);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    map.on('focus click', () => map.scrollWheelZoom.enable());

    const pin = L.divIcon({ className: 'roofer-pin', html: '<span></span>', iconSize: [28, 36], iconAnchor: [14, 34], popupAnchor: [0, -30] });
    const cluster = L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 42 });
    map.addLayer(cluster);

    function el(tag, attrs, text) {
        const node = document.createElement(tag);
        Object.entries(attrs || {}).forEach(([k, v]) => node.setAttribute(k, v));
        if (text) node.textContent = text;
        return node;
    }

    function popup(r) {
        const box = el('div', { class: 'roofer-popup' });
        box.appendChild(el('strong', {}, r.name));
        box.appendChild(el('span', { class: 'roofer-popup-city' }, `${r.city}, ${r.county} County`));
        if (r.services && r.services.length) {
            box.appendChild(el('span', { class: 'roofer-popup-services' }, r.services.map(s => LABELS[s] || s).join(' · ')));
        }
        const links = el('span', { class: 'roofer-popup-links' });
        if (r.phone) {
            const digits = r.phone.replace(/\D/g, '').slice(-10);
            links.appendChild(el('a', { href: `tel:+1${digits}`, 'data-roofer': r.name }, r.phone));
        }
        if (r.website) {
            links.appendChild(el('a', { href: r.website, target: '_blank', rel: 'nofollow noopener', 'data-roofer': r.name }, 'Website'));
        }
        box.appendChild(links);
        box.appendChild(el('a', { href: '#quote', class: 'roofer-popup-cta' }, 'Get up to 3 free quotes'));
        return box;
    }

    const markers = roofers.map(r => {
        const m = L.marker([r.lat, r.lon], { icon: pin, title: r.name, alt: r.name });
        m.bindPopup(() => popup(r));
        m.roofer = r;
        return m;
    });
    const byName = new Map(markers.map(m => [m.roofer.name, m]));

    function matches(r, q, county, service) {
        if (county && r.county !== county) return false;
        if (service && !(r.services || []).includes(service)) return false;
        if (q && !`${r.name} ${r.city}`.toLowerCase().includes(q)) return false;
        return true;
    }

    function apply(fit) {
        const q = search.value.trim().toLowerCase();
        const county = countySel.value;
        const service = serviceSel.value;
        const visible = markers.filter(m => matches(m.roofer, q, county, service));
        cluster.clearLayers();
        cluster.addLayers(visible);

        const shown = new Set(visible.map(m => m.roofer.name));
        cards.forEach(c => { c.hidden = !shown.has(c.querySelector('h3').textContent); });
        groups.forEach(gr => { gr.hidden = !gr.querySelector('.roofer-card:not([hidden])'); });
        if (emptyEl) emptyEl.hidden = visible.length > 0;
        countEl.textContent = `${visible.length} roofer${visible.length === 1 ? '' : 's'}`;

        if (fit && visible.length) {
            map.fitBounds(L.latLngBounds(visible.map(m => m.getLatLng())).pad(0.2), { maxZoom: 12 });
        }
    }

    // Allow links like /roofers/?county=Blount or ?q=maryville
    const params = new URLSearchParams(window.location.search);
    if (params.get('county')) countySel.value = params.get('county');
    if (params.get('q')) search.value = params.get('q');
    if (params.get('service')) serviceSel.value = params.get('service');
    apply(Boolean(params.get('county') || params.get('q') || params.get('service')));

    let typing;
    search.addEventListener('input', () => { clearTimeout(typing); typing = setTimeout(() => apply(true), 200); });
    countySel.addEventListener('change', () => apply(true));
    serviceSel.addEventListener('change', () => apply(true));

    document.querySelectorAll('.roofer-locate').forEach(btn => {
        btn.addEventListener('click', () => {
            const m = byName.get(btn.dataset.name);
            if (!m) return;
            mapEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            cluster.zoomToShowLayer(m, () => m.openPopup());
        });
    });

    document.addEventListener('click', (e) => {
        const link = e.target.closest('a[data-roofer]');
        if (!link || typeof gtag !== 'function') return;
        gtag('event', link.href.startsWith('tel:') ? 'roofer_phone_click' : 'roofer_site_click', { roofer: link.dataset.roofer });
    });
})();
