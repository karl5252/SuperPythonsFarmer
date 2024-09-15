"""Game manager module."""
import random
from game.animal import Animal, Rabbit, Sheep, Pig, Cow, Foxhound, Wolfhound, Horse
from game.exchange_board import ExchangeBoard
from game.exchange_request import ExchangeRequest
from game.game_state import GameState
from game.player import Player


def exchange_board_rules_setup():
    """Set up the exchange board rules."""
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
    # Additional direct exchanges
    ExchangeBoard.set_exchange_rate("Horse", "Pigs", 6)  # Exchange 1 Horse for 6 Pigs
    ExchangeBoard.set_exchange_rate("Horse", "Sheep", 12)  # Exchange 1 Horse for 12 Sheep
    ExchangeBoard.set_exchange_rate("Horse", "Rabbits", 72)  # Exchange 1 Horse for 72 Rabbits

    ExchangeBoard.set_exchange_rate("Cow", "Sheep", 6)  # Exchange 1 Cow for 6 Sheep
    ExchangeBoard.set_exchange_rate("Cow", "Rabbits", 36)  # Exchange 1 Cow for 36 Rabbits

    ExchangeBoard.set_exchange_rate("Pig", "Rabbits", 12)  # Exchange 1 Pig for 12 Rabbits


def roll_dice():
    """Roll the dice and return the results."""
    dice_green_faces = ['Cow', 'Pig', 'Rabbit', 'Rabbit', 'Rabbit', 'Sheep', 'Rabbit', 'Sheep', 'Rabbit', 'Sheep',
                        'Rabbit', 'Wolf']
    dice_red_faces = ['Horse', 'Pig', 'Rabbit', 'Sheep', 'Rabbit', 'Rabbit', 'Pig', 'Rabbit', 'Rabbit', 'Sheep',
                      'Rabbit', 'Fox']

    result_green = random.choice(dice_green_faces)
    result_red = random.choice(dice_red_faces)

    return result_green, result_red


def check_victory_condition(player: Player) -> bool:
    """Check if the player has at least one of each required animal to win the game."""
    required_animals = ["Rabbit", "Sheep", "Pig", "Cow", "Horse"]
    player_herd = player.get_herd

    for animal in required_animals:
        if player_herd.get(animal, 0) < 1:
            return False

    return True


