# imports


# @deyan chatgpt said the arms are called following:

# Front Right (FR)

# Front Left (FL)

# Rear Right (RR)

# Rear Left (RL)

import time


class motor():
    def __init__(self):
        self.yaw = 0 # Get Yaw from Sensor later @deyan
        self.pitch = 0 # Get Pitch from Sensor later @deyan
        self.last_print = 0

    def _rate_limited_print(self, message):
        current_time = time.time()
        if current_time - self.last_print >= 1:
            print(message)
            self.last_print = current_time

    def set_FR(self, strength: float):
        self._rate_limited_print(f"Front Right Motor set to {strength} strength.")

    def set_FL(self, strength: float):
        self._rate_limited_print(f"Front Left Motor set to {strength} strength.")

    def set_RR(self, strength: float):
        self._rate_limited_print(f"Rear Right Motor set to {strength} strength.")

    def set_RL(self, strength: float):
        self._rate_limited_print(f"Rear Left Motor set to {strength} strength.")

    def all_motors(self, strength: float):
        self._rate_limited_print(f"All Motors set to {strength} strength.")

    def set_yaw(self, yaw: float):
        self._rate_limited_print(f"Yaw set to {yaw} degrees.")
    