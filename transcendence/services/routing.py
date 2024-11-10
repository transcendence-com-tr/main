
from django.urls import re_path
from transcendence.services.WebSocketRouter import WebSocketRouter

websocket_urlpatterns = [
    re_path(r'ws/', WebSocketRouter.as_asgi()),
    #re_path(r'ws/friends/', FriendConsumer.as_asgi()),
]