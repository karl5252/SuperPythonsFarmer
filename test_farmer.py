import unittest

from main import Player, GameManager


class TestProcessDice(unittest.TestCase):
    def test_given_is_empty_player_herd_and_different_animals_rolled_herd_is_not_updated(self):
        """Test if herd is not updated when different animals are rolled."""
        test_player = Player()
        game_manager = GameManager()
        game_manager.process_dice(test_player, "Rabbit", "Sheep")
        player_herd = test_player.get_herd()
        for animal_type in player_herd.values():
            self.assertEqual(animal_type, 0)

    def test_given_is_empty_player_herd_and_same_animals_rolled_herd_is_updated_by_one(self):
        """Test if herd is updated by one when same animals are rolled."""
        test_player = Player()
        game_manager = GameManager()
        game_manager.process_dice(test_player, "Rabbit", "Rabbit")
        player_herd = test_player.get_herd()
        self.assertEqual(player_herd["Rabbit"], 1)

    def test_given_is_two_pairs_in_player_herd_and_same_animals_rolled_herd_is_updated_by_number_of_pairs(self):
        """Test if herd is updated by number of pairs when same animals are rolled."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 4})
        test = test_player.get_herd()
        game_manager = GameManager()
        # when
        game_manager.process_dice(test_player, "Rabbit", "Rabbit")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(player_herd["Rabbit"], 6)

    def test_given_is_all_animals_but_no_foxhound_when_player_rolls_fox_then_looses_rabbits(self):
        """Test if player looses rabbits when fox is rolled."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 1})
        test_player.update_herd({"Sheep": 1})
        test_player.update_herd({"Pig": 1})
        test_player.update_herd({"Cow": 1})
        test_player.update_herd({"Horse": 1})
        test_player.update_herd({"Wolfhound": 1})

        test = test_player.get_herd()
        game_manager = GameManager()
        # when
        game_manager.process_dice(test_player, "Rabbit", "Fox")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(player_herd["Rabbit"], 0)

    def test_given_is_all_animals_and_foxhound_when_player_rolls_fox_then_looses_foxhound_but_herd_is_intact(self):
        """Test if player looses only foxhound when fox is rolled."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 1})
        test_player.update_herd({"Sheep": 1})
        test_player.update_herd({"Pig": 1})
        test_player.update_herd({"Cow": 1})
        test_player.update_herd({"Horse": 1})
        test_player.update_herd({"Foxhound": 1})
        test_player.update_herd({"Wolfhound": 1})

        test = test_player.get_herd()
        game_manager = GameManager()
        # when
        game_manager.process_dice(test_player, "Rabbit", "Fox")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(player_herd["Rabbit"], 1)
        self.assertEqual(player_herd["Sheep"], 1)
        self.assertEqual(player_herd["Pig"], 1)
        self.assertEqual(player_herd["Cow"], 1)
        self.assertEqual(player_herd["Horse"], 1)
        self.assertEqual(player_herd["Wolfhound"], 1)
        self.assertEqual(player_herd["Foxhound"], 0)

    def test_given_low_main_herd_when_player_rolls_matching_animals_then_max_count_not_dropped_below_zero(self):
        """Test if max_count is not dropped below zero when low main herd and player rolls matching animals."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 4})  # two pairs
        game_manager = GameManager()

        game_manager.main_herd[0].max_count = 1  # set main herd Rabbit to one

        initial_main_herd_count = game_manager.main_herd[0].max_count

        # when
        game_manager.process_dice(test_player, "Rabbit", "Rabbit")
        # then
        final_main_herd_count = game_manager.main_herd[0].max_count

        player_herd = test_player.get_herd()
        self.assertEqual(player_herd["Rabbit"], 4)  # 4 initial + none added

        self.assertGreaterEqual(initial_main_herd_count,
                                final_main_herd_count)  # Assert that max_count is not dropped below zero


if __name__ == '__main__':
    unittest.main()
