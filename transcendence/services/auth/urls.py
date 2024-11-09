from django.urls import path , include

urlpatterns = [
    path('auth/', include('transcendence.services.auth.endpoints')),
]
