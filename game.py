class Game:
    def __init__(self, gui_components):
        self.tiles = {}
        self.pieces = {}
        self.print_move_on = True

        self.root = gui_components[0]
        self.chessboard = gui_components[1]
        self.player = gui_components[2]
        self.move_number = gui_components[3]
