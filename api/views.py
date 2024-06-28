from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = AccessToken(request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1])
        content = {
            "message": f'Welcome {token["user_id"]} to the JWT Authentication page using React Js and Django!'
        }
        return Response(content)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            print(token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
