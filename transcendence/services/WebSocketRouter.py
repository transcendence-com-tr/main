import re  # Düzenli ifadeler için gerekli
import json
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import parse_qs
import jwt
from django.conf import settings
from transcendence.services.responses import socket_response
from transcendence.services.models.user import User
from django.utils import timezone

from transcendence.services.consumers.chat import ChatConsumer
from transcendence.services.consumers.friend import FriendConsumer
from transcendence.services.consumers.service import ServicesConsumer

accepted_paths = {
    r"^/ws/$": ServicesConsumer,
    r"^/ws/friends/$": FriendConsumer,
    r"^/ws/chat/(?P<room_name>[^/]+)/$": ChatConsumer,
}

class WebSocketRouter(WebsocketConsumer):
    def connect(self):
        print(f"WebSocket bağlantısı kuruldu. Gelen URL: {self.scope['path']}")

        params = parse_qs(self.scope['query_string'].decode('utf-8'))
        token = params.get("token", None)
        matched_consumer = None
        extracted_params = {}
        for path_pattern, consumer_class in accepted_paths.items():
            match = re.match(path_pattern, self.scope['path'])
            if match:
                matched_consumer = consumer_class
                extracted_params = match.groupdict()
                break

        if not matched_consumer:
            self.close()
            return

        try:
            data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=data['user_id'])
            self.scope['user'] = user
            params.update(extracted_params)
            if (matched_consumer == ChatConsumer):
                room_name = params.get('room_name', None)
                if room_name is None or not room_name or room_name.count('_') != 1:
                    self.close()
                    return
                user1_id = room_name.split('_')[0]
                user2_id = room_name.split('_')[1]
                problem = False
                if (user1_id == user2_id):
                    problem = True
                elif (user1_id == str(user.id)):
                    params['user'] = user
                    if (User.objects.filter(id=user2_id).exists()):
                        params['friend'] = User.objects.get(id=user2_id)
                    else:
                        problem = True
                elif (user2_id == str(user.id)):
                    params['user'] = user
                    if (User.objects.filter(id=user1_id).exists()):
                        params['friend'] = User.objects.get(id=user1_id)
                    else:
                        problem = True
                else:
                    problem = True
                if problem:
                    self.close()
                    return
            self.scope['params'] = params
        except Exception as e:
            print(f"JWT doğrulama hatası: {e}")
            self.close()
            return
        """
        
        if (params['room_name'] != None):
            self.room_name = params['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(f"Gruba eklendi: {self.room_group_name}, Kanal: {self.channel_name}")
            
        """
        self.accept()

    def disconnect(self, close_code):

        """
                if (self.room_name != None):
            self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        print("WebSocket bağlantısı kesildi.")

        """

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['event'] == 'ping':
            User.objects.filter(id=self.scope['user'].id).update(last_activity=timezone.now())
            response = socket_response('ping', 'pong')
            self.send(response)
        else:
            matched_consumer = None
            for path_pattern, consumer_class in accepted_paths.items():
                match = re.match(path_pattern, self.scope['path'])
                if match:
                    matched_consumer = consumer_class
                    break
            if matched_consumer:
                matched_consumer(self, self.scope['user'], data, self.scope['params'])

    def chat_message(self, event):
        # This method will be called when a message is sent to the group
        print("TRUE")
        message = event['message']
        # Send the message to the WebSocket
        self.send(text_data=json.dumps({
            'event': 'chat_message',
            'message': message
        }))