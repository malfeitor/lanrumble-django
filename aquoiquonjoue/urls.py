from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse

urlpatterns = [
    path('', include('jeux.urls')),
    path('rectangle_game/', include('rectangle_game.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^robots.txt$', lambda r: HttpResponse("User-agent: *</br>Disallow: /")),
]
