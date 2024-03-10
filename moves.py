import os
import winsound
from winsound import PlaySound
from tkinter import messagebox
from abstract_piece import get_king, get_attacked_positions, movement
from pieces import attempt_promote


opposite_colour = {"black": "white", "white": "black"}


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


def get_sound(sound_number):
    d = {1: "next_move", 2: "piece_captured", 3: "check"}
    sound = os.path.dirname(__file__) + f"\\sounds\\{d[sound_number]}.wav"
    PlaySound(sound, winsound.SND_ASYNC)


class MoveMaker:
    def __init__(
        self,
        move_list,
        game_tiles,
        game_pieces,
        player,
        ep,
        checks,
        root,
        move_number,
        print_move_on,
    ):
        self.first_tile_location = ""
        self.second_tile_location = ""
        self.piece = None
        self.piece_colour = ""
        self.enemy_colour = ""
        self.move_list = move_list
        self.game_tiles = game_tiles
        self.game_pieces = game_pieces
        self.player = player
        self.ep = ep
        self.checks = checks
        self.root = root
        self.move_number = move_number
        self.print_move_on = print_move_on

    def tile_pressed(self, location):
        self.move_list.append(location)
        current_tile = self.game_tiles[location]

        # deselection
        if current_tile.selected:
            self.reset_all_tiles()

        else:
            if self.first_tile_location == "":
                self.first_tile_pressed(location, current_tile)
            else:
                self.second_tile_pressed(location, current_tile)

    def first_tile_pressed(self, location, current_tile):
        # if a piece of the player's colour is selected
        if (
            location in self.game_pieces.keys()
            and self.game_pieces[location].piece_colour == self.player.get()
        ):
            self.first_tile_location = location
            self.piece = self.game_pieces[location]
            self.piece_colour = self.piece.piece_colour
            self.enemy_colour = opposite_colour[self.piece_colour]
            self.piece.get_legal_moves()
            current_tile.selected = True
            current_tile.button.configure(bg="magenta")

    def second_tile_pressed(self, location, current_tile):
        self.second_tile_location = location
        conditions = [
            not self.piece.move_blocked(location),
            not current_tile.get_piece_colour() == self.player.get(),
            location in self.piece.legal_moves,
        ]
        if all(conditions):
            self.carry_out_move()
        self.reset_all_tiles()

    def reset_all_tiles(self):
        for tile in self.game_tiles.values():
            tile.reset()
            self.first_tile_location = self.second_tile_location = ""

    def current_player_check(self):
        defender_colour = opposite_colour[self.enemy_colour]
        this_players_king_position = get_king(self.game_pieces, defender_colour)
        if this_players_king_position in get_attacked_positions(
            self.game_pieces, self.enemy_colour
        ):
            get_sound(3)
            res = self.checks[defender_colour] = self.game_pieces[
                this_players_king_position
            ].in_check = True
        else:
            res = self.checks[defender_colour] = self.game_pieces[
                this_players_king_position
            ].in_check = False
        return res

    def enemy_player_check(self):
        player_colour, enemy_colour = self.piece_colour, self.enemy_colour
        enemy_king_position = get_king(self.game_pieces, enemy_colour)
        enemy_king = self.game_pieces[enemy_king_position]
        if enemy_king_position in get_attacked_positions(
            self.game_pieces, player_colour
        ):
            enemy_king.in_check = True
            self.checks[enemy_colour] = True
            return True
        else:
            enemy_king.in_check = False
            self.checks[enemy_colour] = False
            return False

    def complete_castling(self):
        if self.piece.piece_type == "king":
            m1, m2 = movement(self.first_tile_location, self.second_tile_location)
            if abs(m1) == 2:
                r_old = {"g8": "h8", "c8": "a8", "g1": "h1", "c1": "a1"}
                r_new = {"g8": "f8", "c8": "d8", "g1": "f1", "c1": "d1"}
                c1 = r_old[self.second_tile_location]
                c2 = r_new[self.second_tile_location]
                self.game_pieces[c1].move(c2)

    def carry_out_move(self):
        l1, l2 = self.first_tile_location, self.second_tile_location
        attacking = l2 in self.game_pieces.keys()
        self.piece.move(l2)
        self.complete_castling()

        self.ep.complete_en_passant(l2, self.game_pieces)
        self.ep.set_en_passant(self.piece, l1, l2)

        prom = attempt_promote(self.piece, self.game_pieces, self.game_tiles, self.ep)
        check = self.enemy_player_check()

        if self.print_move_on.get():
            print_move(self.piece, l2, prom, attacking, l1, check)

        self.check_and_attempt_game_over()
        self.make_sound(check, attacking)
        self.update_player()
        self.update_move_number()

    @staticmethod
    def make_sound(check, attacking):
        if check:
            get_sound(3)
        elif attacking:
            get_sound(2)
        else:
            get_sound(1)

    def check_and_attempt_game_over(self):
        if self.number_of_legal_moves() == 0:
            if self.checks[self.enemy_colour]:
                output_message = f"{self.piece_colour} wins"
            else:
                output_message = "game is a draw"
            messagebox.showinfo("game over", output_message)
            self.root.destroy()

    def number_of_legal_moves(self):
        legal_moves = 0
        for piece in self.game_pieces.values():
            if piece.piece_colour == self.enemy_colour:
                piece.get_legal_moves()
                legal_moves += len(piece.legal_moves)
        return legal_moves

    def update_player(self):
        new_colour = opposite_colour[self.player.get()]
        self.player.set(new_colour)

    def update_move_number(self):
        if self.player.get() == "white":
            self.move_number.set(self.move_number.get() + 1)
