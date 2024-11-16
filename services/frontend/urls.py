from django.urls import path , include

urlpatterns = [
    path('frontend/', include('transcendence.services.frontend.endpoints')),
]
