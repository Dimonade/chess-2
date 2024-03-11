from constants import Colour, Letter


class Piece:
    def __init__(
        self, colour, piece_type, location, game_pieces, game_tiles, en_passant_manager
    ):
        self.game_pieces = game_pieces
        self.game_tiles = game_tiles
        self.en_passant_manager = en_passant_manager
        self.piece_colour = colour
        self.piece_type = piece_type
        self.location = location
        self.piece_unmoved = True
        self.active = True
        self.new_location = ""
        self.enemy_colour = Colour[colour.upper()].get_opposite().name.lower()
        self.enemy_king_location = get_king(game_pieces, self.enemy_colour)
        self.legal_moves = set()
        self.attack_moves = set()

    def __str__(self):
        return f"{self.piece_colour} {self.piece_type} at {self.location}"

    def move(self, new_location: str):
        del self.game_pieces[self.location]
        self.game_pieces[new_location] = self
        self.location = new_location
        self.piece_unmoved = False

    def remove(self):
        del self.game_pieces[self.location]
        self.location = None

    def find_vector(self):
        s1, s2 = self.location, self.new_location
        v1 = Letter[s2[0].upper()].value - Letter[s1[0].upper()].value
        v2 = int(s2[1]) - int(s1[1])
        return v1, v2

    def find_direction(self):
        v1, v2 = self.find_vector()
        if 0 in (v1, v2) or abs(v1) == abs(v2):
            return self.sign(v1), self.sign(v2)
        else:
            return "invalid"

    @staticmethod
    def sign(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    def move_blocked(self, new_location):
        self.new_location = new_location
        if self.piece_type == "knight":
            return False
        else:
            direction = self.find_direction()
            if direction != "invalid":
                location = add_coordinate(self.location, direction)
                while location != new_location:
                    if location in self.game_pieces.keys():
                        return True
                    location = add_coordinate(location, direction)
                return False

    def attack_valid(self, m1, m2, location):
        pass

    def get_attacks(self):
        self.attack_moves.clear()
        for location in self.game_tiles.keys():
            m1, m2 = movement(location, self.location)
            if self.attack_valid(m1, m2, location):
                self.attack_moves.add(location)
        if self.location in self.attack_moves:
            self.attack_moves.remove(self.location)


def movement(location1: str, location2: str) -> tuple:
    column1, column2 = (
        Letter[location1[0].upper()].value,
        Letter[location2[0].upper()].value,
    )
    row1, row2 = int(location1[1]), int(location2[1])
    return column1 - column2, row1 - row2


def add_coordinate(initial: str, vector: tuple) -> str:
    x, y = Letter[initial[0].upper()].value, int(initial[1])
    final_x, final_y = x + vector[0], y + vector[1]
    return f"{Letter(final_x).name.lower()}{final_y}"


def return_if_available(suggested_key, dictionary, otherwise):
    if suggested_key in dictionary.keys():
        return dictionary[suggested_key]
    else:
        return otherwise


def get_king(game_piece_dict, colour):
    for piece in game_piece_dict.values():
        if piece.piece_type == "king" and piece.piece_colour == colour:
            return piece.location


def get_attacked_positions(dictionary: dict, attacked_by: str = "white", skip=""):
    res = set()
    for piece in dictionary.values():
        if piece.location == skip:
            continue
        piece.get_attacks()
        for legal in piece.attack_moves:
            if attacked_by == "white":
                if piece.piece_colour == "white":
                    res.add(legal)
            elif attacked_by == "black":
                if piece.piece_colour == "black":
                    res.add(legal)
    return res
