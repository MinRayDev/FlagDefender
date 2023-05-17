import os
import threading
import time

from pygame import mixer


def play(song_file):
    from util.instance import get_client
    mixer.music.set_volume((get_client().volume/100))
    mixer.music.load(os.path.join("./resources/audio", song_file))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def play_sound(song_file):
    threading.Thread(target=play, args=(song_file,), daemon=True).start()
