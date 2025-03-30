from .motor import motor
from .gps import GPS
from colorama import init, Fore, Style
init()
motor = motor()
class drone():
    def __init__(self, name: float, hover_speed: float):
        self.name = name
        self.gps = GPS()  # Create GPS instance
        self.position = self.gps.get_position()  # Use instance method
        self.positionx = self.gps.get_x()  # Use instance method
        self.positiony = self.gps.get_y()  # Use instance method
        self.positionz = self.gps.get_z()  # Use instance method
        self.start_postionx = self.positionx
        self.start_postiony = self.positiony
        self.start_postionz = self.positionz
        self.start_postion = (self.positionx, self.positiony, self.positionz)
        self.hover_speed = hover_speed
        self.armed = False
        self.landed = True  # Start as landed
        self.ground_distance = 10 # Get from Camera later @deyan


    def arm(self):
        motor.all_motors(self.hover_speed - 10)
        self.armed = True
        self.start_postionx = self.positionx
        self.start_postiony = self.positiony
        self.start_postionz = self.positionz
        self.start_postion = self.position
        print(f"{Fore.GREEN}{self.name} is armed.{Style.RESET_ALL}")
    
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

    # real land function        
    # def land(self):
    #     self.landed = True
    #     print(f"{Fore.YELLOW}{self.name} is landing.{Style.RESET_ALL}")
    #     while self.ground_distance > 1:
    #         motor.all_motors(self.hover_speed - 10)
    #     if self.ground_distance < 1:
    #         motor.all_motors(self.hover_speed - 20)
    #         print(f"{Fore.GREEN}{self.name} has landed.{Style.RESET_ALL}")
    #         print(f"{Fore.LIGHTBLACK_EX}({self.name} still needs to disarm.){Style.RESET_ALL}")


    #fake land function for testing purposes
    def land(self):
        self.landed = True
        print(f"{Fore.YELLOW}{self.name} is landing.{Style.RESET_ALL}")
        while self.ground_distance > 1:
            motor.all_motors(self.hover_speed - 10)
            self.ground_distance -= 1
            print(f"{Fore.YELLOW}{self.name} is descending. Current ground distance: {self.ground_distance}m.{Style.RESET_ALL}")
        if self.ground_distance < 1:
            motor.all_motors(self.hover_speed - 20)
            print(f"{Fore.GREEN}{self.name} has landed.{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}({self.name} still needs to disarm.){Style.RESET_ALL}")
            

    def fly(self, x: float, y: float, z: float):
        """Fly to the specified coordinates (x, y, z)"""
        # Not working yet
        print(f"{self.name} is flying to coordinates ({x}, {y}, {z}).")