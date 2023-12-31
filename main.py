import random
from enum import Enum


class GameState(Enum):
    MAIN_MENU = 0
    IN_GAME = 1
    GAME_OVER = 2


class Animal:
    """base Animal class"""
    max_count: int = 0

    def _init_(self, count):
        self.count = min(count, self.max_count)


class Rabbit(Animal):
    max_count = 60


class Sheep(Animal):
    max_count = 24


class Pig(Animal):
    max_count = 20


class Cow(Animal):
    max_count = 12


class Horse(Animal):
    max_count = 6


class Foxhound(Animal):
    max_count = 4


class Wolfhound(Animal):
    max_count = 2


class Player:
    def __init__(self):
        self.herd = {"Rabbit": 0, "Sheep": 0, "Pig": 0, "Cow": 0, "Horse": 0, "Foxhound": 0, "Wolfhound": 0}

    def get_herd(self):
        return self.herd

    def update_herd(self, new_herd):
        """Update herd with new dict"""
        self.herd.update(new_herd)


class ExchangeBoard:
    """class to handle animals exchange rates."""
    exchange_rates = {}

    @classmethod
    def set_exchange_rate(cls, from_animal, to_animal, ratio):
        cls.exchange_rates[(from_animal, to_animal)] = ratio

    @classmethod
    def get_exchange_rate(cls, from_animal, to_animal):
        return cls.exchange_rates.get((from_animal, to_animal), 0)


class GameManager:
    def __init__(self):
        self.players = [Player(), Player()]
        self.current_player_index = 0
        self.main_herd = [Rabbit(), Sheep(), Pig(), Cow(), Horse(), Foxhound(), Wolfhound()]
        self.exchange_board = ExchangeBoard()
        self.state = GameState.MAIN_MENU

        # Display instructions when the game starts
        print("initialised")
        print(self.state)
        # self.start_up()

    def start_up(self):
        while True:
            if self.state == GameState.MAIN_MENU:
                self.main_menu()
            elif self.state == GameState.IN_GAME:
                self.play()
            elif self.state == GameState.GAME_OVER:
                self.game_over()

    def main_menu(self):
        print("Welcome to Super Farmer!")

        while True:
            print("\n\n\nMAIN MENU")
            print("1. Instructions")
            print("2. Start Game")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.show_instructions()
            elif choice == "2":
                self.play()
                print("game start")
                break
            elif choice == "3":
                print("bye")
                exit()

    def show_instructions(self):
        print("Super Farmer Game Instructions:")
        print("1. Roll the dice to determine the animals you get.")
        print("2. Each face of the dice represents a different animal:")
        print(" - Cow, Pig, Rabbit, Sheep, Wolf, Fox, Horse.")
        print("3. The first animals of a given type are obtained by rolling two of the same animal.")
        print("4. If you have a pair of animals, you get the number of pairs instead of one.")
        print("5. Exchange rules:")
        print(" - 6 Rabbits = 1 Sheep")
        print(" - 2 Sheep = 1 Pig")
        print(" - 3 Pigs = 1 Cow")
        print(" - 2 Cows = 1 Horse")
        print("6. The first Cow and Horse can only be obtained via exchange.")
        print("7. Beware of the Wolf - it eats all animals except Horses. Use a Wolfhound to chase it away.")
        print("8. The Fox eats all Rabbits unless you have a Foxhound.")
        print("9. Goal: Collect all types of animals to win!")
        print("10. Enjoy the game and have fun!")
        self.state = GameState.MAIN_MENU

    def roll_dice(self):
        dice_green_faces = ['Cow', 'Pig', 'Rabbit', 'Rabbit', 'Rabbit', 'Sheep', 'Rabbit', 'Sheep', 'Rabbit', 'Sheep',
                            'Rabbit', 'Wolf']
        dice_red_faces = ['Horse', 'Pig', 'Rabbit', 'Sheep', 'Rabbit', 'Rabbit', 'Pig', 'Rabbit', 'Rabbit', 'Sheep',
                          'Rabbit', 'Fox']

        result_green = random.choice(dice_green_faces)
        result_red = random.choice(dice_red_faces)

        return result_green, result_red

    def process_dice(self, current_player: Player, result_green: str, result_red: str):
        # result_green, result_red = self.roll_dice()
        # print(f"Dice Results: Green - {result_green}, Red - {result_red}")

        green_animal_count = current_player.get_herd().get(result_green, 0)
        red_animal_count = current_player.get_herd().get(result_red, 0)

        # # Case fox is rolled
        if result_green == "Fox" or result_red == "Fox":
            print("Fox was rolled. What does the fox say? RINDINDINDIN!")
            if current_player.get_herd()["Foxhound"] > 0:
                print("'Woof Woof motherfucker!' Foxhound is in herd. No animals lost to fox. Removing foxhound.")
                current_player.update_herd({"Foxhound": current_player.get_herd()["Foxhound"] - 1})
            else:
                print("Foxhound is not in herd. Loosing rabbits.")
                return_amount = current_player.get_herd()["Rabbit"]
                current_player.update_herd({"Rabbit": 0})
                self.main_herd[0].max_count += return_amount
        # # Case wolf is rolled
        # # Case 1: Player has no animals in his herd
        if green_animal_count == 0 and red_animal_count == 0:
            print("No animals in player herd to update.")
            # return
        # # Case 2: Dice results match, calculate number of pairs he has and add to herd OR add player one animal
        if result_green == result_red:
            print("Same animal on both dice. Increasing herd.")
            if current_player.get_herd()[result_green] > 0:
                current_count = current_player.get_herd()[result_green]
                green_pairs = current_player.get_herd()[result_green] // 2
                # self.main_herd[0].max_count -= green_pairs
                if self.subtract_main_herd(result_green, green_pairs):
                    current_player.update_herd({result_green: current_count + green_pairs})
            else:
                if str(self.main_herd[0].__class__.__name__) == result_green:
                    # self.main_herd[0].max_count -= 1
                    if self.subtract_main_herd(result_green, 1):
                        current_herd = current_player.get_herd()
                        current_player.update_herd({result_green: current_herd[result_green] + 1})

        # # Case 3: Player has one animal that matches the dice
        # # Case 4: Green and red dice show the same animal
        # # Case 5: Player has a few pairs of animal type that was returned by either of the dice
        # # Case 6: Player rolls the dice and should be given the animal, however, there is none left in the main herd

    def subtract_main_herd(self, animal_type: str, count: int) -> bool:
        """Subtract count of animal_type from the main herd. Return True if successful, False otherwise.
        :arg animal_type: Type of animal to subtract from the main herd
        :arg count: Number of animals to subtract from the main herd
        :return: True if successful, False otherwise"""
        for animal in self.main_herd:
            if isinstance(animal, Animal) and animal.__class__.__name__ == animal_type:
                if animal.max_count - count >= 0:
                    # If there are enough animals in the main herd, subtract the count
                    animal.max_count -= count
                    return True
                else:
                    # If not enough animals in the main herd, print an error message
                    print(
                        f"Error: Attempted to subtract {count} {animal_type}(s) from the main herd, but not enough "
                        f"available.")
                    return False

    def play(self):
        self.state = GameState.IN_GAME
        for _ in range(len(self.players)):
            current_player = self.players[self.current_player_index]
            print(f"\n\n{current_player}'s Turn:")

            # self.roll_and_process_dice(current_player)
            print(current_player.get_herd())

            # Alternate turn to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_up()
