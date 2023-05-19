import os
import threading
import time

from pygame import mixer


def play(sound_file: str) -> None:
    """Plays a sound.

        :param sound_file: The song file to play.
        :type sound_file: str.
    """
    from util.instance import get_client
    mixer.music.set_volume((get_client().volume/100))
    mixer.music.load(os.path.join("./resources/audio", sound_file))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def play_sound(sound_file: str) -> None:
    """Plays a sound.

        Plays a sound in a new thread. A thread is used to avoid issue when playing multiple sounds at the same time.
        A daemon thread is used to avoid the thread to prevent the program from closing.

        :param sound_file: The song file to play.
        :type sound_file: str.

    """
    threading.Thread(target=play, args=(sound_file,), daemon=True).start()
