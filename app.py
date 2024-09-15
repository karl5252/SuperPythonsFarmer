from flask import Flask, jsonify, request, render_template

from game.game_manager import GameManager, check_victory_condition, roll_dice
from game.player import Player

app = Flask(__name__)

# Create an instance of GameManager
game_manager = GameManager()


def get_game_manager():
    # Create an instance of GameManager
    return game_manager


# Default GameManager instance for production


@app.route('/')
def index():
    """The main route for the game."""
    # return jsonify(message="Welcome to Super Farmer!")
    # set two players in the future we will set them from mian menu
    web_game_manager = get_game_manager()
    web_game_manager.players.append(Player("Player 1"))
    web_game_manager.players.append(Player("Player 2"))

    return render_template('index.html')  # Render the HTML page


@app.route('/roll-dice', methods=['POST'])
def roll_dice_for_current_player():
    """Route to roll the dice for the current player."""
    result_green, result_red = roll_dice()
    return jsonify(green=result_green, red=result_red)


@app.route('/get-herd/<int:player_index>', methods=['GET'])
def get_player_herd(player_index):
    """Route to get the herd of the given player."""
    game_manager = get_game_manager()
    test_players = game_manager.players
    player_herd = game_manager.players[player_index].get_herd
    return jsonify(herd=player_herd)


@app.route('/check-victory/<int:player_index>', methods=['GET'])
def check_player_victory(player_index):
    """Route to check if the player has won."""
    game_manager = get_game_manager()
    test_players = game_manager.players
    player = game_manager.players[player_index]
    has_won = check_victory_condition(player)
    return jsonify(victory=has_won)


if __name__ == '__main__':
    app.run(debug=True)
