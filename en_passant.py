"""contains a class EnPassantMaker to manage en passant in moves.py"""

from abstract_piece import difference_vector, add_coordinate


class EnPassantMaker:
    def __init__(self):
        self.tile = ""

    def set_en_passant(self, piece, old_location, new_location):
        """if piece is a pawn moving two spaces forward then set the en passant tile to the tile one space behind"""
        h, v = difference_vector(old_location, new_location)
        two_step_pawn_move = piece.type == "pawn" and h == 0 and abs(v) == 2

        if two_step_pawn_move:
            if piece.colour == "white":
                vector = (0, 1)
            else:
                vector = (0, -1)
            self.tile = add_coordinate(old_location, vector)
        else:
            self.tile = ""

    def complete_en_passant(self, location, pieces: dict):
        """if en passant occurs remove the en passant defender piece"""
        if self.tile == location:
            row = location[1]
            if row == "6":
                t = add_coordinate(location, (0, -1))
                del pieces[t]
            elif row == "3":
                t = add_coordinate(location, (0, 1))
                del pieces[t]
