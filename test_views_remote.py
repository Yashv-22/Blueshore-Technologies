import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blueshore_server.settings")
django.setup()

from django.test import Client

c = Client()
routes = [
    "/glossary/",
    "/compare/",
    "/resources/",
    "/technology/",
    "/industry/",
    "/authors/",
    "/tools/roi-calculator/",
    "/sitemap.xml",
    "/admin/seo/dashboard/"
]

for r in routes:
    resp = c.get(r, HTTP_HOST='www.blueshoretech.com', secure=True, follow=True)
    print(f"ROUTE {r}: {resp.status_code}")
    if resp.status_code != 200:
        if hasattr(resp, 'exc_info') and resp.exc_info:
            import traceback
            traceback.print_exception(*resp.exc_info)


