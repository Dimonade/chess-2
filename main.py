"""entry point into the chess game"""

from game import Game
from moves import MoveMaker
from setup_board import create_pieces
from setup_GUI import create_tkinter_window
from tile import create_tiles


if __name__ == "__main__":
    gui_components = create_tkinter_window()  # creates the tkinter gui application
    game = Game(gui_components)  # creates the game
    game.move_maker = MoveMaker(game)  # creates a move maker to manage game moves
    create_tiles(game)  # creates all the tiles and adds them to game
    create_pieces(game)  # creates all the pieces and adds them to the game

    game.root.mainloop()
