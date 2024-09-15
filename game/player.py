
class Player:
    """class to represent a player in the game."""

    def __init__(self, name: object = None, index = 0) -> object:
        self.name = name
        self.index = index
        self.herd = {
            "Rabbit": 0,
            "Sheep": 0,
            "Pig": 0,
            "Cow": 0,
            "Horse": 0,
            "Foxhound": 0,
            "Wolfhound": 0
        }

    @property
    def get_herd(self):
        return self.herd

    def update_herd(self, animal: str, new_count: int):
        """Update herd with new dict"""
        self.herd[animal] = new_count
