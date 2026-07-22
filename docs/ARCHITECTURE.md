# Architecture Overview — BlueShore Technologies

## System Architecture

BlueShore Technologies is designed as a hybrid full-stack application combining server-rendered HTML pages with a modular Django REST API backend, real-time WebSocket telemetry, background Celery workers, and a containerized microservices stack.

```
                    ┌─────────────────────────┐
                    │      Client Browser     │
                    └───────────┬─────────────┘
                                │ HTTP / WebSocket
                                ▼
                    ┌─────────────────────────┐
                    │      Nginx Gateway      │
                    │   (SSL & Rate Limits)   │
                    └───────────┬─────────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼ HTTP                        ▼ WebSockets
       ┌──────────────────┐           ┌──────────────────┐
       │   Gunicorn/WSGI  │           │   Daphne/ASGI    │
       └─────────┬────────┘           └─────────┬────────┘
                 │                              │
                 └──────────────┬───────────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │ Django Framework   │
                     │ (10 Modular Apps)  │
                     └──────────┬─────────┘
                                │
     ┌──────────────────┬───────┴──────────┬──────────────────┐
     ▼                  ▼                  ▼                  ▼
┌──────────┐      ┌───────────┐      ┌───────────┐      ┌───────────┐
│ Postgres │      │   Redis   │      │  Celery   │      │  ClamAV   │
│ Database │      │ Cache/Msg │      │ Worker    │      │ Antivirus │
└──────────┘      └───────────┘      └───────────┘      └───────────┘
```

---

## Django Applications Breakdown (`apps/`)

1. **`core`**: Base models, password validators, security middleware, and MFA/TOTP setup.
2. **`contact`**: Ingests visitor contact requests, saves leads, triggers notifications.
3. **`crm`**: Staff dashboard featuring lead Kanban board, calendar view, and live visitor telemetry UI.
4. **`blog`**: Dynamic blog platform, category filtering, and case studies.
5. **`portfolio`**: Project showcase and freelance application submissions.
6. **`careers`**: Job board and asynchronous resume file uploads with malware scanning.
7. **`newsletter`**: Newsletter subscriptions and subscriber tracking.
8. **`chatbot`**: Integrates with Google Gemini API (`gemini-2.5-flash`) for lead qualification.
9. **`seo`**: Dynamic XML sitemaps, robots.txt, and location-based programmatic landing pages.
10. **`intelligence`**: Real-time WebSocket consumers tracking user scroll depth, URL navigation, and geolocations.

---

## Asynchronous Architecture

- **WebSockets (`apps/intelligence/consumers.py`)**: Streams live visitor heartbeat every 300ms to the admin dashboard at `/admin/live-visitors/`.
- **Task Queue (`celery.py`)**: Offloads long-running tasks such as resume scanning, email notifications, and CRM analytics processing.
- **Cache (`CACHES`)**: Redis instance stores channel layer messages and throttles API routes.
