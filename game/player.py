
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

    def get_herd(self):
        """Return the herd dict"""
        return self.herd

    def update_herd(self, animal: str, new_count: int):
        """Update herd with new dict"""
        self.herd[animal] = new_count

    def transfer_to(self, recipient, animal_type: str, count: int) -> bool:
        """
        Transfer a specified count of animals from the current player (self) to the recipient player.
        Ensures the current player has enough animals to transfer.
        :param recipient: The player receiving the animals
        :param animal_type: Type of animal to transfer
        :param count: Number of animals to transfer
        :return: True if the transfer was successful, False otherwise
        """
        if self.get_herd().get(animal_type, 0) >= count:
            self.update_herd(animal_type, self.get_herd()[animal_type] - count)
            recipient.update_herd(animal_type, recipient.get_herd().get(animal_type, 0) + count)
            return True
        else:
            print(f"Not enough {animal_type} to transfer.")
            return False

    def transfer_from(self, from_player, animal_type, count):
        """
        Transfer animals from another player (or main herd) to this player.
        :param from_player: The player/herd giving the animals.
        :param animal_type: The type of animal to transfer.
        :param count: Number of animals to transfer.
        :return: True if successful, False otherwise.
        """
        return from_player.transfer_to(self, animal_type, count)
