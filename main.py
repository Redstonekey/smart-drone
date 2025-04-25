from smart_drone import Drone

drone = Drone('drone', 5)

drone.arm()
drone.fake_take_off(5)
# drone.fly.forward(drone, 10)
# drone.fly.right(drone, 10)
# drone.fly.left(drone, 10)
# drone.fly.backward(drone, 10)
# drone.fly.right_forward(drone, 10)
# drone.fly.left_backward(drone, 10)
# drone.fly.right_backward(drone, 10)
# drone.fly.left_forward(drone, 10)
drone.fake_land()
drone.disarm()
