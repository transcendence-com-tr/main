import os
from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from transcendence.services.models.friend import Friend


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return render(request, 'home.html', {
        'user': request.user,
        "new_notify": False,
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def game(request):
    return render(request, "game.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def game_friends(request):
    return render(request, "game/friends.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def game_multiplayer(request):
    return render(request, "game/multiplayer.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def game_tournament(request):
    return render(request, "game/tournament.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def game_classic(request):
    return render(request, "game/classic.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def game_ai(request):
    return render(request, "game/ai.html", {

    })


@api_view(["GET"])
@permission_classes([AllowAny])
def profile(request):
    return render(request, "profile.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def login(request):
    return render(request, "login.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def register(request):
    return render(request, "register.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def logout(request):
    return render(request, "logout.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def leaderboard(request):
    return render(request, "leaderboard.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def chat(request):
    return render(request, "chat.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def settings(request):
    return render(request, "settings.html", {
        "friends": Friend.objects.filter(friend=request.user, is_accepted=True)
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def help(request):
    return render(request, "help.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def two_factor_auth(request):
    return render(request, "2fa.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def connect_42(request):
    return render(request, "42-connect.html", {

    })

@api_view(["GET"])
@permission_classes([AllowAny])
def register_42(request):
    return render(request, "42-register.html", {

    })