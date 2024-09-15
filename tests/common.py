import unittest

from game.game_manager import GameManager
from game.player import Player


class CommonSetupTeardown(unittest.TestCase):
    """Common setup and teardown for all tests."""

    @classmethod
    def setUpClass(cls):
        cls.game_manager = GameManager()

    @classmethod
    def tearDownClass(cls):
        cls.game_manager = None

    def setUp(self):
        self.test_player = Player(index=0)

    def tearDown(self):
        self.test_player = None