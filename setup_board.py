from constants import Letter, Colour
from pieces import PieceName


def create_pieces(game):
    def add_piece(piece_type, piece_colour, piece_location):
        game.pieces[piece_location] = piece_type.get_piece_class()(
            piece_colour.name.lower(), piece_location, game
        )

    add_piece(PieceName.ROOK, Colour.WHITE, "a1")
    add_piece(PieceName.KNIGHT, Colour.WHITE, "b1")
    add_piece(PieceName.BISHOP, Colour.WHITE, "c1")
    add_piece(PieceName.QUEEN, Colour.WHITE, "d1")
    add_piece(PieceName.KING, Colour.WHITE, "e1")
    add_piece(PieceName.BISHOP, Colour.WHITE, "f1")
    add_piece(PieceName.KNIGHT, Colour.WHITE, "g1")
    add_piece(PieceName.ROOK, Colour.WHITE, "h1")

    for letter in list(Letter):
        loc = f"{letter.name.lower()}2"
        add_piece(PieceName.PAWN, Colour.WHITE, loc)

    for letter in list(Letter):
        loc = f"{letter.name.lower()}7"
        add_piece(PieceName.PAWN, Colour.BLACK, loc)

    add_piece(PieceName.ROOK, Colour.BLACK, "a8")
    add_piece(PieceName.KNIGHT, Colour.BLACK, "b8")
    add_piece(PieceName.BISHOP, Colour.BLACK, "c8")
    add_piece(PieceName.QUEEN, Colour.BLACK, "d8")
    add_piece(PieceName.KING, Colour.BLACK, "e8")
    add_piece(PieceName.BISHOP, Colour.BLACK, "f8")
    add_piece(PieceName.KNIGHT, Colour.BLACK, "g8")
    add_piece(PieceName.ROOK, Colour.BLACK, "h8")

    for location in game.pieces.keys():
        game.tiles[location].set_piece()

    game.move_number.set(1)
    game.player.set(Colour.WHITE.name.lower())
