# Blueshore Technologies — Project Handover & Optimization Guide

Welcome to the official developer and marketing handover documentation for the **Blueshore Technologies Full-Stack Platform**. This guide provides complete details on setting up, running, maintaining, and optimizing the platform. It includes a dedicated section tailored for **SEO, AEO, and GEO (Generative Engine Optimization)** experts to help maximize organic rankings, search engine discovery, and AI LLM citations.

---

## Table of Contents
1. [System Architecture Overview](#1-system-architecture-overview)
2. [Local Installation & Dependency Setup](#2-local-installation--dependency-setup)
3. [Production VPS & Docker Deployment](#3-production-vps--docker-deployment)
4. [Real-Time Visitor Telemetry & Chatbot Overview](#4-real-time-visitor-telemetry--chatbot-overview)
5. [SEO, AEO, and GEO Expert Manual](#5-seo-aeo-and-geo-expert-manual)
6. [Core Codebase File Map](#6-core-codebase-file-map)

---

## 1. System Architecture Overview

The platform is built on a modern, high-performance web architecture combining traditional MVC page rendering with real-time asynchronous WebSockets:

* **Backend Framework**: Django (Python 3.11)
* **Asynchronous Handler**: Daphne (ASGI server) supporting both HTTP requests and persistent WebSocket connections.
* **Database**: PostgreSQL (relational storage for CRM leads, visitor sessions, and blog posts).
* **Cache & Message Broker**: Redis (manages Django Channels routing and Celery background task state).
* **Background Tasks**: Celery (runs asynchronous workloads such as automated mailers or CRM alerts).
* **Security Scanning**: ClamAV (asynchronously scans uploaded career resumes for malware).
* **Reverse Proxy & Gateway**: Nginx (handles SSL termination, enforces security headers, compresses gzip payloads, rate-limits API routes, and serves static files directly).

---

## 2. Local Installation & Dependency Setup

Follow these steps to run the project locally on your machine for development or content testing:

### Prerequisites
* Python 3.11 installed.
* PostgreSQL and Redis running locally (or configured to use Docker equivalents).

### Step-by-Step Setup

1. **Clone & Open Codebase**:
   Open a terminal in the root of the project directory.

2. **Initialize Python Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies & Requirements**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**:
   Create a file named `.env` in the project root directory and define the following variables:
   ```env
   # Core Django Settings
   DJANGO_SECRET_KEY=your-development-secret-key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

   # Database Settings (Local PostgreSQL)
   USE_POSTGRES=True
   DB_NAME=blueshore
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=127.0.0.1
   DB_PORT=5432

   # Cache & Asynchronous Channels Settings
   USE_REDIS=True
   REDIS_URL=redis://127.0.0.1:6379/1
   CELERY_BROKER_URL=redis://127.0.0.1:6379/0
   CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

   # Third-Party AI API Keys
   GEMINI_API_KEY=your_google_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here

   # ClamAV Antivirus Settings
   CLAMAV_ENABLED=False
   ```

6. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Collect Static Assets**:
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Launch Asynchronous Daphne Server**:
   ```bash
   daphne -b 127.0.0.1 -p 8000 blueshore_server.asgi:application
   ```
   Access the app in your browser at `http://127.0.0.1:8000/`.

---

## 3. Production VPS & Docker Deployment

The application is fully containerized for simplified cloud orchestration. The production stack on the VPS runs behind hardened Nginx routing.

### Key Deployment Commands

Execute these SSH commands inside the server directory `/root/blueshore` to manage the production stack:

* **Rebuild and Re-Launch Containers**:
  Bakes newly transferred code or template adjustments into active images:
  ```bash
  docker compose build web celery_worker
  docker compose up -d
  ```

* **Restart Ingress Gateway**:
  Flushes upstream IP resolutions and reloads SSL configuration:
  ```bash
  docker compose restart nginx
  ```

* **Inspect Real-Time Logs**:
  ```bash
  docker compose logs -f web
  ```

---

## 4. Real-Time Visitor Telemetry & Chatbot Overview

### Live Telemetry Dashboard
Accessible to staff members at `/admin/live-visitors/`.
* **Dynamic Heartbeat**: Updates every 300ms using persistent WebSocket channels.
* **Navigation Tracking**: Displays the active page title alongside a clickable relative path hyperlink (e.g. `/custom-software-development/`).
* **Scroll Section Normalization**: Captures current scrolling focus (e.g. `Services Section` or custom headings like `Our Core Competencies`) and shows scroll percentage visually using mini-progress bars.
* **Geographical Mapping**: Resolves client IP addresses to countries and cities in real-time.

### Interactive Chatbot Rep
Driven by `assets/ai-chat.js` on the client and `apps/chatbot/views.py` on the backend:
* **LLM Model**: Integrates with Google Gemini (`gemini-2.5-flash`) for responsive, context-aware user chats.
* **System Directives**: Guides visitors through service button flows (`[button:Label]`) first, qualifies budget/timeline metrics, and dynamically routes high-intent users to the lead generation form.

---

## 5. SEO, AEO, and GEO Expert Manual

This codebase is specifically engineered to achieve top positions in traditional search indexing (SEO) and to maximize citations in AI engines (AEO/GEO) like Perplexity, ChatGPT Search, Gemini, and Claude.

### 5.1 Programmatic SEO & Service Pillar Pages
The platform implements a dual-tier organic landing system:
1. **Service Pillar Hubs** (`/services/<service_slug>/`):
   * Serves as high-authority central pillars mapping core services (e.g., custom software, AI automation).
2. **Programmatic Landing Pages** (`/<service_slug>/<location_slug>/`):
   * Dynamically matches service queries with target geographic locations (e.g. `/custom-software-development/new-york/` or `/ai-automation-services/london/`).
   * Scaled layout templates pull location parameters automatically to serve contextually relevant SEO copy.

* **Routing Rule**: Configured at the bottom of [urls.py](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/blueshore_server/urls.py) (`programmatic-seo-landing` rule) to serve pages dynamically without cluttering namespaces.

### 5.2 Dynamic Sitemaps & robots.txt
* **Sitemap Generation** (`/sitemap.xml`):
  Generates XML indexes on-the-fly, fetching all blog posts, authors, service hubs, and programmatic location landing pages dynamically to ensure search bots index new content instantly.
  * Configured in `apps/seo/views.py` ➔ `dynamic_sitemap_view`.
* **Crawling Directives** (`/robots.txt`):
  Dynamically maps accessibility paths, permitting crawler indexing on services/blogs while restricting access to administrative routes (`/admin/` or `/portal/`).
  * Configured in `apps/seo/views.py` ➔ `dynamic_robots_view`.

### 5.3 Semantic HTML Hierarchy & SEO Elements
All templates enforce strict semantic validation:
* **Single H1 Tag**: Every generated landing page contains exactly one main `<h1>` header focusing on target keywords.
* **Heading Cascades**: Headers follow a logical nesting order (`<h1>` ➔ `<h2>` ➔ `<h3>`) to help search engines parse readability.
* **Unique Interactive IDs**: Elements contain unique, explicit `id` parameters to facilitate clean accessibility parsing and modern crawler indexers.
* **Asset Optimization**: High-efficiency WebP/WebM assets are used, with structural layout tags specifying explicit `width`/`height` parameters to eliminate Layout Shifts (CLS) and optimize Core Web Vitals.

### 5.4 AEO & GEO Optimization Strategies (Artificial Intelligence Citations)
To ensure AI Answer Engines recommend and link back to this platform, apply these optimization guidelines inside your content creation workflow:

1. **QA and Conversational FAQ Sections**:
   * AI engines query patterns based on natural language questions. Structure blog and service copy with explicit, search-intent questions as `<h2>` tags followed by immediate, direct answers in paragraph form.
2. **Semantic Density & Contextual Anchors**:
   * Avoid keyword stuffing. Instead, focus on thematic entity density (co-occurring industry phrases). Mention brand names and service pairings within the same sentence as primary solutions.
3. **Structured Schema Data**:
   * Add JSON-LD schema definitions (Organization, Service, FAQPage) directly into head elements. Large Language Models read structured JSON-LD schemas directly to parse data graphs.
4. **Conversational Agent Customization**:
   * System prompts governing the interactive chatbot are defined in [ai-chat.js](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/assets/ai-chat.js) and [views.py](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/apps/chatbot/views.py). Update these prompts to align the chatbot's voice with the brand positioning and key marketing phrases.

---

## 6. Core Codebase File Map

Use this map to locate files when customizing features or adding optimizations:

* **`/templates/`**: HTML views rendered by Django.
  * [/templates/admin/live_visitors.html](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/templates/admin/live_visitors.html): The real-time visitor telemetry dashboard.
  * [/templates/admin/dashboard.html](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/templates/admin/dashboard.html): Main administrative dashboard template.
  * [/templates/seo/service_pillar.html](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/templates/seo/service_pillar.html): Authority pillar page layouts.
  * [/templates/seo/local_landing.html](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/templates/seo/local_landing.html): Programmatic landing templates.
* **`/assets/`**: Static JS, CSS, and media assets served by Nginx.
  * [/assets/ai-chat.js](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/assets/ai-chat.js): Client-side chatbot script and telemetry observer.
  * [/assets/ai-chat.css](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/assets/ai-chat.css): CSS styling for the chatbot interface.
* **`/apps/`**: Back-end Django applications.
  * [/apps/intelligence/consumers.py](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/apps/intelligence/consumers.py): WebSocket telemetry consumers (receives and processes page scrolls, URL navigation, and locations).
  * [/apps/seo/views.py](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/apps/seo/views.py): Sitemaps, robots.txt, and programmatic landing rendering logic.
  * [/apps/chatbot/views.py](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/apps/chatbot/views.py): Backend Gemini API client and system prompts.
* **`/nginx/`**: Production server routing rules.
  * [/nginx/default.conf](file:///c:/Users/dell/Desktop/Blueshore-Full-Stack/nginx/default.conf): SSL protocols, rate-limiting directives, and proxy passes.
* **`docker-compose.yml`**: Multi-container production deployment settings.
* **`requirements.txt`**: List of Python library dependencies.
