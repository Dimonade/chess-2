letters_numbers = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h',
                   'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
opposite_colour = {'black': 'white', 'white': 'black'}


class Piece:
    def __init__(self, colour, piece_type, location, game_pieces, game_tiles, en_passant_manager):
        self.game_pieces = game_pieces
        self.game_tiles = game_tiles
        self.en_passant_manager = en_passant_manager
        self.piece_colour = colour
        self.piece_type = piece_type
        self.location = location
        self.piece_unmoved = True
        self.active = True
        self.new_location = ''
        self.enemy_colour = opposite_colour[colour]
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

    def value_estimate(self):
        piece_values = {'None': 0, 'rook': 5, 'knight': 3, 'bishop': 3, 'queen': 9, 'king': 0, 'pawn': 1}
        d = {'white': 1, 'black': -1, 'None': 0}
        return piece_values[self.piece_type] * d[self.piece_colour]

    def find_vector(self):
        s1, s2 = self.location, self.new_location
        v1 = letters_numbers[s2[0]] - letters_numbers[s1[0]]
        v2 = int(s2[1]) - int(s1[1])
        return v1, v2

    def find_direction(self):
        v1, v2 = self.find_vector()
        if 0 in (v1, v2) or abs(v1) == abs(v2):
            return self.sign(v1), self.sign(v2)
        else:
            return 'invalid'

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
        if self.piece_type == 'knight':
            return False
        else:
            direction = self.find_direction()
            if direction != 'invalid':
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
    column1, column2 = letters_numbers[location1[0]], letters_numbers[location2[0]]
    row1, row2 = int(location1[1]), int(location2[1])
    return column1-column2, row1-row2


def add_coordinate(initial: str, vector: tuple) -> str:
    x, y = letters_numbers[initial[0]], int(initial[1])
    final_x, final_y = x + vector[0], y + vector[1]
    return f'{letters_numbers[final_x]}{final_y}'


def return_if_available(suggested_key, dictionary, otherwise):
    if suggested_key in dictionary.keys():
        return dictionary[suggested_key]
    else:
        return otherwise


def get_king(game_piece_dict, colour):
    for piece in game_piece_dict.values():
        if piece.piece_type == 'king' and piece.piece_colour == colour:
            return piece.location


def get_attacked_positions(dictionary: dict, attacked_by: str = 'white', skip=''):
    res = set()
    for piece in dictionary.values():
        if piece.location == skip:
            continue
        piece.get_attacks()
        for legal in piece.attack_moves:
            if attacked_by == 'white':
                if piece.piece_colour == 'white':
                    res.add(legal)
            elif attacked_by == 'black':
                if piece.piece_colour == 'black':
                    res.add(legal)
    return res