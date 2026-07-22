from django.urls import re_path
from apps.intelligence import consumers

websocket_urlpatterns = [
    re_path(r'^ws/intelligence/visitor/$', consumers.VisitorConsumer.as_asgi()),
    re_path(r'^ws/intelligence/admin/$', consumers.AdminConsumer.as_asgi()),
]
