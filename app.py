from flask import Flask, jsonify, request

from game.game_manager import GameManager

app = Flask(__name__)

# Create an instance of GameManager
game_manager = GameManager()


@app.route('/')
def index():
    """The main route for the game."""
    return jsonify(message="Welcome to Super Farmer!")


if __name__ == '__main__':
    app.run(debug=True)
