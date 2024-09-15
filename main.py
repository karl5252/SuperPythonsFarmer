import random
from enum import Enum
from typing import Tuple


class GameState(Enum):
    MAIN_MENU = 0
    IN_GAME = 1
    GAME_OVER = 2


class Animal:
    """base Animal class"""
    herd_size: int = 0

    def __init__(self, count):
        self.herd_size = count
        self.max_count = count

    def subtract_from_herd(self, count):
        """Subtract count from the herd. Return True if successful, False otherwise."""
        if self.herd_size - count >= 0:
            self.herd_size -= count
            return True
        else:
            print(f"Attempted to subtract {count} from the herd, but not enough available.")
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


class Player:
    def __init__(self):
        self.herd = {"Rabbit": 0, "Sheep": 0, "Pig": 0, "Cow": 0, "Horse": 0, "Foxhound": 0, "Wolfhound": 0}

    def get_herd(self):
        return self.herd

    def update_herd(self, animal, new_count):
        """Update herd with new dict"""
        self.herd[animal] = new_count


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
        self.main_herd = [Rabbit(60), Sheep(24), Pig(20), Cow(12), Horse(6), Foxhound(4), Wolfhound(2)]
        self.exchange_board = ExchangeBoard()
        self.state = GameState.MAIN_MENU

        # Display instructions when the game starts
        print("initialised")
        print(self.state)
        # self.start_up()

    def start_up(self):
        while True:
            # initialize exchange board rules
            ExchangeBoard.set_exchange_rate("Rabbit", "Sheep", 6)
            ExchangeBoard.set_exchange_rate("Sheep", "Pig", 2)
            ExchangeBoard.set_exchange_rate("Pig", "Cow", 3)
            ExchangeBoard.set_exchange_rate("Cow", "Horse", 2)

            ExchangeBoard.set_exchange_rate("Horse", "Cow", 1 / 2)
            ExchangeBoard.set_exchange_rate("Cow", "Pig", 1 / 3)
            ExchangeBoard.set_exchange_rate("Pig", "Sheep", 1 / 2)
            ExchangeBoard.set_exchange_rate("Sheep", "Rabbit", 1 / 6)

            ExchangeBoard.set_exchange_rate("Sheep", "Foxhound", 1)
            ExchangeBoard.set_exchange_rate("Cow", "Wolfhound", 1)

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
        print(" - 1 Sheep = 1 Foxhound")
        print(" - 1 Cow = 1 Wolfhound")
        print("6. The first Cow and Horse can only be obtained via exchange.")
        print("7. Beware of the Wolf - it eats all animals except Horses. Use a Wolfhound to chase it away.")
        print("8. The Fox eats all Rabbits unless you have a Foxhound.")
        print("9. Goals: Collect all types of animals to win!")
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
        green_animal_count = current_player.get_herd().get(result_green, 0)
        red_animal_count = current_player.get_herd().get(result_red, 0)

        test_inputs = [result_green, result_red, green_animal_count, red_animal_count]

        # Case fox is rolled
        if result_green == "Fox" or result_red == "Fox":
            if self.handle_fox(current_player):
                return

        # Case wolf is rolled
        if result_green == "Wolf" or result_red == "Wolf":
            if self.handle_wolf(current_player):
                return

        # Case both dice match
        if result_green == result_red:
            common_result = result_green
            if green_animal_count == 0:
                new_count = current_player.get_herd().get(common_result, 0) + 1
                current_player.update_herd(common_result, new_count)
            else:
                pairs = green_animal_count // 2
                success, subtracted_count = self.subtract_main_herd(common_result, pairs)
                if success:
                    lower_val = min(subtracted_count, pairs)
                    new_count = current_player.get_herd().get(common_result, 0) + lower_val
                    current_player.update_herd(common_result, new_count)
        # Case dice do not match
        else:
            test = 0
            # Add one of each animal to the player's herd if the player has at least one of the rolled animal
            if current_player.get_herd().get(result_green, 0) > 0:
                new_count_green = current_player.get_herd().get(result_green, 0) + 1
                current_player.update_herd(result_green, new_count_green)

            if current_player.get_herd().get(result_red, 0) > 0:
                new_count_red = current_player.get_herd().get(result_red, 0) + 1
                current_player.update_herd(result_red, new_count_red)

    def subtract_main_herd(self, animal_type: str, count: int) -> tuple[bool, int]:
        """Subtract count of animal_type from the main herd. Return True if successful, False otherwise.
        :arg animal_type: Type of animal to subtract from the main herd
        :arg count: Number of animals to subtract from the main herd
        :return: True if successful, False otherwise"""
        for animal in self.main_herd:
            if isinstance(animal, Animal) and animal.__class__.__name__ == animal_type:
                if animal.herd_size - count >= 0:
                    # If there are enough animals in the main herd, subtract the count
                    animal.herd_size -= count
                    return True, count
                else:
                    # check if there are enough animals in the main herd
                    leftover = count - animal.herd_size

                    print(
                        f"Attempted to subtract {count} {animal_type}(s) from the main herd, but not enough "
                        f"available. Returning {leftover}")
                    return True, leftover

        return False, 0

    def play(self):
        self.state = GameState.IN_GAME

        for _ in range(len(self.players)):
            current_player = self.players[self.current_player_index]
            print(f"\n\n{current_player}'s Turn:")
            roll = self.roll_dice()
            print(f"Roll: {roll}")
            self.process_dice(current_player, roll[0], roll[1])

            print(current_player.get_herd())
            # add while loop for player to stop and let him decide to perform an exchange
            while True:
                print("Do you want to perform an exchange? (y/n)")
                answer = input()
                if answer == "y":
                    print("Exchange rules (works both ways!):")
                    print(" - 6 Rabbits = 1 Sheep")
                    print(" - 2 Sheep = 1 Pig")
                    print(" - 3 Pigs = 1 Cow")
                    print(" - 2 Cows = 1 Horse")
                    print(" - 1 Sheep = 1 Foxhound")
                    print(" - 1 Cow = 1 Wolfhound")
                    print("Which animal do you want to exchange?")
                    animal_for_exchange = input()
                    print("Which animal do you want to exchange for?")
                    animal_to_exchange_for = input()
                    self.process_exchange(current_player, animal_for_exchange, animal_to_exchange_for)
                    print(current_player.get_herd())
                elif answer == "n":
                    break
                else:
                    print("Please enter y or n")

            # Check if player is a victor and has one of each animal from the list: Rabbit, Sheep, Pig, Cow, Horse
            if set(current_player.get_herd().keys()) == {"Rabbit", "Sheep", "Pig", "Cow", "Horse"}:
                print(f"Congratulations, {current_player}! You are a victor!")
                self.state = GameState.GAME_OVER
                break

            # Alternate turn to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def process_exchange(self, player: Player, animal_for_exchange: str, animal_to_exchange_for: str) -> None:
        """Process exchange of animals."""
        player_herd = player.get_herd()
        exchange_rate = ExchangeBoard.get_exchange_rate(animal_for_exchange, animal_to_exchange_for)

        if exchange_rate >= 1:
            if player_herd[animal_for_exchange] >= exchange_rate:
                # Update player's herd
                player_herd[animal_for_exchange] -= exchange_rate
                player_herd[animal_to_exchange_for] += 1

                # Update main herd in both exchange directions
                self.subtract_main_herd(animal_for_exchange, exchange_rate)
                self.main_herd[0].herd_size += 1

                return
        elif exchange_rate < 1:
            # If direct exchange doesn't work, try the inverse exchange
            inverse_exchange_rate = int(1 / exchange_rate)
            if player_herd[animal_for_exchange] >= 1:
                # Update player's herd
                player_herd[animal_to_exchange_for] += inverse_exchange_rate
                player_herd[animal_for_exchange] -= 1

                # Update main herd in both exchange directions
                self.subtract_main_herd(animal_to_exchange_for, inverse_exchange_rate)
                self.main_herd[0].herd_size += inverse_exchange_rate

                return
        else:
            print("Not enough animals to exchange!")
            return

    def handle_fox(self, current_player: Player) -> bool:
        if not any(current_player.get_herd().values()):
            print("Oh no it's the fox! Luckily there are no animals in player herd to update.")
            return True
        print("Fox was rolled. What does the fox say? RINDINDINDIN!")
        if current_player.get_herd()["Foxhound"] > 0:
            print("'Woof Woof motherfucker!' Foxhound is in herd. No animals lost to fox. Removing foxhound.")
            current_herd = current_player.get_herd()["Foxhound"]
            current_player.update_herd("Foxhound", current_herd - 1)
            return True
        else:
            print("Foxhound is not in herd. Loosing rabbits.")
            return_amount = current_player.get_herd()["Rabbit"]
            current_player.update_herd("Rabbit", 0)
            self.main_herd[0].herd_size += return_amount
            return False

    def handle_wolf(self, current_player) -> bool:
        if not any(current_player.get_herd().values()):
            print("Oh no it's the wolf! Luckily there are no animals in player herd to update.")
            return True
        print("Wolf was rolled. 'AuuuUUUUuuuu... Better hide your children'")
        if current_player.get_herd()["Wolfhound"] > 0:
            print("'Woof Woof motherfucker!' Wolfhound is in herd. No animals lost to wolf. Removing wolfhound.")
            current_herd = current_player.get_herd()["Wolfhound"]
            current_player.update_herd("Wolfhound", current_herd - 1)
            return True
        else:
            print("Wolfhound not in herd. You lost it all save your old jade...")  # jade means old horse
            animals = list(current_player.get_herd().keys())  # Create a copy of the keys
            for animal in animals:
                if animal in ["Horse", "Foxhound"]:
                    continue
                return_amount = current_player.get_herd()[animal]
                current_player.update_herd(animal, 0)
                self.main_herd[0].herd_size += return_amount
            return False


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_up()
