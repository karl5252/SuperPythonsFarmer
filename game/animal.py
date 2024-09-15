class Animal:
    """base Animal class"""
    herd_size: object

    def __init__(self, count: object) -> object:
        self.herd_size = count
        self.max_count = count

    def subtract_from_herd(self, count):
        """Subtract count from the herd. Return True if successful, False otherwise."""
        if self.herd_size - count >= 0:
            self.herd_size -= count
            return True
        return False


class Rabbit(Animal):
    pass


class Sheep(Animal):
    pass


class Pig(Animal):
    pass


class Cow(Animal):
    pass


class Horse(Animal):
    pass


class Foxhound(Animal):
    pass


class Wolfhound(Animal):
    pass
