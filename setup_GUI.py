from constants import Letter
import tkinter as tk
from tkinter import messagebox


def sequence(move_list):
    print(move_list)
    move_list.clear()


def create_tkinter_window():
    root = tk.Tk()
    root.configure(background="light goldenrod")

    player = tk.StringVar(root, value="white")
    move_number = tk.IntVar(root, value=1)
    chessboard = make_frame(root, 0, 1, (5, 5, 5, 5))

    info_frame = make_frame(root, 0, 2, (10, 10, 10, 10))
    left_labels = make_frame(root, 0, 0)
    bottom_labels = make_frame(root, 1, 1)

    create_main_window(root, left_labels, bottom_labels)

    make_label(info_frame, 0, "move:", font="9")
    make_label(info_frame, 1, move_number, font="9", mode="variable")
    make_label(info_frame, 2, "player turn:", font="15", padding=(0, 0, 50, 0))
    make_label(info_frame, 3, player, font="15", mode="variable", padding=(0, 0, 0, 50))
    draw_button = tk.Button(
        info_frame,
        text="request draw",
        width=12,
        height=2,
        background="dark goldenrod",
        command=lambda: request_draw(root, player.get()),
    )
    draw_button.grid(column=0, row=4)
    draw_button = tk.Button(
        info_frame,
        text="get raw move \nsequence",
        command=sequence,
        width=12,
        height=2,
        background="dark goldenrod",
    )
    draw_button.grid(column=0, row=6)

    return root, chessboard, player, move_number


def make_label(
    frame, row, variable, font="9", mode="normal", padding=(0, 0, 0, 0), column=0
):
    label = ""
    if mode == "normal":
        label = tk.Label(frame, text=variable, font=("Segoe UI", font))
    elif mode == "variable":
        label = tk.Label(frame, textvariable=variable, font=("Segoe UI", font))
    label.grid(
        row=row,
        column=column,
        padx=(padding[0], padding[1]),
        pady=(padding[2], padding[3]),
    )
    label.configure(background="goldenrod")
    return label


def make_frame(master, row, column, padding=(0, 0, 0, 0)):
    f1 = tk.Frame(master, background="goldenrod")
    f1.grid(row=row, column=column, padx=(padding[0:2]), pady=(padding[2:4]))
    return f1


def create_main_window(root, left_labels, bottom_labels):
    root.title("Chess")
    root.geometry("600x600")

    for j in range(8, 0, -1):
        make_label(left_labels, 8 - j, j, padding=(5, 5, 18, 18))

    for j0, j in enumerate(Letter):
        make_label(bottom_labels, 0, j.name.lower(), padding=(20, 20, 0, 0), column=j0)


def request_draw(frame, player_colour):
    response_is_yes = messagebox.askyesno(
        "draw offered", f"player {player_colour} has offered a draw, do you accept?"
    )
    if response_is_yes:
        messagebox.showinfo(
            "game over", "both players have accepted the game is a draw"
        )
        frame.destroy()
