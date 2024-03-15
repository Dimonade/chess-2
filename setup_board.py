"""adds the pieces to the board"""

from constants import Letter, Colour
from pieces import PieceEnum


def create_pieces(game):
    def add_piece(piece_type, piece_colour, piece_location):
        game.pieces[piece_location] = piece_type.get_piece_class()(
            piece_colour.name.lower(), piece_location, game
        )

    colour = Colour.WHITE

    add_piece(PieceEnum.ROOK, colour, "a1")
    add_piece(PieceEnum.KNIGHT, colour, "b1")
    add_piece(PieceEnum.BISHOP, colour, "c1")
    add_piece(PieceEnum.QUEEN, colour, "d1")
    add_piece(PieceEnum.KING, colour, "e1")
    add_piece(PieceEnum.BISHOP, colour, "f1")
    add_piece(PieceEnum.KNIGHT, colour, "g1")
    add_piece(PieceEnum.ROOK, colour, "h1")

    for letter in list(Letter):
        loc = f"{letter.name.lower()}2"
        add_piece(PieceEnum.PAWN, colour, loc)

    colour = Colour.BLACK

    for letter in list(Letter):
        loc = f"{letter.name.lower()}7"
        add_piece(PieceEnum.PAWN, colour, loc)

    add_piece(PieceEnum.ROOK, colour, "a8")
    add_piece(PieceEnum.KNIGHT, colour, "b8")
    add_piece(PieceEnum.BISHOP, colour, "c8")
    add_piece(PieceEnum.QUEEN, colour, "d8")
    add_piece(PieceEnum.KING, colour, "e8")
    add_piece(PieceEnum.BISHOP, colour, "f8")
    add_piece(PieceEnum.KNIGHT, colour, "g8")
    add_piece(PieceEnum.ROOK, colour, "h8")

    for location in game.pieces.keys():
        game.tiles[location].set_piece()

    game.move_number.set(1)
    game.player.set(Colour.WHITE.name.lower())
