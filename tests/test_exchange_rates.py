import unittest
from parameterized import parameterized as parametrized
from game.exchange_board import ExchangeBoard
from tests.test_farmer import CommonSetupTeardown


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
