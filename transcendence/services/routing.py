
from django.urls import re_path
from transcendence.services.consumers.service import ServicesConsumer
from transcendence.services.consumers.chat import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/$', ServicesConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
]