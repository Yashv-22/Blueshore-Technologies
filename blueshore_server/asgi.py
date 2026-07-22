"""
ASGI config for blueshore_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueshore_server.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing consumer/routing modules.
django_asgi_app = get_asgi_application()

# Import routing details after django.setup() is implicit in get_asgi_application()
import apps.intelligence.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                apps.intelligence.routing.websocket_urlpatterns
            )
        )
    ),
})
