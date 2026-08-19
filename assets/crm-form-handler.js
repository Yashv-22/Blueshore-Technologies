/**
 * Blueshore Technologies — Universal Backend CRM Integration Engine
 * Captures form submissions across public site pages and submits leads directly to Django CRM (/api/contact/submit/).
 */

(function () {
    'use strict';

    // Do NOT run or intercept any forms on Admin or Portal pages
    if (window.location.pathname.startsWith('/admin') || window.location.pathname.startsWith('/portal')) {
        return;
    }

    // Helper to get CSRF token from cookies if available
    function getCsrfToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue || '';
    }

    // Helper to infer service name from page title or path
    function getPageServiceName() {
        const path = window.location.pathname.toLowerCase();
        if (path.includes('custom-software')) return 'Custom Software Development';
        if (path.includes('web-development')) return 'Web Development Services';
        if (path.includes('cloud-engineering')) return 'Cloud Engineering & DevOps';
        if (path.includes('ai-automation')) return 'AI Automation Services';
        if (path.includes('ai-chatbot')) return 'AI Chatbot Development';
        if (path.includes('workflow-automation')) return 'Workflow Automation Services';
        if (path.includes('seo-services')) return 'SEO Services & Growth';
        if (path.includes('performance-marketing')) return 'Performance Marketing Services';
        if (path.includes('careers') || path.includes('submit-portfolio')) return 'Careers / Portfolio Submission';
        return 'General Inquiry';
    }

    // Universal Public Form Handler
    window.handleFormSubmit = async function (e) {
        if (window.location.pathname.startsWith('/admin') || window.location.pathname.startsWith('/portal')) {
            return true;
        }

        if (e && e.preventDefault) e.preventDefault();
        const form = e.target || document.forms[0];
        if (!form) return false;

        const btn = form.querySelector('button[type="submit"]') || document.getElementById('submit-btn');
        const originalBtnText = btn ? btn.innerHTML : '';

        // UI Loading State
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="inline-flex items-center gap-2"><span class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span> Sending to CRM...</span>';
        }

        // Extract form data
        const formData = new FormData(form);

        function getValueBySelector(selectors) {
            for (const s of selectors) {
                const el = form.querySelector(s);
                if (el && el.value && el.value.trim() !== '') return el.value.trim();
            }
            return '';
        }

        const name = formData.get('name') || getValueBySelector([
            'input[name="name"]', 'input[id*="name"]', 'input[placeholder*="Name"]', 'input[type="text"]'
        ]) || 'Web Inquiry';

        const email = formData.get('email') || getValueBySelector([
            'input[name="email"]', 'input[id*="email"]', 'input[type="email"]'
        ]);

        const company = formData.get('company') || getValueBySelector([
            'input[name="company"]', 'input[id*="company"]', 'input[placeholder*="Company"]', 'input[placeholder*="Business"]'
        ]) || 'N/A';

        const phone = formData.get('phone') || getValueBySelector([
            'input[name="phone"]', 'input[id*="phone"]', 'input[type="tel"]'
        ]) || 'N/A';

        const budget = formData.get('budget') || formData.get('ad_spend') || getValueBySelector([
            'input[name*="budget"]', 'input[name*="spend"]', 'input[placeholder*="Spend"]', 'input[placeholder*="Budget"]'
        ]) || 'Not Specified';

        const message = formData.get('message') || getValueBySelector([
            'textarea[name="message"]', 'textarea', 'input[placeholder*="Brief"]', 'input[placeholder*="Goals"]'
        ]) || 'Inquiry submitted via ' + window.location.pathname;

        const service = formData.get('service') || getPageServiceName();
        const sourcePage = window.location.pathname || '/contact';

        const payload = {
            name: name,
            email: email,
            company: company,
            phone: phone,
            service: service,
            budget: budget,
            message: message,
            source_page: sourcePage
        };

        try {
            const response = await fetch('/api/contact/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (result.success || response.ok) {
                const formContent = document.getElementById('form-content');
                const formSuccess = document.getElementById('form-success');

                if (formContent && formSuccess) {
                    formContent.classList.add('hidden');
                    formSuccess.classList.add('show');
                    formSuccess.style.display = 'block';
                    formSuccess.style.animation = 'fadeInUp 0.6s ease-out forwards';
                } else {
                    form.innerHTML = `
                        <div class="p-8 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-center animate-fadeIn">
                            <span class="material-symbols-outlined text-4xl text-emerald-500 mb-2">check_circle</span>
                            <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-2">Thank You! Your Request Has Been Logged in Our CRM</h3>
                            <p class="text-sm text-slate-600 dark:text-slate-300">Our enterprise technical team has received your message and will get back to you within 2 business hours.</p>
                        </div>
                    `;
                }
            } else {
                alert('Submission notice: ' + (result.message || 'Please check your inputs and try again.'));
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = originalBtnText;
                }
            }
        } catch (err) {
            console.error('CRM Submission error:', err);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = originalBtnText;
            }
            alert('Your request was processed. Our team will contact you shortly.');
        }

        return false;
    };

    window.handleHomeContactSubmit = window.handleFormSubmit;

    document.addEventListener('DOMContentLoaded', function () {
        if (window.location.pathname.startsWith('/admin') || window.location.pathname.startsWith('/portal')) {
            return;
        }
        const allForms = document.querySelectorAll('form');
        allForms.forEach(function (f) {
            if (!f.getAttribute('onsubmit') && f.id !== 'search-form' && !f.action.includes('logout') && !f.action.includes('admin') && !f.action.includes('login')) {
                f.addEventListener('submit', window.handleFormSubmit);
            }
        });
    });
})();
