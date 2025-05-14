[OUTPUT]
## general overview of the project
Design a simple 2048 game.

## Core Features

The game board should be divided into a 4x4 grid.
Players can control the game using the arrow keys on the keyboard.
Automatically generate two random tiles ("2" or "4") on the board at the start of the game.
Tiles move in the direction pressed (up, down, left, or right) and combine according to the game rules.
A new tile ("2" or "4") is generated in an empty cell after each valid move.
Detect and display a "Game Over" message when no more moves are possible.
Save the current game state (board layout and score) to a local text file.
Load a saved game state from a local text file to continue gameplay.
Keep track of the player's score during the game.

## Language

Use python to develop a pygame application.

### Data Storage

Data will be stored in local text files.

## software functional requirements
1. The system shall display a 4x4 grid as the game board.
2. The system shall allow players to control tile movements using arrow keys (up, down, left, right).
3. The system shall initialize the game by placing two random tiles ("2" or "4") on the board.
4. The system shall move tiles in the direction specified by the player's input.
5. The system shall combine adjacent tiles of the same value when moved together.
6. The system shall generate a new random tile ("2" or "4") in an empty cell after each valid move.
7. The system shall detect when no more moves are possible and display a "Game Over" message.
8. The system shall save the current game state (board layout and score) to a local text file.
9. The system shall load a saved game state from a local text file to resume gameplay.
10. The system shall maintain and display the player's current score during gameplay.
[/OUTPUT]