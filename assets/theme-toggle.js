/**
 * Blueshore Technologies — Theme Toggle
 *
 * Injects a sun/moon button into the nav and persists the user's
 * dark/light preference to localStorage.
 *
 * The <html> element starts with class="dark" in every page.
 * Removing that class activates light-theme.css overrides.
 */
(function () {
    'use strict';

    var STORAGE_KEY = 'blueshore-theme-pref';
    var html = document.documentElement;

    /* ------------------------------------------------------------------ */
    /* Apply stored theme immediately — runs before DOMContentLoaded so   */
    /* there's no flash when the user has saved a light preference.        */
    /* ------------------------------------------------------------------ */
    (function applyStoredTheme() {
        var stored = localStorage.getItem(STORAGE_KEY);
        if (stored === 'dark') {
            html.classList.add('dark');
        } else {
            // Default (including first visit) = light
            html.classList.remove('dark');
        }
    })();

    /* ------------------------------------------------------------------ */
    /* Helpers                                                              */
    /* ------------------------------------------------------------------ */
    function isDark() {
        return html.classList.contains('dark');
    }

    function setTheme(dark) {
        if (dark) {
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
        }
        localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light');
        syncIcons();
    }

    function syncIcons() {
        var dark = isDark();
        var icon  = dark ? 'light_mode' : 'dark_mode';
        var label = dark ? 'Switch to light mode' : 'Switch to dark mode';
        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
            btn.innerHTML =
                '<span class="material-symbols-outlined" ' +
                'style="font-size:20px;line-height:1;pointer-events:none;">' +
                icon + '</span>';
            btn.setAttribute('aria-label', label);
            btn.title = label;
        });
    }

    /* ------------------------------------------------------------------ */
    /* Build the toggle button element                                      */
    /* ------------------------------------------------------------------ */
    function makeButton() {
        var btn = document.createElement('button');
        btn.setAttribute('data-theme-toggle', '');
        btn.className = 'theme-toggle-btn';
        btn.type = 'button';
        btn.addEventListener('click', function () {
            setTheme(!isDark());
        });
        return btn;
    }

    /* ------------------------------------------------------------------ */
    /* Inject button into the desktop nav                                   */
    /* ------------------------------------------------------------------ */
    function injectIntoNav() {
        var nav = document.querySelector('nav');
        if (!nav) return;

        // Avoid double-injection on re-runs
        if (document.querySelector('[data-theme-toggle]')) return;

        // The right-side flex container: flex items-center gap-4
        var rightSection = nav.querySelector('.flex.items-center.gap-4');
        if (!rightSection) return;

        var btn = makeButton();

        // Place it just before the "Let's Talk" CTA button so it sits
        // beside the phone link on desktop and is always visible.
        var ctaButton = rightSection.querySelector('button:not(.hamburger-btn)');
        if (ctaButton) {
            rightSection.insertBefore(btn, ctaButton);
        } else {
            rightSection.insertBefore(btn, rightSection.firstChild);
        }

        syncIcons();
    }

    /* ------------------------------------------------------------------ */
    /* Wait for DOM                                                         */
    /* ------------------------------------------------------------------ */
    document.addEventListener('DOMContentLoaded', function () {
        injectIntoNav();
        syncIcons();
    });
})();
