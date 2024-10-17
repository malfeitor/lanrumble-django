from .test_setup import TestSetupAnonymous, TestSetupLoged
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


class TestViewLogged(TestSetupLoged):
    def test_joueur_logout(self):
        request = self.client.post(
            "/api/logout/",
            json.dumps({"refresh_token": self.refreshToken}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 205)
