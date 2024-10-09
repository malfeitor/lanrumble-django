from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
import os
from dotenv import load_dotenv

load_dotenv()


urlpatterns = [
    path("", include("jeux.urls")),
    path("rectangle_game/", include("rectangle_game.urls")),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
    re_path(r"^robots.txt$", lambda r: HttpResponse("User-agent: *</br>Disallow: /")),
    path("api/", include("api.urls")),
]

if os.environ["DEBUG"]:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
