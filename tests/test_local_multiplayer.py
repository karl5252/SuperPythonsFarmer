import unittest

from game.player import Player
from tests.common import CommonSetupTeardown


class MyTestCase(CommonSetupTeardown):

    def setUp(self):
        super().setUp()
        # Additional setup code if needed
        self.test_player_1 = Player(index=0)
        self.test_player_2 = Player(index=1)
        self.game_manager.players = [self.test_player_1, self.test_player_2]

    def tearDown(self):
        # Additional teardown code if needed
        super().tearDown()
        self.test_player_1 = None
        self.test_player_2 = None

    def test_given_two_players_when_subtracting_and_adding_herd_is_not_exceeded(self):
        """Test that two players interacting with the main herd don't cause it to exceed its max size."""

        # Set herd size for testing
        self.game_manager.main_herd[0].herd_size = 5  # Rabbit
        self.game_manager.main_herd[0].max_count = 10  # Rabbit max_count is 10

        # Player 1: Subtract 3 rabbits from the main herd
        self.test_player_1.update_herd("Rabbit", 3)
        self.game_manager.subtract_main_herd("Rabbit", 3)

        # Player 2: Subtract 2 rabbits from the main herd
        self.test_player_2.update_herd("Rabbit", 2)
        self.game_manager.subtract_main_herd("Rabbit", 2)

        # Check if the main herd has subtracted correctly
        self.assertEqual(0, self.game_manager.main_herd[0].herd_size, "Main herd should be empty after subtraction")

        # Player 1 adds 2 rabbits back to the herd
        self.game_manager.add_to_main_herd("Rabbit", 2)

        # Player 2 adds 4 rabbits back (but max herd size is 10)
        self.game_manager.add_to_main_herd("Rabbit", 4)

        # Check that the herd is capped at 5 (previous herd of 2 + adding max of 3, not exceeding max_count of 10)
        self.assertEqual(5, self.game_manager.main_herd[0].herd_size, "Main herd should not exceed 5 rabbits.")

    def test_herd_not_exceeding_max_count_on_fox_or_wolf(self):
        """Test that the main herd doesn't exceed its max size when adding back animals from fox or wolf attacks."""

        # Set up the main herd for rabbits
        self.game_manager.main_herd[0].herd_size = 58  # Close to max
        self.game_manager.main_herd[0].max_count = 60  # Max size of rabbit herd is 60

        # Player 1 has 3 rabbits
        self.test_player_1.update_herd("Rabbit", 3)

        # Player 1 rolls a wolf (loses rabbits), but should not exceed max count of 60 when added back
        self.game_manager.process_dice(self.test_player_1, "Rabbit", "Wolf")

        # Check that the herd size does not exceed max count of 60
        self.assertEqual(60, self.game_manager.main_herd[0].herd_size, "Main herd rabbit count should not exceed 60")

    def test_multiple_players_subtracting_and_adding_with_fox(self):
        """Test multiple players interact with the main herd when fox is rolled."""

        # Set up main herd
        self.game_manager.main_herd[0].herd_size = 40  # Rabbits
        self.game_manager.main_herd[0].max_count = 60

        # Player 1 has 3 rabbits
        self.test_player_1.update_herd("Rabbit", 3)
        # Player 2 has 5 rabbits
        self.test_player_2.update_herd("Rabbit", 5)

        # Both players roll a fox (both lose all rabbits)
        self.game_manager.process_dice(self.test_player_1, "Rabbit", "Fox")
        self.game_manager.process_dice(self.test_player_2, "Rabbit", "Fox")

        # Check the main herd should have rabbits added back but not exceeding max count
        self.assertEqual(48, self.game_manager.main_herd[0].herd_size, "Main herd should now have 48 rabbits")

    def test_main_herd_does_not_go_negative(self):
        """Test that the main herd does not drop below zero when more animals are subtracted than available."""

        # Set herd size to 1 (only 1 rabbit left)
        self.game_manager.main_herd[0].herd_size = 1

        # Player 1 attempts to subtract 3 rabbits
        success, subtracted = self.game_manager.subtract_main_herd("Rabbit", 3)

        # Check that only 1 rabbit is subtracted, and the main herd is now empty
        self.assertTrue(success)
        self.assertEqual(1, subtracted, "Only 1 rabbit should be subtracted since the herd has only 1 rabbit")
        self.assertEqual(0, self.game_manager.main_herd[0].herd_size, "Main herd should not go negative")

    def test_main_herd_capped_at_max_count_after_addition(self):
        """Test that adding animals back to the main herd does not exceed max count."""

        # Set herd size to 58 rabbits (max_count is 60)
        self.game_manager.main_herd[0].herd_size = 58
        self.game_manager.main_herd[0].max_count = 60

        # Player 1 adds 5 rabbits (should only be able to add 2 to reach 60)
        added = self.game_manager.add_to_main_herd("Rabbit", 5)

        # Check that only 2 rabbits were added, and the herd is now capped at 60
        self.assertEqual(2, added, "Only 2 rabbits should be added since the max count is 60")
        self.assertEqual(60, self.game_manager.main_herd[0].herd_size, "Main herd should be capped at 60")

    def test_players_herd_does_not_exceed_total_rabbits_available(self):
        """Test that players' total rabbit herd across all players doesn't exceed the total available in the game."""

        # Set up the main herd size to 60 rabbits
        self.game_manager.main_herd[0].herd_size = 60
        self.game_manager.main_herd[0].max_count = 60

        # Player 1 starts with 5 rabbits
        self.test_player_1.update_herd("Rabbit", 5)
        # Player 2 starts with 4 rabbits
        self.test_player_2.update_herd("Rabbit", 4)

        # Subtract rabbits for Player 1's roll (shouldn't give more than available)
        self.game_manager.process_dice(self.test_player_1, "Rabbit", "Rabbit")

        # Subtract rabbits for Player 2's roll
        self.game_manager.process_dice(self.test_player_2, "Rabbit", "Rabbit")

        # Ensure the total number of rabbits in both player herds and the main herd equals 60
        total_rabbits_in_game = (
                self.test_player_1.get_herd["Rabbit"] +
                self.test_player_2.get_herd["Rabbit"] +
                self.game_manager.main_herd[0].herd_size
        )

        self.assertEqual(60, total_rabbits_in_game,
                         "Total rabbits in players' herds and the main herd should not exceed 60.")


if __name__ == '__main__':
    unittest.main()
