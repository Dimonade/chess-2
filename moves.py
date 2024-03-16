"""contains MoveMaker class which contains tile_pressed which is activated by Tile in tile.py and manages the move"""

from audio import make_sound
from abstract_piece import difference_vector
from selection import Selection
from en_passant import EnPassantMaker
from pawnpromoter import PawnPromoter
from constants import Colour
from tkinter import messagebox


class MoveMaker:
    def __init__(self, game):
        self.game = game
        self.selection = Selection()
        self.ep = EnPassantMaker()
        self.location = ""

    def tile_pressed(self, location):
        """the command made by a tile from tile.py to signify the user has pressed it"""
        self.location = location

        self.selection.current_tile = self.game.tiles[location]
        if self.is_deselection():
            self.reset()
        elif self.selection.first_tile == "":
            self.first_tile_selected()
        else:
            self.second_tile_selected()

    def first_tile_selected(self):
        """given tile is the first selection complete the selection process"""
        if self.is_piece_player_colour():
            location = self.location
            selection = self.selection
            pieces = self.game.pieces

            selection.set_first_tile(location, pieces[location])
            piece = selection.piece
            piece.get_legal_moves_with_check(mode="normal")

    def second_tile_selected(self):
        """given tile is the second selection complete the selection process"""
        self.selection.second_tile = self.location
        if self.is_legal_destination():
            self.carry_out_move()
        self.reset()

    def is_deselection(self):
        """returns whether the current tile press results in deselection"""
        return self.selection.current_tile.selected

    def is_piece_player_colour(self) -> bool:
        """if a piece of the player's colour is at the current location return true else return false"""
        pieces = self.game.pieces
        location = self.location
        player_colour = self.game.player.get()
        if location in pieces.keys():
            piece = pieces[location]
            return piece.colour == player_colour
        return False

    def is_legal_destination(self):
        """return True if move not blocked, current piece colour is not player colour and location in legal moves"""
        selection = self.selection
        piece = selection.piece
        location = selection.second_tile
        conditions = [
            location in piece.legal_moves,
        ]
        return all(conditions)

    def reset(self):
        """resets the selection and all the tiles on the board"""
        self.selection.reset()
        self.game.reset_all_tiles()

    def complete_castling(self):
        """Check piece is king, if so check movement is 2 horizontal tiles, if so move corresponding rook"""
        selection = self.selection
        if selection.piece.type == "king":
            king_start, king_end = selection.get_tiles()
            horizontal_movement, _ = difference_vector(king_start, king_end)
            if abs(horizontal_movement) == 2:
                rook_start = {"g8": "h8", "c8": "a8", "g1": "h1", "c1": "a1"}
                rook_end = {"g8": "f8", "c8": "d8", "g1": "f1", "c1": "d1"}
                rook_start_tile = rook_start[king_end]
                rook_end_tile = rook_end[king_end]
                self.game.pieces[rook_start_tile].move_to(rook_end_tile)

    def carry_out_move(self):
        """two valid selections have been made so a move may now be carried out"""
        selection = self.selection
        game = self.game
        pieces = game.pieces
        piece = selection.piece

        tile1, tile2 = selection.get_tiles()
        is_attacking = (
            tile2 in pieces.keys()
        )  # don't move below piece.move as will cause error
        piece.move_to(tile2)

        self.complete_castling()
        self.ep.complete_en_passant(tile2, pieces)
        self.ep.set_en_passant(piece, tile1, tile2)
        pp = PawnPromoter(piece, game)
        prom = pp.attempt_promote()
        if prom[0]:
            piece = self.game.pieces[self.location]

        enemy_colour = Colour.get_opposite(game.player.get())
        enemy_king_location = game.get_king_location(enemy_colour)
        check = enemy_king_location in piece.get_attacks()
        if check:
            if enemy_colour == "white":
                game.white_in_check = True
            if enemy_colour == "black":
                game.black_in_check = True
        else:
            game.white_in_check = False
            game.black_in_check = False
        checkmate = False
        if self.number_of_legal_moves_of_opponent() == 0:
            self.game.root.update()
            checkmate = self.game_over()

        if game.print_move_on:
            print_move(piece, tile2, prom, is_attacking, tile1, check, checkmate)
        make_sound(checkmate, check, is_attacking)
        game.next_turn()

    def game_over(self):
        checkmate = True
        if self.game.black_in_check:
            messagebox.showinfo("game over", "white wins - black in checkmate")
        elif self.game.white_in_check:
            messagebox.showinfo("game over", "black wins  - white in checkmate")
        else:
            messagebox.showinfo("game over", "draw - stalemate")
            checkmate = False
        return checkmate

    def number_of_legal_moves_of_opponent(self):
        """return the number of legal moves of the given piece"""
        legal_moves = 0
        opponent_colour = Colour.get_opposite(self.selection.piece.colour)
        for piece in self.game.pieces_of_specific_colour(opponent_colour):
            if piece.colour == self.selection.enemy_colour:
                piece.get_legal_moves_with_check(mode="different")
                legal_moves += len(piece.legal_moves)
        return legal_moves

    def get_piece_colour(self):
        """return the colour of the given piece"""
        location = self.location
        pieces = self.game.pieces
        if location in pieces.keys():
            return pieces[location].colour
        else:
            return "piece does not exist"


def print_move(piece, location, prom, attacking, old_location, check, checkmate):
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
        if piece.type == "pawn":
            at = f"{old_location[0]}x"
        else:
            at = "x"
    else:
        at = ""
    end_string = ""
    if checkmate:
        end_string = "#"
    elif check:
        end_string = "+"
    output_string = f"{d[piece.type]}{at}{location}{promotion}{end_string}"
    print(output_string)
