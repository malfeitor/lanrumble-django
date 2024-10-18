from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from jeux.models import Player, Videogame
import json


class TestSetupAnonymous(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", email="user@foo.com", password="pass"
        )
        self.user.save()
        self.player = Player.objects.create(utilisateur=self.user)
        self.player.save()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestSetupLoged(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", email="user@foo.com", password="pass"
        )
        self.user.save()
        self.player = Player.objects.create(utilisateur=self.user)
        self.player.save()
        login_data = {"username": "user", "password": "pass"}
        request = self.client.post(
            "/api/token/",
            json.dumps(login_data),
            content_type="application/json",
            secure=True,
        )
        self.accessToken = request.data["access"]
        self.refreshToken = request.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestSetupWithGames(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", email="user@foo.com", password="pass"
        )
        self.user.save()
        self.player = Player.objects.create(utilisateur=self.user)
        self.player.save()
        login_data = {"username": "user", "password": "pass"}
        request = self.client.post(
            "/api/token/",
            json.dumps(login_data),
            content_type="application/json",
            secure=True,
        )
        self.accessToken = request.data["access"]
        self.refreshToken = request.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.accessToken)

        videogame = Videogame.objects.create()
        videogame.save()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
