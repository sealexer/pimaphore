from threading import Thread
from time import sleep, time
from buttons import Button
from lamps import Lamp
from mode import SemaphoreMode


WHITE_DELAY = 1
RED_DELAY = 0.6
SEMAPHORE_MODE_SWITCH_THRESHOLD = 2     # seconds
SEMAPHORE_MODE_SWITCH_BLINKING_PRE_ON_DELAY = 0.1
SEMAPHORE_MODE_SWITCH_BLINKING_POST_ON_DELAY = 0.1


class SoundPlayerController(Thread):
    def __init__(self, sound_player, event_start, event_stop):
        Thread.__init__(self)
        self.sound_player = sound_player
        self.event_start = event_start
        self.event_stop = event_stop

    def run(self):
        # self.sound_player.start()
        # self.sound_player.pause()
        while True:
            self.event_start.wait()
            self.sound_player.start()
            # self.sound_player.resume()
            self.event_stop.wait()
            self.sound_player.stop()
            # self.sound_player.pause()


class WhiteLampController(Thread):
    def __init__(self, pin, event_stop, semaphore_mode):
        Thread.__init__(self)
        self.event_stop = event_stop
        self.semaphore_mode = semaphore_mode
        self.lamp = Lamp(pin)
        self.lamp.off()

    def run(self):
        while True:
            self.event_stop.wait()
            while self.event_stop.isSet():
                if self.semaphore_mode.value == SemaphoreMode.RED_AND_WHITE:
                    self.lamp.invert_state()
                sleep(WHITE_DELAY)
            self.lamp.off()

    def blink_twice(self):
        initial_state_was_on = self.lamp.is_on()
        self.lamp.off()
        for i in range(2):
            sleep(SEMAPHORE_MODE_SWITCH_BLINKING_PRE_ON_DELAY)
            self.lamp.on()
            sleep(SEMAPHORE_MODE_SWITCH_BLINKING_POST_ON_DELAY)
            self.lamp.off()
        if initial_state_was_on:
            self.lamp.on()


class RedLampsController(Thread):
    def __init__(self, pin_left, pin_right, event_start):
        Thread.__init__(self)
        self.event_start = event_start
        self.lamp_left = Lamp(pin_left)
        self.lamp_right = Lamp(pin_right)
        self.lamp_left.off()
        self.lamp_right.off()

    def run(self):
        while True:
            self.event_start.wait()
            self.lamp_left.on()
            self.lamp_right.off()
            sleep(RED_DELAY)
            while self.event_start.isSet():
                self.lamp_left.invert_state()
                self.lamp_right.invert_state()
                # print(str(self.lamp_left) + "\t" + str(self.lamp_right))
                sleep(RED_DELAY)
            self.lamp_right.off()
            self.lamp_left.off()


class ButtonController(Thread):
    def __init__(self, button_pin, event_start, event_stop, white_lamp_controller, semaphore_mode):
        Thread.__init__(self)
        self.button = Button(button_pin)
        self.event_start = event_start
        self.event_stop = event_stop
        self.white_lamp_controller = white_lamp_controller
        self.semaphore_mode = semaphore_mode

    def invert_start_stop_state(self):
        if self.event_start.isSet():
            self.event_start.clear()
            self.event_stop.set()
        else:
            self.event_start.set()
            self.event_stop.clear()

    def run(self):
        while True:
            duration = self.button.wait_for_pressure()
            # print("Pressure detected")
            if duration >= SEMAPHORE_MODE_SWITCH_THRESHOLD:
                self.semaphore_mode.invert()
                self.white_lamp_controller.blink_twice()
                # print("Semaphore mode inverted")
            else:
                self.invert_start_stop_state()
