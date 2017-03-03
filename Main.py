import signal
from threading import Event

from RPi import GPIO

from controllers import SoundPlayerController, WhiteLampController, RedLampsController, ButtonController
from mode import SemaphoreMode
from soundplayers import RotatingSoundPlayer

PIN_WHITE = 23
PIN_RED_LEFT = 27
PIN_RED_RIGHT = 22
PIN_BUTTON = 17

SOUND_PATH = "/D/Projects/Idea/Pimaphore/resources"
SOUND_FILES = ["pereezd-1.mp3", "pereezd-2.mp3", "pereezd-3.mp3", "pereezd-4.mp3"]


class Semaphore:
    def __init__(self, sound_files):
        self.event_stop = Event()
        self.event_start = Event()
        # self.sound_files = sound_files
        self.sound_player = RotatingSoundPlayer(sound_files)
        self.semaphore_mode = SemaphoreMode()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.add_event_detect(PIN_BUTTON, GPIO.FALLING, callback=lambda x: self.button_pressed(), bouncetime=1000)
        self.sound_player.init()
        self.event_stop.set()

    def start(self):
        # print("Creating and starting threads")
        t1 = RedLampsController(PIN_RED_LEFT, PIN_RED_RIGHT, self.event_start)
        t2 = SoundPlayerController(self.sound_player, self.event_start, self.event_stop)
        t3 = WhiteLampController(PIN_WHITE, self.event_stop, self.semaphore_mode)
        t4 = ButtonController(PIN_BUTTON, self.event_start, self.event_stop, t3, self.semaphore_mode)
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t4.daemon = True
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        # print("Threads started")

    def cleanup(self):
        GPIO.cleanup()
        self.sound_player.shutdown()
        # TODO Add graceful controllers shutdown


def main():
    semaphore = Semaphore([SOUND_PATH + "/" + sound_file for sound_file in SOUND_FILES])
    semaphore.setup()
    semaphore.start()
    try:
        signal.pause()
    finally:
        semaphore.cleanup()


if __name__ == '__main__':
    main()
