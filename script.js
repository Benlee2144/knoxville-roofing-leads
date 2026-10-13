document.addEventListener('DOMContentLoaded', function() {
    initLeadForm();
    initScrollAnimations();
    initPhoneFormatting();
    initZipInput();
    initSmoothScroll();
    initFloatingCta();
    initThankYouTracking();
    initCostCalculator();
    initContactTracking();
});

// =============================================
// MULTI-STEP LEAD FORM
// =============================================

const DOWNS = ['1st down', '2nd down', '3rd down'];

function initLeadForm() {
    const form = document.getElementById('leadForm');
    if (!form) return;

    const steps = Array.from(form.querySelectorAll('.form-step'));
    const backBtn = form.querySelector('.step-back');
    const counter = form.querySelector('.form-step-count');
    const bar = form.querySelector('.form-progress-bar');
    let current = 0;

    // Without JS every step stays visible and native validation applies.
    form.classList.add('is-stepped');
    form.noValidate = true;

    const timestamp = form.querySelector('[name="timestamp"]');
    if (timestamp) timestamp.value = new Date().toISOString();
    const page = form.querySelector('[name="page"]');
    if (page) page.value = window.location.pathname;
    const referrer = form.querySelector('[name="referrer"]');
    if (referrer) referrer.value = document.referrer;
    const utm = form.querySelector('[name="utm"]');
    if (utm) {
        const params = new URLSearchParams(window.location.search);
        utm.value = ['utm_source', 'utm_medium', 'utm_campaign', 'gclid']
            .filter(k => params.get(k)).map(k => `${k}=${params.get(k)}`).join('&');
    }
    const renterHint = form.querySelector('.renter-hint');

    function show(index, focus = true) {
        current = index;
        steps.forEach((step, i) => step.classList.toggle('is-active', i === index));
        if (backBtn) backBtn.hidden = index === 0;
        if (counter) counter.textContent = `${DOWNS[index] || ''} \u00b7 Step ${index + 1} of ${steps.length}`;
        if (bar) bar.style.width = `${((index + 1) / steps.length) * 100}%`;
        if (focus && index > 0) {
            const first = steps[index].querySelector('input:not([type="radio"]):not([type="checkbox"])');
            if (first && window.matchMedia('(min-width: 769px)').matches) first.focus({ preventScroll: true });
        }
    }

    function stepIsValid(step) {
        let valid = true;
        step.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

        step.querySelectorAll('input').forEach(input => {
            let ok = input.checkValidity();
            if (ok && input.name === 'phone') ok = input.value.replace(/\D/g, '').length >= 10;
            if (!ok) {
                valid = false;
                const wrapper = input.closest('.form-group, .option-grid, .checkbox-group') || input;
                wrapper.classList.add('is-invalid');
            }
        });

        if (!valid) {
            const firstBad = step.querySelector('.is-invalid input, input.is-invalid');
            if (firstBad && firstBad.type !== 'radio') firstBad.focus();
        }
        return valid;
    }

    let started = false;
    form.addEventListener('change', (e) => {
        const group = e.target.closest('.is-invalid');
        if (group) group.classList.remove('is-invalid');

        if (!started && typeof gtag === 'function') {
            started = true;
            gtag('event', 'form_start', { form_location: form.querySelector('[name="location"]').value });
        }

        if (e.target.name === 'owner' && renterHint) {
            renterHint.hidden = e.target.value !== 'Renter';
        }

        // Picking a project on step 1 moves straight on.
        if (e.target.name === 'project' && current === 0) {
            setTimeout(() => show(1), 180);
        }
    });

    form.addEventListener('input', (e) => {
        const group = e.target.closest('.is-invalid');
        if (group) group.classList.remove('is-invalid');
    });

    form.querySelectorAll('.step-next').forEach(btn => {
        btn.addEventListener('click', () => {
            if (stepIsValid(steps[current])) show(current + 1);
        });
    });

    if (backBtn) backBtn.addEventListener('click', () => show(Math.max(0, current - 1)));

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const firstInvalid = steps.findIndex(step => !stepIsValid(step));
        if (firstInvalid !== -1) {
            show(firstInvalid);
            stepIsValid(steps[firstInvalid]); // re-run so focus lands on the now-visible field
            return;
        }
        submitLead(form);
    });

    // Service pages arrive with the project already chosen, so skip straight to step 2.
    const preselected = form.querySelector('input[name="project"]:checked');
    show(form.dataset.preselect && preselected ? 1 : 0, false);
}

