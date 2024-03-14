from constants import Letter, image_names
import tkinter as tk
from PIL import Image, ImageTk


class Tile:
    def __init__(self, row: int, column: str, game, images):
        self.game = game
        self.images = images
        self.location = f"{column}{row}"
        d = {0: "gray", 1: "wheat1"}
        column_value = Letter.to_num(column)
        self.base_colour = d[(row + column_value) % 2]
        d = {"gray": "empty_tile_1", "wheat1": "empty_tile_2"}
        self.base_image = images[d[self.base_colour]]
        self.selected = False
        self.highlighted = False
        self.button = None
        self.has_piece = False

        self.make_button(row, column)

    def make_button(self, row, column):
        self.button = tk.Button(
            self.game.chessboard,
            width=50,
            height=50,
            command=lambda: self.game.move_maker.tile_pressed(self.location),
        )
        self.set_bg()
        self.set_img()
        self.button.grid(row=8 - row, column=Letter.to_num(column))
        self.button.bind("<Button-3>", lambda event: self.change_selection())

    def set_piece(self):
        location = self.location
        pieces = self.game.pieces

        if location in pieces.keys():
            piece = pieces[location]
            image_name = f"{piece.type}_{piece.colour}"
            button_image = self.images[image_name]
            self.has_piece = True
        else:
            button_image = self.base_image
            self.has_piece = False
        self.set_bg()
        self.set_img(button_image)

    def change_selection(self):
        self.highlighted = not self.highlighted
        d = {
            "wheat1": ("PaleTurquoise1", "empty_tile_2_selected"),
            "gray": ("PaleTurquoise3", "empty_tile_1_selected"),
        }

        if self.highlighted:
            self.set_bg(d[self.base_colour][0])
            if not self.has_piece:
                self.set_img(self.images[d[self.base_colour][1]])
        else:
            self.set_bg()
            if not self.has_piece:
                self.set_img()

    def set_bg(self, bg=None):
        if not bg:
            bg = self.base_colour
        self.button.configure(bg=bg, activebackground=bg)

    def set_img(self, image=None):
        if not image:
            image = self.base_image
        self.button.configure(image=image)

    def reset(self):
        self.selected = False
        self.highlighted = False
        self.set_bg()
        self.set_piece()

    def select_as_first_tile(self):
        self.selected = True
        self.set_bg("magenta")


def load_photo_images():
    photo_images = dict()
    for image in image_names:
        file_name = f"piece_images/{image}.png"
        loaded_image = Image.open(file_name)
        resized_image = loaded_image.resize((50, 50), Image.Resampling.LANCZOS)
        photo_images[image] = ImageTk.PhotoImage(resized_image)
    return photo_images


def create_tiles(game):
    photo_images = load_photo_images()
    for row in range(1, 9):
        for letter in Letter:
            column = letter.name.lower()
            location = f"{column}{row}"
            game.tiles[location] = Tile(row, column, game=game, images=photo_images)
