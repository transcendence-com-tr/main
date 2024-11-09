# transcendence/services/friends.py
from channels.generic.websocket import WebsocketConsumer
import json


def socket_response(event, payload, status="success"):
    return str(json.dumps({
        'event': event,
        'payload': payload,
        'status': status
    }))


class FriendConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('Connected')

    def receive(self, text_data):
        print('Received:', {text_data})
        if text_data == 'ping':
            self.send(socket_response('pingpong', 'pong', 'success'))

    
    def disconnect(self, close_code):
        print('Disconnected')
