from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from jeux.models import Joueur


class TestSetup(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        self.user.save()
        self.player = Joueur.objects.create(utilisateur=self.user)
        self.player.save()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()