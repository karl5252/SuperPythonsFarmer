import os

from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from game.game_manager import GameManager, check_victory_condition, roll_dice
from game.player import Player

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
    data = request.get_json()
    player_names = data.get('player_names', [])
    ref_game_manager = get_game_manager()

    if len(player_names) == len(set(player_names)) and all(player_names):  # Ensure no empty or duplicate names
        # Store player names (which are serializable) in the session
        session['player_names'] = player_names

        # Initialize the GameManager with the player names
        for index, name in enumerate(player_names):
            ref_game_manager.players.append(Player(name, index))

        # Redirect to the game page
        return redirect(url_for('game'))
    else:
        return jsonify(error="Invalid player names, please try again."), 400


@app.route('/game')
def game():
    ref_game_manager = get_game_manager()

    if not ref_game_manager.players:
        return redirect(url_for('main_menu'))

    # Get player names from session to pass to the game page
    players = session.get('player_names', [])

    return render_template('game.html',
                           players=players,  # Player names to display in the game
                           herd=ref_game_manager.main_herd.get_herd(),  # Main herd to display in the game
                           )


@app.route('/process-menu', methods=['POST'])
def process_menu():
    """Process the player's menu choice."""
    choice = request.json.get('choice')
    result = game_manager.process_menu_choice(choice)
    return jsonify(message=result)


@app.route('/roll-dice', methods=['POST'])
def roll_dice_for_current_player():
    """Route to roll the dice for the current player."""
    data = request.get_json()
    player_index = data.get('player_index')

    # Process the dice roll for the current player
    result_green, result_red = roll_dice()

    current_player = game_manager.players[player_index]
    game_manager.process_dice(current_player, result_green, result_red)

    # Update the player index (move to the next player)
    player_index = (player_index + 1) % len(game_manager.players)  # Loop back to first player if at the end

    # Prepare data to send back to the client
    response_data = {
        'green': result_green,
        'red': result_red,
        'current_player_index': player_index,
        'main_herd': game_manager.main_herd.get_herd(),  # This is now a dictionary
        'player_herd': current_player.get_herd()  # This is now a dictionary
    }

    return jsonify(response_data)


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


@app.route('/exchange', methods=['POST'])
def exchange_animals():
    data = request.get_json()

    player1_index = data['player1_index']
    player2_index = data['player2_index']
    request_index = data.get('request_index')  # Assuming we pass the index or ID of the exchange request

    # Retrieve players involved
    player1 = game_manager.players[player1_index]
    player2 = game_manager.players[player2_index]

    # Retrieve the exchange request based on its index or unique ID
    if 0 <= request_index < len(game_manager.exchange_requests):
        exchange_request = game_manager.exchange_requests[request_index]

        # Process the exchange using the stored count1 and count2 in the request
        if game_manager.process_exchange(player1, player2, exchange_request.from_animal, exchange_request.to_animal, exchange_request.count1, exchange_request.count2):
            exchange_request.status = 'completed'  # Mark the request as completed
            return jsonify(success=True, message="Exchange completed!")
        else:
            return jsonify(success=False, message="Exchange failed. Check animal counts.")
    else:
        return jsonify(success=False, message="Invalid exchange request.")



@app.route('/reset-game', methods=['POST'])
def reset_game():
    """Reset the game state."""
    game_manager.reset_game()
    return jsonify(success=True, message="Game reset successfully.")


if __name__ == '__main__':
    app.run(debug=True)
