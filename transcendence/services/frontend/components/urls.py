from django.urls import path , include

urlpatterns = [
    path('frontend/components/', include('transcendence.services.frontend.components.endpoints')),
]
