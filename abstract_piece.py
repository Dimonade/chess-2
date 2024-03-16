"""contains an abstract class Piece used by all the subclasses in pieces.py, as well as extra functions"""

from constants import Colour, Letter
from coordinate import Coordinate


class Piece:
    def __init__(self, colour, piece_type, location, game):
        self.game = game
        self.colour = colour
        self.type = piece_type
        self.location = location
        self.new_location = ""
        self.enemy_colour = Colour.get_opposite(colour)
        self.enemy_king_location = get_king(self.game.pieces, self.enemy_colour)
        self.legal_moves = set()
        self.attack_moves = set()
        self.unmoved = True

    def move_to(self, new_location: str):
        """moves piece to new location"""
        self.remove()
        self.game.pieces[new_location] = self
        self.location = new_location
        self.unmoved = False

    def remove(self):
        """removes piece from game pieces"""
        del self.game.pieces[self.location]

    def get_direction(self):
        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        v1, v2 = difference_vector(self.new_location, self.location)
        if 0 in (v1, v2) or abs(v1) == abs(v2):
            return sign(v1), sign(v2)
        else:
            return "invalid"

    def is_move_blocked(self, new_location):
        self.new_location = new_location
        direction = self.get_direction()
        if direction != "invalid":
            location = add_coordinate(self.location, direction)
            while location != new_location:
                if location in self.game.pieces.keys():
                    return True
                location = add_coordinate(location, direction)
            return False

    def is_attack_valid(self, m1, m2, location):
        pass

    def get_attacks(self):
        am = self.attack_moves
        piece_location = self.location

        am.clear()
        for location in self.game.tiles.keys():
            m1, m2 = difference_vector(location, piece_location)
            if self.is_attack_valid(m1, m2, location):
                am.add(location)
        if piece_location in am:
            am.remove(piece_location)
        return am

    def piece_custom_rule(self, location):
        pass

    def get_legal_moves(self, mode="normal"):
        lm = self.legal_moves
        tiles = self.game.tiles

        lm.clear()
        for location in tiles.keys():
            same_colour = self.has_piece_with_same_colour(location)
            move_blocked = self.is_move_blocked(location)
            if (
                self.piece_custom_rule(location)
                and not same_colour
                and not move_blocked
            ):
                lm.add(location)
                if mode == "normal":
                    tiles[location].change_selection()
        if self.location in self.attack_moves:
            lm.remove(self.location)

    def get_legal_moves_with_check(self, mode):
        self.get_legal_moves("different")
        res = []
        for move in self.legal_moves:
            if not self.would_result_in_self_check(move):
                res.append(move)
        if mode == "normal":
            for location in res:
                self.game.tiles[location].change_selection()
        self.legal_moves = set(res)
        return res

    def would_result_in_self_check(self, target_location):
        would_result_in_check = False

        capturing_piece = False
        captured_piece = None
        if target_location in self.game.pieces.keys():
            capturing_piece = True
            captured_piece = self.game.pieces[target_location]

        del self.game.pieces[self.location]
        self.game.pieces[target_location] = self

        player_king_location = self.game.get_king_location(self.colour)
        if self.type == "king":
            player_king_location = target_location
        opposing_colour = Colour.get_opposite(self.colour)

        for piece in self.game.pieces_of_specific_colour(opposing_colour):
            h, v = difference_vector(player_king_location, piece.location)
            if h == 0 or v == 0 or abs(h) == abs(v) or {abs(v), abs(h)} == {1, 2}:
                piece.get_attacks()
                if player_king_location in piece.attack_moves:
                    would_result_in_check = True
                    break

        del self.game.pieces[target_location]
        self.game.pieces[self.location] = self
        if capturing_piece:
            self.game.pieces[target_location] = captured_piece
        return would_result_in_check

    def is_attack_valid(self, m1, m2, location):
        return self.piece_custom_rule(location) and not self.is_move_blocked(location)

    def has_piece_with_same_colour(self, location):
        """if location contains piece and this piece is the same this current piece's colour return True else return
        false"""
        same_colour = False
        pieces = self.game.pieces
        if location in pieces.keys():
            if pieces[location].colour == self.colour:
                same_colour = True
        return same_colour


def difference_vector(location1: str, location2: str) -> tuple:
    c1, c2 = Coordinate.create_from_strs(location1, location2)
    return Coordinate.diff_vector(c1, c2)


def add_coordinate(start: str, vector: tuple) -> str:
    x0, y0 = Letter.to_num(start[0]), int(start[1])
    x1 = x0 + vector[0]
    y1 = y0 + vector[1]
    return f"{Letter.num_to_lower(x1)}{y1}"


def get_king(game_pieces: dict, colour) -> str:
    for piece in game_pieces.values():
        if piece.type == "king" and piece.colour == colour:
            return piece.location


def get_attacked_positions(pieces: dict, attacked_by: str = "white", skip="") -> set:
    res = set()
    for piece in pieces.values():
        if piece.location == skip:
            continue
        piece.get_attacks()
        for move in piece.attack_moves:
            if attacked_by == "white" and piece.colour == "white":
                res.add(move)
            elif attacked_by == "black" and piece.colour == "black":
                res.add(move)
    return res
