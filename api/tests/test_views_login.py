from .test_setup import TestSetupAnonymous
import json


class TestViewsAnonymous(TestSetupAnonymous):
    def test_joueur_login_successfull(self):
        login_data = {"username": "user", "password": "pass"}
        request = self.client.post(
            "/api/token/",
            json.dumps(login_data),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 200)

    def test_joueur_login_no_credentials(self):
        login_data = {}
        request = self.client.post(
            "/api/token/",
            json.dumps(login_data),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 400)

    def test_joueur_login_wrong_password(self):
        login_data = {"username": "user", "password": "passe"}
        request = self.client.post(
            "/api/token/",
            json.dumps(login_data),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 401)

    def test_joueur_login_wrong_username(self):
        login_data = {"username": "usere", "password": "pass"}
        request = self.client.post(
            "/api/token/",
            json.dumps(login_data),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 401)
