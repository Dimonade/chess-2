from pieces import Pawn, Rook, Knight, Bishop, Queen, King, eight_letters


def reset_board_pieces(game_pieces: dict, game_tiles: dict, ep, move_number, player):
    def add_piece(piece_type, piece_colour, piece_location):
        d = {'pawn': Pawn, 'rook': Rook, 'knight': Knight, 'bishop': Bishop, 'queen': Queen, 'king': King}
        game_pieces[piece_location] = d[piece_type](piece_colour, piece_location, game_pieces, game_tiles, ep)

    add_piece('rook', 'white', 'a1')
    add_piece('knight', 'white', 'b1')
    add_piece('bishop', 'white', 'c1')
    add_piece('queen', 'white', 'd1')
    add_piece('king', 'white', 'e1')
    add_piece('bishop', 'white', 'f1')
    add_piece('knight', 'white', 'g1')
    add_piece('rook', 'white', 'h1')

    for letter in eight_letters:
        loc = f'{letter}2'
        add_piece('pawn', 'white', loc)

    for letter in eight_letters:
        loc = f'{letter}7'
        add_piece('pawn', 'black', loc)

    add_piece('rook', 'black', 'a8')
    add_piece('knight', 'black', 'b8')
    add_piece('bishop', 'black', 'c8')
    add_piece('queen', 'black', 'd8')
    add_piece('king', 'black', 'e8')
    add_piece('bishop', 'black', 'f8')
    add_piece('knight', 'black', 'g8')
    add_piece('rook', 'black', 'h8')

    for location in game_pieces.keys():
        game_tiles[location].set_piece()

    move_number.set(1)
    player.set('white')