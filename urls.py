from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/', include('transcendence.services.urls')),
    re_path(r'^$', serve, {'path': 'index.html', 'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),

]
