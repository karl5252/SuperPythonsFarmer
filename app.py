""" Main application file for the game. """
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
    """Start the game with the given player names."""
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

    return jsonify(error="Invalid player names, please try again."), 400


@app.route('/game')
def game():
    """Render the game page."""
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
    # player_index = (player_index + 1) % len(game_manager.players)  # Loop back to first player if at the end

    # Prepare data to send back to the client
    response_data = {
        'green': result_green,
        'red': result_red,
        'current_player_index': player_index,
        'main_herd': game_manager.main_herd.get_herd(),  # This is now a dictionary
        'player_herd': current_player.get_herd()  # This is now a dictionary
    }
    #player_index = (player_index + 1) % len(game_manager.players)

    return jsonify(response_data)


@app.route('/get-players', methods=['GET'])
def get_players():
    """Route to get the list of players."""
    players = [player.name for player in game_manager.players]
    return jsonify(players=players)


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


@app.route('/post-exchange-request', methods=['POST'])
def post_exchange_request():
    """
    Handles exchange requests between players and/or the main herd.
    If exchanging with the main herd, process immediately.
    If player-to-player, post the request.
    """
    data = request.get_json()

    player_index = data['player_index']
    give_animal = data['give_animal']
    give_count = data['give_count']
    receive_animal = data['receive_animal']
    receive_count = data['receive_count']

    player = game_manager.players[player_index]

    # Check if the exchange is with the main herd
    if data.get('recipient') == 'main-herd':
        # Process the exchange immediately with the main herd
        if game_manager.process_exchange(
                player,
                game_manager.main_herd,
                give_animal,
                receive_animal,
                give_count):
            return jsonify(
                success=True,
                player_herd=player.get_herd(),
                main_herd=game_manager.main_herd.get_herd()
            )

        return jsonify(success=False, message="Main herd exchange failed.")
    else:
        # Handle player-to-player exchange by posting the request
        recipient_name = data['player_index']
        player = game_manager.players[recipient_name]

        if game_manager.post_exchange_request(
                player,
                give_animal,
                receive_animal,
                give_count,
                receive_count):
            return jsonify(success=True, message="Exchange request posted!")

        return jsonify(success=False, message="Failed to post exchange request.")


@app.route('/view-exchange-requests', methods=['GET'])
def view_exchange_requests():
    pending_requests = [
        {
            'requestor_name': request.requestor.name,
            'from_animal': request.from_animal,
            'to_animal': request.to_animal,
            'give_count': request.count1,
            'receive_count': request.count2
        }
        for request in game_manager.exchange_requests if request.status == "pending"
    ]
    return jsonify(requests=pending_requests)


@app.route('/forfeit', methods=['POST'])
def forfeit():
    """Handles when a player forfeits the game."""
    # You can add logic here to handle the forfeit
    game_manager.reset_game()  # Reset game state if that's the desired outcome
    return jsonify(success=True, message="Player forfeited and game reset.")


if __name__ == '__main__':
    app.run(debug=True)
