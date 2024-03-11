from moves import MoveMaker
from setup_board import reset_board_pieces
from setup_GUI import create_tkinter_window
from tile import create_tiles


def create_game_engine():
    moves = []
    game_tiles = {}
    game_pieces = {}
    checks = {"white": False, "black": False}

    m = MoveMaker(
        moves,
        game_tiles,
        game_pieces,
        player,
        checks,
        root,
        move_number,
        print_move_on,
    )
    create_tiles(game_tiles, game_pieces, chessboard_frame, m)

    return moves, m, game_pieces, game_tiles, checks


if __name__ == "__main__":
    root, chessboard_frame, player, move_number, print_move_on = create_tkinter_window()
    moves, m, game_pieces, game_tiles, checks = create_game_engine()
    reset_board_pieces(game_pieces, game_tiles, move_number, player)

    root.mainloop()
