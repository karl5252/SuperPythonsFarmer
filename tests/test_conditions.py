import unittest

from game.game_manager import GameManager, check_victory_condition
from game.player import Player
from tests.common import CommonSetupTeardown


class TestGameConditions(CommonSetupTeardown):

    def test_victory_condition(self):
        player = Player("Test Player")
        player.update_herd("Rabbit", 1)
        player.update_herd("Sheep", 1)
        player.update_herd("Pig", 1)
        player.update_herd("Cow", 1)
        player.update_herd("Horse", 1)

        assert True == check_victory_condition(player)

    def test_no_victory_condition(self):
        player = Player("Test Player")
        player.update_herd("Rabbit", 1)
        player.update_herd("Sheep", 0)  # Missing one required animal

        assert False == check_victory_condition(player)


if __name__ == '__main__':
    unittest.main()
