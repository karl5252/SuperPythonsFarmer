import unittest

from app import app, get_game_manager
from game.player import Player


class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and the test client
        self.app = app
        self.client = self.app.test_client()

        # Create a single GameManager instance for testing
        self.test_game_manager = get_game_manager()
        test = 0
        self.test_game_manager.players.append(Player("Player 1"))
        self.test_game_manager.players.append(Player("Player 2"))

        app.get_game_manager = lambda: self.test_game_manager

    def test_roll_dice(self):
        response = self.client.post('/roll-dice')
        self.assertEqual(200, response.status_code, "Expected success")
        data = response.get_json()
        self.assertIn('green', data)
        self.assertIn('red', data)

    def test_get_herd(self):
        game_manager = get_game_manager()
        test_players = game_manager.players
        response = self.client.get('/get-herd/0')
        self.assertEqual(200, response.status_code, "Expected success")
        data = response.get_json()
        self.assertIn('herd', data)

    def test_check_victory(self):
        response = self.client.get('/check-victory/0')
        self.assertEqual(200, response.status_code, "Expected success")
        data = response.get_json()
        self.assertIn('victory', data)


if __name__ == '__main__':
    unittest.main()
