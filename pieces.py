from tkinter import messagebox
from abstract_piece import Piece, movement, get_attacked_positions
import keyboard

letters_numbers = {
    1: "a",
    2: "b",
    3: "c",
    4: "d",
    5: "e",
    6: "f",
    7: "g",
    8: "h",
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
}
opposite_colour = {"black": "white", "white": "black"}
eight_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Pawn(Piece):
    def __init__(self, colour, location, game_pieces, game_tiles, en_passant_manager):
        super().__init__(
            colour, "pawn", location, game_pieces, game_tiles, en_passant_manager
        )

    def get_legal_moves(self):
        self.legal_moves.clear()
        for location in self.game_tiles.keys():
            filled = False
            if location in self.game_pieces.keys():
                filled = True
            not_filled_with_same_colour = True
            if filled:
                if self.game_pieces[location].piece_colour == self.piece_colour:
                    not_filled_with_same_colour = False
            m1, m2 = movement(location, self.location)
            c1 = 3 > m2 > 0 and self.piece_colour == "white"
            c2 = -3 < m2 < 0 and self.piece_colour == "black"
            c4 = abs(m1) == 0 and not filled
            c8 = location == self.en_passant_manager.tile
            c6 = abs(m1) == 1 and (filled or c8)
            c5 = {abs(m1), abs(m2)} != {1, 2}
            c7 = (self.piece_unmoved and self.move_blocked(location) is False) or abs(
                m2
            ) == 1
            if (c1 or c2) and (c4 or c6) and c5 and c7 and not_filled_with_same_colour:
                self.legal_moves.add(location)
                self.game_tiles[location].configure_selection()
        if self.location in self.legal_moves:
            self.legal_moves.remove(self.location)

    def attack_valid(self, m1, m2, location):
        c1 = abs(m1) == 1
        c2 = (m2 == 1 and self.piece_colour == "white") or (
            m2 == -1 and self.piece_colour == "black"
        )
        return all([c1, c2])


class Rook(Piece):
    def __init__(self, colour, location, game_pieces, game_tiles, en_passant_manager):
        super().__init__(
            colour, "rook", location, game_pieces, game_tiles, en_passant_manager
        )

    def get_legal_moves(self, mode="normal"):
        self.legal_moves.clear()
        for location in self.game_tiles.keys():
            not_filled_with_same_colour = True
            if location in self.game_pieces.keys():
                if self.game_pieces[location].piece_colour == self.piece_colour:
                    not_filled_with_same_colour = False
            m1, m2 = movement(location, self.location)
            if (
                0 in {m1, m2}
                and not_filled_with_same_colour
                and not self.move_blocked(location)
            ):
                self.legal_moves.add(location)
                if mode == "normal":
                    self.game_tiles[location].configure_selection()
        if self.location in self.legal_moves:
            self.legal_moves.remove(self.location)

    def attack_valid(self, m1, m2, location):
        c1 = 0 in {m1, m2}
        c2 = not self.move_blocked(location)
        return all([c1, c2])


class Knight(Piece):
    def __init__(self, colour, location, game_pieces, game_tiles, en_passant_manager):
        super().__init__(
            colour, "knight", location, game_pieces, game_tiles, en_passant_manager
        )

    def get_legal_moves(self):
        self.legal_moves.clear()
        for location in self.game_tiles.keys():
            not_filled_with_same_colour = True
            if location in self.game_pieces.keys():
                if self.game_pieces[location].piece_colour == self.piece_colour:
                    not_filled_with_same_colour = False
            m1, m2 = movement(location, self.location)
            if {abs(m1), abs(m2)} == {1, 2} and not_filled_with_same_colour:
                self.legal_moves.add(location)
                self.game_tiles[location].configure_selection()
        if self.location in self.legal_moves:
            self.legal_moves.remove(self.location)

    def attack_valid(self, m1, m2, location):
        c1 = {abs(m1), abs(m2)} == {1, 2}
        return c1


class Bishop(Piece):
    def __init__(self, colour, location, game_pieces, game_tiles, en_passant_manager):
        super().__init__(
            colour, "bishop", location, game_pieces, game_tiles, en_passant_manager
        )

    def get_legal_moves(self):
        self.legal_moves.clear()
        for location in self.game_tiles.keys():
            not_filled_with_same_colour = True
            if location in self.game_pieces.keys():
                if self.game_pieces[location].piece_colour == self.piece_colour:
                    not_filled_with_same_colour = False
            m1, m2 = movement(location, self.location)
            if (
                abs(m1) == abs(m2)
                and not_filled_with_same_colour
                and not self.move_blocked(location)
            ):
                self.legal_moves.add(location)
                self.game_tiles[location].configure_selection()
        if self.location in self.legal_moves:
            self.legal_moves.remove(self.location)

    def attack_valid(self, m1, m2, location):
        c1 = abs(m1) == abs(m2)
        c2 = not self.move_blocked(location)
        return all([c1, c2])


