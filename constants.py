from enum import Enum


class Colour(Enum):
    WHITE = 0
    BLACK = 1

    def get_opposite(self):
        return Colour((self.value + 1) % 2)


class Letter(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8


image_names = [
    "pawn_white",
    "pawn_black",
    "bishop_white",
    "bishop_black",
    "king_white",
    "king_black",
    "empty_tile_1",
    "empty_tile_2",
    "knight_white",
    "knight_black",
    "rook_white",
    "rook_black",
    "queen_white",
    "queen_black",
    "empty_tile_1_selected",
    "empty_tile_2_selected",
]
