import unittest
from game.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Test Player", 0)

    def test_get_herd(self):
        self.assertEqual(self.player.get_herd, {
            "Rabbit": 0,
            "Sheep": 0,
            "Pig": 0,
            "Cow": 0,
            "Horse": 0,
            "Foxhound": 0,
            "Wolfhound": 0
        })

    def test_update_herd(self):
        self.player.update_herd("Rabbit", 5)
        self.assertEqual(self.player.get_herd["Rabbit"], 5)


if __name__ == '__main__':
    unittest.main()
