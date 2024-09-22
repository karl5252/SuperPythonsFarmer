# SuperPython Farmer
## Overview
Super Farmer is a classic board game that originated in Poland during World War II, created by mathematician Karol Borsuk. The game involves collecting and exchanging different animals while avoiding predators. It is suitable for 2 to 4 players, aged 7 and above, and takes about 15 to 30 minutes to play.

## Game Components
Two arrays representing 12-sided dice with animal symbols
Virtual images representing tokens of different animals and dogs
## Objective
The goal of the game is to collect at least one of each animal: rabbit, sheep, pig, cow, and horse, and become the super farmer.

## Gameplay
On each turn, the player rolls the dice and either gains, loses, or exchanges animals with the main herd or other players, depending on the outcome.
Players can set exchanges between themselves by any amount, adding a layer of strategic thinking.
Players must watch out for the fox and the wolf, which can attack and steal the animals, unless the player has a small or a big dog to protect them.
The game is based on a mathematical model of animal breeding and exchange, teaching players about counting, probability, and strategy.
## Historical Significance
The game was created during the Nazi occupation of Poland and helped people cope with the hardships of war. It has been reissued several times, with different editions and variations, such as Super Farmer Deluxe, Super Farmer Card Game, and Super Farmer with Stork.

### Implementation Choices:
Decide on the type of game version: command-line (https://github.com/karl5252/SuperPythonsFarmer/tree/c2fd42ed524b29d8c5b363fa9fdb55c7de01f051/game), graphical web-based (latest).
Depending on the choice, use different libraries or frameworks such as Pygame , Flask.
### Design of Data Structures, Functions and architecture:
Use classes, dictionaries, lists, or tuples to store information about players, animals, dice, and exchange rates.
Implement game logic using functions, methods, loops, or conditional statements for actions like rolling dice, gaining or losing animals, exchanging animals, checking for predators, and determining the winner.
### Testing the Code:
Use the unittest library to write and run unit tests for the code.
Utilize unittest subtests for cleaner and less problematic imports.
### Why Python, unittest, and Flask?
Python: A versatile, easy-to-learn, and powerful programming language suitable for various applications such as data analysis, web development, automation, and machine learning.
unittest: A built-in testing framework in Python that supports test automation, aggregation, and independence. It helps ensure that your code works correctly and prevents bugs.
Flask: A lightweight web framework for Python that allows you to create web applications quickly and easily.
By using these tools, you can improve the quality, reliability, and efficiency of your code, saving time and effort by avoiding manual testing and debugging.

## Installation
Clone the repository:
``` git clone https://github.com/yourusername/superpython-farmer.git ```

Navigate to the project directory:
``` cd superpython-farmer ```

Create a virtual environment:
``` python -m venv venv ```

Activate the virtual environment:
On Windows:
``` venv\Scripts\activate ```

On macOS and Linux:
``` source venv/bin/activate ```

Install the required dependencies:
``` pip install -r requirements.txt ```

Usage
Run the application:
``` python app.py ```

Open your web browser and go to http://localhost:5000 to start playing the game.
### Future Plans
Random Events: Add optional random events to the game to spice it up, providing an additional layer of excitement and unpredictability.
### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Please visit my blog: https://www.qabites.blog/
