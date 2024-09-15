import unittest
from parameterized import parameterized as parametrized

from game.exchange_board import ExchangeBoard
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
        self.test_player = Player()

    def tearDown(self):
        self.test_player = None


class TestProcessDice(CommonSetupTeardown):

    def test_given_is_empty_player_herd_and_different_animals_rolled_herd_is_not_updated(self):
        """Test if herd is not updated when different animals are rolled."""
        init__herd = self.test_player.get_herd
        self.game_manager.process_dice(self.test_player, "Rabbit", "Sheep")
        player_herd = self.test_player.get_herd
        for animal_type in player_herd.values():
            self.assertEqual(0, animal_type, "Herd should not be updated when different animals are rolled.")

    def test_given_is_empty_player_herd_and_same_animals_rolled_herd_is_updated_by_one(self):
        """Test if herd is updated by one when same animals are rolled."""

        self.game_manager.process_dice(self.test_player, "Rabbit", "Rabbit")
        player_herd = self.test_player.get_herd
        self.assertEqual(1, player_herd["Rabbit"], "Herd should be updated by one when same animals are rolled.")

    def test_given_is_two_pairs_in_player_herd_and_one_matching_animal_rolled_herd_is_updated_by_number_of_pairs(self):
        """Test if herd is updated by number of pairs when matching animal is rolled."""
        # given
        self.test_player.update_herd("Rabbit", 4)
        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Cow")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(5, player_herd["Rabbit"], "Herd should be updated by number of pairs when matching animal is "
                                                   "rolled.")

    def test_given_is_two_pairs_in_player_herd_and_same_animals_rolled_herd_is_updated_by_number_of_pairs(self):
        """Test if herd is updated by number of pairs when same animals are rolled."""
        # given
        self.test_player.update_herd("Rabbit", 4)
        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Rabbit")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(6, player_herd["Rabbit"], "Herd should be updated by number of pairs when same animals are ")

    def test_given_is_all_animals_but_no_foxhound_when_player_rolls_fox_then_looses_rabbits(self):
        """Test if player looses rabbits when fox is rolled."""
        # given
        self.test_player.update_herd("Rabbit", 1)
        self.test_player.update_herd("Sheep", 1)
        self.test_player.update_herd("Pig", 1)
        self.test_player.update_herd("Cow", 1)
        self.test_player.update_herd("Horse", 1)
        self.test_player.update_herd("Wolfhound", 1)
        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Fox")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(0, player_herd["Rabbit"], "Player should loose rabbits when fox is rolled.")

    def test_given_is_all_animals_and_foxhound_when_player_rolls_fox_then_looses_foxhound_but_herd_is_intact(self):
        """Test if player looses only foxhound when fox is rolled."""
        # given
        self.test_player.update_herd("Rabbit", 1)
        self.test_player.update_herd("Sheep", 1)
        self.test_player.update_herd("Pig", 1)
        self.test_player.update_herd("Cow", 1)
        self.test_player.update_herd("Horse", 1)
        self.test_player.update_herd("Foxhound", 1)
        self.test_player.update_herd("Wolfhound", 1)
        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Fox")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(1, player_herd["Rabbit"], "Player should loose only foxhound when fox is rolled.")
        self.assertEqual(1, player_herd["Sheep"], "Player should loose only foxhound when fox is rolled.")
        self.assertEqual(1, player_herd["Pig"], "Player should loose only foxhound when fox is rolled.")
        self.assertEqual(1, player_herd["Cow"], "Player should loose only foxhound when fox is rolled.")
        self.assertEqual(1, player_herd["Horse"], "Player should loose only foxhound when fox is rolled.")
        self.assertEqual(1, player_herd["Wolfhound"], "Player should loose only foxhound when fox is rolled.")
        self.assertEqual(0, player_herd["Foxhound"], "Player should loose only foxhound when fox is rolled.")

    def test_given_is_all_animals_but_no_wolfhound_when_player_rolls_wolf_then_looses_all_but_horse_and_dogs(self):
        """Test if player looses all but horse and dogs when wolf is rolled."""
        # given
        self.test_player.update_herd("Rabbit", 1)
        self.test_player.update_herd("Sheep", 1)
        self.test_player.update_herd("Pig", 1)
        self.test_player.update_herd("Cow", 1)
        self.test_player.update_herd("Horse", 1)
        self.test_player.update_herd("Wolfhound", 0)
        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Wolf")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(0, player_herd["Rabbit"], "Player should loose rabbits when wolf is rolled.")
        self.assertEqual(0, player_herd["Sheep"], "Player should loose rabbits when wolf is rolled.")
        self.assertEqual(0, player_herd["Pig"], "Player should loose rabbits when wolf is rolled.")
        self.assertEqual(0, player_herd["Cow"], "Player should loose rabbits when wolf is rolled.")
        self.assertEqual(1, player_herd["Horse"], "Player should loose rabbits when wolf is rolled.")

    def test_given_is_all_animals_and_wolfhound_when_player_rolls_wolf_then_herd_is_intact_and_looses_wolfhound(self):
        """Test if player looses only wolfhound when wolf is rolled."""
        # given
        self.test_player.update_herd("Rabbit", 1)
        self.test_player.update_herd("Sheep", 1)
        self.test_player.update_herd("Pig", 1)
        self.test_player.update_herd("Cow", 1)
        self.test_player.update_herd("Horse", 1)
        self.test_player.update_herd("Foxhound", 1)
        self.test_player.update_herd("Wolfhound", 1)

        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Wolf")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(1, player_herd["Rabbit"])
        self.assertEqual(1, player_herd["Sheep"])
        self.assertEqual(1, player_herd["Pig"])
        self.assertEqual(1, player_herd["Cow"])
        self.assertEqual(1, player_herd["Horse"])
        self.assertEqual(0, player_herd["Wolfhound"])
        self.assertEqual(1, player_herd["Foxhound"])

    def test_given_low_main_herd_when_player_rolls_matching_animals_then_max_count_not_dropped_below_zero(self):
        """Test if we don`t debt the bank when main herd is low and player rolls matching animals."""
        # given
        self.test_player.update_herd("Rabbit", 4)  # two pairs

        self.game_manager.main_herd[0].herd_size = 1  # set main herd Rabbit to one

        initial_main_herd_count = self.game_manager.main_herd[0].herd_size
        init_player_herd = self.test_player.get_herd
        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Rabbit")  # due to remaining size should add
        # player just one rabbit
        # then
        final_main_herd_count = self.game_manager.main_herd[0].herd_size

        player_herd = self.test_player.get_herd
        self.assertEqual(5, player_herd["Rabbit"], "4 initial + one added")  # 4 initial + none added

        self.assertGreaterEqual(initial_main_herd_count,
                                final_main_herd_count, "Assert that max_count is not dropped below zero")

    def test_given_player_has_to_return_animals_main_herd_is_not_updated_over_the_max_value(self):
        """Test if player returns animal then main herd is not updated over the max value."""
        # given
        self.test_player.update_herd("Rabbit", 4)
        self.game_manager.main_herd[0].max_count = 1  # set main herd Rabbit to one

        # when
        self.game_manager.process_dice(self.test_player, "Rabbit", "Fox")
        final_main_herd_count = self.game_manager.main_herd[0].max_count

        self.assertEqual(1, final_main_herd_count, "Assert that main herd is not updated over the max value")

    def test_given_player_has_animals_in_herd_when_player_rolls_matching_animals_then_herd_is_updated(self):
        """Test if herd is updated when player has animals in herd and player rolls matching animals albeit other
        than already had."""
        # given
        self.test_player.update_herd("Rabbit", 4)

        # when
        self.game_manager.process_dice(self.test_player, "Pig", "Pig")
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(4, player_herd["Rabbit"], "4 initial + none added")  # 4 initial + none added
        self.assertEqual(1, player_herd["Pig"], "none initial + 1 added")  # none initial + 1 added

    def test_given_player_has_three_rabbits_and_rolls_cow_and_rabbit_then_herd_has_two_rabbits_and_no_cows(self):
        """Test if herd is updated correctly when player has three rabbits and rolls a cow on one dice and a rabbit
        on the other."""
        # given
        self.test_player.update_herd("Rabbit", 3)

        # when
        self.game_manager.process_dice(self.test_player, "Cow", "Rabbit")

        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(4, player_herd["Rabbit"], "Player should have 2 rabbits after rolling a rabbit and a cow.")
        self.assertEqual(0, player_herd["Cow"], "Player should have no cows after rolling a rabbit and a cow.")


