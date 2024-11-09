# transcendence/services/friends.py
from channels.generic.websocket import WebsocketConsumer
from transcendence.services.responses import socket_response


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
