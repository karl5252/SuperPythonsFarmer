import unittest

from game.exchange_board import ExchangeBoard
from tests.test_farmer import CommonSetupTeardown


class TestExchangeRates(CommonSetupTeardown):
    """Test the exchange rates between animals."""

    def test_given_player_invert_exchanges_animal_for_animal_then_herd_is_updated(self):
        """Test that the player can exchange animals for animals. Inverted exchange rate."""
        test_cases = [
            ("Horse", "Cow", 1, 2),
            ("Cow", "Pig", 1, 3),
            ("Pig", "Sheep", 1, 2),
            ("Sheep", "Rabbit", 1, 6)
        ]
        for from_animal, to_animal, offered_amount, requested_amount in test_cases:
            with self.subTest(from_animal=from_animal, to_animal=to_animal, offered_amount=offered_amount,
                              requested_amount=requested_amount):
                print(
                    f"Testing {from_animal} -> {to_animal} with offered amount {offered_amount} and requested amount {requested_amount}")

                self.test_player.update_herd(from_animal, offered_amount)
                ExchangeBoard.set_exchange_rate(from_animal, to_animal, offered_amount, requested_amount)
                self.game_manager.process_exchange(self.test_player, self.game_manager.main_herd, from_animal,
                                                   to_animal, offered_amount, requested_amount)
                player_herd = self.test_player.get_herd()
                self.assertEqual(0, player_herd[from_animal], "Player should lose animal when exchanging.")
                self.assertEqual(requested_amount, player_herd[to_animal], "Player should gain animal when exchanging.")

    def test_given_player_exchanges_animal_for_animal_then_herd_is_updated(self):
        """Test that the player can exchange animals for animals."""
        test_cases = [
            ("Rabbit", "Sheep", 6, 1),
            ("Sheep", "Pig", 2, 1),
            ("Pig", "Cow", 3, 1),
            ("Cow", "Horse", 2, 1),
            ("Sheep", "Foxhound", 1, 1),
            ("Cow", "Wolfhound", 1, 1),
        ]
        for from_animal, to_animal, offered_amount, requested_amount in test_cases:
            with self.subTest(from_animal=from_animal, to_animal=to_animal, offered_amount=offered_amount,
                              requested_amount=requested_amount):
                self.test_player.update_herd(from_animal, offered_amount)
                ExchangeBoard.set_exchange_rate(from_animal, to_animal, offered_amount, requested_amount)
                self.game_manager.process_exchange(self.test_player, self.game_manager.main_herd, from_animal,
                                                   to_animal, offered_amount, requested_amount)
                player_herd = self.test_player.get_herd()
                self.assertEqual(0, player_herd[from_animal], "Player should lose animal when exchanging.")
                self.assertEqual(requested_amount, player_herd[to_animal], "Player should gain animal when exchanging.")


if __name__ == '__main__':
    unittest.main()
