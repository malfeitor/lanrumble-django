from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name = "api"
urlpatterns = [
    path("videogames", views.VideogamesView.as_view(), name="video_games"),
    path("videogame/<id>", views.VideogameView.as_view(), name="video_game"),
    path("user/<user_id>/videogames", views.UserVideogamesView.as_view(), name="video_games"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
