from constants import Colour


class Game:
    def __init__(self, gui_components):
        self.tiles = {}
        self.pieces = {}
        self.print_move_on = True

        self.root = gui_components[0]
        self.chessboard = gui_components[1]
        self.player = gui_components[2]
        self.move_number = gui_components[3]

        self.white_in_check = False
        self.black_in_check = False

    def reset_all_tiles(self):
        for tile in self.tiles.values():
            tile.reset()

    def update_move_number(self):
        if self.player.get() == "white":
            self.move_number.set(self.move_number.get() + 1)

    def next_player(self):
        new_colour = Colour[self.player.get().upper()].get_opposite().name.lower()
        self.player.set(new_colour)
