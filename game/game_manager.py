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
    player_herd = player.get_herd()

    for animal in required_animals:
        if player_herd.get(animal, 0) < 1:
            return False

    return True


class GameManager:
    """class to manage the game."""

    def __init__(self):
        self.herd_modifiable = False
        self.players = []
        self.current_player_index = 0
        # Initialize Main Herd as a Player-like object
        self.main_herd = Player("Main Herd", 99)
        self.main_herd.update_herd("Rabbit", 60)
        self.main_herd.update_herd("Sheep", 24)
        self.main_herd.update_herd("Pig", 20)
        self.main_herd.update_herd("Cow", 12)
        self.main_herd.update_herd("Horse", 6)
        self.main_herd.update_herd("Foxhound", 4)
        self.main_herd.update_herd("Wolfhound", 2)
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
        """Process dice roll and transfer animals between the main herd and the current player."""
        if result_green == "Fox" or result_red == "Fox":
            if self.handle_fox(current_player):
                return
        if result_green == "Wolf" or result_red == "Wolf":
            if self.handle_wolf(current_player):
                return

        # Matched dice: process pairs
        if result_green == result_red:
            pairs = current_player.get_herd().get(result_green, 0) // 2
            available_animals = self.main_herd.get_herd().get(result_green, 0)
            transfer_count = min(available_animals, max(pairs, 1))
            self.main_herd.transfer_to(current_player, result_green, transfer_count)
        else:
            # Borrow one rabbit from the main herd if the player has an odd number of rabbits
            if current_player.get_herd().get(result_green, 0) % 2 != 0:
                if self.main_herd.get_herd().get(result_green, 0) > 0:
                    self.main_herd.transfer_to(current_player, result_green, 1)
            # Transfer one of each animal rolled on the dice to the player if available in the main herd
            if current_player.get_herd().get(result_green, 0) > 0:
                self.main_herd.transfer_to(current_player, result_green, 1)
            if current_player.get_herd().get(result_red, 0) > 0:
                self.main_herd.transfer_to(current_player, result_red, 1)

    def handle_fox(self, current_player: Player) -> bool:
        """Handle the fox event."""
        if current_player.get_herd().get("Foxhound", 0) > 0:
            current_player.transfer_to(self.main_herd, "Foxhound", 1)
            return True
        else:
            rabbits = current_player.get_herd()["Rabbit"]
            current_player.transfer_to(self.main_herd, "Rabbit", rabbits)
            return False

    def handle_wolf(self, current_player: Player) -> bool:
        """Handle the wolf event."""
        if current_player.get_herd().get("Wolfhound", 0) > 0:
            current_player.transfer_to(self.main_herd, "Wolfhound", 1)
            return True
        else:
            for animal in current_player.get_herd():
                if animal not in ["Horse", "Foxhound"]:
                    lost_animals = current_player.get_herd()[animal]
                    current_player.transfer_to(self.main_herd, animal, lost_animals)
            return False

    def play(self):
        self.state = GameState.IN_GAME

        for _ in range(len(self.players)):
            current_player = self.players[self.current_player_index]
            print(f"\n\n{current_player.name}'s Turn:")
            roll = roll_dice()
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

            if check_victory_condition(current_player):
                print(f"{current_player.name} is the victor!")
                self.state = GameState.GAME_OVER
                break

            # Alternate turn to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def process_exchange(self, player1: Player, player2: Player, animal1: str, animal2: str, ratio: float) -> bool:
        """
        Process an exchange between two players (including Main Herd as player).
        Handles both normal and inverse exchanges.
        """
        # Get the count of animal1 in player1's herd
        count1 = player1.get_herd().get(animal1, 0)

        # Check if it's a normal or inverse exchange based on the ratio
        if ratio >= 1:  # Normal exchange (e.g., 6 Rabbits = 1 Sheep)
            count2 = int(count1 // ratio)  # Number of animal2 player1 should receive
            if count1 >= ratio and player2.get_herd().get(animal2, 0) >= count2:
                return player1.transfer_to(player2, animal1, int(ratio)) and player2.transfer_to(player1, animal2,
                                                                                                 count2)
        else:  # Inverse exchange (e.g., 1 Horse = 2 Cows)
            count2 = int(count1 * (1 / ratio))  # Number of animal2 player1 should receive
            if count1 >= 1 and player2.get_herd().get(animal2, 0) >= count2:
                return player1.transfer_to(player2, animal1, 1) and player2.transfer_to(player1, animal2, count2)

        return False  # If conditions are not met, return False

    def post_exchange_request(self, requestor, from_animal, to_animal):
        """Post an exchange request."""
        # Validate if the requestor has enough animals to make the request
        requestor_herd = requestor.get_herd()
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
            if requestor.get_herd()[request.from_animal] > 0:
                requestor.update_herd(request.from_animal, requestor.get_herd()[request.from_animal] - 1)
                recipient.update_herd(request.to_animal, recipient.get_herd()[request.to_animal] + 1)
                request.status = "accepted"
                return True
            else:
                request.status = "pending"
                return False
        return False

    def invalidate_requests(self):
        """Invalidate exchange requests if the requestor no longer has the necessary animals."""
        for request in self.exchange_requests:
            requestor_herd = self.players[request.requestor.index].get_herd()
            if requestor_herd[request.from_animal] == 0:
                request.status = "invalid"

