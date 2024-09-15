import tkinter as tk
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
    def __init__(self, root):
        self.players = [Player(), Player()]
        self.current_player_index = 0
        self.main_herd = [Rabbit(60), Sheep(24), Pig(20), Cow(12), Horse(6), Foxhound(4), Wolfhound(2)]
        self.exchange_board = ExchangeBoard()
        self.state = GameState.MAIN_MENU

        # UI elements
        self.root = root
        self.root.title("Super Farmer Game")
        self.menu_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)
        self.setup_ui()

    def setup_ui(self):
        # Main Menu UI
        tk.Label(self.menu_frame, text="Welcome to Super Farmer!", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.menu_frame, text="Start Game", command=self.play).pack(pady=10)
        tk.Button(self.menu_frame, text="Instructions", command=self.show_instructions).pack(pady=10)
        tk.Button(self.menu_frame, text="Exit", command=self.root.quit).pack(pady=10)

        # Game UI
        self.roll_button = tk.Button(self.game_frame, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)

        self.result_label = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.herd_label = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.herd_label.pack(pady=10)

        self.exchange_button = tk.Button(self.game_frame, text="Perform Exchange", command=self.perform_exchange)
        self.exchange_button.pack(pady=10)

        self.back_to_menu_button = tk.Button(self.game_frame, text="Back to Menu", command=self.back_to_menu)
        self.back_to_menu_button.pack(pady=10)

        self.menu_frame.pack()

    def back_to_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack()

    def play(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack()
        self.state = GameState.IN_GAME

    def show_instructions(self):
        instruction_window = tk.Toplevel(self.root)
        instruction_window.title("Instructions")
        tk.Label(instruction_window, text="Super Farmer Game Instructions:\n"
                                          "1. Roll the dice to determine the animals you get.\n"
                                          "2. Exchange animals based on the rules.\n"
                                          "3. First to collect all types wins!",
                 justify=tk.LEFT, padx=10, pady=10).pack()

    def roll_dice(self):
        dice_green_faces = ['Cow', 'Pig', 'Rabbit', 'Rabbit', 'Rabbit', 'Sheep', 'Rabbit', 'Sheep', 'Rabbit', 'Sheep',
                            'Rabbit', 'Wolf']
        dice_red_faces = ['Horse', 'Pig', 'Rabbit', 'Sheep', 'Rabbit', 'Rabbit', 'Pig', 'Rabbit', 'Rabbit', 'Sheep',
                          'Rabbit', 'Fox']

        result_green = random.choice(dice_green_faces)
        result_red = random.choice(dice_red_faces)

        self.result_label.config(text=f"Roll: {result_green}, {result_red}")

        current_player = self.players[self.current_player_index]
        self.process_dice(current_player, result_green, result_red)

        # Update the herd display
        self.herd_label.config(text=f"Herd: {current_player.get_herd()}")

    def process_dice(self, current_player: Player, result_green: str, result_red: str):
        green_animal_count = current_player.get_herd().get(result_green, 0)
        red_animal_count = current_player.get_herd().get(result_red, 0)

        # Case fox is rolled
        if "Fox" in [result_green, result_red]:
            self.handle_fox(current_player)

        # Case wolf is rolled
        if "Wolf" in [result_green, result_red]:
            self.handle_wolf(current_player)

        # Case both dice match
        if result_green == result_red:
            common_result = result_green
            if green_animal_count == 0:
                current_player.update_herd({common_result: current_player.get_herd().get(common_result, 0) + 1})
            else:
                pairs = green_animal_count // 2
                success, subtracted_count = self.subtract_main_herd(common_result, pairs)
                if success:
                    lower_val = min(subtracted_count, pairs)
                    current_player.update_herd({common_result: current_player.get_herd()[common_result] + lower_val})

    def subtract_main_herd(self, animal_type: str, count: int) -> tuple[bool, int]:
        for animal in self.main_herd:
            if isinstance(animal, Animal) and animal.__class__.__name__ == animal_type:
                if animal.herd_size - count >= 0:
                    animal.herd_size -= count
                    return True, count
                else:
                    leftover = count - animal.herd_size
                    return True, leftover
        return False, 0

    def perform_exchange(self):
        # You can add exchange functionality in the same way as the console version
        pass

    def handle_fox(self, current_player: Player):
        if current_player.get_herd()["Foxhound"] > 0:
            current_player.update_herd({"Foxhound": current_player.get_herd()["Foxhound"] - 1})
        else:
            current_player.update_herd({"Rabbit": 0})

    def handle_wolf(self, current_player: Player):
        if current_player.get_herd()["Wolfhound"] > 0:
            current_player.update_herd({"Wolfhound": current_player.get_herd()["Wolfhound"] - 1})
        else:
            animals = current_player.get_herd()
            for animal in ["Rabbit", "Sheep", "Pig", "Cow"]:
                animals[animal] = 0
            current_player.update_herd(animals)


if __name__ == "__main__":
    root = tk.Tk()
    game_manager = GameManager(root)
    root.mainloop()
