import json
from channels.generic.websocket import WebsocketConsumer
from transcendence.services.friends.FriendConsumer import FriendConsumer
from transcendence.services.ServicesConsumer import ServicesConsumer
from urllib.parse import parse_qs
import django
import os
import jwt
from django.conf import settings
from transcendence.services.responses import socket_response
from transcendence.services.models.user import User
from django.utils import timezone

accepted_paths = {
    "/ws/": ServicesConsumer,
    "/ws/friends/": FriendConsumer,
}

class WebSocketRouter(WebsocketConsumer):
    def connect(self):
        print(f"WebSocket bağlantısı kuruldu. Gelen URL: {self.scope['path']}")

        params = parse_qs(self.scope['query_string'].decode('utf-8'))
        token = params.get("token", None)
        try:
            data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=data['user_id'])
            self.scope['user'] = user
            if not self.scope['path'] in accepted_paths:
                self.close()
                return
        except:
            self.close()
            return
        else:
            self.accept()

    def disconnect(self, close_code):
        print("WebSocket bağlantısı kesildi.")

    def receive(self, text_data):
        data = json.loads(text_data)
        if (data['event'] == 'ping'):
            User.objects.filter(id=self.scope['user'].id).update(last_activity = timezone.now())
            response =  socket_response('ping','pong')
            self.send(response)
        accepted_paths[self.scope['path']](self, self.scope['user'], data)