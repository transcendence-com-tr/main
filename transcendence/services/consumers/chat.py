from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import jwt
from django.conf import settings
import json
from transcendence.services.responses import socket_response
from transcendence.services.models.user import User
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            params = parse_qs(self.scope['query_string'].decode('utf-8'))
            token = params.get("token", None)
            data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
            user = await sync_to_async(User.objects.get)(id=data['user_id'])
            self.scope['user'] = user
            room_name = self.scope['url_route']['kwargs']['room_name']
            if room_name is None or not room_name or room_name.count('_') != 1:
                raise Exception("Invalid room name")
            user1_id = room_name.split('_')[0]
            user2_id = room_name.split('_')[1]
            if (user1_id == user2_id or not sync_to_async(User.objects.filter(id=user1_id).exists)() or not sync_to_async(User.objects.filter(id=user2_id).exists)()):
                raise Exception("Invalid room name")
            elif (user1_id == str(user.id)):
                self.scope["room_user"] = user
                self.scope["room_friend"] = sync_to_async(User.objects.get)(id=user2_id)
            elif (user2_id == str(user.id)):
                self.scope["room_user"] = user
                self.scope["room_friend"] = sync_to_async(User.objects.get)(id=user1_id)
            else:
                raise Exception("Invalid room name")

            await self.channel_layer.group_add(
                room_name,
                self.channel_name
            )
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
        if data['event'] == 'message':
            message = data["payload"]
            room_name = self.scope['url_route']['kwargs']['room_name']
            await self.channel_layer.group_send(
                room_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
    async def chat_message(self, event):
        message = event['message']
        await self.send(socket_response('message', {
            'message': message,
            'user': {
                'username': self.scope['user'].username,
                'image': self.scope['user'].image
            }
        }))

