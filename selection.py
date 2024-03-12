from constants import Colour


class Selection:
    def __init__(self):
        self.first_tile = ""
        self.second_tile = ""
        self.piece = None
        self.piece_colour = ""
        self.enemy_colour = ""
        self.current_tile = ""

    def reset(self):
        self.first_tile = ""
        self.second_tile = ""

    def get_tiles(self):
        return self.first_tile, self.second_tile

    def set_first_tile(self, first_tile, piece):
        self.first_tile = first_tile
        self.piece = piece
        self.piece_colour = piece.piece_colour
        self.enemy_colour = (
            Colour[piece.piece_colour.upper()].get_opposite().name.lower()
        )
        self.current_tile.select_as_first_tile()
