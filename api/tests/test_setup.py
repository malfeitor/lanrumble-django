from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from jeux.models import Player, Videogame
import json


class TestSetupAnonymous(APITestCase):
    def setUp(self):
        self.client = APIClient()
        create_user(self)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestSetupLoged(APITestCase):
    def setUp(self):
        self.client = APIClient()
        create_user(self)
        authentificate(self)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


def authentificate(self):
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


def create_user(self):
    self.user = User.objects.create_user(
        username="user", email="user@foo.com", password="pass"
    )
    self.user.save()
    self.player = Player.objects.create(user=self.user)
    self.player.save()


def create_game(
    title,
    coop,
    pvp,
    max_hot_seat_players,
    max_online_players,
    f2p,
):
    videogame = Videogame.objects.create(
        title=title,
        coop=coop,
        pvp=pvp,
        max_hot_seat_players=max_hot_seat_players,
        max_online_players=max_online_players,
        f2p=f2p,
    )
    videogame.save()
