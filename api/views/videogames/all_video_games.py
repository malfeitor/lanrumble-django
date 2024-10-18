from rest_framework.views import APIView
from rest_framework.response import Response
from jeux.models import Videogame


class VideogamesView(APIView):
    def get(self, request):
        all_games = Videogame.objects.all()
        return Response(list(map(lambda jeu: jeu.title, all_games)))
