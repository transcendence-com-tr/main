from django.urls import path , include

urlpatterns = [
    path('auth/', include('transcendence.services.auth.endpoints')),
    path('frontend/', include('transcendence.services.frontend.endpoints')),
    path('friends/', include('transcendence.services.friends.endpoints')),
]
