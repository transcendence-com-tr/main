
from django.urls import re_path
from transcendence.services.friends.FriendConsumer import FriendConsumer

websocket_urlpatterns = [
    re_path(r'ws/friends/', FriendConsumer.as_asgi()),
]