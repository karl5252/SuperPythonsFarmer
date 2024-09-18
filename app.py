import os

from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from game.game_manager import GameManager, check_victory_condition, roll_dice

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Create an instance of GameManager
game_manager = GameManager()


def get_game_manager():
    return game_manager


@app.route('/')
def main_menu():
    """Render the main game page."""
    return render_template('main_menu.html')


@app.route('/start-game', methods=['POST'])
def start_game():
    # Extract player names from the form data
    data = request.get_json()
    player_names = data.get('player_names', [])
    ref_game_manager = get_game_manager()
    print("players on start count: " + str(len(player_names)))
    if len(player_names) == len(set(player_names)) and all(player_names):  # Ensure no empty or duplicate names
        print(player_names)
        ref_game_manager.players = player_names
        print(ref_game_manager.players)
        session['players'] = player_names  # Store player names in session
        return redirect(url_for('game'))
    else:
        return "Invalid player names, please try again."


@app.route('/game')
def game():
    # Retrieve players from session
    players = session.get('players', [])
    return render_template('game.html', players=players)


@app.route('/process-menu', methods=['POST'])
def process_menu():
    """Process the player's menu choice."""
    choice = request.json.get('choice')
    result = game_manager.process_menu_choice(choice)
    return jsonify(message=result)


@app.route('/roll-dice', methods=['POST'])
def roll_dice_for_current_player():
    """Route to roll the dice for the current player."""
    result_green, result_red = roll_dice()
    ref_game_manager = get_game_manager()
    print(ref_game_manager.players)
    current_player_index = ref_game_manager.current_player_index
    current_player = ref_game_manager.players[current_player_index]
    #print(current_player.get_herd)
    #ref_game_manager.process_dice(current_player, result_green, result_red)
    #print(current_player.get_herd)

    return jsonify(green=result_green, red=result_red)


@app.route('/get-herd/<int:player_index>', methods=['GET'])
def get_player_herd(player_index):
    """Route to get the herd of the given player."""
    player_herd = game_manager.players[player_index].get_herd
    return jsonify(herd=player_herd)


@app.route('/check-victory/<int:player_index>', methods=['GET'])
def check_player_victory(player_index):
    """Route to check if the player has won."""
    player = game_manager.players[player_index]
    has_won = check_victory_condition(player)
    return jsonify(victory=has_won)


if __name__ == '__main__':
    app.run(debug=True)
