from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import jwt
from django.conf import settings
import json
from transcendence.services.responses import socket_response
from transcendence.services.models.user import User
from transcendence.services.models.friend import Friend
from django.utils import timezone

class ServicesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            params = parse_qs(self.scope['query_string'].decode('utf-8'))
            token = params.get("token", None)
            data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
            user = await sync_to_async(User.objects.get)(id=data['user_id'])
            self.scope['user'] = user
        except Exception as e:
            await self.close()
            return
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['event'] == 'ping':
            await sync_to_async(User.objects.filter(id=self.scope['user'].id).update)(last_activity=timezone.now())
            response = socket_response(data['event'], 'pong')
            await self.send(response)
        if data['event'] == 'notify':
            friends = await sync_to_async(Friend.objects.filter(friend=self.scope["user"], is_accepted=False).exists)()
            result = friends
            response = socket_response(data['event'], result)
            await self.send(response)