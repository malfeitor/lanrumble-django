from .test_setup import TestSetupLoged, TestSetupAnonymous, create_game
import logging


class TestViewLogged(TestSetupLoged):
    @classmethod
    def setUpTestData(cls):
        create_game(
            title="Helldivers 2",
            coop=True,
            pvp=False,
            max_hot_seat_players=1,
            max_online_players=4,
            f2p=False,
        )

    def test_get_game_1(self):
        request = self.client.get(
            "/api/videogame/1",
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 200)


class TestViewAnonymous(TestSetupAnonymous):
    def test_get_all_videogames(self):
        request = self.client.get(
            "/api/videogames",
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(request.status_code, 200)
