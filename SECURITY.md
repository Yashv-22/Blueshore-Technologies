# Security Policy

## Reporting Security Vulnerabilities

The BlueShore Technologies engineering team takes security seriously. If you discover a security vulnerability, please notify us responsibly.

**Do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security issues by sending an email to `security@blueshoretech.com` or contacting the repository maintainer.

---

## Response Timeline

- **Acknowledgement**: Within 48 hours.
- **Assessment & Triage**: Within 5 business days.
- **Fix & Patch Release**: Dependent on severity, usually within 14 days.

---

## Security Architecture Highlights

1. **Environment Variables**: All production credentials (database passwords, API keys, secret keys) are injected exclusively via environment variables (`.env`).
2. **Brute Force Protection**: Implemented via `django-axes` with IP lockout after 5 failed attempts.
3. **Malware Resume Scanning**: Uploaded candidate resumes are scanned asynchronously using ClamAV prior to storage.
4. **Content Security Policy & Headers**: Hardened HTTP security headers (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, `Referrer-Policy`) enforced at Nginx and Django middleware levels.
5. **Session & Cookie Hardening**: `HttpOnly`, `SameSite=Lax`, and `Secure` cookie flags enforced in production environments.
