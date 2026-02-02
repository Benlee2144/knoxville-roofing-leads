// =============================================
// KNOXVILLE ROOF PROS - Lead Generation Scripts
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    initFormHandler();
    initScrollAnimations();
    initPhoneFormatting();
    initTimestamp();
    initSmoothScroll();
});

// =============================================
// FORM HANDLER
// =============================================

function initFormHandler() {
    const form = document.getElementById('leadForm');

    if (form) {
        form.addEventListener('submit', function(e) {
            // Validate required fields
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e63946';
                    field.style.animation = 'shake 0.5s ease';
                } else {
                    field.style.borderColor = '#e9ecef';
                }
            });

            // Validate phone number format
            const phoneField = document.getElementById('phone');
            if (phoneField && phoneField.value) {
                const phoneDigits = phoneField.value.replace(/\D/g, '');
                if (phoneDigits.length < 10) {
                    isValid = false;
                    phoneField.style.borderColor = '#e63946';
                }
            }

            // Validate email format
            const emailField = document.getElementById('email');
            if (emailField && emailField.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(emailField.value)) {
                    isValid = false;
                    emailField.style.borderColor = '#e63946';
                }
            }

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields correctly.');
                return;
            }

            // If form action is placeholder, show success message
            if (form.action.includes('YOUR_FORM_ID')) {
                e.preventDefault();
                showSuccessMessage();
            }
        });

        // Remove error styling on input
        form.querySelectorAll('input, select').forEach(field => {
            field.addEventListener('input', () => {
                field.style.borderColor = '#e9ecef';
                field.style.animation = '';
            });
        });
    }
}

// =============================================
// SUCCESS MESSAGE
// =============================================

function showSuccessMessage() {
    const form = document.getElementById('leadForm');
    const formCard = form.closest('.form-card');

    formCard.innerHTML = `
        <div class="success-message" style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 4rem; margin-bottom: 20px;">✅</div>
            <h2 style="color: #2d6a4f; font-size: 1.8rem; margin-bottom: 15px;">Request Received!</h2>
            <p style="color: #4a4a6a; font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
                Thank you! One of our roofing specialists will contact you within <strong>24 hours</strong> to schedule your free inspection.
            </p>
            <p style="color: #6c757d; font-size: 0.95rem;">
                📞 Need immediate help? Call us at <a href="tel:+18655551234" style="color: #e63946; font-weight: 600;">(865) 555-ROOF</a>
            </p>
        </div>
    `;

    // Scroll to form
    formCard.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Track conversion (placeholder for analytics)
    if (typeof gtag === 'function') {
        gtag('event', 'lead_form_submit', {
            'event_category': 'Lead Generation',
            'event_label': 'Knoxville Roofing'
        });
    }
}

// =============================================
// SCROLL ANIMATIONS
// =============================================

function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe cards
    document.querySelectorAll('.problem-card, .service-card, .testimonial-card').forEach(el => {
        observer.observe(el);
    });
}

// =============================================
// PHONE NUMBER FORMATTING
// =============================================

function initPhoneFormatting() {
    const phoneInput = document.getElementById('phone');

    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length >= 10) {
                value = `(${value.slice(0,3)}) ${value.slice(3,6)}-${value.slice(6,10)}`;
            } else if (value.length >= 6) {
                value = `(${value.slice(0,3)}) ${value.slice(3,6)}-${value.slice(6)}`;
            } else if (value.length >= 3) {
                value = `(${value.slice(0,3)}) ${value.slice(3)}`;
            }

            e.target.value = value;
        });
    }
}

// =============================================
// TIMESTAMP FOR FORM
// =============================================

function initTimestamp() {
    const timestampField = document.getElementById('timestamp');
    if (timestampField) {
        timestampField.value = new Date().toISOString();
    }
}

// =============================================
// SMOOTH SCROLL
// =============================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// =============================================
// SHAKE ANIMATION
// =============================================

const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

// =============================================
// CONSOLE BRANDING
// =============================================

console.log('%c🏠 Knoxville Roof Pros', 'color: #1e3a5f; font-size: 24px; font-weight: bold;');
console.log('%cLead Generation Landing Page', 'color: #6c757d; font-size: 14px;');
console.log('%c📞 (865) 555-ROOF', 'color: #e63946; font-size: 16px; font-weight: bold;');
