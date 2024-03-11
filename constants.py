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
