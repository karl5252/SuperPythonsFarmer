import unittest

from main import Player, GameManager


class TestProcessDice(unittest.TestCase):
    def test_given_is_empty_player_herd_and_different_animals_rolled_herd_is_not_updated(self):
        test_player = Player()
        game_manager = GameManager()
        game_manager.process_dice(test_player, "Rabbit", "Sheep")
        player_herd = test_player.get_herd()
        for animal_type in player_herd.values():
            self.assertEqual(animal_type, 0)

    def test_given_is_empty_player_herd_and_same_animals_rolled_herd_is_updated(self):
        test_player = Player()
        game_manager = GameManager()
        game_manager.process_dice(test_player, "Rabbit", "Rabbit")
        player_herd = test_player.get_herd()
        self.assertEqual(player_herd["Rabbit"], 2)


if __name__ == '__main__':
    unittest.main()