class TestExchangeRates(CommonSetupTeardown):

    @parametrized.expand([
        ("Horse", "Cow", 1 / 2, 2),
        ("Cow", "Pig", 1 / 3, 3),
        ("Pig", "Sheep", 1 / 2, 2),
        ("Sheep", "Rabbit", 1 / 6, 6)
    ])
    def test_given_player_invert_exchanges_animal_for_animal_then_herd_is_updated(self, from_animal, to_animal, ratio,
                                                                                  expected_result):
        """Test if player exchanges animal for animal then herd is updated."""
        # given
        self.test_player.update_herd(from_animal, 1)
        ExchangeBoard.set_exchange_rate(from_animal, to_animal, ratio)

        # when
        self.game_manager.process_exchange(self.test_player, from_animal, to_animal)
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(0, player_herd[from_animal], "Player should loose animal when exchanging.")
        self.assertEqual(expected_result, player_herd[to_animal], "Player should gain animal when exchanging.")

    @parametrized.expand([
        ("Rabbit", "Sheep", 6),
        ("Sheep", "Pig", 2),
        ("Pig", "Cow", 3),
        ("Cow", "Horse", 2),
        ("Sheep", "Foxhound", 1),
        ("Cow", "Wolfhound", 1),
    ])
    def test_given_player_exchanges_animal_for_animal_then_herd_is_updated(self, from_animal, to_animal, ratio):
        """Test if player exchanges animal for animal then herd is updated."""
        # given
        self.test_player.update_herd(from_animal, ratio)
        ExchangeBoard.set_exchange_rate(from_animal, to_animal, ratio)

        # when
        self.game_manager.process_exchange(self.test_player, from_animal, to_animal)
        # then
        player_herd = self.test_player.get_herd
        self.assertEqual(0, player_herd[from_animal], "Player should loose animal when exchanging.")
        self.assertEqual(1, player_herd[to_animal], "Player should gain animal when exchanging.")


if __name__ == '__main__':
    unittest.main()
