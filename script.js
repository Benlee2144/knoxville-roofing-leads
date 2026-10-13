document.addEventListener('DOMContentLoaded', function() {
    initLeadForm();
    initScrollAnimations();
    initPhoneFormatting();
    initZipInput();
    initSmoothScroll();
    initFloatingCta();
    initThankYouTracking();
});

// =============================================
// MULTI-STEP LEAD FORM
// =============================================

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

    function show(index) {
        current = index;
        steps.forEach((step, i) => step.classList.toggle('is-active', i === index));
        if (backBtn) backBtn.hidden = index === 0;
        if (counter) counter.textContent = `Step ${index + 1} of ${steps.length}`;
        if (bar) bar.style.width = `${((index + 1) / steps.length) * 100}%`;
        if (index > 0) {
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

    form.addEventListener('change', (e) => {
        const group = e.target.closest('.is-invalid');
        if (group) group.classList.remove('is-invalid');

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

    show(0);
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
    zip.addEventListener('input', () => {
        zip.value = zip.value.replace(/\D/g, '').slice(0, 5);
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
