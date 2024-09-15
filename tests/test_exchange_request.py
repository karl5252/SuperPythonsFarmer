import unittest

from game.game_manager import GameManager
from game.player import Player
from game.exchange_request import ExchangeRequest


class TestGameManager(unittest.TestCase):

    def setUp(self):
        self.game_manager = GameManager()
        self.player1 = Player("Player1", 0)
        self.player2 = Player("Player2", 1)
        self.game_manager.players.append(self.player1)
        self.game_manager.players.append(self.player2)

    def test_post_exchange_request(self):
        self.player1.update_herd("Rabbit", 5)
        self.assertTrue(self.game_manager.post_exchange_request(self.player1, "Rabbit", "Sheep"))
        self.assertEqual(len(self.game_manager.exchange_requests), 1)
        self.assertIsInstance(self.game_manager.exchange_requests[0], ExchangeRequest)

    def test_post_exchange_request_invalid(self):
        self.player1.update_herd("Rabbit", 0)
        self.assertFalse(self.game_manager.post_exchange_request(self.player1, "Rabbit", "Sheep"))
        self.assertEqual(len(self.game_manager.exchange_requests), 0)

    def test_view_exchange_requests(self):
        self.player1.update_herd("Rabbit", 5)
        self.player2.update_herd("Sheep", 5)
        self.game_manager.post_exchange_request(self.player1, "Rabbit", "Sheep")
        self.game_manager.post_exchange_request(self.player2, "Sheep", "Pig")
        self.assertEqual(len(self.game_manager.view_exchange_requests()), 2)

    def test_accept_exchange_request(self):
        self.player1.update_herd("Rabbit", 5)
        self.game_manager.post_exchange_request(self.player1, "Rabbit", "Sheep")
        request = self.game_manager.exchange_requests[0]
        self.assertTrue(self.game_manager.accept_exchange_request(1, request))
        self.assertEqual(request.status, "accepted")

    def test_invalidate_requests(self):
        self.player1.update_herd("Rabbit", 5)
        self.game_manager.post_exchange_request(self.player1, "Rabbit", "Sheep")
        self.player1.update_herd("Rabbit", 0)
        self.game_manager.invalidate_requests()
        self.assertEqual(self.game_manager.exchange_requests[0].status, "invalid")


if __name__ == '__main__':
    unittest.main()
