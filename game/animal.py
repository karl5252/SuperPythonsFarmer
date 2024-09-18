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

    def add_to_herd(self, count):
        """Add count to the herd but ensure herd_size does not exceed max_count."""
        available_space = self.max_count - self.herd_size
        to_add = min(count, available_space)
        self.herd_size += to_add
        return to_add  # Return the number of animals actually added


class Rabbit(Animal):
    """Rabbit class"""
    def __init__(self, count=60):
        super().__init__(count)
        self.max_count = 60


class Sheep(Animal):
    """Sheep class"""
    def __init__(self, count=24):
        super().__init__(count)
        self.max_count = 24


class Pig(Animal):
    """Pig class"""
    def __init__(self, count=20):
        super().__init__(count)
        self.max_count = 20


class Cow(Animal):
    """Cow class"""
    def __init__(self, count=12):
        super().__init__(count)
        self.max_count = 12


class Horse(Animal):
    """Horse class"""
    def __init__(self, count=6):
        super().__init__(count)
        self.max_count = 6


class Foxhound(Animal):
    """Foxhound class"""
    def __init__(self, count=4):
        super().__init__(count)
        self.max_count = 4


class Wolfhound(Animal):
    """Wolfhound class"""
    def __init__(self, count=2):
        super().__init__(count)
        self.max_count = 2
