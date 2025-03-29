class motor():
    def __init__(self, motor_id: str, motor_type: str, max_rpm: float, max_thrust: float):
        self.motor_id = motor_id
        self.motor_type = motor_type
        self.max_rpm = max_rpm
        self.max_thrust = max_thrust
    def left_upper_motor(self, strength: float):
        print(f"Left upper Motor set to {strength} strength.")
    def right_lower_motor(self, strength: float):
        print(f"Right lower Motor set to {strength} strength.")
    def left_lower_motor(self, strength: float):
        print(f"Left lower Motor set to {strength} strength.")
    def right_upper_motor(self, strength: float):
        print(f"Right upper Motor set to {strength} strength.")
    def all_motors(self, strength: float):
        print(f"All Motors set to {strength} strength.")
    