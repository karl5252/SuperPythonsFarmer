""" Main application file for the game. """
import os
from typing import Dict, Any

from flask import Flask, jsonify, request, render_template, redirect, url_for, session

from game.exchange_board import ExchangeBoard
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


@app.route('/roll-dice', methods=['POST'])
def roll_dice_for_current_player():
    """Route to roll the dice for the current player."""
    player_index = game_manager.current_player_index  # Get the current player's index
    current_player = game_manager.players[player_index]  # Fetch the current player object

    print(f"Processing dice roll for player: {current_player.name}")

    # Process the dice roll
    result_green, result_red = roll_dice()
    game_manager.process_dice(current_player, result_green, result_red)

    # Prepare data to send back to the client (before updating the player index)
    response_data = {
        'green': result_green,
        'red': result_red,
        'current_player_index': player_index,  # Send the current player index (before updating it)
        'player_herd': current_player.get_herd(),  # Player herd after rolling
        'main_herd': game_manager.main_herd.get_herd()  # Main herd
    }

    # Update to the next player
    game_manager.current_player_index = (player_index + 1) % len(game_manager.players)
    print(f"Next player will be: {game_manager.players[game_manager.current_player_index].name}")

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

    player_index = data['player_index']  # The player initiating the exchange
    current_player = game_manager.players[player_index]
    print(f"Processing exchange for player: {current_player.name}")

    give_animal = data['give_animal']
    give_count = data['give_count']
    receive_animal = data['receive_animal']
    receive_count = data['receive_count']

    # Check if the exchange is with the main herd
    if data.get('recipient') == 'main-herd':
        if game_manager.process_exchange(
                current_player,
                game_manager.main_herd,
                give_animal,
                receive_animal,
                give_count,
                receive_count):
            return jsonify(
                success=True,
                player_herd=current_player.get_herd(),
                main_herd=game_manager.main_herd.get_herd()
            )
        return jsonify(success=False, message="Main herd exchange failed.")

    # Handle player-to-player exchange
    else:
        # recipient_index = data['recipient_index']
        # recipient_player = game_manager.players[recipient_index]

        if game_manager.post_exchange_request(
                current_player,
                give_animal,
                receive_animal,
                give_count,
                receive_count):
            return jsonify(success=True, message="Exchange request posted!")

        return jsonify(success=False, message="Failed to post exchange request.")


@app.route('/accept-exchange-request', methods=['POST'])
def accept_exchange_request():
    """Similar to post exchange request, but for the recipient to accept the request."""
    data = request.get_json()

    player_index = data['player_index']  # The player accepting the exchange
    recipient_player = game_manager.players[player_index]
    print(f"Processing exchange for player: {recipient_player.name}")
    print(f"data: {data}")

    give_animal = data['from_animal']
    give_count = data['give_count']
    receive_animal = data['to_animal']
    receive_count = data['receive_count']

    # Find the exchange request to accept
    request_to_accept = None
    print("exchange_requests: ")
    for req in game_manager.exchange_requests:
        print(vars(req))
    for req in game_manager.exchange_requests:
        if req.requestor != recipient_player and \
                req.from_animal == give_animal and \
                req.to_animal == receive_animal and \
                req.amount_offered == give_count and \
                req.amount_wanted == receive_count:
            request_to_accept = req
            break

    if not request_to_accept:
        return jsonify(success=False, message="Exchange request not found.")

    # Process the exchange
    if game_manager.process_exchange(
            request_to_accept.requestor,
            recipient_player,
            give_animal,
            receive_animal,
            give_count,
            receive_count):
        request_to_accept.status = "accepted"
        game_manager.exchange_requests.remove(request_to_accept)
        return jsonify(
            success=True,
            player_herd=recipient_player.get_herd(),
            other_player_herd=request_to_accept.requestor.get_herd()
        )

    return jsonify(success=False, message="Exchange failed.")


@app.route('/view-exchange-requests', methods=['GET'])
def view_exchange_requests():
    """Route to view pending exchange requests."""
    pending_requests = [
        {
            'requestor_name': request.requestor.name,
            'from_animal': request.from_animal,
            'to_animal': request.to_animal,
            'give_count': request.amount_offered,
            'receive_count': request.amount_wanted
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


@app.route('/exchange-rules', methods=['GET'])
def exchange_rules():
    """Render the exchange rules page."""
    rules = ExchangeBoard.get_all_exchange_rates()
    return jsonify(rules)


if __name__ == '__main__':
    app.run(debug=True)
