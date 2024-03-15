"""contains all the different piece classes e.g. Pawn, Rook etc."""

from abstract_piece import Piece, difference_vector
from enum import Enum


class PieceEnum(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

    def get_abbreviation(self):
        name = self.name
        if name == "PAWN":
            return ""
        elif name == "KNIGHT":
            return "N"
        else:
            return name[0]

    def get_piece_class(self):
        return [Pawn, Rook, Knight, Bishop, Queen, King][self.value - 1]


class Pawn(Piece):
    def __init__(self, colour, location, game):
        super().__init__(colour, "pawn", location, game)

    def piece_custom_rule(self, target_location):
        """returns true is target_location can be reached by pawn"""
        h, v = difference_vector(target_location, self.location)
        # h is horizontal, v is vertical

        v_valid = self.vertical_movement_is_valid(v)
        h_valid = self.horizontal_movement_is_valid(h, target_location)
        not_knight_move = {abs(h), abs(v)} != {1, 2}
        only_moved_two_spaces_if_unmoved = self.unmoved or abs(v) == 1

        conditions = [
            v_valid,
            h_valid,
            not_knight_move,
            only_moved_two_spaces_if_unmoved,
        ]
        return all(conditions)

    def vertical_movement_is_valid(self, vertical_movement):
        white_valid = self.colour == "white" and vertical_movement in {1, 2}
        black_valid = self.colour == "black" and vertical_movement in {-1, -2}
        return white_valid or black_valid

    def horizontal_movement_is_valid(self, horizontal_movement, target_location):
        h = horizontal_movement
        piece_is_present = target_location in self.game.pieces.keys()
        en_passant_tile = self.game.move_maker.ep.tile
        non_attacking_valid = h == 0 and not piece_is_present
        attacking_valid = h in {-1, 1} and (
            piece_is_present or target_location == en_passant_tile
        )
        return non_attacking_valid or attacking_valid

    def is_attack_valid(self, m1, m2, location):
        horizontal_valid = abs(m1) == 1

        white_valid = m2 == 1 and self.colour == "white"
        black_valid = m2 == -1 and self.colour == "black"

        vertical_valid = white_valid or black_valid

        return horizontal_valid and vertical_valid


class Rook(Piece):
    def __init__(self, colour, location, game):
        super().__init__(colour, "rook", location, game)

    def piece_custom_rule(self, target_location):
        """is orthogonal"""
        m1, m2 = difference_vector(target_location, self.location)
        return 0 in {m1, m2}


class Knight(Piece):
    def __init__(self, colour, location, game):
        super().__init__(colour, "knight", location, game)

    def piece_custom_rule(self, target_location):
        """is L shape"""
        m1, m2 = difference_vector(target_location, self.location)
        return {abs(m1), abs(m2)} == {1, 2}

    def is_move_blocked(self, new_location):
        self.new_location = new_location
        return False


class Bishop(Piece):
    def __init__(self, colour, location, game):
        super().__init__(colour, "bishop", location, game)

    def piece_custom_rule(self, target_location):
        """is diagonal"""
        m1, m2 = difference_vector(target_location, self.location)
        return abs(m1) == abs(m2)


class Queen(Piece):
    def __init__(self, colour, location, game):
        super().__init__(colour, "queen", location, game)

    def piece_custom_rule(self, target_location):
        """is diagonal or orthogonal"""
        m1, m2 = difference_vector(target_location, self.location)
        return 0 in {m1, m2} or abs(m1) == abs(m2)


class King(Piece):
    def __init__(self, colour, location, game):
        super().__init__(colour, "king", location, game)
        self.in_check = False

    def piece_custom_rule(self, target_location):
        king_castling_locations = (
            ("c1", "e1"),
            ("g1", "e1"),
            ("c8", "e8"),
            ("g8", "e8"),
        )
        end, start = target_location, self.location
        king_can_castle = (end, start) in king_castling_locations and self.unmoved
        rook_can_castle = self.can_rook_castle(target_location)
        are_castle_conditions_met = king_can_castle and rook_can_castle

        return (
            self.is_valid_normal_king_move(target_location) or are_castle_conditions_met
        )

    def is_valid_normal_king_move(self, target_location):
        m1, m2 = difference_vector(target_location, self.location)
        return abs(m1) <= 1 and abs(m2) <= 1

    def is_attack_valid(self, m1, m2, location):
        return self.is_valid_normal_king_move(location)

    def can_rook_castle(self, new_location):
        """If the king were to castle is there a rook available?"""
        r_old = {"g8": "h8", "c8": "a8", "g1": "h1", "c1": "a1"}
        r_new = {"g8": "f8", "c8": "d8", "g1": "f1", "c1": "d1"}
        if new_location in r_old.keys():
            if r_old[new_location] in self.game.pieces.keys():
                rook_loc = self.game.pieces[r_old[new_location]]
                if rook_loc.unmoved and rook_loc.type == "rook":
                    rook_loc.get_legal_moves(mode="castling")
                    return r_new[new_location] in rook_loc.legal_moves
        return False
