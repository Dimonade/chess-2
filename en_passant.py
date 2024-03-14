from abstract_piece import movement, add_coordinate


class EnPassantMaker:
    def __init__(self):
        self.tile = ""

    def set_en_passant(self, piece, old_location, new_location):
        m1, m2 = movement(old_location, new_location)
        self.tile = ""
        if piece.type == "pawn" and m1 == 0 and abs(m2) == 2:
            if piece.colour == "white":
                vector = (0, 1)
            else:
                vector = (0, -1)
            self.tile = add_coordinate(old_location, vector)

    def complete_en_passant(self, location, pieces: dict):
        if self.tile == location:
            t = ""
            if location[1] == "6":
                t = add_coordinate(location, (0, -1))
            elif location[1] == "3":
                t = add_coordinate(location, (0, 1))
            del pieces[t]
