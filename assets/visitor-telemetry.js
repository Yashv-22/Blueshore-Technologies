/**
 * Blueshore Technologies — Real-Time Live Visitor Telemetry Client
 * Tracks visitor presence, current page, active duration, and live scroll percentage depth.
 */
(function () {
    'use strict';

    if (window.location.pathname.startsWith('/admin') || window.location.pathname.startsWith('/portal')) {
        return;
    }

    // Generate or retrieve persistent session ID
    let sessionId = localStorage.getItem('blueshore_telemetry_sid');
    if (!sessionId) {
        sessionId = 'sid_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
        localStorage.setItem('blueshore_telemetry_sid', sessionId);
    }

    let startTime = Date.now();
    let maxScroll = 0;

    function getScrollPercentage() {
        const docEl = document.documentElement;
        const body = document.body;
        const scrollTop = window.pageYOffset || docEl.scrollTop || body.scrollTop || 0;
        const scrollHeight = (docEl.scrollHeight || body.scrollHeight || 1) - window.innerHeight;
        if (scrollHeight <= 0) return 100;
        const pct = Math.min(100, Math.max(0, Math.round((scrollTop / scrollHeight) * 100)));
        if (pct > maxScroll) maxScroll = pct;
        return pct;
    }

    async function sendTelemetryPing() {
        const payload = {
            session_id: sessionId,
            current_url: window.location.href,
            current_page_title: document.title || window.location.pathname,
            scroll_percentage: getScrollPercentage(),
            max_scroll: maxScroll,
            total_duration: Math.round((Date.now() - startTime) / 1000)
        };

        try {
            await fetch('/api/telemetry/ping/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } catch (e) {
            // Silent error catching for smooth client UX
        }
    }

    // Initial ping on page load
    document.addEventListener('DOMContentLoaded', sendTelemetryPing);
    window.addEventListener('scroll', function () {
        getScrollPercentage();
    }, { passive: true });

    // Periodic heartbeat every 4 seconds
    setInterval(sendTelemetryPing, 4000);
})();
