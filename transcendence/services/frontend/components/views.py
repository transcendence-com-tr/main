import os
from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from transcendence.services.models.user import User
from transcendence.services.models.friend import Friend

@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    search = request.GET.get('search')
    if not search:
        return render(request, 'components/search.html', {
            'users': [],
        })
    users = User.objects.filter(username__icontains=search).exclude(id=request.user.id).order_by('username')[:5]
    for user in users:
        user.is_friend_request = Friend.objects.filter(user=request.user, friend=user).exists() or Friend.objects.filter(user=user, friend=request.user).exists()
        user.is_friend = Friend.objects.filter(user=request.user, friend=user, is_accepted=True).exists() or Friend.objects.filter(user=user, friend=request.user, is_accepted=True).exists()

    #maximum 5 user
    return render(request, 'components/search.html', {
        'users': users,
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def notification(request):
    friends = Friend.objects.filter(friend=request.user, is_accepted=False)
    return render(request, 'components/notification.html', {
        'friends': friends,
    })


