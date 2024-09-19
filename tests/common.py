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
        self.test_player = Player(name="test", index=0)
        self.game_manager.main_herd.update_herd("Rabbit", 60)
        self.game_manager.main_herd.update_herd("Sheep", 24)
        self.game_manager.main_herd.update_herd("Pig", 20)
        self.game_manager.main_herd.update_herd("Cow", 12)
        self.game_manager.main_herd.update_herd("Horse", 6)
        self.game_manager.main_herd.update_herd("Foxhound", 4)
        self.game_manager.main_herd.update_herd("Wolfhound", 2)

    def tearDown(self):
        self.test_player = None