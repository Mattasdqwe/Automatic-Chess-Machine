import RPi.GPIO as GPIO
import time


class Electromagnet:

    def __init__(self, control_pin):
        self.control_pin = control_pin
        self.off_delay = 2  # seconds required for electromagnet to be fully off

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.control_pin, GPIO.OUT, initial=False)

    def on(self):
        GPIO.output(self.control_pin, True)

    def off(self):
        GPIO.output(self.control_pin, False)
        time.sleep(self.off_delay)