async function submitLead(form) {
    const button = form.querySelector('button[type="submit"]');
    const errorBox = form.querySelector('.form-error');
    const label = button.querySelector('.btn-text');
    const originalLabel = label.textContent;

    button.disabled = true;
    label.textContent = 'Sending...';
    if (errorBox) errorBox.hidden = true;

    let response;
    try {
        response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { Accept: 'application/json' }
        });
    } catch (err) {
        // Network/CORS problem: fall back to a normal form post so the lead isn't lost.
        form.submit();
        return;
    }

    if (response.ok) {
        const data = new FormData(form);
        try {
            sessionStorage.setItem('leadSubmitted', JSON.stringify({
                project: data.get('project') || '',
                timeframe: data.get('timeframe') || '',
                location: data.get('location') || 'Knoxville, TN'
            }));
        } catch (err) { /* storage blocked; lead is still sent */ }
        window.location.href = '/thank-you/';
        return;
    }

    const body = await response.json().catch(() => ({}));
    const message = body.errors && body.errors.length
        ? body.errors.map(e => e.message).join(' ')
        : 'Something went wrong sending your request. Please try again.';
    if (errorBox) {
        errorBox.textContent = message;
        errorBox.hidden = false;
    }
    button.disabled = false;
    label.textContent = originalLabel;
}

function initThankYouTracking() {
    if (!document.body.classList.contains('thank-you-page')) return;
    let lead = null;
    try {
        lead = JSON.parse(sessionStorage.getItem('leadSubmitted') || 'null');
        sessionStorage.removeItem('leadSubmitted');
    } catch (err) { /* ignore */ }
    celebrate();
    if (lead && typeof gtag === 'function') {
        gtag('event', 'generate_lead', {
            project: lead.project,
            timeframe: lead.timeframe,
            form_location: lead.location
        });
    }
}

// =============================================
// INPUT HELPERS
// =============================================

function initPhoneFormatting() {
    const phoneInput = document.getElementById('phone');
    if (!phoneInput) return;

    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '').slice(0, 10);
        if (value.length >= 6) {
            value = `(${value.slice(0,3)}) ${value.slice(3,6)}-${value.slice(6)}`;
        } else if (value.length >= 3) {
            value = `(${value.slice(0,3)}) ${value.slice(3)}`;
        }
        e.target.value = value;
    });
}

function initZipInput() {
    const zip = document.getElementById('zip');
    if (!zip) return;
    const hint = zip.parentElement.querySelector('.zip-hint');
    let areas = null;

    zip.addEventListener('input', async () => {
        zip.value = zip.value.replace(/\D/g, '').slice(0, 5);
        if (!hint) return;
        if (zip.value.length < 5) {
            hint.textContent = '';
            return;
        }
        if (!areas) {
            try {
                areas = await (await fetch('/zips.json')).json();
            } catch (err) {
                areas = {};
            }
        }
        const area = areas[zip.value];
        hint.textContent = area
            ? `Great, we have roofers who serve ${area}.`
            : 'Thanks. We\'ll check which local roofers cover this ZIP.';
        hint.classList.toggle('is-match', Boolean(area));
    });
}

// =============================================
// PAGE BEHAVIOUR
// =============================================

