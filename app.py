from flask import Flask, jsonify, request, render_template
from game.game_manager import GameManager, check_victory_condition

app = Flask(__name__)

# Create an instance of GameManager
game_manager = GameManager()


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/main-menu', methods=['GET'])
def main_menu():
    """Return the main menu options."""
    return jsonify(game_manager.main_menu())


@app.route('/process-menu', methods=['POST'])
def process_menu():
    """Process the player's menu choice."""
    choice = request.json.get('choice')
    result = game_manager.process_menu_choice(choice)
    return jsonify(message=result)


@app.route('/roll-dice', methods=['POST'])
def roll_dice_for_current_player():
    """Route to roll the dice for the current player."""
    result_green, result_red = game_manager.roll_dice()
    return jsonify(green=result_green, red=result_red)


@app.route('/get-herd/<int:player_index>', methods=['GET'])
def get_player_herd(player_index):
    """Route to get the herd of the given player."""
    player_herd = game_manager.players[player_index].get_herd()
    return jsonify(herd=player_herd)


@app.route('/check-victory/<int:player_index>', methods=['GET'])
def check_player_victory(player_index):
    """Route to check if the player has won."""
    player = game_manager.players[player_index]
    has_won = check_victory_condition(player)
    return jsonify(victory=has_won)


if __name__ == '__main__':
    app.run(debug=True)
