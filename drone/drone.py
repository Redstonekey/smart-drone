from motor import motor
from gps import GPS
from colorama import init, Fore, Style
init()

class drone():
    def __init__(self, name: str, model: str, max_speed: float, battery_life: float, positionx: float, positiony: float, positionz: float, hover_speed: float):
        self.name = name
        self.battery_life = battery_life
        self.position = GPS.get_position()
        self.positionx = GPS.get_x()
        self.positiony = GPS.get_y()
        self.positionz = GPS.get_z()
        self.start_postionx = positionx
        self.start_postiony = positiony
        self.start_postionz = positionz
        self.start_postion = positionx, positiony, positionz
        self.hover_speed = hover_speed
        self.armed = False
        self.landed = False
        self.ground_distance = 0 # Get from Camera later @deyan


    def arm(self):
        motor.all_motors(self.hover_speed - 10)
        self.armed = True
        self.start_postionx = self.positionx
        self.start_postiony = self.positiony
        self.start_postionz = self.positionz
        self.start_postion = self.position
        print(f"{self.name} is armed.")
    
    def disarm(self):
        if self.armed == False:
            print(f"{Fore.RED}{self.name} is already disarmed.{Style.RESET_ALL}")
            return
        elif self.landed == False:
            print(f"{Fore.RED}{self.name} must be landed before disarming.{Style.RESET_ALL}")
            return
        motor.all_motors(0)
        self.armed = False
        print(f"{Fore.GREEN}{self.name} is disarmed.{Style.RESET_ALL}")


    def take_off(self, height: float = 5):
        if self.armed == False:
            print(f"{Fore.RED}{self.name} must be armed before take off.{Style.RESET_ALL}")
            return
        print(f"{Fore.YELLOW}{self.name} is taking off to {height} meters.{Style.RESET_ALL}")
        while self.positiony < self.start_postiony + height:
            motor.all_motors(100)
        motor.all_motors(self.hover_speed)
        print(f"{Fore.GREEN}{self.name} is in the air at {height}m.{Style.RESET_ALL}")

        
    def land(self):
        self.landed = True
        print(f"{Fore.YELLOW}{self.name} is landing.{Style.RESET_ALL}")
        while self.ground_distance > 1:
            motor.all_motors(self.hover_speed - 10)
        if self.ground_distance < 1:
            motor.all_motors(self.hover_speed - 20)
            print(f"{Fore.GREEN}{self.name} has landed.{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}({self.name} still needs to disarm.){Style.RESET_ALL}")
        

    def fly(self, x: float, y: float, z: float):
        """Fly to the specified coordinates (x, y, z)"""
        # Not working yet
        print(f"{self.name} is flying to coordinates ({x}, {y}, {z}).")