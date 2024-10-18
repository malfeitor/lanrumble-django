from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jeux.models import Player, Videogame


class UserVideogamesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        def extract_data(jeu):
            return {"id": jeu.id, "title": jeu.nom}

        joueur = Player.objects.get(pk=user_id)
        try:
            all_games = joueur.videogames_list.all()
        except ObjectDoesNotExist:
            raise Http404
        return Response(list(map(extract_data, all_games)))
