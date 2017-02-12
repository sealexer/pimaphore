from RPi import GPIO

LEVEL_HIGH = 1
LEVEL_LOW = 0


class Lamp:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def __str__(self):
        return str(self.pin) + " : " + str(self.is_on())

    def on(self):
        GPIO.output(self.pin, LEVEL_HIGH)

    def off(self):
        GPIO.output(self.pin, LEVEL_LOW)

    def is_on(self):
        return GPIO.input(self.pin) == LEVEL_HIGH

    def invert_state(self):
        if self.is_on():
            self.off()
        else:
            self.on()
