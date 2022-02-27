# Description

This is a python implementation of chess that allows two players to play locally against each other through the terminal. It uses unicode characters
to display the pieces and includes two different "boards" to play on: a less cluttered board that uses spaces as tiles so that pieces are more
easily seen and a board that uses unicode squares of alternating colors. Currently, it only supports two players moving and taking pieces around 
the board and does not have a win verification system.

# Installation

To install PYChess, you can fork/clone this repo. Navigate to the src directory and use `python main.py` to run the program

# Future updates
### Short term
At the moment, the scripts allow very basic chess movement. I plan to implement:
- a move verification method for the king that ensures a move doesn't place it in check
- a win condition for when the king has no possible moves
- a castling option (the ability to switch a rook and the king if they have not been moved yet)
- an en pasant condition (where an unmoved pawn moves two spaces late in the game)


### Long term
Some large scale updates include:
- switching from a terminal base to a gui-based system using tkinter and sprites
- the ability to play against a cpu instead of another local player
- a save/load system that saves and loads past/incomplete sessions for specific players
- a redo/undo system for finished sessions that allow for analysis of the game
- a win percentage calculation that determines a team's win percentage after a move