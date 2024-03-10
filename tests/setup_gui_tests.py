import tkinter as tk
from .. import setup_GUI
import unittest


class CreateTkinterWindowTests(unittest.TestCase):
    def setUp(self):
        values = setup_GUI.create_tkinter_window()
        self.root = values[0]
        self.chessboard = values[1]
        self.player = values[2]
        self.move_number = values[3]
        self.print_move_on = values[4]

    def test_chessboard_in_root_window(self):
        self.assertIs(self.chessboard.master, self.root)

    def test_start_player_equals_white(self):
        self.assertEqual(self.player.get(), "white")

    def test_move_number_equals_1(self):
        self.assertEqual(self.move_number.get(), 1)

    def tearDown(self):
        self.root.destroy()


class AdditionalGuiTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def test_make_label(self):
        text_variable = tk.StringVar(self.root, value="test")
        label = setup_GUI.make_label(self.root, 0, text_variable)
        self.assertIs(label.master, self.root)
        label.destroy()

    def test_make_frame(self):
        frame = setup_GUI.make_frame(self.root, 0, 0)
        self.assertIs(frame.master, self.root)

    def test_create_main_window(self):
        frame1 = tk.Frame(self.root)
        frame2 = tk.Frame(self.root)
        setup_GUI.create_main_window(self.root, frame1, frame2)
        self.root.update()
        self.assertEqual(self.root.winfo_geometry()[:7], "600x600")
        frame1.destroy()
        frame2.destroy()

    def tearDown(self):
        self.root.destroy()


if __name__ == "__setup_gui_tests__":
    unittest.main()