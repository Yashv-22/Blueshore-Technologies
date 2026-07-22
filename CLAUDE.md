# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static marketing website for **Blueshore Technologies** — a B2B software development and consulting company. Built with plain HTML/CSS/JavaScript (no build tools, no npm). Python scripts are manual transformation utilities, not a build pipeline.

## Tech Stack

- **HTML5** pages served as-is (no server-side rendering or templating)
- **Tailwind CSS 3** via CDN (no pre-processing)
- **Vanilla JavaScript** (no frameworks)
- **AOS** (Animate On Scroll), **Swiper 11**, **Material Symbols Outlined** — all via CDN
- **Python 3** stdlib only (`os`, `re`, `glob`, `zipfile`) — no pip dependencies

## Running & Previewing

No build step. Open any `.html` file directly in a browser, or serve locally:

```bash
python -m http.server 8080
```

## Assets Folder

`assets/` contains all images, CSS, and JavaScript files that pages reference:

| File | Role |
|---|---|
| `styles.css` | Global responsive overrides using `!important` to win against Tailwind CDN's runtime injection |
| `responsive.css` | Additional tablet/desktop layout overrides |
| `light-theme.css` | Light-mode overrides — applied when `dark` class is absent from `<html>` |
| `ai-chat.css` | Styles for the AI chatbot widget |
| `responsive.js` | Injects mobile hamburger menu, mobile drawer, and scroll-reveal/count-up animations. Also injects critical responsive CSS inline via `boostResponsiveCSS()` |
| `theme-toggle.js` | Injects a sun/moon toggle button into the nav. Defaults to **light mode** on first visit; persists preference to `localStorage` under key `blueshore-theme-pref` |
| `ai-chat.js` | Injects the full AI chatbot widget. Uses Gemini 2.0 Flash API with streaming SSE when the user provides a key (stored in `localStorage` under `blueshore-gemini-key`); falls back to pattern-matching replies |

Every HTML page must include all three JS files and all four CSS files.

## Theme System

`<html class="dark">` is the default markup in every page. `theme-toggle.js` removes the `dark` class on first visit, making **light mode the default** for new visitors. Dark mode is restored if the user has previously saved that preference.

Color palette:
- Dark background: `#030816`, Dark surface: `#131B2F`
- Accent: `#f8ba19` (gold), Highlight text: `#3790ff` (cyan)

**All responsive overrides must use `!important`** because Tailwind CDN injects its styles at runtime after the stylesheet is parsed, meaning standard CSS specificity is insufficient.

## Python Utility Scripts

These scripts are **one-shot transformation tools**, not a continuous build pipeline. Run them manually when content needs updating:

| Script | Purpose |
|---|---|
| `optimize_seo.py` | Inject per-page `<title>`, meta tags, JSON-LD structured data, Open Graph/Twitter card tags, and a GEO/AEO content block with FAQ accordion before the footer |
| `update_all.py` | Standardize nav and inject WhatsApp button across all pages |
| `enhance.py` | Add AOS animations, custom CSS, Tailwind enhancements |
| `dark_theme_converter.py` | Apply dark theme CSS class replacements site-wide |
| `standardize_nav.py` | Ensure consistent navigation bar markup |
| `update_links.py` | Fix button onclick handlers and broken hrefs |
| `fix_footer.py` | Standardize footer links |
| `fix_html.py` | Clean up malformed tags and apply final dark theme fixes |

Run a script:
```bash
python <script_name>.py
```

Scripts operate on HTML files in the working directory using regex-based string replacements — they are **not idempotent**, so re-running may produce duplicated injections (e.g. double WhatsApp buttons). `optimize_seo.py` strips existing SEO tags before injecting, making it safer to re-run.

`scratch/` contains one-off diagnostic scripts (tag checkers, spacing analyzers). They are not part of any workflow and should not be run unless debugging a specific layout issue.

## Architecture & Conventions

**No component system.** Each page is a standalone HTML file. Shared UI (nav, footer, WhatsApp FAB, AI chatbot) is injected via Python scripts and JavaScript and then lives as static markup or runtime-injected DOM in each page.

**Background images** are hard-coded AWS S3 URLs (`binmile-media.s3.ap-south-1.amazonaws.com`) carried over from reference/competitor HTML in the `Reference/` folder.

**Reference/**: Contains scraped HTML from a competitor site used as a design reference. Do not modify these files.

## Page Inventory

`index.html`, `about.html`, `services.html`, `portfolio.html` (Case Studies), `industries.html`, `blog.html`, `contact.html`, `careers.html`, `submit-portfolio.html` (freelance roster), `privacy.html`, `terms.html`, `cookie.html`

## No Tests

There are no automated tests or test runners in this project.
