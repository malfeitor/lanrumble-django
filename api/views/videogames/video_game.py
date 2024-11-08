from rest_framework.views import APIView
from rest_framework.response import Response
from jeux.models import Videogame
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class VideogameView(APIView):
    def get(self, request, id):
        try:
            game = Videogame.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return Response(game.title)
