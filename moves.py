from audio import get_sound
from abstract_piece import movement
from pieces import attempt_promote
from selection import Selection
from en_passant import EnPassantMaker


class MoveMaker:
    def __init__(self, game):
        self.game = game
        self.selection = Selection()
        self.ep = EnPassantMaker()
        self.location = ""

    def tile_pressed(self, location):
        self.location = location
        selection = self.selection
        selection.current_tile = self.game.tiles[location]
        if self.is_deselection():
            self.reset()
        else:
            if selection.first_tile == "":
                self.first_tile_pressed()
            else:
                self.second_tile_pressed()

    def first_tile_pressed(self):
        location = self.location
        selection = self.selection
        pieces = self.game.pieces

        if self.is_piece_player_colour():
            selection.set_first_tile(location, pieces[location])
            piece = selection.piece

            if piece.piece_type == "pawn":
                piece.get_legal_moves(self.ep)
            else:
                piece.get_legal_moves()

    def second_tile_pressed(self):
        self.selection.second_tile = self.location
        if self.is_legal_destination():
            self.carry_out_move()
        self.reset()

    def is_deselection(self):
        return self.selection.current_tile.selected

    def is_piece_player_colour(self) -> bool:
        pieces = self.game.pieces
        location = self.location
        player_colour = self.game.player.get()
        if location in pieces.keys():
            return pieces[location].piece_colour == player_colour
        return False

    def is_legal_destination(self):
        selection = self.selection
        piece = selection.piece
        location = selection.second_tile
        conditions = [
            not piece.is_move_blocked(location),
            not selection.current_tile.get_piece_colour() == self.game.player.get(),
            location in piece.legal_moves,
        ]
        return all(conditions)

    def reset(self):
        self.selection.reset()
        self.game.reset_all_tiles()

    def complete_castling(self):
        """Check piece is king, if so check movement is 2 horizontal tiles, if so move corresponding rook"""
        selection = self.selection
        if selection.piece.piece_type == "king":
            king_start, king_end = selection.get_tiles()
            horizontal_movement, _ = movement(king_start, king_end)
            if abs(horizontal_movement) == 2:
                rook_start = {"g8": "h8", "c8": "a8", "g1": "h1", "c1": "a1"}
                rook_end = {"g8": "f8", "c8": "d8", "g1": "f1", "c1": "d1"}
                rook_start_tile = rook_start[king_end]
                rook_end_tile = rook_end[king_end]
                self.game.pieces[rook_start_tile].move(rook_end_tile)

    def carry_out_move(self):
        tile1, tile2 = self.selection.get_tiles()
        attacking = tile2 in self.game.pieces.keys()
        self.selection.piece.move(tile2)
        self.complete_castling()

        self.ep.complete_en_passant(tile2, self.game.pieces)
        self.ep.set_en_passant(self.selection.piece, tile1, tile2)

        prom = attempt_promote(self.selection.piece, self.game.pieces, self.game.tiles)

        check = False

        if self.game.print_move_on:
            print_move(self.selection.piece, tile2, prom, attacking, tile1, check)

        self.make_sound(check, attacking)
        self.game.next_player()
        self.game.update_move_number()

    @staticmethod
    def make_sound(check, attacking):
        if check:
            get_sound(3)
        elif attacking:
            get_sound(2)
        else:
            get_sound(1)

    def number_of_legal_moves(self):
        legal_moves = 0
        for piece in self.game.pieces.values():
            if piece.piece_colour == self.selection.enemy_colour:
                if piece.piece_type == "pawn":
                    piece.get_legal_moves(self.ep)
                else:
                    piece.get_legal_moves()
                legal_moves += len(piece.legal_moves)
        return legal_moves


def print_move(piece, location, prom, attacking, old_location, check):
    d = {
        "rook": "R",
        "bishop": "B",
        "knight": "N",
        "queen": "Q",
        "king": "K",
        "pawn": "",
    }
    if prom[0]:
        promotion = f"={prom[1]}"
    else:
        promotion = ""
    if attacking:
        if piece.piece_type == "pawn":
            at = f"{old_location[0]}x"
        else:
            at = "x"
    else:
        at = ""
    d2 = {False: "", True: "+", "checkmate": "#"}
    output_string = f"{d[piece.piece_type]}{at}{location}{promotion}{d2[check]}"
    print(output_string)
