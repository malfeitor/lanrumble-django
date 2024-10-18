from .test_setup import TestSetupLoged
import json


class TestViewLoged(TestSetupLoged):
    def test_joueur_refresh_successfull(self):
        request = self.client.post(
            "/api/token/refresh/",
            json.dumps({"refresh": self.refreshToken}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 200)

    def test_joueur_refresh_error_in_refresh_token(self):
        request = self.client.post(
            "/api/token/refresh/",
            json.dumps({"refresh": "asd"}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 401)

    def test_joueur_refresh_not_logged(self):
        self.client.credentials()
        request = self.client.post(
            "/api/token/refresh/",
            json.dumps({"refresh": self.refreshToken}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 200)

    def test_joueur_refresh_bad_authorization_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "dasdsad")
        request = self.client.post(
            "/api/token/refresh/",
            json.dumps({"refresh": self.refreshToken}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 200)
