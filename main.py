from drone.drone import drone
import time

drone = drone('drone', 5)

drone.arm()
drone.land()
drone.disarm()
