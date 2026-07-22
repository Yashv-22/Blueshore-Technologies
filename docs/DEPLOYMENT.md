# Production Deployment Guide — BlueShore Technologies

This document outlines the steps required to deploy the **BlueShore Technologies** stack in production using Docker Compose behind an Nginx reverse proxy with SSL termination.

---

## 1. Server Prerequisites

- **OS**: Ubuntu 22.04 LTS or Debian 12 (recommended)
- **RAM**: Minimum 2 GB (4 GB recommended for ClamAV container)
- **Software Installed**:
  - Docker 24.0+
  - Docker Compose v2.20+
  - Certbot (for SSL certificates)

---

## 2. Production Docker Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/Yashv-22/BlueShore-Technologies.git /opt/blueshore
cd /opt/blueshore
```

### Step 2: Configure Production Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and fill in production secrets:
```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=generate-a-strong-random-50-character-string
DJANGO_ALLOWED_HOSTS=blueshoretech.com,www.blueshoretech.com

USE_POSTGRES=True
DB_NAME=blueshore_prod
DB_USER=blueshore_admin
DB_PASSWORD=your-secure-db-password

USE_REDIS=True
REDIS_PASSWORD=your-secure-redis-password

GEMINI_API_KEY=your-production-gemini-key
CLAMAV_ENABLED=True
```

### Step 3: Launch Docker Stack
```bash
docker compose up -d --build
```

### Step 4: Verify Stack Status & Logs
```bash
docker compose ps
docker compose logs -f web
```

---

## 3. Operations & Maintenance

- **Apply Database Migrations**:
  ```bash
  docker compose exec web python manage.py migrate
  ```
- **Collect Static Files**:
  ```bash
  docker compose exec web python manage.py collectstatic --noinput
  ```
- **Create Superuser**:
  ```bash
  docker compose exec web python manage.py createsuperuser
  ```
- **Restart Nginx Gateway**:
  ```bash
  docker compose restart nginx
  ```
