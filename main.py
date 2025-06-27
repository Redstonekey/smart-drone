from smart_drone import Drone, GPS
from flask import Flask, request, jsonify

app = Flask(__name__)
drone = Drone('drone', 5)
gps = GPS(simulation_duration=600, update_interval=10)

def drone_command():
    drone.arm()
    drone.fake_take_off(5)
    drone.fly.forward(drone, 10)
    # drone.fly.right(drone, 10)
    # drone.fly.left(drone, 10)
    # drone.fly.backward(drone, 10)
    # drone.fly.right_forward(drone, 10)
    # drone.fly.left_backward(drone, 10)
    # drone.fly.right_backward(drone, 10)
    # drone.fly.left_forward(drone, 10)
    drone.fake_land()
    drone.disarm()
@app.route('/api/gps')
def get_gps():
    latitude, longitude, altitude = gps.get_position()
    return {
        'latitude': latitude,
        'longitude': longitude,
        'altitude': altitude
    }

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        drone_command()