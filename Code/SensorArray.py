import smbus
import time


class SensorArray:

    def __init__(self, address):
        self.address = address

        self.bus = smbus.SMBus(1)  # open I2C bus 1
        self.bus.write_byte_data(self.address, 0x00, 0xFF)  # A bank inputs
        self.bus.write_byte_data(self.address, 0x01, 0xFF)  # B bank inputs
        self.bus.write_byte_data(self.address, 0x0C, 0xFF)  # A bank pull-up resistors
        self.bus.write_byte_data(self.address, 0x0D, 0xFF)  # B bank pull-up resistors

    # Returns an array of the form [A Bank 0-7, B Bank 0-7] where array elements are either True or False
    def detect(self):

        detection_array = [False for _ in range(16)]
        a_bank = self.bus.read_byte_data(self.address, 0x12)  # Read bank A
        b_bank = self.bus.read_byte_data(self.address, 0x13)  # Read bank B

        for i in range(8):
            if not a_bank & 2**i:
                detection_array[i] = True
            if not b_bank & 2**i:
                detection_array[i+8] = True

        return detection_array
