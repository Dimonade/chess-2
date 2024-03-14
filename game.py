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

        self.move_maker = None

        self.white_in_check = False
        self.black_in_check = False

    def reset_all_tiles(self):
        for tile in self.tiles.values():
            tile.reset()

    def next_turn(self):
        self.update_move_number()
        self.next_player()

    def update_move_number(self):
        if self.player.get() == "white":
            mn = self.move_number
            mn.set(mn.get() + 1)

    def next_player(self):
        p = self.player
        p.set(Colour.get_opposite(p.get()))
