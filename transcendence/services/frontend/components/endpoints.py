
from django.urls import path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('notification/', views.notification, name='notification'),
]