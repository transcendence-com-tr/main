
from django.urls import path
from . import views
from django.urls import path , include

app_name = 'frontend'
urlpatterns = [
    path('components/', include('transcendence.services.frontend.components.endpoints')),
    path('home/', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/friends/', views.game_friends, name='game_friends'),
    path('game/multiplayer/', views.game_multiplayer, name='game_multiplayer'),
    path('game/tournament/', views.game_tournament, name='game_tournament'),
    path('game/classic/', views.game_classic, name='game_classic'),
    path('game/ai/', views.game_ai, name='game_ai'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('chat/', views.chat, name='chat'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
    path("2fa/", views.two_factor_auth, name="two_factor_auth"),
    path("42-connect/", views.connect_42, name="connect_42"),
    path("42-register/", views.register_42, name="register_42"),
]