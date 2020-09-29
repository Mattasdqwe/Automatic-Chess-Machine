import RPi.GPIO as GPIO
import time


class Motor:

    # step_pin: the pin number for stepping
    # dir_pin: the pin number for direction
    # ls_pin: the pin number for the limit switch
    # step_limit: maximum range in the positive direction
    def __init__(self, step_pin, dir_pin, ls_pin, step_limit):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.ls_pin = ls_pin
        self.step_limit = step_limit

        self.step_count = 0
        self.homed = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup([self.step_pin, self.dir_pin], GPIO.OUT, initial=False)
        GPIO.setup(self.ls_pin, GPIO.IN)

    # Private function
    # Steps in a direction regardless of other factors
    # delay: the delay between steps
    def _step(self, delay):
        GPIO.output(self.step_pin, True)
        GPIO.output(self.step_pin, False)
        time.sleep(delay)

    #
    def step(self, steps, direction, speed):
        if direction not in [-1, 1]:
            raise ValueError("Invalid direction")
        final_position = self.step_count + direction*steps
        if final_position > self.step_limit or final_position < 0:
            raise ValueError("Out of bounds")
        if not self.homed:
            raise TypeError("Motor not homed")

        if speed <= 0:
            return

        delay = 1/speed
        GPIO.output(self.dir_pin, direction > 0)
        for k in range(steps):
            self._step(delay)
            self.step_count += direction

    def home(self):
        delay = 0.005
        short_delay = 0.03
        GPIO.output(self.dir_pin, False)  # move towards 0

        for steps in range(self.step_limit):
            if steps % 5 == 0:
                ls_reached = not GPIO.input(self.ls_pin)
                if ls_reached:
                    GPIO.output(self.dir_pin, True)
                    while not GPIO.input(self.ls_pin):
                        self._step(short_delay)
                    GPIO.output(self.dir_pin, False)
                    while GPIO.input(self.ls_pin):
                        self._step(short_delay)
                    self.homed = True
                    self.step_count = 0
                    return
            self._step(delay)

        raise SystemError("Machine unable to home")

    def getStepCount(self):
        return self.step_count


