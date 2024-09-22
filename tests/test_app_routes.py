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
        self.test_game_manager.players.append(Player("Player 1"))
        self.test_game_manager.players.append(Player("Player 2"))

        app.get_game_manager = lambda: self.test_game_manager

    def test_roll_dice(self):
        # Assuming player_index 0 for the test
        response = self.client.post('/roll-dice', json={'player_index': 0})
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

    @unittest.skip("requires env variable SECRET_KEY. Run conditionally")
    def test_start_game(self):
        response = self.client.post('/start-game', json={'player_names': ['Player 1', 'Player 2']})
        self.assertEqual(302, response.status_code)  # Redirect to /game
        self.assertEqual(len(self.test_game_manager.players), 2)

    @unittest.skip("dirtied test. Run separately passes hence better isolation is required")
    def test_get_players(self):
        response = self.client.get('/get-players')
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertIn('players', data)
        self.assertEqual( 2, len(data['players']))

    def test_post_exchange_request(self):
        response = self.client.post('/post-exchange-request', json={
            'player_index': 0,
            'give_animal': 'Sheep',
            'give_count': 2,
            'receive_animal': 'Pig',
            'receive_count': 1,
            'recipient': 'main-herd'
        })
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertIn('success', data)

    def test_view_exchange_requests(self):
        response = self.client.get('/view-exchange-requests')
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertIn('requests', data)

    def test_forfeit(self):
        response = self.client.post('/forfeit')
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertIn('success', data)


if __name__ == '__main__':
    unittest.main()