class Queen(Piece):
    def __init__(self, colour, location, game_pieces, game_tiles, en_passant_manager):
        super().__init__(
            colour, "queen", location, game_pieces, game_tiles, en_passant_manager
        )

    def get_legal_moves(self):
        self.legal_moves.clear()
        for location in self.game_tiles.keys():
            not_filled_with_same_colour = True
            if location in self.game_pieces.keys():
                if self.game_pieces[location].piece_colour == self.piece_colour:
                    not_filled_with_same_colour = False
            m1, m2 = movement(location, self.location)
            c1 = 0 in {m1, m2} or abs(m1) == abs(m2)
            if c1 and not_filled_with_same_colour and not self.move_blocked(location):
                self.legal_moves.add(location)
                self.game_tiles[location].configure_selection()
        if self.location in self.attack_moves:
            self.legal_moves.remove(self.location)

    def attack_valid(self, m1, m2, location):
        c1 = 0 in {m1, m2} or abs(m1) == abs(m2)
        c2 = not self.move_blocked(location)
        return all([c1, c2])


class King(Piece):
    def __init__(self, colour, location, game_pieces, game_tiles, en_passant_manager):
        super().__init__(
            colour, "king", location, game_pieces, game_tiles, en_passant_manager
        )
        self.in_check = False

    def get_legal_moves(self):
        self.legal_moves.clear()
        o = opposite_colour[self.piece_colour]
        ap = get_attacked_positions(self.game_pieces, attacked_by=o)
        for location in self.game_tiles.keys():
            # not filled with same colour
            not_filled_with_same_colour = True
            if location in self.game_pieces.keys():
                if self.game_pieces[location].piece_colour == self.piece_colour:
                    not_filled_with_same_colour = False

            m1, m2 = movement(location, self.location)
            c1 = abs(m1) <= 1
            c2 = abs(m2) <= 1
            tuples = ("c1", "e1"), ("g1", "e1"), ("c8", "e8"), ("g8", "e8")
            c6 = (location, self.location) in tuples and self.piece_unmoved
            c7 = self.legal_rook_castle(location)
            c3 = not_filled_with_same_colour
            c4 = location not in ap
            c5 = not self.move_blocked(location)
            if ((c1 and c2) or (c6 and c7)) and c3 and c4 and c5:
                self.legal_moves.add(location)
                self.game_tiles[location].configure_selection()
        if self.location in self.legal_moves:
            self.legal_moves.remove(self.location)

    def attack_valid(self, m1, m2, location):
        c1 = abs(m1) <= 1
        c2 = abs(m2) <= 1
        return all([c1, c2])

    def legal_rook_castle(self, new_location):
        """If the king were to castle is there a rook available?"""
        r_old = {"g8": "h8", "c8": "a8", "g1": "h1", "c1": "a1"}
        r_new = {"g8": "f8", "c8": "d8", "g1": "f1", "c1": "d1"}
        if new_location in r_old.keys():
            if r_old[new_location] in self.game_pieces.keys():
                rook_loc = self.game_pieces[r_old[new_location]]
                if rook_loc.piece_unmoved and rook_loc.piece_type == "rook":
                    rook_loc.get_legal_moves(mode="castling")
                    return r_new[new_location] in rook_loc.legal_moves
        return False


def attempt_promote(piece, game_pieces, game_tiles, ep):
    if piece.piece_type == "pawn" and piece.location[1] in {"1", "8"}:
        message = (
            "press q to promote to queen, k to a knight, b to a bishop or r to a rook"
        )
        messagebox.showinfo("promotion", message)
        x1, x2 = piece.piece_colour, piece.location
        d = {
            "q": Queen(x1, x2, game_pieces, game_tiles, ep),
            "k": Knight(x1, x2, game_pieces, game_tiles, ep),
            "b": Bishop(x1, x2, game_pieces, game_tiles, ep),
            "r": Rook(x1, x2, game_pieces, game_tiles, ep),
        }

        pressed = ""
        while pressed not in d.keys():
            pressed = keyboard.read_key()
        game_pieces[piece.location] = d[pressed]
        return True, pressed.upper()
    else:
        return False, ""