class GameManager:
    """class to manage the game."""

    def __init__(self):
        self.players = []
        self.current_player_index = 0
        self.main_herd = [Rabbit(60), Sheep(24), Pig(20), Cow(12), Horse(6), Foxhound(4), Wolfhound(2)]
        self.exchange_requests = []  # List of active exchange requests
        self.state = GameState.MAIN_MENU

    def start_game(self):
        """Start the game."""
        self.state = GameState.IN_GAME
        exchange_board_rules_setup()
        return "Game started. Players are now playing."

    def main_menu(self):
        """Return menu options instead of printing."""
        return {
            "1": "Show Instructions",
            "2": "Start Game",
            "3": "Exit"
        }

    def show_instructions(self):
        """Return game instructions as a string instead of printing."""
        return (
            "Super Farmer Game Instructions:\n"
            "1. Roll the dice to determine the animals you get.\n"
            "2. Each face of the dice represents a different animal:\n"
            " - Cow, Pig, Rabbit, Sheep, Wolf, Fox, Horse.\n"
            "3. The first animals of a given type are obtained by rolling two of the same animal.\n"
            "4. If you have a pair of animals, you get the number of pairs instead of one.\n"
            "5. Exchange rules:\n"
            " - 6 Rabbits = 1 Sheep\n"
            " - 2 Sheep = 1 Pig\n"
            " - 3 Pigs = 1 Cow\n"
            " - 2 Cows = 1 Horse\n"
            " - 1 Sheep = 1 Foxhound\n"
            " - 1 Cow = 1 Wolfhound\n"
            "6. The first Cow and Horse can only be obtained via exchange.\n"
            "7. Beware of the Wolf - it eats all animals except Horses. Use a Wolfhound to chase it away.\n"
            "8. The Fox eats all Rabbits unless you have a Foxhound.\n"
            "9. Goals: Collect all types of animals to win!\n"
            "10. Enjoy the game and have fun!\n\n\n"
            "Visit my blog for more details: https://www.qabites.blog/\n\n\n"

        )

    def process_menu_choice(self, choice):
        """Process the player's menu choice."""
        if choice == "1":
            return self.show_instructions()
        elif choice == "2":
            return self.start_game()
        elif choice == "3":
            return "Exiting game."
        else:
            return "Invalid choice."

    def process_dice(self, current_player: Player, result_green: str, result_red: str):
        """Process the dice roll results and update the player's herd accordingly."""
        green_animal_count = current_player.get_herd.get(result_green, 0)
        red_animal_count = current_player.get_herd.get(result_red, 0)

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
                new_count = current_player.get_herd.get(common_result, 0) + 1
                current_player.update_herd(common_result, new_count)
            else:
                pairs = green_animal_count // 2
                success, subtracted_count = self.subtract_main_herd(common_result, pairs)
                if success:
                    lower_val = min(subtracted_count, pairs)
                    new_count = current_player.get_herd.get(common_result, 0) + lower_val
                    current_player.update_herd(common_result, new_count)
        # Case dice do not match
        else:
            test = 0
            # Add one of each animal to the player's herd if the player has at least one of the rolled animal
            if current_player.get_herd.get(result_green, 0) > 0:
                new_count_green = current_player.get_herd.get(result_green, 0) + 1
                current_player.update_herd(result_green, new_count_green)

            if current_player.get_herd.get(result_red, 0) > 0:
                new_count_red = current_player.get_herd.get(result_red, 0) + 1
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
            print(f"\n\n{current_player.name}'s Turn:")
            roll = roll_dice()
            print(f"Roll: {roll}")
            self.process_dice(current_player, roll[0], roll[1])

            print(current_player.get_herd)
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
                    print(current_player.get_herd)
                elif answer == "n":
                    break
                else:
                    print("Please enter y or n")

            # Check if player is a victor and has one of each animal from the list: Rabbit, Sheep, Pig, Cow, Horse

            if check_victory_condition(current_player):
                print(f"{current_player.name} is the victor!")
                self.state = GameState.GAME_OVER
                break

            # Alternate turn to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def process_exchange(self, player: Player, animal_for_exchange: str, animal_to_exchange_for: str) -> None:
        """Process exchange of animals."""
        player_herd = player.get_herd
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
        if not any(current_player.get_herd.values()):
            print("Oh no it's the fox! Luckily there are no animals in player herd to update.")
            return True
        print("Fox was rolled. What does the fox say? RINDINDINDIN!")
        if current_player.get_herd["Foxhound"] > 0:
            print("'Woof Woof motherfucker!' Foxhound is in herd. No animals lost to fox. Removing foxhound.")
            current_herd = current_player.get_herd["Foxhound"]
            current_player.update_herd("Foxhound", current_herd - 1)
            return True
        else:
            print("Foxhound is not in herd. Loosing rabbits.")
            return_amount = current_player.get_herd["Rabbit"]
            current_player.update_herd("Rabbit", 0)
            self.main_herd[0].herd_size += return_amount
            return False

    def handle_wolf(self, current_player) -> bool:
        if not any(current_player.get_herd.values()):
            print("Oh no it's the wolf! Luckily there are no animals in player herd to update.")
            return True
        print("Wolf was rolled. 'AuuuUUUUuuuu... Better hide your children'")
        if current_player.get_herd["Wolfhound"] > 0:
            print("'Woof Woof motherfucker!' Wolfhound is in herd. No animals lost to wolf. Removing wolfhound.")
            current_herd = current_player.get_herd["Wolfhound"]
            current_player.update_herd("Wolfhound", current_herd - 1)
            return True
        else:
            print("Wolfhound not in herd. You lost it all save your old jade...")  # jade means old horse
            animals = list(current_player.get_herd.keys())  # Create a copy of the keys
            for animal in animals:
                if animal in ["Horse", "Foxhound"]:
                    continue
                return_amount = current_player.get_herd[animal]
                current_player.update_herd(animal, 0)
                self.main_herd[0].herd_size += return_amount
            return False

    def post_exchange_request(self, requestor, from_animal, to_animal):
        """Post an exchange request."""
        # Validate if the requestor has enough animals to make the request
        requestor_herd = requestor.get_herd
        if requestor_herd[from_animal] > 0:
            new_request = ExchangeRequest(requestor, from_animal, to_animal)
            self.exchange_requests.append(new_request)
            return True
        return False

    def view_exchange_requests(self):
        """View all pending exchange requests."""
        return [request for request in self.exchange_requests if request.status == "pending"]

    def accept_exchange_request(self, player_index, request):
        """Accept an exchange request."""
        if request.status == "pending":
            requestor = self.players[request.requestor.index]
            recipient = self.players[player_index]

            # Check if requestor still has enough animals to fulfill the request
            if requestor.get_herd[request.from_animal] > 0:
                requestor.update_herd(request.from_animal, requestor.get_herd[request.from_animal] - 1)
                recipient.update_herd(request.to_animal, recipient.get_herd[request.to_animal] + 1)
                request.status = "accepted"
                return True
            else:
                request.status = "pending"
                return False
        return False

    def invalidate_requests(self):
        """Invalidate exchange requests if the requestor no longer has the necessary animals."""
        for request in self.exchange_requests:
            requestor_herd = self.players[request.requestor.index].get_herd
            if requestor_herd[request.from_animal] == 0:
                request.status = "invalid"

