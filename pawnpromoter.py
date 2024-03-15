import tkinter as tk
from pieces import Queen, Rook, Bishop, Knight


class PawnPromoter:
    def __init__(self, piece, game):
        self.piece = piece
        self.game = game
        self.win = None
        self.promotion_choice = None
        self.submission_made = None

    def attempt_promote(self) -> tuple:
        row = self.piece.location[1]

        is_pawn = self.piece.type == "pawn"
        is_promotion_row = row in {"1", "8"}
        is_promotion = is_pawn and is_promotion_row

        choice_letter = ""
        if is_promotion:
            promotion_choice = self.complete_promote()
            choice_letter = promotion_choice[0].upper()

        return is_promotion, choice_letter

    def complete_promote(self):
        win = tk.Toplevel()
        self.win = win
        win.title("Promotion")
        promotion_choice = tk.StringVar(master=win, value="Q")
        self.promotion_choice = promotion_choice
        submission_made = tk.BooleanVar(master=win, value=False)
        self.submission_made = submission_made
        message_label = tk.Label(master=win, text="Please choose promotion")
        message_label.grid(row=0, column=0)

        mrb = self.make_radio_button
        mrb("Queen", "Q", 1)
        mrb("Rook", "R", 2)
        mrb("Bishop", "B", 3)
        mrb("Knight", "K", 4)

        self.make_submit_button()

        win.waitvar(submission_made)
        win.destroy()
        return promotion_choice.get()

    def make_submit_button(self):
        submit_button = tk.Button(
            master=self.win,
            text="select",
            command=lambda: self.get_choice(),
        )
        submit_button.grid(row=5, column=0)

    def make_radio_button(self, text, value, row):
        radio_button = tk.Radiobutton(
            master=self.win, text=text, variable=self.promotion_choice, value=value
        )
        radio_button.grid(row=row, column=0)

    def get_choice(self):
        piece = self.piece
        x1, x2 = piece.colour, piece.location
        game = self.game
        pieces = self.game.pieces
        d = {
            "q": Queen(x1, x2, game),
            "k": Knight(x1, x2, game),
            "b": Bishop(x1, x2, game),
            "r": Rook(x1, x2, game),
        }
        pieces[piece.location] = d[self.promotion_choice.get()[0].lower()]
        self.submission_made.set(True)