function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.problem-card, .service-card').forEach(el => observer.observe(el));

    const revealTargets = document.querySelectorAll(
        'section:not(.hero) .section-header, .step-card, .service-link-card, .guide-card, .hire-card, ' +
        '.faq-accordion, .area-group, .county-block, .content-aside .aside-card, .table-wrap, .illustration, ' +
        '.gameday-inner > *, .storm-layout > *, .signs-layout > *, .next-steps-card, .proof-item'
    );
    revealTargets.forEach(el => {
        const siblings = Array.from(el.parentElement.children);
        el.style.setProperty('--delay', `${Math.min(siblings.indexOf(el), 6) * 0.07}s`);
        el.classList.add('reveal');
        observer.observe(el);
    });
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (!target) return;
            e.preventDefault();
            const offset = target.getBoundingClientRect().top + window.pageYOffset - 80;
            window.scrollTo({ top: offset, behavior: 'smooth' });
        });
    });
}

function initFloatingCta() {
    const cta = document.querySelector('.floating-cta');
    const form = document.getElementById('quote');
    if (!cta || !form) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => cta.classList.toggle('is-hidden', entry.isIntersecting));
    }, { threshold: 0.15 });
    observer.observe(form);
}

// =============================================
// ROOF COST CALCULATOR
// =============================================

function initCostCalculator() {
    const card = document.getElementById('calculator');
    if (!card) return;
    const prices = JSON.parse(card.dataset.prices);
    const pitch = { low: [1.06, 1], medium: [1.15, 1], steep: [1.32, 1.15] };
    const money = n => '$' + (Math.round(n / 100) * 100).toLocaleString('en-US');
    let tracked = false;

    function update(userAction) {
        const sqft = Math.min(Math.max(parseFloat(document.getElementById('calc-sqft').value) || 0, 0), 20000);
        const stories = parseFloat(card.querySelector('[name="calc-stories"]:checked').value);
        const [slope, labor] = pitch[card.querySelector('[name="calc-pitch"]:checked').value];
        const material = document.getElementById('calc-material').value;
        const garage = document.getElementById('calc-garage').checked ? 480 : 0;

        const footprint = sqft / stories + garage;
        const roofArea = footprint * slope * 1.1;
        const [low, high] = prices[material];

        document.getElementById('calc-range').textContent =
            sqft ? `${money(roofArea * low * labor)} - ${money(roofArea * high * labor)}` : 'Enter your home size';
        document.getElementById('calc-detail').textContent =
            sqft ? `About ${Math.round(roofArea / 100)} squares (${Math.round(roofArea).toLocaleString('en-US')} sq ft of roof)` : '';

        if (userAction && !tracked && typeof gtag === 'function') {
            tracked = true;
            gtag('event', 'calculator_used', { material });
        }
    }

    card.addEventListener('input', () => update(true));
    card.addEventListener('change', () => update(true));
    update(false);
}

// =============================================
// CALL / TEXT TRACKING
// =============================================

function initContactTracking() {
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a[href^="tel:"], a[href^="sms:"]');
        if (!link || typeof gtag !== 'function') return;
        gtag('event', link.href.startsWith('tel:') ? 'phone_click' : 'text_click', {
            link_location: link.dataset.loc || link.closest('header, footer, .floating-cta, main, section')?.className.split(' ')[0] || 'page'
        });
    });
}

// =============================================
// TOUCHDOWN CONFETTI (thank-you page)
// =============================================

function celebrate() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const colors = ['#FF8200', '#FFFFFF', '#FF8200', '#58595B'];
    for (let i = 0; i < 90; i++) {
        const piece = document.createElement('span');
        piece.className = 'confetti';
        piece.style.left = `${Math.random() * 100}vw`;
        piece.style.background = colors[i % colors.length];
        piece.style.boxShadow = '0 0 1px rgba(0,0,0,0.25)';
        piece.style.animationDuration = `${2.4 + Math.random() * 2.2}s`;
        piece.style.animationDelay = `${Math.random() * 0.6}s`;
        piece.style.setProperty('--drift', `${(Math.random() - 0.5) * 220}px`);
        piece.style.setProperty('--spin', `${Math.random() * 900}deg`);
        document.body.appendChild(piece);
        piece.addEventListener('animationend', () => piece.remove());
    }
}
