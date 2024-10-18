from .test_setup import TestSetupLoged
import json


class TestViewLogged(TestSetupLoged):
    def test_joueur_logout_successfull(self):
        request = self.client.post(
            "/api/logout/",
            json.dumps({"refresh_token": self.refreshToken}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 205)

    def test_joueur_logout_error_in_refresh_token(self):
        request = self.client.post(
            "/api/logout/",
            json.dumps({"refresh_token": "asd"}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 400)
