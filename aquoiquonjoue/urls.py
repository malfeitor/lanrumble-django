from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from rest_framework_simplejwt import views as jwt_views

import os
from dotenv import load_dotenv
load_dotenv()


urlpatterns = [
    path('', include('jeux.urls')),
    path('rectangle_game/', include('rectangle_game.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^robots.txt$', lambda r: HttpResponse("User-agent: *</br>Disallow: /")),
    path('api/token/',
        jwt_views.TokenObtainPairView.as_view(),
        name ='token_obtain_pair'),
    path('api/token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name ='token_refresh'),
    path('api/api-auth/', include('rest_framework.urls')),
]

if (os.environ['DEBUG']):
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)