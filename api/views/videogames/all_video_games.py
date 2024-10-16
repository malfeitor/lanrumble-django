from rest_framework.views import APIView
from rest_framework.response import Response
from jeux.models import Jeu


class VideogamesView(APIView):
    def get(self, request):
        all_games = Jeu.objects.all()
        return Response(list(map(lambda jeu: jeu.nom, all_games)))
