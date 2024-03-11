from constants import Letter
import tkinter as tk
from PIL import Image, ImageTk

image_names = [
    "pawn_white",
    "pawn_black",
    "bishop_white",
    "bishop_black",
    "king_white",
    "king_black",
    "empty_tile_1",
    "empty_tile_2",
    "knight_white",
    "knight_black",
    "rook_white",
    "rook_black",
    "queen_white",
    "queen_black",
    "empty_tile_1_selected",
    "empty_tile_2_selected",
]


class Tile:
    def __init__(
        self, row: int, column: str, chessboard, images, move_maker, game_pieces
    ):
        self.chessboard = chessboard
        self.images = images
        self.game_pieces = game_pieces
        self.location = f"{column}{row}"
        d = {0: "gray", 1: "wheat1"}
        self.base_colour = d[(row + Letter[column.upper()].value) % 2]
        d = {"gray": "empty_tile_1", "wheat1": "empty_tile_2"}
        self.base_image = images[d[self.base_colour]]
        self.button = tk.Button(
            self.chessboard,
            width=50,
            height=50,
            bg=self.base_colour,
            highlightcolor="black",
            activebackground=self.base_colour,
            image=self.base_image,
            command=lambda: move_maker.tile_pressed(self.location),
        )
        self.button.grid(row=8 - row, column=Letter[column.upper()].value)
        self.button.bind("<Button-3>", lambda event: self.configure_selection())

        self.selected = False
        self.highlighted = False

    def set_piece(self):
        if self.location in self.game_pieces.keys():
            piece = self.game_pieces[self.location]
            t = piece.piece_type
            c = piece.piece_colour
            button_image = self.images[f"{t}_{c}"]
        else:
            button_image = self.base_image
        self.button.configure(
            bg=self.base_colour, activebackground=self.base_colour, image=button_image
        )

    def configure_selection(self):
        self.highlighted = not self.highlighted
        d = {
            "wheat1": ("PaleTurquoise1", "empty_tile_2_selected"),
            "gray": ("PaleTurquoise3", "empty_tile_1_selected"),
        }
        piece_present = self.location in self.game_pieces.keys()
        if self.highlighted:
            self.button.configure(
                bg=d[self.base_colour][0], activebackground=d[self.base_colour][0]
            )
            if not piece_present:
                self.button.configure(image=self.images[d[self.base_colour][1]])
        else:
            self.button.configure(
                bg=self.base_colour, activebackground=self.base_colour
            )
            if not piece_present:
                self.button.configure(image=self.base_image)

    def reset(self):
        self.selected = False
        self.highlighted = False
        self.button.configure(bg=self.base_colour)
        self.set_piece()

    def get_piece_colour(self):
        piece_exists = self.location in self.game_pieces.keys()
        if piece_exists:
            return self.game_pieces[self.location].piece_colour
        else:
            return "piece does not exist"


def get_piece_images():
    res = dict()
    for i in image_names:
        res[i] = ImageTk.PhotoImage(
            Image.open(f"piece_images/{i}.png").resize(
                (50, 50), Image.Resampling.LANCZOS
            )
        )
    return res


def create_tiles(game_tiles, game_pieces, chessboard_frame, m):
    for i in range(1, 9):
        for j in Letter:
            letter = j.name.lower()
            game_tiles[f"{letter}{i}"] = Tile(
                i,
                letter,
                chessboard=chessboard_frame,
                images=get_piece_images(),
                move_maker=m,
                game_pieces=game_pieces,
            )
