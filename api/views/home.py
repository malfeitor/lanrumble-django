from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from jeux.models import Joueur, Vote_Jeu_Video


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # token = AccessToken(request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1])
        # print(vars(request.user))
        joueur = Joueur.objects.get(utilisateur=request.user.id)
        print(vars(joueur))
        print(joueur.amis.all())
        print(joueur.liste_jeux.all())
        content = {
            "message": f"Welcome {request.user} to the JWT Authentication page using React Js and Django!"
        }
        return Response(content)
