import time
from RPi import GPIO

PRESSURE_LENGTH_OBSERVATION_MAX_TIMEOUT = 2.5  # seconds
PRESSURE_CHECK_PERIOD = 0.05                   # seconds
LEVEL_LOW = 0


class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __str__(self):
        return str(self.pin) + " : " + str(self.is_pressed())

    def is_pressed(self):
        return GPIO.input(self.pin) == LEVEL_LOW

    def wait_for_pressure(self):
        """ Blocks until button is pressed. Returns the pressure duration in seconds """
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)
        for i in range(int(PRESSURE_LENGTH_OBSERVATION_MAX_TIMEOUT / PRESSURE_CHECK_PERIOD)):
            if GPIO.input(self.pin):
                break
            time.sleep(PRESSURE_CHECK_PERIOD)
        duration = i * PRESSURE_CHECK_PERIOD    # TODO: refactor this
        return duration


class PressureResult:
    SUCCESS = 1
    FAILURE = 0

    def __init__(self, status, duration):
        self.status = status
        self.duration = duration
