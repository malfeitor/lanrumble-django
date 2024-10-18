from rest_framework import serializers
from .models import Player, Videogame, Boardgame, VideogameRating


class JeuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videogame
        fields = (
            "id",
            "nom",
            "coop",
            "pvp",
            "joueurs_max_hot_seat",
            "f2p",
            "joueurs_max_online",
        )
