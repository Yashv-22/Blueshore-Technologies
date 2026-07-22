/**
 * Blueshore Technologies — Mobile Navigation Controller
 * Handles hamburger menu, mobile drawer, and submenu toggling.
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        boostResponsiveCSS(); // Instantly optimize responsive layouts for fluid mobile/tablet viewports
        injectMobileMenu();
        injectHamburgerButton();
        bindEvents();
    });

    window.onload = function() {
        // Wait 50ms so the !important CSS from boostResponsiveCSS is painted
        // before the scroll-reveal observer reads card positions.
        setTimeout(initExpertiseReveal, 50);
        setTimeout(initStatsCountUp, 50);
    };

    /**
     * Aggressively inject critical responsive overrides as an inline <style> tag.
     * Uses a MutationObserver to ensure it stays at the very end of <head>,
     * winning the cascade against Tailwind CDN's runtime style injection.
     */
    function boostResponsiveCSS() {
        var styleId = 'responsive-boost';
        var existing = document.getElementById(styleId);
        if (existing) existing.remove();

        var css = [
            '@media(max-width:767px){',
            '  html,body{overflow-x:hidden!important;width:100%!important;max-width:100vw!important;margin:0!important;padding:0!important}',
            '  *{box-sizing:border-box!important}',
            '  .px-8,.px-6{padding-left:16px!important;padding-right:16px!important}',
            '  .mx-auto{margin-left:auto!important;margin-right:auto!important}',
            '  .grid-cols-4,.grid-cols-5,.grid-cols-6{grid-template-columns:1fr!important;gap:24px!important}',
            '  .grid[class*="md:grid-cols-2"],.grid[class*="md:grid-cols-3"],.grid[class*="md:grid-cols-4"],.grid[class*="lg:grid-cols-4"],.grid[class*="lg:grid-cols-6"]{grid-template-columns:1fr!important;gap:24px!important}',
            '  .grid.grid-cols-2.md\\:grid-cols-4.items-center{grid-template-columns:repeat(2,1fr)!important;gap:24px!important}',
            '  .md\\:col-span-2,.md\\:col-span-3,.md\\:col-span-4,.lg\\:col-span-2{grid-column:span 1!important}',
            '  .py-\\[120px\\]{padding-top:48px!important;padding-bottom:48px!important}',
            '  .py-24,.py-20{padding-top:40px!important;padding-bottom:40px!important}',
            '  .text-headline-display{font-size:24px!important;line-height:30px!important}',
            '  .text-\\[60px\\]{font-size:24px!important;line-height:30px!important}',
            '  .text-\\[20px\\]{font-size:13.5px!important;line-height:19px!important}',
            '  footer .grid{grid-template-columns:1fr!important;text-align:center!important}',
            '  footer .flex.gap-4{justify-content:center!important;margin:0 auto 24px!important;display:flex!important}',
            '  footer .flex-wrap{flex-direction:column!important;align-items:center!important;gap:12px!important;display:flex!important;width:100%!important}',
            '  footer .flex.flex-col.md\\:flex-row{flex-direction:column!important;align-items:center!important;gap:20px!important;display:flex!important}',
            '  .max-w-2xl,.max-w-3xl,.max-w-4xl,.max-w-md,.w-\\[600px\\]{max-width:100%!important;width:100%!important}',
            '  section{overflow-x:hidden!important;width:100%!important}',
            '  .flex.justify-between.items-end{flex-direction:column!important;align-items:center!important;text-align:center!important;gap:12px!important}',
            '  .flex.justify-between.items-end .max-w-2xl{text-align:center!important;margin-left:auto!important;margin-right:auto!important}',
            '  .cta-process-content{text-align:center!important}',
            '  .cta-process-step{flex-direction:column!important;align-items:center!important;text-align:center!important;gap:12px!important}',
            '  .cta-impact-card{padding:24px 16px!important;border-radius:16px!important}',
            '  .cta-impact-card .grid.grid-cols-3{gap:8px!important;margin-bottom:24px!important}',
            '  .cta-impact-card .grid.grid-cols-3>div{padding:10px 4px!important;border-radius:10px!important}',
            '  .cta-impact-card .grid.grid-cols-3 .text-3xl{font-size:20px!important;line-height:1.2!important}',
            '  .cta-impact-card .grid.grid-cols-3 .text-xs{font-size:9px!important;line-height:12px!important;margin-top:2px!important}',
            '  .cta-impact-card h3{font-size:16px!important;margin-bottom:16px!important}',
            '  .cta-impact-card ul{margin-bottom:24px!important;gap:12px!important}',
            '  .cta-impact-card ul li span.text-sm{font-size:12.5px!important;line-height:18px!important}',
            '  .cta-impact-card a{padding:12px 16px!important;font-size:13.5px!important;border-radius:10px!important}',
            '  .cta-impact-card .flex.items-center.justify-center.gap-6{gap:12px!important;margin-top:16px!important;padding-top:16px!important}',
            '  .cta-impact-card .flex.items-center.justify-center.gap-6>div{gap:4px!important}',
            '  .cta-impact-card .flex.items-center.justify-center.gap-6 span.text-xs{font-size:10px!important}',
            '  .swiper-slide:not(.caseStudiesSwiper .swiper-slide){width:85vw!important;max-width:300px!important}',
            '  .case-studies-carousel-shell{width:100%!important;max-width:100%!important;left:auto!important;transform:none!important;padding-left:16px!important;padding-right:16px!important}',
            '  .caseStudiesSwiper{overflow:hidden!important;padding:0!important}',
            '  .caseStudiesSwiper .swiper-slide{max-width:none!important;min-width:0!important;height:auto!important;display:flex!important}',
            '  .caseStudiesSwiper .swiper-slide>div{width:88vw!important;max-width:310px!important;height:100%!important;margin-left:auto!important;margin-right:auto!important}',
            '  .caseStudiesSwiper .swiper-slide .h-64{height:150px!important}',
            '  .caseStudiesSwiper .swiper-slide .p-8{padding:16px!important}',
            '  .caseStudiesSwiper .swiper-slide h3{font-size:15px!important;line-height:20px!important;margin-bottom:6px!important}',
            '  .caseStudiesSwiper .swiper-slide .p-8 p{min-height:48px!important;font-size:11px!important;line-height:15px!important;margin-bottom:10px!important}',
            '  .caseStudiesSwiper .swiper-slide .grid.grid-cols-3{padding:8px!important;margin-bottom:10px!important;gap:4px!important}',
            '  .caseStudiesSwiper .swiper-slide .grid.grid-cols-3 .text-base{font-size:13px!important}',
            '  .caseStudiesSwiper .swiper-slide .grid.grid-cols-3 .text-\\[9px\\]{font-size:8px!important}',
            '  .caseStudiesSwiper .swiper-slide .space-y-1{margin-bottom:14px!important}',
            '  .caseStudiesSwiper .swiper-slide .space-y-1 div{font-size:10.5px!important;line-height:14px!important}',
            '  .caseStudiesSwiper .swiper-slide .space-y-1 .font-semibold{font-size:10px!important;margin-bottom:4px!important}',
            '  .case-studies-prev,.case-studies-next{display:none!important}',
            '  nav>div{padding-left:12px!important;padding-right:12px!important}',
            '  .mobile-menu-row{display:flex!important;align-items:center!important;justify-content:space-between!important;width:100%!important;border-bottom:1px solid rgba(255,255,255,0.05)!important}',
            '  :root:not(.dark) .mobile-menu-row{border-bottom:1px solid rgba(0,0,0,0.05)!important}',
            '  .mobile-menu-row a{flex:1!important;padding:14px 0!important;color:#cbd5e1!important;font-size:15px!important;font-weight:500!important;text-decoration:none!important;border-bottom:none!important}',
            '  :root:not(.dark) .mobile-menu-row a{color:#334155!important}',
            '  .mobile-menu-row a:hover{color:#3790ff!important}',
            '  .mobile-menu-row button{padding:14px 0 14px 20px!important;color:#cbd5e1!important;background:none!important;border:none!important;cursor:pointer!important;display:flex!important;align-items:center!important;justify-content:center!important;border-bottom:none!important}',
            '  :root:not(.dark) .mobile-menu-row button{color:#334155!important}',
            '  .mobile-menu-row button:hover{color:#3790ff!important}',
            '  #mobile-menu-drawer{display:flex!important;clip-path:inset(0 0 0 100%);opacity:0}',
            '  #mobile-menu-drawer.active{clip-path:inset(0 0 0 0)!important;opacity:1!important}',
            '  .ai-hero-full{height:80dvh!important;min-height:80dvh!important;max-height:80dvh!important;padding-top:80px!important;padding-bottom:0!important;overflow:hidden!important;display:flex!important;align-items:center!important}',
            '  .hero-enter-4{flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;justify-content:flex-start!important;width:100%!important;gap:8px!important}',
            '  .hero-enter-4::-webkit-scrollbar{display:none!important}',
            '  .hero-enter-4 a{flex:1 1 0%!important;width:auto!important;min-height:42px!important;max-height:46px!important;padding:10px 4px!important;font-size:10.5px!important;margin:0!important;border-radius:12px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;white-space:nowrap!important;letter-spacing:-0.02em!important}',
            '  .mobile-menu-links a{display:flex!important;align-items:center!important;justify-content:flex-start!important;text-align:left!important}',
            '  .mobile-menu-row a{display:flex!important;align-items:center!important;justify-content:flex-start!important;text-align:left!important}',
            /* ALWAYS keep stats strip as a flex row — never let grid rules collapse it */
            '  #stats-strip{padding-top:0!important;padding-bottom:0!important;height:20dvh!important;min-height:20dvh!important;max-height:20dvh!important;display:flex!important;align-items:center!important;overflow:hidden!important}',
            '  #stats-strip-inner{display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;justify-content:space-around!important;width:100%!important;gap:0!important;padding-left:8px!important;padding-right:8px!important}',
            '  #stats-strip-inner>div{flex:1 1 0!important;min-width:0!important}',
            '  #stats-strip .stat-number{font-size:20px!important;line-height:1.1!important}',
            '  #stats-strip .font-label-md{font-size:9px!important;line-height:13px!important}',
            '  .chip-item label{padding:8px 16px!important;font-size:13px!important}',
            '  a[href*="wa.me"]{width:48px!important;height:48px!important;bottom:80px!important;right:16px!important}',
            '  #ai-agent-toggle-btn{width:48px!important;height:48px!important;bottom:16px!important;right:16px!important}',
            '  #ai-agent-toggle-btn span.material-symbols-outlined{font-size:20px!important}',
            '  .ai-chat-window{bottom:80px!important;right:16px!important;max-width:calc(100vw - 32px)!important;max-height:calc(100vh - 110px)!important;border-radius:16px!important}',
            '  .expertise-card{padding:24px!important;min-height:200px!important;border-radius:12px!important}',
            '  .expertise-card .expertise-icon{margin-bottom:12px!important;font-size:28px!important}',
            '  .expertise-card h3{font-size:20px!important;line-height:26px!important;margin-bottom:8px!important}',
            '  .expertise-card p{font-size:14px!important;line-height:20px!important}',
            '  .awards-grid{grid-template-columns:repeat(2,1fr)!important;gap:16px!important;opacity:1!important}',
            '  .awards-grid>div{background:#131B2F!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:16px!important;padding:24px 16px!important;height:100%!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;text-align:center!important;transition:all 0.3s ease!important;box-shadow:0 4px 20px rgba(0,0,0,0.2)!important}',
            '  :root:not(.dark) .awards-grid>div{background:#f8fafc!important;border:1px solid rgba(0,0,0,0.05)!important;box-shadow:0 4px 20px rgba(0,51,102,0.05)!important}',
            '  .awards-grid>div span{color:#3790ff!important;font-size:40px!important;margin-bottom:8px!important;text-shadow:0 0 10px rgba(55,144,255,0.2)!important}',
            '  .awards-grid>div div{font-size:13px!important;line-height:1.4!important;font-weight:600!important;color:#f8fafc!important}',
            '  :root:not(.dark) .awards-grid>div div{color:#0f172a!important}',
            '  .outcome-card{padding:16px!important;border-radius:12px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;text-align:center!important}',
            '  .outcome-card span{margin-bottom:8px!important;font-size:24px!important;margin-left:auto!important;margin-right:auto!important}',
            '  .outcome-card h4{font-size:14px!important;line-height:20px!important;margin-bottom:4px!important}',
            '  .outcome-card p{font-size:11px!important;line-height:16px!important}',
            '}',
            /* Desktop Touch Dropdowns Support */
            '.relative.group.active-dropdown > div[class*="absolute"]{opacity:1!important;visibility:visible!important;pointer-events:auto!important;transform:translateY(0)!important}',
            '.relative.group.active-dropdown button span.material-symbols-outlined{transform:rotate(180deg)!important}',
            '@media(max-width:1023px){',
            '  .hamburger-btn{display:flex!important}',
            '  nav .hidden.lg\\:flex{display:none!important}',
            '}',
            /* Scroll-reveal: keep heading/subtitle/cards hidden until observer fires */
            '.expertise-heading{opacity:0!important;transform:translateY(36px)!important;filter:blur(8px)!important;transition:opacity 0.9s cubic-bezier(0.22,1,0.36,1),transform 0.9s cubic-bezier(0.22,1,0.36,1),filter 0.7s cubic-bezier(0.22,1,0.36,1)!important;will-change:opacity,transform,filter!important}',
            '.expertise-heading--visible{opacity:1!important;transform:translateY(0)!important;filter:blur(0)!important}',
            '.expertise-subtitle{opacity:0!important;transform:translateY(24px)!important;transition:opacity 0.8s cubic-bezier(0.22,1,0.36,1) 0.3s,transform 0.8s cubic-bezier(0.22,1,0.36,1) 0.3s!important;will-change:opacity,transform!important}',
            '.expertise-subtitle--visible{opacity:1!important;transform:translateY(0)!important}',
            '.expertise-card{opacity:0!important;transform:translateY(70px) scale(0.88)!important;filter:blur(6px)!important;transition:opacity 0.75s cubic-bezier(0.22,1,0.36,1),transform 0.75s cubic-bezier(0.22,1,0.36,1),filter 0.55s cubic-bezier(0.22,1,0.36,1)!important;will-change:opacity,transform,filter!important;overflow:hidden!important;position:relative!important}',
            '.expertise-card--visible{opacity:1!important;transform:translateY(0) scale(1)!important;filter:blur(0)!important}'
        ].join('\n');

        var style = document.createElement('style');
        style.id = styleId;
        style.textContent = css;
        document.head.appendChild(style);

        // MutationObserver to keep our style tag at the end
        var observer = new MutationObserver(function() {
            if (document.head.lastChild !== style) {
                document.head.appendChild(style);
            }
        });
        observer.observe(document.head, { childList: true });
    }

    function injectHamburgerButton() {
        // Find the nav's right-side flex container (contains phone + Let's Talk)
        const nav = document.querySelector('nav');
        if (!nav) return;

        const rightSection = nav.querySelector('.flex.items-center.gap-4');
        if (!rightSection) return;

        // Check if hamburger already exists
        if (document.getElementById('hamburger-btn')) return;

        const hamburger = document.createElement('button');
        hamburger.id = 'hamburger-btn';
        hamburger.className = 'hamburger-btn lg:hidden';
        hamburger.setAttribute('aria-label', 'Open navigation menu');
        hamburger.innerHTML = '<span class="material-symbols-outlined">menu</span>';

        rightSection.appendChild(hamburger);
    }

    function injectMobileMenu() {
        if (document.getElementById('mobile-menu-overlay')) return;

        // Overlay
        const overlay = document.createElement('div');
        overlay.id = 'mobile-menu-overlay';
        overlay.className = 'mobile-menu-overlay';

        // Drawer
        const drawer = document.createElement('div');
        drawer.id = 'mobile-menu-drawer';
        drawer.className = 'mobile-menu-drawer';
        drawer.innerHTML = `
            <div class="mobile-menu-header">
                <button class="mobile-menu-close" id="mobile-menu-close" aria-label="Close menu">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <div class="mobile-menu-links">
                <a href="/">Home</a>
                
                <div class="mobile-menu-row">
                    <a href="/services.html">Services</a>
                    <button class="mobile-submenu-toggle" data-target="submenu-services" aria-label="Toggle Services submenu">
                        <span class="material-symbols-outlined" style="font-size: 20px; transition: transform 0.2s;">expand_more</span>
                    </button>
                </div>
                <div class="mobile-submenu" id="submenu-services">
                    <a href="/services.html#software">Custom Software</a>
                    <a href="/services.html#mobile">Mobile Apps</a>
                    <a href="/services.html#cloud">Cloud & DevOps</a>
                    <a href="/services.html#data">AI & Automation</a>
                    <a href="/services.html#growth">Growth & SEO</a>
                    <a href="/services.html#support">Ongoing Support</a>
                </div>

                <div class="mobile-menu-row">
                    <a href="/industries.html">Industries</a>
                    <button class="mobile-submenu-toggle" data-target="submenu-industries" aria-label="Toggle Industries submenu">
                        <span class="material-symbols-outlined" style="font-size: 20px; transition: transform 0.2s;">expand_more</span>
                    </button>
                </div>
                <div class="mobile-submenu" id="submenu-industries">
                    <a href="/industries.html#finance-sector">Finance & Banking</a>
                    <a href="/industries.html#healthcare-sector">Healthcare</a>
                    <a href="/industries.html#ecommerce-sector">Retail & E-Commerce</a>
                    <a href="/industries.html#logistics-sector">Logistics</a>
                    <a href="/industries.html#education-sector">Education & EdTech</a>
                </div>

                <div class="mobile-menu-row">
                    <a href="/about.html">Company</a>
                    <button class="mobile-submenu-toggle" data-target="submenu-company" aria-label="Toggle Company submenu">
                        <span class="material-symbols-outlined" style="font-size: 20px; transition: transform 0.2s;">expand_more</span>
                    </button>
                </div>
                <div class="mobile-submenu" id="submenu-company">
                    <a href="/about.html">About Us</a>
                    <a href="/careers.html">Careers</a>
                    <a href="/portfolio.html">Case Studies</a>
                </div>

                <a href="/blog.html">Insights</a>
                <a href="/contact.html">Contact</a>
            </div>
            <div class="mobile-menu-cta">
                <a href="/contact.html">Let's Talk</a>
                <a href="tel:+919990712555" class="phone-link">
                    <span class="material-symbols-outlined" style="font-size: 18px;">call</span>
                    +91 99907 12555
                </a>
            </div>
        `;

        document.body.appendChild(overlay);
        document.body.appendChild(drawer);
    }

    function bindEvents() {
        // Open menu
        document.addEventListener('click', function (e) {
            const hamburger = e.target.closest('#hamburger-btn');
            if (hamburger) {
                openMenu();
            }
        });

        // Close via close button
        document.addEventListener('click', function (e) {
            if (e.target.closest('#mobile-menu-close')) {
                closeMenu();
            }
        });

        // Close via overlay
        document.addEventListener('click', function (e) {
            if (e.target.id === 'mobile-menu-overlay') {
                closeMenu();
            }
        });

        // Submenu toggles
        document.addEventListener('click', function (e) {
            const toggle = e.target.closest('.mobile-submenu-toggle');
            if (toggle) {
                const targetId = toggle.getAttribute('data-target');
                const submenu = document.getElementById(targetId);
                if (submenu) {
                    const isOpen = submenu.classList.contains('open');
                    // Close all submenus first
                    document.querySelectorAll('.mobile-submenu.open').forEach(function (el) {
                        el.classList.remove('open');
                        const parentBtn = document.querySelector('[data-target="' + el.id + '"]');
                        if (parentBtn) {
                            const icon = parentBtn.querySelector('.material-symbols-outlined');
                            if (icon) icon.style.transform = 'rotate(0deg)';
                        }
                    });
                    // Toggle target
                    if (!isOpen) {
                        submenu.classList.add('open');
                        const icon = toggle.querySelector('.material-symbols-outlined');
                        if (icon) icon.style.transform = 'rotate(180deg)';
                    }
                }
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                closeMenu();
            }
        });

        // Close on window resize to desktop
        window.addEventListener('resize', function () {
            if (window.innerWidth >= 1024) {
                closeMenu();
                // Reset touch active dropdowns
                document.querySelectorAll('nav .relative.group.active-dropdown').forEach(function (el) {
                    el.classList.remove('active-dropdown');
                });
            }
        });

        // Desktop Touch Dropdown Handler: tap-to-toggle dropdowns on touchscreen desktop viewports
        const desktopToggles = document.querySelectorAll('nav .relative.group');
        desktopToggles.forEach(function (groupEl) {
            const btn = groupEl.querySelector('button, a');
            if (!btn) return;

            btn.addEventListener('click', function (e) {
                if (window.innerWidth >= 1024) {
                    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
                    if (isTouch) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const isOpen = groupEl.classList.contains('active-dropdown');
                        
                        // Close all other active dropdowns
                        document.querySelectorAll('nav .relative.group.active-dropdown').forEach(function (el) {
                            if (el !== groupEl) {
                                el.classList.remove('active-dropdown');
                            }
                        });
                        
                        if (isOpen) {
                            groupEl.classList.remove('active-dropdown');
                        } else {
                            groupEl.classList.add('active-dropdown');
                        }
                    }
                }
            });
        });

        // Close dropdowns when tapping anywhere outside
        document.addEventListener('click', function (e) {
            if (!e.target.closest('nav .relative.group')) {
                document.querySelectorAll('nav .relative.group.active-dropdown').forEach(function (el) {
                    el.classList.remove('active-dropdown');
                });
            }
        });
    }

    function openMenu() {
        const overlay = document.getElementById('mobile-menu-overlay');
        const drawer = document.getElementById('mobile-menu-drawer');
        if (overlay) overlay.classList.add('active');
        if (drawer) drawer.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        const overlay = document.getElementById('mobile-menu-overlay');
        const drawer = document.getElementById('mobile-menu-drawer');
        if (overlay) overlay.classList.remove('active');
        if (drawer) drawer.classList.remove('active');
        document.body.style.overflow = '';

        // Reset submenus
        document.querySelectorAll('.mobile-submenu.open').forEach(function (el) {
            el.classList.remove('open');
        });
        document.querySelectorAll('.mobile-submenu-toggle .material-symbols-outlined').forEach(function (icon) {
            icon.style.transform = 'rotate(0deg)';
        });
    }

    /**
     * Scroll-Reveal: Core Expertise Cards
     * Called from window.onload after boostResponsiveCSS(), so opacity:0!important
     * is already in the DOM before we start observing card positions.
     */
    function initExpertiseReveal() {
        var isMobile = window.innerWidth < 768;

        /* --- 1. Heading: blur-lift reveal --- */
        var heading = document.querySelector('.expertise-heading');
        if (heading) {
            var headingObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('expertise-heading--visible');
                        headingObserver.unobserve(entry.target);
                    }
                });
            }, { 
                threshold: isMobile ? 0.1 : 0.3,
                rootMargin: isMobile ? '0px 0px -120px 0px' : '0px 0px 0px 0px'
            });
            headingObserver.observe(heading);
        }

        /* --- 2. Subtitle: fade-lift (CSS handles the 0.3s delay) --- */
        var subtitle = document.querySelector('.expertise-subtitle');
        if (subtitle) {
            var subtitleObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('expertise-subtitle--visible');
                        subtitleObserver.unobserve(entry.target);
                    }
                });
            }, { 
                threshold: isMobile ? 0.1 : 0.3,
                rootMargin: isMobile ? '0px 0px -120px 0px' : '0px 0px 0px 0px'
            });
            subtitleObserver.observe(subtitle);
        }

        /* --- 3. Cards: staggered scale+blur+lift --- */
        var cards = document.querySelectorAll('.expertise-card');
        if (!cards.length) return;

        var cardObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('expertise-card--visible');
                    cardObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: isMobile ? 0.05 : 0.08,
            rootMargin: isMobile ? '0px 0px -100px 0px' : '0px 0px -40px 0px'
        });

        cards.forEach(function(card, index) {
            card.style.transitionDelay = (isMobile ? 0 : (index * 130)) + 'ms';
            cardObserver.observe(card);
        });
    }

    /**
     * Count-Up: Stats Section
     * Animates each .stat-number from 0 to data-target when scrolled into view.
     * Uses easeOutQuart for a fast-start, smooth-decelerate feel.
     */
    function initStatsCountUp() {
        var statEls = document.querySelectorAll('.stat-number');
        if (!statEls.length) return;

        function easeOutQuart(t) {
            return 1 - Math.pow(1 - t, 4);
        }

        function animateCount(el) {
            var target   = parseInt(el.getAttribute('data-target'), 10);
            var suffix   = el.getAttribute('data-suffix') || '';
            var duration = parseInt(el.getAttribute('data-duration'), 10) || 1800;
            var start    = null;

            // Start at 0
            el.textContent = '0' + suffix;

            function step(timestamp) {
                if (!start) start = timestamp;
                var elapsed  = timestamp - start;
                var progress = Math.min(elapsed / duration, 1);
                var eased    = easeOutQuart(progress);
                var current  = Math.round(eased * target);
                el.textContent = current + suffix;

                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    // Snap to final value precisely
                    el.textContent = target + suffix;
                }
            }

            requestAnimationFrame(step);
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.3
        });

        statEls.forEach(function (el) {
            observer.observe(el);
        });
    }

})();
