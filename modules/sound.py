import os
from playsound import playsound
import threading


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADD_SOUND = os.path.join(BASE_DIR, "assets", "sounds", "add.wav")
SUCCESS_SOUND = os.path.join(BASE_DIR, "assets", "sounds", "success.wav")


def play_add():

    threading.Thread(
        target=lambda: playsound(ADD_SOUND),
        daemon=True
    ).start()


def play_success():

    threading.Thread(
        target=lambda: playsound(SUCCESS_SOUND),
        daemon=True
    ).start()
