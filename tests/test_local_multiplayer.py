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



if __name__ == '__main__':
    unittest.main()
