from motor import motor

class drone():
    def __init__(self, name: str, model: str, max_speed: float, battery_life: float, positionx: float, positiony: float, positionz: float):
        self.name = name
        self.model = model
        self.max_speed = max_speed
        self.battery_life = battery_life
        self.position = positionx, positiony, positionz

    def arm(self):
        print(f"{self.name} is armed.")
    def disarm(self):
        print(f"{self.name} is disarmed.")
    def take_off(self):
        motor.all_motors(100)
        print(f"{self.name} is taking off.")
    def land(self):
        print(f"{self.name} is landing.")
    def fly(self, x: float, y: float, z: float):

        print(f"{self.name} is flying to coordinates ({x}, {y}, {z}).")