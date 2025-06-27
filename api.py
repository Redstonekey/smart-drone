from flask import Flask, jsonify, render_template
from smart_drone import Drone, API
app = Flask(__name__)

@app.route('/api/live')
def api_live_update():
    lat, long = API.get.gps()
    flight_time = API.get.flight_time()
    battery = API.get.battery()
    altitude = API.get.altitude()
    speed = API.get.speed()
    remaining_time = API.get.remaining_time()
    gps_status = API.get.status.gps()
    signal_status = API.get.status.signal()
    motors_status = API.get.status.motors()
    sensors_status = API.get.status.sensors()
    return jsonify({
        "lat": lat,
        "long": long,
        "flight_time": flight_time,
        "battery": battery,
        "altitude": altitude,
        "speed": speed,
        "remaining_time": remaining_time,
        "gps_status": gps_status,
        "signal_status": signal_status,
        "motors_status": motors_status,
        "sensors_status": sensors_status
    })
app.run()