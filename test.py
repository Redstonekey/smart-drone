from smart_drone import Drone, GPS # Assuming GPS is in smart_drone module
from flask import Flask, request
import time # Import time if not already imported

app = Flask(__name__)
drone = Drone('drone', 5)
gps = GPS(simulation_duration=600, update_interval=10) # Instantiate GPS, simulation starts in thread

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Attempt to stop the GPS simulation thread when the Flask app stops
        # This might not be perfectly reliable with Flask's development server
        # but is good practice for cleaner shutdown.
        print("Stopping GPS simulation...")
        gps.stop_simulation()
        # You might add a small sleep here to allow the thread to finish
        # time.sleep(1)
        print("GPS simulation stopped.")

