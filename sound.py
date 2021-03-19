import os


def play_sound():
    os.system("aplay -q sound1.wav &")


def play_sound2():
    os.system("aplay -q sound2.wav &")
