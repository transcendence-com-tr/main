
from django.urls import path
from . import views

app_name = 'friends'
urlpatterns = [
    path('', views.friends, name='friends'),
    path('<int:friend_id>/accept/', views.accept_friend, name='accept_friend'),
    path('<int:friend_id>/reject/', views.reject_friend, name='reject_friend'),
]