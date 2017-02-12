class SemaphoreMode:
    RED_ONLY = 1
    RED_AND_WHITE = 2

    def __init__(self):
        self.value = self.RED_AND_WHITE

    def invert(self):
        if self.value == self.RED_ONLY:
            self.value = self.RED_AND_WHITE
        elif self.value == self.RED_AND_WHITE:
            self.value = self.RED_ONLY
