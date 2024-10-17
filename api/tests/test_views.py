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
