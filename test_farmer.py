import unittest

from main import Player, GameManager, ExchangeBoard


class TestProcessDice(unittest.TestCase):
    def test_given_is_empty_player_herd_and_different_animals_rolled_herd_is_not_updated(self):
        """Test if herd is not updated when different animals are rolled."""
        test_player = Player()
        game_manager = GameManager()
        game_manager.process_dice(test_player, "Rabbit", "Sheep")
        player_herd = test_player.get_herd()
        for animal_type in player_herd.values():
            self.assertEqual(0, animal_type, )

    def test_given_is_empty_player_herd_and_same_animals_rolled_herd_is_updated_by_one(self):
        """Test if herd is updated by one when same animals are rolled."""
        test_player = Player()
        game_manager = GameManager()
        game_manager.process_dice(test_player, "Rabbit", "Rabbit")
        player_herd = test_player.get_herd()
        self.assertEqual(1, player_herd["Rabbit"])

    def test_given_is_two_pairs_in_player_herd_and_one_matching_animal_rolled_herd_is_updated_by_number_of_pairs(self):
        """Test if herd is updated by number of pairs when matching animal is rolled."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 4})
        test = test_player.get_herd()
        game_manager = GameManager()
        # when
        game_manager.process_dice(test_player, "Rabbit", "Cow")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(6, player_herd["Rabbit"])

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
        self.assertEqual(6, player_herd["Rabbit"])

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
        self.assertEqual(0, player_herd["Rabbit"])

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
        self.assertEqual(1, player_herd["Rabbit"])
        self.assertEqual(1, player_herd["Sheep"])
        self.assertEqual(1, player_herd["Pig"])
        self.assertEqual(1, player_herd["Cow"])
        self.assertEqual(1, player_herd["Horse"])
        self.assertEqual(1, player_herd["Wolfhound"])
        self.assertEqual(0, player_herd["Foxhound"])

    def test_given_is_all_animals_but_no_wolfhound_when_player_rolls_wolf_then_looses_all_but_horse_and_dogs(self):
        """Test if player looses rabbits when fox is rolled."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 1})
        test_player.update_herd({"Sheep": 1})
        test_player.update_herd({"Pig": 1})
        test_player.update_herd({"Cow": 1})
        test_player.update_herd({"Horse": 1})
        test_player.update_herd({"Foxhound": 1})

        test = test_player.get_herd()
        game_manager = GameManager()
        # when
        game_manager.process_dice(test_player, "Rabbit", "Wolf")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(0, player_herd["Rabbit"])
        self.assertEqual(0, player_herd["Sheep"])
        self.assertEqual(0, player_herd["Pig"])
        self.assertEqual(0, player_herd["Cow"])
        self.assertEqual(1, player_herd["Horse"])

    def test_given_is_all_animals_and_wolfhound_when_player_rolls_wolf_then_herd_is_intact_and_looses_wolfhound(self):
        """Test if player looses only wolfhound when wolf is rolled."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 1})
        test_player.update_herd({"Sheep": 1})
        test_player.update_herd({"Pig": 1})
        test_player.update_herd({"Cow": 1})
        test_player.update_herd({"Horse": 1})
        test_player.update_herd({"Wolfhound": 1})
        test_player.update_herd({"Foxhound": 1})

        test = test_player.get_herd()
        game_manager = GameManager()
        # when
        game_manager.process_dice(test_player, "Rabbit", "Wolf")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(1, player_herd["Rabbit"])
        self.assertEqual(1, player_herd["Sheep"])
        self.assertEqual(1, player_herd["Pig"])
        self.assertEqual(1, player_herd["Cow"])
        self.assertEqual(1, player_herd["Horse"])
        self.assertEqual(0, player_herd["Wolfhound"])
        self.assertEqual(1, player_herd["Foxhound"])

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
        self.assertEqual(4, player_herd["Rabbit"])  # 4 initial + none added

        self.assertGreaterEqual(initial_main_herd_count,
                                final_main_herd_count)  # Assert that max_count is not dropped below zero

    #print("5. Exchange rules:")
    #print(" - 6 Rabbits = 1 Sheep")
   # print(" - 2 Sheep = 1 Pig")
  #  print(" - 3 Pigs = 1 Cow")
 #   print(" - 2 Cows = 1 Horse")

    def test_given_player_exchanges_rabbits_for_sheep_then_herd_is_updated(self):
        """Test if player exchanges rabbits for sheep then herd is updated."""
        # given
        test_player = Player()
        test_player.update_herd({"Rabbit": 6})
        game_manager = GameManager()
        ExchangeBoard.set_exchange_rate("Rabbit", "Sheep", 6)

        # when
        game_manager.process_exchange(test_player, "Rabbit", "Sheep")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(0, player_herd["Rabbit"])
        self.assertEqual(1, player_herd["Sheep"])

    def test_given_player_exchanges_sheep_for_pig_then_herd_is_updated(self):
        """Test if player exchanges sheep for pig then herd is updated."""
        # given
        test_player = Player()
        test_player.update_herd({"Sheep": 2})
        game_manager = GameManager()
        ExchangeBoard.set_exchange_rate("Sheep", "Pig", 2)

        # when
        game_manager.process_exchange(test_player, "Sheep", "Pig")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(0, player_herd["Sheep"])
        self.assertEqual(1, player_herd["Pig"])

    def test_given_player_exchanges_pig_for_cow_then_herd_is_updated(self):
        """Test if player exchanges pig for cow then herd is updated."""
        # given
        test_player = Player()
        test_player.update_herd({"Pig": 3})
        game_manager = GameManager()
        ExchangeBoard.set_exchange_rate("Pig", "Cow", 3)

        # when
        game_manager.process_exchange(test_player, "Pig", "Cow")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(0, player_herd["Pig"])
        self.assertEqual(1, player_herd["Cow"])

    def test_given_player_exchanges_cow_for_horse_then_herd_is_updated(self):
        """Test if player exchanges cow for horse then herd is updated."""
        # given
        test_player = Player()
        test_player.update_herd({"Cow": 2})
        game_manager = GameManager()
        ExchangeBoard.set_exchange_rate("Cow", "Horse", 2)

        # when
        game_manager.process_exchange(test_player, "Cow", "Horse")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(0, player_herd["Cow"])
        self.assertEqual(1, player_herd["Horse"])

    def test_given_player_exchanges_horse_for_cow_then_herd_is_updated(self):
        """Test if player exchanges horse for cow then herd is updated."""
        # given
        test_player = Player()
        test_player.update_herd({"Horse": 1})
        game_manager = GameManager()
        ExchangeBoard.set_exchange_rate("Horse", "Cow", 1)

        # when
        game_manager.process_exchange(test_player, "Horse", "Cow")
        # then
        player_herd = test_player.get_herd()
        self.assertEqual(0, player_herd["Horse"])
        self.assertEqual(2, player_herd["Cow"])


if __name__ == '__main__':
    unittest.main()
