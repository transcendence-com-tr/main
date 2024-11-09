
from django.urls import re_path
from transcendence.services.friends.FriendConsumer import FriendConsumer
from transcendence.services.ServiceConsumer import ServiceConsumer

websocket_urlpatterns = [
    re_path(r'ws/', ServiceConsumer.as_asgi()),
    re_path(r'ws/friends/', FriendConsumer.as_asgi()),
]