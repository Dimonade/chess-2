"""holds the game data"""

from constants import Colour


class Game:
    def __init__(self, gui_components):
        self.tiles = dict()
        self.pieces = dict()
        self.print_move_on = False

        self.root = gui_components[0]
        self.chessboard = gui_components[1]
        self.player = gui_components[2]
        self.move_number = gui_components[3]

        self.move_maker = None

        self.white_in_check = False
        self.black_in_check = False

    def pieces_of_specific_colour(self, colour):
        return [piece for piece in self.pieces.values() if piece.colour == colour]

    def reset_all_tiles(self):
        for tile in self.tiles.values():
            tile.reset()

    def next_turn(self):
        self.increment_move_number()
        self.next_player()

    def get_king_location(self, colour):
        for location, piece in self.pieces.items():
            if piece.colour == colour and piece.type == "king":
                return location

    def increment_move_number(self):
        if self.player.get() == "white":
            mn = self.move_number
            mn.set(mn.get() + 1)

    def next_player(self):
        p = self.player
        p.set(Colour.get_opposite(p.get()))
