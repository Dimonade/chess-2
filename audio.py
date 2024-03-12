import os
import platform

if platform.system() == "Windows":
    import winsound
    from winsound import PlaySound


def get_sound(sound_number):
    if platform.system() == "Windows":
        d = {1: "next_move", 2: "piece_captured", 3: "check"}
        sound = os.path.dirname(__file__) + f"\\sounds\\{d[sound_number]}.wav"
        PlaySound(sound, winsound.SND_ASYNC)
