from transcendence.services.models.friend import Friend
from transcendence.services.responses import socket_response
from django.utils import timezone

def ServicesConsumer(self, user , data):
    if (data['event'] == 'notify'):
        friends = Friend.objects.filter(friend=user, is_accepted=False).exists()
        result = friends
        response =  socket_response('notify',  result)
        self.send(response)

