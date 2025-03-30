# imports


# @deyan chatgpt said the arms are called following:

# Front Right (FR)

# Front Left (FL)

# Rear Right (RR)

# Rear Left (RL)

class motor():
    def __init__(self, motor_id: str, motor_type: str, max_rpm: float, max_thrust: float):
        self.motor_id = motor_id
        self.motor_type = motor_type
        self.max_rpm = max_rpm
        self.max_thrust = max_thrust
    def set_FR(self, strength: float):
        print(f"Front Right Motor set to {strength} strength.")
    def set_FL(self, strength: float):
        print(f"Front Left Motor set to {strength} strength.")
    def set_RR(self, strength: float):
        print(f"Rear Right Motor set to {strength} strength.")
    def set_RL(self, strength: float):
        print(f"Rear Left Motor set to {strength} strength.")
    def all_motors(self, strength: float):
        print(f"All Motors set to {strength} strength.")
    