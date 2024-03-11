from game import Game
from moves import MoveMaker
from setup_board import create_pieces
from setup_GUI import create_tkinter_window
from tile import create_tiles


if __name__ == "__main__":
    gui_components = create_tkinter_window()
    game = Game(gui_components)
    m = MoveMaker(game)
    create_tiles(game, m)
    create_pieces(game)

    game.root.mainloop()
