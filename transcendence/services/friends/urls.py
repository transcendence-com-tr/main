from django.urls import path , include

urlpatterns = [
    path('friends/', include('transcendence.services.friends.endpoints')),
]
