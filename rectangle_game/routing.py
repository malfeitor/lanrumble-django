from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/rectangle_game/<str:room_name>/', consumers.PlayerConsumer),
]
