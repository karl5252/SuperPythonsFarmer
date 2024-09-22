"""Game manager module."""
import random
from typing import Union
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
    ExchangeBoard.set_exchange_rate("Foxhound", "Rabbit", 12)  # Exchange 1 Foxhound for 12 Rabbits
    ExchangeBoard.set_exchange_rate("Wolfhound", "Sheep", 6)  # Exchange 1 Wolfhound for 6 Sheep
    ExchangeBoard.set_exchange_rate("Horse", "Pigs", 6)  # Exchange 1 Horse for 6 Pigs
    ExchangeBoard.set_exchange_rate("Horse", "Sheep", 12)  # Exchange 1 Horse for 12 Sheep

    ExchangeBoard.set_exchange_rate("Cow", "Sheep", 6)  # Exchange 1 Cow for 6 Sheep
    ExchangeBoard.set_exchange_rate("Cow", "Rabbits", 36)  # Exchange 1 Cow for 36 Rabbits

    ExchangeBoard.set_exchange_rate("Pig", "Rabbits", 12)  # Exchange 1 Pig for 12 Rabbits


def roll_dice():
    """Roll the dice and return the results."""
    dice_green_faces = ['Cow', 'Pig', 'Rabbit',
                        'Rabbit', 'Rabbit', 'Sheep',
                        'Rabbit', 'Sheep', 'Rabbit',
                        'Sheep', 'Rabbit', 'Wolf']
    dice_red_faces = ['Horse', 'Pig', 'Rabbit',
                      'Sheep', 'Rabbit', 'Rabbit',
                      'Pig', 'Rabbit', 'Rabbit',
                      'Sheep', 'Rabbit', 'Fox']

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
        exchange_board_rules_setup()
        self.exchange_requests = []  # List of active exchange requests

        self.state = GameState.MAIN_MENU

    def add_player(self, name):
        index = len(self.players)
        player = Player(name, index)
        self.players.append(player)

    def start_game(self):
        """Start the game."""
        self.state = GameState.IN_GAME
        exchange_board_rules_setup()
        return "Game started. Players are now playing."

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
        print(f"Processing dice roll for player: {current_player.name} has herd: {current_player.get_herd()}")

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

    def process_exchange(self, player1: Player, player2: Union[Player, None], give_animal: str, receive_animal: str,
                         amount_offered: int, amount_wanted: int) -> bool:
        """
        Process an exchange between two players or a player and the main herd.
        """
        print(f"Players exchange: {player1.name}")
        try:
            amount_offered = int(amount_offered)
            amount_wanted = int(amount_wanted)
        except ValueError:
            print("Error: Invalid amount offered or wanted value.")
            return False

        ratio = amount_offered / amount_wanted

        if ratio >= 1:
            return self._process_normal_exchange(player1, player2, give_animal, receive_animal, ratio, amount_offered,
                                                 amount_wanted)
        else:
            return self._process_inverted_exchange(player1, player2, give_animal, receive_animal, ratio, amount_offered,
                                                   amount_wanted)

    def _process_normal_exchange(self, player1: Player, player2: Union[Player, None], give_animal: str,
                                 receive_animal: str, ratio: float, amount_offered: int, amount_wanted) -> bool:
        # Normal exchange
        print(f"Processing exchange: {give_animal} -> {receive_animal} with ratio {ratio}")
        print(f"Player1 herd: {player1.get_herd()}")
        print(f"Player1 has {amount_offered} {give_animal}(s)")

        # count2 = int(count1 // ratio)
        if isinstance(player2, Player):
            print(f"Player2 herd: {player2.get_herd()}")
            print(f"Player2 needs {amount_wanted} {receive_animal}(s)")
            if player1.get_herd().get(give_animal, 0) >= amount_offered and player2.get_herd().get(receive_animal,
                                                                                                   0) >= amount_wanted:
                return player1.transfer_to(player2, give_animal, amount_offered) and player2.transfer_to(player1,
                                                                                                         receive_animal,
                                                                                                         amount_wanted)
        else:
            print(f"Main Herd: {self.main_herd.get_herd()}")
            print(f"Main Herd needs {amount_wanted} {receive_animal}(s)")
            if player1.get_herd().get(give_animal, 0) >= amount_offered and self.main_herd.get_herd().get(
                    receive_animal, 0) >= amount_wanted:
                return player1.transfer_to(self.main_herd, give_animal, amount_offered) and self.main_herd.transfer_to(
                    player1, receive_animal, amount_wanted)
        return False

    def _process_inverted_exchange(self, player1: Player, player2: Union[Player, None], give_animal: str,
                                   receive_animal: str, ratio: float, amount_offered: int, amount_wanted: int) -> bool:
        # If ratio is less than 1, swap the animals and adjust the ratio
        ratio = 1 / ratio
        print(f"Processing inverted exchange: {give_animal} -> {receive_animal} with ratio {ratio}")
        print(f"Player1 herd: {player1.get_herd()}")
        print(f"Player1 offers {amount_offered} {give_animal}(s)")

        if isinstance(player2, Player):
            print(f"Player2 herd: {player2.get_herd()}")
            print(f"Player2 needs {amount_wanted} {receive_animal}(s)")
            if amount_offered >= 1 and player2.get_herd().get(receive_animal, 0) >= amount_wanted:
                return player1.transfer_to(player2, give_animal, amount_offered) and player2.transfer_to(player1,
                                                                                                         receive_animal,
                                                                                                         amount_wanted)
        else:
            print(f"Main Herd: {self.main_herd.get_herd()}")
            print(f"Main Herd needs {amount_wanted} {receive_animal}(s)")
            if amount_offered >= 1 and self.main_herd.get_herd().get(receive_animal, 0) >= amount_wanted:
                return player1.transfer_to(self.main_herd, give_animal, amount_offered) and self.main_herd.transfer_to(
                    player1, receive_animal, amount_wanted)
        return False

    def post_exchange_request(self, requestor: Player, from_animal: str, to_animal: str, count1: int,
                              count2: int) -> bool:
        """
        Post an exchange request from one player to another or with the main herd.
        count1 is the amount offered, and count2 is the expected amount in return.
        The exchange ratio is calculated as count1 / count2 and stored in the request.
        """
        requestor_herd = requestor.get_herd()

        # Ensure requestor has enough animals to meet the count1 for exchange
        if int(requestor_herd.get(from_animal, 0)) >= int(count1):
            # Calculate the ratio based on amounts offered and expected
            ratio = int(count1) / int(count2)

            # Create a new exchange request with the calculated ratio and offered amounts
            new_request = ExchangeRequest(requestor, from_animal, to_animal, int(count1), int(count2), ratio)
            self.exchange_requests.append(new_request)
            return True
        return False

    def view_exchange_requests(self):
        """View all pending exchange requests."""
        return [request for request in self.exchange_requests if request.status == "pending"]

    def accept_exchange_request(self, player_index: int, request: ExchangeRequest) -> bool:
        """
        Accept an exchange request using the stored count1, count2, and ratio for exchange.
        """
        if request.status == "pending":
            requestor = self.players[request.requestor.index]
            recipient = self.players[player_index]

            # Check if the requestor still has enough animals to fulfill the exchange
            if requestor.get_herd().get(request.from_animal, 0) >= request.amount_wanted:
                # Execute the exchange using the stored amounts and ratio in the request
                request.status = "accepted"
                success = self.process_exchange(requestor, recipient, request.from_animal, request.to_animal,
                                                request.amount_offered, request.amount_wanted)
                if success:
                    self.exchange_requests.remove(request)
                return success
            else:
                request.status = "invalid"
                self.exchange_requests.remove(request)
                return False
        return False

    def invalidate_requests(self):
        """
        Invalidate exchange requests if the requestor no longer has the required animals.
        This method ensures that old requests don’t clutter the pending requests list.
        """
        for request in self.exchange_requests:
            requestor_herd = self.players[request.requestor.index].get_herd()
            if requestor_herd.get(request.from_animal, 0) == 0:
                request.status = "invalid"

    def reset_game(self):
        """Reset the game state."""
        self.herd_modifiable = False
        self.players = []
        self.current_player_index = 0
        self.main_herd = Player("Main Herd", 99)
        self.main_herd.update_herd("Rabbit", 60)
        self.main_herd.update_herd("Sheep", 24)
        self.main_herd.update_herd("Pig", 20)
        self.main_herd.update_herd("Cow", 12)
        self.main_herd.update_herd("Horse", 6)
        self.main_herd.update_herd("Foxhound", 4)
        self.main_herd.update_herd("Wolfhound", 2)
        self.exchange_requests = []
        self.state = GameState.MAIN_MENU
        return "Game reset. Players can now join."
